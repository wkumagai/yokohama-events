# -*- coding: utf-8 -*-
"""共通ユーティリティ: 取得(待機つき)・日付解析・カテゴリ/エリア判定"""
import hashlib
import re
import time
import unicodedata
from datetime import date, timedelta

import requests

UA = "yokohama-events-local/0.1 (personal local use; polite crawler)"
_session = requests.Session()
_session.headers.update({"User-Agent": UA})
_last_fetch = [0.0]
FETCH_INTERVAL = 2.0  # 秒


def fetch(url, timeout=20, retries=2):
    """2秒以上の間隔を空けて取得。接続エラーは待機を伸ばして再試行。失敗時はNone"""
    for attempt in range(retries + 1):
        wait = FETCH_INTERVAL - (time.time() - _last_fetch[0])
        if wait > 0:
            time.sleep(wait)
        try:
            r = _session.get(url, timeout=timeout)
            _last_fetch[0] = time.time()
            if r.status_code == 200:
                r.encoding = r.apparent_encoding if not r.encoding or r.encoding.lower() == "iso-8859-1" else r.encoding
                return r.text
            if r.status_code in (429, 500, 502, 503) and attempt < retries:
                time.sleep(5 * (attempt + 1))
                continue
            print(f"  ! HTTP {r.status_code}: {url}")
            return None
        except requests.exceptions.SSLError:
            # macOS標準PythonのLibreSSLが古くTLS交渉に失敗するサイトがある → curlで代替
            _last_fetch[0] = time.time()
            return _fetch_curl(url, timeout)
        except Exception as e:
            _last_fetch[0] = time.time()
            if attempt < retries:
                time.sleep(5 * (attempt + 1))  # 接続リセット等は間隔を空けて再試行
                continue
            print(f"  ! fetch error: {url}: {e}")
    return None


def _fetch_curl(url, timeout=20):
    import subprocess
    try:
        r = subprocess.run(
            ["curl", "-sL", "--max-time", str(timeout), "-A", UA, url],
            capture_output=True, timeout=timeout + 5,
        )
        if r.returncode == 0 and r.stdout:
            return r.stdout.decode("utf-8", errors="replace")
        print(f"  ! curl fallback failed ({r.returncode}): {url}")
    except Exception as e:
        print(f"  ! curl fallback error: {url}: {e}")
    return None


# ---------- 日付 ----------

TODAY = date.today()
_DATE_FULL = re.compile(r"(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日")
_DATE_MD = re.compile(r"(\d{1,2})\s*月\s*(\d{1,2})\s*日")
_DATE_ISO = re.compile(r"(20\d{2})-(\d{2})-(\d{2})")


def _guess_year(month, day):
    """年なし日付の年推定: 60日以上過去になるなら翌年"""
    try:
        d = date(TODAY.year, month, day)
    except ValueError:
        return None
    if (TODAY - d).days > 60:
        try:
            return date(TODAY.year + 1, month, day)
        except ValueError:
            return None
    return d


def parse_dates(text):
    """テキスト中の日付(最大2つ)を(start,end)のISO文字列で返す。endはNone可"""
    if not text:
        return None, None
    text = unicodedata.normalize("NFKC", text)
    found = []
    iso = _DATE_ISO.findall(text)
    for y, m, d in iso:
        try:
            found.append(date(int(y), int(m), int(d)))
        except ValueError:
            pass
    if not found:
        year = None
        pos = 0
        for m in _DATE_FULL.finditer(text):
            year = int(m.group(1))
            try:
                found.append(date(year, int(m.group(2)), int(m.group(3))))
            except ValueError:
                pass
            pos = m.end()
        # 年なし(または後半だけ年なし)の 月日 を拾う
        for m in _DATE_MD.finditer(text[pos:] if found else text):
            mo, dy = int(m.group(1)), int(m.group(2))
            if year:
                try:
                    d = date(year, mo, dy)
                    if found and d < found[-1]:
                        d = date(year + 1, mo, dy)
                    found.append(d)
                except ValueError:
                    pass
            else:
                d = _guess_year(mo, dy)
                if d:
                    found.append(d)
    if not found:
        return None, None
    start = min(found[0:1])  # 最初に出た日付を開始日とする
    end = found[1] if len(found) > 1 and found[1] >= found[0] else None
    return start.isoformat(), end.isoformat() if end else None


# ---------- エリア ----------

