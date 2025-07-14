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
    
    def getImageCenterPos(self, image_path:str, confidence:float = 0.8, is_print:bool = True, max_retries:int = 3, retry_interval:float = 0.5):
        """
        获取图片在窗口坐标系下的中心位置
        Args:
            image_path: 图片路径
            confidence: 置信度
            is_print: 是否打印错误信息
            max_retries: 最大重试次数（默认3次）
            retry_interval: 重试间隔秒数（默认0.5秒）
        Returns:
            Point: 图片中心位置
            None: 未找到图片
        """
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                # 动态获取当前窗口位置，而不是使用缓存的位置
                window_rect = self.window_manager.getWindowRect(self.hwnd)
                current_window_x = window_rect[0]
                current_window_y = window_rect[1]
                current_window_width = window_rect[2] - window_rect[0]
                current_window_height = window_rect[3] - window_rect[1]
                
                window_region = (current_window_x, current_window_y, current_window_width, current_window_height)
                pic_region = pyautogui.locateOnScreen(
                    image=image_path, 
                    confidence=confidence,
                    grayscale=False,
                    region=window_region    # 指定搜索区域
                )
                if pic_region is not None:
                    local_pic_x = int(pic_region.left + pic_region.width / 2 - current_window_x)
                    local_pic_y = int(pic_region.top + pic_region.height / 2 - current_window_y) 
                    bbox_left = pic_region.left - current_window_x
                    bbox_top = pic_region.top - current_window_y
                    bbox_right = pic_region.left + pic_region.width - current_window_x
                    bbox_bottom = pic_region.top + pic_region.height - current_window_y
                    self.window_manager.saveBboxImage(self.hwnd, Bbox(bbox_left, bbox_top, bbox_right, bbox_bottom))
                    
                    # 如果是重试成功的，打印提示信息
                    if attempt > 0:
                        print(f"[图像识别] 第{attempt + 1}次尝试成功找到图像")
                    
                    return Point(local_pic_x, local_pic_y)
                else:
                    # 图像未找到，如果还有重试机会，继续尝试
                    if attempt < max_retries - 1:
                        if is_print:
                            print(f"[图像识别] 第{attempt + 1}次未找到图像，{retry_interval}秒后重试...")
                        time.sleep(retry_interval)
                        continue
                    
            except Exception as e:
                last_exception = e
                # 如果还有重试机会，继续尝试
                if attempt < max_retries - 1:
                    if is_print:
                        print(f"[图像识别] 第{attempt + 1}次识别出错: {e}，{retry_interval}秒后重试...")
                    time.sleep(retry_interval)
                    continue
        
        # 所有重试都失败了，打印最终错误信息
        if is_print:
            if last_exception:
                print(f"获取图片中心位置失败: {last_exception}")
            else:
                print(f"获取图片中心位置失败: 未找到图像（已重试{max_retries}次）")
        
        return None
    
    def getImageBbox(self, image_path:str, confidence:float = 0.8, is_print:bool = True, max_retries:int = 3, retry_interval:float = 0.5):
        """
        获取图片在窗口坐标系下的bbox
        Args:
            image_path: 图片路径
            confidence: 置信度
            is_print: 是否打印错误信息
            max_retries: 最大重试次数（默认3次）
            retry_interval: 重试间隔秒数（默认0.5秒）
        Returns:
            Bbox: 图片bbox
            None: 未找到图片
        """
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                # 动态获取当前窗口位置，而不是使用缓存的位置
                window_rect = self.window_manager.getWindowRect(self.hwnd)
                current_window_x = window_rect[0]
                current_window_y = window_rect[1]
                current_window_width = window_rect[2] - window_rect[0]
                current_window_height = window_rect[3] - window_rect[1]
                
                window_region = (current_window_x, current_window_y, current_window_width, current_window_height)
                pic_region = pyautogui.locateOnScreen(
                    image=image_path, 
                    confidence=confidence,
                    grayscale=False,
                    region=window_region    # 指定搜索区域
                )
                if pic_region is not None:
                    bbox_left = pic_region.left - current_window_x
                    bbox_top = pic_region.top - current_window_y
                    bbox_right = pic_region.left + pic_region.width - current_window_x
                    bbox_bottom = pic_region.top + pic_region.height - current_window_y
                    self.window_manager.saveBboxImage(self.hwnd, Bbox(bbox_left, bbox_top, bbox_right, bbox_bottom))
                    
                    # 如果是重试成功的，打印提示信息
                    if attempt > 0:
                        print(f"[图像识别] 第{attempt + 1}次尝试成功找到图像")
                    
                    return Bbox(bbox_left, bbox_top, bbox_right, bbox_bottom)
                else:
                    # 图像未找到，如果还有重试机会，继续尝试
                    if attempt < max_retries - 1:
                        if is_print:
                            print(f"[图像识别] 第{attempt + 1}次未找到图像，{retry_interval}秒后重试...")
                        time.sleep(retry_interval)
                        continue
                        
            except Exception as e:
                last_exception = e
                # 如果还有重试机会，继续尝试
                if attempt < max_retries - 1:
                    if is_print:
                        print(f"[图像识别] 第{attempt + 1}次识别出错: {e}，{retry_interval}秒后重试...")
                    time.sleep(retry_interval)
                    continue
        
        # 所有重试都失败了，打印最终错误信息
        if is_print:
            if last_exception:
                print(f"获取图片bbox失败: {last_exception}")
            else:
                print(f"获取图片bbox失败: 未找到图像（已重试{max_retries}次）")
        
        return None


if __name__ == "__main__":
    pass
        
        

    
        








