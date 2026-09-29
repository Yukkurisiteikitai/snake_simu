"""
Central Pattern Generator (CPG)
脳から来る「筋肉活動の波」を生成するモジュール

学べることは：
- sin() を使って周期的な信号を作る
- 時間とともに波が移動する原理
"""

import math


def get_muscle_activation(num_joints: int,
                         amplitude: float = 1.0,
                         frequency: float = 1.0,
                         wavelength: float = 4.0,
                         time: float = 0.0) -> list:
    """
    CPG からの出力：各関節での筋肉活動を計算する。

    Parameters:
    -----------
    num_joints : int
        蛇の関節数（例：30）

    amplitude : float
        筋肉活動の大きさ（0～1、正規化されている）

    frequency : float
        波が進む速さ（高いほど速くくねくね）

    wavelength : float
        波が長いか短いか（低いほど短い波）

    time : float
        現在の時刻（秒）

    Returns:
    --------
    list
        [a0, a1, a2, ..., a_{num_joints-1}]
        各関節での筋肉活動（-1 ～ 1）

    使い方の例：
    -----------
    >>> activation = get_muscle_activation(30, amplitude=0.8,
    ...                                    frequency=2.0, time=0.0)
    >>> print(activation[0])  # 関節0の活動量
    0.6532...  # sin(0) の結果

    高校数学でのポイント：
    - sin(θ) は周期 2π で同じ値を繰り返す
    - θ = i * (2π/wavelength) - time * frequency
    を計算することで、「時間とともに進む波」を作る
    """

    activation = []

    for i in range(num_joints):
        # 関節 i での phase（位相）を計算
        # i * (2*pi / wavelength)  ← 関節ごとに位相をずらす
        # time * frequency          ← 時間とともに位相が進む

        phase = (i * 2 * math.pi / wavelength) - (time * 2 * math.pi * frequency)

        # sin() を使って、-amplitude ～ +amplitude の値を作る
        a = amplitude * math.sin(phase)

        activation.append(a)

    return activation


def split_into_left_right(activation: list) -> tuple:
    """
    筋肉活動を左右に分ける（対立筋制御）。

    蛇は左の筋肉と右の筋肉を交互に収縮させることで、
    体を左右に曲げます。

    Parameters:
    -----------
    activation : list
        get_muscle_activation() の出力

    Returns:
    --------
    (left, right)
        left  : [l0, l1, ..., l_{n-1}]  左筋肉の活性度
        right : [r0, r1, ..., r_{n-1}]  右筋肉の活性度

    原理：
    ------
    activation が [0, 0.7, 0.3, -0.5, ...]

    これを左右に分けると：
    - activation > 0 なら左が優位
    - activation < 0 なら右が優位

    具体的には：
    left[i]  = max(0, activation[i])      （負にはならない）
    right[i] = max(0, -activation[i])     （負にはならない）

    例：
    activation[i] = 0.7
    → left[i] = 0.7, right[i] = 0

    activation[i] = -0.5
    → left[i] = 0, right[i] = 0.5
    """

    left = []
    right = []

    for a in activation:
        # 負にならないようにする（活性度は ≥ 0）
        left.append(max(0, a))
        right.append(max(0, -a))

    return left, right


if __name__ == "__main__":
    # デモ：CPG の出力を見る
    print("=== CPG デモ ===\n")

    # Phase 1: 時刻 t=0 での筋肉活動
    activation_t0 = get_muscle_activation(
        num_joints=10,
        amplitude=1.0,
        frequency=1.0,
        wavelength=4.0,
        time=0.0
    )

    print("時刻 t=0 での各関節の筋肉活動：")
    for i, a in enumerate(activation_t0):
        print(f"  関節{i}: {a:+.3f}")

    # Phase 2: 時刻 t=0.1 での筋肉活動
    activation_t01 = get_muscle_activation(
        num_joints=10,
        amplitude=1.0,
        frequency=1.0,
        wavelength=4.0,
        time=0.1
    )

    print("\n時刻 t=0.1 での各関節の筋肉活動：")
    for i, a in enumerate(activation_t01):
        print(f"  関節{i}: {a:+.3f}")

    print("\n※ 時刻が進むと、波が後ろへ移動するのがわかります。")

    # Phase 3: 左右に分ける
    left, right = split_into_left_right(activation_t0)

    print("\n時刻 t=0 での左右の筋肉活動：")
    for i in range(10):
        print(f"  関節{i}: 左={left[i]:+.3f}  右={right[i]:+.3f}")
