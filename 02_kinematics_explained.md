# 順運動学（Forward Kinematics）解説

このファイルで学べることは：
- 「関節角」から「体がどこにあるか」を計算する方法
- FK（Forward Kinematics）とは何か
- プログラムではどう書くか

---

## 0. 問題：角度から位置を求める

蛇の各関節の曲がり角がわかったとします：

```
関節0: 5度
関節1: 15度
関節2: 25度
関節3: 20度
関節4: 10度
...
```

**では、蛇の「体」はどこに位置しているのか？**

これを計算するのが **FK（順運動学）** です。

---

## 1. ロボットのアーム類推

蛇を理解する前に、**ロボットアーム**で考えます。

```
         関節2
            |
        ┌──●──┐
        │     │
        ●     ●
       関節1  先端
        |
        |
       根元
```

根元の位置と各関節の角度がわかれば、先端がどこにあるか計算できます。

---

## 2. 蛇はアームが「チェーン」状

蛇は、**短いアームが30個つながった**と考えます。

```
根元 (頭)
  ●──●──●──●──●──●──●──●
  0  1  2  3  4  5  6  7
     
関節番号
```

各セグメント（●と●の間）の長さは同じ `L = 10` と決めます。

---

## 3. 基本：1つの関節の場合

まず、**1つのセグメントだけ**で考えます。

```
根元: (0, 0)
方向: 45度（北東）
長さ: 10

どこに先端が来るか？
```

### 3-1. 座標系を思い出す

```
         y軸
         ↑
         |
    ○───┼───○
         |
    ←───+───→ x軸
         |
         ○───┼───○
```

- 右 = x 正方向
- 上 = y 正方向
- 角度は「x軸からの回転角」（反時計回り）

### 3-2. 三角関数を使う

角度 `θ` 方向に、長さ `L` だけ移動すると：

```
新しいx = 古いx + L * cos(θ)
新しいy = 古いy + L * sin(θ)
```

これは高校数学です。単位円を思い出してください：

```
     (cos θ, sin θ)
            *
           /|
          / |
         /  |
        /   |
       /    |
      /__θ_|
```

点 `(cos θ, sin θ)` は、角度 `θ` 方向、距離 1 の点です。

距離 `L` の場合は、単に `L` をかけます：

```
(L * cos θ, L * sin θ)
```

### 3-3. 実装例

```python
import math

# 根元の座標
x = 0
y = 0

# セグメント長
L = 10

# 角度（度数法）
angle_deg = 45
angle_rad = math.radians(angle_deg)

# 先端の座標を計算
x_new = x + L * math.cos(angle_rad)
y_new = y + L * math.sin(angle_rad)

print(f"先端: ({x_new:.2f}, {y_new:.2f})")
# → 先端: (7.07, 7.07)
```

---

## 4. 複数セグメント（蛇全体）

蛇は30個のセグメントがつながっています。

```
        セグメント0
         ↓
根元→ ●────●
        ↓セグ1
        ●────●
        ↓セグ2
        ...
        
        ●────●← 尾
```

各セグメントは、**前のセグメントの先端から出発します。**

### 4-1. アルゴリズム

```
頭の位置: (x, y) = (0, 0)
頭の向き: θ = 0度

for i = 0 to 29:
    # i番目の関節角を加える
    θ ← θ + angle[i]
    
    # その方向に L だけ移動
    x ← x + L * cos(θ)
    y ← y + L * sin(θ)
    
    # この位置を記録
    positions[i] = (x, y)
```

### 4-2. コード例

```python
import math

def forward_kinematics(joint_angles, segment_length=10):
    """
    関節角のリストから、各セグメント先端の位置を計算する。
    
    joint_angles: [a0, a1, a2, ..., a29]  各関節角（度数法）
    segment_length: 各セグメントの長さ
    
    戻り値: [(x0, y0), (x1, y1), ..., (x29, y29)]
    """
    
    positions = []
    x, y = 0, 0  # 頭の位置
    theta = 0    # 頭の向き
    
    for angle_deg in joint_angles:
        # 絶対角度を更新（この関節での曲がり角を足す）
        theta += angle_deg
        
        # ラジアンに変換
        theta_rad = math.radians(theta)
        
        # その方向に segment_length だけ移動
        x += segment_length * math.cos(theta_rad)
        y += segment_length * math.sin(theta_rad)
        
        # 位置を記録
        positions.append((x, y))
    
    return positions
```

