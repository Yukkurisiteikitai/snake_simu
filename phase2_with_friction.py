"""
Phase 2: 異方性摩擦を加える
蛇が前進し始める！

このコードで学べることは：
- 異方性摩擦の効果
- なぜ蛇は前進するのか
- パラメータ変更による影響

実行方法：
  python phase2_with_friction.py

このコードを実行すると、蛇が波を作りながら
右へ移動するのが見えます。
"""

import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import sys

from components.cpg import get_muscle_activation, split_into_left_right
from components.kinematics import (
    get_joint_angles_from_activation,
    forward_kinematics,
    compute_segment_directions
)
from components.friction import compute_friction_forces, apply_translation


class SnakeSimulatorPhase2:
    """
    Phase 2: 蛇のシミュレーター（異方性摩擦対応）

    蛇が前進するようになります！
    """

    def __init__(self, num_joints=30, segment_length=10):
        """
        シミュレーターを初期化する。
        """
        self.num_joints = num_joints
        self.segment_length = segment_length

        # シミュレーションパラメータ
        self.amplitude = 1.0        # 筋肉活動の大きさ
        self.max_bend = 30.0        # 最大曲がり角（度）
        self.frequency = 1.0        # 波の周波数（Hz）
        self.wavelength = 4.0       # 波の長さ

        # 摩擦パラメータ
        self.c_forward = 1.0        # 前後方向の摩擦係数（小さい）
        self.c_lateral = 10.0       # 左右方向の摩擦係数（大きい）

        # 時間管理
        self.time = 0.0
        self.dt = 0.01  # シミュレーション時間ステップ

        # 蛇の位置（移動する！）
        self.snake_x = 0.0
        self.snake_y = 0.0

        # 履歴保存
        self.history = []

    def step(self):
        """
        1ステップのシミュレーション。
        """
        # Step 1: CPG から筋肉活動
        activation = get_muscle_activation(
            num_joints=self.num_joints,
            amplitude=self.amplitude,
            frequency=self.frequency,
            wavelength=self.wavelength,
            time=self.time
        )

        # Step 2: 筋肉活動を左右に分ける
        left, right = split_into_left_right(activation)

        # Step 3: 関節角を計算
        joint_angles = get_joint_angles_from_activation(
            left, right,
            max_bend=self.max_bend
        )

        # Step 4: FK で蛇の形を計算
        positions = forward_kinematics(
            joint_angles,
            segment_length=self.segment_length,
            start_pos=(self.snake_x, self.snake_y),
            start_angle=0.0
        )

        # Step 5: セグメント方向を計算
        directions = compute_segment_directions(positions)

        # Step 6: 摩擦力を計算
        # （相対位置を使用）
        positions_rel = [(x - self.snake_x, y - self.snake_y)
                         for x, y in positions]

        fx_total, fy_total = compute_friction_forces(
            positions_rel,
            directions,
            c_forward=self.c_forward,
            c_lateral=self.c_lateral
        )

        # Step 7: 摩擦力から蛇全体の移動量を計算
        # 簡略化：摩擦力に比例して移動
        move_scale = self.dt * 0.1  # 調整因数
        dx = fx_total * move_scale
        dy = fy_total * move_scale

        # Step 8: 蛇の位置を更新
        self.snake_x += dx
        self.snake_y += dy

        # 履歴に保存
        self.history.append({
            'time': self.time,
            'positions': positions,
            'joint_angles': joint_angles,
            'activation': activation,
            'snake_x': self.snake_x,
            'snake_y': self.snake_y,
            'friction_x': fx_total,
            'friction_y': fy_total
        })

        # 時刻を進める
        self.time += self.dt

    def get_positions(self):
        """最新の蛇の位置。"""
        if self.history:
            return self.history[-1]['positions']
        return []

    def run_simulation(self, duration=10.0):
        """
        シミュレーションを実行。
        """
        steps = int(duration / self.dt)
        for i in range(steps):
            self.step()
            if (i + 1) % 100 == 0:
                print(f"  計算中... {i+1}/{steps} ステップ")


