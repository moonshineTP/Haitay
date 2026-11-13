// Haitay speedcubing timer - Wokwi simulation on ESP32-S3.
// Pads are pushbuttons (touched = pressed), the FRAM log is a RAM ring with the same layout
// as the real device, and every committed record is printed as "REC <32 hex chars>".
//
// Record layout, 16 bytes little-endian: seq u32 | time_ms u32 | ts u32 | session u8 | flags u8 | crc16 u16
// CRC-16/CCITT-FALSE (poly 0x1021, init 0xFFFF) over the first 14 bytes.

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <RTClib.h>
#include "esp_timer.h"

// ---- pins and constants ----------------------------------------------------
const uint8_t PIN_PAD_L = 4, PIN_PAD_R = 5;
const uint8_t PIN_SELECT = 15, PIN_SESSION = 16, PIN_SYNC = 17;
const uint8_t PIN_SDA = 8, PIN_SCL = 9;

const uint32_t ARM_MS = 1500;      // both pads held this long before READY
const uint8_t DEBOUNCE = 3;        // stable 1 kHz samples that confirm an edge
const uint16_t SLOTS = 512;        // FRAM ring: 8 KB / 16 B
const uint32_t DNF_T = 0xFFFFFFFEu, UNDEF = 0xFFFFFFFFu;
const uint8_t BOOT_ID = 1;

// Types used in function signatures sit above the first function, because the Arduino
// builder inserts its generated prototypes there.
enum State { IDLE, ARMING, READY, RUNNING, STOPPED };
struct Sample { uint32_t us; uint8_t bits; };
struct Button { uint8_t pin; bool down; uint32_t changedMs; };

// flags
const uint8_t PEN_OK = 0, PEN_PLUS2 = 1, PEN_DNF = 2;
const uint8_t F_TIME_UNSET = 1 << 2;

// ---- CRC and record packing -------------------------------------------------
uint16_t crc16(const uint8_t *d, size_t n, uint16_t crc = 0xFFFF) {
  for (size_t i = 0; i < n; i++) {
    crc ^= (uint16_t)d[i] << 8;
    for (int b = 0; b < 8; b++) crc = (crc & 0x8000) ? (uint16_t)((crc << 1) ^ 0x1021) : (uint16_t)(crc << 1);
  }
  return crc;
}

void put32(uint8_t *p, uint32_t v) { for (int i = 0; i < 4; i++) p[i] = (v >> (8 * i)) & 0xFF; }
uint32_t get32(const uint8_t *p) { return p[0] | (p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24); }

void packRecord(uint8_t out[16], uint32_t seq, uint32_t timeMs, uint32_t ts, uint8_t session, uint8_t flags) {
  put32(out, seq);
  put32(out + 4, timeMs);
  put32(out + 8, ts);
  out[12] = session;
  out[13] = flags;
  uint16_t c = crc16(out, 14);
  out[14] = c & 0xFF;
  out[15] = c >> 8;
}

// ---- RAM ring standing in for the FRAM log ----------------------------------
uint8_t ring[SLOTS][16];
uint32_t head = 0;     // last committed seq
uint32_t lastAck = 0;  // highest seq already dumped on a sync (stands in for the PC ACK)
uint8_t session = 1;

uint8_t *slotOf(uint32_t seq) { return ring[(seq - 1) % SLOTS]; }

// Log is full when the next slot still holds a record that was never synced.
bool ringFull() {
  uint32_t old = get32(slotOf(head + 1));
  return old != 0 && old > lastAck;
}

void printRec(const uint8_t *r) {
  char line[40] = "REC ";
  for (int i = 0; i < 16; i++) snprintf(line + 4 + 2 * i, 3, "%02x", r[i]);
  Serial.println(line);
}

// ---- statistics (csTimer style, same as haitay/stats.py) --------------------
uint32_t effectiveOf(const uint8_t *r) {
  uint8_t pen = r[13] & 3;
  if (pen == PEN_DNF) return DNF_T;
  return get32(r + 4) + (pen == PEN_PLUS2 ? 2000 : 0);
}

// Returns the average in ms (centisecond resolution), DNF_T, or UNDEF when fewer than n solves.
uint32_t averageOf(uint8_t n) {
  if (head < n) return UNDEF;
  uint32_t w[100];
  for (uint8_t i = 0; i < n; i++) w[i] = effectiveOf(slotOf(head - n + 1 + i));
  for (uint8_t i = 1; i < n; i++) {  // insertion sort, DNF_T sorts last
    uint32_t v = w[i];
    int j = i - 1;
    while (j >= 0 && w[j] > v) { w[j + 1] = w[j]; j--; }
    w[j + 1] = v;
  }
  uint8_t cut = (n + 19) / 20;  // ceil(5% n)
  uint8_t k = n - 2 * cut;
  if (w[n - cut - 1] == DNF_T) return DNF_T;
  uint64_t sum = 0;
  for (uint8_t i = cut; i < n - cut; i++) sum += w[i];
  uint64_t den = 10ull * k, q = sum / den, r = sum % den;
  if (2 * r > den || (2 * r == den && (q & 1))) q++;  // round half to even, like Python round()
  return (uint32_t)(q * 10);
}

