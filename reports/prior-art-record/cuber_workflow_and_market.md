# Cuber workflow, objectives, pain points and market (domain basis for Haitay)

Compiled 2026-10-08. Every claim carries a URL and a year. Items tagged [UNVERIFIED] lack a fetched primary source. Items tagged [OWN CALC] come from my own computation on WCA public API data fetched 2026-10-08.

Access limits that shaped coverage: reddit.com and old.reddit.com were blocked to the fetch tool, so r/Cubers is NOT mined (no Reddit claims below). YouTube comments and Facebook groups were not reachable. Forum evidence is therefore from speedsolving.com, retailer pages and app stores. WCA website pages are JS-rendered; figures come from the WCA public API (`/api/v0/...`) and WCA posts.

---

## 1. Who the users are (roles)

| Role | Evidence | Relevance to Haitay |
|---|---|---|
| Solo practicer (csTimer + Stackmat or keyboard) | Forum thread on tracking: one csTimer session per cube/puzzle (Aug 2020) https://www.speedsolving.com/threads/how-do-you-track-your-solves.78339/ | Baseline user; owns the data problem |
| WCA competitor | Official events use Stackmat Gen 4/5 (Wikipedia, 2026) https://en.wikipedia.org/wiki/Speedcubing ; WCA Regulations A1b: "A speedsolving timer must be used in addition to the stopwatch." (2026) https://www.worldcubeassociation.org/regulations/ | Haitay is practice-side; cannot claim WCA approval [UNVERIFIED that any non-Stackmat timer is approved] |
| Child + parent | Parent asking which Stackmat to buy for a son who solves under 40 s (Nov 2022) https://www.speedsolving.com/threads/should-i-buy-my-son-gen-4-or-gen-5-stackmat-timer.88407/ | Parent buys; child practices; progress tracking is the parent's visible value |
| School club (shared equipment) | Dublin High School Rubik's Cube Club ran a competition with Stackmat timers (Nov 2025) https://www.independentnews.com/news/dublin_news/dublin-high-students-host-speedcubing-competition/article_ef1ed38e-f76b-45fb-b8c7-222424a3392b.html ; Hanoi school clubs CSP, Phan Dinh Phung (COP, founded 2018), REMS (Oct 2020) per a Vietnamese FAQ aggregator (search snippet, undated) https://vncubeassociation.com/cac-clb-truc-thuoc-hiep-hoi-rubik-viet-nam/ [page itself unreachable; club list is from search summary, UNVERIFIED in primary] | Supports "switch user" feature; no source found documenting a shared-timer workflow explicitly |
| Coach / student | Systematic-training posts treat split data as coaching input (2012) https://www.speedsolving.com/threads/a-method-of-cfop-speedcubing-training-that-yields-systematic-progress.39406/ | A coach view = read-only dashboard over a student's sessions; no source found describing a formal coach role in tools |
| Vietnamese school programs | Quang Ngai "Thu tai Rubik" III (2023) with primary/lower-secondary/upper-secondary brackets, 25 finalists https://doanthanhnien.vn/tin-tuc/tuoi-tre-sang-tao/quang-ngai-thu-tai-rubik-lan-iii-%E2%80%93-san-choi-toa-sang-tai-nang-tre ; THCS Nguyen Tri Phuong plan: class teams of 10, 2 individuals per class https://c2nguyentriphuong.badinh.edu.vn/tin-nha-truong/thcs-ntp-ke-hoach-thi-rubik-va-hat-mua-hanh-khuc-doi-tntp--pmtd22sw241 ; Ngo Thoi Nhiem school made Rubik an elective (Sep 2024) https://rubikbmt.vn/articles/detail/rubik-bmt-mang-am-me-rubik-en-voi-hoc-sinh-ngo-tho-e6e2fb82 | Many users per timer, per class: strong fit for multi-user |

Multi-user in existing tools: csTimer handles "multiple people" only by manual session-per-person (unlimited sessions, rename/merge) https://cstimer.net/ ; no per-person login. Existing phone apps offer profiles, e.g. "Cube Timer" with up to four profiles https://apps.apple.com/us/app/cube-timer/id444929094 (App Store, undated). GAN Halo page does not mention user profiles (2026) https://www.gancube.com/products/gan-halo-smart-timer . Gap: no hardware timer found with on-device user switching [UNVERIFIED as a universal claim].

