"""Virtual Haitay device: timing core, FRAM ring log, NVS, BLE peripheral logic.

The firmware modules map one to one: TimingCore (touch + timer), Fram/Nvs (storage),
VirtualDevice.handle_* (BLE GATT server). Only the transport is simulated.
"""
import json
import os
import random

from . import proto, stats


class PowerCut(Exception):
    """Raised when the simulated supply drops in the middle of a write."""


class Fram:
    """FM24CL64B model: 8 KB, bytes land as they arrive, no write delay."""

    SIZE = 8192

    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            with open(path, "wb") as f:
                f.write(bytes(self.SIZE))
        with open(path, "rb") as f:
            self.mem = bytearray(f.read())

    def read(self, addr, n):
        return bytes(self.mem[addr:addr + n])

    def write(self, addr, data, cut_after=None):
        """Write byte by byte; cut_after=k stops after k bytes, as a pulled cable would."""
        for i, b in enumerate(data):
            if cut_after is not None and i >= cut_after:
                self._flush()
                raise PowerCut(addr + i)
            self.mem[addr + i] = b
        self._flush()

    def _flush(self):
        with open(self.path, "wb") as f:
            f.write(self.mem)


class Nvs:
    """ESP-IDF NVS model: small key-value store with atomic commit."""

    def __init__(self, path):
        self.path = path
        self.data = json.load(open(path)) if os.path.exists(path) else {}

    def get(self, key, default=0):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        tmp = self.path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.data, f)
        os.replace(tmp, self.path)


class LogFull(Exception):
    pass


class VirtualDevice:
    SLOTS = Fram.SIZE // proto.REC_SIZE  # 512

    def __init__(self, workdir, device_id="HT-0001", mtu=185, rtc_valid=False):
        os.makedirs(workdir, exist_ok=True)
        self.device_id = device_id
        self.mtu = mtu
        self.fram = Fram(os.path.join(workdir, "fram.bin"))
        self.nvs = Nvs(os.path.join(workdir, "nvs.json"))
        self.rtc_valid = rtc_valid  # DS3231 holds time while the CR2032 is present
        self.rtc_unix = 0
        self.boot()

    # ---- boot and storage -------------------------------------------------
    def boot(self):
        """Rebuild state by scanning the ring; no header to keep consistent."""
        self.boot_id = self.nvs.get("boot_id") + 1
        self.nvs.set("boot_id", self.boot_id)
        self.uptime_s = 0
        self.last_ack = self.nvs.get("last_ack")
        self.records = {}
        torn = 0
        for slot in range(self.SLOTS):
            raw = self.fram.read(slot * proto.REC_SIZE, proto.REC_SIZE)
            rec = proto.unpack(raw)
            if rec:
                self.records[rec["seq"]] = rec
            elif raw != bytes(proto.REC_SIZE):
                torn += 1
        self.head = max([self.last_ack, *self.records])  # wipe keeps seq monotonic
        self.session = self.records[self.head]["session"] if self.head in self.records else 1
        return torn

    def _append(self, time_ms, flags, cut_after=None):
        seq = self.head + 1
        slot = (seq - 1) % self.SLOTS
        old = proto.unpack(self.fram.read(slot * proto.REC_SIZE, proto.REC_SIZE))
        if old and old["seq"] > self.last_ack:
            raise LogFull(seq)  # never overwrite a record the PC has not acknowledged
        if self.rtc_valid:
            ts = self.rtc_unix + self.uptime_s
        else:
            ts, flags = (self.boot_id << 20) | (self.uptime_s & 0xFFFFF), flags | proto.F_TIME_UNSET
        raw = proto.pack(seq, time_ms, ts, self.session, flags)
        self.fram.write(slot * proto.REC_SIZE, raw, cut_after)  # commit point: byte 16 lands
        if old:
            self.records.pop(old["seq"], None)
        self.records[seq] = proto.unpack(raw)
        self.head = seq
        return seq

    def record_solve(self, time_ms, penalty=proto.PEN_OK, cut_after=None):
        return self._append(time_ms, penalty, cut_after)

    def edit(self, target_seq, penalty=None, deleted=False):
        cur = self.view().get(target_seq)
        pen = cur["penalty"] if penalty is None and cur else (penalty or 0)
        return self._append(target_seq, proto.F_EDIT | pen | (proto.F_DELETED if deleted else 0))

    def new_session(self):
        self.session = (self.session % 255) + 1

    def tick(self, seconds):
        self.uptime_s += seconds

    # ---- derived view and on-device statistics ----------------------------
    def view(self):
        """Solves after applying edit records in seq order."""
        out = {}
        for seq in sorted(self.records):
            r = self.records[seq]
            if r["flags"] & proto.F_EDIT:
                t = out.get(r["time_ms"])
                if t:
                    t["penalty"] = r["flags"] & proto.PEN_MASK
                    t["deleted"] = bool(r["flags"] & proto.F_DELETED)
            else:
                out[seq] = {"time_ms": r["time_ms"], "penalty": r["flags"] & proto.PEN_MASK,
                            "deleted": False}
        return out

    def stats(self):
        v = self.view()
        times = [stats.effective(s["time_ms"], s["penalty"]) for _, s in sorted(v.items())
                 if not s["deleted"]]
        return stats.summary(times)

    # ---- BLE GATT server ---------------------------------------------------
    def read_info(self):
        return {"device_id": self.device_id, "fw": "0.1.0-sim", "hw": "sim",
                "record_format": 1, "slots": self.SLOTS}

    def read_state(self):
        return {"boot_id": self.boot_id, "uptime_s": self.uptime_s, "head": self.head,
                "last_ack": self.last_ack, "unsynced": self.head - self.last_ack,
                "rtc_valid": self.rtc_valid, "session": self.session}

    def write_control(self, data: bytes):
        op, arg = data[0], int.from_bytes(data[1:5], "little")
        if op == proto.CMD_ACK:
            if arg > self.last_ack:
                self.last_ack = min(arg, self.head)
                self.nvs.set("last_ack", self.last_ack)
        elif op == proto.CMD_SET_TIME:
            self.rtc_unix, self.rtc_valid = arg - self.uptime_s, True
        elif op == proto.CMD_WIPE:
            if self.head != self.last_ack:
                return "REFUSED_UNSYNCED"
            for slot in range(self.SLOTS):
                self.fram.write(slot * proto.REC_SIZE, bytes(proto.REC_SIZE))
            self.records.clear()
            self.new_session()
        return "OK"

    def sync_frames(self):
        """Notify stream for CMD_SYNC: every record after last_ack, packed per MTU."""
        per = proto.records_per_frame(self.mtu)
        pending = [s for s in sorted(self.records) if s > self.last_ack]
        for i in range(0, len(pending), per):
            chunk = pending[i:i + per]
            yield proto.log_frame([proto.pack(**self.records[s]) for s in chunk])
        yield proto.end_frame(self.head)


