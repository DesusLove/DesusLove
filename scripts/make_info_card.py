"""Generate info-card.svg — a neofetch-style info panel.

Edit the ROWS list and HOST below with your real data.
Keep height matching the portrait (adjust H if it overflows).
"""

# --- CONFIG: edit these ---
HOST = "kunta@devsecops"

ROWS = [
    ("", ""),
    ("OS", "Arch Linux · AWS Linux · macOS"),
    ("Shell", "zsh · bash"),
    ("Uptime", "DevSecOps since 2021"),
    ("", ""),
    ("Stack", "Python · Java · TS · Go · C++ · Kotlin"),
    ("Cloud", "AWS · Kubernetes · Docker · Terraform"),
    ("Security", "SAST/DAST · Zero-Trust · Threat Modeling"),
    ("CI/CD", "GitHub Actions · GitLab CI · ArgoCD"),
    ("", ""),
    ("Cert", "AWS Certified · CCNA · CyberOps"),
    ("Highlight", "94% vuln escape rate reduction"),
    ("Highlight", "Sub-6min MTTD · 500K+ MAU infra"),
    ("Highlight", "Zero credential incidents · 2+ yrs"),
    ("", ""),
    ("Open to", "Staff DevSecOps · Security Arch"),
    ("", "AI Threat Intel · Cloud Security"),
]

# --- rendering ---
W = 490
H = 370
MARGIN = 24
COLOR = "#c9d1d9"
ACCENT = "#a78bfa"
DIM = "#8b949e"
BG = "#0d1117"
BORDER = "#21262d"
FONT = "JetBrains Mono, Courier, monospace"
FS_TITLE = 14
FS_LABEL = 11
FS_VALUE = 11
LINE_H = 18


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"')
    lines.append(f'     viewBox="0 0 {W} {H}" style="background:{BG}">')
    lines.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="8" fill="{BG}" '
                 f'stroke="{BORDER}" stroke-width="1"/>')

    y = MARGIN

    lines.append(f'<text x="{MARGIN}" y="{y}" font-family="{FONT}" font-size="{FS_TITLE}" '
                 f'font-weight="700" fill="{ACCENT}">{esc(HOST)}</text>')
    y += 22

    lines.append(f'<text x="{MARGIN}" y="{y}" font-family="{FONT}" font-size="{FS_LABEL}" '
                 f'fill="{DIM}">{"─" * 28}</text>')
    y += LINE_H

    for label, value in ROWS:
        if not label and not value:
            y += LINE_H // 2
            continue

        if label in ("",):
            lines.append(f'<text x="{MARGIN}" y="{y}" font-family="{FONT}" font-size="{FS_LABEL}" '
                         f'fill="{DIM}">{"·" * 28}</text>')
            y += LINE_H
            continue

        lx = MARGIN
        lw = 80
        vx = lx + lw

        lines.append(f'<text x="{lx}" y="{y}" font-family="{FONT}" font-size="{FS_LABEL}" '
                     f'fill="{ACCENT}" font-weight="600">{esc(label)}</text>')
        lines.append(f'<text x="{vx}" y="{y}" font-family="{FONT}" font-size="{FS_VALUE}" '
                     f'fill="{COLOR}">{esc(value)}</text>')
        y += LINE_H

    lines.append("</svg>")

    with open("info-card.svg", "w") as f:
        f.write("\n".join(lines))

    used = y + MARGIN
    print(f"info-card.svg — {W}x{H} (content used {used}px)")
    if used > H:
        print(f"  ! Content overflows by {used - H}px — bump H in the script")
    else:
        print(f"  Looks good with {H - used}px spare")


if __name__ == "__main__":
    main()
