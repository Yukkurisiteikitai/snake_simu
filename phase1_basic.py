"""
Phase 1: 基本的な蛇シミュレーション
KHが固定位置でくねくね動く（前進なし）

このコードで学べることは：
- CPG（脳）から筋肉活動を生成する
- 筋肉活動から関節角を計算する
- 関節角から体の形を計算する（FK）
- その流れをアニメーションで見る

実行方法：
  python phase1_basic.py

キー操作：
  スペースキー: 一時停止/再開
  右矢印キー: 1フレーム進める
  Qキー: 終了
"""

import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import sys

# 自分たちのモジュールをインポート
from components.cpg import get_muscle_activation, split_into_left_right
from components.kinematics import (
    get_joint_angles_from_activation,
    forward_kinematics,
    compute_segment_directions
)


class SnakeSimulatorPhase1:
    """
    Phase 1: 蛇のシミュレーター（固定位置版）
    """

    def __init__(self, num_joints=30, segment_length=10):
        """
        シミュレーターを初期化する。

        Parameters:
        -----------
        num_joints : int
            蛇の関節数

        segment_length : float
            各セグメントの長さ
        """
        self.num_joints = num_joints
        self.segment_length = segment_length

        # シミュレーションパラメータ
        self.amplitude = 1.0        # 筋肉活動の大きさ
        self.max_bend = 30.0        # 最大曲がり角（度）
        self.frequency = 1.0        # 波の周波数（Hz）
        self.wavelength = 4.0       # 波の長さ（関節数単位）

        # 時間管理
        self.time = 0.0
        self.dt = 0.01  # シミュレーション時間ステップ（秒）

        # 蛇の位置（Phase 1では固定）
        self.snake_x = 0
        self.snake_y = 0

        # 履歴保存（アニメーション用）
        self.history = []

    def step(self):
        """
        1ステップシミュレーションを進める。
        """
        # Step 1: CPG から筋肉活動を取得
        activation = get_muscle_activation(
            num_joints=self.num_joints,
            amplitude=self.amplitude,
            frequency=self.frequency,
            wavelength=self.wavelength,
            time=self.time
        )

        # Step 2: 筋肉活動を左右に分ける
        left, right = split_into_left_right(activation)

        # Step 3: 左右の筋肉活動から関節角を計算
        joint_angles = get_joint_angles_from_activation(
            left, right,
            max_bend=self.max_bend
        )

        # Step 4: 関節角から蛇の形を計算（FK）
        positions = forward_kinematics(
            joint_angles,
            segment_length=self.segment_length,
            start_pos=(self.snake_x, self.snake_y),
            start_angle=0.0
        )

        # 履歴に保存
        self.history.append({
            'time': self.time,
            'positions': positions,
            'joint_angles': joint_angles,
            'activation': activation
        })

        # 時刻を進める
        self.time += self.dt

    def get_positions(self):
        """最新の蛇の位置を取得。"""
        if self.history:
            return self.history[-1]['positions']
        return []

    def run_simulation(self, duration=10.0):
        """
        シミュレーションを指定時間実行する。

        Parameters:
        -----------
        duration : float
            シミュレーション時間（秒）
        """
        steps = int(duration / self.dt)
        for _ in range(steps):
            self.step()


def create_animation(simulator, duration=10.0):
    """
    matplotlib でアニメーションを作成・表示する。

    Parameters:
    -----------
    simulator : SnakeSimulatorPhase1
        蛇シミュレーター

    duration : float
        アニメーション時間（秒）
    """

    # シミュレーションを事前計算
    print(f"シミュレーション実行中（{duration}秒）...")
    simulator.run_simulation(duration)
    print(f"フレーム数: {len(simulator.history)}")

    # グラフの準備
    fig, ax = plt.subplots(figsize=(12, 8))

    # スケール
    margin = 50
    ax.set_xlim(-margin, simulator.num_joints * simulator.segment_length + margin)
    ax.set_ylim(-margin, margin)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    ax.set_title('Phase 1: 蛇が固定位置でくねくね動く')

    # 蛇のライン
    line, = ax.plot([], [], 'b-', linewidth=2, label='Snake body')

    # 各セグメントの円
    circles = []
    for _ in range(simulator.num_joints):
        circle = Circle((0, 0), radius=3, color='blue', alpha=0.6)
        ax.add_patch(circle)
        circles.append(circle)

    # 頭
    head, = ax.plot([], [], 'ro', markersize=10, label='Head')

    # 尾
    tail, = ax.plot([], [], 'gs', markersize=8, label='Tail')

    # 時刻表示
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    # 情報表示
    info_text = ax.text(0.02, 0.85, '', transform=ax.transAxes,
                        fontsize=10, verticalalignment='top')

    ax.legend(loc='upper right')

    def animate(frame_idx):
        """各フレームの描画。"""
        if frame_idx >= len(simulator.history):
            return

        state = simulator.history[frame_idx]
        positions = state['positions']

        # 蛇のライン描画
        xs = [0] + [x for x, y in positions]
        ys = [0] + [y for x, y in positions]

        line.set_data(xs, ys)

        # セグメントの円を配置
        for i, (circle, (x, y)) in enumerate(zip(circles, positions)):
            circle.set_center((x, y))

        # 頭
        head.set_data([0], [0])

        # 尾
        if positions:
            tail.set_data([positions[-1][0]], [positions[-1][1]])

        # 時刻表示
        time_text.set_text(f'Time: {state["time"]:.2f}s')

        # 情報表示
        if state['activation']:
            # 最初の関節の活性度を表示
            act0 = state['activation'][0]
            angle0 = state['joint_angles'][0]
            info_text.set_text(
                f'Joint 0: activation={act0:+.3f}, angle={angle0:+.1f}°\n'
                f'Num joints: {simulator.num_joints}\n'
                f'Wavelength: {simulator.wavelength}\n'
                f'Frequency: {simulator.frequency} Hz'
            )

        return line, head, tail, time_text, info_text

    # アニメーション作成
    frames = len(simulator.history)
    fps = int(1.0 / simulator.dt)

    # 実際のアニメーション速度調整（見やすくするため遅くする）
    display_fps = 30
    interval = int(1000 / display_fps)  # ミリ秒

    # フレームスキップを計算
    skip = max(1, fps // display_fps)
    frame_indices = list(range(0, frames, skip))

    ani = animation.FuncAnimation(
        fig, animate,
        frames=frame_indices,
        interval=interval,
        blit=False,
        repeat=True
    )

    print("\n=== 操作方法 ===")
    print("スペースキー: 一時停止/再開")
    print("Qキー: 終了")
    print()

    plt.show()


def main():
    """メイン関数。"""
    print("=" * 60)
    print("Phase 1: 蛇が固定位置でくねくね動く")
    print("=" * 60)
    print()
    print("特徴：")
    print("- 蛇の頭は固定位置にある")
    print("- 筋肉の波が尾の方へ流れる")
    print("- でも前進しない（摩擦がないため）")
    print()

    # シミュレーター作成
    simulator = SnakeSimulatorPhase1(
        num_joints=30,
        segment_length=10
    )

    # パラメータを調整
    simulator.amplitude = 1.0
    simulator.frequency = 2.0  # 速くくねくね
    simulator.wavelength = 4.0

    print(f"パラメータ：")
    print(f"  関節数: {simulator.num_joints}")
    print(f"  セグメント長: {simulator.segment_length} mm")
    print(f"  周波数: {simulator.frequency} Hz")
    print(f"  波長: {simulator.wavelength} 関節")
    print()

    # アニメーション実行
    create_animation(simulator, duration=5.0)


if __name__ == "__main__":
    main()
