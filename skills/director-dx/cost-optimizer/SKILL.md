---
name: cost-optimizer
description: トークン使用量を深掘り分析し、Max 5x プランの価値判定と Pro ダウングレード推奨を行う。毎朝ブリーフで必須。
version: 1.0.0
author: akatsuki-hd
metadata:
  hermes:
    tags: [dx, cost, optimizer, anthropic, downgrade, max5x]
model: claude-sonnet-4-5
max_turns: 12
---

# cost-optimizer — Max 5x → Pro ダウングレード判定

**Ticket #1 で最重要のスキル。** 毎朝ブリーフで必須実行。

## 目的

1. 直近7日 / 30日のトークン使用量を可視化
2. Anthropic Max 5x プラン（約 $100/月）と Pro プラン（$20/月）を比較
3. 実際の消費量から **Pro にダウングレードしても大丈夫か** を数字で判断
4. 判断材料を CEO に返す

## 実行手順

### 1. 今日のトークン
```bash
hermes insights --period today 2>/dev/null
```

### 2. 直近7日
```bash
hermes insights --period week 2>/dev/null
```

### 3. 今月累積
```bash
hermes insights --period month 2>/dev/null
```

### 4. 長文コンテキストは必ず /compress
サマリを `/compress` してから分析する。生ログを全部context に載せない。

### 5. モデル別内訳
```bash
hermes insights --by-model 2>/dev/null | head -40
```
Sonnet 4.5 と Opus の比率を把握。

## 判定ロジック（Max 5x → Pro）

### 月間推定コスト計算
- 入力トークン × $3 / 1M
- 出力トークン × $15 / 1M
- キャッシュヒット分は割引適用
- 円換算：1 USD ≈ ¥155（レートは参考値、最新は takumi に確認）

### 判定基準

| 月間推定コスト | プラン推奨 | アクション |
|---|---|---|
| ≤ ¥3,000（$20以下） | **Pro（$20/月）で十分** | Max 5x 解約候補 |
| ¥3,000〜¥4,000 | 様子見、来月再判定 | 余裕なし、効率化検討 |
| ¥4,000〜¥15,000 | Max 5x 継続が妥当 | 現状維持 |
| > ¥15,000 | Max 5x でも赤字リスク | 使い方を見直し |

### 閾値アラート（ハードリミット）

- 月間 ¥4,000 超えたら **「Pro ダウングレード推奨」を CEO に即エスカレーション**
- 朝ブリーフで毎日この判定を含める

## 出力フォーマット

```
【💰 コスト最適化レポート】
期間: 直近7日 / 今月累積

■ 使用量
- 今日: in={{N}}K / out={{M}}K (~$X.XX)
- 今週: in={{N}}K / out={{M}}K (~$X.XX)
- 今月: in={{N}}K / out={{M}}K (~$X.XX ≈ ¥YYY)

■ モデル比率
- Sonnet 4.5: {{X}}%
- Opus 4.5:   {{Y}}%  ← CEO複雑判定時のみ想定
- Kimi(fb):   {{Z}}%

■ プラン判定
- 現在: Max 5x（$100/月相当）
- 実消費: ¥XXX / 月（推定）
- **推奨: {{Pro / 継続 / 見直し}}**
- 判断材料: {{理由2〜3行}}

■ 所感
- 最もトークン食ってる箇所: {{...}}
- 改善案: {{...}}
```

## 削減アクション候補（提案用）

- 長文コンテキストは `/compress` 徹底
- 繰り返し処理は cron 側で前処理済みファイルを渡す
- Opus 呼び出しの抑制（CEO Skill の条件分岐強化）
- Kimi へのフォールバック比率を増やす

## 禁止

- `.env` や API キーを出力
- Anthropic 管理画面への勝手なサブスクリプション操作（人間のみ）
- Opus 4.5 を使ってこの分析をする（Sonnet 4.5 で完結する）