AREA_RULES = [
    ("bashamichi", ["馬車道", "北仲", "BankART", "万国橋"]),
    ("sakuragicho", ["桜木町", "野毛", "紅葉ケ丘", "紅葉坂", "にぎわい座", "掃部山", "日ノ出町", "伊勢山"]),
    ("yamashita", ["山下", "中華街", "元町", "山手", "港の見える丘", "マリンタワー", "氷川丸", "人形の家", "アメリカ山", "石川町"]),
    ("honmoku", ["三溪園", "三渓園", "本牧"]),
    ("yokohama_st", ["横浜駅", "ベイクォーター", "そごう", "高島屋", "ジョイナス", "ニュウマン", "アソビル", "ポルタ", "モアーズ", "ビブレ", "CIAL", "ルミネ", "平沼", "鶴屋町", "北幸", "南幸"]),
    ("kannai", ["関内", "日本大通り", "伊勢佐木", "横浜公園", "横浜スタジアム", "大さん橋", "大桟橋", "開港記念会館", "県庁", "海岸通", "太田町", "相生町", "住吉町", "常盤町", "尾上町", "真砂町", "港町", "本町", "弁天通", "南仲通"]),
    ("mm", ["みなとみらい", "新港", "赤レンガ", "臨港パーク", "汽車道", "運河パーク", "ハンマーヘッド", "パシフィコ", "クイーンズ", "ランドマーク", "マークイズ", "ワールドポーターズ", "象の鼻", "コスモワールド", "新高島", "高島", "Kアリーナ", "ぴあアリーナ", "カップヌードル", "日本丸", "女神橋", "グランモール", "MM", "ドックヤード"]),
]

AREA_LABELS = {
    "bashamichi": "馬車道",
    "sakuragicho": "桜木町・野毛",
    "kannai": "関内・日本大通り",
    "mm": "みなとみらい・新港",
    "yamashita": "山下公園・中華街・元町・山手",
    "honmoku": "三溪園・本牧",
    "yokohama_st": "横浜駅周辺",
    "other": "その他(中・西区等)",
}


def detect_area(*texts):
    """テキスト群からエリアidを推定。判定不能ならNone"""
    joined = " ".join(t for t in texts if t)
    for area_id, kws in AREA_RULES:
        for kw in kws:
            if kw in joined:
                return area_id
    return None


# welcome.city のエリア名 → area id
WELCOME_AREA = {
    "みなとみらい21": "mm",
    "関内・馬車道・伊勢佐木町": "kannai",
    "桜木町・野毛": "sakuragicho",
    "元町・山手・中華街・山下公園": "yamashita",
    "横浜駅周辺": "yokohama_st",
    "山手・本牧・根岸": "honmoku",
}


# ---------- カテゴリ ----------

CATEGORY_LABELS = {
    "music": "音楽・ライブ",
    "stage": "舞台・演劇・ダンス",
    "traditional": "伝統芸能",
    "art": "アート・展覧会",
    "museum": "歴史・学び・ミュージアム",
    "festival": "祭り・季節行事",
    "food": "グルメ・マルシェ",
    "night": "イルミ・花火・夜間",
    "family": "ファミリー・体験",
    "sports_other": "スポーツ・その他",
}

_KW = [
    ("night", ["イルミ", "花火", "ライトアップ", "ナイトフラワーズ", "キャンドル", "夜景", "ヨルノヨ", "光のショー"]),
    ("traditional", ["能楽", "能・狂言", "狂言", "落語", "寄席", "講談", "浪曲", "雅楽", "邦楽", "歌舞伎", "民謡", "神楽"]),
    ("festival", ["祭り", "まつり", "祭 ", "フェスタ", "盆踊り", "春節", "パレード", "大道芸", "縁日", "例大祭", "神輿", "サンバ", "ハロウィン"]),
    ("food", ["グルメ", "ビール", "ビア", "マルシェ", "物産展", "フード", "スイーツ", "パンの", "パン祭", "酒", "ワイン", "オクトーバーフェスト", "肉", "ラーメン", "カレー", "コーヒー", "美食"]),
    ("music", ["コンサート", "ライブ", "LIVE", "リサイタル", "オーケストラ", "ジャズ", "JAZZ", "音楽会", "演奏", "合唱", "吹奏楽", "オルガン", "ピアノ", "クラシック", "フェス "]),
    ("stage", ["演劇", "ミュージカル", "ダンス", "バレエ", "舞台", "朗読劇", "オペラ", "公演"]),
    ("art", ["展覧会", "美術", "アート", "絵画", "写真展", "作品展", "個展", "彫刻", "ギャラリー", "陶芸", "イラスト", "デザイン展", "版画"]),
    ("family", ["こども", "子ども", "子供", "親子", "キッズ", "ファミリー", "体験", "ワークショップ", "工作", "自由研究", "スタンプラリー", "夏休み"]),
    ("museum", ["展示", "博物館", "資料館", "講座", "講演", "セミナー", "歴史", "文学", "図書館", "企画展", "特別展", "学芸員", "サイエンス"]),
    ("sports_other", ["野球", "サッカー", "マラソン", "スポーツ", "大会", "ヨガ", "ラン", "ウォーキング", "フリーマーケット", "フリマ", "即売", "ポップアップ", "POP UP"]),
]


