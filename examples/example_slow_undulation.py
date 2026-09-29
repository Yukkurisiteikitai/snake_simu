"""
例1：ゆっくりした蛇行

低周波数で、ゆっくりくねくね動く蛇。
現実の蛇の多くはこのような速度で移動します。

実行方法：
  python examples/example_slow_undulation.py
"""

import sys
sys.path.insert(0, '..')

from phase2_with_friction import SnakeSimulatorPhase2, create_animation


def main():
    print("例1：ゆっくりした蛇行")
    print()

    simulator = SnakeSimulatorPhase2(num_joints=30, segment_length=10)

    # パラメータ：ゆっくり
    simulator.amplitude = 1.0
    simulator.frequency = 0.5      # ← 低周波数（ゆっくり）
    simulator.wavelength = 6.0     # ← 長めの波
    simulator.c_forward = 1.0
    simulator.c_lateral = 10.0

    print(f"周波数: {simulator.frequency} Hz （ゆっくり）")
    print(f"波長: {simulator.wavelength} 関節")
    print()

    create_animation(simulator, duration=10.0)


if __name__ == "__main__":
    main()
