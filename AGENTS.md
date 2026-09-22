# AGENTS.md（システム側）

規約は ops リポジトリの AGENTS.md が唯一の正。作業前に読む: https://github.com/wkumagai/ops/blob/main/AGENTS.md

このリポジトリ固有の情報は `docs/runbook.md` にある。以下は最小限。

- `/health` は ops の `docs/HEALTH_SPEC.md` の形式で応答すること。
- 本番へ出るものはすべて PR 経由。戻せる変更は `automerge` ラベル。
- systems.yml（ops）の登録内容と実体がずれたら、ops に PR を出して直す。
