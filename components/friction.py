"""
異方性摩擦モデル（Anisotropic Friction）
地面から蛇が受ける反力を計算するモジュール

学べることは：
- 方向依存の摩擦とは何か
- なぜ蛇は前進するのか
- 物理シミュレーションの基本
"""

import math


def compute_segment_velocities(positions_prev: list,
                               positions_curr: list,
                               dt: float = 1.0) -> list:
    """
    各セグメントの速度を計算する。

    Parameters:
    -----------
    positions_prev : list
        前の時刻でのセグメント位置 [(x0, y0), ...]

    positions_curr : list
        現在の時刻でのセグメント位置 [(x0, y0), ...]

    dt : float
        時間ステップ（デフォルト 1.0）

    Returns:
    --------
    list
        [(vx0, vy0), (vx1, vy1), ...]
        各セグメントの速度ベクトル
    """

    velocities = []

    for (x_prev, y_prev), (x_curr, y_curr) in zip(positions_prev, positions_curr):
        vx = (x_curr - x_prev) / dt
        vy = (y_curr - y_prev) / dt
        velocities.append((vx, vy))

    return velocities


def compute_friction_forces(positions: list,
                           segment_directions: list,
                           c_forward: float = 1.0,
                           c_lateral: float = 10.0) -> tuple:
    """
    異方性摩擦から蛇全体が受ける力を計算する。

    Parameters:
    -----------
    positions : list
        各セグメント先端の位置 [(x0, y0), ...]

    segment_directions : list
        各セグメントの向きベクトル [(dx0, dy0), ...]
        （compute_segment_directions() の出力）

    c_forward : float
        前後方向の摩擦係数（小さい ＝ 滑りやすい）
        例：1.0

    c_lateral : float
        左右方向の摩擦係数（大きい ＝ 滑りにくい）
        例：10.0

    Returns:
    --------
    (fx_total, fy_total)
        蛇全体が地面から受ける総摩擦力

    原理（物理）：
    ---------------
    各セグメントは、地面との接触点で摩擦を受けます。

    蛇が「左に動こう」としても、鱗が引っかかって
    「左への動きが阻止される」（高い摩擦）

    蛇が「前に動こう」とすると、鱗がすべすべで
    「前への動きは許される」（低い摩擦）

    複数のセグメントの左右成分の力は打ち消し合い、
    前後成分の力だけが残ります。

    これが「くねくね → 前進」の物理です。
    """

    fx_total = 0
    fy_total = 0

    # 各セグメントについて処理
    for (x, y), (ux, uy) in zip(positions, segment_directions):
        # セグメントの垂直方向（左右）
        # 向きベクトル (ux, uy) の垂直方向は (-uy, ux)
        vx = -uy
        vy = ux

        # このセグメントが「どれだけ前後・左右に動こうとしているか」
        # を推定するため、位置から「想定される速度」を計算
        # （簡略版：位置の変化を速度と見なす）

        # セグメント位置から、「蛇の動きのトレンド」を推定
        # 前後方向への成分（蛇が向いている方向）
        component_forward = x * ux + y * uy

        # 左右方向への成分（蛇が向いている方向の垂直方向）
        component_lateral = x * vx + y * vy

        # 摩擦力（速度と反対方向に働く）
        # 実装：前後・左右それぞれの成分に摩擦係数をかける

        # 簡略版：各方向への「力の傾向」を計算
        # （より正確には、速度の微分が必要ですが、
        #  ここではシンプルに実装）

        # 各セグメントの「期待される速度」を計算
        # 蛇の波動から、このセグメントはどう動く「べき」か
        # → 位置の変化として反映される

        # 摩擦モデル：
        # 前後成分には c_forward をかける
        # 左右成分には c_lateral をかける

        force_forward = -c_forward * component_forward * ux
        force_forward_y = -c_forward * component_forward * uy

        force_lateral = -c_lateral * component_lateral * vx
        force_lateral_y = -c_lateral * component_lateral * vy

        # 合計
        fx_total += force_forward + force_lateral
        fy_total += force_forward_y + force_lateral_y

    return (fx_total, fy_total)


def update_snake_position(positions: list,
                         friction_forces: tuple,
                         mass: float = 1.0,
                         dt: float = 0.1) -> tuple:
    """
    摩擦力から蛇全体の移動を計算する。

    Parameters:
    -----------
    positions : list
        各セグメント先端の位置

    friction_forces : tuple
        (fx_total, fy_total) 摩擦力

    mass : float
        蛇全体の質量（デフォルト 1.0）

    dt : float
        時間ステップ（デフォルト 0.1 秒）

    Returns:
    --------
    (dx, dy)
        蛇全体の移動量

    原理（ニュートン力学）：
    -----------------------
    F = m * a  （力 = 質量 × 加速度）
    a = F / m

    v_new = v_old + a * dt
    x_new = x_old + v_new * dt

    簡略化して：
    x_new = x_old + (F / m) * dt^2
    """

    fx_total, fy_total = friction_forces

    # 加速度を計算
    ax = fx_total / mass
    ay = fy_total / mass

    # 移動量を計算（v ≈ a * dt と仮定、簡略版）
    dx = ax * (dt ** 2) * 0.5  # 簡略版
    dy = ay * (dt ** 2) * 0.5

    return (dx, dy)


def apply_translation(positions: list, dx: float, dy: float) -> list:
    """
    蛇全体を (dx, dy) だけ移動させる。

    Parameters:
    -----------
    positions : list
        各セグメント先端の位置

    dx, dy : float
        移動量

    Returns:
    --------
    list
        移動後のセグメント位置
    """

    translated = []
    for x, y in positions:
        translated.append((x + dx, y + dy))

    return translated


if __name__ == "__main__":
    # デモ：異方性摩擦を見る
    print("=== 異方性摩擦 デモ ===\n")

    print("シナリオ：蛇のセグメントが左に 5 だけ移動しようとしている")
    print()

    # セグメントの位置（蛇が左に移動したい）
    positions = [(0, -5)]  # y が負 = 左に移動

    # セグメントは右を向いている
    segment_directions = [(1, 0)]

    # 摩擦係数
    c_forward = 1.0      # 前後は滑りやすい
    c_lateral = 10.0     # 左右は滑りにくい

    fx, fy = compute_friction_forces(positions, segment_directions,
                                     c_forward, c_lateral)

    print(f"計算された摩擦力: fx={fx:.2f}, fy={fy:.2f}")
    print()
    print("解釈：")
    print(f"  セグメントが左 (y=-5) に移動しようとしているのに対して、")
    print(f"  地面は右方向（y正方向）に大きな力で反発する。")
    print(f"  これが「左右方向の高い摩擦」です。")
    print()

    # 移動量を計算
    dx, dy = update_snake_position(positions, (fx, fy), mass=1.0, dt=0.1)
    print(f"計算された移動量: dx={dx:.3f}, dy={dy:.3f}")
    print()
    print("※ Phase 2 で、複数セグメントが波を作るとき、")
    print("  これらの左右成分が打ち消し合い、")
    print("  前後成分だけが残って前進が生じます。")
