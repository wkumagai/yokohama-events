#!/bin/bash
# launchdから毎朝呼ばれる更新スクリプト。実行ログを1本に残す(先頭に開始時刻)。
set -u
cd "$(dirname "$0")/.."
{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') scrape start ====="
  /usr/bin/python3 scraper/run.py
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') scrape end ====="
} >> logs/scrape.log 2>&1

# ログが1MBを超えたら古い方を捨てて簡易ローテーション
if [ -f logs/scrape.log ] && [ "$(stat -f%z logs/scrape.log)" -gt 1048576 ]; then
  tail -n 2000 logs/scrape.log > logs/scrape.log.tmp && mv logs/scrape.log.tmp logs/scrape.log
fi
