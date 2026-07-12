# -*- coding: utf-8 -*-
"""横浜市役所アトリウム https://www.atrium.city.yokohama.lg.jp/event/ (馬車道駅直結)"""
from bs4 import BeautifulSoup

from common import fetch, parse_dates, make_event

URL = "https://www.atrium.city.yokohama.lg.jp/event/"


def scrape():
    html = fetch(URL)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    events = []
    for div in soup.select("div.event"):
        a = div.find("a", href=True)
        h3 = div.find("h3")
        if not a or not h3:
            continue
        title = h3.get_text(strip=True)
        date_el = div.select_one("p.date")
        place_el = div.select_one("p.place")
        start, end = parse_dates(date_el.get_text(strip=True) if date_el else "")
        place = place_el.get_text(strip=True) if place_el else ""
        detail_text = ""
        dhtml = fetch(a["href"])
        if dhtml:
            detail_text = BeautifulSoup(dhtml, "html.parser").get_text(" ", strip=True)
        events.append(make_event(
            "atrium", title, a["href"], start, end,
            venue=("横浜市役所アトリウム " + place).strip(),
            area="bashamichi",
            detect_text=detail_text,
        ))
    return events
