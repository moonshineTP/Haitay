# scripts/

Project-level helper scripts: flashing, seeding the demo dataset, measurement rigs, log analysis. Also holds the prior-art report build: `build_report_pdf.py` (markdown to PDF) and `report_charts.py` (its four figures). LaTeX compile tooling stays in `../writing/scripts/`.

- Each script states its usage in a header comment and writes outputs outside this folder.
- Generated measurement data and plots feed the report's validation chapter; record the run date and device firmware version beside them.
