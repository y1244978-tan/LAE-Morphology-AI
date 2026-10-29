# AI開発ログ

## Day1 (2026-10-27)

### 目的

銀河画像自動分類支援システムの開発開始

### 現状

教師データ確認を実施

重複除去前 : 373件

重複除去後 : 347件

ユニーク天体数 : 347件

### ラベル統計

Detectable        : 295 (85.0%)

Bright Neighbor   : 101 (29.1%)

Multiple Component: 106 (30.5%)

Point Source      : 90 (25.9%)

### 実施内容

#### 1. プロジェクト作成

新規プロジェクト

LAE-Morphology-AI

を作成

フォルダ構成

- data
- docs
- logs
- src

#### 2. CSV読込確認

train.py を作成し、labels.csv の読込に成功

確認項目

- 列名取得成功
- 全347件取得成功

取得列

- id
- image_subset
- detectable
- bright_neighbor
- multiple_component
- point_source
- memo
- created_at

#### 3. FITS画像探索

既存分類システムと同じ画像ディレクトリを利用

画像数

F277W : 3780

OBJ   : 3780

ASY   : 3780

合計 : 11340

#### 4. IDとFITSの対応付け

CSVのIDから対応するF277W画像を取得できることを確認

例

ID : 476630

対応FITS :

NIRCam_F277Wv1r_id476630.fits

#### 5. FITS読込確認

astropyを用いてFITS画像の読込に成功

結果

shape : (601, 601)

dtype : >f4

min : -0.044

max : 216.230

#### 6. 画像表示確認

matplotlibで表示確認を実施

### 重要な発見

現在読込んでいるFITS画像は

601 × 601 pixel

であり、

人間が分類時に見ている

- F277W
- OBJ
- ASY

の3画像とは異なることを確認

現在の教師ラベルは

F277W + OBJ + ASY

を用いた目視判定結果である

そのため、

AI学習時にも可能な限り同じ画像を入力として使用する必要がある

### 評価

教師データ読込からFITS画像読込まで完了

CSVと画像の対応付けにも成功

AI学習に必要な基礎部分を構築できた

### 7. PyTorch環境構築

PyTorchおよびtorchvisionをインストール。

確認結果

torch==2.14.1+cpu

学習環境の構築に成功。

### 8. DataLoader構築

GalaxyDatasetをPyTorch Datasetへ移行。

DataLoaderによるバッチ読み込みに成功。

確認結果

dict_keys([
    'id',
    'image',
    'label'
])

これにより学習用データパイプラインが完成した。

### 9. ResNet18接続確認

ResNet18を導入。

入力画像を1チャネル対応へ変更。

入力

torch.Size([4, 1, 100, 100])

出力

torch.Size([4, 4])

を確認。

画像から4ラベルを出力するネットワークを構築した。

学習ループ実装前の最終確認が完了した。

### 評価

画像読込・Dataset作成・PyTorch導入まで完了。

学習ループ実装前の最終確認が完了した。

## Day2 (2026-10-28)

### 目的

教師データを用いてResNet18による銀河形態分類AIを構築し、
学習および性能評価を実施する。

### 実施内容

#### 1. Dataset構築

前日に作成したGalaxyDatasetを利用し、
PyTorch学習用データセットとして運用した。

入力画像

100 × 100 pixel

対象ラベル

- Detectable
- Bright Neighbor
- Multiple Component
- Point Source

#### 2. Train / Test 分割

教師データ347件を

Train : 277件
Test  : 70件

へ分割した。

分割比

80 : 20

#### 3. ResNet18実装

ResNet18を利用した分類モデルを構築した。

変更点

入力チャネル

3 → 1

出力ユニット数

1000 → 4

対応ラベル

- Detectable
- Bright Neighbor
- Multiple Component
- Point Source

#### 4. 学習ループ実装

損失関数

BCEWithLogitsLoss

最適化手法

Adam

を導入した。

以下の処理が正常に動作することを確認した。

Forward
↓
Loss計算
↓
Backward
↓
Optimizer更新

#### 5. 学習実行

学習条件

Epoch : 5
Batch Size : 4

学習結果

