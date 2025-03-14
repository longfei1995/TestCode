import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.animation as animation
import math
# qt5
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 1代表彩色，0是灰度图，-1包含透明通道的彩色图
img_bgr = cv2.imread(os.path.join(current_dir, "bgr.png"), 1)
img_lena = cv2.imread(os.path.join(current_dir, "lena.png"), 1)

def showOpenCVImage(img):
    # opencv中是以BGR为顺序的，而matplotlib中是以RGB为顺序的
    # 所以需要将BGR转换为RGB
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.title("Image Show RGB")
    plt.imshow(img2)
    plt.show()

# 创建动画
if __name__ == "__main__":
    # 显示原始图像
    # showOpenCVImage(img_lena)
    
    # 转换为灰度图
    gray_lena = cv2.cvtColor(img_lena, cv2.COLOR_BGR2GRAY)
    
    # 固定阈值法
    ret1, thresh1 = cv2.threshold(gray_lena, 127, 255, cv2.THRESH_BINARY)
    # otsu阈值法
    ret2, thresh2 = cv2.threshold(gray_lena, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 先高斯滤波，再阈值分割
    blur = cv2.GaussianBlur(gray_lena, (5, 5), 0)
    ret3, thresh3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 用 Matplotlib 把原图, 阈值图都显示出来
    plt.subplot(2, 2, 1), plt.imshow(gray_lena, cmap='gray')
    plt.title('original image')
    plt.subplot(2, 2, 2), plt.imshow(thresh1, cmap='gray')
    plt.title('fixed threshold')
    plt.subplot(2, 2, 3), plt.imshow(thresh2, cmap='gray')
    plt.title('Otsu threshold')
    plt.subplot(2, 2, 4), plt.imshow(thresh3, cmap='gray')
    plt.title('Gaussian blur threshold')
    plt.show()
    
    














