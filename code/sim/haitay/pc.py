"""PC side: simulated BLE link and the ingest service over SQLite.

Rule of the protocol: the PC acknowledges a seq only after the transaction that holds
it has committed, and the acknowledged prefix never has holes.
"""
import os
import sqlite3
import struct

from . import proto, stats


class LinkDropped(Exception):
    pass


class Link:
    """BLE link model. drop_after: frames delivered before the link drops.
    corrupt: index of a frame whose payload gets one flipped byte."""

    def __init__(self, device, drop_after=None, corrupt=None, lose_ack=None):
        self.dev, self.drop_after, self.corrupt = device, drop_after, corrupt
        self.lose_ack = lose_ack  # index of an ACK write that never reaches the device
        self.frames_sent, self.acks = 0, 0

    def read_info(self):
        return self.dev.read_info()

    def read_state(self):
        return self.dev.read_state()

    def write(self, data):
        if data[0] == proto.CMD_ACK:
            self.acks += 1
            if self.lose_ack == self.acks - 1:
                self.lose_ack = None
                raise LinkDropped("ack lost")  # PC committed, device never heard the ACK
        return self.dev.write_control(data)

    def stream(self):
        for i, frame in enumerate(self.dev.sync_frames()):
            if self.drop_after is not None and i >= self.drop_after:
                self.drop_after = None  # the next connection works
                raise LinkDropped(i)
            if self.corrupt == i:
                self.corrupt = None
                frame = frame[:5] + bytes([frame[5] ^ 0x40]) + frame[6:]
            self.frames_sent += 1
            yield frame


class PcService:
    def __init__(self, db_path):
        fresh = not os.path.exists(db_path)
        self.db = sqlite3.connect(db_path)
        if fresh:
            here = os.path.dirname(__file__)
            self.db.executescript(open(os.path.join(here, "schema.sql")).read())

    def create_user(self, name, now=0):
        cur = self.db.execute("INSERT INTO app_user(name, created_at) VALUES (?, ?)", (name, now))
        self.db.commit()
        return cur.lastrowid

    # ---- sync ---------------------------------------------------------------
    def sync(self, link, user_id, now, max_attempts=5):
        """Run SYNC until END arrives intact. Returns a per-call report."""
        report = {"attempts": 0, "frames_ok": 0, "frames_bad": 0, "drops": 0,
                  "new": 0, "dup": 0, "acked": None}
        for _ in range(max_attempts):
            report["attempts"] += 1
            try:
                if self._sync_once(link, user_id, now, report):
                    return report
            except LinkDropped:
                report["drops"] += 1  # reconnect and resume from last_ack + 1
        return report

    def _sync_once(self, link, user_id, now, rep):
        info, state = link.read_info(), link.read_state()
        dev = info["device_id"]
        self.db.execute("INSERT INTO device(device_id, fw_version, hw_version, last_seen) "
                        "VALUES (?,?,?,?) ON CONFLICT(device_id) DO UPDATE SET "
                        "fw_version=excluded.fw_version, last_seen=excluded.last_seen",
                        (dev, info["fw"], info["hw"], now))
        self.db.commit()
        link.write(proto.cmd(proto.CMD_SET_TIME, now))
        expected = state["last_ack"] + 1
        link.write(proto.cmd(proto.CMD_SYNC))
        for frame in link.stream():
            if frame[0] == proto.FRAME_END:
                last = struct.unpack("<I", frame[1:5])[0]
                return expected - 1 >= last
            n = frame[1]
            raws = [frame[2 + 16 * i: 18 + 16 * i] for i in range(n)]
            recs = [proto.unpack(r) for r in raws]
            if any(r is None for r in recs) or [r["seq"] for r in recs] != list(
                    range(expected, expected + n)):
                rep["frames_bad"] += 1
                return False  # stop acking; re-SYNC resumes after the last good frame
            with self.db:  # one transaction per frame, ACK only after COMMIT
                for r in recs:
                    self._apply(dev, r, user_id, state, now, rep)
                self.db.execute("UPDATE device SET last_ack=? WHERE device_id=?",
                                (recs[-1]["seq"], dev))
            link.write(proto.cmd(proto.CMD_ACK, recs[-1]["seq"]))
            rep["frames_ok"] += 1
            rep["acked"] = recs[-1]["seq"]
            expected = recs[-1]["seq"] + 1
        return False

    def _resolve_ts(self, dev, r, state, now):
        if not r["flags"] & proto.F_TIME_UNSET:
            return r["ts"], 0
        boot, up = r["ts"] >> 20, r["ts"] & 0xFFFFF
        if boot == state["boot_id"]:  # same power-on: exact conversion from uptime
            return now - (state["uptime_s"] - up), 0
        row = self.db.execute("SELECT ts FROM solve WHERE device_id=? AND seq<? "
                              "ORDER BY seq DESC LIMIT 1", (dev, r["seq"])).fetchone()
        return (row[0] if row else now), 1  # older boot: estimate from the previous solve

    def _session_for(self, dev, r, user_id, ts):
        row = self.db.execute("SELECT session_id, session_no FROM session WHERE device_id=? "
                              "AND first_seq<=? ORDER BY first_seq DESC LIMIT 1",
                              (dev, r["seq"])).fetchone()
        if row and row[1] == r["session"]:
            return row[0]
        return self.db.execute("INSERT INTO session(device_id, session_no, first_seq, user_id, "
                               "started_at) VALUES (?,?,?,?,?)",
                               (dev, r["session"], r["seq"], user_id, ts)).lastrowid

    def _apply(self, dev, r, user_id, state, now, rep):
        if r["flags"] & proto.F_EDIT:
            cur = self.db.execute(
                "UPDATE solve SET penalty=?, deleted=?, edit_seq=? WHERE device_id=? AND seq=? "
                "AND edit_seq<?", (r["flags"] & proto.PEN_MASK, int(bool(r["flags"] & proto.F_DELETED)),
                                   r["seq"], dev, r["time_ms"], r["seq"]))
            rep["new" if cur.rowcount else "dup"] += 1
            return
        if self.db.execute("SELECT 1 FROM solve WHERE device_id=? AND seq=?",
                           (dev, r["seq"])).fetchone():
            rep["dup"] += 1
            return
        ts, est = self._resolve_ts(dev, r, state, now)
        sid = self._session_for(dev, r, user_id, ts)
        self.db.execute("INSERT INTO solve(device_id, seq, session_id, time_ms, penalty, ts, "
                        "ts_estimated) VALUES (?,?,?,?,?,?,?)",
                        (dev, r["seq"], sid, r["time_ms"], r["flags"] & proto.PEN_MASK, ts, est))
        rep["new"] += 1

    # ---- queries used by the dashboard API ------------------------------------
    def solves(self, user_id, ts_from=0, ts_to=2**31):
        return self.db.execute(
            "SELECT s.seq, s.time_ms, s.penalty, s.ts FROM solve s JOIN session x "
            "ON s.session_id=x.session_id WHERE x.user_id=? AND s.deleted=0 AND s.ts BETWEEN ? AND ? "
            "ORDER BY s.ts, s.seq", (user_id, ts_from, ts_to)).fetchall()

    def rolling(self, user_id, n, **kw):
        rows = self.solves(user_id, **kw)
        times = [stats.effective(t, p) for _, t, p, _ in rows]
        return [ts for *_, ts in rows], stats.rolling(times, n)
