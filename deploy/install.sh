#!/bin/bash
# 配信と取得の launchd ジョブを (再)セットアップする（docs/runbook.md の「デプロイ」）。何度流しても同じ状態になる。
#   ~/yokohama-events/deploy/install.sh
# 雛形は本番の作業ツリー（~/yokohama-events。main）のもの。__HOME__ をこの Mac の $HOME で書き出し、形を確かめてから置き、
# bootout → bootstrap で入れ直す。MBP でない・解釈系（/opt/homebrew/bin/python3.12）が無い・requests と bs4 が無い・本番が main でないときは入れずに止まる。
# 入れた後に配信が 200 を返さなければ終了コード 1。
set -euo pipefail

RENDERED=""
trap 'rm -f "$RENDERED"' EXIT   # 途中で止まっても書き出しの一時ファイルを残さない

LIVE="$HOME/yokohama-events"
PY=/opt/homebrew/bin/python3.12
DOMAIN="gui/$(id -u)"
LABELS="com.kuma.yokohama-events com.kuma.yokohama-events-scrape"

# 本番は MBP だけ（MBA の 2 つのジョブは disable 済み。enable で外さないように、ほかの機体では入れない）
if [ "$(scutil --get LocalHostName)" != "WatarunoMacBook-Pro" ]; then
  echo "本番は MBP（WatarunoMacBook-Pro）だけ。この機体: $(scutil --get LocalHostName)" >&2
  exit 1
fi
if [ ! -x "$PY" ]; then
  echo "$PY が無い（brew install python@3.12）" >&2
  exit 1
fi
if ! "$PY" -c 'import requests, bs4' 2>/dev/null; then
  echo "$PY に requests・beautifulsoup4 が無い: $PY -m pip install --user --break-system-packages -r $LIVE/requirements.txt" >&2
  exit 1
fi
BRANCH="$(git -C "$LIVE" branch --show-current)"
if [ "$BRANCH" != "main" ]; then
  echo "本番の作業ツリー ($LIVE) のブランチが main ではない: ${BRANCH:-(detached HEAD)}。docs/runbook.md の「デプロイ」の手順で main にしてから流す" >&2
  exit 1
fi

mkdir -p "$HOME/Library/LaunchAgents"
for LABEL in $LABELS; do
  RENDERED="$(mktemp -t "$LABEL")"
  sed "s#__HOME__#$HOME#g" "$LIVE/deploy/$LABEL.plist" > "$RENDERED"
  plutil -lint "$RENDERED" >/dev/null
  if [ "$(/usr/libexec/PlistBuddy -c 'Print :Label' "$RENDERED")" != "$LABEL" ]; then
    echo "$LIVE/deploy/$LABEL.plist の Label が $LABEL ではない" >&2
    exit 1
  fi
  DST="$HOME/Library/LaunchAgents/$LABEL.plist"
  mv "$RENDERED" "$DST"
  chmod 644 "$DST"
  launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
  for _ in $(seq 1 50); do launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1 || break; sleep 0.2; done
  launchctl enable "$DOMAIN/$LABEL"   # 永続的な disable が付いていると bootstrap が失敗するので外す
  launchctl bootstrap "$DOMAIN" "$DST"
  echo "入れた: $LABEL（$(launchctl print "$DOMAIN/$LABEL" | awk '$1 == "program" {print $3; exit}')）"
done

for _ in $(seq 1 40); do
  curl -fs -o /dev/null http://127.0.0.1:8788/ 2>/dev/null && break
  sleep 0.25
done
CODE="$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8788/ || true)"
echo "配信: http://127.0.0.1:8788/ → $CODE"
if [ "$CODE" != 200 ]; then
  echo "配信が 200 を返さない（launchctl print gui/$(id -u)/com.kuma.yokohama-events と、配信のログ /tmp/yokohama-events-server.log〔plist の StandardErrorPath〕を見る）" >&2
  exit 1
fi
