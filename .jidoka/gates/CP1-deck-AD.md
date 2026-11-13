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