void fmtTime(char *buf, size_t n, uint32_t ms) {
  if (ms == UNDEF) { snprintf(buf, n, "-"); return; }
  if (ms == DNF_T) { snprintf(buf, n, "DNF"); return; }
  uint32_t cs = ms / 10, s = cs / 100;
  if (s >= 60) snprintf(buf, n, "%lu:%02lu.%02lu", (unsigned long)(s / 60), (unsigned long)(s % 60), (unsigned long)(cs % 100));
  else snprintf(buf, n, "%lu.%02lu", (unsigned long)s, (unsigned long)(cs % 100));
}

// ---- 1 kHz pad sampling ------------------------------------------------------
// An esp_timer callback reads both pads every 1 ms with its own micros() stamp and queues the
// sample, so a slow OLED refresh in loop() only delays processing, never the timestamps.
const uint16_t QSIZE = 256;
Sample queue[QSIZE];
volatile uint16_t qHead = 0, qTail = 0;

// Scripted test mode: the browser cannot hold two keys at once, so AUTOPLAY feeds synthetic
// pad samples of known durations. Real pad buttons still work (OR-ed in), and so do the
// Chon / Session / Dong bo buttons. Comment the define out for fully manual play.
#define AUTOPLAY
#ifdef AUTOPLAY
const uint32_t AP_SOLVE_MS[] = {2870, 3240, 2530, 3610, 3050, 2420};  // short, so the run fits a slow host
const uint8_t AP_N = sizeof AP_SOLVE_MS / sizeof AP_SOLVE_MS[0];
const uint32_t AP_T0 = 500, AP_ARM = 1600, AP_STOP = 150, AP_GAP = 150;

// Pad bits at t ms after boot: both pads for AP_ARM, left only while solving, both to stop,
// then none. The next solve's both-press commits the previous one, as on the real device.
uint8_t apBits(uint32_t t) {
  if (t < AP_T0) return 0;
  t -= AP_T0;
  for (uint8_t i = 0; i < AP_N; i++) {
    uint32_t len = AP_ARM + AP_SOLVE_MS[i] + AP_STOP + AP_GAP;
    if (t < len) {
      if (t < AP_ARM) return 3;
      if (t < AP_ARM + AP_SOLVE_MS[i]) return 1;
      return t < AP_ARM + AP_SOLVE_MS[i] + AP_STOP ? 3 : 0;
    }
    t -= len;
  }
  return 0;
}
#endif

void IRAM_ATTR sampleCb(void *) {
  uint16_t h = qHead, next = (h + 1) % QSIZE;
  if (next == qTail) return;  // queue full: drop (loop() stalled for 255 ms)
  queue[h].us = micros();
  queue[h].bits = (digitalRead(PIN_PAD_L) == LOW ? 1 : 0) | (digitalRead(PIN_PAD_R) == LOW ? 2 : 0);
#ifdef AUTOPLAY
  queue[h].bits |= apBits(millis());
#endif
  __sync_synchronize();
  qHead = next;
}

// ---- debounce with back-dating (same rule as TimingCore) --------------------
struct Pad {
  bool stable, cand;
  uint8_t run;
  uint32_t edgeUs;     // micros() of the first sample of the current candidate run
  uint32_t lastOnUs;   // back-dated time of the last confirmed touch
  uint32_t lastOffUs;  // back-dated time of the last confirmed release
};
Pad pads[2];
bool padsInit = false;

bool later(uint32_t a, uint32_t b) { return (int32_t)(a - b) > 0; }
uint32_t laterOf(uint32_t a, uint32_t b) { return later(a, b) ? a : b; }

// ---- state machine -----------------------------------------------------------
const char *STATE_NAME[] = {"IDLE", "ARMING", "READY", "RUNNING", "STOPPED"};
State state = IDLE;
uint32_t armSinceUs = 0, startUs = 0, stopUs = 0;
bool releasedSinceStop = false;
uint32_t pendTimeMs = 0;
uint8_t pendPen = PEN_OK;
uint32_t lastTimeMs = UNDEF;  // effective time of the last committed solve

void setState(State s) {
  state = s;
  Serial.printf("# state %s\n", STATE_NAME[s]);
}

RTC_DS1307 rtc;
bool rtcOk = false;

