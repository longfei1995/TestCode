import os
import sys
import warnings
import logging

# 解决OpenMP库冲突问题
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 关闭各种警告和输出
warnings.filterwarnings('ignore')  # 关闭所有警告
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 关闭TensorFlow日志
os.environ['PADDLEOCR_DEBUG'] = 'False'  # 关闭PaddleOCR调试信息

# 设置日志级别为ERROR，只显示错误信息
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger('ppocr').setLevel(logging.ERROR)
logging.getLogger('paddle').setLevel(logging.ERROR)

# 临时重定向stdout来关闭初始化时的输出
class SuppressOutput:
    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._stdout
        sys.stderr = self._stderr

import win32gui
from PIL import Image, ImageGrab
import numpy as np
from typing import Tuple, Optional, List, Dict, Any
from datetime import datetime

# 使用上下文管理器来静默导入PaddleOCR
with SuppressOutput():
    from paddleocr import PaddleOCR

from window_manager import WindowManager

class TextOCR:
    """文字识别器 - 基于PaddleOCR"""
    
    def __init__(self):
        """初始化文字识别器"""
        # 静默初始化PaddleOCR
        with SuppressOutput():
            self.paddle_ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
        print("文字识别器初始化完成")
    
    def captureWindow(self, hwnd: int, x: int, y: int, width: int, height: int) -> Optional[Image.Image]:
        """
        截取窗口区域
        Args:
            hwnd: 窗口句柄
            x: 相对于窗口的X坐标偏移（默认0）
            y: 相对于窗口的Y坐标偏移（默认0）
            width: 截图宽度
            height: 截图高度
        Returns:
            PIL Image对象或None
        """
        try:
            # 获取窗口位置
            window_rect = win32gui.GetWindowRect(hwnd)
            window_x, window_y = window_rect[0], window_rect[1]
            
            # 计算截图区域（转换为屏幕坐标）
            left = window_x + x
            top = window_y + y
            right = left + width
            bottom = top + height
            
            # 截图
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            print(f"截图区域: ({left}, {top}, {right}, {bottom})")
            
            # 保存截图（可选）
            current_dir = os.path.dirname(os.path.abspath(__file__))
            pics_dir = os.path.join(current_dir, "pics")
            if not os.path.exists(pics_dir):
                os.makedirs(pics_dir)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = os.path.join(pics_dir, f"ocr_screenshot_{timestamp}.png")
            screenshot.save(screenshot_path)
            print(f"截图已保存到: {screenshot_path}")
            
            return screenshot
        except Exception as e:
            print(f"截取窗口区域失败: {e}")
            return None
    
    def extractTextFromImage(self, image: Image.Image) -> Dict[str, Any]:
        """
        从图像中提取文字
        Args:
            image: PIL Image对象
        Returns:
            Dict: 包含识别结果的字典
        """
        try:
            # 将PIL Image对象转换为PaddleOCR的输入格式numpy数组
            image_array = np.array(image)
            
            # 静默执行OCR识别
            with SuppressOutput():
                ocr_result = self.paddle_ocr.ocr(image_array, cls=True)
            
            # 设置置信度阈值
            confidence_threshold = 0.5
            high_confidence_texts = []
            
            # 处理识别结果
            for idx in range(len(ocr_result)):
                res = ocr_result[idx]
                if res is None:
                    continue
                    
                for line in res:
                    text = line[1][0]
                    confidence = line[1][1]
                    # 只保留置信度大于阈值的文字
                    if confidence > confidence_threshold:
                        high_confidence_texts.append(text)
            
            # 生成所有文字的集合字符串
            all_text = ' '.join(high_confidence_texts)
            
            result = {
                'success': True,
                'all_text': all_text,
            }
            return result
            
        except Exception as e:
            print(f"文字识别失败: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def extractTextFromWindow(self, hwnd: int, x: int, y: int, width: int, height: int) -> Dict[str, Any]:
        """
        从窗口截图并提取文字
        Args:
            hwnd: 窗口句柄
            x: 相对于窗口的X坐标偏移（默认0）
            y: 相对于窗口的Y坐标偏移（默认0）
            width: 截图宽度
            height: 截图高度
        Returns:
            Dict: 包含识别结果的字典
        """
        # 先截取窗口
        image = self.captureWindow(hwnd, x, y, width, height)
        if image is None:
            return {
                'success': False,
                'error': '截图失败'
            }
        
        # 提取文字并返回结果
        return self.extractTextFromImage(image)

# 使用示例
if __name__ == "__main__":
    # 获取当前窗口句柄
    window_manager = WindowManager()
    hwnd = window_manager.selectWindow()
    if hwnd is None:
        print("未选择窗口")
        exit()
    
    # 打印窗口位置和大小
    window_rect = win32gui.GetWindowRect(hwnd)
    print(f"窗口位置: ({window_rect[0]}, {window_rect[1]})")
    print(f"窗口大小: {window_rect[2] - window_rect[0]}x{window_rect[3] - window_rect[1]}")
    
    # 文字识别
    ocr = TextOCR()
    result = ocr.extractTextFromWindow(hwnd, 0, 0, window_rect[2] - window_rect[0], window_rect[3] - window_rect[1])
    if result['success']:
        print(f"识别结果:{result['all_text']}")
    else:
        print(f"识别失败: {result['error']}")
    