def classify(*texts, default="sports_other"):
    joined = " ".join(t for t in texts if t)
    for cat, kws in _KW:
        for kw in kws:
            if kw.lower() in joined.lower():
                return cat
    return default


def scrape_rss(source, feed_url, venue, area, category=None, limit=30):
    """WordPress等の標準RSS(/feed/)からイベントらしき記事を抽出する共通処理。
    pubDateは投稿日でしかないため、日付はtitle/descriptionから抽出する。"""
    import xml.etree.ElementTree as ET

    xml_text = fetch(feed_url)
    if not xml_text:
        return []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    events = []
    for item in root.iter("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        if title_el is None or link_el is None or not (title_el.text and link_el.text):
            continue
        desc_el = item.find("description") or item.find(
            "{http://purl.org/rss/1.0/modules/content/}encoded"
        )
        desc = re.sub(r"<[^>]+>", " ", desc_el.text) if desc_el is not None and desc_el.text else ""
        title = title_el.text.strip()
        start, end = parse_dates(title + " " + desc)
        if not start:
            continue
        events.append(make_event(
            source, title, link_el.text.strip(), start, end,
            venue=venue, area=area, category=category or classify(title, desc),
            detect_text=desc,
        ))
        if len(events) >= limit:
            break
    return events


# ---------- 予約要否 ----------
# 「定員」「先着」「申込」のような単独語はページの項目ラベルや関係ない文脈
# (「対象・定員」欄、出店者募集、メルマガ申込等)に頻出し誤検出が多いため、
# 予約行為を明示する強いパターンのみ拾う。

_NO_RESERVATION_RE = re.compile(
    r"予約不要|申込不要|申し込み不要|予約は不要|当日受付|当日参加|参加自由|自由参加"
    r"|入場自由|入退場自由|観覧自由|見学自由|申込みは不要"
)
# 予約優先=予約なしでも入れる。どちらとも言い切れないので判定なしにする
_NEUTRAL_RE = re.compile(r"予約優先|申込優先")
_RESERVATION_RE = re.compile(
    r"要予約|予約制|予約必須|事前予約|要申込|要申し込み|申込制|事前申込|事前の申し?込み"
    r"|申込方法|申し込み方法|申込期間|申込締切|申込先着|参加申込|申込フォーム"
    r"|要応募|応募方法|応募期間|抽選で|抽選により|要整理券|整理券が必要"
)


def detect_reservation_tag(*texts):
    """テキストから予約要否タグを推定。判定不能ならNone。
    否定表現(「予約不要」等)が一つでもあれば主催者の「そのまま来て良い」表明を優先する。"""
    joined = " ".join(t for t in texts if t)
    if not joined:
        return None
    if _NO_RESERVATION_RE.search(joined):
        return "no_reservation"
    if _NEUTRAL_RE.search(joined):
        return None
    if _RESERVATION_RE.search(joined):
        return "reservation_required"
    return None


def make_id(source, url, start):
    h = hashlib.sha1(f"{source}|{url}|{start}".encode()).hexdigest()[:12]
    return h


def make_event(source, title, url, start=None, end=None, venue=None, area=None,
               category=None, tags=None, time_note=None, detect_text=None):
    title = re.sub(r"\s+", " ", (title or "")).strip()
    tags = list(tags or [])
    if not ({"reservation_required", "no_reservation"} & set(tags)):
        res_tag = detect_reservation_tag(title, venue or "", time_note or "", detect_text or "")
        if res_tag:
            tags.append(res_tag)
    return {
        "id": make_id(source, url or title, start or ""),
        "title": title,
        "start_date": start,
        "end_date": end,
        "time": time_note,
        "venue": (venue or "").strip() or None,
        "area": area or "other",
        "category": category or classify(title, venue or ""),
        "tags": tags,
        "url": url,
        "source": source,
    }
