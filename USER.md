# User Profile — takumi

## Identity

- **Name:** Takumi Ueshima（上島 匠）
- **Role:** CEO / Founder — あかつきHD（持株会社モデル）
- **Email:** tahaizhidao@gmail.com
- **Timezone:** Asia/Tokyo（JST）

## Business Portfolio

- **Q10 EC事業**（子会社）：`~/q10_tool/` で運用中、cron駆動
- **持株会社（HD）側のオペレーション:** `~/.hermes/` + `~/personal-holdings-dashboard/`
- Phase 1 は **EC + DX + Finance(RO)** 優先、SNS / NewBiz は構築中

## Communication Preferences

- **言語:** 日本語
- **スタイル:** 構造化された応答、実行優先、冗長な前置きは不要
- **判断材料は数値で:** 「たぶん」「多分」は避け、「直近3回中2回成功」「コスト ¥X」で伝える
- **確認が必要な破壊的操作** は必ず事前に聞く（rm、git reset、外部送信など）
- **コード変更を伴う提案は差分で示す**

## Working Style

- 長い説明より、まず「何ができて何ができないか」を1行で
- Directorを跨ぐ話題はCEO Skillに一度集約してから返答
- 進捗は TaskCreate / TaskUpdate で可視化
- エラーや不確実性は隠さず出す

## Hard Constraints

- **`~/q10_tool/` は読み取り専用**（HD側から書き込み禁止）
- sudo 使用禁止（許可なしに）
- 新規パッケージインストール禁止（許可なしに）
- `.env` の中身は絶対に出力しない
- `hermes gateway start` の起動は takumi 本人が行う

## Channels

- Discord / Telegram 経由で Hermes にアクセス
- 朝ブリーフは毎日自動配信予定
