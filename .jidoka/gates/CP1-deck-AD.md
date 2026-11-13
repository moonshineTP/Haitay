# CP1-deck-AD: Checkpoint 1 deck, analysis-and-design and feasibility

- Owner: chap3 session (gatekeeper by user request, 13-11-2026). Producer: beamer-cp1 session.
- Scope: `presentation/checkpoint1.tex` for the Checkpoint 1 talk at 09:30 +07 only. Self-contained: no criterion depends on another gate file. Expires after the talk; later checkpoints write their own gate and inherit nothing from this one.
- Sources read: AGENTS.md team decisions as of 09:09 +07 (FRAM dropped, internal-flash ring 12 KB), writing/chapters/chap3.tex as of 09:09 +07, code/sim.
- History: v1 locked 09:12 +07 in tmp/gate-deck-AD.md with FRAM totals (1.372.000). Premise changed at 09:09 +07 (FRAM dropped), so v1 G5 was stale, not a deck drift. v2 below amends G5 to the new ruling and, on the user's request ("self-encapsulated and properly narrowed"), narrows G7 so the deck carries only Checkpoint 1 items.

| # | Criterion | Pass condition |
|---|---|---|
| G1 | Use cases | <= 5, verb+object, one user demand each, equal to chap3 UC1-UC4; actors Người chơi, Người chơi kế tiếp; UC4 include UC3 |
| G2 | Architecture | 4 layers with course names, protocol on every hop Device, Gateway, Server, App |
| G3 | Technology choices | protocol, DB, backend, web each with a reason and a rejected alternative, consistent with chap3 |
| G4 | Requirements | >= 5 functional requirements visible (mapped to the use cases) and >= 4 measurable NFR equal to chap3 |
| G5 | Devices and cost | BOM equals chap3: total 1.066.000, one unit 650.000; benefit stated |
| G6 | Data flow evidence | end-to-end flow with honest simulation vs hardware status; no WCA-legality, cloud or multi-device claim |
| G7 | Narrow scope | only the 8 Checkpoint 1 items; no slide depends on the report to be understood; elasticity and ablation detail stay in the report |
| G8 [edge] | Weakest feasibility link | every feasibility number traces to a source that models the current design (flash ring), or is labelled as not yet modelled |

## Verdict v2, 09:13 +07 (deck as of 09:09 +07)

| # | Result | Evidence |
|---|---|---|
| G1 | FAIL, fix in progress | slide 3 still shows 12 use cases; beamer-cp1 is redrawing it |
| G2 | PASS | frame "4. Kiến trúc bốn lớp": four layers, BLE GATT, HTTP/REST 127.0.0.1, SQL, HTTP/REST + SSE |
| G3 | PASS | frame "6. Lựa chọn công nghệ": seven rows, each with an alternative |
| G4 | FAIL | NFR N1-N12 match chap3; no slide lists >= 5 functional requirements once use cases drop to 4 |
| G5 | PASS | 1.066.000 and 650.000 in deck and chap3; sum re-checked |
| G6 | PASS | frame "7. Tiến độ" separates simulated from missing hardware |
| G7 | PASS | no cross-reference to the report; no elasticity slide |
| G8 | FAIL | S3 (100 power cuts, 0 lost) and S5 come from the FRAM byte-write model (code/sim/haitay/device.py: 8 KB, 512 slots); flash sector erase and page-program tears are not modelled |

## Verdict v3, 09:16 +07 (deck tex and PDF as of 09:13 +07)

| # | Result | Evidence |
|---|---|---|
| G1 | PASS on content, FAIL on drawing | frame "3. Yêu cầu chức năng: 4 use case": UC1-UC4 verb+object, two actors, UC4 include UC3; render at 110 dpi shows the ellipses' left ends outside the system boundary; fix sent to beamer-cp1 |
| G2 | PASS | unchanged frame |
| G3 | PASS | unchanged frame |
| G4 | PASS | slide 3 maps 10 chap1 functions to UC1-UC4 (4+2+3+1), Smart Cube marked optional; N1-N12 unchanged |
| G5 | PASS | pdftotext: 1.066.000 and 650.000 present, 0 hits for FRAM or FM24 |
| G6 | PASS | unchanged frame |
| G7 | PASS | no report cross-reference, no elasticity slide |
| G8 | PASS | pdftotext shows footnote "S3, S5 dùng mô hình ghi từng byte; xóa sector flash chưa được mô phỏng" |

## Verdict v4, 09:29 +07 (deck tex and PDF as of 09:16 +07): CLOSED, 8/8 PASS

G1 drawing fixed: boundary (1.5,1.0) to (12.6,-6.65); render of PDF page 4 at 110 dpi shows all four ellipses inside the box and «include» inside. Largest overfull vbox 2.9 pt (< 5 pt). G2 to G8 unchanged since v3.

Debt carried out of this gate (owner: orchestrator, not the deck): code/sim still models FRAM, so the report's flash power-loss claims have no simulation evidence.
