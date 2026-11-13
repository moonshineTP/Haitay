# Class project benchmarks for Haitay (IT4735 midterm)

Research date: 2026-10-08. Scope: sizing frame for a 2-person IoT midterm/mini-project (device + BLE + PC dashboard).

Evidence tags used throughout:
- [PRIMARY] official syllabus, regulation, standard, or dataset read directly in this session.
- [SYSTEMATIC] peer-reviewed study or review (abstract-level unless stated).
- [ANECDOTAL] blog, forum, repo README, single-course report, vendor page.
- [SNIPPET] statement seen only in a search-result summary, page not opened directly. Treat as unverified until opened.
- [INFERENCE] my own reasoning from the sources, not a sourced fact.
- [UNVERIFIED] needs a source before use in the report.

---

## 0. Bottom line

1. HUST publishes no rubric for the IT4735 project. What is public: 2 credits, 2(2-1-0-4), a "teamwork exercise building a specific IoT application", and (from the 2021 lecture slide) 50% process score (weekly exercises, major assignment) + 50% final (major assignment, report, presentation, oral Q&A). Exact midterm weight, team size, deliverable list: ask the lecturer or find the Teams/LMS post. Do not assume.
2. The official workload is small. HUST defines 1 credit as 50 learner-hours, so the whole 2-credit course is about 100 hours per student, and the course notation allots 4 h/week self-study. Any plan above roughly 60-90 project hours per student is voluntary over-investment. Decide that cap on purpose.
3. Comparable courses grade the same five things: a plan/proposal, a mid-point check, a working demo against a written spec, a written report (often the heaviest item, 20-50% of project grade), and individual accountability (peer evaluation or interview). Measured results ("measurable outcomes", "techniques for design and validation") are named explicitly in UVA and Cornell criteria. Haitay's validation plan (timing vs camera, power-loss, sync-loss, user trial) targets exactly that gap.
4. Student team capacity evidence clusters at 8-12 h/person/week alongside other courses; intensive embedded design courses ask 16-20 h/person/week for 4-5 weeks. A 2-person team therefore has about 16-24 person-hours per week.
5. Estimation evidence says to plan a 30-40% effort overrun on top of the estimate (software surveys), and BLE first projects are reported to take 3-10x longer than expected (anecdotal). Use PERT per work package, MoSCoW with Must <= 60% of capacity, and a frozen MVP gate two weeks before the demo.
6. Alignment risk [INFERENCE]: the IT4735 labs observed in a 20251 student repo are REST, MQTT (HiveMQ), Kafka, ESP32 WiFi config, Wokwi sensors. A BLE-to-PC design sits outside that taught stack. Adding a visible MQTT or REST hop (PC app to broker/DB) makes the architecture map to the course's protocol and data-pipeline content at little cost.

---

## 1. HUST SoICT IT4735 "IoT va ung dung": what is findable

### 1.1 Program document [PRIMARY]
SoICT Computer Engineering program PDF lists the course. Extracted text (diacritics lost in the PDF encoding, meaning clear):
- IT4735 IoT va ung dung (IoT and Applications), 2(2-1-0-4), prerequisite none, pre-course IT3030.
- Objectives: overview of IoT; architecture, layer model, components; communication protocols; application fields; IoT data collection, processing and analysis; reliability, security and privacy; "students will execute step by step to build IoT application in some specific fields"; teamwork, research, presentation skills.
- Contents end with "teamwork exercise for building a specific application of IoT" (bai tap nhom xay dung mot ung dung cu the cua IoT).
- URL: https://soict.hust.edu.vn/wp-content/uploads/Bachelor-Computer-Engineering-program.pdf (course is in elective Module 1, Embedded Systems and IoT; alongside IT4210 Embedded Systems, IT4785 Mobile Programming).

### 1.2 Assessment slide, lecture deck v2021 [SNIPPET + one fetch]
A fetch of the SlideShare deck returned slide 4 "Gioi thieu hoc phan":
- "Qua trinh: 50%, Bai tap tuan, Bai tap lon"
- "Cuoi ky: 50%, Bai tap lon, bao cao, thuyet trinh, van dap"
- Lecturer on that deck: TS. Pham Ngoc Hung. Deck is 2021 and may be outdated.
- URL: https://www.slideshare.net/slideshow/it4735iot-va-ung-dungv2021pdf/262849382
- Not stated: team size, deliverable list, midterm checkpoint, rubric. [UNVERIFIED] for the current semester and for Dr. Dang Tuan Linh's section.

### 1.3 Lecturer context [PRIMARY]
Dr. Dang Tuan Linh's SoICT profile lists IT4735 and IT4735E (English version); research: object detection, lightweight ML, computer vision on edge devices. https://soict.hust.edu.vn/ts-dang-tuan-linh.html
[INFERENCE] An AIoT/edge-leaning lecturer may reward the data-analysis and edge-computation angle (on-device Ao5/Ao12/Ao100 statistics, trend analysis) in addition to connectivity.

