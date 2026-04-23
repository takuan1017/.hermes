---
name: infra-health
description: macOS ローカルのインフラ健康診断（ディスク・メモリ・プロセス・LaunchAgent）。
version: 1.0.0
author: akatsuki-hd
metadata:
  hermes:
    tags: [dx, infra, health, macos]
model: claude-sonnet-4-5
max_turns: 10
---

# infra-health — インフラ健康診断

## 実行手順

### 1. ディスク使用率
```bash
df -h / ~/ 2>/dev/null | awk 'NR==1 || /\// {print}'
```

### 2. メモリ・スワップ
```bash
vm_stat | head -8
```

### 3. ロードアベレージ
```bash
uptime
```

### 4. Hermes 関連プロセス
```bash
pgrep -fla hermes | head -10
```

### 5. LaunchAgent 登録状況（あかつき関連）
```bash
ls ~/Library/LaunchAgents/ | grep -iE "(akatsuki|hermes|q10)"
launchctl list 2>/dev/null | grep -iE "(akatsuki|hermes|q10)"
```

### 6. Hermes ログサイズ（肥大化チェック）
```bash
du -sh ~/.hermes/logs/ 2>/dev/null
du -sh ~/.hermes/sessions/ 2>/dev/null
```

## 出力フォーマット

```
【インフラ健康度】
- Disk /:    {{used}}% ({{alert_if_over_85}})
- Disk ~/:   {{used}}%
- Load avg:  {{1m}} / {{5m}} / {{15m}}
- Hermes proc: {{count}} 個稼働
- LaunchAgent: ✅登録 / ❌未登録
- logs/: {{size}}
- sessions/: {{size}}
- 判定: ✅健全 / ⚠️要注意 / ❌異常
```

## 閾値

| 項目 | ⚠️ | ❌ |
|---|---|---|
| Disk / 使用率 | > 80% | > 90% |
| Disk ~/ 使用率 | > 75% | > 90% |
| Load avg 5m | > コア数 | > コア数 × 2 |
| logs/ サイズ | > 500MB | > 2GB |

## 禁止

- `sudo` の使用
- プロセスの kill（takumi 許可なし）
- `/var/log` への書き込み
