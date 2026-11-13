"""Data contract shared by the virtual device and the PC service.

One solve record is 16 bytes, little-endian:
    seq u32 | time_ms u32 | ts u32 | session u8 | flags u8 | crc16 u16
The CRC (CRC-16/CCITT-FALSE) covers the first 14 bytes. seq 0 marks an empty slot.

An edit record reuses the layout: flags carries EDIT, time_ms carries the target seq.
The log is append-only, so a torn write can only damage the newest, uncommitted record.
"""
import struct

REC = struct.Struct("<IIIBBH")
REC_SIZE = REC.size  # 16

# flags
PEN_MASK = 0b11          # 0 OK, 1 +2, 2 DNF
PEN_OK, PEN_PLUS2, PEN_DNF = 0, 1, 2
F_TIME_UNSET = 1 << 2    # ts = (boot_id << 20) | uptime_s instead of unix time
F_DELETED = 1 << 3
F_EDIT = 1 << 4          # edit record: time_ms = target seq

# BLE frames (notify on the Log characteristic)
FRAME_LOG, FRAME_END = 0x10, 0x11
# commands (write on the Control characteristic)
CMD_SYNC, CMD_ACK, CMD_SET_TIME, CMD_WIPE = 0x01, 0x02, 0x03, 0x04

ATT_HEADER = 3


def crc16(data: bytes, crc: int = 0xFFFF) -> int:
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def pack(seq, time_ms, ts, session, flags) -> bytes:
    body = REC.pack(seq, time_ms, ts, session, flags, 0)[:14]
    return body + struct.pack("<H", crc16(body))


def unpack(raw: bytes):
    """Return a dict, or None for an empty slot or a CRC mismatch."""
    seq, time_ms, ts, session, flags, crc = REC.unpack(raw)
    if seq == 0 or crc != crc16(raw[:14]):
        return None
    return {"seq": seq, "time_ms": time_ms, "ts": ts, "session": session, "flags": flags}


def records_per_frame(mtu: int) -> int:
    return (mtu - ATT_HEADER - 2) // REC_SIZE  # 2 bytes: frame type + count


def log_frame(raw_records) -> bytes:
    return bytes([FRAME_LOG, len(raw_records)]) + b"".join(raw_records)


def end_frame(last_seq: int) -> bytes:
    return bytes([FRAME_END]) + struct.pack("<I", last_seq)


def cmd(op: int, arg: int = 0) -> bytes:
    return bytes([op]) + struct.pack("<I", arg)