class TimingCore:
    """Two-pad state machine: IDLE -> ARMING -> READY -> RUNNING -> STOPPED.

    Input is the raw 1 kHz touch decision per pad (after the hardware threshold and
    hysteresis). A debounce of `debounce` stable samples confirms an edge, and the
    timestamp is back-dated to the first sample of the stable run.
    """

    ARM_MS = 1500

    def __init__(self, debounce=3):
        self.debounce = debounce

    def run(self, left, right):
        """left/right: lists of 0/1 samples at 1 ms. Returns (start_ms, stop_ms, events)."""
        state, arm_since, start, events = "IDLE", None, None, []
        stable = [left[0], right[0]]
        run_len, cand = [0, 0], [left[0], right[0]]
        edge_at = [0, 0]
        for t in range(len(left)):
            for p, raw in enumerate((left[t], right[t])):
                if raw != cand[p]:
                    cand[p], run_len[p], edge_at[p] = raw, 1, t
                else:
                    run_len[p] += 1
                if cand[p] != stable[p] and run_len[p] >= self.debounce:
                    stable[p] = cand[p]
                    events.append((edge_at[p], p, stable[p]))
            both = stable[0] and stable[1]
            if state == "IDLE" and both:
                state, arm_since = "ARMING", max(e[0] for e in events if e[2])
            elif state == "ARMING":
                if not both:
                    state = "IDLE"
                elif t - arm_since >= self.ARM_MS:
                    state = "READY"
            elif state == "READY" and not both:
                state, start = "RUNNING", max(e[0] for e in events if not e[2])
            elif state == "RUNNING" and both:
                return start, max(e[0] for e in events[-2:] if e[2]), events
        return start, None, events


def hand_trace(rng, solve_ms, sense_ms=(2, 10), chatter=True):
    """Simulated pad samples for one solve, plus the true solve time.

    True start: the first hand leaves its pad. True stop: the second hand lands.
    Each edge reaches the MCU after a random sensing delay, with optional chatter.
    """
    arm = rng.randint(1700, 3000)
    lift = [arm, arm + rng.randint(0, 40)]
    lift_true = min(lift)
    land_first = lift_true + solve_ms - rng.randint(30, 200)
    land = [land_first, lift_true + solve_ms]
    rng.shuffle(land)
    n = lift_true + solve_ms + 400
    pads = []
    for p in range(2):
        on_at = rng.randint(50, 150)
        d_off = lift[p] + rng.uniform(*sense_ms)
        d_on = land[p] + rng.uniform(*sense_ms)
        s = [1 if (on_at <= t < d_off or t >= d_on) else 0 for t in range(n)]
        if chatter:  # a few flips around each edge, shorter than the debounce window
            for edge in (int(d_off), int(d_on)):
                for k in rng.sample(range(-3, 0), 1):
                    if 0 <= edge + k < n:
                        s[edge + k] ^= 1
        pads.append(s)
    return pads[0], pads[1], solve_ms