Epoch 1 : 0.6006
Epoch 2 : 0.5513
Epoch 3 : 0.5233
Epoch 4 : 0.4905
Epoch 5 : 0.5029

全体としてLossの低下を確認した。

#### 6. Testデータによる性能評価

学習に使用していない70件の銀河画像を用いて評価を実施した。

結果

Detectable         : 85.7%

Bright Neighbor    : 74.3%

Multiple Component : 52.9%

Point Source       : 72.9%

#### 7. 学習済みモデル保存

学習済みモデル

resnet18_f277w.pth

の保存に成功した。

保存先

models/

#### 8. 誤分類サンプル抽出

Testデータに対して誤分類サンプルの抽出を実施した。

代表例

ID=1173943

True:
[1,1,0,0]

Pred:
[1,0,1,0]

など、

Bright Neighbor
↓
Multiple Component

への誤分類が多数確認された。

### 重要な発見

誤分類サンプルを目視確認した結果、
Bright NeighborとMultiple Componentが混同される傾向が確認された。

代表例としてID=1173943およびID=915248では、
R80外側に独立した明るい成分が存在しており、
Bright Neighborと判定した根拠は妥当と考えられた。

一方、

ID=686553
ID=572195
ID=1161956

などについては、

F277W画像では明るい構造が見えるものの、

OBJ画像
ASY画像

では独立成分として確認できなかった。

そのため、

Bright Neighbor : 1

ではなく、

Detectableのみ

と再判定すべき可能性があることが分かった。

### 考察

今回の誤分類の一部は、
AIモデルの性能不足だけでなく、
教師ラベルの一貫性の問題を反映している可能性がある。

特にBright Neighborの判定については、

F277W画像で見える構造

と

OBJ・ASY画像で独立成分として確認できる構造

を区別する必要があることが分かった。

今後は、

- 誤分類天体の再確認
- Bright Neighborラベルの再点検
- ラベル品質の向上

を進める予定である。

### 評価

ResNet18による銀河形態分類AIの初期版構築に成功した。

347件の教師データを用いた学習および評価環境を構築し、
未知データに対する性能評価まで実施できた。

また、誤分類解析を通じて、
モデル性能だけでなく教師ラベル自体の課題を発見することができた。

### 9. 誤分類CSV自動出力機能の実装

誤分類天体の再確認作業を効率化するため、
誤分類結果をCSVへ自動保存する機能を実装した。

出力内容

- id
- true
- pred

保存形式

misclassified_YYYYMMDD.csv

例

misclassified_20261028.csv

保存先

data/

これにより誤分類天体を一覧化し、
後からWebアプリ上で確認できる基盤を整備した。

### 10. 教師データ自動切替機能の実装

教師データの更新に伴い、
コード内の日付を毎回書き換える必要があったため、
最新版CSVを自動取得する仕組みを導入した。

実装内容

config.py を作成し、

morphology_labels_*.csv

の中から最新ファイルを自動選択するよう変更した。

実行時表示例

Using CSV: morphology_labels_20261028.csv

これにより、

morphology_labels_20261027.csv
↓
morphology_labels_20261028.csv
↓
morphology_labels_20261029.csv

と教師データを更新しても、
train.py や predict.py を修正する必要がなくなった。

### 11. 誤分類サンプル再確認

AIが誤分類したサンプルについて、
F277W・OBJ・ASY画像を用いて再確認を実施した。

確認対象

誤分類上位10天体

確認結果

AIの誤判定 : 6件

教師ラベル再検討候補 : 4件

と判定した。

特に一部の天体については、

F277Wでは明るい構造が見えるが、
OBJおよびASYでは独立成分として確認できない

ケースが存在した。

そのため、

Bright Neighbor

として登録していたラベルの一部は、

Detectableのみ

へ変更すべき可能性があることが分かった。

### 重要な発見

AIの誤分類解析を通じて、
モデル性能だけでなく教師データ品質の課題を発見した。

誤分類上位10件のうち、

40%

について教師ラベルの再検討余地が存在した。

この結果から、

現在の性能評価はAIモデル性能だけでなく、
教師データ品質にも依存していることが示唆された。

AIを利用することで、
人間が見落としていたラベルの不整合を効率的に発見できる可能性が確認された。

