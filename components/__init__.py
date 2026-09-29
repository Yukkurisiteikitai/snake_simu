"""
蛇シミュレーションの各コンポーネント

このパッケージは以下のモジュールを含みます：
- cpg: Central Pattern Generator（脳）
- kinematics: Forward Kinematics（関節角→位置）
- friction: 異方性摩擦モデル
"""

from .cpg import get_muscle_activation, split_into_left_right
from .kinematics import (
    get_joint_angles_from_activation,
    forward_kinematics,
    compute_segment_directions
)
from .friction import (
    compute_friction_forces,
    update_snake_position,
    apply_translation
)

__all__ = [
    'get_muscle_activation',
    'split_into_left_right',
    'get_joint_angles_from_activation',
    'forward_kinematics',
    'compute_segment_directions',
    'compute_friction_forces',
    'update_snake_position',
    'apply_translation',
]
