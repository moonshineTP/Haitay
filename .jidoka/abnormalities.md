# Abnormality register

Project: Haitay Checkpoint 1 (report spec ch3-5, Beamer slides, Wokwi PoC). Host: orchestrator session. Deadline 09:30 +07, 13-11-2026.

| ID | Signal | Detector | Class | Action |
|---|---|---|---|---|
| A1 | A number in report or slides differs from `code/sim/out/*.json` or the prior-art report | verify pass, grep diff | stop | freeze merge, fix the source of the number, re-run verify |
| A2 | `main.tex` or `checkpoint1.tex` fails to compile, has undefined references, or overfull hbox above 10 pt | compile log | stop | revert last edit, fix, recompile |
| A3 | A claim violates a team decision in `Haitay/AGENTS.md` (battery power, cloud, multi-device, WCA legality, user data on device) | grep, critic | stop | remove the claim, record in lessons |
| A4 | Two sessions write the same file, or a session edits outside its scope | `git status`, session reports | stop | freeze both, merge by hand, restate scopes |
| A5 | A sub-session reports PASS without fresh evidence (no output, no screenshot) | report review | warn | label UNVERIFIED, add debt, request evidence |
| A6 | Simulation scenario or ablation regresses (fewer than 17/17, different ablation counts) | re-run scripts | stop | bisect last code change |
| A7 | Clock passes 09:00 +07 with a gate still open | `date` | warn | cut scope to what has evidence, list the rest as debt |
| A8 | Outward action (Wokwi save/share, publish) beyond the user's approved scope | session report | stop | undo if possible, tell the user |
