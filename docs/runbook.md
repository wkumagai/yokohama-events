# runbook — yokohama-events

## 概要
- 目的:
- 本番URL / エントリポイント:
- 実行形態: 常駐 | cron | イベント駆動
- 依存（外部サービス・鍵の名前のみ、値は書かない）:

## /health
- URL:
- `last_run` の意味（何の開始時刻か）:
- `duration_ms` の意味:

## デプロイ
- 本番は MBP の作業ツリー `~/yokohama-events`（main）。launchd の 2 つのジョブ（配信 `com.kuma.yokohama-events`・取得 `com.kuma.yokohama-events-scrape`）がここを指す。
  HEAD を動かす操作（switch・pull など）はこの節の手順でだけ行う（R-185）。MBA の 2 つのジョブは disable 済みで、入れない。
- 解釈系は配信・取得とも Homebrew の `/opt/homebrew/bin/python3.12`（前は macOS 付属の `/usr/bin/python3`。yokohama-events#8）。依存は
  `/opt/homebrew/bin/python3.12 -m pip install --user --break-system-packages -r ~/yokohama-events/requirements.txt`（`deploy/install.sh` は無ければ止まる）。
- 手順（main の変更を本番に入れる）:
  1. `git -C ~/yokohama-events branch --show-current` が `main`、`git -C ~/yokohama-events status --short` が `data/` の行だけ（取得が毎日書き換える）。
  2. `git -C ~/yokohama-events pull --ff-only origin main`（通らなければ止めて、手元の変更を確かめる）。
  3. `deploy/` の雛形か `requirements.txt` が変わったときは、`~/yokohama-events/deploy/install.sh`（雛形を書き出して 2 つとも入れ直す）。`scraper/` だけの変更なら要らない（次の 06:00 に新しいコードで動く）。
  4. 確かめ: `launchctl print gui/$(id -u)/com.kuma.yokohama-events` の `program` が plist の解釈系、`curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8788/` が 200。
     取得を変えたときは `launchctl kickstart gui/$(id -u)/com.kuma.yokohama-events-scrape` → 数分後（2026-11-24〜26 の 06:00 の取得は 3〜4 分）に `tail -n 5 ~/yokohama-events/logs/scrape.log` が `scrape end` で、`stats:` に `ERROR` が無い。
- 1 回目だけ（2026-11-26 に見た本番はブランチ `fix/public-dir-5`。origin に無い #5 のコミット `cb86156` が 1 つ。`data/`・`scraper/` は main と同じ）:
  手順 1 の前に `git -C ~/yokohama-events switch main`（`data/` の手元の変更はそのまま持ち越す）。`fix/public-dir-5` は手元に残る（#5 で扱う）。
  続けて 2〜4（3 は要る。plist を雛形から入れ直す）。
- 所要時間: 入れ直しは数秒（その間 8788 は答えない）。取得の確かめは数分。
- 避ける時間: 06:00 からの数分（取得の最中に `deploy/install.sh` を流すと、bootout がその回の取得を止める）。

## 復旧
- ロールバック手順（1コマンドで戻るなら、そのコマンド）: main で戻す PR（revert）をマージし、「デプロイ」の手順で入れる。解釈系だけを急いで戻すなら:
  - 配信: `~/Library/LaunchAgents/com.kuma.yokohama-events.plist` の先頭の引数を `/usr/bin/python3` に替え、`launchctl bootout gui/$(id -u)/com.kuma.yokohama-events` → `launchctl print gui/$(id -u)/com.kuma.yokohama-events` が失敗する（消えた）のを待つ → `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.kuma.yokohama-events.plist`（間を置かずに続けると `Bootstrap failed: 5` になりうる）。
  - 取得: 解釈系は追跡しているファイル `scraper/scrape_and_log.sh` の中にあるので、本番の作業ツリーで手で替えない（手元の変更が残り、次の `pull --ff-only` が止まる）。revert の PR で戻す。`/usr/bin/python3` にも requests・bs4 は残っている。
- 再起動手順:
- データ修復が必要になる典型（＝5類型1、人の判断）:

## 既知の癖
- 日次スクレイプ（MBP、launchd `com.kuma.yokohama-events-scrape`、毎朝 06:00）の実行記録は
  `/Users/kuma/yokohama-events/logs/scrape.log` と `data/events.json` の更新時刻で見る。
  launchd の StandardOutPath（`/tmp/yokohama-events-scrape-launchd.log`）はスクリプトが出力を自前のログへ
  追記するため常に 0 バイトで、これを見ると「止まっている」ように見える（2026-09-23 ops#65 の誤検知）。
- 再起動: `ssh MBP 'launchctl kickstart -k gui/501/com.kuma.yokohama-events-scrape'`（データ修復は不要。戻せる）
- 一覧の配信は launchd `com.kuma.yokohama-events`（常駐、ポート 8788、plist `~/Library/LaunchAgents/com.kuma.yokohama-events.plist`）。再起動: `ssh MBP 'launchctl kickstart -k gui/501/com.kuma.yokohama-events'`