def create_animation(simulator, duration=10.0):
    """
    アニメーション作成・表示。
    """

    # シミュレーション実行
    print(f"シミュレーション実行中（{duration}秒）...")
    simulator.run_simulation(duration)
    print(f"フレーム数: {len(simulator.history)}")
    print()

    # グラフの準備
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # ========== 上：蛇の動き ==========
    margin = 50
    max_x = max([s['snake_x'] for s in simulator.history]) + 100
    ax1.set_xlim(-margin, max_x)
    ax1.set_ylim(-margin, margin)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('x (mm)')
    ax1.set_ylabel('y (mm)')
    ax1.set_title('Phase 2: 蛇が異方性摩擦で前進する')

    # 蛇のライン
    line, = ax1.plot([], [], 'b-', linewidth=2.5, label='Snake body')
    head, = ax1.plot([], [], 'ro', markersize=12, label='Head')
    tail, = ax1.plot([], [], 'gs', markersize=10, label='Tail')

    # 時刻表示
    time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes)

    # 情報表示
    info_text = ax1.text(0.02, 0.85, '', transform=ax1.transAxes,
                        fontsize=9, verticalalignment='top', family='monospace')

    ax1.legend(loc='upper right')

    # ========== 下：位置と摩擦力の時系列 ==========
    ax2.set_xlim(0, simulator.history[-1]['time'])
    ax2.set_ylim(-50, 300)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Position (mm)')
    ax2.set_title('蛇の位置の時系列（X座標）')

    # 位置の軌跡
    trajectory_x, = ax2.plot([], [], 'b-', linewidth=2, label='Snake x position')
    ax2.legend(loc='upper left')

    def animate(frame_idx):
        """フレーム描画。"""
        if frame_idx >= len(simulator.history):
            return

        state = simulator.history[frame_idx]
        positions = state['positions']

        # ========== 上のグラフ：蛇の動き ==========

        # 蛇のライン
        xs = [state['snake_x']] + [x for x, y in positions]
        ys = [state['snake_y']] + [y for x, y in positions]

        line.set_data(xs, ys)
        head.set_data([state['snake_x']], [state['snake_y']])

        if positions:
            tail.set_data([positions[-1][0]], [positions[-1][1]])

        # 情報表示
        time_text.set_text(f'Time: {state["time"]:.2f}s')

        info_str = (
            f"Position: ({state['snake_x']:6.1f}, {state['snake_y']:6.1f}) mm\n"
            f"Friction:  ({state['friction_x']:+7.1f}, {state['friction_y']:+7.1f})\n"
            f"Joint[0]: angle={state['joint_angles'][0]:+.1f}°, "
            f"act={state['activation'][0]:+.2f}"
        )
        info_text.set_text(info_str)

        # ========== 下のグラフ：位置の時系列 ==========

        times = [s['time'] for s in simulator.history[:frame_idx+1]]
        x_positions = [s['snake_x'] for s in simulator.history[:frame_idx+1]]

        trajectory_x.set_data(times, x_positions)

        return line, head, tail, time_text, info_text, trajectory_x

    # アニメーション作成
    frames = len(simulator.history)
    fps = int(1.0 / simulator.dt)
    display_fps = 30
    interval = int(1000 / display_fps)
    skip = max(1, fps // display_fps)
    frame_indices = list(range(0, frames, skip))

    ani = animation.FuncAnimation(
        fig, animate,
        frames=frame_indices,
        interval=interval,
        blit=False,
        repeat=True
    )

    print("=== 操作方法 ===")
    print("スペースキー: 一時停止/再開")
    print("Qキー: 終了")
    print()
    print("=== 観察ポイント ===")
    print("1. 蛇が左下から右上へ移動している")
    print("2. 蛇の形は波を保ったまま移動している")
    print("3. 下のグラフで、位置（x座標）が時間とともに増加している")
    print()

    plt.tight_layout()
    plt.show()


def main():
    """メイン関数。"""
    print("=" * 70)
    print("Phase 2: 異方性摩擦を加えて蛇が前進する")
    print("=" * 70)
    print()
    print("特徴：")
    print("- Phase 1 に「異方性摩擦」を加えた")
    print("- 蛇が「横」には滑りにくく、「前」には滑りやすい")
    print("- 結果：蛇がくねくねしながら前進する！")
    print()

    # シミュレーター作成
    simulator = SnakeSimulatorPhase2(
        num_joints=30,
        segment_length=10
    )

    # パラメータ
    simulator.amplitude = 1.0
    simulator.frequency = 2.0
    simulator.wavelength = 4.0
    simulator.c_forward = 1.0
    simulator.c_lateral = 10.0

    print(f"パラメータ：")
    print(f"  関節数: {simulator.num_joints}")
    print(f"  セグメント長: {simulator.segment_length} mm")
    print(f"  周波数: {simulator.frequency} Hz")
    print(f"  波長: {simulator.wavelength} 関節")
    print(f"  前後摩擦係数 c_forward: {simulator.c_forward}")
    print(f"  左右摩擦係数 c_lateral: {simulator.c_lateral}")
    print(f"  摩擦比 (c_lateral/c_forward): {simulator.c_lateral/simulator.c_forward:.1f}")
    print()

    # アニメーション実行
    create_animation(simulator, duration=8.0)


if __name__ == "__main__":
    main()
