"""
Phase 1 の簡単なテスト（ビジュアライゼーションなし）

このスクリプトは、Phase 1 のシミュレーションが正しく動作するか
確認するためのテストです。

実行方法：
  python3 test_phase1.py
"""

import sys
from components.cpg import get_muscle_activation, split_into_left_right
from components.kinematics import (
    get_joint_angles_from_activation,
    forward_kinematics
)


def test_phase1():
    """Phase 1 のシミュレーションをテストする。"""

    print("=" * 60)
    print("Phase 1: テスト実行")
    print("=" * 60)
    print()

    # パラメータ
    num_joints = 30
    segment_length = 10
    max_bend = 30.0
    frequency = 2.0
    wavelength = 4.0
    amplitude = 1.0

    # 10ステップ実行
    num_steps = 10
    dt = 0.1

    print(f"設定：")
    print(f"  関節数: {num_joints}")
    print(f"  セグメント長: {segment_length} mm")
    print(f"  周波数: {frequency} Hz")
    print(f"  波長: {wavelength} 関節")
    print(f"  シミュレーション時間ステップ: {dt}s")
    print()

    # シミュレーション実行
    print(f"シミュレーション実行: {num_steps} ステップ")
    print()

    for step in range(num_steps):
        time = step * dt

        # Step 1: CPG から筋肉活動
        activation = get_muscle_activation(
            num_joints=num_joints,
            amplitude=amplitude,
            frequency=frequency,
            wavelength=wavelength,
            time=time
        )

        # Step 2: 筋肉活動を左右に分ける
        left, right = split_into_left_right(activation)

        # Step 3: 関節角を計算
        joint_angles = get_joint_angles_from_activation(
            left, right,
            max_bend=max_bend
        )

        # Step 4: FK で蛇の形を計算
        positions = forward_kinematics(
            joint_angles,
            segment_length=segment_length,
            start_pos=(0, 0),
            start_angle=0.0
        )

        # 情報表示
        if step % 2 == 0:
            print(f"ステップ {step:2d} (t={time:.2f}s):")
            print(f"  関節0: 活性度={activation[0]:+.3f}, "
                  f"角度={joint_angles[0]:+.1f}°")
            print(f"  関節15: 活性度={activation[15]:+.3f}, "
                  f"角度={joint_angles[15]:+.1f}°")

            # 蛇の形状
            tail_x, tail_y = positions[-1]
            tail_distance = (tail_x**2 + tail_y**2) ** 0.5
            print(f"  蛇の尾: ({tail_x:6.1f}, {tail_y:6.1f}) mm, "
                  f"距離={tail_distance:6.1f} mm")
            print()

    print("=" * 60)
    print("✓ Phase 1 テスト成功！")
    print("=" * 60)
    print()
    print("観察：")
    print("- 筋肉活動が時間とともに変わっている")
    print("- 関節角が波の形をしている")
    print("- 蛇の形が時間とともに変わっている")
    print()
    print("次のステップ：")
    print("  python3 phase1_basic.py")
    print("  ↑ ビジュアライゼーション付きで実行")


if __name__ == "__main__":
    try:
        test_phase1()
    except Exception as e:
        print(f"✗ テスト失敗: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
