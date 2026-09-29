# クイックリファレンス

**5分で始めたい人向けの最小限ガイド**

---

## インストール

```bash
pip install matplotlib numpy
```

---

## Phase 1 を実行（蛇がくねくね）

```bash
python3 phase1_basic.py
```

**何が見えるか**：
- 蛇が固定位置でくねくね動く
- 波が頭から尾へ流れる
- でも移動しない（摩擦がないため）

---

## Phase 2 を実行（蛇が前進）

```bash
python3 phase2_with_friction.py
```

**何が見えるか**：
- Phase 1 と同じ蛇が移動している
- 波を作りながら右上へ前進
- 摩擦の効果で前進が生まれる

---

## 数学を学ぶ

```bash
# 1. sin/cos を学ぶ（15分）
cat 01_high_school_math.md

# 2. FK を学ぶ（20分）
cat 02_kinematics_explained.md

# 3. 摩擦を学ぶ（15分）
cat 03_physics_explained.md
```

---

## コンポーネント一覧

| ファイル | 役割 | 入力 | 出力 |
|---------|------|------|------|
| `components/cpg.py` | 脳 | time | activation(-1~1) |
| `components/kinematics.py` | 関節→位置 | joint angles | positions |
| `components/friction.py` | 摩擦 | positions | friction forces |

---

## よく使うコード

### 筋肉活動を作る

```python
from components.cpg import get_muscle_activation

activation = get_muscle_activation(
    num_joints=30,
    amplitude=1.0,
    frequency=2.0,    # Hz（高いほど速い）
    wavelength=4.0,   # 関節数（小さいほど短い波）
    time=0.0
)
# → [-1.0 ~ 1.0] の値 30個
```

### 角度から位置を計算

```python
from components.kinematics import forward_kinematics

positions = forward_kinematics(
    joint_angles=[10, 20, 15, ...],
    segment_length=10.0,
    start_pos=(0, 0)
)
# → [(x0, y0), (x1, y1), ...] の座標
```

### 摩擦力を計算

```python
from components.friction import compute_friction_forces

fx, fy = compute_friction_forces(
    positions=[(x0, y0), ...],
    segment_directions=[(ux0, uy0), ...],
    c_forward=1.0,     # 前後は滑りやすい
    c_lateral=10.0     # 左右は滑りにくい
)
# → 総摩擦力 (fx, fy)
```

---

## パラメータを変えて実験

### 速い蛇

```python
simulator.frequency = 3.0      # 高周波数
simulator.wavelength = 3.0     # 短い波
```

### ゆっくりした蛇

```python
simulator.frequency = 0.5      # 低周波数
simulator.wavelength = 6.0     # 長い波
```

### 摩擦を強くする

```python
simulator.c_lateral = 20.0     # 横をもっと滑りにくく
```

### 摩擦を弱くする

```python
simulator.c_lateral = 5.0      # 横を少し滑りやすく
```

---

## テスト

```bash
# 非ビジュアル版テスト
python3 test_phase1.py

# モジュール単体テスト
python3 -c "from components.cpg import get_muscle_activation; print(get_muscle_activation(10, time=0))"
```

---

## ファイル構成（最重要）

```
.
├── 01_high_school_math.md      ← sin/cos を学ぶ
├── 02_kinematics_explained.md  ← FK を学ぶ
├── 03_physics_explained.md     ← 摩擦を学ぶ
├── phase1_basic.py             ← 実行：蛇がくねくね
├── phase2_with_friction.py     ← 実行：蛇が前進
└── components/
    ├── cpg.py                  ← 脳
    ├── kinematics.py           ← FK
    └── friction.py             ← 摩擦
```

---

## トラブルシューティング

### Q: `ModuleNotFoundError: No module named 'matplotlib'`

```bash
pip install matplotlib
```

### Q: 蛇が動かない

1. `phase1_basic.py` で動いているか確認
2. `test_phase1.py` が成功しているか確認
3. パラメータの値を確認

```python
# 確実に動く設定
amplitude = 1.0
frequency = 2.0
wavelength = 4.0
c_forward = 1.0
c_lateral = 10.0   # ← これが重要！
```

### Q: アニメーションが遅い

matplotlib は遅いです。

- Phase 1: ~5秒で 0.5秒分のシミュレーション
- Phase 2: ~10秒で 0.8秒分のシミュレーション

実装上の改善策：
- Cython で計算を最適化
- NumPy を活用
- より高速な描画ライブラリを使う

---

## 次のステップ

### 1段階：理解する
1. `01_high_school_math.md` を読む
2. `phase1_basic.py` を実行
3. コードを読む

### 2段階：実験する
1. `examples/` のスクリプトを実行
2. パラメータを変える
3. 結果を観察

### 3段階：拡張する
1. Phase 3 を実装（筋肉の詳細モデル）
2. 障害物を加える
3. 3D 版を作る

---

## リンク集

| 項目 | ファイル |
|------|---------|
| プロジェクト概要 | `README.md` |
| クイックスタート | `00_QUICK_START.md` |
| 高校数学解説 | `01_high_school_math.md` |
| FK 解説 | `02_kinematics_explained.md` |
| 物理解説 | `03_physics_explained.md` |
| 実装詳細 | `IMPLEMENTATION_SUMMARY.md` |
| このファイル | `QUICK_REFERENCE.md` |

---

## 覚えるべき式（3つだけ）

### 1. 筋肉活動（CPG）

```
activation[i] = amplitude * sin(i * 2π/wavelength - time * 2π * frequency)
```

### 2. 関節角

```
angle[i] = (left[i] - right[i]) * max_bend
```

### 3. 順運動学（FK）

```
θ_abs = θ_abs + angle[i]
x = x + L * cos(θ_abs)
y = y + L * sin(θ_abs)
```

---

## 最後に

この実装は **「学習用」** です。

- 使いやすさ重視
- 拡張性重視
- 研究用の最適化は後回し

わからないことがあったら、対応する `.md` ファイルを読んでください。

全て「高校数学で理解できる」レベルで書いてあります。
