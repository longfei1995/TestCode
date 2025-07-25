from typing import Dict, Tuple
from dataclasses import dataclass
import os
import sys

def getBasePath():
    """获取exe所在的路径，兼容开发环境和打包后的环境"""
    # 判断是否是打包后的环境
    if getattr(sys, 'frozen', False):
        # 打包后的环境
        if hasattr(sys, '_MEIPASS'):
            # onefile模式：从临时资源目录读取
            base_path = getattr(sys, '_MEIPASS')
        else:
            # onedir模式：从可执行文件所在目录读取
            base_path = os.path.dirname(sys.executable)
    else:
        # 开发环境，在脚本同目录查找
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return base_path

# 全局路径常量
kBaseDir = getBasePath()
kPicDir = os.path.join(kBaseDir, "img_src")

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

@dataclass(frozen=True)
class ImagePath:
    class auto_return:
        auto_find: str = os.path.join(kPicDir, "auto_return\\1.png")
        di_fu: str = os.path.join(kPicDir, "auto_return\\2.png")
        meng_po: str = os.path.join(kPicDir, "auto_return\\3.png")
        da_li: str = os.path.join(kPicDir, "auto_return\\4.png")
        xue_yuan: str = os.path.join(kPicDir, "auto_return\\5.png")
        chu_qiao: str = os.path.join(kPicDir, "auto_return\\6.png")     # 出窍按钮
        si_xiang: str = os.path.join(kPicDir, "auto_return\\7.png")      # 四象天门阵场景
        hui_yi: str = os.path.join(kPicDir, "auto_return\\8.png")      # 回营按钮
        qian_wang_ji_tan: str = os.path.join(kPicDir, "auto_return\\9.png")      # 前往祭坛按钮
        
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
    pet_attack: str = "F5"
    pet_eat: str = "F6"
    xue_ji: str = "F7"
    qing_xin: str = "F8"
    ding_wei_fu: str = "F9"
    horse: str = "F10"

# 创建实例
kHPBar = HPBarConfig()
kMPBar = MPBarConfig()
kDefaultKey = DefaultKeyConfig()
kProfilePhoto = PhotoConfig()