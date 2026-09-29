# 実装サマリー：蛇シミュレーション

このドキュメントは、作成された実装の構造と、各コンポーネントの役割をまとめています。

---

## 📐 システムアーキテクチャ

```
┌────────────────────────────────────────────────┐
│  Central Pattern Generator (CPG)               │
│  脳から来る「筋肉を動かせ」という指令         │
│  components/cpg.py                            │
└─────────────────┬──────────────────────────────┘
                  ↓
          activation: [-1.0 ~ 1.0]
                      [a0, a1, ..., a29]
                  ↓
┌─────────────────────────────────────────────────┐
│  Muscle Model                                   │
│  活性度を左右の筋肉に分ける                     │
│  components/kinematics.py (split_into_lr)      │
└─────────────────┬───────────────────────────────┘
                  ↓
         left_activation, right_activation
                  ↓
┌─────────────────────────────────────────────────┐
│  Joint Angle Controller                        │
│  左右の筋肉活動から関節角を計算                 │
│  components/kinematics.py                      │
│  (get_joint_angles_from_activation)            │
└─────────────────┬───────────────────────────────┘
                  ↓
         joint_angles: [q0, q1, ..., q29] (degrees)
                  ↓
┌─────────────────────────────────────────────────┐
│  Forward Kinematics (FK)                        │
│  関節角から体の形を計算                         │
│  components/kinematics.py (forward_kinematics) │
└─────────────────┬───────────────────────────────┘
                  ↓
         positions: [(x0,y0), (x1,y1), ..., (x29,y29)]
                  ↓
┌─────────────────────────────────────────────────┐
│  Segment Directions                            │
│  各セグメントの向きを計算                       │
│  components/kinematics.py                      │
│  (compute_segment_directions)                  │
└─────────────────┬───────────────────────────────┘
                  ↓
         directions: [(dx0,dy0), ...]
                  ↓
┌─────────────────────────────────────────────────┐
│  Anisotropic Friction Model                    │
│  地面から蛇が受ける摩擦力を計算                │
│  components/friction.py                        │
└─────────────────┬───────────────────────────────┘
                  ↓
     friction_forces: (fx_total, fy_total)
                  ↓
┌─────────────────────────────────────────────────┐
│  Snake Position Update                         │
│  蛇全体を移動させる                            │
│  Phase 2 でのみ使用                            │
└─────────────────────────────────────────────────┘
                  ↓
            蛇が前進！
```

---

## 🧬 各モジュールの詳細

### 1. `components/cpg.py` - Central Pattern Generator

**役割**：周期的な筋肉活動の波を生成する（脳）

**主な関数**：

#### `get_muscle_activation()`
```python
activation = get_muscle_activation(
    num_joints=30,
    amplitude=1.0,
    frequency=2.0,      # Hz
    wavelength=4.0,     # 関節数
    time=0.0            # 秒
)
# → [-1.0 ~ 1.0] の値 30個
```

**式**：
```
activation[i] = amplitude * sin(i * 2π/wavelength - time * 2π * frequency)
```

**意味**：
- `i * 2π/wavelength` ： 関節ごとに位相をずらす
- `time * 2π * frequency` ： 時間とともに波が移動

#### `split_into_left_right()`
```python
left, right = split_into_left_right(activation)
# left[i]  = max(0, activation[i])
# right[i] = max(0, -activation[i])
```

**意味**：活性度を左筋肉と右筋肉に分ける
- activation[i] > 0 なら左筋肉が優位
- activation[i] < 0 なら右筋肉が優位

---

### 2. `components/kinematics.py` - Kinematics

**役割**：関節角から体の形を計算（FK）

#### `get_joint_angles_from_activation()`
```python
joint_angles = get_joint_angles_from_activation(
    left_activation,
    right_activation,
    max_bend=30.0  # 度数法
)
# → [-30.0 ~ 30.0] 度の値 30個
```

**式**：
```
angle[i] = (left[i] - right[i]) * max_bend
```

**意味**：左右の筋肉の差を角度に変換

