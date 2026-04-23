---
name: q10-status
description: Q10 (Qoo10) EC の稼働状況を即答する。読み取り専用で q10_tool の cron 出力・状態ファイルを参照。
version: 1.0.0
author: akatsuki-hd
metadata:
  hermes:
    tags: [q10, qoo10, ec, status]
model: claude-sonnet-4-5
max_turns: 10
---

# q10-status — Q10 稼働状況 即答

`~/q10_tool/` は **読み取り専用**。以下のコマンドのみ実行する。

## 実行手順

### 1. Cron 登録確認
```bash
crontab -l 2>/dev/null | grep -i q10
```
期待値：
- `sync_prices.py` が `0 0,6,12,18 * * *`（6時間おき）
- `order_watcher.py` が `*/15 * * * *`（15分おき）

### 2. 直近の注文 watcher ログ（最新日付のみ）
```bash
ls -t ~/q10_tool/logs/order_watcher_*.log 2>/dev/null | head -1 | xargs tail -n 30
```

### 3. 最後の注文チェック時刻
```bash
cat ~/q10_tool/data/last_order_check.json 2>/dev/null
```

### 4. 直近の同期ログ
```bash
tail -n 20 ~/q10_tool/logs/cron_sync.log 2>/dev/null
```

### 5. 処理済み注文件数（軽量）
```bash
python3 -c "import json; d=json.load(open('$HOME/q10_tool/data/processed_orders.json')); print(f'processed={len(d) if isinstance(d,(list,dict)) else \"?\"}' )" 2>/dev/null
```

## 出力フォーマット

```
【Q10 EC 状況】
- cron: ✅/❌ sync(6h), order_watcher(15m)
- 最終注文チェック: {{timestamp}}（{{経過時間}}前）
- 直近注文watcher: ✅成功 / ⚠️ エラーN件
- 同期直近: ✅成功 / ❌ 失敗（理由: ...）
- 処理済み注文: N件
- 所感: （1〜2行）
```

## 判断ルール

| 状態 | 判定 |
|---|---|
| last_order_check が 30分以上前 | ⚠️ watcher 異常の可能性 |
| last_order_check が 6h 以上前 | ❌ 即 CEO + DX へエスカレーション |
| cron_sync.log に直近 `Error` / `Traceback` | ⚠️ 注意喚起 |
| ログファイル自体が欠落 | ❌ DX Director / infra-health へ引き継ぎ |

## 禁止

- `~/q10_tool/` への書き込み一切（`>`, `>>`, `tee`, `sed -i`, `touch`, `rm`, `mv`, `cp`）
- ソースコード（`*.py`）の改変提案
- `data/order_tokens.json` や `.env` の表示
