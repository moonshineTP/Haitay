# Haitay Wins on Service

*Prior art, domain model, class positioning and project plan for the Haitay speedcubing timer (HUST IT4735 midterm, team of two). Research date 2026-10-08.*

**Bottom line.** Haitay's device is reproducible prior art, so its standing in class comes from the service layer and from measured claims. ESP32 touch-pad timers with BLE have existed since 2020 ([ojdip.net](https://ojdip.net/2020/11/esp32-cube-timer/)), GAN, QiYi and MoYu sell BLE timers with apps, and csTimer, Cubeast and a new Speedsolving.com timer (August 2026) already chart Ao5 to Ao100. No searched source shows the full combination of a standalone two-pad timer, store-and-forward sync with acknowledgement, and a persistent PC time-series service; this is the defensible gap, and it rests on search results only. Cuber pain supports the service, since csTimer users report losing thousands of solves and fighting the audio-jack path. Course rubrics reward a working end-to-end demo, a written spec and measured outcomes more than novelty, so the recommended scope pairs a demo (with a visible MQTT or REST hop) with a validation chapter. At the 8-week baseline the plan holds **121 person-hours of expected effort (plan figure 158 h against 160 h capacity at 10 h/person/week)**, with 6- and 10-week ladders that drop features in a fixed order. Four requirement defects need fixing before build: the 15 V power line, the 0.001 s latency line, the Ao100 location conflict, and the missing numeric acceptance criteria. Haitay is a practice timer because the WCA allows only Approved Timer List timers, and the HUST rubric is unpublished, so the lecturer must confirm team size, weight and demo format.

Evidence tags carried from the notes: [UNVERIFIED] lacks a fetched primary source; [SNIPPET] was seen only in a search summary; [ANECDOTAL] is a blog, forum or single course; [OWN CALC] is the notes' own computation on WCA API data; [INFERENCE] and [EST] mark this report's own reasoning and estimates. Reddit, YouTube and Facebook groups were not mined, and several fetches were model-summarised.

## Prior art and establishment

Every Haitay feature exists somewhere, but the combination was absent from all searched sources. Hardware timers dominate on price and rules, software dominates on analytics, and hobby builds cover the electronics. Novelty therefore sits in the integrated pipeline and its validation.

### Hardware timers

