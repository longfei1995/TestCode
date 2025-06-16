import win32gui
import win32ui
import win32con
import win32api
from PIL import Image, ImageGrab
import numpy as np
from typing import Tuple, Optional, List
import time

class ColorDetector:
    """颜色检测器"""
    
    def __init__(self):
        pass
    
    def getPixelColorAtScreen(self, x: int, y: int) -> Tuple[int, int, int]:
        """获取屏幕指定位置的像素颜色 (RGB)"""
        try:
            # 使用PIL截图方式
            screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
            pixel_color = screenshot.getpixel((0, 0))
            # 确保返回RGB三元组
            if isinstance(pixel_color, tuple) and len(pixel_color) >= 3:
                return (pixel_color[0], pixel_color[1], pixel_color[2])
            else:
                return (0, 0, 0)
        except Exception as e:
            print(f"获取屏幕像素颜色失败: {e}")
            return (0, 0, 0)
    
    def getPixelColorInWindow(self, hwnd: int, x: int, y: int) -> Tuple[int, int, int]:
        """获取窗口内指定位置的像素颜色 (相对于窗口左上角)"""
        try:
            # 获取窗口位置
            window_rect = win32gui.GetWindowRect(hwnd)
            window_x, window_y = window_rect[0], window_rect[1]
            
            # 转换为屏幕坐标
            screen_x = window_x + x
            screen_y = window_y + y
            
            return self.getPixelColorAtScreen(screen_x, screen_y)
        except Exception as e:
            print(f"获取窗口像素颜色失败: {e}")
            return (0, 0, 0)
    
    def captureWindow(self, hwnd: int, x: int, y: int, width: int, height: int) -> Optional[Image.Image]:
        """截取窗口指定区域"""
        try:
            # 获取窗口位置
            window_rect = win32gui.GetWindowRect(hwnd)
            window_x, window_y = window_rect[0], window_rect[1]
            
            # 计算截图区域
            left = window_x + x
            top = window_y + y
            right = left + width
            bottom = top + height
            
            # 截图
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            return screenshot
        except Exception as e:
            print(f"截取窗口区域失败: {e}")
            return None
    
    def isColorMatch(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], tolerance: int = 0) -> bool:
        """检查两个颜色是否匹配（在容差范围内）"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        return (abs(r1 - r2) <= tolerance and 
                abs(g1 - g2) <= tolerance and 
                abs(b1 - b2) <= tolerance)
    
    def rgb2Hex(self, rgb: Tuple[int, int, int]) -> str:
        """将RGB颜色转换为十六进制字符串"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def hex2RGB(self, hex_color: str) -> Tuple[int, int, int]:
        """将十六进制颜色转换为RGB"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            return (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))
        else:
            return (0, 0, 0)

# 使用示例
if __name__ == "__main__":
    from window_manager import WindowManager
    
    # 创建实例
    wm = WindowManager()
    cd = ColorDetector()
    
    