### 1.4 What peer teams build (IT4735 student repos) [ANECDOTAL]
- IoT Kiosk Check-in (GitHub nguyenLTpk/IoT-IT4735): one ESP32, three readers (RDM6300 125 kHz RFID over UART, MFRC522 13.56 MHz over SPI, QR scanner over UART), SH1106 OLED, buzzer, button; Python FastAPI + paho-mqtt + SQLite server; React/Vite/Tailwind dashboard with 3 s refresh; device lock sequence. This is the "RFID/attendance" archetype and sets the visible bar for a polished conventional project: 3 peripherals + MQTT + REST + DB + web UI. https://github.com/nguyenLTpk/IoT-IT4735
- 20251 lab repo (hunganh1310): weekly work is REST/MQTT scripts (wk5), Kafka producers/consumers (wk7), ESP32 + DHT22 + PIR + I2C LCD on Wokwi (wk10), WiFi provisioning via AP mode and Preferences (wk10 HW), MQTT remote LED/button via HiveMQ (wk11). https://github.com/hunganh1310/20251-IT4735-IoT-Lab
- Studocu lists HUST IT4735 reports (e.g. smart irrigation, group 12; ESP32/MQTT/HTTP/RabbitMQ weekly reports): https://www.studocu.vn/vn/course/truong-dai-hoc-bach-khoa-ha-noi/iot-va-ung-dung/6533465 (page body not retrievable; titles via search snippet).
- Slides cite a demo repo for MQTT sensor ingestion (https://github.com/hungpn37/iot_mqttdemo, via search snippet) [SNIPPET].

### 1.5 HUST credit arithmetic [PRIMARY]
HUST Training Regulation (QD 4600, 2023), Article 4: "1 TC = 50 hours of learner workload" including class, guided, self-study, research, assessment. Per credit the class-time equivalence is at least 15 lecture hours, or 30 practice/lab/discussion hours, or 45 hours of term paper / major assignment / project. Article 5: for courses of 2+ credits, final score weight is 0.5 to 0.8 per the course syllabus; process score may include midterm, regular tests, labs, major assignments, essays, attendance (attendance modifies the process score: 0 absences +1, 1-2 absences 0, 3-4 absences -1, 5+ absences -2). Component below 3/10 is a fail ("diem liet").
- URL: https://soict.hust.edu.vn/wp-content/uploads/QCDT.pdf (2023 edition). A 2025 edition exists (QD 5445): https://ctt.hust.edu.vn/Upload/Nguy%E1%BB%85n%20Qu%E1%BB%91c%20%C4%90%E1%BA%A1t/files/DTDH_QDQC/Hoctap/QCDT_2025_5445_QD-DHBK.pdf [SNIPPET for 2025 differences; I read only the 2023 text].
- Reading 2(2-1-0-4) as 2 credits, 2 h/week theory, 1 h/week exercises, 0 lab, 4 h/week self-study is consistent with other HUST syllabi (PH1110 3(2-1-1-6), PH1120 2(2-0-1-4)) [SNIPPET from search; not an official definition page].
- [INFERENCE] 2 credits x 50 h = 100 h per student for the whole course; 4 self-study h x 15 weeks = 60 h. A project exceeding about 60-90 h per student already exceeds the nominal allowance.

---

## 2. Deliverables and rubrics in comparable courses

Quoted or paraphrased from the syllabus pages. Weights are of the project component unless noted.

| Course | Team | Deliverables | Weights | URL |
|---|---|---|---|---|
| Cornell ECE 4760 (Pico, 4-5 wk final project) | pairs implied | weekly progress report (tasks, hours spent, next goals), demo with code review, HTML report with test data, schematics, task breakdown | Project = 50% of course: preparedness 10, weekly progress 20, demo 30, report 40 (page also shows 20/30/50 in its outline, internally inconsistent) | https://vanhunteradams.com/Pico/CourseMaterials/Final_Project.html |
| Berkeley ME 100 (ESP32 IoT, 2021) | 1 or 2 | concept outline (need, users, requirements, approach), live design review with Q&A, final video + slides | concept 25, design review 25, final outcome 50; project = 25% of course; no final exam | https://tbp.studentorg.berkeley.edu/syllabi/1548/download/ |
| UVA ECE 4430/6501 (Spring 2026) | 3-4 | milestones chosen mid-semester, end-of-semester design competition with demo, optional report, peer grading by rubric | final project 20%; judged on idea, "techniques used for design and validation", "demonstrating working prototypes and measurable outcomes", presentation quality | https://homa-alem.github.io/teaching/ece_6501/6501_syllabus.pdf |
| Pitt ECE 455/599 [SNIPPET] | n/a | proposal, midterm presentation, final presentation, final report | project 50%: proposal 5, mid presentation 10, final presentation 15, report 20 | https://sites.pitt.edu/~weigao/old_courses/ece455/fall2012/ece455-fa12.html (2012, outside window) |
| UPRM ICOM4217 [SNIPPET] | 2-4 | proposal, progress reports, written report, presentation, peer evaluation, individual interviews | 40 points: progress 10, report 15, "happy hour" 10, presentation 5 | http://www.ece.uprm.edu/~mjimenez/icom4217/ |
| Oregon Tech embedded program report [SNIPPET] | n/a | block diagram, HW/SW description, live demo | live demo 30 points, items-complete/total scoring, no partial credit | https://www.oit.edu/sites/default/files/2021/documents/2019-20%20Embedded%20Systems%20Engineering%20Technology%20BS%20Report.pdf |
| Cornell ECE 5725 (RPi) [ANECDOTAL via past projects] | pairs typical | project website with demo video, objective, budget, team section | rubric not public | https://skovira.ece.cornell.edu/ece5725/ |
| Berkeley INFO 290 IoT (2016) [SNIPPET] | 2-3 | team prototype, final presentations | n/a | https://courses.ischool.berkeley.edu/i290-iot/s16/ |

Cornell ECE 4760 demo criteria [PRIMARY]: appropriate hardware/software complexity; appropriate external hardware; "works according to a specification you write"; usability and user experience; possible code review. Report sections include results with "test data, speed, accuracy, and safety", a "what failed" discussion, and a task breakdown appendix. Groups can be graded differentially if one person does the bulk. Late demo scores zero.

Pattern across rows [INFERENCE]: proposal 5-25%, midpoint 10-25%, demo 30-50%, report 20-40%, with individual accountability handled by peer evaluation or interview. Haitay deliverable set that satisfies all rows: one-page spec (written up front), architecture diagram, repo with README, demo (live + backup video), report with measurement chapter, contribution statement per member (git log + task table).

### 2.1 IoT project-based learning literature [SYSTEMATIC, abstract-level only; full texts returned 403]
- Zhou and Liang, "Transforming Internet of Things Education Through Project-Based Learning: A Decade of Experience," Applied System Innovation 9(10):205 (2026). Three-stage sequence: single-node sensing/actuation, network-connected device with standard protocols, open-ended capstone prototype. Evaluated with anonymous pre/post surveys and rubric-based project assessment across Fall 2020, Fall 2021, Spring 2023, Spring 2024; discusses hardware debugging, toolchain configuration, and project scoping as recurring problems. https://www.mdpi.com/2571-5577/9/10/205
- Tecnologico de Monterrey, PBL with IoT in COVID era (ACM 2022): 112 participants over 4 periods; measures were questionnaires, rubrics, interviews, observation, artifacts, log data. https://dl.acm.org/doi/fullHtml/10.1145/3510309.3510327
- Kleinschmidt (2021), IoT for engineering via project-based cooperative approach: technology areas are sensing/actuation, embedded computing, communication, cloud, analytics. https://journals.sagepub.com/doi/abs/10.1177/0020720919867437
- ET601X (IoT + data analytics, PBL): checkpoints follow requirements, planning/scheduling, design/coding, testing. https://www.researchgate.net/publication/312485338_Project_Based_Learning_for_Internet_of_Things_and_Data_Analytics_Experience_Report_of_Learning_from_ET601X
- Assessing IoT projects in university education, a problem-based learning framework (3-year action research; argues a general evaluation criteria set can be composed despite varying project complexity). https://www.researchgate.net/publication/315754361_Assessing_IOT_Projects_in_University_Education_-_A_Framework_for_Problem-Based_Learning
- Review (IEEE, via search summary): 15 PjBL papers, 5 problem-based, 5 collaborative; example 7-week project course; teams of 3-4 in a hands-on ECE course. [SNIPPET] https://ieeexplore.ieee.org/ielaam/6287639/9668973/9749084-aam.pdf (fetch returned 418).
- Gap: no systematic source found that states a typical sensor count, firmware LOC, or screen count for a 6-10 week student IoT project. Scope benchmarks below come from course pages and repos instead.

---

## 3. Scope benchmarks (6-10 week, 2 students)

No systematic LOC or module-count benchmark found. Calibration points:

1. Cornell ECE 4760: 4-5 weeks, "no other assignments during that period", students told to plan "~16-20 hours per week" [PRIMARY]. Past topics (169 listed) are single-MCU devices with one core idea each (WiFi walkie talkies, WiFi bike navigation, ScopeBoy handheld oscilloscope, logic analyzer, BLDC controller, custom smartwatch). Page titles only; no BLE-labelled project. https://ece4760.github.io/Projects/Projects.html
2. Peer IT4735 kiosk (section 1.4): 1 MCU, 3 input peripherals, MQTT, FastAPI, SQLite, React dashboard. Similar breadth to Haitay's MVP, but no custom timing, storage, or BLE layer.
3. Hobbyist speedcubing timers (direct size comparators) [ANECDOTAL]:
   - ojdip ESP32 Bluetooth timer: capacitive touch pads, 4 buttons, 2 LEDs, OLED, BLE to a Create React App web demo, no enclosure, breadboard only, BOM about 15 EUR, build time not stated. Lessons: OLED I2C transfer took about 15 ms so state machine moved to a 1 ms hardware timer; Classic Bluetooth gave random crashes so moved to BLE; separate state characteristic gave "GATT operation failed" so merged into one packed characteristic. https://ojdip.net/2020/11/esp32-cube-timer/
   - tibordp/cube-timer: same design with KiCad files, tests, GitHub Pages Web Bluetooth demo, 5 commits, claimed accuracy about 2 ms with no supporting data. https://github.com/tibordp/cube-timer
   - StackmatLink: ESP32-S3 converts raw Stackmat audio-jack signal into GAN Smart Timer BLE protocol for csTimer. https://github.com/liusonwood/StackmatLink
   [INFERENCE] The "ESP32 + display + BLE + web demo" core is already hobby-reproducible. Haitay's differentiators are on-device Ao5/Ao12/Ao100, per-user storage, BLE sync with conflict handling, a PC dashboard with time-series analysis, and measured validation. The smart-cube link is an extra dependency: GAN-protocol cubes encrypt traffic with AES and derive keys from the cube MAC address, and Web Bluetooth cannot always read the MAC (csTimer needs an experimental Chrome flag). https://gist.github.com/afedotov/52057533a8b27a0277598160c384ae71 and https://github.com/mjohnson139/gan-cube-sample [SNIPPET]. Treat as Could/Won't-for-now.
4. What makes projects stand out, from rubric language [PRIMARY]: written spec and meeting it (Cornell), measurable outcomes and validation technique (UVA), user experience (Cornell), a demo that works end to end (OIT: demo carries 30 points). Novelty alone is not a listed criterion in these syllabi. [INFERENCE] The angle "operational service for the cuber" is rewarded only if the demo shows data flowing device to dashboard with an insight (trend, PB detection) and a measured claim.

---

## 4. Effort, availability, slippage

### 4.1 Hours available [mixed]
- HUST nominal: 4 h/week self-study for the entire course [PRIMARY inference, section 1.5].
- Intensive embedded course: 16-20 h/week/person for 4-5 weeks (Cornell) [PRIMARY].
- Other capstone expectations [SNIPPET]: BYU 10 h/person/week (8 project); UT Dallas teams of 4-6 average 10-12 h/week each; AIChE curriculum survey: most common weekly time 6-10 h at 62% of institutions; Northeastern Khoury 20 h/week for 15 weeks; a 2026 Capstone Design Conference paper expects 24 h/week; College of the Ozarks quotes about 600 person-hours for teams of 2-4. URLs: https://capstone.groups.et.byu.net/wikis/doku.php?id=project-wiki%3Asyllabus%3Acapstone_time_management , https://utdesign.utdallas.edu/partners/faq-corporate , https://www.cofo.edu/Academics/Majors-Minors/Engineering/Capstone-Projects-FAQ , https://www.khoury.northeastern.edu/research/capstone-projects/
- NSSE (US): engineering seniors prepare for class about 19 h/week across all courses, the highest of any major group [SNIPPET, 2011/2014 data]. https://www.chronicle.com/article/engineering-majors-hit-the-books-more-than-business-majors-do-survey-finds/ . Implication: a student carrying 4-6 courses cannot give one 2-credit course more than about 8-12 h/week without displacing others [INFERENCE].
- Planning figure for the team: 8-12 h/person/week, 16-24 person-h/week for two.

### 4.2 Time to build comparable systems
No source gives hours for MCU + BLE + companion app + dashboard built by students. Nearest evidence:
- Cornell: pair, 4-5 weeks, 16-20 h/week/person is the design intent for one self-contained MCU project: about 130-200 person-h for two [INFERENCE from PRIMARY inputs].
- College of the Ozarks: 600 person-h per capstone for 2-4 members [SNIPPET].
- BLE alone: "somewhere between three and ten times longer than they expected" for a first BLE project because of stacked stages (advertising, connection, discovery, permissions, descriptors) and a phone OS that misreports cached GATT state [ANECDOTAL, vendor blog]. https://hubble.com/community/guides/why-your-first-ble-project-won-t-connect-and-how-to-fix-it/
- BLE gotchas that consume days [ANECDOTAL/vendor docs]: ATT MTU stuck at 23 (20-byte notifications) until negotiated; Web Bluetooth has no MTU or connection-priority API; supervision timeout under 500 ms drops links; reconnect can re-trigger MTU events. https://punchthrough.com/ble-connection-parameters-guide/ , https://github.com/WebBluetoothCG/web-bluetooth/issues/383 , https://www.espruino.com/Troubleshooting+BLE
- Overall software effort overrun: 60-80% of projects overrun effort; average 30-40% (Moloekken-Oestvold and Joergensen survey review); later work suggests 20-30% (Halkjelsvik and Joergensen 2012) [SYSTEMATIC via summaries]. https://cms.simula.no/sites/default/files/publications/SE.3.Moloekken-Oestvold.2004.pdf . Also: a 90% confidence interval contained the actual effort only 60-70% of the time [SNIPPET].
- Student-specific planning fallacy: Buehler, Griffin and Ross (1994, JPSP 67(3):366-381), honors-thesis students predicted 33.9 days, took 55.5 days; the actual time exceeded the average worst-case estimate (48.6); about 30% finished by their predicted time. Numbers via secondary summaries [SNIPPET]; DOI https://doi.org/10.1037/0022-3514.67.3.366 (ResearchGate copy returned 403). Debiasing: recalling similar past tasks removed the bias (Study 4), supporting reference-class estimates.
- Hardware slippage (quadcopter capstone, 10 weeks, pairs after the first two labs) [ANECDOTAL single course, 2018, outside window]: "an error in a student design can delay their project by at least two weeks" and the largest delays were PCB layout finalization, assembly, and the PID/flight software; PCBs from JLCPCB "usually arrive within 5-7 days of ordering" (US delivery); staff added a "software blackout" so software work did not displace PCB layout. https://arxiv.org/pdf/1810.07646 (read from the downloaded PDF).

### 4.3 PCB versus perfboard versus enclosure [INFERENCE from 4.2]
A custom PCB adds a design-review loop with a minimum 2-week penalty per respin and international shipping to Vietnam [UNVERIFIED lead time]. Both hobby precedents (ojdip, tibordp) stayed on breadboards. Evidence-consistent plan: perfboard or module-based MVP; PCB or 3D-printed enclosure only as a Could with its own gate date.

---

## 5. Estimation and management methods that fit 2 people

| Method | Use for Haitay | Reference |
|---|---|---|
| Work breakdown structure | List every deliverable and its work packages; the 100% rule says child elements sum to the parent scope. "8/80 rule" (8-80 h per package) is a practitioner heuristic, not in the PMI standard. | PMI Practice Standard for WBS (3rd ed., 2019); summary: https://whichframework.org/frameworks/work-breakdown-structure.html [SNIPPET] |
| Three-point (PERT) | E = (O + 4M + P)/6, SD = (P - O)/6; add variances across packages. Most useful with new technology and limited history (BLE, Web Bluetooth). Beta/4:1 weighting is a convention. | PMBOK three-point estimating; https://projectmanagementacademy.net/resources/blog/a-three-point-estimating-technique-pert/ [SNIPPET, not PMBOK itself] |
| MoSCoW | Must is the minimum usable subset; guideline: Must <= 60% of timebox effort, Should/Could about 20% each as contingency; percentages are effort, not item counts. | Agile Business Consortium (DSDM): https://www.agilebusiness.org/resource/what-is-moscow-prioritization/ |
| Definition of Done, increments | A backlog item is done only when it meets the DoD; items that fail it return to the backlog. Scrum Guide 2020 prescribes no story points or velocity; those are optional practice. | https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-US.pdf |
| T-shirt size or story points + velocity | With 2 people and about 6-10 weeks, velocity needs 2-3 sprints to stabilize, so use hours-based PERT for packages and use weekly check-ins to recompute remaining work. [INFERENCE] | n/a |
| Risk register | Probability x impact. PMBOK example scales: probability 0.1/0.3/0.5/0.7/0.9, impact 0.05/0.1/0.2/0.4/0.8. Matrices need agreed definitions per level. | https://www.pmi.org/learning/library/risk-analysis-decisions-uncertain-times-6686 [SNIPPET] |
| Cone of uncertainty | Estimates at initial concept can be off by 4x high or 0.25x low; after requirements spec 1.5x / 0.67x; the cone narrows only through decisions, not with time. Argues for freezing requirements and the BLE/data contract early. | Construx/McConnell: https://www.construx.com/wp-content/uploads/2019/02/CxWhitePaper_ConeOfUncertainty.pdf |
| COCOMO limits | COCOMO II was calibrated on 161 projects (2000), depends on KLOC estimated before coding, and its constants date from large professional projects. Not suitable for a 2-person, few-KLOC mixed HW/SW project; use as a sanity check only. Lower size bound claim "about 2 KSLOC" came from the search tool's memory: [UNVERIFIED]. | https://dl.acm.org/doi/10.5555/557000 |
| COCOMO 81 phase split (small) | Plans/requirements 6% (added on top), product design 16%, programming 68%, integration and test 16% for small projects; large projects shift toward test (to 25%+). Detailed design/code split 26/42 recalled by the search tool: [UNVERIFIED]. | https://dl.acm.org/doi/pdf/10.1145/1414004.1414016 [SNIPPET] |
| Brooks's law | "Adding manpower to a late software project makes it later": ramp-up, communication paths n(n-1)/2, indivisible tasks. For n = 2 there is one communication path, so the law is no argument against two people; its practical content is to cut scope, not add help, and to split by interface. | Brooks, The Mythical Man-Month (1975); summary: https://en.wikipedia.org/wiki/Brooks%27s_law |
| Hofstadter's law / planning fallacy | "It always takes longer than you expect, even when you take into account Hofstadter's Law" (GEB, 1979). Planning fallacy evidence in section 4.2. | https://en.wikipedia.org/wiki/Hofstadter%27s_law |

### 5.1 Illustrative PERT frame for Haitay [INFERENCE, placeholder numbers to be replaced by the team]
Person-hours for the whole team, invented as a template, not evidence:

| Work package | O | M | P | E | SD |
|---|---|---|---|---|---|
| 1 Requirements, spec, BOM, ordering | 4 | 6 | 10 | 6.3 | 1.0 |
| 2 Timer core firmware (sensing, 1 ms timebase, display, state machine) | 12 | 20 | 40 | 22.0 | 4.7 |
| 3 On-device stats + per-user storage, power-fail-safe | 10 | 18 | 36 | 19.7 | 4.3 |
| 4 BLE GATT service + sync protocol (firmware side) | 10 | 20 | 50 | 23.3 | 6.7 |
| 5 PC app + dashboard | 16 | 28 | 56 | 30.7 | 6.7 |
| 6 Integration and stabilization | 8 | 14 | 30 | 15.7 | 3.7 |
| 7 Validation (timing, power-loss, sync-loss, user trial) | 8 | 14 | 24 | 14.7 | 2.7 |
| 8 Report, video, demo rehearsal | 10 | 16 | 24 | 16.3 | 2.3 |
| Total | | | | 148.7 | 12.5 (sqrt of summed variances) |
| 9 Smart-cube BLE link (Could) | 12 | 24 | 60 | 28.0 | 8.0 |

Check against capacity: if Must work is at most 60% of capacity (DSDM guideline), 149 h needs about 248 person-h of capacity, which is about 10 weeks at 24 h/week or 8 weeks at 31 h/week for the team. The +3 SD upper tail of the PERT estimate is 149 + 37 = 186 h, and planning-fallacy evidence suggests the true tail is fatter. If the deadline is closer, cut package 5 or 3 to the minimum that still tells the story (a CSV import plus three charts) before cutting validation.

---

## 6. Milestone structure for hardware + software projects

Sources give structure, not measured proportions for IoT. Anchor points:
- Cornell ECE 4760: weekly progress report with hours; demo; HTML report. Report and demo = 70% of the project grade.
- Berkeley ME 100: concept, design review, final video; mid-point review at about the 60% mark of a roughly 11-week window (2020 dates: Oct 19, Nov 2, Dec 11) [SNIPPET].
- Quadcopter capstone course in arXiv 1810.07646 (10 weeks, university not verified): H1 and H2 PCB basics 1 week each, H3 design 1.5, H4 layout 1.5, S1 1 week, S2 and S3 1.5 each; flight integration last; about three weeks held for slippage; no enforced deadlines after H3 [ANECDOTAL].
- COCOMO 81 small-project split (section 5).
- 12-week IoT project plan (non-HUST, Studocu, via search): requirements and system diagram wk2, analysis and design wk4, detailed design and UI mockup wk6, prototype demo wk9, test report wk10, final report and demo wk11-12 [SNIPPET, non-HUST]. https://www.studocu.com/my/document/uitm-kampus-dungun/chemical-engineering-program/ke-hoach-12-tuan-thuc-hien-bai-tap-lon-cong-nghe-iot/148878102

Proposed sequence and share of effort [INFERENCE; derived from the COCOMO and course shapes above]:

| Phase | Share | Exit gate |
|---|---|---|
| Requirements, spec, BOM, order parts (long-lead first) | 8-10% | one-page spec with numeric targets (e.g. timing error limit), BOM ordered |
| Bring-up of each module in isolation (sensing, display, storage, BLE hello) | 18-22% | each module passes its own bench test with logged evidence |
| Integration | 15-20% | device runs a full solve-to-stats loop |
| Firmware stabilization + sync protocol | 10-15% | 30-minute soak with no reset |
| App and dashboard | 15-20% | live data from device to chart |
| Testing and measurement | 10-12% | timing, power-loss, sync-loss, user-trial data in hand |
| Documentation and demo rehearsal | 10-12% | report draft, backup video, two full rehearsals |
| Reserve | held inside each phase via PERT; plus a final 1-week freeze before the demo | feature freeze at 80% of calendar |

Process rules with evidence: blackout window for the discretionary side (software polish) while PCB or enclosure decisions are open (quadcopter course); define the data contract (GATT characteristic layout, sync record format) before both sides code, since BLE failures are hard to localize [ANECDOTAL]; one-characteristic packed-struct notify reduced failures in ojdip's build.

---

## 7. Testing and validation evidence

### 7.1 Timing accuracy
- What the standard demands [PRIMARY]: WCA Regulation 9f1: timed results under 10 min are measured and truncated to hundredths of a second; averages are rounded to the nearest hundredth. Regulation 7f1a: Stackmat Gen 3, 4, 5 Pro Timers must be used; A1b: if the Stackmat time is available it is the original recorded time. https://regulations.worldcubeassociation.org/wca-regulations-and-guidelines.merged.pdf
- Resolution implication [INFERENCE]: the official unit is 10 ms. A device claiming about 2 ms accuracy (tibordp) with no data cannot be certified from the claim alone; a validation showing error well below 10 ms (for example max absolute error under 5 ms) is meaningful against WCA resolution.
- Reference-method options:
  1. High-speed camera filming the device and a reference counter or LED clock together, frame-by-frame readout. Frame interval is 4.17 ms at 240 fps and 1 ms at 1000 fps; exposure, rolling shutter, and dropped frames add error, so verify actual timestamps rather than a slow-motion export. A calibration lab method filmed the stopwatch with a 1 kHz-driven synchronous counter, giving 1 ms readout resolution, and used long intervals so frame quantization matters less. https://www.itc.gov.hk/en/quality/scl/doc/scl/stopwatchescalibration.pdf [SNIPPET]
  2. NIST stopwatch calibration guidance: longer measured intervals reduce operator start/stop uncertainty. https://tf.nist.gov/general/pdf/1930.pdf [SNIPPET]
  3. Logic analyzer or oscilloscope on the start and stop GPIO edge versus a signal generator pulse train of known width gives microsecond-level truth for the firmware path, but not the display path (OLED I2C update took 15 ms in the ojdip build, which only a camera or photodiode shows) [ANECDOTAL].
  4. Compare against a Stackmat on the same sensor event (start and stop together) for relative error.
- Statistics: Bland-Altman limits of agreement. Bland recommends about 100 pairs (CI of the limits about +/-0.34 s_d at n=100); standard error of limit about sqrt(3 s_d^2 / n). Fewer than 30 pairs gives very wide intervals; published studies' median sample size was 65. https://www-users.york.ac.uk/~mb55/meas/sizemeth.htm and https://www.mdpi.com/2075-4418/10/5/334 [SNIPPET]. For a student scope: 3-5 durations (e.g. 2 s, 10 s, 60 s) x 20 repetitions each (60-100 pairs), report mean bias, SD, limits of agreement, and the camera's own frame error budget.
- Clock drift note [UNVERIFIED]: typical ESP32 crystal tolerance about 10 ppm implies about 0.6 ms per minute worst case. Confirm against the datasheet before quoting.

### 7.2 Reliability
- Storage: ESP-IDF documentation presents NVS as designed for power-loss resilience with built-in wear balancing but unsuitable for frequent or large writes; LittleFS has good power-failure resilience and dynamic wear leveling; SPIFFS may corrupt on power loss (repair via esp_spiffs_check); FAT has no power-fail protection. These are design claims, not published test data. https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/file-system-considerations.html , https://docs.espressif.com/projects/esp-faq/en/latest/software-framework/storage/nvs.html [SNIPPET]
- No standard sample size found for student power-loss tests. Practical protocol [INFERENCE]: a second MCU or relay cuts power at randomized offsets during a write loop, N = 50-100 cuts, then verify record integrity on reboot (zero corrupted or lost committed records is the pass criterion; report the count). Add a sync-loss test: drop BLE at randomized points mid-transfer, N = 20-50, verify no duplicate or lost solves after reconnect.

### 7.3 Usability
- Nielsen: qualitative tests with 5 users find about 85% of problems (31% per user), best run as three rounds of 5 with redesign between; quantitative metrics need about 20 users; separate groups need 3-4 each. https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/ [PRIMARY, fetched]
- SUS: Tullis and Stetson (2004) found 12-14 respondents give the correct winner in over 90% of cases when comparing two designs; absolute scores at n of 8-12 have wide intervals. [SNIPPET] https://files.eric.ed.gov/fulltext/EJ1061142.pdf
- For N cubers: 5 cubers of mixed level (beginner, sub-30, sub-15) in one formative round with task list (start solve, inspection, delete last time, switch user, view Ao12, sync) plus SUS, reported as formative. Do not claim statistical significance.

---

## 8. Pitfalls and mitigation

| Pitfall | Evidence | Mitigation |
|---|---|---|
| Scope creep | Cone of uncertainty; Brooks; DSDM Must <= 60% | frozen MVP gate, Won't list, smart cube as Could |
| Parts lead time | Shopee domestic 1-7 working days (SPX Nhanh 1-4); cross-border listed at 10 days (one source), other sources 7-15, up to 20 with customs [SNIPPET]; AliExpress lead time not found [UNVERIFIED]. https://salework.net/thoi-gian-giao-hang-shopee/ | order all long-lead parts in week 1; buy 2 of every module; use local shops (Hanoi) for urgent replacements |
| BLE debugging | 3-10x first-project overrun (vendor blog); MTU/connection-parameter traps | sniffer (nRF Connect or phone logs) from day 1; one packed characteristic; PC-side BLE library chosen before dashboard work; timebox 1 week then fall back |
| Web Bluetooth/OS variance | no MTU API, Linux unofficial; Windows quirks [SNIPPET] | test on the demo laptop weekly; keep demo machine frozen |
| PCB respin | 2+ week penalty per error (quadcopter paper) | perfboard MVP; PCB only if reviewed twice |
| Timing path blocked by display I2C (15 ms) | ojdip | 1 ms hardware timer + ISR for the timebase; display on low priority |
| Demo-day failure | course and student guides recommend backup video, second board, frozen setup, failure rehearsals, one core user journey, script a recovery line, test in venue-like conditions [ANECDOTAL] https://roboticsknowledgebase.com/wiki/robotics-project-guide/demo-day/ , https://openbooks.library.unt.edu/seworkbook/chapter/chapter-11-demos , https://www.techedubyte.com/hardware-project-failed-demo-day-lessons-stem-students/ | 60-90 s backup video; spare assembled board with identical firmware; seeded demo dataset on the PC so the dashboard works with no live device |
| Uneven contribution | Cornell differential grading; UPRM peer eval + interviews | task table with owner per package; commit history; written contribution statement |
| Writing left last | report weight 20-50% in comparable courses | skeleton report in week 2; measurement chapter drafted as tests run |

---

## 9. Cost norms (Vietnam)

No survey of student IoT mini-project budgets in VND found. Price points seen [SNIPPET unless noted]:
- ESP32 learning kits about 270,000 to 485,000 VND (lkcg.vn combo 270,000; Dien tu Tuyet Nga 300 pcs 355,000; ESP-2S starter 485,000; BLK basic kit 1,200,000 excl. VAT). https://lkcg.vn/combo-bo-kit-hoc-tap-nhung-iot-esp-32s , https://dientutuyetnga.com/products/bo-kit-hoc-tap-phat-trien-iot-esp32 , https://www.linhkientot.vn/products/esp32-iot-supper-starter-kit-bo-thuc-hanh-esp32-iot-esp-2s-starter-kits , https://banlinhkien.com/bo-kit-hoc-tap-esp32-iot-co-ban-blk-p38420583.html
- hoclaptrinhrobot.com (page dated 05/07/2026) [fetched]: extra cost per small ESP32 project 30,000 to 250,000 VND (weather station with OLED 110,000; phone-controlled car 250,000); ten projects together under 1.1 million VND; board price not included. https://hoclaptrinhrobot.com/kien-thuc/10-du-an-robot-esp32-cho-nguoi-moi
- ojdip BOM about 15 EUR for the full ESP32 timer on breadboard [ANECDOTAL, 2020].
- Cornell ECE 5725 (2017): budget limit under 100 USD excluding RPi, display, charger, SD, case [ANECDOTAL].
- Search-tool estimate bands (not a source): basic 150,000-500,000 VND; medium 500,000-1.5 M; advanced with custom PCB and 3D-printed case 1.5-4 M VND. [INFERENCE/UNVERIFIED]
- [INFERENCE] Haitay: two ESP32 boards, display, touch pads or optical sensor, Li-ion cell + charger module, wiring, a printed or bought case, and spares plausibly fall around 0.6-1.5 M VND; a custom PCB order and printed enclosure push toward 1.5-3 M VND. Verify with real Shopee cart prices.
- Funding: no course-level or SoICT funding for IT4735 projects found. Search returned only PhD/scholarship items, not student project grants. Ask the lecturer, the SoICT lab, or the student-research office; labs may lend instruments (logic analyzer, oscilloscope, high-speed camera). [UNVERIFIED]

---

## 10. Open items for the team

1. Ask the lecturer: project weight, midterm date and what is graded then, team rules, required report format, whether a non-WiFi/MQTT architecture is acceptable.
2. Record the actual calendar: weeks remaining until the midterm demo; replace the capacity table with real hours.
3. Replace section 5.1 numbers with the team's own O/M/P and re-run capacity check.
4. Decide a measured-claim list up front (timing error limit, power-loss pass criterion, sync-loss pass criterion, SUS target) and make it the spec.
5. Open the unfetched primary texts before citing: MDPI 2026 paper (403), ACM 2022 paper (403), IEEE review (418), Buehler 1994 (403), Pitt and UPRM syllabi, NIST/SCL stopwatch PDFs, PMBOK itself.

---

## 11. Source list (consolidated)

HUST and course:
- https://soict.hust.edu.vn/wp-content/uploads/Bachelor-Computer-Engineering-program.pdf
- https://soict.hust.edu.vn/wp-content/uploads/QCDT.pdf
- https://www.slideshare.net/slideshow/it4735iot-va-ung-dungv2021pdf/262849382
- https://soict.hust.edu.vn/ts-dang-tuan-linh.html
- https://hocbk.daotao.ai/courses/course-v1:SoICT+IT4735+2023-1-144947/about
- https://soict.daotao.ai/courses/course-v1:SoICT+IT4735+LinhDT/about
- https://github.com/nguyenLTpk/IoT-IT4735
- https://github.com/hunganh1310/20251-IT4735-IoT-Lab
- https://tailieuhust.com/tai-lieu-iot-va-ung-dung-hust/ (links to external Drive folder only)

Syllabi and course pages:
- https://vanhunteradams.com/Pico/CourseMaterials/Final_Project.html
- https://tbp.studentorg.berkeley.edu/syllabi/1548/download/
- https://homa-alem.github.io/teaching/ece_6501/6501_syllabus.pdf
- https://ece4760.github.io/Projects/Projects.html
- https://skovira.ece.cornell.edu/ece5725/
- https://arxiv.org/pdf/1810.07646

IoT education literature:
- https://www.mdpi.com/2571-5577/9/10/205
- https://dl.acm.org/doi/fullHtml/10.1145/3510309.3510327
- https://journals.sagepub.com/doi/abs/10.1177/0020720919867437
- https://www.researchgate.net/publication/312485338_Project_Based_Learning_for_Internet_of_Things_and_Data_Analytics_Experience_Report_of_Learning_from_ET601X
- https://www.researchgate.net/publication/315754361_Assessing_IOT_Projects_in_University_Education_-_A_Framework_for_Problem-Based_Learning

Project management and estimation:
- https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-US.pdf
- https://www.agilebusiness.org/resource/what-is-moscow-prioritization/
- https://www.construx.com/wp-content/uploads/2019/02/CxWhitePaper_ConeOfUncertainty.pdf
- https://cms.simula.no/sites/default/files/publications/SE.3.Moloekken-Oestvold.2004.pdf
- https://doi.org/10.1037/0022-3514.67.3.366
- https://dl.acm.org/doi/10.5555/557000 and https://dl.acm.org/doi/pdf/10.1145/1414004.1414016
- https://en.wikipedia.org/wiki/Brooks%27s_law and https://en.wikipedia.org/wiki/Hofstadter%27s_law
- https://www.pmi.org/learning/library/risk-analysis-decisions-uncertain-times-6686
- https://whichframework.org/frameworks/work-breakdown-structure.html
- https://projectmanagementacademy.net/resources/blog/a-three-point-estimating-technique-pert/

Validation:
- https://regulations.worldcubeassociation.org/wca-regulations-and-guidelines.merged.pdf
- https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/
- https://files.eric.ed.gov/fulltext/EJ1061142.pdf
- https://www-users.york.ac.uk/~mb55/meas/sizemeth.htm
- https://www.itc.gov.hk/en/quality/scl/doc/scl/stopwatchescalibration.pdf
- https://tf.nist.gov/general/pdf/1930.pdf
- https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/file-system-considerations.html
- https://docs.espressif.com/projects/esp-faq/en/latest/software-framework/storage/nvs.html

Speedcubing prior builds:
- https://ojdip.net/2020/11/esp32-cube-timer/
- https://github.com/tibordp/cube-timer
- https://github.com/liusonwood/StackmatLink
- https://gist.github.com/afedotov/52057533a8b27a0277598160c384ae71

BLE:
- https://hubble.com/community/guides/why-your-first-ble-project-won-t-connect-and-how-to-fix-it/
- https://punchthrough.com/ble-connection-parameters-guide/
- https://github.com/WebBluetoothCG/web-bluetooth/issues/383
- https://www.espruino.com/Troubleshooting+BLE

Cost, logistics, demo:
- https://salework.net/thoi-gian-giao-hang-shopee/
- https://hoclaptrinhrobot.com/kien-thuc/10-du-an-robot-esp32-cho-nguoi-moi
- https://lkcg.vn/combo-bo-kit-hoc-tap-nhung-iot-esp-32s
- https://roboticsknowledgebase.com/wiki/robotics-project-guide/demo-day/
- https://openbooks.library.unt.edu/seworkbook/chapter/chapter-11-demos
- https://www.techedubyte.com/hardware-project-failed-demo-day-lessons-stem-students/

Method note: the instruction file researcher.md under AppData was not read, because the user's global CLAUDE.md forbids reading AppData. Research followed general practice: multi-source search, direct fetch of primary documents where possible, evidence tags above.
