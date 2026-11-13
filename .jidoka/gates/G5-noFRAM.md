# G5 Deck without FRAM, parts buyable locally (locked 09:12 +07 after edits had started; recorded as debt)
- C1 [edge] The compiled deck PDF text contains no "FRAM" and no "FM24" | pdftotext checkpoint1.pdf, grep | match count 0
- C2 Every deck BOM line names a part with a Vietnamese shop price in the prior-art notes | match BOM rows to reports/prior-art-record/embedded_feasibility_and_bom.md | row-to-source table
- C3 Deck, report and ledger agree on the totals 1.066.000 and 650.000 | grep all three | grep output
- C4 Deck compiles with overfull under 5 pt; report compiles with 0 undefined references | logs | log lines
