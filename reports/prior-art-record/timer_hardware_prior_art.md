# Hardware speedcubing timers: prior art (Stackmat, commercial, open-source/DIY, academic, WCA rules)

Research date: 2026-10-08. All URLs fetched or surfaced in this session. "[UNVERIFIED]" marks claims without a fetched primary source. Several product pages did not display a date; where a repo's last update is unknown, it is stated.

## 1. Stackmat timers: generations, price, features, protocol, WCA/Speedstacks relationship, complaints

### Takeaway
Stackmat (Speed Stacks) is the de facto and, as of 2026, the only WCA-approved timer family; Gen 5 (2021) added a 2-pad/4-pad switch, hold-to-activate buttons and a data port, and sells for about USD 30 (about 900,000 VND in Vietnam). Its output is a documented-by-reverse-engineering 1200-baud RS-232-style packet on a 2.5 mm jack, carrying state, time digits and a checksum, but the timer itself has no on-device history beyond best-time memory, no wireless link and no app.

### Cited Findings

**Generations and history**
- Gen 1 was first used at World Championship 2003; WCA adopted Stackmats as its official timer at its founding in 2004. Gen 2 had the reset button between the hand plates (accidental resets); production stopped around US Nationals 2012; WCA removed Gen 2 from approved timers on 1 Feb 2023. Gen 3 was announced in 2011 and times to 0.001 s, with reported failures to stop or reset. Gen 3 and Gen 4 differ only in minor ergonomics. — [Speedsolving wiki: StackMat](https://www.speedsolving.com/wiki/index.php/StackMat)
- Gen 5 (G5 StackMat Pro, 2021) has 2-pad and 4-pad modes, buttons that must be held 0.2 s to activate, and controls disabled 0.5 s after each stop. — [Speedsolving wiki: StackMat](https://www.speedsolving.com/wiki/index.php/StackMat)
- WCA announced in Oct 2021 that G5 would be approved alongside the 2022 Regulations and Gen 2 would stop being approved with the 2023 Regulations, citing malfunction concerns. — [WCA post, Oct 2021](https://www.worldcubeassociation.org/posts/updating-the-official-list-of-approved-timers-october-2021)
- Stackmat was preferred over a light-sensor timer partly because a cube could be dropped during one-handed solves; requiring two hands to stop was a clearer "solve complete" signal. — [Speedsolving wiki: StackMat](https://www.speedsolving.com/wiki/index.php/StackMat)

**Price (USD, VND)**
- G5 timer only: USD 29.99 on the official store (Blackout/Black Mist/Phantom colours +5). — [Speed Stacks G5 page](https://www.speedstacks.com/store/retail/speed-stacks-g5-timer/)
- G5 bundle (timer, mat, bag): USD 41.70 to 45.95 at US retailers. — [Wolverine Sports](https://wolverinesports.com/products/stackmat); [Gym Closet](https://gymcloset.com/speedstacksstackmatpro.html); [Great Lakes Sports](https://www.greatlakessports.com/speed-stacks-pro-timer)
- G4 Pro timer: USD 39.99 (Velocity Cubing) and a USD 23.99 discounted bundle at TheCubicle (the retailer pages show both; timestamps unclear). — [Velocity Cubing](https://www.velocitycubing.com/product/speedstacks-gen-4-timer/); [TheCubicle Gen4 bundle](https://www.thecubicle.com/products/speedstacks-gen4-bundle)
- Vietnam: SpeedStacks G5 Pro Timer 900,000 VND (listed out of stock when fetched). — [H2 Rubik Shop](https://rubikonline.vn/speedstacks-g5-pro-timer-dong-ho-bam-gio-rubik-cao-cap)
- Vietnam (secondary aggregator, Shopee data may be stale): G4/G5 sold on Shopee; "about 900,000 VND and up". — [websosanh.vn](https://websosanh.vn/s/gi%E1%BB%9D+rubik.htm) (search summary only; page not fetched)
- Speed Stacks Tournament Display Pro about 3,500,000 VND in Vietnam (same aggregator summary, [UNVERIFIED] against the shop page); the open-source ledmat project states the commercial Speedstacks Tournament Display costs about USD 95 in the US. — [ledmat docs](https://jayanth-rajakumar.github.io/ledmat/)
- Data cable for G4/G5 to a PC: USD 3.99; needs a dedicated mic jack or a splitter, not compatible with phones or combo headphone/mic jacks; reviewers note combo-jack laptops need an adapter. — [TheCubicle data connector](https://www.thecubicle.com/products/data-connector-for-stackmat-g5)

**Features, memory, display, interface**
- G5: 0.001 s accuracy, memory storing best stacking times, 2 AAA batteries, "data port to connect to external display" (TD cord plugs underneath), hold-feature on RESET/POWER, 2-pad (speed cubing) and 4-pad (stacking) selectable by holding RESET 5 s; not compatible with Gen 3/Gen 4 mats. — [Speed Stacks G5 page](https://www.speedstacks.com/store/retail/speed-stacks-g5-timer/)
- The official page lists no statement of solve-history capacity, no wireless link and no app. The only retail-listed memory is "best times". The Speed Stacks page itself does not mention WCA approval; WCA approval of G3/G4/G5 is established on the WCA side (see Q3). — [Speed Stacks G5 page](https://www.speedstacks.com/store/retail/speed-stacks-g5-timer/)
- Gen 4 retail listing: curved design, 0.001 s accuracy, "memory feature to save best times", data port for external display, works with G3 and G4 mats. — [Cube Nation / retailer summary via TheCubicle Gen4 bundle](https://www.thecubicle.com/products/speedstacks-gen4-bundle)
- The large tournament display shows times with a delay, so the number can "jump" by up to 0.3 s after stopping; the wiki says the timer itself is usually accurate. — [Speedsolving wiki: StackMat](https://www.speedsolving.com/wiki/index.php/StackMat)

**Audio-jack serial protocol (reverse-engineered, community-documented)**
- Electrical: 2.5 mm jack, tip = signal, sleeve = ground, mono signal; PC software treats it as audio (line/mic in). — [Arduino forum thread, summarized in search](https://forum.arduino.cc/t/display-for-stackmat-timer/946502); [TheCubicle data connector](https://www.thecubicle.com/products/data-connector-for-stackmat-g5)
- Serial: RS-232-style, 1200 baud, 8 data bits, no parity, 1 stop bit; a packet about every 0.15 s (another user says about 6 per second); signal levels about 0 to 3 V can be read directly by an ATmega328 digital pin. — [ledmat docs](https://jayanth-rajakumar.github.io/ledmat/); original write-up by Florian Weingarten (2008) archived at [web.archive.org](http://web.archive.org/web/20100820185842/http://hackvalue.de:80/hv_atmel_stackmat) (cited via ledmat; archive page not fetched)
- Gen 2/3-era packet, 9 bytes: byte 1 state char (`I` reset, `A` ready, `S` stopped, `L` left hand, `R` right hand, `C` both hands, space = running), bytes 2 to 6 time digits as ASCII (min, 10 s, s, tenths, hundredths), byte 7 checksum = sum of digit values + 64, then CR/LF. Hand presence is carried only in the state byte; thousandths not documented. — [PaddyCo/StackmatTimer Protocol.md](https://raw.githubusercontent.com/PaddyCo/StackmatTimer/master/Protocol.md)
- Gen 4 changes: packets are 10 bytes (6 time digits, checksum over 6 digits), and the gap between packets is shorter; older decoders may fail. — [m9aertner/StackMatGen4TimerTeensy](https://github.com/m9aertner/StackMatGen4TimerTeensy)
- Signal polarity differs across hardware paths; StackmatLink auto-detects inverted signals; Tinkerman notes Stackmat uses inverted UART logic and used SoftwareSerial in his build. — [StackmatLink](https://github.com/liusonwood/StackmatLink); [Tinkerman](https://tinkerman.cat/post/smart-cubes-and-wisblock/)
- Discrepancy: PaddyCo lists the line ending as `\n\r`, a search-result summary of Weingarten says CR (0x0D) then LF (0x0A). Treat as unresolved until a scope capture. Speed Stacks has published no official protocol spec that I found.

**WCA/Speedstacks relationship**
- WCA defines the speedsolving timer as an approved timer on the Approved Timer List (Regulation 7f1a, version 1 April 2026); a G5 must be in 2-pad mode (A3b). — [WCA Regulations markdown, official branch](https://raw.githubusercontent.com/thewca/wca-regulations/official/wca-regulations.md)
- From 2 Jan 2027, official attempts with a speedsolving timer must use a G5 in 4-pad mode; the WCA will supply G5 timers to regions that lack them. — [WCA post, Aug 2026](https://www.worldcubeassociation.org/posts/adoption-of-4-pad-timing-august-2026)
- The sport-stacking governing body WSSA also uses the product (G5 "approved by WCA and WSSA" per the retailer listing). — [Wolverine Sports listing summarized via search](https://wolverinesports.com/products/stackmat) ([UNVERIFIED] on manufacturer page)

**Known user complaints**
- Accidental reset with the thumb when stopping on Gen 2/3/4 (reset button between pads); WCWC 2017 replacement-solve example on the wiki. — [Speedsolving wiki](https://www.speedsolving.com/wiki/index.php/StackMat); [forum thread: Stackmat Pro timer issues](https://www.speedsolving.com/threads/stackmat-pro-timer-issues.43761/)
- Gen 3 failing to stop, failing to start, unresponsive pads. — [Stackmat Timer Pro Malfunctioning](https://www.speedsolving.com/threads/stackmat-timer-pro-malfunctioning.41697/); [Stackmat Pro Timer Problem](https://www.speedsolving.com/threads/stackmat-pro-timer-problem.51413/)
- Low battery glitches (8:88.888 display, runaway counting); one forum poster says the timer takes a CR2032, while G5 retail pages say AAA, so forum claims are version-dependent. — search summary of speedsolving threads; [Stackmat Timer Pro Malfunctioning](https://www.speedsolving.com/threads/stackmat-timer-pro-malfunctioning.41697/) (page not individually fetched)
- WCA states the 0.06 s threshold for premature stops exists because of timer malfunction concerns (A6b1+). — [WCA Regulations markdown](https://raw.githubusercontent.com/thewca/wca-regulations/official/wca-regulations.md)
- WCA's 4-pad rationale: 2-pad timers make start/stop rules hard to enforce and judges cannot see infractions live. — [WCA post, Aug 2026](https://www.worldcubeassociation.org/posts/adoption-of-4-pad-timing-august-2026)

### Inferences
- The Stackmat data path is a one-way, stateless, unauthenticated broadcast (state + time + checksum). A Haitay-style device does not need Stackmat compatibility to be useful, but a decoder for it is cheap (many MIT repos) and a natural "bridge mode".
- Neither the timer nor the G5 data port is a logging product; every logging solution in the wild (csTimer, Cubeast, ESP32 bridges) is external. This is the structural reason an operational-service layer is open space.

### Gaps
- No official Speed Stacks protocol document or memory specification (capacity of "best times", whether solve history is stored) found.
- No fetched primary source for G4 list price in USD at launch or total Vietnamese G4 pricing.
- Line-ending order (CR LF vs LF CR) unresolved; Gen 5 packet format not checked separately from Gen 4.

## 2. Other commercial and "smart" timers (GAN, QiYi, MoYu, YJ, others)

### Takeaway
Three consumer lines have BLE and an app: GAN (Halo, Smart Timer, Cube Station, USD 35 to 55), QiYi Smart Timer (USD 13 to 20, Smart Player app), MoYu AI/V2 timers (USD 11 to 31, WCU Cube app). None is WCA-approved; apps are widely reported finicky, and the only cross-vendor logging/analytics products are third-party (csTimer, Cubeast). I found no YJ timer with BLE.

### Cited Findings
- GAN Halo Smart Timer: Bluetooth to the CubeStation app, stores 10,000 results offline, cloud account sync, 0.001 s accuracy, auto Ao5, 2 s button freeze after a stop, rechargeable (about 42 h), 132 g. The Standard Halo has no app/cloud, stores only 5 solves. — [Cubelelo / Amazon product text](https://www.amazon.com/Bluetooth-Competition-Connectivity-Automatic-Calculation/dp/B083TW9WFT); [Cubelelo](https://www.cubelelo.com/products/gan-halo-timer-smart)
- GAN Halo price spread: about USD 38 to 55 at specialist shops (Kewbz USD 38, speedcubing.org USD 42, EUR 31.96 MasterCubeStore, INR 3,399 Cubelelo); GAN's own page lists the Halo at USD 39.99. — [Kewbz](https://kewbz.co.uk/en-us/products/gan-halo-timer); [Speedcubing.org](https://speedcubing.org/products/gan-halo-timer); [MasterCubeStore](https://mastercubestore.com/gancube/2044-gan-halo-smart-timer-blue-bluetooth-6970697964432.html); [GAN Smart Timer page](https://www.gancube.com/products/gan-smart-timer)
- GAN Smart Timer (older): USD 34.99, buttons freeze 1 s, averages of 5, 2.5 mm aux out, syncs to Cube Station, timer holds only the 5 latest results and their Ao5; both variants marked sold out/unavailable at fetch time (availability, not a confirmed discontinuation). — [GAN official](https://www.gancube.com/products/gan-smart-timer); [TheCubicle](https://www.thecubicle.com/products/gan-smart-timer)
- GAN timers are readable via Web Bluetooth: MIT library `gan-web-bluetooth` exposes states IDLE, HANDS_ON, HANDS_OFF, GET_SET, RUNNING, STOPPED, FINISHED, DISCONNECT, recorded time, and previous times; README warns the protocol is not designed for polling the display time. 104 stars, 30 forks. — [afedotov/gan-web-bluetooth](https://github.com/afedotov/gan-web-bluetooth)
- GAN protocol uses a 0xFE magic packet and CRC16/CCITT-FALSE according to StackmatLink's README. — [StackmatLink](https://github.com/liusonwood/StackmatLink)
- User complaints on GAN: CubeStation account registration failures, slow or finicky connections, outdated Play Store build, Firefox lacks Web Bluetooth; reviews are old (about 1,300 to 2,000 days at fetch time). — [TheCubicle Halo reviews](https://www.thecubicle.com/products/gan-halo-smart-timer); [TheCubicle Smart Timer reviews](https://www.thecubicle.com/products/gan-smart-timer)
- QiYi Smart Timer (Bluetooth): QiYi Smart Player app, 0.001 s, Ao5/Ao12 on device, cloud storage and "in-app solve analysis tools for trends", 2 x AAA, 2.5 mm aux output; USD 13 to 20. — [SpeedCubeShop](https://speedcubeshop.com/products/qiyi-smart-timer-bluetooth-xuanwu)
- QiYi Smart Timer (New 2023) in Vietnam: 412,500 VND, 95 g, LED display, touching a side starts a 15 s inspection that runs on the phone; computes Ao5/Ao12 without phone; memory capacity not stated. — [ZyO Rubik](https://zyorubik.com/products/phu-kien-rubik-qiyi-smart-timer-new-2023-thiet-bi-bam-gio-hang-qiyi-thong-minh-ket-noi-bluetooth-zyo-rubik)
- QiYi basic Timer: no stored history; 149,000 to 199,000 VND on Shopee per aggregator, 175,000 VND at ZyO. — [SpeedCubeShop QiYi Timer](https://speedcubeshop.com/products/qiyi-timer); [websosanh.vn](https://websosanh.vn/s/gi%E1%BB%9D+rubik.htm); [ZyO QiYi Timer](https://zyorubik.com/products/phu-kien-rubik-thiet-bi-bam-gio-qiyi-timer-chinh-hang-zyo-rubik)
- QiYi Timer Display Pro (tournament display): 2,970,000 VND, sold out at fetch; WCA approval not stated; supplied with a 2 x 3.5 mm cable. — [ZyO Rubik](https://zyorubik.com/products/qiyi-timer-display-pro-dong-ho-tinh-gio-rubik-su-dung-trong-cac-giai-thi-dau-zyo-rubik)
- MoYu AI Bluetooth Timer: WCU Cube app, 0.001 s, USD 11.95 to 13.46 (V2/AI), Training Assistant USD 29.99 to 31.46; reviewers report the app "now refuses to work", battery drain; memory not stated. — [SpeedCubeShop MoYu AI](https://speedcubeshop.com/products/moyu-ai-bluetooth-timer); [TheCubicle MoYu AI](https://www.thecubicle.com/products/moyu-ai-timer)
- Vietnam price ladder (H2 Rubik Shop / ZyO, one 2023-era aggregation): ShengShou 115,000 VND; FanXin 165,000; QiYi 175,000; MoYu 235,000; GAN Smart Timer Bluetooth 680,000; SpeedStacks G5 900,000. — [websosanh.vn](https://websosanh.vn/s/gi%E1%BB%9D+rubik.htm) (aggregator summary; individual shop pages [ShengShou](https://rubikonline.vn/shengshou-timer-sengso-timer-dong-ho-bam-gio-rubik), [FanXin](https://rubikonline.vn/fanxin-timer-dong-ho-bam-gio-rubik-gia-re), [MoYu](https://rubikonline.vn/moyu-timer-dong-ho-bam-gio-rubik-moyu) not fetched)
- YuXin timers use AAA batteries and QJ's third-gen timer has a data port. — [Speedsolving wiki](https://www.speedsolving.com/wiki/index.php/StackMat). No YJ BLE timer found.
- Third-party software layer: Cubeast (PWA, Chrome-only) records, stores and analyzes solves from Bluetooth cubes and external timers such as Stackmat, with shareable solve links; csTimer (GPLv3) supports Stackmat, GAN timer BLE and smart cubes. — [Speedsolving Cubeast thread](https://www.speedsolving.com/threads/cubeast-a-speedcubing-timer-for-bluetooth-cubes-with-support-for-all-bluetooth-cubes-all-timers-and-all-major-solving-methods.77406/); [Hacker News Cubeast](https://news.ycombinator.com/item?id=30581829); [csTimer](https://cstimer.net/)

### Inferences
- Every BLE product syncs to a phone app/cloud, not to a PC time-series store; none markets multi-user local profiles on the device. GAN is the only one with a large on-device buffer (10,000) in the retail tier.
- Third-party apps (Cubeast, csTimer) already provide sessions and averages in a browser. The novelty claim therefore cannot be "stats/sessions" in general; it has to be about the integrated pipeline and trend analytics (see Q6).

### Gaps
- No official GAN, QiYi, MoYu product-spec pages fetched for storage capacity of QiYi/MoYu (retailer pages omit it).
- No source confirming discontinuation of any named timer.
- QiYi Smart Player and MoYu WCU app feature lists (export, PC client) not checked.
- Reddit r/Cubers threads were not reachable via search results; complaints come from retailer reviews and Speedsolving.

## 3. WCA Regulations on timers

### Takeaway
There is no Article 6 in the current text (April 1, 2026): articles jump from 5 to 7. Timer rules live in Regulation 7f (equipment), Article A (speed solving) and B; the timer must come from the WCA Approved Timer List (a Google Drive PDF I could not read), which in practice is only Speed Stacks G3/G4/G5. A DIY/Haitay device is therefore practice-only at official competitions.

### Cited Findings
- Version 1 April 2026; Article 6 and 8 are absent from the headings. — [WCA Regulations (raw, official branch)](https://raw.githubusercontent.com/thewca/wca-regulations/official/wca-regulations.md); [regulations site](https://www.worldcubeassociation.org/regulations/)
- 7f1a: "Speedsolving timer: An approved timer from the Approved Timer List" (Google Drive PDF); 7f1c: timer = speedsolving timer or stopwatch; 7f2: timer must be attached to the mat nearest the competitor; 7f3: organizers should make buttons harder to press accidentally (e.g. O-rings) and secure batteries. — [WCA Regulations](https://raw.githubusercontent.com/thewca/wca-regulations/official/wca-regulations.md)
- A3b: judge turns the timer on/resets it; G5 must be set to 2-pad mode. A3a1: inspection is strictly less than 15 s. — [WCA Regulations](https://raw.githubusercontent.com/thewca/wca-regulations/official/wca-regulations.md)
- A4b: fingers on the elevated sensor surfaces, palms down, on the competitor side; wrong contact +2 s. A4d: hands stay on the timer until it is ready; timer starts when hands are removed. A4d1: +2 s if the solve starts at or after 15 s of inspection; A4d2: DNF at or after 17 s. — [WCA Regulations](https://raw.githubusercontent.com/thewca/wca-regulations/official/wca-regulations.md)
- A6b/A6b1/A6b2: competitor responsible for stopping correctly; premature stop under 0.06 s gets an extra attempt, 0.06 s or more is a DNF unless the Delegate rules malfunction. A6c: release the puzzle before stopping (+2 s). A6d: stop with both hands flat, palms down (+2 s). A6f: do not reset before both signatures. — [WCA Regulations](https://raw.githubusercontent.com/thewca/wca-regulations/official/wca-regulations.md)
- 9f1/9f2: times under 10 min are truncated (not rounded) to hundredths; averages are rounded to the nearest hundredth. A7b2: the judge may write extra decimals from the timer, which are not part of the official result. So display resolution of 0.01 s is the official resolution (G3+ display 0.001 s). — [WCA Regulations](https://raw.githubusercontent.com/thewca/wca-regulations/official/wca-regulations.md)
- Ao5 as the official "Average of 5" removes best and worst; one DNF allowed. 3a4: puzzles must not have electronic components (Bluetooth, Wi-Fi, sensors), i.e. smart cubes are practice-only. — [WCA Regulations](https://raw.githubusercontent.com/thewca/wca-regulations/official/wca-regulations.md)
- Approved list content: secondary sources say only G3, G4, G5 Stackmats are approved. — [Speedsolving wiki](https://www.speedsolving.com/wiki/index.php/StackMat); [Speedcubers Digest](https://www.speedcubersdigest.com/p/wca-to-implement-4-pad-timers-starting). Primary list not accessible (Drive PDF requires sign-in; fetched page showed only a loader).
- Change effective 2 Jan 2027: official attempts must use a G5 in 4-pad mode; records are not reset and 4-pad results rank with 2-pad; draft Regulation changes to be published for feedback in September 2026. — [WCA post](https://www.worldcubeassociation.org/posts/adoption-of-4-pad-timing-august-2026); [Speedcubers Digest](https://www.speedcubersdigest.com/p/wca-to-implement-4-pad-timers-starting)
- Inspection and +2/DNF logic matters for device firmware: the penalties in A4d1 and A4d2 are the reference behaviour for an inspection mode. — [WCA Regulations](https://raw.githubusercontent.com/thewca/wca-regulations/official/wca-regulations.md)

### Inferences
- A DIY, non-Stackmat timer cannot be used in WCA rounds; nothing in the regulations offers a certification path for third-party timers (no application process found), so Haitay is a practice/training device. After 2027, even G3/G4 would be excluded.
- Haitay's 2-pad "hands-on / lift to start" behaviour mirrors A4b/A4d, while the WCA's move to 4-pad mode shows that 2-pad pad semantics are the official pain point; a 2-pad design is closer to the practice reality (most home timers are 2-pad).

### Gaps
- Approved Timer List PDF itself not readable; whether any non-Speed Stacks timer was ever on it not verified.
- Article 6 does not exist in the 2026 text; the assignment's "Article 6" label may refer to an older edition (the 2022 PDF placed Stackmat definitions in 7f). Older editions were not checked.
- Draft 2027 Regulation wording (September 2026 feedback) not found.

## 4. Open-source and DIY projects

### Takeaway
About ten relevant repos/posts exist; all fall into three buckets: (a) Stackmat decoders/displays (Arduino/Teensy/ESP32), (b) BLE-bridge or minimal standalone timers (ESP32), and (c) one richer all-in-one companion (WisBlock). None combines a standalone two-pad timer, multi-user on-device storage, BLE sync to a PC time-series dashboard and trend analytics.

### Cited Findings

| Project | MCU | Sensor | Display | On-device stats | Sync | License | Maturity | URL |
|---|---|---|---|---|---|---|---|---|
| tibordp/cube-timer + blog "Building a Bluetooth speedcubing timer with ESP32" (Nov 2020) | ESP32 DevKitC | Capacitive touch (foil pad, 1 pad) with hysteresis, 1 ms timer ISR | 128x64 SH1106 OLED | No (author says OLED too small); +2/DNF buttons, adjustable inspection | BLE GATT, one characteristic (state, epoch, duration), Web Bluetooth demo app | MIT | 5 commits, 0 stars, no dates shown | [repo](https://github.com/tibordp/cube-timer), [blog](https://ojdip.net/2020/11/esp32-cube-timer/) |
| xoseperez/wisblock-smartcube-companion (May 2023) | nRF52840 (RAK4631) | Smart cube BLE, optional Stackmat via UART (soldering) | 230x320 RAK14014 touch TFT | Yes: PB, Ao5, Ao12, last 12 solves, 4 users, 6 puzzles | BLE to cubes; no PC sync described | GPL-3.0 | 101 commits, 15 stars | [repo](https://github.com/xoseperez/wisblock-smartcube-companion), [blog](https://tinkerman.cat/post/smart-cubes-and-wisblock/) |
| liusonwood/StackmatLink | ESP32-S3 | Stackmat audio via LM393 comparator | WS2812 status LED only | No | BLE emulating "GAN-Timer" for csTimer | MIT firmware, CC BY-NC-SA 4.0 hardware | 54 commits, 5 stars, updated 25 May 2026 per topic page | [repo](https://github.com/liusonwood/StackmatLink) |
| m9aertner/StackMatGen4TimerTeensy | Teensy-LC | Stackmat TRS to hardware UART (no inverter) | 128x64 OLED or MAX7219 8x32 LED | No | None | MIT | 8 commits, 4 stars, updated 29 Aug 2020; documents Gen4 10-byte packet | [repo](https://github.com/m9aertner/StackMatGen4TimerTeensy) |
| PaddyCo/StackmatTimer | AVR/ESP8266 (per Arduino library page) | Stackmat serial | n/a (library) | No | None | MIT | 4 commits, 8 stars; includes Protocol.md | [repo](https://github.com/PaddyCo/StackmatTimer), [Arduino docs](https://docs.arduino.cc/libraries/stackmattimer/) |
| jayanth-rajakumar/ledmat | Arduino Nano | Stackmat jack to a digital pin | MAX7219 dot matrix (5 digits) | No | None | not named in docs, stated open source | docs site | [docs](https://jayanth-rajakumar.github.io/ledmat/) |
| diegoquintanilha/StackHack | Arduino (topics also list esp32) | Stackmat signal | custom displays | No | None | MIT | 2 commits, 0 stars, updated 25 Jul 2025 | [repo](https://github.com/diegoquintanilha/StackHack) |
| bahadircan-bc/StackmatTimerDIY | Arduino (not named) | TTP223 touch sensor | not mentioned | not mentioned | not mentioned | none shown | 2 commits, 0 stars, updated 30 Aug 2022 | [repo](https://github.com/bahadircan-bc/StackmatTimerDIY) |
| automatedhome.party ESP32+OLED timer (5 Sep 2023) | ESP32 with built-in OLED | 2 buttons (both pressed, release to start) | SSD1306 OLED | No (RAM only) | None | none stated | blog with inline code | [post](https://automatedhome.party/2023/09/05/creating-a-speed-cube-timer-using-an-esp32-with-oled/) |
| Instructables "DIY Speed Stacks Timer for Speed Cubing" | Makey Makey (not an MCU build) | Aluminium foil pads, acts as spacebar | none | via web timer | via PC | not stated | about 5 years old per search summary; page body not fetched | [page](https://www.instructables.com/DIY-Speed-Stacks-Timer-for-Speed-Cubing/) |

- StackmatLink's own listing on the GitHub `stackmat` topic: five repos total (the four above plus matheusaraujoc/Stackly, a JavaScript web timer with WCA-style stats and CSV export in localStorage, 1 commit). — [GitHub topic: stackmat](https://github.com/topics/stackmat); [Stackly](https://github.com/matheusaraujoc/Stackly)
- Software-only timers with strong stats and graphing (no hardware): csTimer (GPLv3, Stackmat + BLE cubes), MagicMannnnn/cube-timer (Mo3, Ao5/12/25/50/100), josef-stips/SpeedCubingTimer (Ao5/Ao12, median), Rubik's Timer (React/Express/MySQL). — [csTimer on GitHub](https://github.com/cs0x7f/cstimer); [MagicMannnnn/cube-timer](https://github.com/MagicMannnnn/cube-timer); [josef-stips/SpeedCubingTimer](https://github.com/josef-stips/SpeedCubingTimer); [GitHub topic rubiks-cube-timer](https://github.com/topics/rubiks-cube-timer)
- Hackaday: searches returned the rubiks-cube tag page but no speedcubing timer article; none found. — [Hackaday tag](https://hackaday.com/tag/rubiks-cube/)
- Searches for RP2040/STM32 speedcube timers returned only generic example repos, no cube timers. — search for `raspberry pi pico OR stm32 OR arduino speedcube timer touch sensor OLED stats` (no relevant result)
- IR/optical sensor cube timers on GitHub: not found in this search round.

### Inferences
- The closest single-reference designs are tibordp/cube-timer (touch + BLE + OLED, no stats, 1 pad) and wisblock-smartcube-companion (multi-user stats on device, no PC sync). Both are stale/hobbyist, small star counts.
- No repo found with RP2040/STM32, Wi-Fi, or time-series backend for solves. This is a negative search result, not proof of absence.

### Gaps
- tibordp blog says no licence; repo says MIT (taking the repo as authoritative).
- Repo "last commit" dates are not shown by the fetch tool for several repos (tibordp, wisblock); only topic-page "updated" dates are known for five.
- Reddit r/Cubers and Speedsolving DIY threads were not systematically searched (StackmatTimerDIY README points to a Reddit post, unread).

## 5. Academic and student work

### Takeaway
I found one directly relevant thesis (ASU, 2023, smart-cube app platform, not a hardware timer) and no peer-reviewed paper or Vietnamese university report on a speedcubing timer. The prior art in the academic space is thin.

### Cited Findings
- "Speedcuber Timer: Creating an Open-Source Platform for Smart Rubik's Cube Applications" by Joseph Hale, Arizona State University thesis (2023; advisor Ajay Bansal): an offline-capable Android/iOS app supporting smart cubes from three manufacturers, up to six simultaneous cubes, solve analysis tools and a smart-cube communication API; addresses fragmentation of manufacturer apps. It is software for smart cubes, not a hardware timer. — [ASU Library](https://keep.lib.asu.edu/items/187330) (abstract seen through search; page returned 403 to the fetch tool); [ProQuest](https://www.proquest.com/openview/d323757c4f4f3b4f999c68b50a27efe5/1?pq-origsite=gscholar&cbl=18750&diss=y)
- Vietnamese search ("do an thiet ke may bam gio rubik vi dieu khien") returned only retail pages and mobile app lists, no thesis or capstone report. — [FPT Shop list of cube timer apps](https://fptshop.com.vn/tin-tuc/giai-tri/cube-timer-194566)
- Searches with Consensus and Google Scholar-style queries for "Stackmat microcontroller" were not run through the Consensus tool in this session. Only the web search was used.

### Inferences
- Academic novelty bar is low; the closest literature is the ASU smart-cube platform, which reinforces that "analysis tools for solves" are already an academic topic when tied to smart cubes.

### Gaps
- No arXiv, IEEE, ACM paper on speedcubing timers verified.
- No Vietnamese thesis found; HUST, UET, PTIT repositories not searched directly (access limits).

## 6. Gap analysis: feature combinations not found

### Takeaway
Individually, every Haitay feature exists somewhere: touch-pad timers (tibordp), on-device Ao5/Ao12 (QiYi, GAN, wisblock), multi-user on-device stats (wisblock only), BLE (GAN, QiYi, MoYu, tibordp), and long-term analytics (Cubeast, csTimer, GAN Cube Station). The combination of standalone two-pad device + multi-user local profile + BLE to a PC app with a persistent time-series dashboard and trend analytics was not found as a product or repository.

### Cited Findings
- GAN Halo: standalone with 10,000-result storage and Ao5, BLE/cloud to phone app, one account; no PC dashboard or per-device multi-user profile documented. — [Amazon listing text](https://www.amazon.com/Bluetooth-Competition-Connectivity-Automatic-Calculation/dp/B083TW9WFT)
- QiYi Smart Timer: Ao5/Ao12 on device, phone app with cloud and "trend" analysis; PC sync not documented. — [SpeedCubeShop](https://speedcubeshop.com/products/qiyi-smart-timer-bluetooth-xuanwu)
- wisblock-smartcube-companion: multi-user (4) on-device stats; no sync described. — [repo](https://github.com/xoseperez/wisblock-smartcube-companion)
- tibordp/cube-timer: BLE logging to a Web Bluetooth demo app, no on-device history. — [blog](https://ojdip.net/2020/11/esp32-cube-timer/)
- Cubeast: browser (Chrome-only PWA) analytics including phase breakdown; consumes Stackmat/Bluetooth cube data. — [Speedsolving thread](https://www.speedsolving.com/threads/cubeast-a-speedcubing-timer-for-bluetooth-cubes-with-support-for-all-bluetooth-cubes-all-timers-and-all-major-solving-methods.77406/)
- Third-party pipeline already available: GAN protocol is emulated by StackmatLink for csTimer, so "Stackmat to BLE to browser" is established prior art. — [StackmatLink](https://github.com/liusonwood/StackmatLink)

**Feature matrix (derived from the cited findings; absence = not found in sources)**

| Feature | Established prior art | Not found |
|---|---|---|
| Two-pad hands-on/lift-to-start timer | Stackmat; GAN Halo; QiYi; tibordp (1 pad) | n/a |
| WCA inspection (15 s, +2/DNF) on device | tibordp (adjustable inspection); QiYi (inspection in phone) | Hardware-timed inspection with WCA penalty rules as firmware spec: not verified for commercial timers |
| On-device Ao5 | GAN, QiYi, wisblock | n/a |
| On-device Ao12 / Ao100 | QiYi Ao12; wisblock Ao12; Ao100 only in software timers | Ao100 on a standalone device: not found |
| Multi-user local storage on device | wisblock (4 users) | Any commercial timer: not found |
| BLE sync to phone app/cloud | GAN, QiYi, MoYu | n/a |
| Open BLE to browser/PC | GAN protocol via Web Bluetooth; StackmatLink; tibordp | PC time-series dashboard with retention: not found |
| Trend analytics / sessions | Cubeast, csTimer, QiYi app, GAN Cube Station | Integration with an open standalone device with offline-first sync and conflict handling: not found |

### Inferences
- Defensible novelty: (1) a combined device plus operational service (device-side multi-user store, store-and-forward BLE sync, PC time-series dashboard with trends); (2) transparent open protocol and data model for the sync; (3) offline-first on-device Ao100.
- Not defensible as novel: touch-pad timing with hysteresis (tibordp 2020), BLE emulation of GAN timers (StackmatLink 2025/26), Ao5/Ao12 on a device (GAN, QiYi, wisblock), Stackmat-protocol decoding (many repos since 2008), session/average analytics in a browser (csTimer, Cubeast, Stackly).
- "Multi-user" claim must be scoped: the assignment states one active user local storage with PC long-term storage, so wisblock's 4-user feature is only relevant if Haitay claims multi-user.

### Gaps
- Absence claims rest on search results only; commercial app internals (QiYi Smart Player, MoYu WCU, Cube Station export or PC clients) were not tested.
- GAN Cube Station may already provide long-term trend charts; this was not verified (no fetch of the app/site).
- Unknown unpublished or non-English (Chinese, Japanese) hardware projects may exist; one Japanese blog on Stack timer history was surfaced ([note.com](https://note.com/squid_sushi/n/nba538882eef5?hl=en)) but not fetched.
