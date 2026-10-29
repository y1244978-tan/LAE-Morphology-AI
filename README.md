# LAE Morphology AI

LAE・SF・Q銀河の形態分類を支援するための学習・推論システムです。

修士研究で実施している

- LAE (Lyα Emitter)
- SF (Star Forming Galaxy)
- Q (Quiescent Galaxy)

の形態比較研究のために開発しました。

教師データを用いてAIを学習し、

- Detectable
- Bright Neighbor
- Multiple Component
- Point Source

の4ラベルを自動推定します。

また、

人間による分類
↓
AI学習
↓
推論
↓
Uncertain抽出
↓
人間確認
↓
教師データ改善

という Human-in-the-Loop 環境の構築を目的としています。

---

## 主な機能

### 学習

- ResNet18による学習
- 3チャネル入力対応(F277W / OBJ / ASY)
- 学習済みモデル保存
- Test評価
- 誤分類抽出

### 推論

- 単一天体推論
- LAE推論
- SF推論
- Q推論
- 一括推論

### 品質改善

- 誤分類CSV出力
- ラベル再検討支援
- 再学習サイクル
- Human-in-the-Loop運用

### Uncertain抽出

- AI低信頼サンプル抽出
- Review対象作成
- Inspector連携

### Inspector連携

- prediction.csv出力
- prediction_SF.csv出力
- prediction_Q.csv出力

- uncertain.csv出力
- uncertain_SF.csv出力
- uncertain_Q.csv出力

---

## ディレクトリ構成

```text
LAE-Morphology-AI

README.md

data/
docs/
images_all/
logs/
models/
src/
```

### data

教師データおよび推論結果

```text
morphology_labels_*.csv

prediction.csv
prediction_SF.csv
prediction_Q.csv

uncertain.csv
uncertain_SF.csv
uncertain_Q.csv
```

---

### docs

研究メモおよび開発ログ

```text
development_log.md
research_notes.md
roadmap.md
```

---

### images_all

AI学習および推論に利用する画像

```text
images_all_LAE
images_all_SF
images_all_Q
```

---

### logs

学習ログおよび実験ログ

---

### models

学習済みモデル

```text
resnet18_f277w.pth
```

---

### src

ソースコード

```text
train.py

predict.py
predict_all.py

predict_sf.py
predict_q.py

model.py
dataset.py

config.py
config_sf.py
config_q.py
```

---

## 現在の状態

### 学習

✅ ResNet18

✅ 3チャネル入力

✅ 教師データ自動切替

✅ 評価環境

✅ 誤分類解析

---

### 推論

✅ LAE推論

✅ SF推論

✅ Q推論

✅ 一括推論

✅ Uncertain抽出

---

### Human-in-the-Loop

✅ 教師データ作成

✅ AI学習

✅ 推論

✅ Uncertain抽出

✅ Inspector連携

✅ 再学習サイクル

---

## 現在の成果

教師データ

```text
347天体
```

---

SF推論

```text
3394天体
```

Uncertain

```text
764天体
```

---

Q推論

```text
37天体
```

Uncertain

```text
5天体
```

---

## 今後の予定

- Uncertainレビュー
- Active Learning
- 半教師あり学習
- モデル性能向上
- ラベル品質向上
- AIと人間の協調分類
