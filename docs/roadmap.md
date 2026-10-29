# AI分類器 開発目標・ロードマップ

## 最終目標

LAE教師データを利用してAI分類器を構築し、

- SF銀河
- Q銀河

を含む大規模サンプルの分類作業を効率化する。

さらに、

AI
↓
推論
↓
Uncertain抽出
↓
人間確認
↓
教師データ改善
↓
再学習

という Human-in-the-Loop 環境を構築する。

---

## 現在完了

### 教師データ

✅ 教師データ347件作成

✅ ラベル品質改善

✅ 誤分類レビュー

✅ 教師データ改善フロー構築

---

### AI学習

✅ GalaxyDataset実装

✅ DataLoader構築

✅ ResNet18導入

✅ F277W + OBJ + ASY の3チャネル化

✅ AI学習

✅ Test評価

✅ 誤分類解析

✅ 学習済みモデル保存

---

### 推論

✅ 単一天体推論

✅ LAE一括推論

✅ SF一括推論

✅ Q一括推論

✅ prediction.csv出力

✅ prediction_SF.csv出力

✅ prediction_Q.csv出力

---

### Human-in-the-Loop

✅ AI予測結果CSV出力

✅ Uncertain抽出

✅ Webアプリ連携

✅ Inspector連携

✅ AI確率表示

✅ 人間判定比較

---

## 現在の成果

### 教師データ

347天体

---

### SF推論

3394天体

Uncertain

764天体

---

### Q推論

37天体

Uncertain

5天体

---

## 短期目標

- Uncertainサンプルレビュー
- SF教師データ作成
- Q教師データ作成
- ラベル品質改善
- 誤分類分析継続

---

## 中期目標

- Active Learning導入
- 高信頼サンプル自動採用
- AIと人間の一致率評価
- クラス不均衡対策
- モデル性能向上

---

## 長期目標

LAEだけでなく、

- SF
- Q

を含む教師データで再学習を実施する。

さらに、

高信頼サンプル
↓
自動採用

低信頼サンプル
↓
人間確認

を実現し、

数千〜数万天体規模の形態分類作業を効率化する。

---

## 将来構想

```text
人間による分類
        ↓
教師データ
        ↓
AI学習
        ↓
全サンプル推論
        ↓
Uncertain抽出
        ↓
Inspector
        ↓
人間確認
        ↓
教師データ改善
        ↓
再学習
        ↓
性能向上
```

---

## 現在位置

```text
教師データ作成
        ↓
AI学習
        ↓
SF/Q推論
        ↓
Inspector統合
        ↓
Human-in-the-Loop構築
        ↓
Uncertainレビュー　　　← 現在ここ
        ↓
Active Learning
        ↓
半教師あり学習
```