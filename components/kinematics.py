"""
Forward Kinematics (FK)
関節角から蛇の体の形を計算するモジュール

学べることは：
- 関節角から位置を計算する
- 順運動学の原理
- sin/cos の使い方
"""

import math


def get_joint_angles_from_activation(left_activation: list,
                                     right_activation: list,
                                     max_bend: float = 30.0) -> list:
    """
    筋肉活動から関節角を計算する。

    Parameters:
    -----------
    left_activation : list
        [l0, l1, ..., l_{n-1}]  左筋肉の活性度

    right_activation : list
        [r0, r1, ..., r_{n-1}]  右筋肉の活性度

    max_bend : float
        最大曲がり角（度数法、例：30度）

    Returns:
    --------
    list
        [q0, q1, ..., q_{n-1}]  各関節の曲がり角（度数法）

    原理：
    ------
    左筋肉 > 右筋肉 なら → 左に曲がる（正の角度）
    右筋肉 > 左筋肉 なら → 右に曲がる（負の角度）

    例：
    left[i] = 0.8, right[i] = 0.3
    → 差 = 0.8 - 0.3 = 0.5
    → 角度 = 0.5 * max_bend = 0.5 * 30 = 15度（左に曲がる）
    """

    assert len(left_activation) == len(right_activation), \
        "左右の活性度リストの長さが一致していません"

    joint_angles = []

    for l, r in zip(left_activation, right_activation):
        # 左右の活性度の差を計算
        diff = l - r

        # 差を角度に変換（-max_bend ～ +max_bend）
        angle = diff * max_bend

        joint_angles.append(angle)

    return joint_angles


def forward_kinematics(joint_angles: list,
                       segment_length: float = 10.0,
                       start_pos: tuple = (0, 0),
                       start_angle: float = 0.0) -> list:
    """
    関節角から蛇の各セグメント先端の位置を計算する。

    Parameters:
    -----------
    joint_angles : list
        [q0, q1, ..., q_{n-1}]  各関節の曲がり角（度数法）

    segment_length : float
        各セグメントの長さ（例：10）

    start_pos : tuple
        蛇の頭の初期位置 (x, y)

    start_angle : float
        蛇の頭の向き（度数法）

    Returns:
    --------
    list
        [(x0, y0), (x1, y1), ..., (x_{n-1}, y_{n-1})]
        各セグメント先端の位置（x, y）

    高校数学での計算方法：
    ---------------------
    角度 θ 方向に距離 L だけ移動すると：

    Δx = L * cos(θ)     ← θが0なら右へ L だけ移動
    Δy = L * sin(θ)     ← θが90度なら上へ L だけ移動

    蛇の場合、各セグメントで方向が変わるので、
    絶対角度を累積していく：

    θ_abs[0] = start_angle + q[0]
    θ_abs[1] = θ_abs[0] + q[1]
    θ_abs[2] = θ_abs[1] + q[2]
    ...

    各位置は：
    x[i+1] = x[i] + segment_length * cos(θ_abs[i])
    y[i+1] = y[i] + segment_length * sin(θ_abs[i])
    """

    positions = []
    x, y = start_pos
    current_angle = start_angle  # 現在の絶対角度（度数法）

    for q in joint_angles:
        # 絶対角度を更新（このセグメントでの曲がり角を加える）
        current_angle += q

        # ラジアンに変換（math.cos/sin はラジアンを使う）
        angle_rad = math.radians(current_angle)

        # その方向に segment_length だけ移動
        x += segment_length * math.cos(angle_rad)
        y += segment_length * math.sin(angle_rad)

        # この位置を記録
        positions.append((x, y))

    return positions


def compute_segment_directions(positions: list) -> list:
    """
    各セグメントの向きベクトルを計算する。

    摩擦計算で使われます。

    Parameters:
    -----------
    positions : list
        FK から得た [(x0, y0), (x1, y1), ...]

    Returns:
    --------
    list
        [(dx0, dy0), (dx1, dy1), ...]
        各セグメントの方向を表す単位ベクトル

    用途：
    ------
    セグメントが「どの方向に向いているか」を知ることで、
    「どの方向への摩擦が大きいか」を計算できます。
    """

    directions = []

    # 蛇の頭は (0, 0) と仮定（FK の start_pos）
    prev_x, prev_y = 0, 0

    for x, y in positions:
        # このセグメント(前のセグメント先端 → このセグメント先端)
        # の方向ベクトルを計算
        dx = x - prev_x
        dy = y - prev_y

        # ベクトルの大きさ
        norm = math.sqrt(dx**2 + dy**2)

        if norm < 1e-6:
            # セグメント長がほぼ 0（不正）
            # → 前のベクトルを使う（フォールバック）
            if directions:
                directions.append(directions[-1])
            else:
                directions.append((1, 0))  # デフォルト
        else:
            # 正規化：単位ベクトル（大きさ 1）にする
            ux = dx / norm
            uy = dy / norm
            directions.append((ux, uy))

        prev_x, prev_y = x, y

    return directions


if __name__ == "__main__":
    # デモ：FK の計算を見る
    print("=== Forward Kinematics デモ ===\n")

    # 簡単な例：関節が3つ、それぞれ5度ずつ左に曲がる
    angles = [5.0, 5.0, 5.0, 0.0, 0.0]

    print(f"関節角: {angles}")
    print(f"セグメント長: 10\n")

    positions = forward_kinematics(angles, segment_length=10.0)

    print("各セグメント先端の位置：")
    for i, (x, y) in enumerate(positions):
        # 距離（原点からどれだけ離れているか）を計算
        dist = math.sqrt(x**2 + y**2)
        print(f"  セグメント{i}: ({x:6.2f}, {y:6.2f})  距離={dist:6.2f}")

    # 波の場合をシミュレート
    print("\n\n=== 波の場合 ===")

    import sys
    sys.path.append('..')
    from components.cpg import get_muscle_activation, split_into_left_right

    # t=0 での筋肉活動から関節角を計算
    activation = get_muscle_activation(
        num_joints=10,
        amplitude=1.0,
        frequency=1.0,
        wavelength=4.0,
        time=0.0
    )

    left, right = split_into_left_right(activation)
    angles = get_joint_angles_from_activation(left, right, max_bend=30.0)

    positions = forward_kinematics(angles, segment_length=10.0)

    print("波を作る場合の各セグメント先端の位置：")
    for i, (x, y) in enumerate(positions):
        dist = math.sqrt(x**2 + y**2)
        print(f"  セグメント{i}: ({x:6.2f}, {y:6.2f})")
