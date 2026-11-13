"""Mechanism ablations: remove one design mechanism at a time and measure what breaks.

Usage (from Haitay/):  python -I code/sim/run_ablations.py
Each ablation reuses the scenario of run_scenarios.py that exercises the mechanism.
Results go to code/sim/out/ablations.json.
"""
import json
import os
import random
import struct
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")  # Vietnamese labels on a cp1252 console

from haitay import proto  # noqa: E402
from haitay.device import PowerCut, TimingCore, VirtualDevice, hand_trace  # noqa: E402
from haitay.pc import Link, LinkDropped, PcService  # noqa: E402

RUN = time.strftime("%Y%m%d-%H%M%S")
WORK = os.path.join(ROOT, "tmp", "sim", "abl-" + RUN)
T0 = 1_791_849_600
out = {}


def report(key, baseline, ablated, broken):
    out[key] = {"baseline": baseline, "ablated": ablated, "requirement_broken": broken}
    print(f"{key}: baseline={baseline} ablated={ablated} -> {broken}")


def a1_no_debounce(rng, n=200):
    """Debounce 3 samples vs 1 sample, same chattering traces."""
    def bad_count(debounce):
        core, bad = TimingCore(debounce=debounce), 0
        r = random.Random(7)
        for _ in range(n):
            true_ms = r.randint(3000, 12000)
            left, right, _ = hand_trace(r, true_ms)
            start, stop, _ = core.run(left, right)
            bad += start is None or stop is None or abs((stop - start) - true_ms) > 10
        return bad
    report("A1 no debounce", f"{bad_count(3)}/{n} sai", f"{bad_count(1)}/{n} sai", "N2, N3")


class AckFirstPc(PcService):
    """Ablation A2: ACK is written before the transaction commits; the PC dies in between once."""
    crash_at = 3

    def _sync_once(self, link, user_id, now, rep):
        info, state = link.read_info(), link.read_state()
        dev = info["device_id"]
        self.db.execute("INSERT OR IGNORE INTO device(device_id) VALUES (?)", (dev,))
        link.write(proto.cmd(proto.CMD_SYNC))
        for i, frame in enumerate(link.stream()):
            if frame[0] == proto.FRAME_END:
                return True
            recs = [proto.unpack(frame[2 + 16 * k: 18 + 16 * k]) for k in range(frame[1])]
            link.write(proto.cmd(proto.CMD_ACK, recs[-1]["seq"]))  # ACK first
            if i == self.crash_at:
                self.crash_at = None
                self.db.rollback()
                raise LinkDropped("PC process died before COMMIT")
            with self.db:
                for r in recs:
                    self._apply(dev, r, user_id, state, now, rep)
        return False


def a2_ack_first(rng):
    def lost(cls, tag):
        dev = VirtualDevice(os.path.join(WORK, tag), rtc_valid=True)
        pc = cls(os.path.join(WORK, tag, "pc.sqlite"))
        u = pc.create_user("A")
        for _ in range(100):
            dev.record_solve(rng.randint(15000, 30000))
        link = Link(dev, lose_ack=3) if cls is PcService else Link(dev)
        pc.sync(link, u, T0)
        return 100 - pc.db.execute("SELECT COUNT(*) FROM solve").fetchone()[0]
    report("A2 ACK before COMMIT", f"mất {lost(PcService, 'a2b')} bản ghi",
           f"mất {lost(AckFirstPc, 'a2a')} bản ghi", "N5, F5")


