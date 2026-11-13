"""SVG figures for the Haitay report (dataviz reference palette, light mode, static print)."""
from html import escape

INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURF = "#e1e0d9", "#c3c2b7", "#fcfcfb"
BLUE, ORANGE = "#2a78d6", "#eb6834"
FONT = "'Segoe UI', Arial, sans-serif"

# Inputs copied from the report tables (PERT totals, week-by-week table, BOM, WCA data).
HORIZONS = [("6 weeks", 91.5, 119.0, 120), ("8 weeks", 121.3, 157.7, 160), ("10 weeks", 152.5, 198.2, 200)]
CUM_E = [0.0, 13.8, 28.8, 44.2, 62.2, 80.2, 98.8, 116.3, 121.3]  # 'Cum. E' column of the week-by-week table
BOM_PARTS = [("Tier A", "minimum", 603), ("Tier B", "recommended", 1284), ("Tier C", "premium", 2485)]
TOOLING_K, CONTINGENCY = 210, 0.15
WCA_COMPETITIONS = {2018: 1154, 2019: 1330, 2020: 479, 2021: 305, 2022: 1096, 2023: 2144, 2024: 2723, 2025: 2712}
VN_ACCOUNTS = {2017: 1173, 2018: 671, 2019: 517, 2022: 891, 2023: 585, 2024: 635, 2025: 389, 2026: 397}


def _svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{escape(label)}" font-family="{FONT}" font-size="11">'
            f'<rect width="{w}" height="{h}" fill="{SURF}"/>{body}</svg>')


def _t(x, y, s, size=11, fill=INK2, anchor="start", weight="400"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{escape(s)}</text>')


def _bar(x, y, w, h, color, round_top=True):
    """Column with a 4px rounded data-end and a square baseline."""
    if h <= 0:
        return ""
    r = min(4, w / 2, h) if round_top else 0
    if r == 0:
        return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{color}"/>'
    return (f'<path d="M{x:.1f},{y + h:.1f} V{y + r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x + r:.1f},{y:.1f} '
            f'H{x + w - r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x + w:.1f},{y + r:.1f} V{y + h:.1f} Z" fill="{color}"/>')


def _dot(x, y, color):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}" stroke="{SURF}" stroke-width="2"/>'


def _yaxis(x0, x1, y_of, ticks, fmt=lambda v: f"{v:,.0f}"):
    out = []
    for v in ticks:
        y = y_of(v)
        out.append(f'<line x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{AXIS if v == 0 else GRID}" stroke-width="1"/>')
        out.append(_t(x0 - 8, y + 4, fmt(v), 10, MUTED, "end"))
    return "".join(out)


def _legend(items, x=8, y=14):
    out, cx = [], x
    for kind, color, label in items:
        if kind == "bar":
            out.append(f'<rect x="{cx}" y="{y - 9}" width="10" height="10" rx="2" fill="{color}"/>')
            off = 16
        else:
            out.append(f'<line x1="{cx}" x2="{cx + 16}" y1="{y - 4}" y2="{y - 4}" stroke="{color}" stroke-width="2" stroke-linecap="round"/>')
            off = 22
        out.append(_t(cx + off, y, label, 11, INK2))
        cx += off + len(label) * 5.9 + 18
    return "".join(out)


