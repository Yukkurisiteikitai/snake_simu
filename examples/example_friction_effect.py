"""
例3：摩擦係数の効果を見る

左右摩擦係数（c_lateral）を変えると、
蛇の前進効率がどう変わるか観察できます。

実行方法：
  python examples/example_friction_effect.py

高い摩擦比 (c_lateral >> c_forward) ほど、
蛇行による前進が効率的になります。
"""

import sys
sys.path.insert(0, '..')

from phase2_with_friction import SnakeSimulatorPhase2, create_animation


def main():
    print("例3：摩擦係数の効果")
    print()

    simulator = SnakeSimulatorPhase2(num_joints=30, segment_length=10)

    # パラメータ：摩擦が異方性（横に強い）
    simulator.amplitude = 1.0
    simulator.frequency = 2.0
    simulator.wavelength = 4.0

    # ここを変更して実験してみてください：
    simulator.c_forward = 1.0      # 前後方向は滑りやすい
    simulator.c_lateral = 15.0     # ← これを変えてみよう！
                                   #   10 → 15 : より効率的に前進
                                   #   15 → 5  : 前進が弱くなる

    print(f"前後摩擦係数 c_forward: {simulator.c_forward}")
    print(f"左右摩擦係数 c_lateral: {simulator.c_lateral}")
    print(f"摩擦比: {simulator.c_lateral / simulator.c_forward:.1f}")
    print()
    print("実験：c_lateral を変えてみよう")
    print("  高いほど → 前進が素早い")
    print("  低いほど → 前進が遅い/ほぼ動かない")
    print()

    create_animation(simulator, duration=8.0)


if __name__ == "__main__":
    main()
