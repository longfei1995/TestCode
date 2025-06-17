from typing import Dict, Tuple
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

@dataclass
class HPBarConfig:
    # 血条设置在4/5的位置
    player1: Point = Point(200, 66)
    player2: Point = Point(140, 160)
    player3: Point = Point(140, 205)
    player4: Point = Point(140, 250)
    player5: Point = Point(140, 295)
    player6: Point = Point(140, 340)
    pet: Point = Point(217, 109)

@dataclass
class MPBarConfig:
    player1: Point = Point(167, 73)

@dataclass
class PhotoConfig:
    player1: Point = Point(40, 66)
    player2: Point = Point(24, 160)
    player3: Point = Point(24, 205)
    player4: Point = Point(24, 250)
    player5: Point = Point(24, 295)
    player6: Point = Point(24, 340)

@dataclass
class DefaultKeyConfig:
    pet_attack: str = "F7"
    pet_eat: str = "F8"
    xue_ji: str = "F9"
    qing_xin: str = "F10"

# 创建实例
kHPBar = HPBarConfig()
kMPBar = MPBarConfig()
kDefaultKey = DefaultKeyConfig()
kProfilePhoto = PhotoConfig()