def effort_vs_capacity():
    w, h, x0, x1, yb, yt = 680, 320, 56, 660, 262, 52
    y = lambda v: yb - (yb - yt) * v / 200
    slot = (x1 - x0) / len(HORIZONS)
    body = _legend([("bar", BLUE, "Expected effort E"), ("bar", ORANGE, "Plan hours (E x 1.3)"),
                    ("line", INK2, "Capacity at 20 h per week")])
    body += _t(8, 40, "Team person-hours", 10, MUTED) + _yaxis(x0, x1, y, [0, 50, 100, 150, 200])
    for i, (name, e, plan, cap) in enumerate(HORIZONS):
        cx = x0 + slot * (i + 0.5)
        body += _bar(cx - 25, y(e), 24, yb - y(e), BLUE) + _bar(cx + 1, y(plan), 24, yb - y(plan), ORANGE)
        body += f'<line x1="{cx - 44:.1f}" x2="{cx + 44:.1f}" y1="{y(cap):.1f}" y2="{y(cap):.1f}" stroke="{INK2}" stroke-width="2"/>'
        body += _t(cx - 13, y(e) - 6, f"{e:.1f}", 11, INK, "middle") + _t(cx + 13, y(max(plan, cap)) - 7, f"{plan:.1f}", 11, INK, "middle")
        body += _t(cx, yb + 20, name, 12, INK, "middle", "600") + _t(cx, yb + 36, f"capacity {cap} h", 11, INK2, "middle")
    return _svg(w, h, body, "Expected effort, plan hours and capacity for 6, 8 and 10 week horizons")


def cumulative_baseline():
    w, h, x0, x1, yb, yt = 680, 320, 56, 560, 262, 52
    y = lambda v: yb - (yb - yt) * v / 180
    x = lambda wk: x0 + (x1 - x0) * wk / 8
    cum_e = CUM_E
    series = [("Capacity at 20 h per week", INK2, [20.0 * k for k in range(9)]),
              ("Plan hours (E x 1.3)", ORANGE, [1.3 * v for v in cum_e]),
              ("Expected effort E", BLUE, cum_e)]
    body = _legend([("line", BLUE, "Expected effort E"), ("line", ORANGE, "Plan hours (E x 1.3)"),
                    ("line", INK2, "Capacity at 20 h per week")])
    body += _t(8, 40, "Cumulative team person-hours", 10, MUTED) + _yaxis(x0, x1, y, [0, 40, 80, 120, 160])
    for wk in range(9):
        body += _t(x(wk), yb + 20, str(wk), 11, MUTED, "middle")
    body += _t((x0 + x1) / 2, yb + 38, "Week of the baseline 8-week plan", 11, INK2, "middle")
    body += f'<line x1="{x(4):.1f}" x2="{x(4):.1f}" y1="{yt}" y2="{yb}" stroke="{AXIS}" stroke-width="1"/>'
    for _, color, vals in series:
        pts = " ".join(f"{x(k):.1f},{y(v):.1f}" for k, v in enumerate(vals))
        body += f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'
    for _, color, vals in series:
        body += _dot(x(8), y(vals[8]), color)
    body += _dot(x(4), y(series[0][2][4]), INK2) + _dot(x(4), y(series[1][2][4]), ORANGE)
    body += _t(x(4) - 12, y(110), "Week 4 gate (M2)", 11, INK, "end", "600")
    body += _t(x(4) - 12, y(110) + 15, f"plan {series[1][2][4]:.1f} h meets capacity 80 h", 11, INK2, "end")
    lx = x(8) + 12
    body += _t(lx, y(160) - 6, "Capacity 160 h", 11, INK2) + _t(lx, y(158) + 14, f"Plan {series[1][2][8]:.0f} h", 11, INK2)
    body += _t(lx, y(cum_e[8]) + 4, f"Expected {cum_e[8]:.0f} h", 11, INK2)
    return _svg(w, h, body, "Cumulative expected effort, plan hours and capacity over the baseline 8-week plan")


