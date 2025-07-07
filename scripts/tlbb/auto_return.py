"""
@author: Hu Yunhao
@time: 2025/07/04
@desc: 自动回点
"""

from window_manager import WindowManager
from color_detector import ColorDetector
from keyboard_simulator import KeyboardSimulator
from img_match import ImageMatch
from game_param import ImagePath
from dig_seed import DigSeed  # 导入DigSeed类
import time

class AutoReturn:
    def __init__(self, hwnd:int):
        self.hwnd = hwnd
        self.window_manager = WindowManager()
        self.image_match = ImageMatch(self.hwnd)
        self.keyboard_simulator = KeyboardSimulator()
        # 创建DigSeed实例，用于复用其方法
        self.dig_seed_helper = DigSeed(hwnd)
    
    def _moveSceneConfirm(self):
        """移动场景确认 - 使用DigSeed类的方法"""
        return self.dig_seed_helper.moveSceneConfirm()
    
    def _getDownHorse(self):
        """下马"""
        return self.dig_seed_helper.getDownHorse()  
    
    def _getUpHorse(self):
        """上马"""
        return self.dig_seed_helper.getUpHorse()
    
    def _isPersonStop(self):
        """判断人物是否停止"""
        return self.dig_seed_helper.isPersonStop()
    
    def _typeNumber(self, number:str):
        """输入数字"""
        # 按数字前按三下删除
        for _ in range(3):
            self.keyboard_simulator.pressKey("backspace", self.hwnd)
            time.sleep(0.05)
        # 输入数字 - 使用typeChar方法发送WM_CHAR消息
        for char in number:
            self.keyboard_simulator.typeChar(char, self.hwnd)
            time.sleep(0.05)
    
    def _escapeHell(self):
        """从地府去大理"""
        print("当前人物在地府，开始逃离地府去大理....")
        # 点击自动寻路
        self.keyboard_simulator.mouseClick(960, 252, self.hwnd)
        time.sleep(1)
        
        # 双击孟婆
        meng_po_pos = self.image_match.getImageCenterPos(ImagePath.auto_return.meng_po)
        if meng_po_pos is not None:
            self.keyboard_simulator.mouseDoubleClick(meng_po_pos.x, meng_po_pos.y, self.hwnd)
            time.sleep(10) # 等待大理对话框弹出
        else:
            print("未找到自动寻路中的孟婆标签，逃离地府失败")
            return False
        
        # 点击大理
        da_li_pos = self.image_match.getImageCenterPos(ImagePath.auto_return.da_li)
        if da_li_pos is not None:
            self.keyboard_simulator.mouseClick(da_li_pos.x, da_li_pos.y, self.hwnd)
            time.sleep(7) # 等待到场景大理
        else:
            print("未找到大理标签，逃离地府失败")
            return False
        
        return True
    
    def _isInHell(self):
        """判断是否在地府"""
        # 获取地府图片
        bbox = self.image_match.getImageBbox(ImagePath.auto_return.di_fu)
        if bbox is not None:
            return True
        return False
    
    def _isInXueYuan(self):
        """判断是否在雪原"""
        # todo
        # 获取雪原图片
        # bbox = self.image_match.getImageBbox(ImagePath.auto_return.xue_yuan)
        # if bbox is not None:
        #     return True
        return False
    
    def locateAutoReturn(self, x:str, y:str):
        # 获取自动寻路对话框
        self.keyboard_simulator.pressKey("`", self.hwnd)
        time.sleep(1)
        bbox = self.image_match.getImageBbox(ImagePath.auto_return.auto_find)
        if bbox is not None:
            # 计算两个坐标框的坐标，和移动按钮
            y1 = y2 = y3 = (int)(bbox.top + 10)
            x1 = (int)(bbox.left + 44)
            x2 = (int)(bbox.left + 75)
            x3 = (int)(bbox.left + 113)
            # 输入x坐标
            self.keyboard_simulator.mouseClick(x1, y1, self.hwnd)
            self._typeNumber(x)
            time.sleep(0.5)
            # 输入y坐标
            self.keyboard_simulator.mouseClick(x2, y2, self.hwnd)
            self._typeNumber(y)
            time.sleep(0.5)
            # 点击移动按钮
            self.keyboard_simulator.mouseClick(x3, y3, self.hwnd)
            time.sleep(0.5)
            return True
        else:
            return False
    
    def toXueYuan(self, is_return_immediately:bool = False):
        """去雪原"""
        # todo
        # 如果是立即返回，那么检查是否有确定框
        if is_return_immediately:
            pass
            # todo 检查是否存在确定框
        # 如果在地府，那么执行回点流程，否则不做其他动作
        if self._isInHell():
            self._escapeHell()
        else:
            pass


if __name__ == "__main__":
    window_manager = WindowManager()
    hwnd = window_manager.selectWindow()
    if hwnd is None:
        print("未选择窗口")
        exit()
    auto_return = AutoReturn(hwnd)
    auto_return._escapeHell()

