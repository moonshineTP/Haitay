"""Feed Wokwi serial output (REC lines) into the PC simulation.

Usage (from the iot folder):  python -I Haitay/code/sim/wokwi_ingest.py <serial.txt>

Each valid record is written raw into a fresh virtual device's FRAM slot, the device boots,
and the real PcService.sync pulls the records into SQLite. The report ends with Ao5, Ao12
and Ao100 recomputed on the PC from the database.
"""
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from haitay import proto, stats  # noqa: E402
from haitay.device import Fram, Nvs, VirtualDevice  # noqa: E402
from haitay.pc import Link, PcService  # noqa: E402

REC_LINE = re.compile(r"^REC ([0-9a-fA-F]{32})\s*$")


def fmt(ms):
    if ms is None:
        return "undefined"
    return "DNF" if ms == stats.DNF else f"{ms / 1000:.2f} s"


def parse(path):
    """Return (records by seq, crc_failures, parsed line count). Later duplicates replace earlier ones."""
    by_seq, bad, parsed = {}, 0, 0
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = REC_LINE.match(line.strip())
            if not m:
                continue
            parsed += 1
            raw = bytes.fromhex(m.group(1))
            rec = proto.unpack(raw)
            if rec is None:
                bad += 1
                continue
            by_seq[rec["seq"]] = (raw, rec)
    return by_seq, bad, parsed


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    by_seq, bad, parsed = parse(argv[1])
    print(f"records parsed: {parsed}")
    print(f"CRC failures: {bad}")
    if not by_seq:
        return 1

    # Keep the contiguous run that starts at the lowest seq; a hole would stall the PC's resume logic.
    first = min(by_seq)
    seqs = [first]
    while seqs[-1] + 1 in by_seq:
        seqs.append(seqs[-1] + 1)
    if len(seqs) < len(by_seq):
        print(f"warning: gap after seq {seqs[-1]}, {len(by_seq) - len(seqs)} later records skipped")
    seqs = seqs[-VirtualDevice.SLOTS:]  # a ring only holds the newest SLOTS records

    work = os.path.join(ROOT, "tmp", "sim", "wokwi-" + time.strftime("%Y%m%d-%H%M%S"))
    os.makedirs(work, exist_ok=True)
    fram = Fram(os.path.join(work, "fram.bin"))
    for s in seqs:
        fram.write(((s - 1) % VirtualDevice.SLOTS) * proto.REC_SIZE, by_seq[s][0])
    Nvs(os.path.join(work, "nvs.json")).set("last_ack", seqs[0] - 1)  # earlier seqs count as synced
    dev = VirtualDevice(work, device_id="HT-WOKWI", rtc_valid=False)  # boot() scans the ring
    # boot_id of the sketch is 1, equal to the fresh device's, so unset timestamps convert exactly
    # when the device clock stands at the newest record's uptime.
    dev.uptime_s = max(by_seq[s][1]["ts"] & 0xFFFFF for s in seqs)

    pc = PcService(os.path.join(work, "pc.sqlite"))
    user = pc.create_user("wokwi")
    now = int(time.time())
    rep = pc.sync(Link(dev), user, now)

    rows = pc.db.execute("SELECT COUNT(*) FROM solve").fetchone()[0]
    times = [stats.effective(t, p) for _, t, p, _ in pc.solves(user)]
    print(f"sync: new {rep['new']}, dup {rep['dup']}, bad frames {rep['frames_bad']}, acked {rep['acked']}")
    print(f"rows in SQLite: {rows}")
    print(f"Ao5: {fmt(stats.average_of(times, 5))}")
    print(f"Ao12: {fmt(stats.average_of(times, 12))}")
    print(f"Ao100: {fmt(stats.average_of(times, 100))}")
    print("database: " + os.path.relpath(os.path.join(work, "pc.sqlite"), ROOT))  # ASCII-safe on cp1252
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
