"""Render contrib-heatmap.svg from data/contributions.json.

Animated GitHub-style contribution grid with streak stats.
"""

import json
from datetime import datetime, timedelta

# --- tunables ---
CELL = 11
GAP = 2
COLS = 53
ROWS = 7
LEGEND_W = 80
LABEL_H = 20
MONTH_H = 16
STREAK_H = 40
PAD = 16
BG = "#0d1117"
EMPTY = "#161b22"
COLORS = ["#0e4429", "#006d32", "#26a641", "#39d353"]
COLOR = "#c9d1d9"
DIM = "#8b949e"
ACCENT = "#a78bfa"
FONT = "JetBrains Mono, Courier, monospace"
CELL_DUR = 0.004


def main():
    with open("data/contributions.json") as f:
        data = json.load(f)

    contribs = data.get("contributions", {})
    streak = data.get("streak", {"total": 0, "longest": 0, "current": 0})

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = today
    start = end - timedelta(weeks=52 * 1 + 8)
    start = start - timedelta(days=start.weekday())

    grid = {}
    d = start
    while d <= end:
        key = d.strftime("%Y-%m-%d")
        grid[key] = contribs.get(key, 0)
        d += timedelta(days=1)

    w = PAD * 2 + COLS * (CELL + GAP) + LEGEND_W
    h = PAD + MONTH_H + ROWS * (CELL + GAP) + STREAK_H + LABEL_H + PAD

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"')
    lines.append(f'     viewBox="0 0 {w} {h}" style="background:{BG}">')
    lines.append(f'<style>')
    lines.append(f'text {{ font:{11}px {FONT}; }}')
    lines.append(f'</style>')

    gx = PAD
    gy = PAD + MONTH_H

    idx = 0
    total_cells = 0
    for col in range(COLS):
        for row in range(ROWS):
            date = start + timedelta(weeks=col, days=row)
            key = date.strftime("%Y-%m-%d")
            count = grid.get(key, 0)

            if date > today:
                count = -1

            x = gx + col * (CELL + GAP)
            y = gy + row * (CELL + GAP)

            if count < 0:
                continue

            total_cells += 1
            if count == 0:
                fill = EMPTY
            elif count <= 3:
                fill = COLORS[0]
            elif count <= 6:
                fill = COLORS[1]
            elif count <= 9:
                fill = COLORS[2]
            else:
                fill = COLORS[3]

            delay = idx * CELL_DUR
            lines.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{fill}">'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{delay:.3f}s" dur="0.01s" fill="freeze"/>'
                f'</rect>'
            )
            idx += 1

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    last_month = -1
    for col in range(COLS):
        d = start + timedelta(weeks=col)
        if d.month != last_month:
            last_month = d.month
            x = gx + col * (CELL + GAP)
            lines.append(
                f'<text x="{x}" y="{MONTH_H}" fill="{DIM}">{months[d.month - 1]}</text>'
            )

    day_labels = ["Mon", "", "Wed", "", "Fri", "", ""]
    for row, label in enumerate(day_labels):
        if label:
            y = gy + row * (CELL + GAP) + CELL - 2
            lines.append(
                f'<text x="{gx - 14}" y="{y}" fill="{DIM}" text-anchor="end">{label}</text>'
            )

    lx = gx + COLS * (CELL + GAP) + 12
    ly = gy + ROWS * (CELL + GAP) - 8
    lines.append(f'<text x="{lx}" y="{ly - 12}" fill="{DIM}" font-size="10">Less</text>')
    levels = [EMPTY] + COLORS
    for i, c in enumerate(levels):
        x = lx + 32 + i * (CELL + 2)
        lines.append(
            f'<rect x="{x}" y="{ly - 10}" width="{CELL - 1}" height="{CELL - 1}" '
            f'rx="2" fill="{c}"/>'
        )
    lines.append(f'<text x="{lx + 32 + len(levels) * (CELL + 2)}" y="{ly - 12}" '
                 f'fill="{DIM}" font-size="10">More</text>')

    sy = gy + ROWS * (CELL + GAP) + 8
    stats = [
        f"{streak['total']} contributions in the last year",
        f"Longest streak: {streak['longest']} days",
        f"Current streak: {streak['current']} days",
    ]
    for i, s in enumerate(stats):
        lines.append(
            f'<text x="{gx}" y="{sy + i * 16}" fill="{COLOR}" font-size="11">{s}</text>'
        )

    lines.append("</svg>")

    with open("contrib-heatmap.svg", "w") as f:
        f.write("\n".join(lines))

    print(f"contrib-heatmap.svg — {total_cells} cells, {w}x{h}")


if __name__ == "__main__":
    main()