---

## 2. Workflow, end to end

### 2.1 Competition attempt (WCA Regulations, 2026)
Source for all rules: https://www.worldcubeassociation.org/regulations/

1. Competitor hands the puzzle to a scrambler. Scrambles come from TNoodle, run on the delegate's own computer https://www.worldcubeassociation.org/score-tools (via search summary 2026). Scrambler signs the scorecard. Runner carries puzzle to station https://www.worldcubeassociation.org/score-tools
2. Judge lifts cover; inspection starts. A3a1: "strictly less than 15 seconds to inspect the puzzle and start the solve." Judge calls 8 s and 12 s (A3b3/b4). No moves during inspection (A3c1).
3. Start (A4): palms down on the timer; the timer starts when hands lift (A4d). Start by 15 s else +2 (A4d1; exactly 15.00 is +2). Start by 17 s else DNF (A4d2).
4. Solve (A5). Stop (A6): release the puzzle fully, then both hands flat on sensors. +2 for releasing late or one-handed stop (A6c/A6d). Timer stopped early showing 0.06 s or more: DNF (A6b2).
5. Record (A7): judge writes the result on the scorecard and signs, format "T + X = F" for penalties (A7b4); competitor checks and signs (A7c). Reset only after both have signed, else DNF at judge discretion (A6f).
6. Score taker types results into WCA Live (2026) https://github.com/thewca/wca-live/wiki/guide
7. Times truncated to hundredths under 10 min (9f1). Average of 5 drops best and worst and means the middle 3 (9f8). One DNF counts as the worst in Ao5; two DNFs make it DNF (9f9). Mean of 3 for 6x6/7x7 (9f10). Best of X for blindfolded events.

Implication for Haitay: the inspection stopwatch is the judge's (separate from the timer); a practice timer that models inspection (15 s countdown, auto +2/DNF) mimics the rule. csTimer already does this: "Enable WCA inspection procedure" with auto +2/DNF https://cstimer.net/ (2026).

### 2.2 Practice session (synthesized from csTimer feature set and forum practice)
1. Scramble generated by the app (csTimer: any number of event types and sessions) https://cstimer.net/
2. Optional inspection (15 s) then hands on timer, release to start, stop with both hands.
3. Penalty toggled after the fact: OK / +2 / DNF; delete last solve. (csTimer supports; Stackmat itself keeps only the last time.)
4. Record: Stackmat has no store for cube solves. A speedsolving reply notes "Pro timers have a built in mode where you can save your speedstacking times." (kinch2002, Mar 2015) https://www.speedsolving.com/threads/stackmat-timer-glitch.52610/ , i.e. memory exists for stacking, not as a cubing log. Cubers log in csTimer (via mic jack), a text file, Excel (swburk, Tabe, Aug 2020) https://www.speedsolving.com/threads/how-do-you-track-your-solves.78339/ .
5. Review: Ao5/Ao12, graphs, best-of-session; some compute phase shares from splits (see 3.3).
6. Reset: timer reset, next scramble, optional session split/merge ("How do you merge 2 sessions?" BenChristman1, Aug 2020, same thread).

### 2.3 Training modes
- Full solves, average-of-N sessions (a user makes a fresh session per day for an Ao100, then merges; Aug 2020, same speedsolving thread).
- Sub-step trainers: csTimer scrambles for F2L, OLL, PLL, ZBLL with case filtering https://cstimer.net/ (2026).
- Split timing: csTimer "time-split timing", phase count and a key per split https://cstimer.net/ . Smart cube gives automatic CFOP segmentation https://cstimer.net/ .
- PLL drill loop: "Time every PLL and drill the slowest one" (speedpicker, Nov 2012) https://www.speedsolving.com/threads/a-method-of-cfop-speedcubing-training-that-yields-systematic-progress.39406/
- Last-layer isolation: average F2L, flip the cube, then time LL to remove the recognition head start (same thread).
- Goal comparison: Sub-X tool estimates solves needed to reach a target and shows a confidence band https://subx.guru/ (2026).

---

## 3. Objectives and metrics

