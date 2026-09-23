# yokohama-events（サイト名「ヨコハマイベント帖」）

馬車道・桜木町を中心に、関内・みなとみらい・山下公園・元町・山手・三溪園・横浜駅周辺のイベントを毎日自動収集し、1枚の HTML で一覧表示する。
[ops](https://github.com/wkumagai/ops) が管理する常時稼働システムの1つ。MacBook Pro 上の launchd ジョブが毎朝収集し、一覧はその Mac で Web サーバーを起動するか、HTML を直接開いて見る。
外部サービス・認証・鍵は使わない。

## 使い方

```
pip3 install -r requirements.txt                    # requests と beautifulsoup4 のみ
python3 scraper/run.py                              # 収集して data/events.json と data/events.data.js を生成（数十分かかる）
python3 -m http.server 8788                         # http://localhost:8788/ で一覧を表示
launchctl kickstart -k gui/$(id -u)/com.kuma.yokohama-events-scrape   # 定期実行を待たずに今すぐ収集する
```

- 同じ Wi-Fi 内の他の端末からは `http://<この Mac のホスト名>.local:8788/` で開ける
- `site/index.html` をブラウザで直接（file://）開いても動く
- 収集は 1 日 1 回、リクエスト間 2 秒以上、robots.txt を尊重する。保存するのはタイトル・日時・会場・カテゴリ・元 URL だけで、本文と画像は保存しない

## 画面の見方

| 場所 | 意味 |
|---|---|
| 期間の行（すべて／今日／今週末／7日以内／30日以内） | 開催期間で絞り込む |
| ★ お気に入り | 星を付けたイベントだけ表示する。件数は括弧内 |
| エリアの行・カテゴリの行 | それぞれで絞り込む。期間・エリア・カテゴリ・キーワードの条件はすべて AND |
| キーワード欄 | イベント名と会場名で絞り込む |
| 「区民施設の講座・教室も表示」 | 外すと区の施設のイベントを隠す |
| 右端の「N件」 | 現在の絞り込みに合う件数 |
| 一覧の区切り | 期間を選ぶと「単発・短期」と「長期開催中」に分かれる。「すべて」では「開催中」の後に月ごとに並ぶ。各区切りは 24 件を超えると「残り N 件をすべて表示」ボタンが出る |
| カードの ☆ | お気に入りに追加・解除。カードの背表紙の色はカテゴリ |
| カードのリンク | 必ず元サイトへ移動する |

**お気に入りはブラウザの localStorage に保存されるため、同じ URL で開き続けること。** `http://localhost:8788/` と file:// では別々に保存される。

## 仕組み

- launchd のジョブ `com.kuma.yokohama-events-scrape` が毎朝 06:00 に `scraper/scrape_and_log.sh` を実行する。ログは `logs/scrape.log`（1 MB を超えると末尾 2000 行だけ残す）
- `scraper/run.py` が `scraper/sources/` の情報源モジュールを順に実行し、`data/annual.json`（毎年恒例のイベント）を加える
- 終了済み・400 日より先・日付のないイベントを除外し、重複を統合する（タイトルと開始日の完全一致、次に表記ゆれ）。優先順は施設の公式サイト > 専門の集約サイト > 汎用の集約サイト > 区の施設 > 恒例
- `data/overrides.json` があれば、イベント id ごとの手動補正を上書きする
- `data/events.json` と `data/events.data.js` を書き出す。ページは `events.data.js` をキャッシュを避けて読むため、ブラウザを再読み込みするだけで最新になる
- 取得は `scraper/common.py` の `fetch()` が担い、間隔 2 秒・User-Agent 明示・失敗時は間隔を空けて再試行する。TLS で失敗するサイトは curl で取得する

## 対象と設定

| 何 | どこ |
|---|---|
| 収集する情報源とその優先順 | `scraper/run.py` の `SOURCE_MODULES` |
| 情報源ごとの取得処理 | `scraper/sources/<名前>.py`（`scrape()` がイベントの list を返す） |
| 毎年恒例のイベント | `data/annual.json` |
| カテゴリ・エリアの手動補正（任意） | `data/overrides.json`（`id` で対象を指定し、他のキーを上書き） |
| カテゴリの体系と判定ルール | [docs/categories.md](docs/categories.md) |
| 情報源の候補（未実装を含む） | [docs/sources.md](docs/sources.md) |
| 一覧ページ | `site/index.html`（素の HTML/CSS/JS、ビルド不要） |

`SOURCE_MODULES` に登録されていて `scraper/sources/` に実装がない情報源は `not implemented yet, skipped` と表示して飛ばす。これは正常。

## 障害時の対処

| 症状 | 対処 |
|---|---|
| 一覧が古い | `tail -n 30 logs/scrape.log` で最終実行の時刻と結果を確認する。実行されていなければ `launchctl kickstart -k gui/$(id -u)/com.kuma.yokohama-events-scrape`。実行後にブラウザを再読み込みする |
| launchd の標準出力ログが 0 バイトで止まって見える | 正常。スクリプトが出力を `logs/scrape.log` に自前で追記するため、launchd 側のログは常に空になる。実行記録は `logs/scrape.log` と `data/events.json` の更新時刻で見る |
| ある情報源だけ 0 件、または `ERROR:` になる | `python3 scraper/run.py` を手で実行し、`[<名前>]` で始まる行と末尾の `stats:` を見る。相手サイトの構造が変わったなら `scraper/sources/<名前>.py` を直す |
| `! HTTP 4xx` や `! fetch error` が続く | 一時的なら翌日の実行を待つ。同じ情報源で続くなら URL とパーサーを見直す。取得先の負荷にならないよう再試行を増やさない |
| ページが開けない | Web サーバーが動いていない。リポジトリのディレクトリで `python3 -m http.server 8788` を起動する |
| お気に入りが消えた | 別の URL（localhost と file://、ホスト名の違い）で開いている。以前と同じ URL で開く |
| 収集を止めたい | `launchctl bootout gui/$(id -u)/com.kuma.yokohama-events-scrape`。再開は launchd の設定ファイル（plist）を `launchctl bootstrap gui/$(id -u) <plist のパス>` で登録し直す |

## 開発

自動テストは無い。変更後は `python3 scraper/run.py` を実行し、末尾の `Total:` と `stats:` に `ERROR` が無いことと、ブラウザで一覧が表示されることを確認する。

情報源を追加するには `scraper/sources/` に 1 ファイル書き、`scraper/run.py` の `SOURCE_MODULES` に登録する。取得は必ず `common.fetch()` か `common.scrape_rss()` を通す。

運用手順は [docs/runbook.md](docs/runbook.md)、ディレクトリ構成・イベントのデータ形式・収集の方針・経緯は [docs/background.md](docs/background.md)。
