# Haitay embedded feasibility and bill of materials

Scope: standalone BLE speedcubing timer, 2 students, 6-10 weeks, Hanoi. Research date 2026-10-08. Currency assumption: 1 USD = 25,500 VND [assumption, unverified; used only for rough conversion]. All VND prices below were read from the cited page or search snippet on or around 2026-10-08; the pages show no price date unless stated, so treat every price as "observed this session, undated". Items marked [UNVERIFIED] have no cited source.

Tool note for the report writer: WebFetch returns model-written summaries of pages, so quoted page facts are as relayed by that tool. Where only a search snippet supports a price (no successful page fetch), this is stated.

---

## 1. MCU choice (ESP32 family, nRF52840, RP2040/RP2350, STM32)

### Takeaway
ESP32-S3 (or classic ESP32) is the lowest-risk pick: native capacitive touch, BLE with both roles, cheapest in Vietnam, richest examples. XIAO nRF52840 is the low-power alternative but has no touch peripheral, and no hshop product page for it could be fetched. ESP32-C3/C6 have no touch peripheral.

### Cited Findings
- Apache NimBLE on ESP32 supports Broadcaster, Observer, Peripheral and Central roles concurrently; connections are counted as one pool regardless of role; Espressif's multi-connection guide lists a configurable maximum (70 in v6.0.x docs for newer chips, 9 in older v5.2 docs) and says real limits depend on RAM — [ESP-IDF v6.0.1 ESP32-C6 multi-connection guide](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-guides/ble/ble-multiconnection-guide.html); [ESP-IDF v5.2 ESP32-S3 guide](https://docs.espressif.com/projects/esp-idf/en/release-v5.2/esp32s3/api-guides/ble/ble-multiconnection-guide.html)
- A forum thread reports running ESP32 as BLE server and client combined with NimBLE in Arduino (one peripheral link to the PC plus one central link to a cube is the Haitay case) — [ESP32 forum t=34803](https://esp32.com/viewtopic.php?t=34803) (thread content not read in full; existence only)
- Nordic S140 SoftDevice (nRF52840): up to 20 links with freely selectable role per link, practically 15-16 depending on memory; SoftDevice/nRF5 SDK are in maintenance mode and Nordic recommends nRF Connect SDK (Zephyr) for new work — [Nordic DevZone: S140 links](https://devzone.nordicsemi.com/f/nordic-q-a/42378/would-like-to-understand-maximum-concurrent-connections-for-nrf52832-or-nrf52840); [Nordic S140 page](https://www.nordicsemi.com/Products/Development-software/S140)
- Native capacitive touch peripheral: ESP32 (V1), ESP32-S2/S3 (V2), ESP32-P4 (V3). ESP32-C2/C3/C6/H2 have no touch peripheral per the ESP-IDF version table and ESPHome list (the "no touch" conclusion for C-series is the search tool's reading of absence from those tables; two marketing pages claim otherwise and look unreliable) — [ESP-IDF ESP32-S3 cap touch guide v6.1](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/cap_touch_sens.html); [ESPHome esp32_touch](https://esphome.io/components/binary_sensor/esp32_touch/)
- ESP32-S3 touch (ESP-IDF 5.4): 14 touch pads (T1-T14 on GPIO1-14), interrupts for ACTIVE and INACTIVE (touch and release), debounce count 0-7, IIR filters, hardware-timer or software-started scan — [ESP-IDF v5.4 ESP32-S3 touch_pad](https://docs.espressif.com/projects/esp-idf/en/v5.4/esp32s3/api-reference/peripherals/touch_pad.html)
- The ojdip.net ESP32 cube timer uses the original ESP32 touch peripheral with touchAttachInterrupt for touch-down, polling for touch-up, noting the Arduino API lacks an interrupt for both edges — [ojdip.net](https://ojdip.net/2020/11/esp32-cube-timer/)
- Bluetooth versions: original ESP32 supports DLE but not 2M PHY; ESP32-C3, S3, C6 support both — [Espressif BLE FAQ via search result](https://docs.espressif.com/projects/esp-faq/en/latest/software-framework/bt/ble.html) (claim relayed from search summary of the FAQ, page not fetched in full)
- Pico 2 W (RP2350) on hshop: Bluetooth 5.2 (BLE and Classic) — [hshop Pico 2 W](https://hshop.vn/mach-raspberry-pi-pico-2-w-rp2350)
- XIAO nRF52840: nRF52840 Cortex-M4F 64 MHz, 1 MB flash, 256 kB RAM, 2 MB QSPI flash, BQ25101 on-board LiPo charger, deep sleep 5 uA, USB-C — hshop listing text relayed by search: [hshop XIAO Sense page](https://hshop.vn/mach-seeed-studio-xiao-nrf52840-sense-bluetooth-5-0-imu-microphone-supports-arduino-and-circuitpython); Seeed wiki: [wiki.seeedstudio.com/XIAO_BLE](https://wiki.seeedstudio.com/XIAO_BLE/)
- Vietnam prices (VND):
  - ESP32 DevKit V1 30-pin Type-C CP2102: 120,000, in stock — [pyworld.vn](https://pyworld.vn/san-pham/esp32-devkit-v1-30pin.html) (fetched). Other shops 95,000-175,000 per search snippets (Pyworld CH340 95,000; Chợ Trời HN 148,000; Linh Kiện Việt 140,000) — [Chợ Trời HN](https://chotroihn.vn/mach-module-esp32-devkit-v1-30p-cp2102), [Linh Kiện Việt](https://linhkienvietnam.vn/module-node-mcu-32s-esp32-devkitc-dung-module-esp-wroom-32)
  - MKE-K01 ESP32-S3 Dev Kit (WROOM-1, DevKitC-1 compatible), hshop SKU HS2247V: N4 230,000; N16 255,000; N16R8 295,000; in stock — [hshop MKE-K01](https://hshop.vn/mach-phat-trien-mke-k01-esp32-s3-dev-kit) (fetched)
  - Genuine Espressif ESP32-S3-DevKitC-1 650,000 at proe.vn — [proe.vn](https://www.proe.vn/esp32-s3-devkitc-1) (search snippet)
  - XIAO nRF52840: 345,000-351,000 on hshop per search snippets — [hshop Seeed XIAO collection](https://hshop.vn/collections/seeed-studio-xiao); BUT a direct fetch of [hshop.vn/seeed-studio-xiao](https://hshop.vn/seeed-studio-xiao) listed only RP2040 (125,000), ESP32C3 (170,000), SAMD21 (135,000), Grove shield, and no nRF52840, ESP32-S3 or C6. Conflicting; stock unconfirmed. XIAO nRF52840 Sense 485,000-486,000, marked out of stock on one page.
  - Seeed official: XIAO nRF52840 Pre-Soldered US$10.99 — [Seeed Studio](https://www.seeedstudio.com/Seeed-Studio-XIAO-nRF52840-Pre-Soldered-p-6332.html) (search snippet)
  - Pico 2 W 275,000 (hshop, fetched); Pico 2 (no radio) 195,000 (snippet); Pico W (RP2040) 228,000-265,000 at other shops — [mlab.com.vn](https://mlab.com.vn/raspberry-pi-pico-w), [linhkientot.vn](https://www.linhkientot.vn/products/raspberry-pi-pico-w-da-ra-chan)
  - XIAO ESP32-C3 170,000 (hshop snippet/fetch)
  - Adafruit Feather nRF52840 / ESP32-C6 / STM32WB: no Vietnamese vendor page found; not recommended for this project.

### Inferences
- Rubric (BLE roles / touch / VN price / tooling): ESP32-S3 N16R8 = yes+yes / yes / 295k / ESP-IDF + Arduino + PlatformIO; classic ESP32 = BLE 4.2 only, no 2M PHY / yes / 120k / same; XIAO nRF52840 = best sleep power, integrated charger / no touch (needs MPR121 etc.) / ~345k / Arduino or Zephyr; Pico 2 W = BLE 5.2 via CYW43 / no touch / 275k / Pico SDK + BTstack [BTstack claim UNVERIFIED]; STM32 BLE parts (WB/WBA) = no VN dev-board source found.
- Classic ESP32 is adequate for Haitay (peripheral link to PC at 1M PHY is enough for 10k records) and is the cheapest; ESP32-S3 buys better touch (V2 filters, interrupt on release), BLE 5 and USB-native debugging for about 175k VND more.
- Central+peripheral concurrency on one ESP32 is supported by NimBLE but not guaranteed stable under load (see risk list); mitigate by making the smart-cube link a stretch goal.

### Gaps
- No measurement found of ESP32 NimBLE central+peripheral simultaneous operation with active notification streams on both links.
- No Nshop.vn or Thegioiic product page was retrieved for any MCU board (searches did not surface them); only hshop, pyworld, proe, mlab etc.
- Zephyr vs Arduino maturity for Pico 2 W BLE central was not researched.

---

## 2. Touch and pad sensing (Stackmat-style)

### Takeaway
ESP32 native capacitive touch (S3 preferred) or MPR121 can reach single-digit-millisecond detection with proper config; cheap TTP223 modules are rejected by their own datasheet (60 ms fast, 220 ms low-power worst-case). How the real Stackmat senses hands is not documented in any source found.

### Cited Findings
- TTP223 output response time: max about 60 ms in fast mode and 220 ms in low-power mode at VDD = 3 V; BA6 variant (common on cheap modules) is low-power-mode only, 220 ms max — [TTP223 datasheet (Seeed)](https://files.seeedstudio.com/wiki/Grove-Touch_Sensor/res/TTP223.pdf); [TTP223-BA6 datasheet](https://vakits.com/sites/default/files/TTP223B%20Touch%20Switch.pdf)
- MPR121: sample interval (ESI) programmable 1 ms to 128 ms (default 16 ms); touch status updates every ESI x SFI (SFI = second-filter sample count); 1 ms ESI costs 393 uA run current vs 199 uA at 2 ms and 29 uA at 16 ms; NXP fact sheet headline response 64 ms at 16 ms rate — [MPR121 datasheet](https://cdn-shop.adafruit.com/datasheets/MPR121.pdf); [NXP AN3890](https://www.nxp.com/docs/en/application-note/AN3890.pdf); [NXP fact sheet](https://www.nxp.com/docs/en/fact-sheet/MPR121FS.pdf)
- ESP-IDF touch: total latency is sleep interval plus measurement time; "excessive total time will slow down the touch response"; ESP32-S3 debounce registers a touch after n+1 consecutive over-threshold readings; recommended about 1 ms per measurement — [ESP-IDF v5.4 S3 touch_pad](https://docs.espressif.com/projects/esp-idf/en/v5.4/esp32s3/api-reference/peripherals/touch_pad.html); legacy API max measurement time 8.19 ms, and v6 driver exposes meas_interval_us plus a periodic software filter on original ESP32 whose interval also adds latency — [ESP-IDF v5.1 ESP32 touch_pad](https://docs.espressif.com/projects/esp-idf/en/v5.1/esp32/api-reference/peripherals/touch_pad.html); [ESP-IDF v6.1 cap_touch_sens (ESP32)](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/cap_touch_sens.html)
- Prior art ojdip.net: ESP32 touch pin 15, touch-down threshold 40 via interrupt, touch-up when touchRead > 50 (hysteresis), polled by a 1 ms hardware timer ISR; pad made from coffee-bag tab, "copper tape would be better"; calibration by tapping; no latency figure published; about 15 EUR total — [ojdip.net](https://ojdip.net/2020/11/esp32-cube-timer/)
- Stackmat sensing mechanism: forum members disagree (conductance between contacts, capacitive, body warmth, brand-dependent, some timers use infrared); no teardown or schematic found; pads need direct skin contact, gloves problematic — [Speedsolving: Stackmat timer and gloves](https://www.speedsolving.com/threads/stackmat-timer-and-gloves.19635/); [Speedsolving: How does a stackmat timer work](https://www.speedsolving.com/threads/how-does-a-stackmat-timer-work.92335/) (fetched; two posts only)
- DIY threads: most "home-made Stackmat" builds reuse mouse switches with PC software; one lid-switch build was "too unreliable, doesn't always respond and sometimes it responds double" — [Speedsolving: Home-made stackmat timer](https://www.speedsolving.com/threads/home-made-stackmat-timer.3618/)
- WCA rules for hands: timer starts when hands are removed (A4d); stop with both hands flat on sensors, palms down, +2 s penalty otherwise (A6d); judge sets G5 to 2-pad mode (A3b) — [WCA Regulations](https://www.worldcubeassociation.org/regulations/)
- Prices: MPR121 breakout 25,000 VND (dientutuyetnga, fetched; stock not stated) — [dientutuyetnga MPR121](https://dientutuyetnga.com/products/cam-ung-dien-dung-mpr121-1); other shops 65,000-80,000 (tae.vn, makerstore.vn, search snippet; the 80,000 item is a 3x4 keypad); TTP223 B module 8,000 at hshop per search snippet but the product URL returned HTTP 404 when fetched — [hshop TTP223B](https://hshop.vn/products/cam-ung-1-cham-dien-dung-ttp223b) (UNVERIFIED current)

### Inferences
- Candidate ranking for hands-on detection: (1) ESP32-S3 native touch with copper-foil pads, debounce 1-2, release interrupt (cost 0, tightest integration); (2) MPR121 at ESI 1 ms, SFI 2-4 (about 2-4 ms update, about 0.4 mA) as a drop-in fallback if native touch is noisy near the display or battery; (3) IR reflective (TCRT5000-style) or FSR pads: not researched, no source, treat as [UNVERIFIED] alternatives; (4) TTP223: reject.
- Start (release) and stop (touch) detection have different latencies on ESP32 touch because touch-down can be interrupt-driven while the original ESP32 Arduino API lacks a release interrupt (ojdip). A same-sign, similar-magnitude delay on both edges largely cancels in the elapsed time; unequal delays do not. Choose S3 (ACTIVE and INACTIVE interrupts) to make them symmetric.
- False triggers: a floating metal pad near a Li-ion charger or a USB cable adds noise; use hysteresis, per-edge debounce, and require both pads for arming (a two-pad AND is also the Stackmat-like logic and the WCA regulation behaviour).

### Gaps
- No source describes the real Stackmat pad technology or its detection latency.
- No measured end-to-end touch latency for ESP32 touch with release interrupt was found.
- IR reflective and FSR options: not researched; no Vietnamese price collected.

---

## 3. Timing accuracy

### Takeaway
A 1 ms timebase and 1 ms displayed resolution are achievable; a hard "under 1 ms" accuracy claim is not defensible once sensor response and debounce (several ms) are included. The honest spec: 1 ms resolution, single-digit-ms sensing uncertainty, stated and measured. WCA only uses hundredths (truncated), so this is already beyond competition need.

### Cited Findings
- GPIO interrupt to ISR latency on ESP32 is a few microseconds (about 2 us Espressif engineer on original ESP32 at 240 MHz; 5.6 us skew with the IDF ISR service; 4 us on ESP32-S3 by oscilloscope) but spikes occur with Bluetooth active or flash cache misses (IDF 5.4 issue) — [ESP32 forum t=26047 (S3)](https://esp32.com/viewtopic.php?t=26047); [ESP32 forum t=422](https://www.esp32.com/viewtopic.php?t=422); [esp-idf issue #15611](https://github.com/espressif/esp-idf/issues/15611); [ESP32 forum t=6407](https://www.esp32.com/viewtopic.php?t=6407)
- Espressif recommends GPTimer over esp_timer for real-time use, with `CONFIG_GPTIMER_ISR_HANDLER_IN_IRAM` to avoid cache-miss delays; gptimer_get_raw_count() software capture — [ESP-IDF GPTimer](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gptimer.html); [ESP-IDF esp_timer (S3)](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/esp_timer.html)
- OLED frame transfer over I2C took about 15 ms in the ojdip build, which motivated moving timing into a 1 ms hardware-timer ISR — [ojdip.net](https://ojdip.net/2020/11/esp32-cube-timer/)
- Stackmat: Gen-3 and later display to 0.001 s; WCA truncates to hundredths in the database; Gen-5 (2021) has 2-pad and 4-pad modes and WCA allows only 2-pad; large tournament display can lag up to about 0.3 s after stop (display, not timer); YuXin timer cited as accurate only to 0.016 s — [Speedsolving wiki: StackMat](https://www.speedsolving.com/wiki/index.php/StackMat); retailer/aggregate statement that G5 is "accurate to 0.001" — [speedcubing.org G5](https://speedcubing.org/products/speedstack-timer-g5)
- WCA Regulations: extra decimals shown on timer are not official, e.g. 12.678 recorded as 12.67 (A7b2); results under 10 min truncated to hundredths (9f1); a timer stopping before the solve with a time under 0.06 s triggers an extra attempt (A6b1), 0.06 s or more is DNF (A6b2); speedsolving timer must be "an approved timer from the Approved Timer List" (7f1a); timer must be attached to the mat (7f2) — [WCA Regulations](https://www.worldcubeassociation.org/regulations/)
- Display of official results is centiseconds "h:mm:ss.cc" (A7b1) — same source.

### Inferences
- Error budget (my estimate, not measured): ISR latency about 2-10 us (negligible); timer tick 1 us-1 ms depending on design (use a free-running 1 MHz GPTimer and timestamp in the ISR, not a polled 1 ms tick, to keep quantization at about 1 us); touch scan interval plus debounce about 2-10 ms per edge (dominant); display refresh 15 ms+ (harmless if decoupled from timestamping); BLE adds no error to the measurement if records are timestamped on-device, only to the live display on the phone.
- Recommended spec wording: "time resolution 1 ms; start/stop detection delay typically below 10 ms, characterised against a reference (logic analyzer or GPIO-driven test fixture)". Aim measurement at the first edge detection plus a fixed calibrated offset, because a constant bias is correctable while jitter is not.
- Since the WCA truncates to 0.01 s and requires an approved timer (7f1a), Haitay cannot be a competition timer; this is a limitation worth stating once and treating as out of scope for a class project.
- Offered verification method: drive a MOSFET/relay or a conductive tip with a pulse generator to emulate touch and release, log both edges and the ESP32 report on a logic analyzer; report mean offset and standard deviation over 100+ trials.

### Gaps
- No credible third-party measurement of ESP32 capacitive-touch detection latency in ms was found.
- No datasheet-level latency spec for Stackmat pad detection found; "accurate to 0.001" is a retailer claim about the timebase, not the sensors.
- WCA "Article 6" numbering no longer matches the current regulations text; the timer rules live in Article A, 7 and 9; the Approved Timer List itself was not fetched.

---

## 4. Display

### Takeaway
A 0.96 inch OLED (65,000 VND) is the cheapest working option but small for viewing across a table; a 1.54 inch 240x240 IPS ST7789 (85,000 VND) is the better readable display at similar cost; 7-segment (TM1637) is cheapest and large-digit friendly but cannot show stats. Decouple display from timing in every case.

### Cited Findings
- hshop OLED 0.96 inch 128x64 I2C, SKU HS0617V, 65,000 VND, in stock; driver listed as SSD1315 (datasheet link is SSD1306); 3.3-5 V; 25.2 x 26 mm — [hshop OLED](https://hshop.vn/lcd-oled-trang-0-96-inch-i2c) (fetched). Listing text relays 0.04 W power consumption (search snippet).
- Other OLED prices: Nshop 82,000 (2-color), Hoằng Long 80,000, IoT Maker 85,000 — [Nshop OLED](https://nshopvn.com/product/man-hinh-oled-0-96-inch-giao-tiep-i2c-2-mau/) (search snippet)
- TFT IPS ST7789 1.54 inch 240x240: 85,000 VND (hshop snippet) — [hshop 1.54 ST7789](https://hshop.vn/panel-man-hinh-lcd-tft-ips-1-54-inch-st7789-spi-interface); 1.69 inch rounded 75,000; 1.47 inch 125,000; 1.3 inch 240x240 elsewhere 105,000-137,000 (Điện Tử Tuyết Nga, lkcg.vn, Thế Giới IC out of stock) — [Thegioiic 1.3 ST7789](https://www.thegioiic.com/lcd-1-3inch-240x240-ips-st7789-giao-tiep-spi)
- TM1637 4-digit 0.36 inch module: hshop 13,000 VND but out of stock; other shops about 20,000-27,000 — [hshop TM1637](https://hshop.vn/mach-hien-thi-led-7-doan-tm1637-4-digit-display-0-36-inch-module-with-clock-dot); [dke.vn TM1637](https://dke.vn/module-cam-bien/hien-thi/module-hien-thi-4-led-7-doan-tm1637); 0.56 inch variants exist at linhkienck.vn (price not captured) — [linhkienck 0.56](https://linhkienck.vn/module-hien-thi-4-led-7-thanh-tm1637-0.56-inch-mau-xanh-duong-p4902480.html)
- 15 ms I2C OLED frame transfer observed in prior art — [ojdip.net](https://ojdip.net/2020/11/esp32-cube-timer/)

### Inferences
- Stats display (best, mean, Ao5, Ao12, Ao100) needs graphics, so OLED or TFT. SPI TFT at 40 MHz can refresh a partial region far faster than 400 kHz I2C OLED (about 1024 bytes x 9 bits / 400 kHz is about 23 ms per full frame by arithmetic); run display in its own FreeRTOS task, low priority, and never touch it in the touch ISR path.
- Updating the running time at 10 Hz (0.1 s) during the solve and showing full resolution only at stop mirrors the Stackmat feel and keeps CPU/I2C load low.
- E-paper: [UNVERIFIED] general expectation is full-refresh of about 1 s and partial refresh of 0.3 s or more, unsuitable for a running clock but fine for post-solve stats; no source collected.
- Readability from distance: not researched with sources; 0.96 inch OLED digit height is about 15-20 mm at best [estimate].

### Gaps
- No source on e-paper refresh times, viewing distance legibility, or TFT power draw was collected.
- Whether the hshop TM1637 is restocked is unknown.

---

## 5. Storage and power-loss safety

### Takeaway
ESP32 internal flash with LittleFS (or a custom log in a raw partition) holds 100k+ solves comfortably at 16 B/record. I2C FRAM (32 KB) is too small to hold the history and no Vietnamese vendor was found; use it only if the team wants an atomic pointer/journal.

### Cited Findings
- Espressif File System Considerations: LittleFS has integrated power-failure protection, dynamic wear leveling, low fixed RAM; FatFS none; SPIFFS partial; NOR flash erase cycles typically about 100,000; NVS not suitable for logging — [ESP-IDF File System Considerations](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/file-system-considerations.html)
- LittleFS design: copy-on-write, falls back to last good state after power loss, dynamic wear leveling, bad-block handling; updates commit only on sync/close — [littlefs project](https://github.com/littlefs-project/littlefs)
- ESP-IDF Wear Levelling component "performance mode" can lose a 4096-byte sector on power loss — [ESP-IDF Wear Levelling API](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/wear-levelling.html)
- ESP32-S3 dev board flash options on hshop: N4 (4 MB), N16 (16 MB), N16R8 (16 MB + 8 MB PSRAM) — [hshop MKE-K01](https://hshop.vn/mach-phat-trien-mke-k01-esp32-s3-dev-kit)
- DS3231 RTC module with CR2032: 44,000 VND hshop (search snippet; one hshop page shows out of stock), Điện tử Đạt 37,000, dke.vn 45,000 — [hshop DS3231](https://hshop.vn/products/mach-thoi-gian-thuc-rtc-ds3231); [Nshop DS3231](https://nshopvn.com/product/module-thoi-gian-thuc-rtc-ds3231/)
- MB85RC256V FRAM 32 KB I2C breakout: about US$3.72-7.29 abroad (AliExpress, eBay, ProtoSupplies US$5.95), no Vietnamese page found; supports 1 MHz I2C — [ProtoSupplies FRAM](https://protosupplies.com/product/fram-32k-i2c/)

### Inferences
- Record design (16 B): u32 seq, u32 time_ms, u32 unix_ts (or u16 date offset), u8 flags (penalty/DNF/session), u8 user, u16 CRC16. Capacity: 100,000 solves = 1.6 MB; 10,000 = 160 KB; at 100 solves/day, 36,500/year (arithmetic). Even a 1 MB partition holds about 65k records, so rolling (compaction) after acked sync is cheap.
- Power-loss pattern: append-only log in fixed-size pages, each record carrying CRC; commit = write record body then a valid-marker last; on boot scan from the last good page; sync state (last_acked_seq) stored in a separate small record. Alternatively rely on LittleFS and fsync after each solve (one write per solve, about 30 s apart at minimum, wear is trivial).
- Wear: 1 record per solve (16 B) with 4 KB sectors; 100k solves/year wears each sector only a few cycles with ring placement. Wear is a non-issue for this use if records are appended, not rewritten.
- RTC: skip the DS3231; set time from the PC on each BLE sync and keep a monotonic seq as ground truth; ESP32 internal RTC drift is acceptable for date stamps [drift magnitude UNVERIFIED].

### Gaps
- microSD module pricing in Vietnam and SPI NOR flash chip/module prices not collected.
- Power-loss behaviour of LittleFS on ESP32 under brownout (cheap battery) not tested by any source found.
- FRAM sold in Vietnam: not found; FM24xx not found.

---

## 6. BLE sync protocol

### Takeaway
A custom GATT service with a seq-numbered record stream (notify, chunked to MTU) and explicit "ack up to seq N" write is enough. Realistic throughput measured by others is 12-100 KB/s, so 10k records (160 KB) transfer in seconds to a minute. Web Bluetooth gives zero-install PC support in Chromium only.

### Cited Findings
- Espressif cites about 700 kbps (about 90 KB/s) between ESP32 boards, up to 1.4 Mbps with 2M PHY; community results: 46 KB/s, then 102.5 KB/s at 2M PHY with logging off, 68.6 KB/s at 1M PHY, and 12 KB/s for an L2CAP COC test with MTU 5000 — [ESP-FAQ BLE](https://docs.espressif.com/projects/esp-faq/en/latest/software-framework/bt/ble.html); [ESP32 forum t=40607](https://esp32.com/viewtopic.php?t=40607); [esp-idf issue #13637](https://github.com/espressif/esp-idf/issues/13637)
- DLE raises link-layer payload from 27 to 251 bytes; use notifications and write-without-response — same FAQ.
- Connection interval: Android accepts down to 7.5 ms (often 11.25 ms in practice), iOS 15 ms minimum; peripheral requests are suggestions, central decides; one notification burst per connection event — [Punch Through connection interval](https://punchthrough.com/ble-connection-interval-throughput/); [Nordic DevZone high-rate notifications](https://devzone.nordicsemi.com/f/nordic-q-a/119171/efficient-handling-of-high-rate-sensor-data-via-ble-notifications)
- Prior-art GATT: ojdip.net timer uses one custom service/characteristic (READ/NOTIFY/INDICATE) with a packed struct {state, epoch, duration_ms} notified on each state change; a second characteristic was dropped after a GATT error on a phone — [ojdip.net](https://ojdip.net/2020/11/esp32-cube-timer/)
- Web Bluetooth: supported in Chrome (56+), Edge (79+), Opera, Samsung Internet, Chrome for Android; not Safari or Firefox; iOS needs a third-party polyfill — [caniuse web-bluetooth](https://caniuse.com/web-bluetooth)
- Smart cube prior art: gan-web-bluetooth (TypeScript, Web Bluetooth) handles GAN Gen2/3/4 cubes and GAN Smart Timers; newer GAN cubes encrypt traffic; Giiker/Mi cubes use a simpler unencrypted GATT flow — [gan-web-bluetooth](https://deepwiki.com/afedotov/gan-web-bluetooth); [gan-cube-sample](https://github.com/afedotov/gan-cube-sample); [Speedsolving GAN 356i protocol](https://www.speedsolving.com/threads/bluetooth-api-decoding-protocol-for-gan-356i-carry.89525/); [AlphaSheep smart cube gist](https://gist.github.com/AlphaSheep/752a19e116f5b5e823676eec4a43027f)

### Inferences
- Throughput arithmetic (mine): 10,000 x 16 B = 160 KB. At a conservative 10 KB/s = 16 s; at 50 KB/s = 3 s. With default MTU 23 (20 B payload) and one notification per 15 ms connection event, 1.3 KB/s = about 2 min; so negotiate MTU 185-247 and DLE. Protocol overhead (seq, CRC per chunk) adds 10-20%.
- Idempotent sync: device sends records with seq; PC replies `ACK(last_contiguous_seq)` after writing to disk and fsync; device marks `acked_seq` and only then reclaims space (or keeps a tail of the last N); resend from `acked_seq+1` after disconnect; duplicates are discarded by seq (user id, seq) on the PC. Chunk-level CRC detects corruption; do not delete on connection loss.
- PC side: Web Bluetooth (Chromium only, needs user gesture, runs a static page) is lowest effort for a class demo; Python bleak [UNVERIFIED: not researched] or Electron [UNVERIFIED] are alternatives if Safari/Firefox must be avoided.
- Smart cube link: GAN protocol requires decryption (key derived from MAC address per forum, not verified from source); recommend handling the cube on the PC with gan-web-bluetooth rather than on the ESP32, and listing the on-device central role as optional stretch. Giiker-style cubes are the realistic on-device target.

### Gaps
- No measured throughput on Haitay-like hardware (ESP32-S3 peripheral to Windows laptop) found.
- bleak and Electron BLE support not researched.
- Exact GAN key derivation and UUIDs not extracted.

---

## 7. Power (15 V question, Li-ion, USB-C)

### Takeaway
"Pin 15 V" is almost certainly an error (a 4S Li-ion pack is nominally 14.8 V and USB PD offers a 15 V step, but neither is needed): the MCU, display and pads run on 3.3 V. Use a single-cell Li-ion with a TP4056 USB-C charger or XIAO's on-board charger. Drop 15 V from the requirements or relegate to "PD trigger, optional".

### Cited Findings
- TP4056 USB-C charging module, hshop SKU HS1439V: 10,000 VND, in stock, 1 A charge, 4.2 V full, input 4.5-8 V or USB-C 5 V, page mentions an over-discharge cutoff; protection IC not named — [hshop TP4056 USB-C](https://hshop.vn/mach-sac-pin-tp4056-lithium-battery-charge-controller-usb-c) (fetched). Other shops 6,000-13,000 — [HTPro TP4056 with protection](https://htpro.vn/pin-acquy-bien-ap-mach-sac/tp4056-mach-sac-pin-usb-type-c-1a-co-bao-ve.html)
- CH224K: WCH USB PD sink/trigger controller, PD 3.0/2.0, BC1.2, up to 100 W; 15 V set via CFG pins CFG1=0, CFG2=1, CFG3=1; CFG pins must not exceed 3.7 V — [LCSC CH224K datasheet](https://www.lcsc.com/datasheet/C970725.pdf); [components101 CH224K](https://components101.com/ics/ch224k-usb-power-delivery-controller-ic); module with DIP switch 5/9/12/15/20 V about SGD 5.60 at Kuriosity, AliExpress 3 pcs about US$0.99, no Vietnamese shop found — [Kuriosity](https://kuriosity.sg/products/usb-c-pd-trigger-module-pd3-0-2-0-bc1-2-fast-charging-protocols-adjustable-voltage-5v-9v-12v-15v-20v)
- ESP32-S3 current (datasheet-style summary): light sleep 240 uA; modem sleep 13-108 mA; BLE TX 116-335 mA, RX 93 mA; on a real XIAO ESP32-S3, light sleep initially measured 2.88 mA because of the flash, later about 692 uA after configuration — [DeepBlueMbedded](https://deepbluembedded.com/esp32-sleep-modes-power-consumption/); [Qoitech](https://www.qoitech.com/blog/esp32-s3-c3-c6-sleep-power-consumption/). Third-party: connected idle with modem sleep about 20-40 mA (ESP32-S3) and about 40 mA (C3 measured) — [Hubble BLE guide](https://hubble.com/community/guides/esp32-power-consumption-in-ble-mode-what-to-expect-from-advertising-scanning-and-connected-states/); [Rob Dobson C3](https://robdobson.com/2023/11/investigating-esp32-c3-power-management/)
- XIAO nRF52840: 5 uA deep sleep, BQ25101 charger on board — [hshop XIAO Sense page](https://hshop.vn/mach-seeed-studio-xiao-nrf52840-sense-bluetooth-5-0-imu-microphone-supports-arduino-and-circuitpython)
- 18650 accessories at hshop: 4-slot USB charger 68,000, 2x18650 holder with switch 13,000; no bare 18650 cell price found — [hshop Pin & Sạc](https://hshop.vn/pin-sac)

### Inferences
- Battery life estimate (my arithmetic, 2,000 mAh cell, S3 board): active session with BLE connected and OLED on about 30-50 mA -> 40-65 h; advertising-only standby with light sleep about 1-3 mA -> 28-80 days; the dev-board USB-UART and LDO often add several mA, so expect lower. nRF52840 would last longer by roughly an order of magnitude in sleep.
- A 15 V rail would need a buck converter to 3.3 V (extra cost, heat, no benefit). If the team means a 4S Li-ion pack (about 14.8 V nominal) it is far above the need; recommend a single 18650/LiPo.
- TP4056 modules provide no load sharing (power-path) [UNVERIFIED general knowledge]; using the device while charging can mis-terminate charging; fine for a class project if documented. Many cheap 18650 sources have inflated capacity claims (eBay buyer complaint of 2600 mAh behaving as about 1200 mAh in the search snippet), so buy from a known shop.
- Safety: Li-ion cell needs protection (DW01-type) and correct 4.2 V charge; use cells with protection board or modules that include it.

### Gaps
- No Vietnamese bare 18650 or LiPo pouch cell price verified.
- No power-path charger (e.g., BQ24074) module found in Vietnam.
- Actual Haitay duty cycle and display current not measured.

---

## 8. Enclosure and ergonomics

### Takeaway
A 3D-printed enclosure and pads are feasible and cheap (about 70,000-250,000 VND per iteration). Print service price is 700-2,500 VND/g, and printing locally is a decision for the team (own printer, university lab, or service).

### Cited Findings
- Nshop FDM 3D print service reference prices: PLA 800 VND/g, PETG 700, ABS 1,800, TPU 2,300; small models 2-3 working days; ships nationwide; page does not state a Hanoi branch — [Nshop 3D print](https://nshopvn.com/dich-vu/in-3d)
- 3D Thinking (Hà Nội) quotes 1,300-2,500 VND/g (ambiguous which material in the snippet); Good Gearz (HCMC) from 1,200 VND/g; CT3D 8,000-20,000 VND/g (outlier); raw filament about 300-500 VND/g — [3dthinking.vn Hà Nội](https://3dthinking.vn/dich-vu/dich-vu-in-3d/); [goodgearz.com](https://goodgearz.com/bang-gia-in-3d/); [3dcoretech.com.vn](https://3dcoretech.com.vn/cap-nhat-bang-gia-in-3d-chi-tiet-moi-nhat/)
- WCA wants a timer "attached to the mat" (7f2) and timers made robust against accidental button presses (7f3); Stackmat Gen-2/3/4 thumb hit the reset button between the plates causing DNFs at the 2017 Worlds — [WCA Regulations](https://www.worldcubeassociation.org/regulations/); [Speedsolving wiki: StackMat](https://www.speedsolving.com/wiki/index.php/StackMat)

### Inferences
- Estimated shell weight 80-150 g -> 64,000-120,000 VND at 800 VND/g, or up to 190,000-375,000 at 2,500 VND/g. Budget two or three iterations (case, pad plate, lid).
- Ergonomics: two pads about the same spacing as a Stackmat, recessed buttons (no button between the pads), cable/USB-C port at the back, flat bottom with rubber feet. Exact Stackmat dimensions not researched [UNVERIFIED].
- PETG is better than PLA for durability and heat in a hot Hanoi bag [engineering judgement, no source].

### Gaps
- No Hanoi-specific price page for a hobby print service with PETG was fully verified; Nshop location unclear.
- Stackmat pad dimensions and ergonomics measurements not researched.

---

## 9. Bill of materials (three tiers)

### Takeaway
Minimum viable about 0.6 million VND (about US$24); recommended about 1.3 million VND (about US$50); premium about 2.5 million VND (about US$97). Only the lines marked "V" have a verified source; every "E" line is an estimate the team must replace by a quote.

Legend: V = price from a cited page/snippet; E = estimate with no source (UNVERIFIED). Prices include VAT where hshop SKU ends in "V". USD at 25,500 VND/USD [assumption]. Shipping from hshop (HCMC) or other sellers to Hanoi: no shipping fee verified; estimated.

### Cited Findings (price evidence, by line)
- ESP32 DevKit V1 Type-C: [pyworld.vn](https://pyworld.vn/san-pham/esp32-devkit-v1-30pin.html) 120,000
- ESP32-S3 MKE-K01 N16R8: [hshop](https://hshop.vn/mach-phat-trien-mke-k01-esp32-s3-dev-kit) 295,000
- XIAO nRF52840: [hshop collection](https://hshop.vn/collections/seeed-studio-xiao) about 345,000 (conflict noted in section 1)
- OLED 0.96 inch: [hshop](https://hshop.vn/lcd-oled-trang-0-96-inch-i2c) 65,000
- ST7789 1.54 inch: [hshop](https://hshop.vn/panel-man-hinh-lcd-tft-ips-1-54-inch-st7789-spi-interface) 85,000 (snippet)
- TP4056 USB-C: [hshop](https://hshop.vn/mach-sac-pin-tp4056-lithium-battery-charge-controller-usb-c) 10,000
- MPR121: [dientutuyetnga](https://dientutuyetnga.com/products/cam-ung-dien-dung-mpr121-1) 25,000
- DS3231: [hshop](https://hshop.vn/products/mach-thoi-gian-thuc-rtc-ds3231) 44,000 (stock doubtful)
- 2x18650 holder with switch 13,000: [hshop Pin & Sạc](https://hshop.vn/pin-sac) (snippet)
- 3D print 800 VND/g: [Nshop](https://nshopvn.com/dich-vu/in-3d)
- FRAM about US$6: [ProtoSupplies](https://protosupplies.com/product/fram-32k-i2c/) (import, not VN)
- CH224K module about US$1-2: [Kuriosity](https://kuriosity.sg/products/usb-c-pd-trigger-module-pd3-0-2-0-bc1-2-fast-charging-protocols-adjustable-voltage-5v-9v-12v-15v-20v) (import, not VN)

### Inferences (tier tables; all arithmetic mine)

**Tier A: Minimum viable (classic ESP32, native touch, OLED)**

| Item | Qty | Unit VND | Line VND | Src |
|---|---|---|---|---|
| ESP32 DevKit V1 30-pin Type-C | 2 (1 spare) | 120,000 | 240,000 | V |
| OLED 0.96 inch I2C | 1 | 65,000 | 65,000 | V |
| TP4056 USB-C charger | 2 | 10,000 | 20,000 | V |
| 18650 holder w/ switch | 1 | 13,000 | 13,000 | V |
| 18650 cell (protected) | 1 | 60,000 | 60,000 | E |
| Copper tape/foil pads, wires, buttons, perfboard | lot | 80,000 | 80,000 | E |
| 3D-printed case (about 100 g) | 1 | 80,000 | 80,000 | V (800/g) |
| Shipping/handling | lot | 45,000 | 45,000 | E |
| **Total** | | | **about 603,000 (US$24)** | verified part 418,000 |

**Tier B: Recommended (ESP32-S3 N16R8, TFT, fallback sensor, RTC optional)**

| Item | Qty | Unit VND | Line VND | Src |
|---|---|---|---|---|
| ESP32-S3 MKE-K01 N16R8 | 2 (1 spare) | 295,000 | 590,000 | V |
| ST7789 1.54 inch IPS | 1 | 85,000 | 85,000 | V (snippet) |
| OLED 0.96 inch (debug/backup) | 1 | 65,000 | 65,000 | V |
| MPR121 breakout (fallback sensing) | 1 | 25,000 | 25,000 | V |
| DS3231 RTC (optional) | 1 | 44,000 | 44,000 | V (stock?) |
| TP4056 USB-C charger | 2 | 10,000 | 20,000 | V |
| 18650 holder + cell | 1+1 | 13,000 + 60,000 | 73,000 | V + E |
| Copper tape/pads/wires/buttons | lot | 130,000 | 130,000 | E |
| 3D-printed case, 2 iterations (about 120 g each) | 2 | 96,000 | 192,000 | V (800/g) |
| Shipping/handling | lot | 60,000 | 60,000 | E |
| **Total** | | | **about 1,284,000 (US$50)** | verified part 1,034,000 incl. holder/print |

**Tier C: Premium (nRF52840 low-power build + extras, custom PCB)**

| Item | Qty | Unit VND | Line VND | Src |
|---|---|---|---|---|
| XIAO nRF52840 | 1 | 345,000 | 345,000 | V (conflict) |
| ESP32-S3 N16R8 (fallback / dev) | 1 | 295,000 | 295,000 | V |
| MPR121 | 2 | 25,000 | 50,000 | V |
| ST7789 1.54 inch | 1 | 85,000 | 85,000 | V |
| OLED 0.96 inch | 1 | 65,000 | 65,000 | V |
| DS3231 | 1 | 44,000 | 44,000 | V (stock?) |
| 3D-printed case, 3 iterations | 3 | 96,000 | 288,000 | V |
| FRAM 32 KB breakout (import) | 1 | 153,000 | 153,000 | E (US$6, import) |
| CH224K PD module (import) | 1 | 40,000 | 40,000 | E |
| Custom 2-layer PCB run + shipping | 1 | 750,000 | 750,000 | E |
| Cells, holders, pads, misc, shipping | lot | 370,000 | 370,000 | E |
| **Total** | | | **about 2,485,000 (US$97)** | verified part 1,172,000 |

Notes:
- Tier A and B are bought from sellers confirmed to list the item with a price; Tier C includes imported items and a PCB whose cost and lead time were not researched.
- Spare parts: one spare MCU per tier is built in; pads and wires are the likeliest consumables.
- Thegioiic, Nshop, Shopee and Lazada pricing for the same MCUs was not captured; the shopee/lazada route may be cheaper but gives no cited price.
- Mouser/DigiKey reference prices were not collected (no VN-shipping check done).

### Gaps
- No cited price for bare Li-ion cells, copper tape, connectors, perfboard, or custom PCB fabrication in Vietnam.
- Shipping fees to Hanoi unknown.
- DS3231 and TM1637 stock uncertain on hshop at fetch time.

---

## 10. Technical risk list

### Takeaway
Top risks: (1) "under 1 ms" requirement not meetable as written, (2) false or delayed touch edges, (3) BLE dual-role stability and smart-cube encryption, (4) scope vs 6-10 weeks. Each has a mitigation below.

### Cited Findings (for the evidence behind risks)
- Touch debounce/measurement interval add latency — [ESP-IDF touch docs](https://docs.espressif.com/projects/esp-idf/en/v5.4/esp32s3/api-reference/peripherals/touch_pad.html)
- TTP223 60-220 ms response — [TTP223 datasheet](https://files.seeedstudio.com/wiki/Grove-Touch_Sensor/res/TTP223.pdf)
- 15 ms I2C display transfer and "GATT operation failed for unknown reasons" when adding a second characteristic — [ojdip.net](https://ojdip.net/2020/11/esp32-cube-timer/)
- GPIO ISR latency spikes with Bluetooth active in IDF 5.4 — [esp-idf issue #15611](https://github.com/espressif/esp-idf/issues/15611)
- ojdip build had random crashes with BluetoothSerial until the hardware timer was moved from group 0 to group 1; root cause unclear — [ojdip.net](https://ojdip.net/2020/11/esp32-cube-timer/)
- NimBLE connection limits and memory dependence — [ESP-IDF multi-connection guide](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-guides/ble/ble-multiconnection-guide.html)
- Spec-text risk: WCA requires an approved timer — [WCA Regulations](https://www.worldcubeassociation.org/regulations/)
- NVS not suitable for logging; flash about 100k erase cycles — [ESP-IDF File System Considerations](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/file-system-considerations.html)
- Web Bluetooth is Chromium-only — [caniuse](https://caniuse.com/web-bluetooth)

### Inferences (likelihood and mitigation are my judgement)

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Requirement "under 0.001 s" taken literally | High | High (fails acceptance) | Redefine: 1 ms resolution, detection delay <10 ms, characterise offset/jitter with logic analyzer |
| Touch false triggers/missed releases (noise, USB charger, sweaty/dry hands, gloves) | Medium-High | High | Hysteresis, per-edge debounce, copper-foil pads with ground ring, MPR121 fallback, per-user threshold calibration |
| Touch latency asymmetry between start and stop | Medium | Medium | Use S3 with ACTIVE+INACTIVE interrupts; calibrate offset with fixture |
| ISR timing spikes from BLE/flash cache | Medium | Medium | IRAM ISR, GPTimer capture, pin timing task to a core, keep BLE on the other core, avoid flash ops in solve |
| Display blocking (15 ms I2C) corrupting timestamps | Medium | Medium | Timestamp in ISR; render in separate low-priority task; SPI TFT |
| BLE central+peripheral instability on one ESP32 | Medium | Medium | Make cube link stretch goal; start from NimBLE multi_conn example; test early (week 3) |
| Smart cube (GAN) encryption | High (if GAN targeted) | Medium | Target Giiker-style unencrypted cubes or do the cube link on the PC with gan-web-bluetooth |
| Flash wear/corruption on power loss | Low-Medium | High (data loss) | LittleFS or CRC log, page-aligned append, last-acked pointer, no delete before ack, brownout detector |
| Data wipe before PC has saved | Low | High | Ack only after PC fsync; keep tail window; resumable by seq |
| Li-ion safety/charger without power path | Medium | Medium | Protected cell, TP4056 w/ protection, no use-while-charging promise; or XIAO nRF52840 with on-board charger |
| 15 V requirement misread | High | Low | Confirm with lecturer; adopt 5 V USB-C + 1S Li-ion; PD trigger only if confirmed |
| Not WCA-approved | Certain | Low (class project) | State as non-goal |
| Schedule (BLE+UI+storage+case in 6-10 weeks) | Medium | High | Weekly milestones: wk1-2 timing+touch fixture, wk3-4 storage+display, wk5-6 BLE sync+PC page, wk7-8 case, wk9-10 cube link and polish |
| Enclosure ergonomics / pad spacing | Medium | Low | 2 print iterations; recessed buttons |

### Gaps
- Likelihood ratings are team-level judgement; no published failure rates exist for these items.
- No source quantifies false-trigger rates of ESP32 touch near USB chargers.

---

## Source quality notes
- Primary: Espressif ESP-IDF docs, TTP223/MPR121/CH224K datasheets, WCA Regulations, hshop/pyworld/dientutuyetnga/Nshop product or service pages (fetched via summarising tool, so quote-level exactness not guaranteed).
- Secondary/weaker: forum threads (ESP32 forum, Speedsolving), blog posts (ojdip.net, Qoitech, Hubble, DeepBlueMbedded), retailer text about Stackmat accuracy.
- Statements marked "search snippet" came from a search tool summary without a successful fetch of the product page; hshop TTP223 URL returned 404, so that price is unverified.
- The hshop XIAO collection pages conflict (one lists XIAO nRF52840 at about 345,000-351,000, another fetch of a different collection URL did not list it); confirm before buying.
