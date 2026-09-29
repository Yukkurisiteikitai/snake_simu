"""
例2：速い蛇行

高周波数で、速くくねくね動く蛇。
パニック時や逃げるときのような速い移動。

実行方法：
  python examples/example_fast_undulation.py
"""

import sys
sys.path.insert(0, '..')

from phase2_with_friction import SnakeSimulatorPhase2, create_animation


def main():
    print("例2：速い蛇行")
    print()

    simulator = SnakeSimulatorPhase2(num_joints=30, segment_length=10)

    # パラメータ：速い
    simulator.amplitude = 1.0
    simulator.frequency = 3.0      # ← 高周波数（速い）
    simulator.wavelength = 3.0     # ← 短めの波
    simulator.c_forward = 1.0
    simulator.c_lateral = 10.0

    print(f"周波数: {simulator.frequency} Hz （速い！）")
    print(f"波長: {simulator.wavelength} 関節")
    print()
    print("観察ポイント：")
    print("- 蛇が素早く前進する")
    print("- 波の周期が短い")
    print()

    create_animation(simulator, duration=6.0)


if __name__ == "__main__":
    main()
