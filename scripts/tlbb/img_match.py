import cv2
import numpy as np
import pyautogui
import time
import os
import sys
import threading
import queue
import logging

from window_manager import WindowManager
from game_param import ImagePath, Point, Bbox
from keyboard_simulator import KeyboardSimulator

class ImageMatch:
    def __init__(self, hwnd:int):
        self.window_manager = WindowManager()
        self.hwnd = hwnd
        window_rect = self.window_manager.getWindowRect(self.hwnd)
        self.window_x = window_rect[0]
        self.window_y = window_rect[1]
        self.window_width = window_rect[2] - window_rect[0]
        self.window_height = window_rect[3] - window_rect[1]
    
    def getImageCenterPos(self, image_path:str, confidence:float = 0.8):
        """
        获取图片在窗口坐标系下的中心位置
        Args:
            image_path: 图片路径
            confidence: 置信度
        Returns:
            Point: 图片中心位置
            None: 未找到图片
        """
        try:
            window_region = (self.window_x, self.window_y, self.window_width, self.window_height)
            pic_region = pyautogui.locateOnScreen(
                image=image_path, 
                confidence=confidence,
                grayscale=False,
                region=window_region    # 指定搜索区域
            )
            if pic_region is not None:
                local_pic_x = int(pic_region.left + pic_region.width / 2 - self.window_x)
                local_pic_y = int(pic_region.top + pic_region.height / 2 - self.window_y) 
                bbox_left = pic_region.left - self.window_x
                bbox_top = pic_region.top - self.window_y
                bbox_right = pic_region.left + pic_region.width - self.window_x
                bbox_bottom = pic_region.top + pic_region.height - self.window_y
                self.window_manager.saveBboxImage(self.hwnd, Bbox(bbox_left, bbox_top, bbox_right, bbox_bottom))
                return Point(local_pic_x, local_pic_y)
        except Exception as e:
            print(f"获取图片中心位置失败: {e}")
        return None
    
    def getImageBbox(self, image_path:str, confidence:float = 0.8):
        """
        获取图片在窗口坐标系下的bbox
        Args:
            image_path: 图片路径
            confidence: 置信度
        Returns:
            Bbox: 图片bbox
            None: 未找到图片
        """
        try:
            window_region = (self.window_x, self.window_y, self.window_width, self.window_height)
            pic_region = pyautogui.locateOnScreen(
                image=image_path, 
                confidence=confidence,
                grayscale=False,
                region=window_region    # 指定搜索区域
            )
            if pic_region is not None:
                bbox_left = pic_region.left - self.window_x
                bbox_top = pic_region.top - self.window_y
                bbox_right = pic_region.left + pic_region.width - self.window_x
                bbox_bottom = pic_region.top + pic_region.height - self.window_y
                self.window_manager.saveBboxImage(self.hwnd, Bbox(bbox_left, bbox_top, bbox_right, bbox_bottom))
                return Bbox(bbox_left, bbox_top, bbox_right, bbox_bottom)
        except Exception as e:
            print(f"获取图片bbox失败: {e}")
        return None


if __name__ == "__main__":
    window_manager = WindowManager()
    hwnd = window_manager.selectWindow()
    keyboard_simulator = KeyboardSimulator()
    if hwnd is None:
        print("未选择窗口")
        exit()
    img_match = ImageMatch(hwnd)
    image_pos = img_match.getImageCenterPos(ImagePath.main.package)
    if image_pos is not None:
        print(f"图片中心位置: x={image_pos.x}, y={image_pos.y}")
        keyboard_simulator.mouseClick(image_pos.x, image_pos.y, hwnd)
    else:
        print("未找到图片")
        
        

    
        








