"""Render reports/Haitay-prior-art.md to reports/Haitay-prior-art.pdf with inline figures.

Usage (any folder): python -I scripts/build_report_pdf.py
Pipeline: markdown -> HTML -> headless Edge. HTML and figure SVGs go to writing/renders/.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

sys.path.insert(0, str(Path(__file__).parent))
from report_charts import FIGURES  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
NAME = "Haitay-prior-art"
SRC, PDF = ROOT / "reports" / f"{NAME}.md", ROOT / "reports" / f"{NAME}.pdf"
RENDERS = ROOT / "writing" / "renders"
HTML = RENDERS / f"{NAME}.html"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Figure placeholder goes right before the heading it follows.
ANCHORS = {
    "### Week-by-week milestones": "FIG1",
    "### Resource cost": "FIG2",
    "### Validation plan": "FIG3",
    "### Recommended edits to chap1.tex": "FIG4",
}

CSS = """
@page { size: A4; margin: 16mm 15mm 18mm; @bottom-center { content: counter(page); font: 8pt 'Segoe UI', Arial, sans-serif; color: #898781; } }
html { color-scheme: light; }
body { font: 9.6pt/1.5 'Segoe UI', Arial, sans-serif; color: #0b0b0b; background: #fff; margin: 0; }
h1 { font-size: 24pt; margin: 0 0 4pt; letter-spacing: -0.01em; }
h2 { font-size: 15pt; margin: 22pt 0 6pt; padding-bottom: 3pt; border-bottom: 1.5px solid #2a78d6; break-after: avoid; }
h3 { font-size: 11.5pt; margin: 14pt 0 4pt; break-after: avoid; }
p { margin: 5pt 0; }
a { color: #1c5cab; text-decoration: none; overflow-wrap: break-word; }
code { font: 8.6pt Consolas, monospace; background: #f0efec; padding: 0 2pt; border-radius: 2px; }
table { width: 100%; border-collapse: collapse; margin: 7pt 0 9pt; font-size: 7.9pt; line-height: 1.35; }
thead { display: table-header-group; }
th { background: #f0efec; text-align: left; font-weight: 600; }
th, td { padding: 3pt 4pt; border-bottom: 1px solid #e1e0d9; vertical-align: top; overflow-wrap: break-word; }
tr { break-inside: avoid; }
ol, ul { margin: 4pt 0 4pt 16pt; padding: 0; }
figure { margin: 10pt 0 12pt; padding: 8pt 10pt 6pt; background: #fcfcfb; border: 1px solid #e1e0d9; border-radius: 6px; break-inside: avoid; }
figure svg { display: block; margin: 0 auto; height: auto; }
.fig-title { font-weight: 600; font-size: 9.6pt; margin-bottom: 4pt; }
figcaption { font-size: 7.9pt; color: #52514e; margin-top: 4pt; }
"""


def figure_html(key):
    title, build, width, caption = FIGURES[key]
    svg = build()
    (RENDERS / f"{key}.svg").write_text(svg, encoding="utf-8")
    return (f'<figure><div class="fig-title">{title}</div>'
            f'<div style="width:{width};margin:0 auto">{svg}</div><figcaption>{caption}</figcaption></figure>')


def main():
    RENDERS.mkdir(exist_ok=True)
    text = SRC.read_text(encoding="utf-8")
    for heading, key in ANCHORS.items():
        text = text.replace(f"\n{heading}\n", f"\n@@{key}@@\n\n{heading}\n", 1)
    body = markdown.markdown(text, extensions=["tables", "sane_lists"])
    body = re.sub(r"<p>@@(FIG\d)@@</p>", lambda m: figure_html(m.group(1)), body)
    HTML.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{NAME}</title>'
                    f"<style>{CSS}</style></head><body>{body}</body></html>", encoding="utf-8")
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run([EDGE, "--headless=new", "--disable-gpu", f"--user-data-dir={profile}",
                        "--no-pdf-header-footer", f"--print-to-pdf={PDF}", HTML.as_uri()],
                       check=True, timeout=120)
    print(PDF.name, PDF.stat().st_size)


if __name__ == "__main__":
    main()
