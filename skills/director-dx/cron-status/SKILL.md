---
name: cron-status
description: crontab 登録と直近実行結果を集約。Q10 cron と Hermes cron の両方を確認。
version: 1.0.0
author: akatsuki-hd
metadata:
  hermes:
    tags: [dx, cron, scheduling]
model: claude-sonnet-4-5
max_turns: 10
---

# cron-status — cron 稼働状況

## 実行手順

### 1. crontab 全体
```bash
crontab -l 2>/dev/null
```

### 2. Q10 関連 cron
```bash
crontab -l 2>/dev/null | grep -iE "(q10|qoo10|sync_prices|order_watcher)"
```

### 3. Q10 cron 最終実行（ログの最終更新時刻）
```bash
stat -f "%Sm %N" ~/q10_tool/logs/cron_sync.log ~/q10_tool/logs/cron_order.log 2>/dev/null
```

### 4. 最新 cron ログ末尾
```bash
tail -n 10 ~/q10_tool/logs/cron_order.log 2>/dev/null
tail -n 10 ~/q10_tool/logs/cron_sync.log 2>/dev/null
```

### 5. Hermes cron（あれば）
```bash
hermes cron list 2>/dev/null | head -20
```

## 出力フォーマット

```
【cron 状態】
- 登録ジョブ数: N
- Q10 sync_prices (6h):    ✅ 最終 {{time}} ({{経過}}前)
- Q10 order_watcher (15m): ✅ 最終 {{time}} ({{経過}}前)
- Hermes cron: {{count}}件
- 最新エラー: なし / ⚠️ N件（抜粋）
- 判定: ✅正常 / ⚠️要調査 / ❌停止中
```

## 判定ルール

| 状態 | 判定 |
|---|---|
| order_watcher ログが 30分以上更新なし | ⚠️ 要調査 |
| order_watcher ログが 1h 以上更新なし | ❌ 停止中 |
| sync_prices ログが 7h 以上更新なし | ❌ 停止中 |
| ログに `Traceback` / `ERROR` 直近 | ⚠️ 原因抜粋を報告 |

## 禁止

- crontab の **編集**（読み取りのみ）
- Q10 cron ログへの書き込み
- `sudo crontab` の使用