### 3.1 Standard vs nice-to-have
Standard (present in csTimer and WCA formats):
- Single/best, mean of 3, Ao5, Ao12, custom aoX/moX; Ao100 widely used by cubers though not in WCA formats. Source: csTimer lists "Mean of 3 and averages of 5 and 12" and custom aoX/moX https://cstimer.net/ . Ao5 rule: WCA 9f8 https://www.worldcubeassociation.org/regulations/ .
- Session management: any number of sessions, split/merge https://cstimer.net/
- Progress graphs and PB tracking: "cstimer is the most efficient way to track improvement." (Nmile7300, Aug 2020) https://www.speedsolving.com/threads/how-do-you-track-your-solves.78339/

Nice-to-have / emerging:
- Standard deviation and consistency. Forum views: report SD as a percent of the mean; under 10% is "fairly good" (Standard Deviation thread, undated) https://www.speedsolving.com/threads/standard-deviation.18285/ ; a poster found Ao12 SD misses inconsistency and suggested SD over Ao50/Ao100, typical Ao100 SD 2.2 to 2.6 s https://www.speedsolving.com/threads/measuring-standard-deviation-of-solve-averages.51546/
- Daily Ao100 plotted with a best-fit line, with a dissenting reply that individual data are too erratic https://www.speedsolving.com/threads/using-calculus-to-determine-the-speed-frontier.52178/
- Phase shares: sub-10 reference proportions cross 12%, cross+1 24.5%, F2L 62%, OLL 16.5%, PLL 21.5%, LL 38% (speedpicker, Nov 2012) https://www.speedsolving.com/threads/a-method-of-cfop-speedcubing-training-that-yields-systematic-progress.39406/ ; CuberPal calls its own ranges "broad coaching heuristics, not published standards" https://www.cuberpal.com/blog/cfop-solve-splits
- DNF rate, solves per day, session length: none found as named, discussed metrics in forum threads [UNVERIFIED as community-demanded]. These are cheap for a service to log, so treat as differentiators, not requirements.
- TPS, pauses, per-pair times (smart cubes only): Sub-X https://subx.guru/

### 3.2 Existing proposals for improvement analytics
- Sub-X (2026): AO100 as long-term level, AO12 as session swings, SD and 14-day slope, growth forecast, AI coaching report, csTimer JSON/CSV import https://subx.guru/ . Sub-X "flags patterns such as a volatility spike" (site wording). This is the closest existing "operational service" competitor; builder unnamed.
- CubeSkills CFOP splits tool compares splits with sub-10 averages https://www.cubeskills.com/blog/cfop-solve-splits-tool (title only; content not fetched).
- Community dissent: "I find that I sometimes do worse when I'm thinking about big averages" (Micah Morrison, Aug 2020) https://www.speedsolving.com/threads/how-do-you-track-your-solves.78339/ . Design cue: dashboards should be opt-in per metric; on-device display during a solve should stay minimal.

---

## 4. Pain points (quotes under 15 words)

### 4.1 Stackmat has no cubing memory; separate logging needed
- "I want a centralized way of keeping track of my improvement" (swburk, Aug 2020) https://www.speedsolving.com/threads/how-do-you-track-your-solves.78339/
- Logging methods in the wild: text file, Excel per event, one csTimer session per puzzle (same thread).
- Pro Stackmat timers save only stacking times (kinch2002, Mar 2015) https://www.speedsolving.com/threads/stackmat-timer-glitch.52610/
- G5 retail page lists no solve memory/recall (2026) https://www.speedstacks.com/store/retail/speed-stacks-g5-timer/
- GAN Halo sells offline storage plus app sync as the answer: it "Stores results offline" and syncs "to prevent data loss" (page paraphrase, 2026) https://www.gancube.com/products/gan-halo-smart-timer . This validates the need but binds the user to GAN's app (CubeStation).

