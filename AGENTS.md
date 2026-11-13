# Haitay

Haitay is a speedcubing timer (two touch pads, on-device Ao stats, BLE sync) plus a PC service (long-term per-user storage, dashboard). It is a group project for HUST IT4735 "IoT và ứng dụng" (class 175680, lecturer Ts. Đặng Tuấn Linh), group "Hai Người": Phạm Gia Hưng (20230036), Đỗ Trường Giang (20235066), Dương Thanh Minh (20230047), Nguyễn Anh Bảo (20220014). Title pages list all four; keep `titlepage.tex`, `titlepage-bai5.tex`, and `titlepage-bai.tex` in step.

## Folders

Each folder has its own `AGENTS.md` with the rules for that topic.

- `writing/`: LaTeX report, the graded written deliverable.
- `reports/`: research notes and the prior-art report; the evidence base for design choices.
- `code/`: device firmware and PC service. Empty so far.
- `presentation/`: defense slides and demo script. Empty so far.
- `scripts/`: project-level helper scripts. Empty so far.
- `tmp/`: scratch; nothing here is a source of truth.
- `../materials/`: course PDFs (IT4735 Ch1, Ch2.1, Ch5). The Read tool reports them "password-protected" but they are not encrypted; extract text with `pypdf` and print through `sys.stdout.buffer` (the Windows console breaks on Vietnamese).

## Course mapping

- Chapter 2 of the report: 2.1 general description, 2.2 context (Stackmat, later WCA rules), 2.3 device layer, then the PC software layer and the communication technology choice. Assignment Bài 4 (topic, functional and non-functional requirements) is `chap1`. Bài 5 is a separate document covering 2.1 to 2.3. Bài 6 is sections 2.1 and 2.4 only, where 2.4 is the communication technology choice (Bluetooth LE). Homework submissions are built from chapter 2 alone, apart from the full report.
- The course grades the reasoning: each technical choice states why and names at least one rejected alternative. Sensors are justified on five criteria: accuracy, durability, power, cost, operating environment.

## Domain rules

- Haitay is a practice timer and is not on the WCA Approved Timer List; never claim competition legality.
- Averages are csTimer-style: effective time is `t`, `t + 2000 ms` for +2, infinity for DNF; trim `ceil(5% * n)` from each end (1 for Ao5 and Ao12, 5 for Ao100); fewer than `n` solves is undefined; compute from stored milliseconds.
- State novelty as "not found in searched sources". Keep the evidence tags ([UNVERIFIED], [SNIPPET], [EST], [OWN CALC]) when quoting numbers from the prior-art report.

## Team decisions

These settle earlier conflicts between `chap1` and the prior-art report. Follow them; ask before changing one.

- Latency: the theoretical target is timing resolution under 0,001 s. Absolute delay is hard to measure without a complex reference, so a touch detection delay of 2 to 10 ms is accepted. Write both numbers and keep them distinct.
- Power: the minimum option. The device runs on USB-C 5 V from a charger or power bank, with no battery powering it, no 15 V rail, and no battery-level reporting. A CR2032 coin cell exists only to hold the DS3231 real-time clock.
- Arming: both pads touched continuously for 1.5 s.
- Ao100: computed on the device and on the PC. The device keeps more than 100 recent solves.
- Input: like Stackmat, arming and stopping need both hands on the pads, and timing starts when at least one hand lifts (WSSA StackMat Pro rule). Touch hysteresis and debounce must be handled well.
- Time: `unix_ts` comes from a DS3231 RTC. The PC sends `SET_TIME` at each connection to set and correct it; records made while the clock is unset carry a flag and are converted after the next `SET_TIME`.
- Hardware baseline in chapter 2: ESP32-S3-WROOM-1 N8 (STM32WB55 as the durability-first alternative, which also has a VBAT pin that would replace the DS3231), FRAM FM24CL64B for the solve log, flash with LittleFS as fallback. Quote only figures verified from primary sources.
- Identity: the device stores no user information, only sessions and relative-time data. Users exist on the PC, which attaches sessions to a user at sync; authentication there is optional. Do not claim the system needs no password or login.
- Scope: one device, one PC, local only. Never introduce cloud, multi-device, or network sharing.
