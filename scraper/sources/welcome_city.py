# -*- coding: utf-8 -*-
"""横浜市観光情報サイト https://www.welcome.city.yokohama.jp/eventinfo/"""
import re

from bs4 import BeautifulSoup

from common import fetch, parse_dates, make_event, classify, WELCOME_AREA, detect_area, detect_reservation_tag

BASE = "https://www.welcome.city.yokohama.jp"
MAX_PAGES = 20

# 「詳細」欄は本体の説明に続けて関連ワークショップ等の案内が入ることがあり、
# そこの「事前申込」を本体の予約要否と誤認しないよう、これらの見出し以降は捨てる
_RELATED_CUT_RE = re.compile(r"関連イベント|同時開催|あわせて|おすすめ")


def _detect_reservation(dsoup):
    """イベント情報テーブル(div.event-information-table)から予約要否を判定。
    ページ全体はサイドバー等の変動コンテンツで誤検出するため使わない。"""
    table = dsoup.select_one("div.event-information-table")
    if not table:
        return None
    parts = []
    has_form_link = False
    for tr in table.find_all("tr"):
        th, td = tr.find("th"), tr.find("td")
        if th is None or td is None:
            continue
        label = th.get_text(strip=True)
        val = td.get_text(" ", strip=True)
        if label == "詳細":
            m = _RELATED_CUT_RE.search(val)
            if m:
                val = val[:m.start()]
        if label == "URL":
            # リンクボタンの文言(「参加申込フォーム」等)は予約必要の強いシグナル
            has_form_link = any("申込" in a.get_text() or "予約" in a.get_text()
                                for a in td.find_all("a"))
            continue
        if label in ("お問合せ", "電話番号", "受付時間", "エリア"):
            continue
        parts.append(val)
    tag = detect_reservation_tag(" ".join(parts))
    if tag:
        return tag
    return "reservation_required" if has_form_link else None


def scrape():
    events = []
    for page in range(1, MAX_PAGES + 1):
        url = f"{BASE}/eventinfo/" + (f"?page={page}" if page > 1 else "")
        html = fetch(url)
        if not html:
            break
        soup = BeautifulSoup(html, "html.parser")
        boxes = soup.select("a.event-list-box")
        if not boxes:
            break
        for box in boxes:
            href = box.get("href", "")
            link = BASE + href if href.startswith("/") else href
            title_el = box.select_one(".event-list-box-title")
            title = title_el.get_text(strip=True) if title_el else ""
            badges = [s.get_text(strip=True) for s in box.select(".event-tag-badge span")]
            area_name = date_text = addr = ""
            for li in box.select(".event-list-disc li"):
                label_el = li.select_one(".event-disc-category")
                if not label_el:
                    continue
                label = label_el.get_text(strip=True)
                value = li.get_text(" ", strip=True).replace(label, "", 1).strip()
                if label == "エリア":
                    area_name = value
                elif label == "開催日程":
                    date_text = value
                elif label == "住所":
                    addr = value
            area = WELCOME_AREA.get(area_name)
            if area is None:
                area = detect_area(area_name, addr, title)
            if area is None:
                continue  # 対象エリア外(新横浜等)は捨てる
            start, end = parse_dates(date_text)
            # 詳細ページを取得: 日程が「…」で切れた場合の補完と、予約要否の判定に使う
            dhtml = fetch(link)
            res_tag = None
            if dhtml:
                dsoup = BeautifulSoup(dhtml, "html.parser")
                res_tag = _detect_reservation(dsoup)
                if date_text.endswith("…") and end is None:
                    dtext = dsoup.get_text(" ", strip=True)
                    i = dtext.find("開催日程")
                    if i >= 0:
                        s2, e2 = parse_dates(dtext[i:i + 120])
                        if s2:
                            start, end = s2, e2
            tags = []
            if res_tag:
                tags.append(res_tag)
            if any("屋外" in b for b in badges):
                tags.append("outdoor")
            if any("無料" in b for b in badges):
                tags.append("free")
            cat_hint = " ".join(badges)
            category = None
            if "グルメ" in cat_hint:
                category = "food"
            elif "祭" in cat_hint:
                category = "festival"
            events.append(make_event(
                "welcome_city", title, link, start, end,
                venue=addr, area=area,
                category=category or classify(title, addr, cat_hint),
                tags=tags,
            ))
    return events
