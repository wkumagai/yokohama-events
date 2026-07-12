# -*- coding: utf-8 -*-
"""横浜赤レンガ倉庫 イベント広場等 https://www.yokohama-akarenga.jp/event/
li.l-card_item の data-event-date 属性(例 "2026-07-04～2026-07-05")が使える。"""
from bs4 import BeautifulSoup

from common import fetch, parse_dates, make_event, classify

BASE = "https://www.yokohama-akarenga.jp"


def scrape():
    html = fetch(f"{BASE}/event/")
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    events = []
    for li in soup.select("li.l-card_item"):
        a = li.find("a", href=True)
        title_el = li.select_one("h3")
        if not a or not title_el:
            continue
        title = title_el.get_text(strip=True)
        href = a["href"]
        link = BASE + href if href.startswith("/") else href
        start, end = parse_dates(li.get("data-event-date", ""))
        if not start:
            metas = [m.get_text(" ", strip=True) for m in li.select(".l-card_meta_value")]
            start, end = parse_dates(" ".join(metas))
        venue = None
        metas = li.select(".l-card_meta_value")
        if len(metas) > 1:
            venue = metas[1].get_text(strip=True)
        tags_text = " ".join(t.get_text(strip=True) for t in li.select(".l-card_tags a"))
        detail_text = ""
        dhtml = fetch(link)
        if dhtml:
            detail_text = BeautifulSoup(dhtml, "html.parser").get_text(" ", strip=True)
        events.append(make_event(
            "akarenga", title, link, start, end,
            venue=("横浜赤レンガ倉庫 " + venue) if venue else "横浜赤レンガ倉庫",
            area="mm",
            category=classify(title, tags_text),
            detect_text=detail_text,
        ))
    return events
