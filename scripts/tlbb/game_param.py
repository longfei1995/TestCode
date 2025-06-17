from typing import Dict, Tuple
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

@dataclass
class HPBarConfig:
    player1: Point = Point(100, 100)  # 玩家1血条，在血条3/4的位置
    player2: Point = Point(200, 200)  # 玩家2血条，在血条3/4的位置
    player3: Point = Point(300, 300)  # 玩家3血条，在血条3/4的位置
    player4: Point = Point(400, 400)  # 玩家4血条，在血条3/4的位置
    player5: Point = Point(500, 500)  # 玩家5血条，在血条3/4的位置
    player6: Point = Point(600, 600)  # 玩家6血条，在血条3/4的位置
    pet: Point = Point(700, 700)      # 宠物血条，在血条3/4的位置

@dataclass
class MPBarConfig:
    player1: Point = Point(100, 100)  # 玩家1魔法条，在魔法条3/4的位置


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