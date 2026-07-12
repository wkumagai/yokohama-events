# -*- coding: utf-8 -*-
"""横浜市 市民利用施設等イベント情報(中区・西区)
https://cgi.city.yokohama.lg.jp/common/event2/{naka,nishi}/event_list.html
GETパラメータ完備。地区センター講座等の区民向けイベント。"""
import re
from datetime import date

from bs4 import BeautifulSoup

from common import fetch, parse_dates, make_event, detect_area

WARDS = ["naka", "nishi"]
MAX_ITEMS = 400  # 区ごとの取得上限

# サイト自体が持つ「事前申込要否」区分(検索フォームの selectiongroups=1/3 に対応)。
# キーワード推定より確実なので、一致したらそのまま使う。
_SELECTION_TAG = {
    "事前申込・連絡が必要": "reservation_required",
    "申込先着順": "reservation_required",
    "先着順": "reservation_required",
    "当日参加自由": "no_reservation",
}


def scrape():
    events = []
    today = date.today().isoformat()
    for ward in WARDS:
        pos = 0
        while pos <= MAX_ITEMS:
            url = (f"https://cgi.city.yokohama.lg.jp/common/event2/{ward}/event_list.html"
                   f"?term_after={today}&num=20&pos={pos}")
            html = fetch(url)
            if not html:
                break
            soup = BeautifulSoup(html, "html.parser")
            links = soup.select("a.event")
            if not links:
                break
            pos += len(links)
            for a in links:
                li = a.find_parent("li")
                if not li:
                    continue
                title = a.get_text(strip=True)
                link = a.get("href")
                date_el = li.select_one("p.date")
                date_text = date_el.get_text(strip=True) if date_el else ""
                start, end = parse_dates(date_text)
                venue_el = li.select_one("p.name_sub")
                venue = ""
                if venue_el:
                    venue = re.sub(r"\(\d+\)$", "", venue_el.get_text(strip=True)).strip()
                tags = ["ward"]
                sel_el = li.select_one("div.released span.selection_method_group")
                sel_text = sel_el.get_text(strip=True) if sel_el else ""
                if sel_text in _SELECTION_TAG:
                    tags.append(_SELECTION_TAG[sel_text])
                events.append(make_event(
                    f"ward_{ward}", title, link, start, end,
                    venue=venue,
                    area=detect_area(venue, title) or "other",
                    tags=tags,
                ))
            if len(links) < 20:
                break
    return events