#### `forward_kinematics()`
```python
positions = forward_kinematics(
    joint_angles=[q0, q1, ..., q29],
    segment_length=10.0,
    start_pos=(0, 0),
    start_angle=0.0
)
# → [(x0, y0), (x1, y1), ..., (x29, y29)]
```

**アルゴリズム**：
```python
x, y = start_pos
theta = start_angle

for q in joint_angles:
    theta += q                              # 絶対角度を更新
    x += segment_length * cos(radians(theta))
    y += segment_length * sin(radians(theta))
    positions.append((x, y))
```

**意味**：
- 各セグメントで方向を更新
- その方向に `segment_length` だけ移動
- 次のセグメントの開始位置とする

#### `compute_segment_directions()`
```python
directions = compute_segment_directions(positions)
# → [(ux0, uy0), (ux1, uy1), ...] (単位ベクトル)
```

**意味**：各セグメント（点から点への矢印）の向きベクトル

**用途**：摩擦計算で「前後」「左右」の成分を分けるのに使う

---

### 3. `components/friction.py` - Friction Model

**役割**：異方性摩擦から蛇全体の移動を計算

#### `compute_friction_forces()`
```python
fx_total, fy_total = compute_friction_forces(
    positions,
    segment_directions,
    c_forward=1.0,
    c_lateral=10.0
)
```

**原理**：

蛇の各セグメントは、地面との接触点で摩擦を受けます。

```
蛇が左に動こうとする
  ↓
地面が横方向に強く反発する（c_lateral が大きい）
  ↓
横への動きが阻止される

一方、蛇が前に動こうとする
  ↓
地面が前方向に弱く反発する（c_forward が小さい）
  ↓
前への動きが許される
```

複数のセグメントが波を作るとき：
- 左右の力が打ち消し合う
- 前後の力だけが残る
- **結果：前進！**

#### `update_snake_position()`
```python
dx, dy = update_snake_position(
    positions,
    friction_forces=(fx, fy),
    mass=1.0,
    dt=0.1
)
```

**式**（ニュートン力学）：
```
加速度 a = f / m
移動量 Δx ∝ a * dt²
```

---

## 🔄 実装のフロー

### Phase 1（固定位置版）

```
for each timestep:
    activation = CPG(time)
    left, right = split(activation)
    angles = activation_to_angles(left, right)
    positions = FK(angles)
    
    表示する
    time += dt
```

**特徴**：
- 蛇の頭は (0, 0) に固定
- 蛇は形を変えるが位置は変わらない
- FK だけで十分
- **ファイル**: `phase1_basic.py`

### Phase 2（移動版）

```
for each timestep:
    activation = CPG(time)
    left, right = split(activation)
    angles = activation_to_angles(left, right)
    positions = FK(angles, start_pos=(snake_x, snake_y))
    directions = compute_directions(positions)
    
    fx, fy = friction(positions, directions)
    dx, dy = calc_movement(fx, fy)
    
    snake_x += dx
    snake_y += dy
    
    表示する
    time += dt
```

**特徴**：
- 異方性摩擦を加える
- 蛇が前進する
- フィードバックループあり
  - 蛇の位置が変わる
  - → 次のステップの FK が異なる
  - → 摩擦力が変わる
- **ファイル**: `phase2_with_friction.py`

---

## 📊 パラメータの意味と効果

| パラメータ | 値 | 効果 |
|-----------|-----|------|
| `amplitude` | 0.5～1.0 | 筋肉活動の大きさ（大きいほど大きく動く） |
| `frequency` | 0.5～3.0 Hz | 波が進む速さ（高いほど速くくねくね） |
| `wavelength` | 2.0～8.0 | 波の長さ（小さいほど短い波） |
| `max_bend` | 20～40 度 | 最大曲がり角（大きいほど大きく曲がる） |
| `c_forward` | 0.5～2.0 | 前後方向の摩擦係数（小さいほど滑りやすい） |
| `c_lateral` | 5.0～20.0 | 左右方向の摩擦係数（大きいほど滑りにくい） |

**重要**：
```
c_lateral > c_forward
```

この条件がないと、蛇は前進できません。

