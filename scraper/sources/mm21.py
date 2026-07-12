# -*- coding: utf-8 -*-
"""みなとみらい21公式 https://minatomirai21.com/eventcampaign
一覧には記事掲載日しかないため、詳細ページのdt/dd(開催日・施設名・場所)を取得する。
取得数を抑えるため最新2ページ(約40件)のみ対象。"""
from bs4 import BeautifulSoup

from common import fetch, parse_dates, make_event, detect_area

LIST_PAGES = 2
MAX_DETAILS = 40


def scrape():
    events = []
    fetched = 0
    seen = set()
    for page in range(1, LIST_PAGES + 1):
        url = "https://minatomirai21.com/eventcampaign" + (f"?pg={page}" if page > 1 else "")
        html = fetch(url)
        if not html:
            break
        soup = BeautifulSoup(html, "html.parser")
        for li in soup.select("li.art-music"):
            a = li.find("a", href=True)
            title_el = li.select_one("h3.tit")
            if not a or not title_el:
                continue
            link = a["href"]
            if link in seen:
                continue
            seen.add(link)
            title = title_el.get_text(strip=True)
            fac_el = li.select_one(".fac-name")
            facility = fac_el.get_text(strip=True) if fac_el else ""
            if fetched >= MAX_DETAILS:
                continue
            fetched += 1
            date_text = place = event_url = detail_text = ""
            dhtml = fetch(link)
            if dhtml:
                dsoup = BeautifulSoup(dhtml, "html.parser")
                detail_text = dsoup.get_text(" ", strip=True)
                for dt in dsoup.find_all("dt"):
                    dd = dt.find_next_sibling("dd")
                    if not dd:
                        continue
                    label = dt.get_text(strip=True)
                    val = dd.get_text(" ", strip=True)
                    if "開催日" in label or "期間" in label:
                        date_text = val
                    elif "場所" in label:
                        place = val
                    elif "施設名" in label and not facility:
                        facility = val
                    elif "URL" in label:
                        event_url = val
            start, end = parse_dates(date_text)
            if not start:
                continue  # 開催日不明(常設・キャンペーン等)は載せない
            venue = facility or place
            events.append(make_event(
                "mm21", title, event_url or link, start, end,
                venue=venue,
                area=detect_area(venue, place, title) or "mm",
                detect_text=detail_text,
            ))
    return events
