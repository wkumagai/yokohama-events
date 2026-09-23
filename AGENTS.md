# AGENTS.md

このリポジトリは `wkumagai/ops` が管理する常時稼働システム（managed-system）の1つ。
**どのエージェント（Claude Code / Codex / Copilot / Cursor / Gemini / その他）も、
作業を始める前にこの文書を読むこと。**

規約の全文は ops リポジトリの `AGENTS.md` が唯一の正。取得:

```bash
gh api repos/wkumagai/ops/contents/AGENTS.md --jq .content | base64 -d
```

**ops は private なので、認証が無いと 404（403 ではない）が返る。**
「存在しない」ように見えるが、実際には権限が無いだけである。
取得できなくても下の「止まる規則」はこの文書だけで完結している。
**読めなかったことを理由に、判定を飛ばして先へ進んではならない。**

<!-- OPS-RULE:BEGIN v1 -->
## 止まる規則（取りに行かなくても守れる最小限）

作業を始める前に、その作業が次の **不可逆5類型** に当たるかを判定する。

1. 本番データの削除・不可逆な変更
2. 外部への送信（メール送信・公開設定への変更・決済実行・SNS投稿）
3. 金の発生（新規契約・プラン変更・有料APIの新規利用）
4. 移行コストが高い構造変更（リポジトリの統合/分割/削除、規約や台帳スキーマの変更）
5. 権限と鍵（シークレット追加・権限付与・トークン発行）

- **当たらない** → 実行してよい。PR を出し `automerge` ラベルを付ける。
- **当たる、または疑わしい** → 実行しない。`needs-decision` ラベルの issue を1本立てて **止まる**。
- **迷ったら「当たる」側に寄せる。エージェントが自分でこの規則を緩めてはならない。**

判定結果は作業前に issue へ1行書く（例: `5類型: 該当なし`）。

タスク管理に Linear / beads(bd) / TodoWrite を使わない。記録は GitHub に一本化した。
<!-- OPS-RULE:END v1 -->

## このリポジトリで作業するとき

1. `docs/runbook.md` を読む（このシステム固有の手順）
2. 上の5類型を判定し、issue に1行コメントする
3. ブランチを切る。**既定ブランチ（`main` / `master`）へ直接 push しない**
4. PR 本文に `Closes #N` を書く。戻せる変更なら `automerge` ラベルを付ける
5. 仮の判断をしたときだけ、ops の `decisions.md` に追記する PR を別に出す

進捗報告を issue に書き足さない。運用者が見るのは ops の README（状態表）と
`needs-decision` ラベルの issue の2箇所だけ。

## この文書の扱い

- `CLAUDE.md` / `.github/copilot-instructions.md` / `GEMINI.md` はこの文書への導線であり、
  **内容を分岐させない**。規約を書き足すならこの `AGENTS.md` に書く。
- `.cursorrules` / `.windsurfrules` / `.clinerules` / `.rules` を置かないこと。
  Zed は最初に見つかった1つだけを読むため、それらがあると **この AGENTS.md が無言で無視される**。