### 4.2 csTimer-with-Stackmat setup (mic/audio)
- "It works perfectly when not connected, but when it is connected." (CUBER1265, Apr 2021) https://www.speedsolving.com/threads/stackmat-cstimer-issues.80169/
- "the input on the mic is maxed out." (KnightCuber, Sep 2021, same thread)
- "they just have too much noise inside their transmission." (abunickabhi on 3.5-to-2.5 mm cables, Sep 2021, same thread)
- "my timer sometimes record 0.04 or 0.05 etc." (SamVorst, Jan 2020) https://www.speedsolving.com/threads/stackmat-timer-and-cstimer-issue.76294/
- "I change the cable 3 times and the same happens." (Wiko, Jan 2020, same thread)
- Fixes reported: external USB sound card (JohnnyReggae, Sep 2021); recording rate set to 44100 Hz (KnightCuber, Sep 2021); mic/headphone splitter (jaredlucas, Dec 2020). Combined headphone/mic jack on laptops needs an adapter (multi-page help thread) https://www.speedsolving.com/threads/help-thread-connecting-a-stackmat-timer-to-computer.27302/ (long-running help thread, multiple pages)
- csTimer even offers a diagnostic tool showing signal state, power and noise level (Vietnamese csTimer page, 2026) https://cstimer.net/?lang=vi , which is evidence that audio-signal setup is a recurring problem.
- Stackmat web library exposes only packet fields (time, hand flags, state) and connection depends on "valid packets arriving" https://github.com/stilesdev/stackmat . A serial/USB link from Haitay can avoid the audio path entirely.

### 4.3 Battery and glitches
- Battery life estimates: "4-5 months normally" (Kenneth, Feb 2008); "My first battery lasted only for about 3 months" (Jacco, Feb 2008) https://www.speedsolving.com/threads/stackmat-timer-batteries.2922/
- Low-battery symptoms: "the timer will show 888:88.888 and will turn off" (Discomantis on a G5, Apr 2023) https://www.speedsolving.com/threads/g5-stackmat-issues.89767/ ; battery reseat is a stopgap that recurs (AlphaSheep, Apr 2015) https://www.speedsolving.com/threads/stackmat-timer-glitch.52610/
- G4 issues: power/reset buttons "can easily be accidentally hit"; batteries "can sometimes come loose" (UncleFrank, Nov 2022) https://www.speedsolving.com/threads/should-i-buy-my-son-gen-4-or-gen-5-stackmat-timer.88407/
- Competition failures: "This happens to me at least once every comp" (avgdi on Stackmat Pro stopping/resetting, Aug 2013) https://www.speedsolving.com/threads/stackmat-pro-timer-issues.43761/page-2

### 4.4 Touch pad sensitivity, false starts
- Capacitive pads can latch "on" or "off" when the trimmers are misadjusted; the thread concerns a Gen2 (search summary of a speedsolving thread, undated) https://www.speedsolving.com/threads/stackmat-timer-pro-malfunctioning.41697/ [UNVERIFIED from primary; summary only]
- Stop-sensing: a poster attributed missed stops to people who tap and release quickly instead of pressing and holding (Noahaha, Aug 2013) https://www.speedsolving.com/threads/stackmat-pro-timer-issues.43761/page-2
- GAN Halo reviews: "accidental-stop protection" freezes buttons for 2 s after stopping; one reviewer found the low profile makes stops easy to miss (retailer reviews, 2026) https://speedcubeshop.com/products/gan-halo-timer
- Random inspection start when the Stackmat is connected to csTimer (search summary of speedsolving, undated) [UNVERIFIED primary].

