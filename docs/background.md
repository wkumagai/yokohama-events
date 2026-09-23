# background — yokohama-events

README から外した「経緯・計画・データ形式・方針」を置く。使い方と障害時の対処は [README](../README.md)、運用手順は [runbook.md](runbook.md)。

## ディレクトリ構成

```
yokohama-events/
├── README.md
├── docs/
│   ├── background.md      ← このファイル
│   ├── runbook.md         ← 運用手順（実行記録の見方、再起動）
│   ├── sources.md         ← 情報源カタログ（実地調査の結果。未実装の候補を含む）
│   └── categories.md      ← カテゴリ体系と正規化ルール
├── scraper/
│   ├── common.py          ← fetch（待機・User-Agent・robots 配慮）、日付解析、カテゴリ／エリア判定、重複排除
│   ├── postprocess.py     ← 表記ゆれを吸収した重複統合
│   ├── sources/           ← 情報源ごとに 1 ファイル
│   ├── run.py             ← 全情報源を実行して data/ を生成
│   └── scrape_and_log.sh  ← launchd から呼ばれる。logs/scrape.log に追記し、1 MB 超で切り詰める
├── data/
│   ├── events.json        ← 収集結果（meta と events）
│   ├── events.data.js     ← 同内容を window.EVENTS / window.EVENTS_META として出力（file:// で開くため）
│   ├── annual.json        ← 毎年恒例イベントの静的リスト
│   └── overrides.json     ← カテゴリ等の手動補正（任意。無ければ何もしない）
├── index.html             ← site/index.html へ転送するだけ
└── site/
    └── index.html         ← 一覧サイト本体（素の HTML/CSS/JS、ビルド不要）
```

## イベントのデータ形式

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

`data/events.json` はこれを `events` に並べ、`meta` に生成時刻・件数・情報源ごとの件数（`stats`）を持つ。
`category` と `tags` の語彙は [categories.md](categories.md)。

## 収集の方針

- 1 日 1 回の巡回。リクエスト間 2 秒以上、robots.txt を尊重し、User-Agent で用途を明示する
- 保存するのはタイトル／日時／会場／カテゴリ／元 URL だけ。本文・画像は転載せず、必ず元サイトへリンクする
- connpass は API 以外の取得を行わない。Peatix は対象外（[sources.md](sources.md) 参照）
- 重複時の優先順は 施設の公式サイト > 専門の集約サイト > 汎用の集約サイト > 区の施設 > 恒例（`scraper/postprocess.py` の `SOURCE_PRIORITY`）

## 実装の段階（当初の計画）

1. 横断アグリゲータ（welcome.city／アートナビ／minatomirai21／区版イベント検索）と、RSS が使える施設（にぎわい座・赤レンガ 1 号館・BUNTAI・人形の家・大佛次郎記念館・西口エリアマネジメント等）、`annual.json` を合わせて一覧・絞り込みを動かす
2. 静的 HTML の主要施設（能楽堂・関内ホール・KAAT・音楽堂・みなとみらいホール・大さん橋・市役所アトリウム・三溪園・山手西洋館…）を順次追加する
3. JS 必須のサイト（パシフィコ・マークイズ等）は Playwright で、bot 遮断サイト（高島屋・スカイビル・京急ミュージアム）は welcome.city／PR TIMES 経由で代替取得する
4. 静的ホスティングへ配置して公開する

`scraper/run.py` の `SOURCE_MODULES` には 2〜3 の情報源も登録してあり、実装のないものは実行時に飛ばされる。

## 配信と公開

- 一覧の配信は `python3 -m http.server 8788`。launchd のジョブ `com.kuma.yokohama-events` として常駐させている
- 同じ Wi-Fi 内の他の端末（iPhone 等）からは `http://<この Mac のホスト名>.local:8788/`
- 外部に公開する場合は Tailscale Funnel が手軽: `tailscale funnel --https=443 http://127.0.0.1:8788`（停止は `tailscale funnel --https=443 off`）
- 静的ホスティングに置く場合は、このフォルダをそのまま配置すればよい

## 経緯

- 情報源の実地調査（全 URL を取得して確認）を行い、その結果を [sources.md](sources.md) にまとめてから実装した
- launchd の StandardOutPath が常に 0 バイトになる仕様のため、監視側が「止まっている」と誤検知したことがある。実行記録の正しい見方は [runbook.md](runbook.md) に書いた
