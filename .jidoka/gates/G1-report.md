# G1 Report specification (chapters 3 to 5)
# Written 08:11 +07 from the checkpoint brief and the user's instructions; drafts already existed, so every criterion is checked against fresh evidence, never against the author's memory.
- C1 [edge] Every simulation and ablation number quoted in chap3, chap4, chap5 equals `code/sim/out/results.json` and `ablations.json` from a fresh run | re-run both scripts, grep each number in the tex | script output plus grep hits
- C2 `main.tex` compiles with 0 errors, 0 undefined references, no overfull hbox above 10 pt | `bash scripts/compile.sh` and log grep | compile log
- C3 Each of the 8 checkpoint items maps to a named section of the report | build the item-to-section table from `main.toc` | table with section numbers
- C4 Every design decision shows candidates, budget, simplicity and an ablation, and states the chosen optimum (user's elasticity rule) | inspect decision and elasticity tables in chap3 plus `tab:sim-ablation` | table labels and row count
- C5 No team-decision violation and no em dash in chapters 3 to 5 | grep for pin nuôi, cloud, đám mây, WCA hợp lệ, U+2014 | grep output with zero offending hits
