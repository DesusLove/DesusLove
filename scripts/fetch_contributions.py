"""Scrape GitHub contribution data from a user's profile (no auth required).

Output: data/contributions.json
Env:    GH_PROFILE_USER  (default: DesusLove)
"""

import json
import os
import re

import requests
from bs4 import BeautifulSoup

USER = os.environ.get("GH_PROFILE_USER", "DesusLove")
URL = f"https://github.com/users/{USER}/contributions"
OUT = "data/contributions.json"

LEVEL_THRESHOLDS = {0: 0, 1: 1, 2: 4, 3: 8, 4: 12}


def main():
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    contributions = {}
    cells = soup.find_all("td", class_="ContributionCalendar-day")
    for cell in cells:
        date = cell.get("data-date", "")
        if not date:
            continue
        level = int(cell.get("data-level", "0"))
        contributions[date] = level

    h2 = soup.find("h2", id="js-contribution-activity-description")
    page_total = 0
    if h2:
        m = re.search(r"(\d+)", h2.get_text())
        if m:
            page_total = int(m.group(1))

    raw_total = sum(LEVEL_THRESHOLDS[v] for v in contributions.values() if v in LEVEL_THRESHOLDS)

    if raw_total > 0 and page_total > 0:
        scale = page_total / raw_total
        scaled = {}
        for date, lv in contributions.items():
            base = LEVEL_THRESHOLDS.get(lv, 0)
            scaled[date] = max(0, round(base * scale))
    else:
        scaled = {d: LEVEL_THRESHOLDS.get(v, 0) for d, v in contributions.items()}

    streak = {"total": 0, "longest": 0, "current": 0}
    if scaled:
        sorted_dates = sorted(scaled.keys())
        total = sum(scaled.values())
        longest = 0
        current_run = 0

        for d in sorted_dates:
            if scaled[d] > 0:
                current_run += 1
                longest = max(longest, current_run)
            else:
                current_run = 0

        current = 0
        for d in reversed(sorted_dates):
            if scaled[d] > 0:
                current += 1
            else:
                break

        streak = {"total": total, "longest": longest, "current": current}

    payload = {
        "user": USER,
        "contributions": scaled,
        "streak": streak,
        "levels": contributions,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)

    days = len(scaled)
    print(f"Fetched {days} days of contributions for {USER}")
    print(f"  Total: {streak['total']} | Longest streak: {streak['longest']} | Current: {streak['current']}")


if __name__ == "__main__":
    main()