---

## 🧪 テスト

### 単体テスト

```bash
# CPG のテスト
python3 -c "from components.cpg import get_muscle_activation; print(get_muscle_activation(5, time=0))"

# FK のテスト
python3 -c "from components.kinematics import forward_kinematics; print(forward_kinematics([10]*5))"

# 摩擦のテスト
python3 -c "from components.friction import compute_friction_forces; print(compute_friction_forces([(10,0)], [(1,0)]))"
```

### 統合テスト

```bash
# Phase 1 の非ビジュアル版テスト
python3 test_phase1.py

# Phase 1 のビジュアル版（要 matplotlib）
python3 phase1_basic.py

# Phase 2 のビジュアル版（要 matplotlib）
python3 phase2_with_friction.py
```

---

## 🎯 重要な設計決定

### 1. モジュール分割

**なぜ？** 各層の責任を明確にして、テストと拡張を容易にする

```
CPG     → 脳（何をするかを決める）
Muscle  → 筋肉（活性度から力を作る）
FK      → 骨格系（力から形を作る）
Friction → 環境（環境との相互作用）
```

### 2. 2D に限定

**なぜ？** 3D は実装が複雑。2D で基本原理を学んでから 3D へ

### 3. 簡潔な摩擦モデル

**なぜ？** 複雑な接触力学は不要。

異方性摩擦だけで、蛇行による前進が再現できます。

### 4. 正規化された値

**なぜ？** `-1.0 ~ 1.0` の値に統一して、スケーリングを単純化

---

## 🚀 拡張の方向

### Phase 3: 筋肉の詳細モデル

現在：
```
activation → joint_angle
```

拡張：
```
activation → muscle_force → joint_torque → joint_acceleration → joint_angle
```

**ファイル**：`components/muscle.py` (未実装)

### Phase 4: 環境との相互作用

現在：
- 地面の摩擦だけ

拡張：
- 障害物との接触
- 傾斜地面
- 液体（水での動き）

### Phase 5: 神経の学習

現在：
- CPG のパラメータは手で設定

拡張：
- 神経ネットワークで CPG を学習
- 環境への適応行動を獲得

---

## 📈 性能・スケーラビリティ

現在の実装：

| 項目 | 値 |
|------|-----|
| 関節数 | 30（可変） |
| シミュレーション時間ステップ | 0.01～0.1 s |
| 計算フレームレート | ~100-1000 Hz（マシン依存） |
| ビジュアル表示 | 30 fps（matplotlib） |

**制限**：
- matplotlib は遅い（large-scale simulation 向けではない）
- 高速シミュレーションには Cython や CUDA への最適化が必要

---

## 📝 コードスタイル

### 命名規則

- **関数**：`snake_case`
- **クラス**：`PascalCase`
- **定数**：`UPPER_CASE`
- **プライベート**：`_leading_underscore`

### ドキュメント

各関数には以下を含む：
- **Docstring**：何をするのか
- **Parameters**：入力パラメータ
- **Returns**：戻り値
- **説明**：数式や原理
- **例**：使い方

---

## 🔍 デバッグのコツ

### 蛇が動かないとき

1. **摩擦係数を確認**
   ```python
   assert simulator.c_lateral > simulator.c_forward
   ```

2. **波が生成されているか確認**
   ```python
   activation = get_muscle_activation(30, time=0)
   print(activation)  # -1.0 ~ 1.0 の値が見えるか？
   ```

3. **FK が正しく動いているか確認**
   ```python
   angles = [30] * 10 + [0] * 20
   positions = forward_kinematics(angles)
   # 最後のセグメントが右へオフセットしているか？
   ```

### 蛇が期待と違う動きをするとき

1. パラメータを一つずつ変える
2. その時だけビジュアルで確認
3. 別のパラメータに移る

**重要**：一度に複数を変えてはいけない

---

まとめ：

この実装は **「最小限で動く蛇シミュレータ」** です。

- 十分リアル（蛇が本当に前進する）
- 十分シンプル（理解・拡張が容易）
- 十分教育的（原理が透ける）

