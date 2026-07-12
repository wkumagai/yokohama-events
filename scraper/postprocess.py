# -*- coding: utf-8 -*-
"""収集後の後処理: 表記ゆれを吸収した重複統合"""
import re
import unicodedata

# 情報源の優先度(小さいほど優先=残す側)。施設直取り > 専門集約 > 汎用集約 > 区 > 恒例
SOURCE_PRIORITY = {
    "akarenga": 0, "atrium": 0,
    "artnavi": 1, "mm21": 2,
    "welcome_city": 3,
    "ward_naka": 4, "ward_nishi": 4,
    "annual": 5,
}

_NOISE = re.compile(
    r"(20\d{2}年|\d{1,2}月\d{1,2}日|\d{1,2}/\d{1,2}|[(（][月火水木金土日・祝]+[)）]"
    r"|開催中?|実施|開幕|[〜~～]|[!！?？]|【|】|「|」|『|』)"
)


def norm(title):
    """比較用正規化: 記号・日付・括弧書き等を除去して小文字化"""
    t = unicodedata.normalize("NFKC", title or "").lower()
    t = _NOISE.sub("", t)
    t = re.sub(r"[\s　\-–—・、。,.:：;／/()（）\[\]<>＜＞&＆'\"”“]+", "", t)
    return t


def bigrams(s):
    return {s[i:i + 2] for i in range(len(s) - 1)} if len(s) >= 2 else {s} if s else set()


def similar(a, b):
    """正規化タイトルの類似判定: 包含 or 文字バイグラムJaccard"""
    if not a or not b:
        return False
    if a == b:
        return True
    shorter, longer = (a, b) if len(a) <= len(b) else (b, a)
    if len(shorter) >= 8 and shorter in longer:
        return True
    ba, bb = bigrams(a), bigrams(b)
    if not ba or not bb:
        return False
    jac = len(ba & bb) / len(ba | bb)
    return jac >= 0.6


def _overlap(ev1, ev2):
    s1, e1 = ev1["start_date"], ev1.get("end_date") or ev1["start_date"]
    s2, e2 = ev2["start_date"], ev2.get("end_date") or ev2["start_date"]
    return s1 <= e2 and s2 <= e1


def fuzzy_dedupe(events):
    """開催期間が重なり、タイトルが類似するイベントを統合する。
    優先度の高い情報源を残し、欠けているフィールドは低優先側から補完。"""
    ordered = sorted(events, key=lambda ev: (SOURCE_PRIORITY.get(ev["source"], 9),
                                             -(len(ev.get("venue") or ""))))
    kept = []
    normed = []
    for ev in ordered:
        n = norm(ev["title"])
        dup_of = None
        for i, k in enumerate(kept):
            # 同一ソースでURLが違うものは別イベント(曜日違いの同名講座等)とみなす
            if ev["source"] == k["source"] and (ev.get("url") or "") != (k.get("url") or ""):
                continue
            if _overlap(ev, k) and similar(n, normed[i]):
                dup_of = k
                break
        if dup_of is not None:
            # 補完: 残す側に無い情報を吸収
            if not dup_of.get("venue") and ev.get("venue"):
                dup_of["venue"] = ev["venue"]
            if not dup_of.get("end_date") and ev.get("end_date"):
                dup_of["end_date"] = ev["end_date"]
            if dup_of.get("area") == "other" and ev.get("area") != "other":
                dup_of["area"] = ev["area"]
            if not dup_of.get("note") and ev.get("note"):
                dup_of["note"] = ev["note"]
            continue
        kept.append(ev)
        normed.append(n)
    return kept