def a3_inplace_edit(rng, trials=200):
    """Power cut while editing a committed record: in-place rewrite vs append-only edit record."""
    lost_inplace = lost_append = 0
    for t in range(trials):
        cut = rng.randint(0, 15)
        for mode in ("inplace", "append"):
            dev = VirtualDevice(os.path.join(WORK, f"a3-{mode}-{t}"), rtc_valid=True)
            for _ in range(10):
                dev.record_solve(rng.randint(15000, 30000))
            target = dev.records[5]
            try:
                if mode == "inplace":
                    raw = proto.pack(5, target["time_ms"], target["ts"], target["session"],
                                     target["flags"] | proto.PEN_PLUS2)
                    dev.fram.write(4 * proto.REC_SIZE, raw, cut_after=cut)
                else:
                    dev._append(5, proto.F_EDIT | proto.PEN_PLUS2, cut_after=cut)
            except PowerCut:
                pass
            dev = VirtualDevice(os.path.join(WORK, f"a3-{mode}-{t}"), rtc_valid=True)
            gone = sum(1 for s in range(1, 11) if s not in dev.records)
            if mode == "inplace":
                lost_inplace += gone
            else:
                lost_append += gone
    report("A3 in-place edit", f"{lost_append} lượt đã chốt bị mất / {trials} lần cắt điện",
           f"{lost_inplace} lượt đã chốt bị mất / {trials} lần cắt điện", "N4")


def a4_no_crc(rng, trials=200):
    """Torn writes over acknowledged slots: how many garbage records would pass without a CRC."""
    def unpack_nocrc(raw):
        seq, time_ms, ts, session, flags, _ = proto.REC.unpack(raw)
        return None if seq == 0 else seq
    dev = VirtualDevice(os.path.join(WORK, "a4"), rtc_valid=True)
    pc = PcService(os.path.join(WORK, "a4", "pc.sqlite"))
    u = pc.create_user("A")
    caught = accepted = 0
    for _ in range(trials):
        for _ in range(rng.randint(3, 8)):
            dev.record_solve(rng.randint(15000, 30000))
        pc.sync(Link(dev), u, T0)
        seq = dev.head + 1
        slot = (seq - 1) % dev.SLOTS
        try:
            dev.record_solve(rng.randint(15000, 30000), cut_after=rng.randint(1, 15))
        except PowerCut:
            pass
        raw = dev.fram.read(slot * 16, 16)
        torn = proto.unpack(raw) is None and raw != bytes(16)
        caught += torn
        accepted += torn and unpack_nocrc(raw) is not None  # would pass as a record without CRC
        dev = VirtualDevice(os.path.join(WORK, "a4"), rtc_valid=True)
    report("A4 no CRC", f"0 bản ghi rác được nhận ({caught} lần ghi dở bị CRC chặn)",
           f"{accepted} bản ghi rác được nhận", "N4")


def a5_no_key(rng):
    dev = VirtualDevice(os.path.join(WORK, "a5"), rtc_valid=True)
    pc = PcService(os.path.join(WORK, "a5", "pc.sqlite"))
    u = pc.create_user("A")
    for _ in range(200):
        dev.record_solve(rng.randint(15000, 30000))
    rep = pc.sync(Link(dev, drop_after=7, lose_ack=10), u, T0)
    report("A5 no (device_id, seq) key", "0 bản ghi trùng", f"{rep['dup']} bản ghi trùng", "N5")


def a6_no_rtc(rng):
    """Device keeps time only from SET_TIME: solves made before a sync and then a reboot."""
    dev = VirtualDevice(os.path.join(WORK, "a6"), rtc_valid=False)
    pc = PcService(os.path.join(WORK, "a6", "pc.sqlite"))
    u = pc.create_user("A")
    for _ in range(20):
        dev.tick(60)
        dev.record_solve(rng.randint(15000, 30000))
    dev = VirtualDevice(os.path.join(WORK, "a6"), rtc_valid=False)  # unplugged before syncing
    pc.sync(Link(dev), u, T0)
    est = pc.db.execute("SELECT SUM(ts_estimated) FROM solve").fetchone()[0]
    report("A6 no RTC", "0/20 mốc giờ phải ước lượng (DS3231 giữ giờ)",
           f"{est}/20 mốc giờ phải ước lượng", "Mốc giờ thực cho dashboard")


def main():
    rng = random.Random(20261113)
    os.makedirs(WORK, exist_ok=True)
    for fn in (a1_no_debounce, a2_ack_first, a3_inplace_edit, a4_no_crc, a5_no_key, a6_no_rtc):
        fn(rng)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "ablations.json"), "w", encoding="utf-8") as f:
        json.dump({"run": RUN, "ablations": out}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
