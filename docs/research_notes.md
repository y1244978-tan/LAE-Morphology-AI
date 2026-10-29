# LAE Morphology Research Notes

## LAEの特徴

- SFより小サイズ
- 高EWほどコンパクト
- Qに近い形態を示す

---

## Point Source判定基準

条件

- Detectable
- Neighborなし
- Multipleなし
- r50 ≲ 0.13 arcsec

補助指標

- r80/r50
- ASY残差
- OBJ形状

---

## ASY画像の解釈

ASY
=
Original
-
Rotate180

Point Source
→ 残差が小さい

Multiple
→ 中心付近に複数残差

Neighbor
→ 周辺残差

---

## Human-in-the-Loop方針

LAE教師データ
↓
AI学習
↓
SF/Q推論
↓
Uncertain抽出
↓
人間確認
↓
再学習