Stackmat is the de facto standard. Gen 1 debuted at World Championship 2003, the WCA adopted Stackmats in 2004, and Gen 2 left the approved list on 1 Feb 2023 ([Speedsolving wiki](https://www.speedsolving.com/wiki/index.php/StackMat); [WCA post](https://www.worldcubeassociation.org/posts/updating-the-official-list-of-approved-timers-october-2021)). The G5 (2021) adds 2-pad and 4-pad modes, 0.2 s hold-to-activate buttons and a 0.5 s lock after each stop. Its output is a reverse-engineered 1200-baud 8N1 serial packet on a 2.5 mm jack: state character, time digits and a checksum, roughly every 0.15 s ([PaddyCo Protocol.md](https://raw.githubusercontent.com/PaddyCo/StackmatTimer/master/Protocol.md); [ledmat](https://jayanth-rajakumar.github.io/ledmat/)). Gen 4 uses a 10-byte packet ([m9aertner](https://github.com/m9aertner/StackMatGen4TimerTeensy)). The line-ending order is unresolved, and Speed Stacks publishes no protocol spec. The timer keeps only best stacking times, with no wireless link and no app ([Speed Stacks G5](https://www.speedstacks.com/store/retail/speed-stacks-g5-timer/)).

| Timer | Price | On-device memory | Link and app | WCA | Sources |
|---|---|---|---|---|---|
| Speed Stacks G5 | USD 29.99; 900,000-950,000 VND | Best stacking times only | Data port, 1200-baud serial; no wireless | Approved (2-pad now, 4-pad from 2 Jan 2027) | [Speed Stacks](https://www.speedstacks.com/store/retail/speed-stacks-g5-timer/); [H2 Rubik](https://rubikonline.vn/speedstacks-g5-pro-timer-dong-ho-bam-gio-rubik-cao-cap); [thegioirubik](https://thegioirubik.com/danh-muc/phu-kien/timer/) |
| GAN Halo Smart Timer | USD 39.99-55; older GAN Smart Timer 680,000-750,000 VND | 10,000 results offline, auto Ao5 (older model holds 5) | BLE to CubeStation app and cloud | No | [Cubelelo](https://www.cubelelo.com/products/gan-halo-timer-smart); [GAN](https://www.gancube.com/products/gan-smart-timer) |
| QiYi Smart Timer | USD 13-20; 220,000-412,500 VND | Ao5/Ao12 on device; capacity not stated | BLE, Smart Player app with cloud and trends | No | [SpeedCubeShop](https://speedcubeshop.com/products/qiyi-smart-timer-bluetooth-xuanwu); [ZyO](https://zyorubik.com/products/phu-kien-rubik-qiyi-smart-timer-new-2023-thiet-bi-bam-gio-hang-qiyi-thong-minh-ket-noi-bluetooth-zyo-rubik) |
| MoYu AI timer | USD 11.95-13.46 | Not stated | BLE, WCU Cube app; reviewers report app failures | No | [SpeedCubeShop](https://speedcubeshop.com/products/moyu-ai-bluetooth-timer) |
| Basic touch timers | 115,000-235,000 VND | None | None | No | [websosanh.vn](https://websosanh.vn/s/gi%E1%BB%9D+rubik.htm) (aggregator summary, [SNIPPET]) |

Stackmat complaints recur: thumb resets between the pads on Gen 2 to 4, failures to stop or start on Gen 3, and low-battery glitches such as 8:88.888 ([Speedsolving wiki](https://www.speedsolving.com/wiki/index.php/StackMat); [G5 issues](https://www.speedsolving.com/threads/g5-stackmat-issues.89767/)). Forum claims vary by hardware version.

### Open-source and DIY builds

About ten repositories and posts exist, in three buckets: Stackmat decoders and displays, BLE bridges or minimal timers, and one richer companion.

| Project | Hardware | What it does | Maturity | Link |
|---|---|---|---|---|
| tibordp/cube-timer + ojdip.net blog (2020) | ESP32, 1 capacitive pad, SH1106 OLED | BLE GATT notify, Web Bluetooth demo; no on-device stats | MIT, 5 commits | [repo](https://github.com/tibordp/cube-timer); [blog](https://ojdip.net/2020/11/esp32-cube-timer/) |
| xoseperez/wisblock-smartcube-companion (2023) | nRF52840, touch TFT | PB, Ao5, Ao12, 4 users, 6 puzzles, smart cubes, Stackmat UART; no PC sync | GPL-3.0, 15 stars | [repo](https://github.com/xoseperez/wisblock-smartcube-companion) |
| liusonwood/StackmatLink | ESP32-S3 | Stackmat audio to BLE emulating a GAN timer for csTimer | MIT, updated 25 May 2026 | [repo](https://github.com/liusonwood/StackmatLink) |
| m9aertner/StackMatGen4TimerTeensy | Teensy-LC | Gen 4 packet decoder with OLED or LED display | MIT, 2020 | [repo](https://github.com/m9aertner/StackMatGen4TimerTeensy) |
| PaddyCo/StackmatTimer, ledmat, StackHack | AVR, Arduino | Stackmat decoders and large displays | MIT, small | [PaddyCo](https://github.com/PaddyCo/StackmatTimer); [ledmat](https://jayanth-rajakumar.github.io/ledmat/) |

The two closest references are tibordp (touch plus BLE plus OLED, no stats) and wisblock (multi-user stats, no sync). Searches for RP2040, STM32, Wi-Fi or time-series cube-timer repositories found none; this is a negative search result, not proof of absence. Academic work is thin: one ASU thesis covers a smart-cube app platform ([ASU](https://keep.lib.asu.edu/items/187330)), and no Vietnamese thesis or capstone turned up. HUST, UET and PTIT repositories were not searched.

### Software and smart-cube layer

| Tool | Provides | Gap versus Haitay | Link |
|---|---|---|---|
| csTimer (GPL-3.0) | Stackmat input, ao5/ao12, per-session trend, multi-session, manual backup | Data lives in browser storage; no cross-session long averages (issues #34, #40) | [cstimer.net](https://www.cstimer.net/); [#40](https://github.com/cs0x7f/cstimer/issues/40); [#34](https://github.com/cs0x7f/cstimer/issues/34) |
| Speedsolving.com timer (thread 2 Aug 2026) | Accounts, batched server sync, best Ao12 over 30d/90d/1y, PBs Ao5-Ao100, heatmap, histogram | No hardware, no Stackmat or Bluetooth mention | [thread](https://www.speedsolving.com/threads/new-speedsolving-timer.97451/) |
| Sub-X | AO100/AO12, SD, 14-day slope, forecast, AI report, csTimer import | Closest operational-analytics competitor; no device | [subx.guru](https://subx.guru/) |
| Cubeast | Smart-cube step analysis, external timers incl. Stackmat | Closed source [UNVERIFIED]; 2026 status unverified | [thread](https://www.speedsolving.com/threads/cubeast-a-speedcubing-timer-for-bluetooth-cubes-with-support-for-all-bluetooth-cubes-all-timers-and-all-major-solving-methods.77406/) |
| CubeProgression, CubeDesk | csTimer-export charts; hosted accounts and stats | Software only | [CubeProgression](https://github.com/jjangsangy/CubeProgression); [CubeDesk](https://github.com/kash/cubedesk) |

Smart-cube protocols are all reverse-engineered. GAN Gen2 to 4 and MoYu32 use AES with MAC-derived keys, QiYi uses a fixed-key AES-ECB, GoCube is plain, and Giiker uses light obfuscation ([cubing.js](https://github.com/cubing/cubing.js); [gan-web-bluetooth](https://github.com/afedotov/gan-web-bluetooth); [MAC FAQ](https://gist.github.com/afedotov/52057533a8b27a0277598160c384ae71)). Web Bluetooth works in Chromium only, with no Firefox or Safari support, and needs HTTPS plus a user gesture ([caniuse](https://caniuse.com/web-bluetooth); [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API)). No ready-made ESP32 GAN-cube project turned up.

### WCA constraints

Haitay cannot compete officially. Regulation 7f1a requires "an approved timer from the Approved Timer List", which secondary sources reduce to Speed Stacks G3, G4 and G5; the list PDF itself was unreadable ([WCA Regulations](https://raw.githubusercontent.com/thewca/wca-regulations/official/wca-regulations.md); [Speedcubers Digest](https://www.speedcubersdigest.com/p/wca-to-implement-4-pad-timers-starting)). Puzzles with electronic components are banned (3a4), so smart cubes are practice-only. From **2 Jan 2027** official attempts need a G5 in 4-pad mode ([WCA post](https://www.worldcubeassociation.org/posts/adoption-of-4-pad-timing-august-2026)). Times under 10 minutes are truncated to hundredths (9f1), so competition resolution is 10 ms. No certification path for third-party timers was found. The inspection rules (15 s, +2 at 15 s, DNF at 17 s, premature stop under 0.06 s) are the reference behaviour for any inspection mode.

### Feature-gap matrix

| Capability | Established prior art | Haitay stance |
|---|---|---|
| Two-pad hands-on timer | Stackmat, GAN, QiYi; tibordp (1 pad) | Table stakes |
| Touch hysteresis, BLE notify, OLED | tibordp 2020 | Table stakes |
| Device Ao5 / Ao12 | GAN, QiYi, wisblock | Table stakes |
| Device Ao100 | None found on a standalone device | Weak gap, cheap to claim |
| Multi-user local profiles | wisblock (4 users); no commercial timer found | Gap, scoped to one active user plus switch |
| Browser or phone analytics | csTimer, Cubeast, Speedsolving timer, Sub-X, GAN CubeStation | Table stakes; value lies in capture |
| BLE to browser logging | tibordp, StackmatLink, gan-web-bluetooth | Table stakes |
| Smart-cube link | csTimer, Cubeast, CubeDesk, CubeRoot; wisblock on an MCU | Established; ESP32 route is Could |
| **Device-side store, acknowledged sync, persistent PC time-series service** | Not found | **Defensible gap** |
| **Open sync protocol with csTimer-compatible export** | Not found (csTimer JSON is the de facto format) | **Defensible gap** |

Absence claims rest on search results. GAN CubeStation may already offer long-term charts, and commercial app internals were not tested.

### Operational pain behind the service claim

Data loss is documented: one csTimer user lost a log of almost 12,000 solves and another wrote "This has happened to me 5 times" ([thread](https://www.speedsolving.com/threads/i-lost-my-cstimer-data.89015/)); another thread reports losses of about 4,000 solves ([thread](https://www.speedsolving.com/threads/cstimer-got-reset.90778/)). Stackmat-to-csTimer setups fail on mic gain, noisy cables and combo jacks ([thread](https://www.speedsolving.com/threads/stackmat-cstimer-issues.80169/)). Cost complaints persist ("Stackmat timers are waaay to overpriced", [thread](https://www.speedsolving.com/threads/should-i-buy-my-son-gen-4-or-gen-5-stackmat-timer.88407/)). These support three service features: capture without a cable, backup that survives browser clearing, and per-user separation on a shared timer. Evidence for a shared-timer club workflow is indirect (school clubs, csTimer session-per-person workarounds).

## Domain model and metrics

A speedcubing session follows a short loop: arm, solve, stop, mark, record, review. Existing tools cover the loop but leave logging to external software. Haitay's objectives, actors and definitions below set the vocabulary for the plan.

### Objectives and actors

| Actor | Objective | Haitay measure |
|---|---|---|
| Solo practicer (csTimer plus Stackmat or keyboard) | Capture every solve; see trends without manual export | Zero manual steps from solve to chart |
| WCA competitor | Practise on a Stackmat-like device | Two-pad arming, optional inspection; not a competition device |
| Child plus parent | Visible progress for the buyer | Dashboard by period, PB events |
| School club (shared equipment) | Many users per timer | User switch with acknowledged wipe |
| Coach | Read a student's history | Read-only dashboard view (no tool found with a formal coach role) |
| Course team | Meet spec with measured evidence | Acceptance numbers in section "Project management layer" |

Vietnam school evidence includes Hanoi club events and class-team contests ([Quang Ngai](https://doanthanhnien.vn/tin-tuc/tuoi-tre-sang-tao/quang-ngai-thu-tai-rubik-lan-iii-%E2%80%93-san-choi-toa-sang-tai-nang-tre); club list is a search summary, [UNVERIFIED]).

### Usual workflow end to end

| Step | Practice flow | Competition reference (WCA 2026) |
|---|---|---|
| 1 Setup | Select user and session; scramble from an app | Scrambler, TNoodle, signed scorecard |
| 2 Inspect | Optional 15 s countdown | Under 15 s; judge calls 8 s and 12 s (A3) |
| 3 Arm and start | Both hands on pads; release starts | Timer starts when hands lift (A4d); +2 at 15 s, DNF at 17 s |
| 4 Solve | Timer runs; display updates at about 10 Hz | Release puzzle, then stop |
| 5 Stop | Both hands flat on pads | Premature stop under 0.06 s: extra attempt; 0.06 s or more: DNF (A6b) |
| 6 Mark | OK, +2 or DNF; delete last | Judge records; competitor signs |
| 7 Record | Append to log with sequence number | Score taker enters in WCA Live |
| 8 Review | Ao5, Ao12 on device; trends on PC | Ao5 ranks; truncation to hundredths |
| 9 Sync and switch | Send log, PC acknowledges, device wipes, next user | Not applicable |

Source: [WCA Regulations](https://raw.githubusercontent.com/thewca/wca-regulations/official/wca-regulations.md); practice flow is synthesised from csTimer features and forum practice ([csTimer](https://cstimer.net/)). Training modes in the wild (split timing, PLL drills, daily Ao100 sessions) are phase-level and need smart cubes or splits; they sit outside the Haitay MVP. One community dissent applies to dashboard design: "I sometimes do worse when I'm thinking about big averages", so keep on-device display minimal during a solve ([thread](https://www.speedsolving.com/threads/how-do-you-track-your-solves.78339/)).

### Metric definitions and exact algorithm

The WCA defines only single, Mean of 3 and Average of 5 (best and worst removed, one DNF tolerated, two DNFs make a DNF). Ao12 and Ao100 are community conventions that trim ceil(5%) from each end ([Speedsolving wiki: Average](https://www.speedsolving.com/wiki/index.php/Average); [WCA Regulations Art. 9](https://www.worldcubeassociation.org/regulations/)). Label them "csTimer-style" in the report. The rule below derives from those sources and a third-party csTimer-style reference script ([kana gist](https://gist.github.com/kana/1e96a2300f8479f67d1f208a57f2b9e7)).

1. Effective time: OK = t, +2 = t + 2000 ms, DNF = infinity. Store the penalty separately and compute the effective time once, since csTimer encodes +2 as an additive flag.
2. Take the window of the latest n solves. Fewer than n solves gives undefined (show "-").
3. Set cut = ceil(0.05 n): 1 for Ao5, 1 for Ao12, 5 for Ao100. Sort, then discard the cut smallest and cut largest.
4. If an infinity remains, the result is DNF. Otherwise take the mean of the n - 2 cut survivors and round to centiseconds (integer rule: round(sum_ms / (10 k)), k = n - 2 cut).
5. Current is the latest window. Best is the minimum over windows ending at each solve, with DNF windows excluded.

Edge cases: Ao5 and Ao12 tolerate one DNF, Ao100 tolerates five, and a DNF is trimmed as the slowest value. Example: 9.50, 10.20, DNF, 8.90, 9.80 gives cut 1, sorted 8.90, 9.50, 9.80, 10.20, DNF, survivors 9.50, 9.80, 10.20, mean 29,500 / 3 = 9,833 ms, shown as 9.83. Two DNFs in an Ao5 give DNF. Session mean excludes DNFs, and Mo3 with any DNF is DNF. Ties do not alter the sum. WCA computes from times already truncated to hundredths, whereas csTimer's display rounding is unverified; compute from stored milliseconds and document the choice.

### Devices, aspects and usual milestones

| Aspect | Content | Key decision | Evidence |
|---|---|---|---|
| Hardware | ESP32-S3, copper-foil pads, display, 1S Li-ion, printed case | Native touch with ACTIVE and INACTIVE interrupts; MPR121 as fallback; reject TTP223 (60-220 ms) | [ESP-IDF touch](https://docs.espressif.com/projects/esp-idf/en/v5.4/esp32s3/api-reference/peripherals/touch_pad.html); [TTP223 datasheet](https://files.seeedstudio.com/wiki/Grove-Touch_Sensor/res/TTP223.pdf) |
| Firmware | 1 MHz GPTimer timestamp in ISR; display in a low-priority task | Timing path must not wait on a 15 ms I2C frame | [ojdip.net](https://ojdip.net/2020/11/esp32-cube-timer/); [GPTimer](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gptimer.html) |
| Protocol | One GATT service, seq-numbered records, `ACK(last_seq)` write | Negotiate MTU 185-247 and DLE; delete only after PC fsync | [ESP-FAQ BLE](https://docs.espressif.com/projects/esp-faq/en/latest/software-framework/bt/ble.html) |
| Data | 16-byte record: seq, time_ms, unix_ts, flags, user, CRC16; LittleFS or CRC log | 100,000 solves = 1.6 MB; PC derives Ao values on the fly | [File systems](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/file-system-considerations.html); schema from the notes |
| Analytics | Rolling Ao5/Ao12/Ao100, PB steps, histogram, session compare, heatmap | Session compare and heatmap appear only in open requests or one competitor | [issue #34](https://github.com/cs0x7f/cstimer/issues/34); [cstimer-analyzer #18](https://github.com/Borys35/cstimer-analyzer/issues/18) |
| UX | Large digits, recessed buttons, no button between pads | Show full resolution only at stop | [Speedsolving wiki](https://www.speedsolving.com/wiki/index.php/StackMat) |
| Validation | Timing, power-loss, sync-loss, user trial | Numeric pass criteria written first | Plan below |

Usual milestone shares for hardware plus software work are roughly: requirements and parts 8-10%, module bring-up 18-22%, integration 15-20%, firmware stabilisation 10-15%, app and dashboard 15-20%, testing 10-12%, documentation and rehearsal 10-12% [INFERENCE from COCOMO 81 and course shapes in the notes]. Standard deliverables are hardware, firmware, protocol spec, schema, dashboard, user guide, BOM, conformance table and test log.

## Positioning for class standing

Peer IT4735 projects sit on a known archetype, and course rubrics elsewhere reward evidence over novelty. Haitay wins by combining a conventional pipeline with a real-time claim, an acknowledged-sync guarantee and measured results. The scope below keeps the Must set demonstrable in one sitting.

### What peers build and what rubrics reward

The visible bar is an RFID kiosk: one ESP32, three readers, OLED, FastAPI with paho-mqtt and SQLite, and a React dashboard ([IoT-IT4735 repo](https://github.com/nguyenLTpk/IoT-IT4735)). The 20251 lab repo shows weekly REST, MQTT (HiveMQ), Kafka and ESP32 Wi-Fi provisioning work ([lab repo](https://github.com/hunganh1310/20251-IT4735-IoT-Lab)). Comparable syllabi grade a proposal (5-25%), a midpoint (10-25%), a demo (30-50%) and a report (20-40%), with peer evaluation for individual accountability ([Cornell ECE 4760](https://vanhunteradams.com/Pico/CourseMaterials/Final_Project.html); [Berkeley ME 100](https://tbp.studentorg.berkeley.edu/syllabi/1548/download/); [UVA](https://homa-alem.github.io/teaching/ece_6501/6501_syllabus.pdf)). UVA names "techniques used for design and validation" and "measurable outcomes"; Cornell requires operation "according to a specification you write". Novelty alone is not a listed criterion in these syllabi.

HUST publishes little: IT4735 is 2(2-1-0-4) with a team exercise "building a specific application", and a 2021 lecture slide shows 50% process and 50% final ([SoICT program](https://soict.hust.edu.vn/wp-content/uploads/Bachelor-Computer-Engineering-program.pdf); [2021 slides](https://www.slideshare.net/slideshow/it4735iot-va-ung-dungv2021pdf/262849382), [SNIPPET plus one fetch]). One credit equals 50 learner-hours, so the course totals about 100 hours per student ([HUST regulation](https://soict.hust.edu.vn/wp-content/uploads/QCDT.pdf)). The lecturer's profile leans toward edge AI ([profile](https://soict.hust.edu.vn/ts-dang-tuan-linh.html)), so on-device statistics and trend analysis may be rewarded [INFERENCE].

### How to differ from conventional projects

| Lever | Conventional project | Haitay move |
|---|---|---|
| Claim type | "Works" | Spec with numbers, then measured pass or fail |
| Data path | Publish and display | Idempotent, acknowledged, resumable sync; wipe only after ack |
| Failure handling | Shown on the happy path | Live power-pull and BLE-drop in the demo |
| Analytics | Latest value chart | Rolling Ao lines, PB events, session compare on a seeded 3-month dataset |
| Interop | Closed schema | csTimer-JSON import and export, three third-party tools already read it |
| Accountability | Shared repo | Task table with owners, git log, contribution statement |

### Scope by MoSCoW

Hours are PERT expected values in team person-hours from the WBS (section "Project management layer").

| Priority | Feature | E (h) |
|---|---|---|
| Must | Two-pad touch timing with 1 ms timestamp; display of last time, Ao5, Ao12; OK/+2/DNF and delete; power-safe CRC log; BLE sync with ack to PC; PC ingest, per-user store, rolling-Ao dashboard; USB-C power; validation and report | 143.8 |
| Should | Li-ion battery path (4.3), printed enclosure and pads (8.7), hardware inspection with +2/DNF (7.7), dashboard extras: PB steps, histogram, heatmap, session compare (8.7), csTimer import and export (5.5) | 34.9 |
| Could | Smart-cube link on the PC via Web Bluetooth (18.7), Stackmat bridge mode (11.0) | 29.7 |
| Won't | WCA approval, custom PCB, smart-cube central role on the ESP32, cloud accounts | 0 |

The DSDM guideline limits Must to 60% of capacity ([Agile Business Consortium](https://www.agilebusiness.org/resource/what-is-moscow-prioritization/)). Haitay's Must needs 144 h, which is 72% of a 10-week capacity at 10 h/person/week; the pre-agreed drop ladder replaces the missing margin.

### Reference architecture and minimum demo

Chain: Haitay (BLE GATT peripheral) to a PC bridge (Web Bluetooth page, or Python bleak [UNVERIFIED]) to MQTT or REST to the ingest service to SQLite to the dashboard. The visible hop maps to the course's REST and MQTT labs, so the BLE design keeps a course-taught protocol on the data path. Keep the smart cube on the PC, because GAN needs AES plus MAC extraction and no ESP32 precedent exists.

Minimum end-to-end demo script (8 minutes):

1. Power the device on USB-C for user A, then perform 12 real solves; show time, Ao5, Ao12; mark one DNF and delete one.
2. Cut power during a write, reboot, and show the record count intact.
3. Sync to the PC; drop BLE mid-transfer, reconnect, and show no duplicate or lost sequence numbers.
4. Switch to user B; show the wipe happens after the PC acknowledgement.
5. Open the dashboard on a seeded 3-month dataset plus today's solves; show rolling Ao5, Ao12, Ao100 and a PB event.
6. Show the Bland-Altman plot of timing error with numbers.

Keep a 60-90 s backup video, a spare assembled board with identical firmware, and a dataset that works without a live device ([demo guide](https://roboticsknowledgebase.com/wiki/robotics-project-guide/demo-day/) [ANECDOTAL]).

## Project management layer

The plan is parameterised by the real deadline, because the HUST rubric is unpublished. A single WBS feeds three horizons that differ only in committed scope. Estimates are PERT person-hours for two people, with a 30% reference-class allowance added for planning.

### Prefeasibility by subsystem

| Subsystem | Verdict | Reason |
|---|---|---|
| Timing core (touch, ISR, state machine) | Green | Two hobby builds exist; ISR latency is a few microseconds; sensing delay of 2-10 ms per edge dominates [EST] and is characterisable |
| Display and UI | Green | Decouple from timing; 15 ms I2C frame is harmless in a low-priority task |
| On-device stats | Green | Algorithm fully defined above |
| Power-safe storage | Amber | LittleFS documents power-fail protection, but no source tested brownout on ESP32 |
| BLE peripheral sync | Amber | A first BLE project reportedly overruns 3-10x ([Hubble](https://hubble.com/community/guides/why-your-first-ble-project-won-t-connect-and-how-to-fix-it/), [ANECDOTAL]); MTU, Web Bluetooth gestures, Chromium-only |
| MQTT or REST hop, ingest, DB | Green | Taught in the course labs |
| PC dashboard | Green | Many open-source comparators and a defined chart set |
| Li-ion power with TP4056 | Amber | No power-path charger; protected cell needed; documented as no use while charging |
| Enclosure | Green | Printing costs 700-2,500 VND/g ([Nshop](https://nshopvn.com/dich-vu/in-3d)) |
| Smart-cube link on PC | Amber | Libraries exist; GAN MAC retrieval needs a Chrome flag |
| Smart-cube central role on ESP32 | Red | No precedent, dual-role load unmeasured, AES in firmware |
| Custom PCB | Red | At least 2-week respin penalty and import lead time ([arXiv 1810.07646](https://arxiv.org/pdf/1810.07646), [ANECDOTAL]) |
| "Latency under 0.001 s" as written | Red | Sensor response and debounce are several milliseconds |
| "15 V battery" as written | Red | Everything runs at 3.3 V |
| WCA-legal competition use | Red | Not on the Approved Timer List |

### Technical-risk register

Scales follow the PMBOK example values: probability 0.1/0.3/0.5/0.7/0.9 and impact 0.05/0.1/0.2/0.4/0.8 ([PMI](https://www.pmi.org/learning/library/risk-analysis-decisions-uncertain-times-6686), [SNIPPET]). Ratings are team-level judgement [EST]; no published failure rates exist.

| # | Risk | P | I | P x I | Mitigation |
|---|---|---|---|---|---|
| R1 | "Under 0.001 s" graded literally | 0.7 | 0.8 | 0.56 | Rewrite spec as 1 ms resolution plus measured delay; lecturer sign-off in week 1 |
| R2 | Schedule overrun (30-40% average in surveys) | 0.7 | 0.4 | 0.28 | PERT plus 30% allowance, weekly burn-down, drop ladder |
| R3 | BLE bring-up overrun | 0.5 | 0.4 | 0.20 | Early GATT test in week 3, one packed characteristic, 1-week timebox, Wi-Fi MQTT fallback |
| R4 | Touch false triggers or missed releases | 0.5 | 0.4 | 0.20 | Hysteresis, per-edge debounce, two-pad AND arming, foil pads, MPR121 fallback |
| R5 | Lecturer mismatch (BLE off the taught stack; no rubric) | 0.5 | 0.4 | 0.20 | Visible MQTT or REST hop; ask the questions in section "Open questions" |
| R6 | Team capacity falls below 10 h/person/week | 0.5 | 0.4 | 0.20 | Pre-agreed ladder; trigger at week-4 gate |
| R7 | Storage corruption on power loss | 0.3 | 0.4 | 0.12 | CRC log, commit marker last, brownout detector, 50-100 cut test |
| R8 | Demo-day failure (laptop BLE variance) | 0.3 | 0.4 | 0.12 | Frozen demo laptop, backup video, seeded data, spare board |
| R9 | Web Bluetooth variance and pairing gestures | 0.5 | 0.2 | 0.10 | Chromium on the demo laptop; test weekly |
| R10 | Parts lead time or DOA | 0.5 | 0.2 | 0.10 | Order domestic in week 1; buy two of each module |
| R11 | Scope creep to smart cube | 0.5 | 0.2 | 0.10 | Could list; freeze gate at about 75-80% of calendar |
| R12 | "csTimer already does this" challenge | 0.5 | 0.2 | 0.10 | Frame as hardware-to-account pipeline; show feature-gap matrix |
| R13 | ISR timing spikes with BLE or flash cache | 0.3 | 0.2 | 0.06 | IRAM ISR, GPTimer capture, BLE on the other core |
| R14 | Li-ion charging without power path | 0.3 | 0.2 | 0.06 | Protected cell, no use-while-charging claim, or 5 V bank |
| R15 | Data wiped before PC saved | 0.1 | 0.4 | 0.04 | Ack after PC fsync; resend from `acked_seq + 1` |

### Work breakdown and PERT estimates

E = (O + 4M + P) / 6 and SD = (P - O) / 6, in team person-hours ([PMA PERT note](https://projectmanagementacademy.net/resources/blog/a-three-point-estimating-technique-pert/), [SNIPPET]). All O, M, P values are this report's estimates [EST], to be replaced by the team's own. Owners: P1 owns the device, P2 owns protocol and PC, and shared packages split evenly.

| ID | Work package | Deliverable | MoSCoW | Owner | O | M | P | E | SD |
|---|---|---|---|---|---|---|---|---|---|
| A | Spec, data contract, BOM, ordering | One-page spec with numbers, GATT and record format | Must | Both | 4 | 6 | 10 | 6.33 | 1.00 |
| B | Timing core | Touch, 1 ms timestamp, arming state machine, bench log | Must | P1 | 8 | 14 | 28 | 15.33 | 3.33 |
| C | Display and UI | 3 screens, mark and delete, user switch | Must | P1 | 5 | 9 | 18 | 9.83 | 2.17 |
| D | On-device stats | Best, mean, Ao5, Ao12 (Ao100 optional), host unit tests | Must | P2 | 4 | 6 | 12 | 6.67 | 1.33 |
| E | Storage | CRC log, per-user store, ack pointer | Must | P1 | 7 | 12 | 26 | 13.50 | 3.17 |
| F | Power | 1S Li-ion, TP4056 USB-C | Should | P1 | 2 | 4 | 8 | 4.33 | 1.00 |
| G | BLE GATT and sync firmware | Service, MTU/DLE, ack/resume | Must | P2 | 9 | 16 | 40 | 18.83 | 5.17 |
| H | PC bridge, MQTT/REST hop, ingest | Bridge, broker, dedupe, ack | Must | P2 | 7 | 12 | 28 | 13.83 | 3.50 |
| I | Database and users | Schema, per-user separation | Must | P2 | 3 | 5 | 10 | 5.50 | 1.17 |
| J | Dashboard core | Rolling Ao5/Ao12/Ao100 with user, session, date filters | Must | P2 | 7 | 11 | 22 | 12.17 | 2.50 |
| K | Integration and stabilisation | Solve-to-chart loop, 30 min soak | Must | Both | 7 | 11 | 22 | 12.17 | 2.50 |
| L | Validation | Rigs, runs, analysis, user trial | Must | Both | 7 | 12 | 22 | 12.83 | 2.50 |
| M | Report, video, rehearsal | Report, README, backup video | Must | Both | 7 | 12 | 20 | 12.50 | 2.17 |
| S1 | Enclosure and pads | Two print iterations | Should | P1 | 4 | 8 | 16 | 8.67 | 2.00 |
| **Committed at 10 weeks** | | | | | | | | **152.49** | **9.87** |

Stretch pool (not committed): hardware inspection with +2/DNF (4/7/14, E 7.67, SD 1.67); dashboard extras (4/8/16, E 8.67, SD 2.00); csTimer import and export (3/5/10, E 5.50, SD 1.17); smart-cube link on the PC (8/16/40, E 18.67, SD 5.33); Stackmat bridge mode (6/10/20, E 11.00, SD 2.33). Hour split at 10 weeks: P1 about 74 h, P2 about 79 h, including half of the shared packages.

### Capacity and horizons

Capacity assumption: **10 h/person/week, so 20 team-hours per week**. Evidence: student teams report 8-12 h/person/week alongside other courses, intensive embedded courses ask 16-20 h for 4-5 weeks, and HUST's nominal allowance is about 60-90 project hours per student ([UT Dallas](https://utdesign.utdallas.edu/partners/faq-corporate), [BYU](https://capstone.groups.et.byu.net/wikis/doku.php?id=project-wiki%3Asyllabus%3Acapstone_time_management), [Cornell](https://vanhunteradams.com/Pico/CourseMaterials/Final_Project.html); mostly [SNIPPET]). Software surveys show 30-40% average effort overrun, and students' worst-case estimates are often exceeded ([Moloekken-Oestvold and Joergensen](https://cms.simula.no/sites/default/files/publications/SE.3.Moloekken-Oestvold.2004.pdf); [Buehler et al. 1994](https://doi.org/10.1037/0022-3514.67.3.366), secondary summaries). The planning rule is: plan hours = E x 1.3 must not exceed weeks x 20.

Per-package expected hours by horizon, with the features dropped:

| ID | 10 wk (relaxed) | 8 wk (baseline) | 6 wk (compressed) | What drops |
|---|---|---|---|---|
| A Spec and contract | 6.33 | 6.33 | 6.33 | Nothing; the data contract is frozen first |
| B Timing core | 15.33 | 15.33 | 15.33 | Nothing |
| C Display and UI | 9.83 | 6.00 | 5.00 | 8 wk: one screen plus cycle button; 6 wk: last time and Ao5 only |
| D On-device stats | 6.67 | 5.00 | 4.00 | 8 wk: Ao100 on PC only; 6 wk: Ao5 only, Ao12 on PC |
| E Storage | 13.50 | 10.00 | 8.00 | 8 wk: no archive tail; 6 wk: one active user, wipe after ack |
| F Li-ion power | 4.33 | 0 | 0 | USB-C power bank instead |
| G Transport firmware | 18.83 | 18.83 | 10.17 | 6 wk: Wi-Fi MQTT replaces BLE (O/M/P 5/9/20, SD 2.50); same record and ack protocol |
| H PC bridge and ingest | 13.83 | 13.83 | 7.67 | 6 wk: broker subscriber only (4/7/14, SD 1.67) |
| I Database and users | 5.50 | 5.50 | 4.00 | 6 wk: user id column, no management screen |
| J Dashboard core | 12.17 | 10.00 | 8.00 | 8 wk: fewer filters; 6 wk: one rolling-average chart |
| K Integration | 12.17 | 10.50 | 8.00 | Shorter soak |
| L Validation | 12.83 | 10.00 | 7.00 | 8 wk: trial of 3, informal; 6 wk: timing and power-loss only, 10-cut sync smoke |
| M Report and demo | 12.50 | 10.00 | 8.00 | Shorter report, one rehearsal |
| S1 Enclosure | 8.67 | 0 | 0 | Perfboard on a flat plate |
| **Total E** | **152.49** | **121.32** | **91.50** | |
| SD (variances summed; lite packages scaled in proportion) | 9.87 | 8.74 | 6.03 | |

Confidence and capacity (hours, team):

| Horizon | E | SD | P80 / P90 nominal | P80 / P90 widened | Plan = E x 1.3 | Capacity (weeks x 20) | Plan h per person |
|---|---|---|---|---|---|---|---|
| 10 weeks | 152.5 | 9.9 | 160.8 / 165.1 | 167.4 / 175.2 | 198.2 | 200 | 99 |
| 8 weeks | 121.3 | 8.7 | 128.6 / 132.5 | 134.5 / 141.4 | 157.7 | 160 | 79 |
| 6 weeks | 91.5 | 6.0 | 96.6 / 99.2 | 100.6 / 105.4 | 119.0 | 120 | 60 |

Nominal P80 = E + 0.84 SD and P90 = E + 1.28 SD under a normal approximation. Widened figures multiply SD by 1.8 [INFERENCE]: one source reports that nominal 90% intervals held the actual effort only 60-70% of the time ([SNIPPET](https://cms.simula.no/sites/default/files/publications/SE.3.Moloekken-Oestvold.2004.pdf)), and a two-sided 65% coverage implies SD about 1.8 times larger. The 80-90% completion range is therefore 161-175 h at 10 weeks, 129-141 h at 8 weeks and 97-105 h at 6 weeks. The plan figure E x 1.3 sits above all of them, so the plan carries margin. The 10-week plan at 99 h per person exceeds the 60-90 h nominal allowance; the baseline at 79 h sits inside it.

Weeks = plan hours / (2 x h per person per week):

| Horizon | h = 8 | h = 10 | h = 12 |
|---|---|---|---|
| Relaxed scope (198.2 h) | 12.4 | 9.9 | 8.3 |
| Baseline scope (157.7 h) | 9.9 | 7.9 | 6.6 |
| Compressed scope (119.0 h) | 7.4 | 6.0 | 5.0 |

If the team has only 8 h/person/week, the baseline needs about 10 weeks, so choose the horizon by real hours, not by calendar alone.

### Week-by-week milestones

Baseline 8 weeks (E hours per week; capacity 20, with the 30% allowance forming the slack):

| Wk | Work | Team E (h) | Cum. E | Gate |
|---|---|---|---|---|
| 1 | A spec and contract, order parts, B bench start, repo and broker skeleton | 13.8 | 13.8 | **M0** spec frozen with numeric targets; parts ordered |
| 2 | B timing core, D stats with host tests, record format | 15.0 | 28.8 | **M1** timing bench log passes |
| 3 | B calibration, C display, E log, early GATT hello, fixture build | 15.3 | 44.2 | BLE hello works (R3 timebox starts) |
| 4 | E storage, C UI, G sync firmware, H ingest | 18.0 | 62.2 | **M2** solve-to-stats loop on device; trigger: cumulative actual above 81 h means switch to the 6-week list |
| 5 | G sync, H bridge, J first chart | 18.0 | 80.2 | **M3** first data on dashboard; BLE fallback decision |
| 6 | G/H polish, J dashboard, K integration, L rigs | 18.7 | 98.8 | **M4** feature freeze |
| 7 | K soak, L runs and trial, M draft | 17.5 | 116.3 | **M5** validation data in hand |
| 8 | M report, video, two rehearsals | 5.0 | 121.3 | **M6** demo; unspent slack absorbs overrun |

Gate weeks across horizons:

| Gate | 6 wk | 8 wk | 10 wk |
|---|---|---|---|
| M0 Spec frozen, parts ordered | 1 | 1 | 1 |
| M1 Timing bench passes | 2 | 2 | 3 |
| M2 Solve-to-stats loop on device | 3 | 4 | 5 |
| M3 First data on dashboard (BLE or MQTT) | 4 | 5 | 6 |
| M4 Feature freeze | 4 | 6 | 8 |
| M5 Validation data in hand | 5 | 7 | 9 |
| M6 Report, video, demo | 6 | 8 | 10 |

Cumulative checks: at baseline week 4 the plan E x 1.3 reaches 80.9 h against 80 h capacity, so the week-4 gate is the decision point.

### Resource cost

FX assumption: 1 USD = 25,500 VND [UNVERIFIED rate]. Prices were observed in the notes' session and are undated; lines marked V cite a page or snippet, E lines are estimates to replace with quotes. Sources: [pyworld](https://pyworld.vn/san-pham/esp32-devkit-v1-30pin.html), [hshop S3](https://hshop.vn/mach-phat-trien-mke-k01-esp32-s3-dev-kit), [hshop OLED](https://hshop.vn/lcd-oled-trang-0-96-inch-i2c), [hshop ST7789](https://hshop.vn/panel-man-hinh-lcd-tft-ips-1-54-inch-st7789-spi-interface), [hshop TP4056](https://hshop.vn/mach-sac-pin-tp4056-lithium-battery-charge-controller-usb-c), [MPR121](https://dientutuyetnga.com/products/cam-ung-dien-dung-mpr121-1), [Nshop print](https://nshopvn.com/dich-vu/in-3d).

| Line (qty) | Tier A minimum (classic ESP32, OLED) | Tier B recommended (S3, TFT, fallback sensor) | Tier C premium (nRF52840, PCB) |
|---|---|---|---|
| MCU boards (spare included) | 2 x 120,000 = 240,000 V | 2 x 295,000 = 590,000 V | XIAO nRF52840 345,000 V (conflicting listings) + S3 295,000 V |
| Display | OLED 65,000 V | TFT 85,000 V + OLED 65,000 V | TFT 85,000 + OLED 65,000 V |
| Sensing fallback | none | MPR121 25,000 V | 2 x MPR121 50,000 V |
| RTC | none | DS3231 44,000 V (stock doubtful) | DS3231 44,000 V |
| Charger, holder, cell | 20,000 + 13,000 V + 60,000 E | 20,000 + 73,000 V/E | 370,000 E (cells, holders, pads, misc) |
| Pads, wires, buttons | 80,000 E | 130,000 E | included above |
| Enclosure (800 VND/g print) | 80,000 V | 2 iterations 192,000 V | 3 iterations 288,000 V |
| Import and PCB | none | none | FRAM 153,000 E, CH224K 40,000 E, 2-layer PCB 750,000 E |
| Shipping and handling | 45,000 E | 60,000 E | in misc |
| **Parts total** | **603,000 (US$24)** | **1,284,000 (US$50)** | **2,485,000 (US$97)** |

Tier B adds tooling and contingency (all [EST]):

| Item | VND |
|---|---|
| Tier B parts | 1,284,000 |
| USB logic analyzer clone for the timing fixture | 150,000 |
| Fixture parts: MOSFET or relay module, wires, pulse source | 60,000 |
| Subtotal | 1,494,000 |
| Contingency 15% | 224,100 |
| **All-in Tier B** | **1,718,100 (US$67; about 859,000 per person)** |

All-in for the other tiers, with the same tooling and 15% contingency: Tier A about 935,000 (US$37), Tier C about 3,099,000 (US$122). Software (ESP-IDF or Arduino, PlatformIO, FastAPI or Node, SQLite, a chart library) assumes open-source cost of zero. Hosting is the demo laptop. A 240 fps phone camera is assumed owned. Oscilloscope or signal-generator loans from a lab are plausible [UNVERIFIED]; no student-project funding for IT4735 was found. A single-unit build costs about 0.6 million VND (S3 295k, TFT 85k, charger 10k, holder 13k, cell 60k, pads about 40k, case 96k) [INFERENCE], against 0.9-1.0 million VND for a G5 and 0.22-0.75 million for Bluetooth timers in Vietnam.

Labour is the larger resource: 158 person-hours at baseline, shown as 79 hours per person. Parts lead time is 1-7 working days domestic and 7-20 days cross-border ([Shopee delivery note](https://salework.net/thoi-gian-giao-hang-shopee/), [SNIPPET]), so buy locally in week 1.

### Validation plan

Write pass criteria into the spec before testing. Targets are proposals [EST] to confirm after the week-2 fixture run.

| Test | Method | Sample | Pass criterion (proposed) |
|---|---|---|---|
| Firmware timing path | Signal generator or MOSFET drives touch and release; logic analyzer records both edges and the device report ([NIST guidance](https://tf.nist.gov/general/pdf/1930.pdf), [SNIPPET]) | At least 100 trials; durations 2 s, 10 s, 60 s | Report mean bias and SD; calibrated mean bias within 2 ms, SD within 2 ms |
| End-to-end timing | 240 fps phone camera (4.17 ms per frame) filming the device and a reference counter, Bland-Altman analysis ([Bland](https://www-users.york.ac.uk/~mb55/meas/sizemeth.htm), [SNIPPET]) | 3 durations x 20 repeats = 60 pairs | 95% limits of agreement within 10 ms, camera frame error stated |
| Power-loss | Second MCU or relay cuts power at random offsets during a write loop | 50-100 cuts | Zero corrupted or lost committed records; report counts |
| Sync-loss | Drop BLE at random points mid-transfer | 20-50 drops | Zero loss, zero duplicates by (user, seq) after reconnect |
| Soak | Continuous solves with periodic sync | 30 minutes | No reset |
| User trial | Formative round: beginner, sub-30, sub-15; tasks: start solve, delete last, switch user, view Ao12, sync; SUS ([Nielsen](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/)) | 5 cubers | Report task success and SUS; claim no statistical significance |

### Deliverables mapped to milestones

| Deliverable | Milestone |
|---|---|
| D1 One-page spec with numeric targets; data contract (GATT, record, ack) | M0 |
| D2 BOM and order record | M0 |
| D3 Timing firmware and bench log | M1 |
| D4 Device firmware with stats, storage, UI | M2 |
| D5 Sync protocol spec; ingest service; first dashboard data | M3 |
| D6 Dashboard with seeded dataset; enclosure (if committed) | M4 |
| D7 Test report: timing, power-loss, sync-loss, trial | M5 |
| D8 Final report with measurement chapter, README, user guide, contribution table | M6 |
| D9 Live demo, backup video, spare board | M6 |

## Open questions and requirement edits

The six flagged issues below carry a recommendation each. Beyond them, the requirements need numeric acceptance targets and one internal conflict resolved.

### Flagged issues

| # | Issue | Evidence | Recommendation |
|---|---|---|---|
| a | "Pin 15 V hoặc sạc Type-C" is likely a drafting error; the glossary rationalises it via USB PD 15 V | MCU, display and pads run at 3.3 V; a 15 V rail needs a buck converter with no benefit; 4S Li-ion is about 14.8 V ([CH224K](https://components101.com/ics/ch224k-usb-power-delivery-controller-ic), [TP4056 module](https://hshop.vn/mach-sac-pin-tp4056-lithium-battery-charge-controller-usb-c)) | Rewrite as single-cell Li-ion (3.7 V nominal) charged over USB-C at 5 V; confirm with the lecturer; PD trigger optional |
| b | "Độ trễ dưới 0,001 s" is indefensible as written | Touch scan plus debounce adds about 2-10 ms per edge [EST]; ISR latency is microseconds; WCA resolution is 10 ms; tibordp claims about 2 ms with no data | State 1 ms resolution, typical detection delay under 10 ms, characterised against a reference with bias and SD reported |
| c | Haitay is not WCA-legal | 7f1a Approved Timer List; 3a4 bans electronics in puzzles; G5 in 4-pad mode from 2 Jan 2027 | Position as a practice timer and list WCA approval as a non-goal |
| d | Course labs cover REST, MQTT and ESP32 Wi-Fi; BLE-to-PC sits outside | 20251 lab repo; peer kiosk uses MQTT, FastAPI, SQLite | Keep BLE for the device link and add a visible MQTT or REST hop from the PC bridge; Wi-Fi MQTT is the 6-week fallback |
| e | Vietnam participation shrinks per event | Table below | Treat as irrelevant to grading; avoid any market-size claim beyond "a few hundred active competitors per year" |
| f | No public IT4735 rubric | Only the program entry and a 2021 slide | Parameterise the schedule (above) and ask the lecturer the questions below |

Vietnam registrations from public WCIF, accepted registrations, not attendance ([OWN CALC](https://www.worldcubeassociation.org/api/v0/competitions/VietnamChampionship2025/wcif/public)):

| Year | VN competitions with data | Registrations | Unique VN accounts |
|---|---|---|---|
| 2017 | 8 | 1,679 | 1,173 |
| 2018 | 7 | 936 | 671 |
| 2019 | 5 | 714 | 517 |
| 2022 | 5 | 1,110 | 891 |
| 2023 | 3 | 702 | 585 |
| 2024 | 12 | 1,170 | 635 |
| 2025 | 4 | 519 | 389 |
| 2026 (to 8 Oct) | 7 | 627 | 397 |

Unique accounts fell from 1,173 (2017) to 389 (2025), and the union over 2017-2026 is about 3,600 [OWN CALC]. Worldwide the WCA reports 265,197 participants and 14,000+ competitions ([WCA post, 2025](https://www.worldcubeassociation.org/posts/wca-world-championship-2025-to-welcome-record-number-of-competitors-in-seattle)), and yearly competitions rose from 305 (2021) to about 2,700 (2024-2025) [OWN CALC]. The recreational base is larger and unmeasured, and no 2025-2026 market-size report was found.

### Recommended edits to chap1.tex

| Location | Current | Proposed |
|---|---|---|
| NFR Hiệu năng | Độ trễ dưới 0,001 s | "Độ phân giải 1 ms; độ trễ phát hiện chạm điển hình dưới 10 ms; sai lệch so với tham chiếu trong khoảng giới hạn 10 ms (đo bằng logic analyzer và camera)." |
| NFR Nguồn điện | Pin 15 V hoặc sạc Type-C | "Pin Li-ion một cell (3,7 V danh định), sạc qua USB Type-C 5 V." Remove the 15 V sentence from the USB Type-C glossary entry or mark PD as optional |
| Device statistics vs boundary table | Functional list shows Ao100 on the device; table puts Ao100 on the PC | Choose one; baseline: device shows best, mean, Ao5, Ao12; PC computes Ao100 and trends; device Ao100 is a Should |
| PC link | "qua Bluetooth" | Add the PC bridge and the MQTT or REST hop to the service |
| Glossary Ao5, Ao12, Ao100 | Trim fastest and slowest; Ao100 five each side | Add cut = ceil(5% n), DNF as infinity, +2 as t + 2000 ms, undefined below n solves, "csTimer-style" label for Ao12 and Ao100 |
| NFR Dữ liệu | "Sức chứa lớn" | At least 10,000 records (160 KB at 16 B); zero loss over N randomised power cuts |
| New acceptance table | none | Numeric targets for timing, power-loss, sync-loss, soak, SUS |
| New sync semantics | Wipe after PC confirms | Acknowledge after fsync, idempotent by (user_id, seq), resend from last acknowledged |
| New non-goals | none | WCA approval, custom PCB, ESP32 smart-cube central role |

### Questions for the lecturer and team

| # | Question | Why it matters |
|---|---|---|
| 1 | Real deadline for the midterm demo and the week count | Selects the 6, 8 or 10-week ladder |
| 2 | Team size, midterm weight, and share of report versus demo | Cornell-type rubrics put 20-50% on the report |
| 3 | Demo format: live, video, or both; who attends | Sets rehearsal and backup requirements |
| 4 | Is a BLE-to-PC design with an MQTT or REST hop acceptable? Is Wi-Fi MQTT an acceptable fallback? | Resolves R5 |
| 5 | Is the 15 V line intentional? | Resolves issue a |
| 6 | Will the lecturer accept 1 ms resolution with a measured delay in place of 0.001 s? | Resolves issue b |
| 7 | Can the lab lend a logic analyzer, oscilloscope or high-speed camera? | Saves about 150,000 VND and raises measurement quality |
| 8 | Are pre-made dev boards and open-source libraries allowed? | Confirms the Tier B BOM |
| 9 | How will individual contribution be assessed? | Shapes the task table and git evidence |
| 10 | Real team hours per week | Replaces the 10 h/person/week assumption |

## Conclusion

The decisive variable is hours per person, not features. At the HUST nominal allowance of about 100 hours per student for the whole course, the 8-week baseline already consumes 79 project hours each, so the team should fix the horizon from real availability and let the drop ladder, not optimism, decide scope. The 6-week list works only if the sync layer moves to Wi-Fi MQTT, which also aligns with the taught stack.

Haitay's strongest argument against "csTimer already does this" is a failure demonstration. Pulling power mid-write and dropping the link mid-sync, with zero lost or duplicated records and a Bland-Altman plot beside them, shows engineering that browser timers do not need to face. Novelty claims stay modest: the gap is the integrated, acknowledged pipeline from a physical timer to a persistent per-user service, and it should be stated as "not found in searched sources".

## Sources

Hardware timers and Stackmat: [Speedsolving wiki StackMat](https://www.speedsolving.com/wiki/index.php/StackMat); [WCA timer list post (Oct 2021)](https://www.worldcubeassociation.org/posts/updating-the-official-list-of-approved-timers-october-2021); [WCA 4-pad post (Aug 2026)](https://www.worldcubeassociation.org/posts/adoption-of-4-pad-timing-august-2026); [Speed Stacks G5](https://www.speedstacks.com/store/retail/speed-stacks-g5-timer/); [H2 Rubik G5](https://rubikonline.vn/speedstacks-g5-pro-timer-dong-ho-bam-gio-rubik-cao-cap); [thegioirubik timers](https://thegioirubik.com/danh-muc/phu-kien/timer/); [Cubelelo GAN Halo](https://www.cubelelo.com/products/gan-halo-timer-smart); [GAN Smart Timer](https://www.gancube.com/products/gan-smart-timer); [SpeedCubeShop QiYi](https://speedcubeshop.com/products/qiyi-smart-timer-bluetooth-xuanwu); [ZyO QiYi](https://zyorubik.com/products/phu-kien-rubik-qiyi-smart-timer-new-2023-thiet-bi-bam-gio-hang-qiyi-thong-minh-ket-noi-bluetooth-zyo-rubik); [SpeedCubeShop MoYu](https://speedcubeshop.com/products/moyu-ai-bluetooth-timer); [websosanh.vn](https://websosanh.vn/s/gi%E1%BB%9D+rubik.htm); [G5 issues](https://www.speedsolving.com/threads/g5-stackmat-issues.89767/); [PaddyCo Protocol.md](https://raw.githubusercontent.com/PaddyCo/StackmatTimer/master/Protocol.md); [ledmat](https://jayanth-rajakumar.github.io/ledmat/); [StackMatGen4TimerTeensy](https://github.com/m9aertner/StackMatGen4TimerTeensy).

WCA: [WCA Regulations (official branch markdown)](https://raw.githubusercontent.com/thewca/wca-regulations/official/wca-regulations.md); [WCA Regulations site](https://www.worldcubeassociation.org/regulations/); [Speedcubers Digest](https://www.speedcubersdigest.com/p/wca-to-implement-4-pad-timers-starting); [WCA 2025 record post](https://www.worldcubeassociation.org/posts/wca-world-championship-2025-to-welcome-record-number-of-competitors-in-seattle); [WCA API example](https://www.worldcubeassociation.org/api/v0/competitions/VietnamChampionship2025/wcif/public).

Open source, software, smart cubes: [tibordp/cube-timer](https://github.com/tibordp/cube-timer); [ojdip.net blog](https://ojdip.net/2020/11/esp32-cube-timer/); [wisblock-smartcube-companion](https://github.com/xoseperez/wisblock-smartcube-companion); [StackmatLink](https://github.com/liusonwood/StackmatLink); [PaddyCo/StackmatTimer](https://github.com/PaddyCo/StackmatTimer); [ASU thesis](https://keep.lib.asu.edu/items/187330); [csTimer](https://www.cstimer.net/); [csTimer repo](https://github.com/cs0x7f/cstimer); [issue #34](https://github.com/cs0x7f/cstimer/issues/34); [issue #40](https://github.com/cs0x7f/cstimer/issues/40); [Speedsolving timer thread](https://www.speedsolving.com/threads/new-speedsolving-timer.97451/); [Sub-X](https://subx.guru/); [Cubeast thread](https://www.speedsolving.com/threads/cubeast-a-speedcubing-timer-for-bluetooth-cubes-with-support-for-all-bluetooth-cubes-all-timers-and-all-major-solving-methods.77406/); [CubeProgression](https://github.com/jjangsangy/CubeProgression); [CubeDesk](https://github.com/kash/cubedesk); [cstimer-analyzer #18](https://github.com/Borys35/cstimer-analyzer/issues/18); [kana gist](https://gist.github.com/kana/1e96a2300f8479f67d1f208a57f2b9e7); [Speedsolving wiki Average](https://www.speedsolving.com/wiki/index.php/Average); [cubing.js](https://github.com/cubing/cubing.js); [gan-web-bluetooth](https://github.com/afedotov/gan-web-bluetooth); [GAN MAC FAQ](https://gist.github.com/afedotov/52057533a8b27a0277598160c384ae71); [caniuse Web Bluetooth](https://caniuse.com/web-bluetooth); [MDN Web Bluetooth](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API).

Pain evidence: [lost csTimer data](https://www.speedsolving.com/threads/i-lost-my-cstimer-data.89015/); [csTimer reset](https://www.speedsolving.com/threads/cstimer-got-reset.90778/); [Stackmat csTimer issues](https://www.speedsolving.com/threads/stackmat-cstimer-issues.80169/); [Stackmat price thread](https://www.speedsolving.com/threads/should-i-buy-my-son-gen-4-or-gen-5-stackmat-timer.88407/); [tracking solves](https://www.speedsolving.com/threads/how-do-you-track-your-solves.78339/); [Quang Ngai contest](https://doanthanhnien.vn/tin-tuc/tuoi-tre-sang-tao/quang-ngai-thu-tai-rubik-lan-iii-%E2%80%93-san-choi-toa-sang-tai-nang-tre).

Embedded and BOM: [ESP-IDF touch](https://docs.espressif.com/projects/esp-idf/en/v5.4/esp32s3/api-reference/peripherals/touch_pad.html); [GPTimer](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gptimer.html); [ESP-FAQ BLE](https://docs.espressif.com/projects/esp-faq/en/latest/software-framework/bt/ble.html); [File systems](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/file-system-considerations.html); [TTP223 datasheet](https://files.seeedstudio.com/wiki/Grove-Touch_Sensor/res/TTP223.pdf); [CH224K](https://components101.com/ics/ch224k-usb-power-delivery-controller-ic); [pyworld ESP32](https://pyworld.vn/san-pham/esp32-devkit-v1-30pin.html); [hshop S3](https://hshop.vn/mach-phat-trien-mke-k01-esp32-s3-dev-kit); [hshop OLED](https://hshop.vn/lcd-oled-trang-0-96-inch-i2c); [hshop ST7789](https://hshop.vn/panel-man-hinh-lcd-tft-ips-1-54-inch-st7789-spi-interface); [hshop TP4056](https://hshop.vn/mach-sac-pin-tp4056-lithium-battery-charge-controller-usb-c); [MPR121](https://dientutuyetnga.com/products/cam-ung-dien-dung-mpr121-1); [Nshop 3D print](https://nshopvn.com/dich-vu/in-3d); [Shopee delivery](https://salework.net/thoi-gian-giao-hang-shopee/).

Course and project management: [SoICT program](https://soict.hust.edu.vn/wp-content/uploads/Bachelor-Computer-Engineering-program.pdf); [HUST regulation](https://soict.hust.edu.vn/wp-content/uploads/QCDT.pdf); [2021 IT4735 slides](https://www.slideshare.net/slideshow/it4735iot-va-ung-dungv2021pdf/262849382); [lecturer profile](https://soict.hust.edu.vn/ts-dang-tuan-linh.html); [IoT-IT4735 kiosk](https://github.com/nguyenLTpk/IoT-IT4735); [20251 lab repo](https://github.com/hunganh1310/20251-IT4735-IoT-Lab); [Cornell ECE 4760](https://vanhunteradams.com/Pico/CourseMaterials/Final_Project.html); [Berkeley ME 100](https://tbp.studentorg.berkeley.edu/syllabi/1548/download/); [UVA ECE](https://homa-alem.github.io/teaching/ece_6501/6501_syllabus.pdf); [arXiv 1810.07646](https://arxiv.org/pdf/1810.07646); [Hubble BLE](https://hubble.com/community/guides/why-your-first-ble-project-won-t-connect-and-how-to-fix-it/); [UT Dallas](https://utdesign.utdallas.edu/partners/faq-corporate); [BYU](https://capstone.groups.et.byu.net/wikis/doku.php?id=project-wiki%3Asyllabus%3Acapstone_time_management); [Moloekken-Oestvold](https://cms.simula.no/sites/default/files/publications/SE.3.Moloekken-Oestvold.2004.pdf); [Buehler 1994](https://doi.org/10.1037/0022-3514.67.3.366); [Agile Business Consortium](https://www.agilebusiness.org/resource/what-is-moscow-prioritization/); [PMI risk](https://www.pmi.org/learning/library/risk-analysis-decisions-uncertain-times-6686); [PMA PERT](https://projectmanagementacademy.net/resources/blog/a-three-point-estimating-technique-pert/); [NIST stopwatch guidance](https://tf.nist.gov/general/pdf/1930.pdf); [Bland sample size](https://www-users.york.ac.uk/~mb55/meas/sizemeth.htm); [Nielsen 5 users](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/); [demo guide](https://roboticsknowledgebase.com/wiki/robotics-project-guide/demo-day/).

Known gaps: the WCA Approved Timer List PDF, GAN CubeStation export features, Cubeast 2026 status, and the real IT4735 rubric were not verified. Several primary papers on IoT education and estimation returned errors and are cited from abstracts or summaries.