### 4.5 Data loss and portability (strong support for the PC dashboard)
- "I had almost 12,000 solves on there," latest export only ~5,000 (Cuban_Cuber, Feb 2023) https://www.speedsolving.com/threads/i-lost-my-cstimer-data.89015/
- "This has happened to me 5 times." (Exmestify, Feb 2023, same thread)
- csTimer reset thread, Aug 2023: "Basically everyone goes through this." (OtaMota); losses of ~4,000 3x3 solves (Caden Fisher) https://www.speedsolving.com/threads/cstimer-got-reset.90778/
- Cause: csTimer data live in browser storage and vanish when it is cleared; backup is manual or "Auto Export (per 100 solves)" https://github.com/cs0x7f/cstimer and https://cstimer.net/
- Apps: "I can't export the solves." (NebraskanSpeedsolver on CubeTime, Jan 2024) https://www.speedsolving.com/threads/timer-reviews.91691/ ; a CuberPal guide (competitor site, biased) says cloud backup is "the quiet essential" https://www.cuberpal.com/guides/best-cube-timer-app
- Design cue: a local-first store with CSV/JSON export in csTimer-compatible format (CubeTime v3 exports "JSON (csTimer format)" https://apps.apple.com/ca/app/cubetime/id1600392245 ) lowers switching cost.

### 4.6 Cost
- "Stackmat timers are waaay to overpriced" (abunickabhi, Nov 2022) https://www.speedsolving.com/threads/should-i-buy-my-son-gen-4-or-gen-5-stackmat-timer.88407/
- A later thread "I built a webcam timer so you don't need a stackmat" (swiftcuber, Jun 2026) https://www.speedsolving.com/threads/timer-reviews.91691/ shows the cost/convenience gap is still being attacked.

---

## 5. Community scale and market

### 5.1 WCA worldwide
- Founded 2004 (formation date 18 Oct 2004) https://en.wikipedia.org/wiki/World_Cube_Association
- 265,197 unique participants and 14,000+ sanctioned competitions, "20 year history", 165 countries (WCA post, 2025) https://www.worldcubeassociation.org/posts/wca-world-championship-2025-to-welcome-record-number-of-competitors-in-seattle
- Over 290,000 participants and 17,500+ competitions (Wikipedia, as of Aug 2026) https://en.wikipedia.org/wiki/World_Cube_Association
- WCA persons records: 299,674 [OWN CALC from `Total` header of WCA API `/api/v0/persons`, 2026-10-08] https://www.worldcubeassociation.org/api/v0/persons?per_page=1 . Note: records include people with a profile who may not have competed; treat as an upper bound on participants.
- Competitions per year (count of competitions starting and ending in that calendar year, WCA API `/api/v0/competitions`, queried 2026-10-08; may include cancelled; 2026 is partial plus announced) [OWN CALC] https://www.worldcubeassociation.org/api/v0/competitions : 2012: 303; 2013: 359; 2014: 481; 2015: 572; 2016: 678; 2017: 924; 2018: 1,154; 2019: 1,330; 2020: 479; 2021: 305; 2022: 1,096; 2023: 2,144; 2024: 2,723; 2025: 2,712; 2026: 2,559 so far incl. announced. Pattern: 2020 to 2021 covid trough, then 2x from 2022 to 2023, plateau at ~2,700 in 2024-2025.
- Competition counts quoted elsewhere: 12 in 2004, 100+ in 2008, 1,150+ in 2018 (Wikipedia) https://en.wikipedia.org/wiki/Speedcubing , consistent with the API numbers.
- World Championship 2025 Seattle: 1,864 competitors, 74 nations (competition page) https://www.worldcubeassociation.org/competitions/wc2025 ; announcement said "over 2,000" https://www.worldcubeassociation.org/posts/wca-world-championship-2025-to-welcome-record-number-of-competitors-in-seattle ; 2027 Uppsala expects 2,500 (Wikipedia) https://en.wikipedia.org/wiki/Speedcubing
- WCA official statistics page (`/statistics`) returned 404; no per-year competitor total was retrievable [gap].

### 5.2 Vietnam (WCA data)
Competition count (WCA API, country VN, queried 2026-10-08; includes announced) [OWN CALC] https://www.worldcubeassociation.org/api/v0/competitions?country_iso2=VN : 83 listed, 80 held (2 cancelled, 3 upcoming after today incl. HanoiWinter2026 14 Nov, HanoiChessNCube2026 29 Nov, MasterCubeHCMC2026 12 Dec). Held per year: 2010: 2; 2011: 2; 2012: 3; 2013: 3; 2014: 5; 2015: 4; 2016: 6; 2017: 8; 2018: 7; 2019: 6; 2020: 2; 2021: 1; 2022: 5; 2023: 3; 2024: 12 (record); 2025: 4; 2026: 7 held so far. Cities (top eight spelling variants only, 78 of 83 tallied): Hanoi at least 49, Ho Chi Minh City at least 28, Da Nang 1; Nha Trang and a few others earlier.

Participation from accepted registrations in public WCIF, Vietnamese-country accounts only; WCIF returned registrations only from 2017 onward; counts are registrations, not proof of attendance [OWN CALC] https://www.worldcubeassociation.org/api/v0/competitions/VietnamChampionship2025/wcif/public (pattern for all comps):

| Year | VN comps with data | VN registrations | Unique VN accounts |
|---|---|---|---|
| 2017 | 8 | 1,679 | 1,173 |
| 2018 | 7 | 936 | 671 |
| 2019 | 5 | 714 | 517 |
| 2020 | 2 | 304 | 262 |
| 2022 | 5 | 1,110 | 891 |
| 2023 | 3 | 702 | 585 |
| 2024 | 12 | 1,170 | 635 |
| 2025 | 4 | 519 | 389 |
| 2026 (to 8 Oct) | 7 | 627 | 397 |

Union of unique Vietnamese accounts across 2017-2026: about 3,600 [OWN CALC]. Reading: the active Vietnamese competing base is a few hundred per year, down from the 2017 peak (1,173 unique) and 2022 post-covid peak (891). Competitions grew in count (12 in 2024) while per-event size shrank, i.e. more local, smaller events. This is the single most useful market-size number: the addressable competitive base in Vietnam is on the order of 400 to 900 per year. The broader recreational base is larger but unmeasured.

Event sizes (WCA competition pages; competitor counts):
- Vietnam Championship 2023: 248 (limit 450) https://www.worldcubeassociation.org/competitions/VietnamChampionship2023 ; 2024: 229 https://www.worldcubeassociation.org/competitions/VietnamChampionship2024 ; 2025: 245 (limit 300) https://www.worldcubeassociation.org/competitions/VietnamChampionship2025 ; 2026 Aug 14-16, Hanoi, limit 275, fee 500,000 VND https://www.worldcubeassociation.org/competitions/VietnamChampionship2026 (my WCIF count: 212 registered, 190 Vietnamese accounts). Organizers include Hiep hoi Rubik Viet Nam, Cubing Hanoi, cubingHCM.
- Foreign guests win the main event (Xuanyi Geng 5.02 avg, 2025), so local competitiveness is partly masked.
- Registration fee rose from 80,000 VND (2022) to 500,000 VND (2026) per the Vietnam competitions summaries above (search summary; check each competition page).

Vietnamese community channels (counts are Facebook likes, not members, undated):
- Rubik VN (Hiep hoi Rubik Viet Nam official page): 11,303 likes https://www.facebook.com/vncubeassociation/
- Rubik Vietnam Club page: 4,010 likes https://www.facebook.com/rubikvietnam/
- Facebook group `groups/vietnamcubingclub` (member count not retrieved) https://rubikstore.vn/cau-hoi-thuong-gap
- Rubik Viet Nam club founded 2 Feb 2008 with ~50 offline and ~11,000 online members then (press summary, 2008-era) https://vtcnews.vn/tham-nhap-ban-doanh-cua-nhung-phu-thuy-rubik-9x-ar19118.html [UNVERIFIED primary; from search summary]
- Google Trends: Vietnam third in Rubik's Cube search interest after Hungary and Poland (H2 Rubik Shop article, 2019) https://rubikonline.vn/bat-mi-nhung-thong-tin-cuc-thu-vi-ve-nguoi-choi-rubik
- Hanoi school clubs organise WCA events (Hanoi Summer by CSP, Phan Dinh Phung, Hanoi-Amsterdam clubs; 2022) https://suckhoecongdongonline.vn/ha-noi-khai-mac-giai-thi-dau-rubik-toan-mien-bac [UNVERIFIED which year]
- Shops that double as community hubs: H2 Rubik Shop, Zyo Rubik, The Gioi Rubik, Rubik Ocean, Rubik For You.

### 5.3 Price tiers

International (USD, 2026):
- QiYi Smart Timer (Bluetooth): $19.99 https://www.thecubicle.com/products/qiyi-smart-timer-bluetooth
- SpeedStacks G5: $29.99 https://www.speedstacks.com/store/retail/speed-stacks-g5-timer/
- GAN Halo Smart Timer: $39.99-41.99 (sold out on GAN site at fetch) https://www.gancube.com/products/gan-halo-smart-timer ; resellers $41.95 https://speedcubeshop.com/products/gan-halo-timer
- GAN 356 i smart cubes: $25.99 to $44.99 https://www.thecubicle.com/collections/smart-cubes-and-bluetooth

Vietnam (VND, retailer listings as fetched 2026; check live):
- SpeedStacks Gen Pro 5: 950,000 VND; GAN Smart Timer: 750,000 (sale 490,000); QiYi Smart Timer: 220,000-250,000; QiYi Timer: 180,000; Moyu Timer V2: 190,000 https://thegioirubik.com/danh-muc/phu-kien/timer/
- H2 Rubik Shop lists G5 Pro Timer at 900,000 VND (out of stock) https://rubikonline.vn/speedstacks-g5-pro-timer-dong-ho-bam-gio-rubik-cao-cap
- Lazada SpeedStacks Pro Gen 5: 1,180,000 VND (50% off 2,360,000) from Toy Land, 1 rating https://www.lazada.vn/products/dong-ho-speedstacks-pro-timer-gen-5-dong-ho-choi-rubik-speed-stacks-rubic-do-choi-lap-rap-xep-hinh-i1877626603.html
- Shopee (via price-comparison pages, search snippet; Shopee itself not fetched): QiYi Timer about 126,000-199,000 VND; unbranded about 32,000 VND; a QiYi-branded item had 941 ratings at 4.9 stars (May 2023) https://websosanh.vn/s/gi%E1%BB%9D+rubik.htm [UNVERIFIED primary]
- Rough conversion (1 USD about 25,000 to 26,000 VND, [UNVERIFIED rate]): G5 is about $36-38 locally vs $30 in the US; QiYi about $5-8.

Tier summary: (a) budget touch timers 130-250k VND, (b) smart/Bluetooth 220-750k, (c) Stackmat G5 about 0.9-1.0M, with an inflated Lazada list price 2.36M. Haitay's BOM target should sit at or below the budget-to-smart tier to win Vietnamese buyers; students at HUST are the price-sensitive reference.

Market context: no 2025-2026 speedcubing market-size report found. Cube sales (300 million by 2005) and Ruwix visitor demographics (42% aged 18-24, 2012-2019) are weak proxies https://rubikonline.vn/bat-mi-nhung-thong-tin-cuc-thu-vi-ve-nguoi-choi-rubik .

---

## 6. What a polished timer + analytics product ships

Observed in prior art:
- GAN Halo: device, USB cable, hex wrench, manual in box; companion app (CubeStation), offline storage, cross-platform sync, Ao5, anti-false-trigger, 0.001 s accuracy, light effects (2026) https://www.gancube.com/products/gan-halo-smart-timer . Rechargeable battery roughly 42 h Smart / 32 h Standard per retailer text https://speedcubeshop.com/products/gan-halo-timer . Complaint: app "filled with promotions" and cannot delete times without CubeStation or reset.
- SpeedStacks G5: 2-pad/4-pad modes (hold RESET 5 s), reinforced buttons, snap-in mount, data port to external display (2026) https://www.speedstacks.com/store/retail/speed-stacks-g5-timer/ and https://rubikonline.vn/speedstacks-g5-pro-timer-dong-ho-bam-gio-rubik-cao-cap
- csTimer (open source, GitHub): web app, scrambles, sessions, export formats, Stackmat diagnostics, smart-cube support https://github.com/cs0x7f/cstimer
- Sub-X: analytics service with csTimer import and AI report https://subx.guru/
- Communication layer in open source: Stackmat JS library exposes packet fields `timeInMilliseconds`, hand flags, status (idle, starting, running, stopped, left/right/both hand, invalid) https://github.com/stilesdev/stackmat

Candidate deliverable set for Haitay (derived, not sourced): device hardware and enclosure; firmware (timing, inspection, penalties, user switch, local store); serial/USB protocol spec; PC dashboard with import/export (csTimer JSON/CSV compatible); data schema (user, session, solve with ms, penalty, scramble optional, splits, timestamp); user guide and setup guide; WCA-rule conformance table (this file, section 2.1); BOM and cost sheet; test log (accuracy against reference, false-start rate, battery life).

---

## 7. Gaps and unverified items
- r/Cubers, YouTube comments and Vietnamese Facebook groups: not mined (tool access blocked).
- No source found for explicit shared-timer club workflow; the evidence is indirect (school clubs, class teams, csTimer session-per-person workaround).
- No Vietnamese forum complaint about Stackmat price/battery found; price evidence is retailer listings only.
- Per-year global competitor totals not retrieved (WCA `/statistics` 404); global competition counts per year come from my API queries.
- Vietnam unique-competitor totals pre-2017 not available from public WCIF.
- Facebook like counts are undated.
- The instruction file `.../skills-plugin/.../deep-research/references/researcher.md` located under AppData was NOT read, because the user's global CLAUDE.md prohibits reading AppData; methodology followed directly: broad search, primary-page fetch, quote verification where possible.
