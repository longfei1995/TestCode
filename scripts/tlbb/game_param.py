from typing import Dict, Tuple
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0

@dataclass(frozen=True)
class Bbox:
    left: int = 0
    top: int = 0
    right: int = 0
    bottom: int = 0

kPicDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img_src")
@dataclass(frozen=True)
class ImagePath:
    class main:
        package: str = os.path.join(kPicDir, "main\\1.png")
    class kun_wu:
        cheng_huang: str = os.path.join(kPicDir, "kun_wu\\1.png")
        ti_jiao_ling_yao: str = os.path.join(kPicDir, "kun_wu\\7.png")
        ren_wu_button: str = os.path.join(kPicDir, "kun_wu\\9.png")
        mi_yin_ling_qu: str = os.path.join(kPicDir, "kun_wu\\10.png")
        move_scene_confirm: str = os.path.join(kPicDir, "kun_wu\\11.png")

@dataclass
class HPBarConfig:
    # 血条设置在4/5的位置
    p1_high: Point = Point(200, 66)
    p2_high: Point = Point(140, 160)
    p3_high: Point = Point(140, 205)
    p4_high: Point = Point(140, 250)
    p5_high: Point = Point(140, 295)
    p6_high: Point = Point(140, 340)
    
    p1_mid: Point = Point(143, 66)
    p2_mid: Point = Point(100, 160)
    p3_mid: Point = Point(100, 205)
    p4_mid: Point = Point(100, 250)
    p5_mid: Point = Point(100, 295)
    p6_mid: Point = Point(100, 340)
    
    p1_low: Point = Point(95, 66)
    p2_low: Point = Point(60, 160)
    p3_low: Point = Point(60, 205)
    p4_low: Point = Point(60, 250)
    p5_low: Point = Point(60, 295)
    p6_low: Point = Point(60, 340)
    
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