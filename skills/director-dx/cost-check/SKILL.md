---
name: cost-check
description: Anthropic API の使用量を即座にスナップショット取得（cost-optimizer の前段軽量チェック）。
version: 1.0.0
author: akatsuki-hd
metadata:
  hermes:
    tags: [dx, cost, anthropic, snapshot]
model: claude-sonnet-4-5
max_turns: 6
---

# cost-check — コスト スナップショット（軽量）

深い分析は `cost-optimizer` へ。こちらは **秒で返す** 軽量版。

## 実行手順

### 1. Hermes の使用量サマリ
```bash
hermes insights --period today 2>/dev/null | head -30
```

### 2. 今月の累積（あれば）
```bash
hermes insights --period month 2>/dev/null | head -30
```

### 3. セッション数ざっくり
```bash
ls ~/.hermes/sessions/ 2>/dev/null | wc -l
```

## 出力フォーマット

```
【コスト スナップショット】
- 本日トークン: in={{N}} / out={{M}}
- 本日推定コスト: $X.XX (約¥YYY)
- 今月累積: $X.XX (約¥YYY)
- セッション数: N
- 次アクション: 詳細分析が必要なら cost-optimizer を呼ぶ
```

## 判定

- 本日 > $2 → cost-optimizer を即発動
- 今月 > $25（約¥4,000）→ Pro ダウングレード検討フラグ

## 禁止

- `.env` の中身を表示
- API キーの一部でも出力
