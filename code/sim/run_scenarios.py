"""Run the Haitay simulation scenarios and write results plus report figures.

Usage (from Haitay/):  python -I code/sim/run_scenarios.py
State files go to tmp/sim/<run>/, results to code/sim/out/, figures to writing/figures/.
"""
import json
import math
import os
import random
import statistics
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from haitay import proto, stats  # noqa: E402
from haitay.device import LogFull, PowerCut, TimingCore, VirtualDevice, hand_trace  # noqa: E402
from haitay.pc import Link, PcService  # noqa: E402

RUN = time.strftime("%Y%m%d-%H%M%S")
WORK = os.path.join(ROOT, "tmp", "sim", RUN)
OUT = os.path.join(HERE, "out")
FIG = os.path.join(ROOT, "writing", "figures")
T0 = 1_791_849_600  # 2026-10-13 00:00 UTC, start of the seeded dataset
results = {}


def check(name, ok, **detail):
    results[name] = {"pass": bool(ok), **detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {json.dumps(detail, ensure_ascii=False)}")


def fresh(tag, **kw):
    dev = VirtualDevice(os.path.join(WORK, tag), **kw)
    pc = PcService(os.path.join(WORK, tag, "pc.sqlite"))
    return dev, pc, pc.create_user("A")


def count(pc):
    return pc.db.execute("SELECT COUNT(*) FROM solve").fetchone()[0]


def u0_unit():
    times = [9500, 10200, stats.DNF, 8900, 9800]
    check("U1 Ao5 with one DNF = 9.83 s", stats.average_of(times, 5) == 9830,
          got=stats.average_of(times, 5))
    check("U2 Ao5 with two DNF = DNF", stats.average_of([1, 2, stats.DNF, stats.DNF, 3], 5) == stats.DNF)
    check("U3 Ao5 with 4 solves undefined", stats.average_of([1, 2, 3, 4], 5) is None)
    check("U4 Ao100 trims 5 per side", math.ceil(0.05 * 100) == 5 and
          stats.average_of(list(range(1000, 101000, 1000)), 100) == 50500)
    check("U5 CRC-16/CCITT-FALSE check value", proto.crc16(b"123456789") == 0x29B1)
    check("U6 records per BLE notify at MTU 185", proto.records_per_frame(185) == 11,
          per_frame=proto.records_per_frame(185))


def t1_timing(rng, n=400):
    # the error comes from the two edges only, so short solves keep the 1 kHz loop fast
    core, errs, misses = TimingCore(debounce=3), [], 0
    for _ in range(n):
        true_ms = rng.randint(3000, 12000)
        left, right, _ = hand_trace(rng, true_ms)
        start, stop, _ = core.run(left, right)
        if start is None or stop is None:
            misses += 1
            continue
        errs.append((stop - start) - true_ms)
    a = [abs(e) for e in errs]
    detail = {"n": n, "missed": misses, "mean_ms": round(statistics.mean(errs), 2),
              "sd_ms": round(statistics.stdev(errs), 2), "min_ms": min(errs), "max_ms": max(errs),
              "p95_abs_ms": sorted(a)[int(0.95 * len(a)) - 1]}
    check("T1 timing error within +-10 ms, no missed solve", misses == 0 and max(a) <= 10, **detail)
    # brief two-hand touch of 800 ms must not arm
    left = [0] * 100 + [1] * 800 + [0] * 3000
    s, _, _ = core.run(left, list(left))
    check("T2 touch shorter than 1.5 s does not arm", s is None)
    return errs


def s1_normal(rng):
    dev, pc, ua = fresh("s1", rtc_valid=True)
    for _ in range(120):
        dev.record_solve(rng.randint(15000, 30000))
    rep = pc.sync(Link(dev), ua, T0)
    check("S1 normal sync of 120 solves", count(pc) == 120 and dev.last_ack == 120,
          frames=rep["frames_ok"], acked=rep["acked"])


def s2_drop(rng):
    dev, pc, ua = fresh("s2", rtc_valid=True)
    for _ in range(200):
        dev.record_solve(rng.randint(15000, 30000))
    rep = pc.sync(Link(dev, drop_after=7, lose_ack=10), ua, T0)
    seqs = [r[0] for r in pc.db.execute("SELECT seq FROM solve ORDER BY seq")]
    check("S2 BLE drop and lost ACK: no loss, no duplicate",
          seqs == list(range(1, 201)) and dev.last_ack == 200,
          attempts=rep["attempts"], drops=rep["drops"], resent_dup=rep["dup"], rows=len(seqs))


def s3_power(rng, trials=100):
    lost, phantom, torn = 0, 0, 0
    dev = VirtualDevice(os.path.join(WORK, "s3"), rtc_valid=True)
    pc = PcService(os.path.join(WORK, "s3", "pc.sqlite"))
    ua = pc.create_user("A")
    for i in range(trials):
        for _ in range(rng.randint(3, 8)):
            dev.record_solve(rng.randint(15000, 30000))
        if i % 2:
            pc.sync(Link(dev), ua, T0)  # half the cuts hit a ring that holds unacked records
        committed = {s: dict(r) for s, r in dev.records.items()}
        attempted, cut = dev.head + 1, rng.randint(0, 15)
        try:
            dev.record_solve(12345, cut_after=cut)
        except PowerCut:
            pass
        dev = VirtualDevice(os.path.join(WORK, "s3"), rtc_valid=True)  # reboot: scan the ring
        torn += cut > 0
        phantom += attempted in dev.records
        lost += sum(1 for s, r in committed.items()
                    if s > dev.last_ack and dev.records.get(s) != r)
    check("S3 power cut during write: committed records intact, torn record never valid",
          lost == 0 and phantom == 0, trials=trials, partial_writes=torn,
          committed_lost=lost, torn_accepted_as_valid=phantom)


def s4_malformed(rng):
    dev, pc, ua = fresh("s4", rtc_valid=True)
    for _ in range(60):
        dev.record_solve(rng.randint(15000, 30000))
    rep = pc.sync(Link(dev, corrupt=3), ua, T0)
    check("S4 corrupted frame rejected, then resent", count(pc) == 60 and rep["frames_bad"] == 1,
          frames_bad=rep["frames_bad"], attempts=rep["attempts"])


def s5_full(rng):
    dev, pc, ua = fresh("s5", rtc_valid=True)
    for _ in range(512):
        dev.record_solve(rng.randint(15000, 30000))
    try:
        dev.record_solve(20000)
        refused = False
    except LogFull:
        refused = True
    pc.sync(Link(dev), ua, T0)
    dev.record_solve(20000)
    check("S5 full log refuses solve 513 until sync", refused and dev.head == 513 and count(pc) == 512)


def s6_clock(rng):
    dev, pc, ua = fresh("s6", rtc_valid=False)
    truth = []
    for _ in range(10):
        dev.tick(rng.randint(20, 40))
        dev.record_solve(rng.randint(15000, 30000))
        truth.append(dev.uptime_s)
    now = T0 + 5000
    pc.sync(Link(dev), ua, now)
    got = [r[0] for r in pc.db.execute("SELECT ts FROM solve ORDER BY seq")]
    exact = [now - (dev.uptime_s - u) for u in truth]
    # power-off before any SET_TIME: a new boot cannot convert older-boot records exactly
    dev2, pc2, ub = fresh("s6b", rtc_valid=False)
    for _ in range(3):
        dev2.tick(30)
        dev2.record_solve(20000)
    dev2 = VirtualDevice(os.path.join(WORK, "s6b"), rtc_valid=False)
    pc2.sync(Link(dev2), ub, now)
    est = pc2.db.execute("SELECT SUM(ts_estimated) FROM solve").fetchone()[0]
    check("S6 RTC unset: same-boot records converted exactly, older boot flagged",
          got == exact and est == 3, same_boot_exact=got == exact, older_boot_estimated=est)


def s7_switch(rng):
    dev, pc, ua = fresh("s7", rtc_valid=True)
    ub = pc.create_user("B")
    for _ in range(30):
        dev.record_solve(rng.randint(15000, 30000))
    refused = dev.write_control(proto.cmd(proto.CMD_WIPE)) == "REFUSED_UNSYNCED"
    pc.sync(Link(dev), ua, T0)
    ok = dev.write_control(proto.cmd(proto.CMD_WIPE)) == "OK"
    for _ in range(12):
        dev.record_solve(rng.randint(15000, 30000))
    pc.sync(Link(dev), ub, T0 + 3600)
    per_user = dict(pc.db.execute("SELECT x.user_id, COUNT(*) FROM solve s JOIN session x "
                                  "ON s.session_id=x.session_id GROUP BY x.user_id").fetchall())
    check("S7 user switch: wipe only after ACK, seq continues, data split per user",
          refused and ok and per_user == {ua: 30, ub: 12} and dev.head == 42,
          per_user={"A": per_user.get(ua), "B": per_user.get(ub)}, next_seq=dev.head + 1)


def s8_edit(rng):
    dev, pc, ua = fresh("s8", rtc_valid=True)
    for _ in range(20):
        dev.record_solve(rng.randint(15000, 30000))
    pc.sync(Link(dev), ua, T0)
    dev.edit(5, penalty=proto.PEN_PLUS2)
    dev.edit(7, deleted=True)
    pc.sync(Link(dev, lose_ack=0), ua, T0)  # edits get replayed once
    row5 = pc.db.execute("SELECT penalty FROM solve WHERE seq=5").fetchone()[0]
    row7 = pc.db.execute("SELECT deleted FROM solve WHERE seq=7").fetchone()[0]
    same = dev.stats()["ao12"] == stats.average_of(
        [stats.effective(t, p) for _, t, p, _ in pc.solves(ua)], 12)
    check("S8 edits after sync (+2, delete) replay idempotently; device and PC agree",
          row5 == 1 and row7 == 1 and same, device_ao12=dev.stats()["ao12"])


def seeded(rng, days=90):
    dev, pc, ua = fresh("seed", rtc_valid=True)
    dev.rtc_unix = T0
    level = 26000
    for d in range(days):
        level *= 0.996
        dev.uptime_s = d * 86400 + 19 * 3600
        dev.new_session()
        for _ in range(rng.randint(15, 60)):
            dev.tick(rng.randint(30, 90))
            pen = rng.choices([0, 1, 2], [0.95, 0.03, 0.02])[0]
            dev.record_solve(int(rng.lognormvariate(math.log(level), 0.12)), pen)
        pc.sync(Link(dev), ua, T0 + dev.uptime_s)
    ts, ao5 = pc.rolling(ua, 5)
    _, ao12 = pc.rolling(ua, 12)
    _, ao100 = pc.rolling(ua, 100)
    check("D1 seeded 90-day dataset synced daily", count(pc) == dev.head, solves=count(pc))
    return ts, ao5, ao12, ao100


def figures(errs, ts, ao5, ao12, ao100):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(FIG, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    idx = list(range(1, len(ts) + 1))  # sessions are dense within a day, so plot by solve order

    def series(v):
        return [None if (x is None or x == stats.DNF) else x / 1000 for x in v]

    fig, ax = plt.subplots(figsize=(6.3, 2.8))
    ax.plot(idx, series(ao5), color="#c5dbf4", lw=0.5, label="Ao5")
    ax.plot(idx, series(ao12), color="#2a78d6", lw=0.8, label="Ao12")
    ax.plot(idx, series(ao100), color="#eb6834", lw=1.8, label="Ao100")
    ax.set_xlabel("Số thứ tự lượt solve (90 ngày, đồng bộ mỗi ngày)")
    ax.set_ylabel("Thời gian (s)")
    ax.grid(color="#e1e0d9", lw=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, ncol=3, loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "sim_rolling.png"), dpi=200)

    fig, ax = plt.subplots(figsize=(6.3, 2.4))
    ax.hist(errs, bins=range(-12, 13), color="#2a78d6", edgecolor="white")
    ax.set_xlabel("Sai lệch đo được trừ thời gian thật (ms)")
    ax.set_ylabel("Số lượt solve")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#e1e0d9", lw=0.5)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "sim_timing.png"), dpi=200)


def main():
    rng = random.Random(20261113)
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    u0_unit()
    errs = t1_timing(rng)
    for fn in (s1_normal, s2_drop, s3_power, s4_malformed, s5_full, s6_clock, s7_switch, s8_edit):
        fn(rng)
    ts, ao5, ao12, ao100 = seeded(rng)
    figures(errs, ts, ao5, ao12, ao100)
    passed = sum(r["pass"] for r in results.values())
    summary = {"run": RUN, "passed": passed, "total": len(results), "results": results}
    with open(os.path.join(OUT, "results.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
    print(f"{passed}/{len(results)} passed, run {RUN}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
