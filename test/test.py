import cv2
import os
import numpy as np
print(cv2.__version__)

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "lena.png")
# 1代表彩色，0是灰度图，-1包含透明通道的彩色图
img = cv2.imread(os.path.join(current_dir, "bgr.png"),1)


# 蓝色的范围
lower_blue = np.array([100,110,110])
upper_blue = np.array([130,255,255])


hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# inRange(): 介于lower_blue和upper_blue之间的颜色是白色，其余是黑色
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# 将mask和img进行按位与运算，得到蓝色部分
res = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("img", img)
cv2.imshow("mask", mask)
cv2.imshow("res", res)

cv2.waitKey(0)
cv2.destroyAllWindows()




















cv2.waitKey(0)
cv2.destroyAllWindows()













