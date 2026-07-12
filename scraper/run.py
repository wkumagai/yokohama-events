# -*- coding: utf-8 -*-
"""全ソースを実行して data/events.json と data/events.data.js を生成する。
使い方: python3 scraper/run.py [--skip-fetch]
"""
import json
import os
import re
import sys
import unicodedata
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources"))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# ソースの優先順(重複時に先勝ち): 施設直取り > 専門集約 > 汎用集約 > 区民施設
SOURCE_MODULES = [
    ("akarenga", "akarenga"),
    ("atrium", "atrium"),
    ("artnavi", "artnavi"),
    ("mm21", "mm21"),
    ("welcome_city", "welcome_city"),
    ("ward", "ward"),
    # RSSベース(施設・団体公式)
    ("nigiwaiza", "nigiwaiza"),
    ("akarenga_hall", "akarenga_hall"),
    ("buntai", "buntai"),
    ("doll_museum", "doll_museum"),
    ("osaragi", "osaragi"),
    ("nishiguchi", "nishiguchi"),
    ("nogedaidogei", "nogedaidogei"),
    ("porta", "porta"),
    ("hamakore", "hamakore"),
    # Phase2: 施設直取り(静的HTML)
    ("nohgakudou", "nohgakudou"),
    ("kannai_hall", "kannai_hall"),
    ("kaat", "kaat"),
    ("ongakudo", "ongakudo"),
    ("mm_hall", "mm_hall"),
    ("osanbashi", "osanbashi"),
    ("sankeien", "sankeien"),
    ("yamate_seiyoukan", "yamate_seiyoukan"),
    ("art_museum", "art_museum"),
    ("zounohana", "zounohana"),
    ("kaikou_shiryoukan", "kaikou_shiryoukan"),
    ("nippon_maru", "nippon_maru"),
    ("newspark", "newspark"),
    # Phase3: Playwright(JS必須)
    ("pacifico", "pacifico"),
    ("markis", "markis"),
]

TODAY = date.today()
HORIZON = TODAY + timedelta(days=400)


def norm_title(t):
    t = unicodedata.normalize("NFKC", t or "").lower()
    return re.sub(r"[\s　!-/:-@\[-`{-~「」『』【】()（）・、。〜～]", "", t)


def load_annual():
    path = os.path.join(DATA, "annual.json")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        items = json.load(f)
    events = []
    from common import make_event
    for it in items:
        ev = make_event(
            "annual", it["title"], it.get("url"),
            it.get("start_date"), it.get("end_date"),
            venue=it.get("venue"), area=it.get("area"),
            category=it.get("category"), tags=it.get("tags", []),
        )
        if it.get("note"):
            ev["note"] = it["note"]
        events.append(ev)
    return events


def apply_overrides(events):
    path = os.path.join(DATA, "overrides.json")
    if not os.path.exists(path):
        return events
    with open(path, encoding="utf-8") as f:
        overrides = json.load(f)
    by_id = {o["id"]: o for o in overrides if "id" in o}
    for ev in events:
        if ev["id"] in by_id:
            ev.update({k: v for k, v in by_id[ev["id"]].items() if k != "id"})
    return events


def main():
    all_events = []
    stats = {}
    for label, mod_name in SOURCE_MODULES:
        try:
            mod = __import__(mod_name)
            print(f"[{label}] scraping...")
            evs = mod.scrape()
            stats[label] = len(evs)
            print(f"[{label}] {len(evs)} events")
            all_events.extend(evs)
        except ModuleNotFoundError:
            print(f"[{label}] not implemented yet, skipped")
            stats[label] = "not implemented"
        except Exception as e:
            import traceback
            traceback.print_exc()
            stats[label] = f"ERROR: {e}"

    annual = load_annual()
    stats["annual"] = len(annual)
    all_events.extend(annual)

    # フィルタ: 終了済み・遠すぎる未来・日付なしを除外
    kept = []
    for ev in all_events:
        s, e = ev.get("start_date"), ev.get("end_date")
        if not s:
            continue
        try:
            sd = date.fromisoformat(s)
            ed = date.fromisoformat(e) if e else sd
        except ValueError:
            continue
        if ed < TODAY or sd > HORIZON:
            continue
        kept.append(ev)

    # 重複排除: まず完全一致(タイトル+開始日)、次に表記ゆれ吸収の類似統合
    seen = {}
    for ev in kept:
        key = (norm_title(ev["title"])[:40], ev["start_date"])
        if key not in seen:
            seen[key] = ev
    from postprocess import fuzzy_dedupe
    result = fuzzy_dedupe(list(seen.values()))
    result = apply_overrides(result)
    result.sort(key=lambda ev: (ev["start_date"], ev.get("end_date") or ev["start_date"]))

    os.makedirs(DATA, exist_ok=True)
    meta = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "count": len(result),
        "stats": stats,
    }
    with open(os.path.join(DATA, "events.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "events": result}, f, ensure_ascii=False, indent=1)
    with open(os.path.join(DATA, "events.data.js"), "w", encoding="utf-8") as f:
        f.write("// 自動生成: python3 scraper/run.py\n")
        f.write("window.EVENTS_META = " + json.dumps(meta, ensure_ascii=False) + ";\n")
        f.write("window.EVENTS = " + json.dumps(result, ensure_ascii=False) + ";\n")
    print(f"\nTotal: {len(result)} events (raw {len(all_events)}, dedup/filtered)")
    print("stats:", json.dumps(stats, ensure_ascii=False))


if __name__ == "__main__":
    main()
