# -*- coding: utf-8 -*-
"""ヨコハマ・アートナビ https://artnavi.yokohama/area/{minatomirai,kannai}/"""
import re

from bs4 import BeautifulSoup

from common import fetch, parse_dates, make_event, detect_area, detect_reservation_tag

AREAS = {
    "minatomirai": "mm",      # みなとみらい・桜木町・新港
    "kannai": "kannai",       # 関内・馬車道・日本大通り
}
MAX_PAGES = 8

CAT_MAP = {
    "音楽": "music",
    "舞踏・演劇": "stage",
    "古典芸能": "traditional",
    "大衆芸能": "traditional",
    "美術": "art",
    "写真・映像": "art",
    "文芸": "museum",
}

_DATE_RE = re.compile(r"\d{1,2}\s*月\s*\d{1,2}\s*日")


def _reservation_tags(link):
    """詳細ページの構造化フィールド(dl.g-data_dl)から予約要否を判定する。
    ページ全文は「対象・定員」等のラベルやおすすめ欄で誤検出するため使わない。
    「申込期間」「申込方法」フィールドの存在が最も確実なシグナル。"""
    dhtml = fetch(link)
    if not dhtml:
        return None
    dsoup = BeautifulSoup(dhtml, "html.parser")
    dl = dsoup.select_one("dl.g-data_dl")
    if not dl:
        return None
    fields = {}
    for dt in dl.find_all("dt"):
        dd = dt.find_next_sibling("dd")
        if dd:
            fields[dt.get_text(strip=True)] = dd.get_text(" ", strip=True)
    for label, val in fields.items():
        if "申込" in label or "予約" in label:
            if re.search(r"不要|なし|無し", val[:20]):
                return ["no_reservation"]
            if val:
                return ["reservation_required"]
    tag = detect_reservation_tag(" ".join(fields.values()))
    return [tag] if tag else None


def scrape():
    events = []
    for slug, default_area in AREAS.items():
        for page in range(1, MAX_PAGES + 1):
            url = f"https://artnavi.yokohama/area/{slug}/" + (f"page/{page}/" if page > 1 else "")
            html = fetch(url)
            if not html:
                break
            soup = BeautifulSoup(html, "html.parser")
            items = soup.select("article.g-event_frame")
            if not items:
                break
            for it in items:
                a = it.select_one(".g-event_frame__title a")
                if not a:
                    continue
                title = a.get_text(strip=True)
                link = a.get("href")
                status_el = it.select_one(".g-icon--status")
                status = status_el.get_text(strip=True) if status_el else ""
                if status == "終了":
                    continue
                cat_el = it.select_one(".g-icon--category")
                genre = cat_el.get_text(strip=True) if cat_el else ""
                # dt/dd から日付らしい値と会場らしい値を拾う
                date_text = venue = ""
                for wrap in it.select(".g-event_frame__data_wrapper"):
                    dd = wrap.find("dd") or wrap
                    val = dd.get_text(" ", strip=True) if dd else wrap.get_text(" ", strip=True)
                    if not val:
                        continue
                    if _DATE_RE.search(val) and not date_text:
                        date_text = val
                    elif not venue:
                        venue = val
                if not date_text:  # dl全体からフォールバック
                    dl = it.select_one("dl.g-event_frame__data")
                    if dl:
                        whole = dl.get_text(" ", strip=True)
                        date_text = whole
                        if not venue:
                            venue = whole
                start, end = parse_dates(date_text)
                area = detect_area(venue, title) or default_area
                events.append(make_event(
                    "artnavi", title, link, start, end,
                    venue=venue if venue and not _DATE_RE.search(venue[:14]) else None,
                    area=area,
                    category=CAT_MAP.get(genre),
                    tags=_reservation_tags(link),
                ))
            if "次へ" not in html:
                break
    return events