def bom_tiers():
    w, h, x0, x1, yb, yt = 560, 330, 70, 540, 262, 52
    y = lambda v: yb - (yb - yt) * v / 3500
    slot = (x1 - x0) / len(BOM_PARTS)
    body = _legend([("bar", BLUE, "Parts"), ("bar", ORANGE, "Tooling plus 15% contingency")])
    body += _t(8, 40, "Thousand VND", 10, MUTED) + _yaxis(x0, x1, y, [0, 1000, 2000, 3000])
    for i, (tier, name, parts) in enumerate(BOM_PARTS):
        total = (parts + TOOLING_K) * (1 + CONTINGENCY)
        cx, bx = x0 + slot * (i + 0.5), x0 + slot * (i + 0.5) - 12
        body += _bar(bx, y(parts), 24, yb - y(parts), BLUE, round_top=False)
        body += _bar(bx, y(total), 24, (y(parts) - y(total)) - 2, ORANGE)
        body += _t(cx, y(total) - 20, f"{total:,.0f}k", 12, INK, "middle", "600")
        body += _t(cx, y(total) - 6, f"US${total * 1000 / 25500:,.0f}", 11, INK2, "middle")
        body += _t(cx, yb + 20, tier, 12, INK, "middle", "600") + _t(cx, yb + 36, name, 11, INK2, "middle")
        body += _t(cx, yb + 51, f"parts {parts:,}k", 11, INK2, "middle")
    return _svg(w, h, body, "All-in cost of three bill-of-materials tiers in thousand VND")


def _panel(x0, x1, data, years, ymax, ticks, title, subtitle, label_years, gap_years=()):
    yb, yt = 240, 76
    y = lambda v: yb - (yb - yt) * v / ymax
    slot = (x1 - x0) / len(years)
    bw = min(20, slot - 6)
    out = _t(x0 - 36, 18, title, 12, INK, "start", "600") + _t(x0 - 36, 33, subtitle, 10, MUTED)
    out += _yaxis(x0, x1, y, ticks)
    for i, yr in enumerate(years):
        cx = x0 + slot * (i + 0.5)
        out += _t(cx, yb + 16, f"{yr}*" if yr == 2026 and 2026 in data else str(yr), 10, MUTED, "middle")
        if yr in data:
            out += _bar(cx - bw / 2, y(data[yr]), bw, yb - y(data[yr]), BLUE)
            if yr in label_years:
                out += _t(cx, y(data[yr]) - 5, f"{data[yr]:,}", 10, INK, "middle")
    if gap_years:
        gx = x0 + slot * (years.index(gap_years[0]) + len(gap_years) / 2)
        out += _t(gx, yb - 8, "no data", 10, MUTED, "middle")
    return out


def market_scale():
    w, h = 680, 290
    body = _panel(78, 330, WCA_COMPETITIONS, list(range(2018, 2026)), 3000, [0, 1000, 2000, 3000],
                  "WCA competitions per year", "Worldwide, count", {2021, 2024, 2025})
    body += _panel(414, 668, VN_ACCOUNTS, list(range(2017, 2027)), 1200, [0, 400, 800, 1200],
                   "Vietnamese accounts registered", "Unique accounts per year", {2017, 2025, 2026}, (2020, 2021))
    return _svg(w, h, body, "Worldwide WCA competitions per year and unique Vietnamese registrants per year")


FIGURES = {
    "FIG1": ("Figure 1. Plan hours stay just under team capacity at every horizon", effort_vs_capacity, "100%",
             "Team person-hours at 10 h per person per week. E is the PERT expected value and plan = E x 1.3; "
             "all work-package inputs are [EST] from the table above."),
    "FIG2": ("Figure 2. In the baseline plan, cumulative hours meet capacity at the week 4 gate", cumulative_baseline, "100%",
             "Cumulative team hours from the week-by-week table. The week 4 gate is the decision point for switching to the 6-week list."),
    "FIG3": ("Figure 3. Tier B costs about 1.7 million VND all-in", bom_tiers, "82%",
             "Thousand VND. Tooling is a logic-analyzer clone (150k) plus fixture parts (60k); contingency is 15% of the subtotal. "
             "FX 25,500 VND per USD [UNVERIFIED]; lines marked E in the BOM are estimates."),
    "FIG4": ("Figure 4. Competitions worldwide rebounded while Vietnamese registrants declined", market_scale, "100%",
             "[OWN CALC] from the public WCA API; registrations, not attendance. Vietnam data starts in 2017, skips 2020-2021, "
             "and *2026 runs to 8 Oct."),
}
