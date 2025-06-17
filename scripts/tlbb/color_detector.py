import win32gui
import win32ui
import win32con
import win32api
from PIL import Image, ImageGrab
import numpy as np
from typing import Tuple, Optional, List
import time
import os
from datetime import datetime

class ColorDetector:
    """颜色检测器"""
    
    def __init__(self):
        pass
    
    def _getPixelColorAtScreen(self, x: int, y: int) -> Tuple[int, int, int]:
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
    
    def getPixelPosColorInWindow(self, hwnd: int, x: int, y: int) -> Tuple[int, int, int]:
        """获取窗口内指定位置的像素颜色 (相对于窗口左上角)"""
        try:
            # 获取窗口位置
            window_rect = win32gui.GetWindowRect(hwnd)
            window_x, window_y = window_rect[0], window_rect[1]
            
            # 转换为屏幕坐标
            screen_x = window_x + x
            screen_y = window_y + y
            
            return self._getPixelColorAtScreen(screen_x, screen_y)
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
            print(f"截图区域: {left}, {top}, {right}, {bottom}")
            # 获取当前文件所在的路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 保存截图
            screenshot.save(os.path.join(current_dir, "pics", f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"))
            return screenshot
        except Exception as e:
            print(f"截取窗口区域失败: {e}")
            return None
    
    def isEmpty(self, color: Tuple[int, int, int]) -> bool:
        """检查血条或者蓝条是否为空"""
        r1, g1, b1 = 23, 23, 23
        r2, g2, b2 = color
        tolerance = 10
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
    window_manager = WindowManager()
    color_detect = ColorDetector()

    # 选择目标窗口
    hwnd = window_manager.selectWindow()
    if hwnd is None:
        print("未选择窗口，程序退出")
        exit()
    
    # 获取窗口信息
    window_rect = window_manager.getWindowRect(hwnd)
    window_width = window_rect[2] - window_rect[0]
    window_height = window_rect[3] - window_rect[1]
    window_title = win32gui.GetWindowText(hwnd)
    
    print(f"\n窗口信息:")
    print(f"  标题: {window_title}")
    print(f"  句柄: {hwnd}")
    print(f"  位置: ({window_rect[0]}, {window_rect[1]})")
    print(f"  大小: {window_width} x {window_height}")
    
    while True:
        print("\n" + "="*50)
        print("请输入要检测的坐标 (相对于窗口左上角):")
        
        try:
            x = int(input(f"X坐标 (0-{window_width-1}): "))
            y = int(input(f"Y坐标 (0-{window_height-1}): "))
            
            if 0 <= x < window_width and 0 <= y < window_height:
                # 检测指定位置的颜色
                color = color_detect.getPixelPosColorInWindow(hwnd, x, y)
                hex_color = color_detect.rgb2Hex(color)
                print(f"\n位置 ({x}, {y}) 的颜色:")
                print(f"  RGB: {color}")
                print(f"  HEX: {hex_color}")
                
                # 自动截图保存
                image = color_detect.captureWindow(hwnd, x, y, 115, 12)
            else:
                print("坐标超出窗口范围")
                
            # 询问是否继续
            continue_choice = input("\n是否继续检测其他位置? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes', '是']:
                print("程序退出")
                break
                
        except ValueError:
            print("请输入有效的数字")
        except KeyboardInterrupt:
            print("\n\n程序被中断，退出")
            break
        except Exception as e:
            print(f"发生错误: {e}")
    
    