void printAverages() {
  char a5[12], a12[12], a100[12];
  fmtTime(a5, sizeof a5, averageOf(5));
  fmtTime(a12, sizeof a12, averageOf(12));
  fmtTime(a100, sizeof a100, averageOf(100));
  Serial.printf("# ao5 %s ao12 %s ao100 %s\n", a5, a12, a100);
}

// Append the pending solve to the ring and print its REC line. False when the log is full.
bool commit() {
  if (ringFull()) {
    Serial.println("# log full, press Dong bo (GPIO17) to sync first");
    return false;
  }
  uint32_t ts;
  uint8_t flags = pendPen;
  DateTime now = rtcOk ? rtc.now() : DateTime((uint32_t)0);
  if (rtcOk && now.year() >= 2024) {
    ts = now.unixtime();
  } else {
    ts = ((uint32_t)BOOT_ID << 20) | ((millis() / 1000) & 0xFFFFF);
    flags |= F_TIME_UNSET;
  }
  uint32_t seq = head + 1;
  packRecord(slotOf(seq), seq, pendTimeMs, ts, session, flags);
  head = seq;
  lastTimeMs = effectiveOf(slotOf(seq));
  printRec(slotOf(seq));
  printAverages();
  return true;
}

void dumpUnsynced() {
  Serial.printf("# sync: resending %lu records\n", (unsigned long)(head - lastAck));
  for (uint32_t s = lastAck + 1; s <= head; s++) printRec(slotOf(s));
  lastAck = head;
}

void runMachine(uint32_t nowUs) {
  bool both = pads[0].stable && pads[1].stable;
  switch (state) {
    case IDLE:
      if (both) {
        armSinceUs = laterOf(pads[0].lastOnUs, pads[1].lastOnUs);
        setState(ARMING);
      }
      break;
    case ARMING:
      if (!both) setState(IDLE);
      else if ((uint32_t)(nowUs - armSinceUs) >= ARM_MS * 1000UL) setState(READY);
      break;
    case READY:
      if (!both) {
        startUs = laterOf(pads[0].lastOffUs, pads[1].lastOffUs);
        setState(RUNNING);
      }
      break;
    case RUNNING:
      if (both) {
        stopUs = laterOf(pads[0].lastOnUs, pads[1].lastOnUs);
        pendTimeMs = (uint32_t)(stopUs - startUs + 500) / 1000;
        pendPen = PEN_OK;
        releasedSinceStop = false;
        setState(STOPPED);
        char t[16];
        fmtTime(t, sizeof t, pendTimeMs);
        Serial.printf("# time %s (%lu ms)\n", t, (unsigned long)pendTimeMs);
      }
      break;
    case STOPPED:
      if (!both) {
        releasedSinceStop = true;
      } else if (releasedSinceStop) {  // touching both pads again commits the solve
        if (commit()) {
          armSinceUs = laterOf(pads[0].lastOnUs, pads[1].lastOnUs);
          setState(ARMING);
        } else {
          releasedSinceStop = false;
        }
      }
      break;
  }
}

void processSample(const Sample &s) {
  for (uint8_t p = 0; p < 2; p++) {
    bool raw = (s.bits >> p) & 1;
    Pad &d = pads[p];
    if (!padsInit) {
      d = {raw, raw, DEBOUNCE, s.us, s.us, s.us};
      continue;
    }
    if (raw != d.cand) { d.cand = raw; d.run = 1; d.edgeUs = s.us; }
    else if (d.run < 255) d.run++;
    if (d.cand != d.stable && d.run >= DEBOUNCE) {
      d.stable = d.cand;
      if (d.stable) d.lastOnUs = d.edgeUs; else d.lastOffUs = d.edgeUs;
    }
  }
  padsInit = true;
  runMachine(s.us);
}

// ---- buttons ------------------------------------------------------------------
Button bSelect = {PIN_SELECT, false, 0}, bSession = {PIN_SESSION, false, 0}, bSync = {PIN_SYNC, false, 0};

// True once per press, with a 30 ms debounce.
bool pressed(Button &b) {
  bool d = digitalRead(b.pin) == LOW;
  if (d != b.down && millis() - b.changedMs > 30) {
    b.down = d;
    b.changedMs = millis();
    return d;
  }
  return false;
}

void onSelect() {
  if (state != STOPPED) return;
  pendPen = (pendPen + 1) % 3;
  Serial.printf("# penalty %s\n", pendPen == PEN_OK ? "OK" : pendPen == PEN_PLUS2 ? "+2" : "DNF");
}

void onSession() {
  if (state == ARMING || state == READY || state == RUNNING) return;
  if (state == STOPPED) {
    if (!commit()) return;
    setState(IDLE);
  }
  session = (session % 255) + 1;
  Serial.printf("# new session %u\n", session);
}