### 再学習結果

修正版教師データ

morphology_labels_20261028.csv

を用いて再学習を実施した。

学習結果

Epoch 1 : 0.5626
Epoch 2 : 0.5010
Epoch 3 : 0.4978
Epoch 4 : 0.4779
Epoch 5 : 0.4535

Test Accuracy

Detectable         : 90.0%

Bright Neighbor    : 68.6%

Multiple Component : 72.9%

Point Source       : 77.1%

誤分類数

52件

### 評価

教師データの見直しと再学習のサイクルを構築した。

また、

AI
↓
誤分類抽出
↓
人間による再確認
↓
教師データ修正
↓
再学習

という継続的改善フローを確立した。

これにより、
AIモデルの性能向上だけでなく、
教師データ品質向上も同時に進められる体制を整備した。

## Day3 (2026-10-29)

### 目的

AI分類器の改善および、人間の分類時に利用している情報と同等の入力をAIへ与えるための改良を実施する。

また、誤分類解析を通して教師データ品質の検証を行う。

### 実施内容

#### 1. 誤分類CSV自動出力機能の実装

誤分類サンプルをCSVとして自動保存する機能を実装した。

出力内容

- id
- true
- pred

保存形式

misclassified_YYYYMMDD.csv

例

misclassified_20261028.csv

保存先

data/

これにより、誤分類サンプルの確認作業を効率化した。

#### 2. 教師データ自動切替機能の実装

教師データを更新するたびにコードを書き換える必要があったため、

morphology_labels_*.csv

の中から最新ファイルを自動取得する仕組みを実装した。

実行時表示例

Using CSV: morphology_labels_20261028.csv

これにより、

morphology_labels_20261027.csv
↓
morphology_labels_20261028.csv
↓
morphology_labels_20261029.csv

と更新した場合でも、コード修正が不要となった。

#### 3. 誤分類サンプル再確認

誤分類上位10天体について再確認を実施した。

結果

AIの誤判定     : 6件

教師ラベル修正 : 4件

であった。

一部の天体については、

F277Wでは明るい構造が見えるが、

OBJおよびASYでは独立成分として確認できない

ケースが存在した。

この結果から、一部ラベルに再検討の余地があることが確認された。

#### 4. 教師データ修正

誤分類解析結果を反映し、

morphology_labels_20261028.csv

を作成した。

修正対象は主に

- Bright Neighbor
- Detectable

の境界的な天体である。

#### 5. F277W + OBJ + ASY の3チャネル化

従来は

F277Wのみ

を入力としていた。

入力形状

torch.Size([1,100,100])

を

F277W
OBJ
ASY

の3チャネル構成へ変更した。

変更後

torch.Size([3,100,100])

を確認した。

これにより、人間が分類時に利用している情報と同等の入力構成を実現した。

#### 6. ResNet18の3チャネル対応

1チャネル入力用に変更していたResNet18を標準構成へ戻した。

従来

Conv2d(
    in_channels=1
)

変更後

Conv2d(
    in_channels=3
)

とした。

#### 7. 20 Epoch学習

学習条件

Epoch : 20

Batch Size : 4

学習結果

Epoch 1  : 0.5706
Epoch 2  : 0.5091
Epoch 3  : 0.4869
Epoch 4  : 0.4761
Epoch 5  : 0.4486
Epoch 6  : 0.4394
Epoch 7  : 0.4381
Epoch 8  : 0.4241
Epoch 9  : 0.3981
Epoch 10 : 0.3836
Epoch 11 : 0.3868
Epoch 12 : 0.3526
Epoch 13 : 0.3281
Epoch 14 : 0.2953
Epoch 15 : 0.2879
Epoch 16 : 0.2785
Epoch 17 : 0.2229
Epoch 18 : 0.2011
Epoch 19 : 0.1621
Epoch 20 : 0.1965

Lossの大幅な低下を確認した。

#### 8. Test Accuracy

評価データ70件に対して性能評価を実施した。

結果

Detectable         : 85.7%

Bright Neighbor    : 67.1%

Multiple Component : 65.7%

Point Source       : 71.4%

誤分類数

49件

