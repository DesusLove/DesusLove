"""Convert source-prepped.png -> avi-ascii.svg — monochrome ASCII portrait."""

from math import ceil

import numpy as np
from PIL import Image

# --- tunables ---
CONTRAST = 1.4
GAMMA = 0.85
WHITE_FLOOR = 20
ROW_DUR = 0.08
STAGGER = 0.015
import os
STATIC = int(os.environ.get("STATIC", "0"))
COLS = 80
MAX_ROWS = 50
CHAR_SET = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "
COLOR = "#c9d1d9"
BG = "#0d1117"
FONT_SIZE = 6.5
FONT_FAMILY = "Courier, monospace"
CHAR_RATIO = 0.53


def main():
    img = Image.open("source-prepped.png").convert("L")
    w, h = img.size

    rows = min(int(h / w * COLS / CHAR_RATIO), MAX_ROWS)
    small = img.resize((COLS, rows), Image.LANCZOS)
    pixels = np.array(small, dtype=np.float32)

    pixels = np.clip((pixels - 128) * CONTRAST + 128, 0, 255)
    pixels = 255.0 * (pixels / 255.0) ** (1.0 / GAMMA)
    pixels = np.clip(pixels, 0, 255).astype(np.uint8)

    chars = []
    n_levels = len(CHAR_SET)
    for r in range(rows):
        line = []
        for c in range(COLS):
            val = pixels[r, c]
            if val >= 255 - WHITE_FLOOR:
                val = 255
            idx = int(val / 255 * (n_levels - 1))
            idx = max(0, min(idx, n_levels - 1))
            line.append(CHAR_SET[idx])
        chars.append("".join(line))

    rows_out = rows
    cols_out = COLS
    char_h = FONT_SIZE
    char_w = char_h * CHAR_RATIO
    svg_w = ceil(cols_out * char_w) + 20
    svg_h = ceil(rows_out * char_h * 1.2) + 20
    total = rows_out * cols_out

    lines_xml = []
    lines_xml.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}"')
    lines_xml.append(f'     viewBox="0 0 {svg_w} {svg_h}" style="background:{BG}">')
    lines_xml.append(f'<style>')
    lines_xml.append(f'@keyframes blink {{')
    lines_xml.append(f'  0%, 40% {{ opacity: 1; }}')
    lines_xml.append(f'  50%, 90% {{ opacity: 0; }}')
    lines_xml.append(f'  100% {{ opacity: 1; }}')
    lines_xml.append(f'}}')
    if not STATIC:
        lines_xml.append(f'.c {{ animation: blink 0.6s step-end infinite; }}')
    lines_xml.append(f'text {{ font:{FONT_SIZE}px {FONT_FAMILY}; fill:{COLOR}; }}')
    lines_xml.append(f'</style>')

    def esc(c):
        return c.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    idx = 0
    for r in range(rows_out):
        row_text = chars[r]
        x = 10
        y = 15 + r * char_h * 1.2
        for ci, ch in enumerate(row_text):
            delay = r * ROW_DUR + ci * STAGGER
            ch_esc = esc(ch)
            if STATIC:
                lines_xml.append(
                    f'<text x="{x:.1f}" y="{y:.1f}">{ch_esc}</text>'
                )
            else:
                lines_xml.append(
                    f'<text x="{x:.1f}" y="{y:.1f}" opacity="0">'
                    f'<animate attributeName="opacity" from="0" to="1" '
                    f'begin="{delay:.3f}s" dur="0.01s" fill="freeze"/>'
                    f'{ch_esc}</text>'
                )
            x += char_w
            idx += 1

    if not STATIC:
        cx = 10 + cols_out * char_w
        cy = 15
        lines_xml.append(
            f'<text x="{cx:.1f}" y="{cy:.1f}" class="c">|</text>'
        )

    lines_xml.append("</svg>")
    svg_content = "\n".join(lines_xml)

    with open("avi-ascii.svg", "w") as f:
        f.write(svg_content)

    print(f"avi-ascii.svg — {rows_out}x{cols_out} ({total} chars), STATIC={STATIC}")


if __name__ == "__main__":
    main()