void onSync() {
  if (state == RUNNING) return;
  if (state == STOPPED) {
    if (!commit()) {
      dumpUnsynced();  // the dump frees ring slots, then retry once
      if (!commit()) return;
    }
    setState(IDLE);
  }
  dumpUnsynced();
}

// ---- display -------------------------------------------------------------------
Adafruit_SSD1306 oled(128, 64, &Wire, -1);
bool oledOk = false;

void drawOled() {
  if (!oledOk) return;
  char big[16], buf[16], a5[12], a12[12], a100[12];
  switch (state) {
    case ARMING: snprintf(big, sizeof big, "HOLD"); break;
    case READY: snprintf(big, sizeof big, "GO!"); break;
    case RUNNING: fmtTime(big, sizeof big, (micros() - startUs) / 1000); break;
    case STOPPED:
      fmtTime(buf, sizeof buf, pendTimeMs);
      snprintf(big, sizeof big, "%s%s", buf, pendPen == PEN_PLUS2 ? "+2" : pendPen == PEN_DNF ? " DNF" : "");
      break;
    default: fmtTime(big, sizeof big, lastTimeMs); break;
  }
  static char prev[48] = "";  // skip the 1 KB I2C frame when nothing on screen changed
  char sig[48];
  snprintf(sig, sizeof sig, "%d|%s|%lu|%u", state, big, (unsigned long)head, session);
  if (strcmp(sig, prev) == 0) return;
  strcpy(prev, sig);
  oled.clearDisplay();
  oled.setTextColor(SSD1306_WHITE);
  oled.setTextSize(1);
  oled.setCursor(0, 0);
  oled.printf("%s S%u #%lu", STATE_NAME[state], session, (unsigned long)head);
  oled.setTextSize(2);
  oled.setCursor(0, 14);
  oled.print(big);
  oled.setTextSize(1);
  fmtTime(buf, sizeof buf, lastTimeMs);
  oled.setCursor(0, 36);
  oled.printf("Last %s", buf);
  fmtTime(a5, sizeof a5, averageOf(5));
  fmtTime(a12, sizeof a12, averageOf(12));
  fmtTime(a100, sizeof a100, averageOf(100));
  oled.setCursor(0, 46);
  oled.printf("Ao5 %s", a5);
  oled.setCursor(0, 55);
  oled.printf("Ao12 %s Ao100 %s", a12, a100);
  oled.display();
}

// ---- setup / loop ---------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("# Haitay Wokwi sim, record format v1");
#ifdef AUTOPLAY
  Serial.printf("# AUTOPLAY: %u scripted solves on the pads\n", AP_N);
#endif

  uint8_t v[] = {'1', '2', '3', '4', '5', '6', '7', '8', '9'};
  uint16_t c = crc16(v, sizeof v);
  if (c == 0x29B1) Serial.println("# crc selftest 29b1 OK");
  else Serial.printf("# crc selftest %04x FAIL\n", c);

  pinMode(PIN_PAD_L, INPUT_PULLUP);
  pinMode(PIN_PAD_R, INPUT_PULLUP);
  pinMode(PIN_SELECT, INPUT_PULLUP);
  pinMode(PIN_SESSION, INPUT_PULLUP);
  pinMode(PIN_SYNC, INPUT_PULLUP);

  Wire.begin(PIN_SDA, PIN_SCL);
  Wire.setClock(400000);
  oledOk = oled.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  rtcOk = rtc.begin() && rtc.isrunning();
  Serial.printf("# oled %s, rtc %s\n", oledOk ? "ok" : "missing", rtcOk ? "ok" : "unset (TIME_UNSET)");

  esp_timer_create_args_t args;
  memset(&args, 0, sizeof args);
  args.callback = sampleCb;
  args.dispatch_method = ESP_TIMER_TASK;
  args.name = "pads";
  esp_timer_handle_t h;
  esp_timer_create(&args, &h);
  esp_timer_start_periodic(h, 1000);
  drawOled();
}

void loop() {
  while (qTail != qHead) {  // drain every queued 1 ms sample, oldest first
    Sample s = queue[qTail];
    qTail = (qTail + 1) % QSIZE;
    processSample(s);
  }
  if (pressed(bSelect)) onSelect();
  if (pressed(bSession)) onSession();
  if (pressed(bSync)) onSync();

  static uint32_t lastDraw = 0;
  if (millis() - lastDraw >= 250) {  // OLED redraw at most 4 Hz
    lastDraw = millis();
    drawOled();
  }
  delay(1);  // lets the core idle, which speeds up the Wokwi simulation; the queue holds 255 ms
}
