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
- 手順（コマンド or ワークフロー名）:
- 所要時間:

## 復旧
- ロールバック手順（1コマンドで戻るなら、そのコマンド）:
- 再起動手順:
- データ修復が必要になる典型（＝5類型1、人の判断）:

## 既知の癖
- 日次スクレイプ（MBP、launchd `com.kuma.yokohama-events-scrape`、毎朝 06:00）の実行記録は
  `/Users/kuma/yokohama-events/logs/scrape.log` と `data/events.json` の更新時刻で見る。
  launchd の StandardOutPath（`/tmp/yokohama-events-scrape-launchd.log`）はスクリプトが出力を自前のログへ
  追記するため常に 0 バイトで、これを見ると「止まっている」ように見える（2026-09-23 ops#65 の誤検知）。
- 再起動: `ssh MBP 'launchctl kickstart -k gui/501/com.kuma.yokohama-events-scrape'`（データ修復は不要。戻せる）
