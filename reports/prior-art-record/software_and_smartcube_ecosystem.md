# Speedcubing software, statistics, data formats, and smart-cube BLE ecosystem (as of 2026-10-08)

Method note: facts come from fetched pages (GitHub READMEs, raw source files, the live csTimer page, WCA Regulations, MDN, caniuse). Some fetches were summarised by a small model, so wording is paraphrase, not verbatim. Items marked [UNVERIFIED] were not confirmed by a fetched source. No key bytes are reproduced.

## 1. Timer and analytics software: what exists, what Haitay's dashboard duplicates

### Takeaway
csTimer already covers on-device-style stats, Stackmat input, multi-session management, backup/export and a per-session trend graph, all free and open source. Third-party tools and a brand-new Speedsolving.com timer (Aug 2026) already offer accounts, cross-session progress charts, histograms and heatmaps. Haitay's differentiation must therefore be the hardware-to-account pipeline (no mic/jack, automatic BLE sync, per-user long-term storage across sessions) and a well-chosen set of long-horizon trends, not "has an Ao5/Ao12/Ao100 chart".

### Cited Findings
**csTimer (cs0x7f)**
- Web app, GPL-3.0, description "Professional Speedcubing/Training Timer"; 1,314 commits, 61 open issues, not archived (781 stars, 204 forks). — [GitHub cs0x7f/cstimer](https://github.com/cs0x7f/cstimer)
- Runs as an offline-capable PWA; data can be uploaded to csTimer's server or Google Storage (server keeps at least the 10 latest uploads); full export/import to file; Stackmat supported (HTTPS needed). — [GitHub cs0x7f/cstimer](https://github.com/cs0x7f/cstimer)
- Live page lists: Stackmat input with a status tool (signal, power, noise); Bluetooth cube tool (state, battery, reconstruction); current/best single and average with ao5 and ao12 shown by default; customisable moX/aoX indicators; configurable trim count; cross-session statistics; sessions can be added, split, merged, renamed; auto-export every 100 solves to local file, csTimer server or Google Storage; a "time trend" tool graphing all solves in the current session; a "time distribution" tool; no accounts mentioned. — [cstimer.net](https://www.cstimer.net/)
- Accounts: the README/live page describe no user accounts, only server/Google backup. — [cstimer.net](https://www.cstimer.net/); [GitHub](https://github.com/cs0x7f/cstimer)
- Open requests show what csTimer lacks: session folders to merge a day's sessions and see long averages such as ao1000; per-date and per-session stats with PBs and a statistics comparator. — [csTimer issue #40](https://github.com/cs0x7f/cstimer/issues/40); [csTimer issue #34](https://github.com/cs0x7f/cstimer/issues/34)

**CubeDesk (kash/cubedesk, cubedesk.io)**
- "Community and timer for the Rubik's Cube"; GPL-3.0; TypeScript; Node + PostgreSQL/Prisma + Redis; hosted accounts, timer sessions, stats page, alg training, play with others; repo has 232 commits, not archived. README does not mention import/export, Stackmat, or smart cubes, but PRs in the repo add GAN, QiYi, MoYu smart cube drivers. — [GitHub kash/cubedesk](https://github.com/kash/cubedesk); [PR #242 GAN rewrite](https://github.com/kash/cubedesk/pull/242); [PR #257 QiYi/GAN Gen1/MoYu AI](https://github.com/kash/cubedesk/pull/257); [PR #256 MoYu](https://github.com/kash/cubedesk/pull/256)

**Cubeast (cubeast.com)**
- Web app launched May 2020 for Bluetooth cubes; claims support for all 3x3 Bluetooth cubes; stats per solving-method step, TPS comparison between cube models, shareable solve links; can work with external timers incl. StackMat. Pricing, csTimer import, cloud sync and 2026 liveness not stated (page links a status page). — [Speedsolving thread (2020)](https://www.speedsolving.com/threads/cubeast-a-speedcubing-timer-for-bluetooth-cubes-with-support-for-all-bluetooth-cubes-all-timers-and-all-major-solving-methods.77406/); [cubeast.com](https://www.cubeast.com/)
- Source licence not stated in these pages (appears closed source) [UNVERIFIED].

**Speedsolving.com "New Speedsolving Timer" (thread started 2026-08-02)**
- Guests store solves locally; logged-in members save to account; solves queued and batched to server; "Restore from Server" to a new device; JSON export/import; csTimer import through file upload. — [Speedsolving thread](https://www.speedsolving.com/threads/new-speedsolving-timer.97451/)
- Analytics: progress chart of best Ao12 and best single (30d/90d/1y/all), PBs (Ao5 through Ao100), practice heatmap, time-distribution histogram, insights, recent-sessions table. Stackmat/Bluetooth support not mentioned. — [same thread](https://www.speedsolving.com/threads/new-speedsolving-timer.97451/)
- This is the closest direct competitor to Haitay's dashboard concept as of today (forum content treated as data).

**CubeProgression (jjangsangy)**
- Reads csTimer .txt/.json exports; progression chart with rolling ao5/12/50/100, PB step chart, distribution box plots by day/week/month, KDE density-shift chart, std-dev/IQR evolution, summary cards, searchable table; MIT licence; 0 stars (hobby-level). — [GitHub jjangsangy/CubeProgression](https://github.com/jjangsangy/CubeProgression)

**CubeRoot (cuberoot.me)**
- React + Three.js website with a Tauri host giving native Bluetooth on Windows/macOS; timer supports GAN, MoYu (incl. MoYu32 WeiLong V10 Ai), QiYi, GoCube, Giiker; accounts exist; own code licence not stated. — [CubeRoot about](https://cuberoot.me/about)

**Twisty Timer (aricneto)**
- Android material-design timer using TNoodle scrambles; GPL-3.0; 405 commits; not marked archived; README itself does not list charts, formats, or Stackmat. — [GitHub aricneto/TwistyTimer](https://github.com/aricneto/TwistyTimer)
- Store/mirror listings describe backup-file export/import and CSV export, categories, comments, penalties, graphs; v4.7.0 fixed export/import. Third-party listing, exact CSV columns not verified. — [Search listing via Play Store page](https://play.google.com/store/apps/details?id=com.aricneto.twistytimer&hl=en_US); [Aptoide listing](https://twisty-timer.fr.aptoide.com/app)

**Cubing.js / smart-puzzle**
- cubing.js: dual GPL-3.0/MPL-2.0; "still under development"; has `bluetooth` folder with `smart-puzzle`, `smart-robot`, `smart-timer`. — [GitHub cubing/cubing.js](https://github.com/cubing/cubing.js); [bluetooth dir](https://github.com/cubing/cubing.js/tree/main/src/cubing/bluetooth)

**Feature matrix vs Haitay (derived)**
| Planned Haitay feature | Already provided by | Gap |
|---|---|---|
| Best/mean/Ao5/Ao12/Ao100 | csTimer, Speedsolving timer | none |
| Rolling-average time-series | csTimer (single-session trend), CubeProgression, Speedsolving timer (best Ao12/single over time) | Persistent cross-session rolling lines across months from hardware |
| Long-term per-user storage | CubeDesk, Speedsolving timer (accounts); csTimer only via manual backups | Hardware-auto-sync with no phone/PC timer in the loop |
| Stackmat input | csTimer (audio), Cubeast (external timers) | Haitay is the Stackmat-class device itself with BLE (no audio jack) |
| Smart-cube link | csTimer, Cubeast, CubeDesk, CubeRoot | Mostly covered in browser; ESP32 route is novel |

### Inferences
- "Dashboard of Ao5/Ao12/Ao100" is table stakes; value is in zero-friction capture (BLE auto-sync from the physical timer, no manual export step) and in session/period comparisons that csTimer users request (issues #34, #40).
- Importing csTimer JSON into the PC app is cheap and removes an adoption barrier (three third-party tools already do it).

### Gaps
- Qqtimer, Cubic Timer, cubedb, WCA-linked tools, iOS/Android store apps (CubeTime etc.): not fetched; no verified feature/licence data. Search results only surfaced an App Store listing for CubeTime and "The Speedcuber Timer" ([CubeTime](https://apps.apple.com/ca/app/cubetime/id1600392245)) with no details read.
- Cubeast 2026 status, pricing, and open-source status unverified.
- Twisty Timer last commit date not shown on the page; "stale" status unverified.

## 2. Statistics definitions

### Takeaway
WCA only defines single, Mean of 3 and Average of 5 (best and worst removed, one DNF/DNS allowed in Ao5, any DNF makes Mo3 a DNF). Ao12/Ao100 are community conventions: drop ceil(5%) fastest and slowest, mean the rest, DNF if a DNF remains among counted times; csTimer follows this and the trim count is configurable.

### Cited Findings
- 9b1a: Average of 5 is the standard full-round format; 9b2a: Mean of 3 for 6x6x6/7x7x7. — [WCA Regulations Art. 9](https://www.worldcubeassociation.org/regulations/)
- 9f8: five attempts, best and worst removed, arithmetic mean of the remaining 3 determines ranking. 9f9: one DNF or DNS may count as the worst result; two or more DNF/DNS make the average DNF. — [WCA Regulations](https://www.worldcubeassociation.org/regulations/)
- 9f10-9f11: Mean of 3 is the arithmetic mean of 3 attempts; any DNF/DNS makes the mean DNF. — [WCA Regulations](https://www.worldcubeassociation.org/regulations/)
- 9f4/9f5: DNF = disqualified or unsolved/unfinished; DNS = eligible but did not start. 9f7: in Best-of-X, DNF/DNS is worst possible. — [WCA Regulations](https://www.worldcubeassociation.org/regulations/)
- 9f1: results under 10 minutes truncated to hundredths; averages/means rounded to the nearest hundredth (9f2: at 10 min or more, truncated/rounded to seconds). — [WCA Regulations](https://www.worldcubeassociation.org/regulations/)
- 10e3: one move needed to finish = solved with +2 s; 10e4: more than one move = DNF. (The +2 penalty is also applied for other infractions elsewhere in Art. 10/A; only these sub-rules were confirmed here.) — [WCA Regulations](https://www.worldcubeassociation.org/regulations/)
- 9f14: ties in averages broken by best attempt; 9f15: identical results get identical rank. — [WCA Regulations](https://www.worldcubeassociation.org/regulations/)
- Community definition: averages are a truncated mean removing 5% best and 5% worst, rounded up; Ao5 drops one each side, Ao12 drops 1 and divides 10 remaining by 10, Ao100 removes five fastest and five slowest; "If any counting time is a DNF or DNS, the average is a DNF." — [Speedsolving Wiki: Average](https://www.speedsolving.com/wiki/index.php/Average)
- A DNF is trimmed with the slowest results, so one DNF does not spoil Ao12/Ao100; ao21 would trim 2 each side (ceil rounding). — [Speedsolving Wiki: Average](https://www.speedsolving.com/wiki/index.php/Average); [Speedsolving thread on trim](https://www.speedsolving.com/threads/number-of-solves-trimmed-at-each-side-5.80134/)
- csTimer: "Averages are trimmed at the better side, and the trim count is configurable"; moX (plain mean) and aoX indicators customisable. — [cstimer.net](https://www.cstimer.net/)
- csTimer-style reference implementation: sort window with DNF = infinity, `cut = ceil(n*0.05)` per side, mean of the rest, DNF if an infinity remains; best average = best window; session mean excludes DNFs; fewer than n solves gives DNF; effective time = time + flag (flag 2000 for +2). — [kana gist summarize-cstimer-stats](https://gist.github.com/kana/1e96a2300f8479f67d1f208a57f2b9e7) (a third-party script, not csTimer's own code)

**Exact algorithm to adopt (derived from the above)**
1. Effective time: OK = t, +2 = t+2000 ms, DNF = infinity.
2. Window of n latest solves; if fewer than n then undefined (show "-").
3. cut = ceil(0.05 n) (Ao5: 1, Ao12: 1, Ao100: 5); sort; discard cut smallest and cut largest.
4. If any remaining value is infinity, result = DNF; else mean of the n-2cut remaining, rounded to centiseconds (WCA: round to nearest hundredth; individual times truncated).
5. Current = latest window; Best = minimum over all windows ending at each solve; DNF windows are excluded from best.
Edge cases: Ao5 allows exactly 1 DNF; Ao12 allows 1 (cut 1); Ao100 allows 5; ties in ordering do not change the sum; trimmed values with equal times are interchangeable.

### Inferences
- "Ao" in practice = ceil-5% truncated mean; WCA formally has only Ao5 and Mo3 (a Mo3 can't tolerate a DNF). Ao12 matching the Ao5 rule (cut 1) is convention, not regulation. Haitay should label Ao12/Ao100 as "csTimer-style" and cite this.
- Whether to apply WCA's centisecond truncation to each time versus rounding is a design choice; csTimer's rounding mode for display not verified.

### Gaps
- The WCA Regulations fetch covered only the first ~100k of ~155k characters; no WCA regulation on Ao12/Ao100 exists to my knowledge, not confirmed by reading the full text.
- csTimer's own source for the stats algorithm was not read directly (gist is third-party); exact rounding for Ao display unverified.
- csTimer docs on "ao100" naming: live page does not mention ao100 by name, though custom aoX indicators exist.

## 3. Data formats and portability

### Takeaway
csTimer's export (a JSON object with `sessionN` arrays plus `properties`) is the de facto interchange format and is already consumed by CubeProgression and the new Speedsolving timer. Haitay should import csTimer JSON and store a flat, per-solve schema containing ms time, penalty, scramble, comment, Unix timestamp and session.

### Cited Findings
- csTimer export: keys `session1`..`sessionN`, each an array of solves `[[flag, timeMs], scramble, comment, started_at]`; flag 0 = OK, 2000 = +2, -1 = DNF; effective time = timeMs + flag (DNF = infinite); `started_at` Unix seconds at solve start (not inspection). — [kana gist](https://gist.github.com/kana/1e96a2300f8479f67d1f208a57f2b9e7)
- `properties.sessionData` is a JSON string keyed by session index with `name`, `opt` (e.g. `scrType`), `rank`, `date` (first/last solve start), `stat` (count, DNF count, mean). — [kana gist](https://gist.github.com/kana/1e96a2300f8479f67d1f208a57f2b9e7)
- csTimer export appears as .txt/.json from "Export to file"; third-party tools accept both. — [CubeProgression](https://github.com/jjangsangy/CubeProgression); [Speedsolving timer thread](https://www.speedsolving.com/threads/new-speedsolving-timer.97451/)
- Twisty Timer: backup file plus CSV export with categories, comments, penalties (third-party listing only). — [Aptoide listing](https://twisty-timer.fr.aptoide.com/app)
- Speedsolving timer export/import is JSON. — [thread](https://www.speedsolving.com/threads/new-speedsolving-timer.97451/)
- WCA result data is published by the WCA but only per official attempt (Regulation 9 rounding/DNF values above); no practice-timer interchange standard exists in what I found.

**Recommended minimal schema (derived)**
`solve`: `id`, `user_id`, `session_id`, `puzzle` (e.g. 333), `time_ms` (raw), `penalty` (`OK|+2|DNF`), `started_at` (Unix s or ms UTC), `scramble` (nullable), `comment` (nullable), `source` (`haitay|csTimer-import|smartcube`), optional `moves` blob (smart cube). `session`: `id`, `name`, `puzzle`, `created_at`. Derive Ao values on the fly from solves; do not store them. Export = csTimer-compatible JSON for round-tripping.

### Inferences
- Because csTimer encodes penalty as additive flag, store penalty separately and compute effective time once to avoid double +2.
- Device-side: a 3-field record (time_ms, penalty, local counter/timestamp) is enough; the PC assigns session and user.

### Gaps
- Official csTimer format spec/source not read (gist is empirical). Cubeast and Twisty Timer exact formats not verified. WCA's own export formats not covered (not relevant to training data).

## 4. Smart cubes and BLE protocols

### Takeaway
All major families are reverse-engineered, not officially documented, and open-source clients exist in TypeScript/JS (cubing.js, gan-web-bluetooth, smartcube-web-bluetooth, csTimer) and in C++ for a Nordic MCU (wisblock-smartcube-companion). GAN Gen2/3/4 and MoYu32 are AES-encrypted with keys derived from the cube's MAC; QiYi uses fixed-key AES-ECB with a MAC-based hello; GoCube is plain; Giiker is plain with a light obfuscation. Moves carry cube timestamps in GAN (Gen2+/linear-fit helper) and QiYi; GoCube timestamps come from the host.

### Cited Findings
**GAN**
- gan-web-bluetooth (afedotov, MIT): supports Gen2 (GAN Mini ui FreePlay, GAN12 ui FreePlay, GAN12 ui, GAN356 i Carry S, GAN356 i Carry, GAN356 i 3, Monster Go 3Ai), Gen3 (GAN356 i Carry 2), Gen4 (GAN12 ui Maglev, GAN14 ui FreePlay), MoYu AI 2023 via the Gen2 protocol; emits MOVE and FACELETS events; move events carry cube timestamps with `cubeTimestampLinearFit()` for clock skew. — [GitHub afedotov/gan-web-bluetooth](https://github.com/afedotov/gan-web-bluetooth)
- UUIDs stated in its definitions file. Gen2: service `6e400001-b5a3-f393-e0a9-e50e24dc4179`, command `28be4a4a-cd67-11e9-a32f-2a2ae2dbcce4`, state `28be4cb6-cd67-11e9-a32f-2a2ae2dbcce4`. Gen3: service `8653000a-43e6-47b7-9cb0-5fc21d4ae340`, command `8653000c-...`, state `8653000b-...` (same base). Gen4: service `00000010-0000-fff7-fff6-fff5fff4fff0`, command `0000fff5-0000-1000-8000-00805f9b34fb`, state `0000fff6-0000-1000-8000-00805f9b34fb`. Keys: one key/IV entry shared by Gen2/3/4 and one for MoYu AI 2023. — [gan-cube-definitions.ts (raw)](https://raw.githubusercontent.com/afedotov/gan-web-bluetooth/master/src/gan-cube-definitions.ts)
- All GAN data AES-encrypted; per-cube key derived from MAC. Web apps read the MAC from advertisement manufacturer data; this needs Chrome flag `chrome://flags/#enable-experimental-web-platform-features` (or Bluefy "Enable BLE Advertisements" on iOS); macOS Chrome shows a spoofed MAC; apps fall back to asking the user. For some older GAN cubes the MAC range was small enough for brute force; not for newer cubes. — [GAN MAC FAQ gist](https://gist.github.com/afedotov/52057533a8b27a0277598160c384ae71)
- cubing.js `gan.ts` (current main file as fetched) uses service `0000fff0`, characteristics fff5/fff7/fff2/fff3 and the Gen1 356i layout: polled (default 150 ms) state reads, last 6 moves per read, key from System ID + firmware, battery at fff7 byte 7, timestamps via `Date.now()`. Newer-gen support may live elsewhere in the repo and was not verified. — [cubing.js gan.ts](https://raw.githubusercontent.com/cubing/cubing.js/main/src/cubing/bluetooth/smart-puzzle/gan.ts)
- Cubes do not advertise their service UUID, scan by name [UNVERIFIED claim from a search summary, not a primary source]. — [search summary](https://gist.github.com/afedotov/52057533a8b27a0277598160c384ae71)

**GoCube / Rubik's Connected**
- cubing.js: service `6e400001-b5a3-f393-e0a9-e50e24dcca9e`, state characteristic `6e400003-b5a3-f393-e0a9-e50e24dcca9e`; no encryption in code; moves are 12-entry byte map; orientation as ASCII quaternion divided by 16384; timestamps from browser `event.timeStamp`, not payload; message type guessed by length (code TODO). — [cubing.js gocube.ts](https://raw.githubusercontent.com/cubing/cubing.js/main/src/cubing/bluetooth/smart-puzzle/gocube.ts)

**Giiker / Xiaomi**
- cubing.js: service `0000aadb-0000-1000-8000-00805f9b34fb`, characteristic `0000aadc-...`; 20-byte message, optional additive decryption (marker at byte 18, 40-entry table), corners/edges as nibbles, last move in nibbles 32-33, no battery in that code, timestamps from browser event. — [cubing.js giiker.ts](https://raw.githubusercontent.com/cubing/cubing.js/main/src/cubing/bluetooth/smart-puzzle/giiker.ts)

**QiYi / XMD Tornado**
- cubing.js: main service `0xfff0`, characteristic `0xfff6`; AES-ECB per 16-byte block with a fixed embedded key; CRC-16 MODBUS; MAC derived from device name prefix `CC:A3:00:00` plus name hex digits and sent reversed in the app-hello; opcodes 0x02 CUBE_HELLO (state, battery byte 35), 0x03 STATE_CHANGE (state, latest move, cube timestamp in bytes 3-6, 12 previous moves), `TIMESTAMP_SCALE = 1.6`; battery only in hello. — [cubing.js qiyi.ts](https://raw.githubusercontent.com/cubing/cubing.js/main/src/cubing/bluetooth/smart-puzzle/qiyi.ts)
- Reverse-engineering notes moved to Codeberg (GitHub README is a stub). — [Flying-Toast/qiyi_smartcube_protocol](https://github.com/Flying-Toast/qiyi_smartcube_protocol/blob/master/README.md); browser visualiser [qiyi_smartcube_protocol_web](https://github.com/KittatamSaisaard/qiyi_smartcube_protocol_web)

**MoYu**
- MoYu AI 2023 uses the GAN Gen2 protocol; WRM/V10/V11 (`WCU_MY3*`) use a separate MoYu32 protocol, AES as in GAN with different key, MAC part of key derivation, MAC guessed from name for some models, state/moves (5-move history)/battery/gyro. — [cubedesk PR #256](https://github.com/kash/cubedesk/pull/256); [smartcube-web-bluetooth](https://github.com/day00/smartcube-web-bluetooth); [CubeRoot credits](https://cuberoot.me/about) citing a `weilong-v10-ai-protocol` spec repo
- csTimer added support for QiYi and MoYu Weilong V10 AI. — [csTimer issue #399 / search result](https://github.com/cs0x7f/cstimer/issues/399)

**Libraries**
- smartcube-web-bluetooth (fork of poliva): GAN Gen1-4, Giiker/Mi/Hi, GoCube/Rubik's Connected, MoYu AI 2023/MHC/WRM, QiYi and XMD Tornado V4, GAN Smart Timer and Halo; moves, facelets, gyro quaternion, battery, dual host/cube timestamps; licence file not read. — [day00/smartcube-web-bluetooth](https://github.com/day00/smartcube-web-bluetooth)
- csTimer's connect page: Giiker, GoCube, GAN; Chrome/Edge on desktop/Android, Bluefy on iOS; newer GANs need a MAC prompt unless the flag is on; multi-phase CFOP/Roux splitting; how auto start/stop is derived is not documented there. — [csTimer wiki](https://github.com/cs0x7f/cstimer/wiki/Use-csTimer-to-connect-to-smart-cubes---%E4%BD%BF%E7%94%A8csTimer%E8%BF%9E%E6%8E%A5%E6%99%BA%E8%83%BD%E9%AD%94%E6%96%B9)

**Microcontroller as BLE central**
- Existing MCU precedent: `wisblock-smartcube-companion` runs on a Nordic nRF52840 (RAK4631), works with GAN 356 i3, Giiker i3/i2, GoCube X, has an "automatic start/stop timer for smart cubes" and also supports a Stackmat audio cable; GPL-3.0; 101 commits, 15 stars; README does not explain pairing/encryption handling or how start/stop is detected. — [GitHub xoseperez/wisblock-smartcube-companion](https://github.com/xoseperez/wisblock-smartcube-companion)
- NimBLE-Arduino supports ESP32 central role (default 3 connections). — [Arduino library page](https://docs.arduino.cc/libraries/nimble-arduino/)
- I found no ready-made ESP32 GAN-cube project. — [search results](https://github.com/h2zero/NimBLE-Arduino)

**Deriving solve start/end**
- Moves arrive with timestamps (GAN, QiYi in payload; GoCube/Giiker via host receive time), and facelet/state data permit solved-state detection; csTimer's multi-phase splitting relies on this. A solve start = first move after scramble; end = state becomes solved. — [gan-web-bluetooth](https://github.com/afedotov/gan-web-bluetooth); [cubing.js qiyi.ts](https://raw.githubusercontent.com/cubing/cubing.js/main/src/cubing/bluetooth/smart-puzzle/qiyi.ts)

### Inferences
- ESP32 as central is feasible for GoCube (no crypto), Giiker (light decode), QiYi (fixed AES-ECB, name-derived MAC); GAN Gen2-4 are feasible but need AES-128 plus MAC extraction from the advertisement, which is easier on an MCU than in a browser (raw advertisement access). Estimated effort: GoCube/QiYi lowest, GAN medium (porting the TS driver), MoYu32 highest (least documented). Not verified on ESP32 hardware.
- For a class project the lowest-risk route is Web Bluetooth on the PC (libraries exist, no porting), keeping the ESP32 to the Haitay timer's own BLE peripheral link; optionally add one cube family (GoCube or QiYi) on ESP32 as a stretch.
- Timestamp quality differs by brand: for reliable millisecond solve times, prefer cubes with in-payload timestamps (GAN, QiYi); GoCube-based times depend on BLE latency.

### Gaps
- GAN Gen2/3/4 packet layouts and opcode tables were not read (only UUIDs and the structure of the definitions). Battery event for GAN Gen2+ not confirmed in the fetched file. Key bytes intentionally not recorded.
- Rubik's Connected (not GoCube-branded) protocol identity with GoCube taken from library naming only.
- QiYi Codeberg repo not read; MoYu32 spec repo not read; Giiker 'Hi-' variants unverified.
- No source states a Tornado V3 AI model name; smartcube-web-bluetooth lists XMD Tornado V4 only.
- Cubes' licensing/ToS on protocol use not researched.

## 5. Web Bluetooth vs desktop app vs local server

### Takeaway
Web Bluetooth works only in Chromium browsers (Chrome/Edge/Opera, Chrome Android), not Firefox or any iOS browser, and needs HTTPS and a user gesture. A browser dashboard fits a class project well for cube links; the timer itself is better linked through a native path (desktop shell or local bridge) if reliable BLE sync is needed.

### Cited Findings
- caniuse: Chrome 56+, Edge 79+, Opera 43+, Chrome for Android supported; Firefox and Safari (desktop and iOS) not supported; global usage 76.52%; Mozilla position "Harmful"; iOSWebBLE polyfill exists but is not WebKit. — [caniuse Web Bluetooth](https://caniuse.com/web-bluetooth)
- MDN: experimental, limited availability, not Baseline; secure context required; permission prompt via `requestDevice()` needs transient user activation; `getDevices()` for previously granted devices; not available in Web Workers; `bluetooth` Permissions Policy default `self`. — [MDN Web Bluetooth API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API)
- csTimer supports iOS only through Bluefy. — [csTimer wiki](https://github.com/cs0x7f/cstimer/wiki/Use-csTimer-to-connect-to-smart-cubes---%E4%BD%BF%E7%94%A8csTimer%E8%BF%9E%E6%8E%A5%E6%99%BA%E8%83%BD%E9%AD%94%E6%96%B9)
- CubeRoot ships a web app with a Tauri host to provide native Bluetooth on Windows/macOS — evidence that a web UI inside a Tauri shell is a working pattern for this domain. — [CubeRoot about](https://cuberoot.me/about)

### Inferences
- Recommended architecture: web dashboard (static page, local or hosted over HTTPS) using Web Bluetooth for the Haitay timer and smart cubes in Chromium; a small local bridge (Python `bleak` or Tauri) as fallback for browsers and for background auto-sync [UNVERIFIED; `bleak`/Tauri docs not fetched]. Web Bluetooth requires a user click on every new pairing, which conflicts with unattended background sync; `getDevices()` partially mitigates this.

### Gaps
- Chrome's `getDevices()`/background reconnect behaviour on desktop Chrome in 2026 and Tauri/Electron BLE specifics not verified.

## 6. Training-data visualisation practice

### Takeaway
Community tooling converges on: rolling Ao5/Ao12/Ao50/Ao100 lines over solve index or date, PB step history of single and averages, time-distribution histograms, per-day or per-session summaries and comparisons, and practice heatmaps.

### Cited Findings
- csTimer offers a per-session time-trend curve and a time-distribution tool. — [cstimer.net](https://www.cstimer.net/)
- Forum answers point to csTimer's trend tool when users ask how to graph progress. — [Speedsolving: Graphing solves](https://www.speedsolving.com/threads/graphing-solves.68823/); [How do you track your solves?](https://www.speedsolving.com/threads/how-do-you-track-your-solves.78339/)
- csTimer issue #40 requests merging sessions/folders for progress over time and long averages such as ao1000; issue #34 requests per-date and per-session stats, session PB summaries and a comparator. — [#40](https://github.com/cs0x7f/cstimer/issues/40); [#34](https://github.com/cs0x7f/cstimer/issues/34)
- cstimer-analyzer issue #18 proposes side-by-side session comparison (mean, median, best single, best Ao5, count, trend, CV), histogram and time-of-day analysis. — [Borys35/cstimer-analyzer #18](https://github.com/Borys35/cstimer-analyzer/issues/18)
- CubeProgression: progression with rolling ao5/12/50/100, PB step chart, box plots by period, density-shift, SD/IQR evolution. — [CubeProgression](https://github.com/jjangsangy/CubeProgression)
- Speedsolving timer: best Ao12/single over time, PBs for Ao5-Ao100, heatmap, histogram, session table. — [thread](https://www.speedsolving.com/threads/new-speedsolving-timer.97451/)
- Cubeast: per-step and TPS/recognition-time analyses specific to smart cubes. — [cubeast.com](https://www.cubeast.com/)

### Inferences
- Priority chart set for Haitay: (1) rolling Ao5/Ao12/Ao100 on a date or solve-index axis with zoom, (2) PB step history, (3) histogram, (4) session-to-session comparison table/overlay, (5) practice heatmap. Items 4 and 5 appear in open requests or in only one competitor, so they are the differentiators.

### Gaps
- No quantitative evidence on which charts cubers value most (no survey found); evidence is feature lists and a few GitHub issues. Reddit/Discord request threads not searched.
