import pyautogui
import random
import time

# 获取当前屏幕的坐标最大值
kScreenSize = pyautogui.size()


# pyautogui.moveTo(kScreenSize.width, kScreenSize.height, 2)
pyautogui.dragTo(kScreenSize.width, kScreenSize.height, 2)

# 鼠标点击函数合集
def leftSingleClick(screen_x, screen_y):
    """模拟人类真实点击操作，在按下和抬起之间添加随机延迟
    
    Args:
        screen_x (int): 屏幕x坐标
        screen_y (int): 屏幕y坐标
    """
    # 移动鼠标到目标位置，使用0.1-0.3秒的随机时间，模拟自然移动
    pyautogui.moveTo(screen_x, screen_y, duration=random.uniform(0.1, 0.3))
    
    # 短暂停顿，模拟人类反应
    time.sleep(random.uniform(0.05, 0.1))
    
    # 按下鼠标左键
    pyautogui.mouseDown(button='left')
    
    # 随机按住时间，范围在0.05-0.15秒之间
    time.sleep(random.uniform(0.05, 0.15))
    
    # 释放鼠标左键
    pyautogui.mouseUp(button='left')
    
    # 操作完成后的随机短暂停顿
    time.sleep(random.uniform(0.1, 0.2))