### 重要な発見

F277Wのみの入力から、

F277W + OBJ + ASY

の3チャネル入力へ変更したが、

現時点では大きな精度向上は確認されなかった。

一方で、誤分類解析を通じて教師ラベル側にも改善余地があることが確認された。

AIは単なる分類器としてだけでなく、

教師データ品質を確認するための支援ツール

としても有効であることが分かった。

### 評価

AI分類器の基本構築は完了した。

現在は、

AI
↓
誤分類抽出
↓
人間による再確認
↓
教師データ修正
↓
再学習

という継続的改善サイクルを構築できている。

また、人間が分類時に利用している

F277W
OBJ
ASY

をすべて入力として利用する環境を整備した。

### 12. predict.py実装

任意の銀河IDに対してAI予測を実行する推論機能を実装した。

実行例

python predict.py 476630

出力

Detectable
Bright Neighbor
Multiple Component
Point Source

それぞれについて確率値を取得できることを確認した。

### 13. predict_all.py実装

教師データ全件に対してAI推論を実行し、

prediction.csv

として保存する機能を実装した。

出力内容

- id
- detectable
- bright_neighbor
- multiple_component
- point_source

この機能により、
大量天体に対する自動分類基盤を構築した。

### 14. Human-in-the-Loop Web Inspector改良

既存のLAE Morphology Inspectorを改良し、
AIの推論結果を分類支援に利用できる環境を整備した。

追加機能

- AI予測確率表示
- AI予測バー表示
- Uncertainモード
- 前回判定表示
- 前回判定との差分表示
- 同一判定時の保存スキップ
- LAE / SF / Q 推論結果切替

AI予測については、

Detectable
Bright Neighbor
Multiple Component
Point Source

の4ラベルそれぞれについて確率表示を実装した。

また、

前回判定
現在判定
AI予測

を同時表示できるインターフェースを構築した。

これにより、
Human-in-the-Loopによるラベル再確認作業を効率化した。


### 15. Uncertainサンプル抽出機能

AI予測確率が0.5付近となる天体を

Uncertain

として抽出する機能を実装した。

判定基準

min(|p - 0.5|) < 0.10

出力ファイル

- uncertain.csv

この機能により、
AIが自信を持てないサンプルのみを優先的に確認できる環境を構築した。


### 16. SF銀河3394天体への一括推論

LAE教師データで学習した1028モデルを用いて、
非LAE Star Forming銀河へ推論を実施した。

対象

SF銀河

3394天体

欠損データ

- ID 718922
- ID 1103622

は除外した。

生成ファイル

- sf_inference.csv
- prediction_SF.csv
- uncertain_SF.csv

推論結果

Detectable         : 3252 (95.8%)

Bright Neighbor    : 506 (14.9%)

Multiple Component : 819 (24.1%)

Point Source       : 714 (21.0%)

Uncertain          : 764 (22.5%)

総天体数           : 3394

これにより、
LAE教師データを用いて学習したモデルを
大量のSF銀河へ適用可能であることを確認した。


### 17. Q銀河への一括推論

Q銀河に対しても
SFと同様の推論環境を構築した。

追加ファイル

- q_inference.csv
- config_q.py
- predict_q.py

生成ファイル

- prediction_Q.csv
- uncertain_Q.csv

これにより

LAE
SF
Q

すべてに対して同一モデルによる推論が可能となった。


### 重要な発見

当初の目的であった、

LAEで教師データ作成
↓
AI学習
↓
大量のSF銀河へ適用

という流れを実現した。

特に、

SF銀河3394天体

に対して推論を実施し、

Uncertainサンプル

764天体

まで絞り込めた。

これは、

3394件
↓
764件

となり、

人間が確認すべき対象を約77.5%削減

できることを示している。


### 評価

AIモデル単体の開発だけでなく、

AI
↓
推論
↓
Uncertain抽出
↓
人間確認

というHuman-in-the-Loop環境を構築できた。

また、

LAE
SF
Q

すべてを同一Webアプリ上で扱える統合環境を整備した。

今後は、

- Uncertainサンプル再確認
- SF/Qラベル追加
- 半教師あり学習
- 再学習

を進める予定である。
