# writing/

LaTeX documents in Vietnamese, sharing one `preamble.tex`:

- `main.tex`: the full report (`titlepage.tex`, `chapters/chapN.tex`). `chap1` (project intro, requirements, glossary) and `chap2` (system analysis) are written; chapters 3 to 5 are commented out.
- `bai5.tex`: the Bài 5 homework (submitted), a standalone PDF with `titlepage-bai5.tex` covering sections 2.1 to 2.3. It defines `\skipcomm` so `chap2.tex` leaves out section 2.4. Treat it as frozen.
- `bai6.tex`: the Bài 6 homework, only sections 2.1 and 2.4. It defines `\skipcontext` and `\skipdevice`, and `titlepage-bai.tex` takes `\hwnumber` and `\hwtitle`. Use `titlepage-bai.tex` for later homework.
- Chapter 2 alone is the unit submitted for homework, so keep it free of references to other chapters.
- `chapters/chap2.tex` only wraps the section files in `chapters/chap2/`: `general` (2.1), `context` (2.2), `device` (2.3), `comm` (2.4; it sets the section counter to 3 so it keeps its number when homework builds drop 2.2 and 2.3). Each section file must stand alone: do not `\ref` into another section file, since homework builds drop sections. Add later sections as new files and list them in `chap2.tex`.

## Commands

Run from this folder:

```bash
bash scripts/compile.sh            # main.tex -> main.pdf; intermediates in build/, junk moved to .trash/
bash scripts/compile.sh bai5.tex   # standalone Bài 5 -> bai5.pdf
bash scripts/compile.sh bai6.tex   # standalone Bài 6 -> bai6.pdf
bash scripts/compile.sh --clean    # only sweep junk from source folders
```

`python -I ../scripts/build_report_pdf.py` renders `../reports/Haitay-prior-art.md` to the PDF beside it; the HTML and figure SVGs land in `renders/`.

## Conventions

- Match `chapters/chap1.tex`: `booktabs` tables with a `haitayblue` header row and `haitayblue!8` stripes, `tcolorbox` callouts, each section opening with a short lead paragraph.
- The Read tool rejects every PDF here as "password-protected", including `main.pdf` right after compiling. To inspect pages, render them: `pdftoppm -r 70 -f N -l M -png main.pdf renders/chk`, then read the PNGs and move them to `.trash/`.
- Run `viet-ai-humanizer` (`../../.claude/skills/`) over new Vietnamese prose, and keep sentences natural to Vietnamese word order rather than translated English. Use third-party images only under free licenses (CC0, public domain, CC BY) and credit the author in the caption.
- A new chapter takes effect only when its `\include` in `main.tex` is uncommented; add any package it needs to `preamble.tex`.
- Requirements text comes from `chap1`. The root `AGENTS.md` "Team decisions" override the prior-art report where they differ.
- Python snippets run through the shell lose doubled backslashes; write LaTeX strings in Python as raw strings (`r"\begin{document}"`).
