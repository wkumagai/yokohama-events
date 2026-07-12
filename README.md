# yokohama-events

馬車道・桜木町を中心に、関内・みなとみらい・山下公園・元町・山手・三溪園・横浜駅周辺までの
イベント・催し物を自動収集してローカルHTMLで一覧表示するプロジェクト（ヨコハマイベント帖）。

## クイックスタート（開発に参加する人向け）

```bash
git clone <このリポジトリ>
cd yokohama-events
pip3 install -r requirements.txt   # requests + beautifulsoup4 のみ
python3 scraper/run.py             # イベント収集 → data/events.json, events.data.js 生成(数十分かかる)
python3 -m http.server 8788        # → http://localhost:8788/ で表示
```

- サイト本体は `site/index.html` 1ファイル（素のHTML/CSS/JS、ビルド不要）
- 情報源を追加するには `scraper/sources/` に1ファイル書いて `scraper/run.py` の `SOURCE_MODULES` に登録
  （未実装の候補は `docs/sources.md` に約80源リストアップ済み）
- 収集ポリシー（後述）を必ず守ること: リクエスト間2秒以上・本文/画像は転載しない

## 構成（計画）

```
yokohama-events/
├── README.md              ← このファイル
├── docs/
│   ├── sources.md         ← 情報源カタログ（約80源・実地調査済み 2026-07-05）
│   └── categories.md      ← カテゴリ体系と正規化ルール
├── scraper/
│   ├── common.py          ← fetch(待機・UA・robots配慮)、正規化、重複排除
│   ├── sources/           ← 情報源ごとに1ファイル（parse_xxx.py）
│   └── run.py             ← 全ソース実行 → data/events.json 生成
├── data/
│   ├── events.json        ← 収集結果（正規イベントデータ）
│   ├── events.data.js     ← 同内容を `const EVENTS=[...]` 形式で出力（file://直開き用）
│   ├── annual.json        ← 毎年恒例イベントの静的リスト（手持ちデータ）
│   └── overrides.json     ← カテゴリ等の手動補正
└── site/
    └── index.html         ← 一覧サイト本体（素のHTML/CSS/JS、ビルド不要）
```

- **常駐サーバー**: launchd (`~/Library/LaunchAgents/com.<user>.yokohama-events.plist` 等) で
  `python3 -m http.server 8788` をMac起動中は常に稼働させる想定。
  - ローカル: http://localhost:8788/
  - 同一Wi-Fi内の他端末(iPhone等)から: `http://<このMacのホスト名>.local:8788/`
  - 外部公開する場合は Tailscale Funnel 等が手軽（`tailscale funnel --https=443 http://127.0.0.1:8788`）。
    停止は `tailscale funnel --https=443 off`
  - launchd停止: `launchctl bootout gui/$(id -u)/com.<user>.yokohama-events`
- `site/index.html` を file:// で直接開いても動く（データは `events.data.js` のscript読込、キャッシュバスター付き）。
- ★お気に入り: カード右上の星で登録、期間行の「★お気に入り」チップで絞り込み。localStorage保存なので**同じURL(オリジン)でアクセスし続けること**（localhostとfile://では別保存になる）。
- **自動更新**: launchd (`~/Library/LaunchAgents/com.<user>.yokohama-events-scrape.plist` 等) で
  毎朝6:00に `scraper/scrape_and_log.sh` → `scraper/run.py` を自動実行し、`data/events.json` / `events.data.js` を更新する。
  ページ側はキャッシュ回避読み込みなので、再読み込みするだけで最新データが反映される。
  - ログ: `logs/scrape.log`
  - 今すぐ更新: `launchctl kickstart gui/$(id -u)/com.<user>.yokohama-events-scrape`
  - 手動更新したい場合は従来通り `python3 scraper/run.py` でも可。
- 公開するときは このフォルダをそのまま任意の静的ホスティングに置くだけ。

## イベントスキーマ

```json
{
  "id": "sha1(source+url+date)",
  "title": "…",
  "start_date": "2026-07-10",
  "end_date": "2026-07-21",
  "time": "19:00開演（分かれば）",
  "venue": "横浜能楽堂",
  "area": "sakuragicho",
  "category": "traditional",
  "tags": ["paid", "indoor", "one_day"],
  "url": "https://…（必ず元サイトへ誘導）",
  "source": "yokohama-nohgakudou"
}
```

## 実装フェーズ

1. **Phase 1（最小動作）**: Tier 1アグリゲータ4本（welcome.city / アートナビ / minatomirai21 / 区版イベント検索）
   + RSSが生きている施設（にぎわい座・赤レンガ1号館・BUNTAI・人形の家・近代文学館・大佛次郎記念館・アソビル・西口エリマネ等）
   + annual.json（恒例イベント）→ site/index.html で一覧・エリア/カテゴリ絞込
2. **Phase 2（施設直取り）**: 静的HTMLの主要施設パーサーを順次追加
   （能楽堂・関内ホール・KAAT・音楽堂・みなとみらいホール・大さん橋・市役所アトリウム・三溪園・山手西洋館…）
3. **Phase 3（難物）**: Playwright導入でJS必須サイト（パシフィコ・マークイズ等）、
   bot遮断サイト（高島屋・スカイビル・京急ミュージアム）はwelcome.city/PR TIMES経由の代替取得
4. **Phase 4（公開）**: 静的ホスティングへ配置（別途）

## 収集ポリシー

- 1日1回巡回・リクエスト間2秒以上、robots.txt尊重
- 保存はタイトル/日時/会場/カテゴリ/元URLのみ。本文・画像は転載せずリンク誘導
- connpassはAPI以外禁止、Peatixは対象外（docs/sources.md 参照）