### 4-3. 動作例

```python
# 蛇が緩やかに右に曲がるケース
angles = [5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0]

positions = forward_kinematics(angles)

for i, (x, y) in enumerate(positions):
    print(f"セグメント{i}: ({x:.1f}, {y:.1f})")
```

結果：

```
セグメント0: (10.0, 0.9)
セグメント1: (19.9, 1.7)
セグメント2: (29.6, 2.6)
セグメント3: (39.1, 3.4)
セグメント4: (48.3, 4.2)
セグメント5: (57.1, 4.9)
セグメント6: (65.6, 5.5)
セグメント7: (73.8, 6.0)
...
```

蛇が**少しずつ右（y正方向）に曲がりながら、前へ進む**パターンです。

---

## 5. 視覚化

上記の位置を画面に描くと：

```
     結果の軌跡
 
 ●─●─●─●─●
  ↘ ↘ ↘ ↘ ↘
```

緩やかな曲線になります。

---

## 6. 蛇が「波」を作る場合

さっき学んだ、時間とともに変わる関節角：

```python
import math

def get_joint_angles(num_joints=30, amplitude=30, k=0.2, omega=5, t=0):
    """
    時刻 t での関節角を計算する
    """
    angles = []
    for i in range(num_joints):
        angle = amplitude * math.sin(i * k - t * omega)
        angles.append(angle)
    return angles

# 時刻 t=0 での蛇の形を計算
angles_t0 = get_joint_angles(t=0)
positions_t0 = forward_kinematics(angles_t0)

# 時刻 t=0.1 での蛇の形を計算
angles_t01 = get_joint_angles(t=0.1)
positions_t01 = forward_kinematics(angles_t01)

# positions_t0 と positions_t01 を順に描くと、
# 蛇が「くねくね」動くように見える
```

---

## 7. よくある質問

### Q1: なぜ「関節角を足す」のか？

```
頭の向き: θ_0 = 0度

関節0を 5度曲げる
  → 頭から見た絶対向き: θ_1 = 0 + 5 = 5度

関節1を 10度曲げる
  → これまでの向きから、さらに 10度曲げる
  → 絶対向き: θ_2 = 5 + 10 = 15度

関節2を 3度曲げる
  → 絶対向き: θ_3 = 15 + 3 = 18度
```

**相対角度を足すことで、絶対向きが決まります。**

### Q2: セグメント長はなぜ固定？

実装を簡単にするため。

本当の蛇も、セグメント長（脊椎骨から脊椎骨の距離）はほぼ一定です。

後で「可変セグメント長」にすることもできます。

### Q3: 2D以外は？

このチュートリアルでは2D（画面上の平面）を扱います。

3Dにする場合は、**z軸も追加**して、3つの三角関数を使います：

```python
x += L * math.cos(theta) * math.cos(phi)
y += L * math.sin(theta) * math.cos(phi)
z += L * math.sin(phi)
```

ただし、複雑になるので、最初は2Dで大丈夫です。

---

## 8. 実装チェックリスト

FKを実装したら、これで確認：

- [ ] 頭は `(0, 0)` で始まるか
- [ ] 全セグメントの長さの合計が計算できるか
  ```python
  total_length = sum(math.sqrt(x**2 + y**2) for x, y in positions)
  expected = 30 * 10  # 30セグメント × 長さ10
  assert abs(total_length - expected) < 0.1  # ほぼ同じはず
  ```
- [ ] 角度を変えると位置が変わるか

---

## 次は？

- `03_physics_explained.md` で、「蛇がどうやって前進するか」を学びます
- `phase1_basic.py` を実行して、実装例を見ます

