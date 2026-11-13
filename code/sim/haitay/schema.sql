-- Haitay PC store (SQLite). Time columns are UTC unix seconds; the dashboard converts to local time.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS app_user (
    user_id      INTEGER PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,
    pin_hash     TEXT,                      -- optional local login
    created_at   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS device (
    device_id    TEXT PRIMARY KEY,
    fw_version   TEXT,
    hw_version   TEXT,
    last_ack     INTEGER NOT NULL DEFAULT 0,
    last_seen    INTEGER
);

CREATE TABLE IF NOT EXISTS session (
    session_id   INTEGER PRIMARY KEY,
    device_id    TEXT NOT NULL REFERENCES device(device_id),
    session_no   INTEGER NOT NULL,          -- u8 from the device, wraps at 255
    first_seq    INTEGER NOT NULL,          -- disambiguates wrapped session_no
    user_id      INTEGER REFERENCES app_user(user_id),
    started_at   INTEGER,
    UNIQUE (device_id, first_seq)
);
CREATE INDEX IF NOT EXISTS idx_session_user ON session(user_id, started_at);

CREATE TABLE IF NOT EXISTS solve (
    device_id    TEXT NOT NULL REFERENCES device(device_id),
    seq          INTEGER NOT NULL,
    session_id   INTEGER NOT NULL REFERENCES session(session_id),
    time_ms      INTEGER NOT NULL,
    penalty      INTEGER NOT NULL DEFAULT 0,  -- 0 OK, 1 +2, 2 DNF
    deleted      INTEGER NOT NULL DEFAULT 0,
    ts           INTEGER NOT NULL,
    ts_estimated INTEGER NOT NULL DEFAULT 0,  -- 1 if the RTC was unset and ts was inferred
    edit_seq     INTEGER NOT NULL DEFAULT 0,  -- last edit applied, makes replays idempotent
    PRIMARY KEY (device_id, seq)              -- deduplication key of the sync protocol
);
CREATE INDEX IF NOT EXISTS idx_solve_session_ts ON solve(session_id, ts);

CREATE TABLE IF NOT EXISTS sync_log (
    sync_id      INTEGER PRIMARY KEY,
    device_id    TEXT NOT NULL REFERENCES device(device_id),
    started_at   INTEGER NOT NULL,
    frames_ok    INTEGER NOT NULL DEFAULT 0,
    frames_bad   INTEGER NOT NULL DEFAULT 0,
    records_new  INTEGER NOT NULL DEFAULT 0,
    records_dup  INTEGER NOT NULL DEFAULT 0,
    last_ack     INTEGER
);
