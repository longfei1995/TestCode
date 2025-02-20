import pyautogui
import pyperclip
import random
import time
import os


# 鼠标点击函数合集
def mouseMoveAndOnceClicked(screen_x, screen_y):
    """模拟人类真实点击操作，在按下和抬起之间添加随机延迟
    
    Args:
        screen_x (int): 屏幕x坐标
        screen_y (int): 屏幕y坐标
    """
    # 加入随机的像素
    screen_x += random.randint(-5, 5)
    screen_y += random.randint(-5, 5)
    
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

def keyPress(key):
    pyautogui.keyDown(key)
    time.sleep(random.uniform(0.05, 0.15))
    pyautogui.keyUp(key)

def chatWithSomeone(message):
    pyperclip.copy(message)
    time.sleep(0.1)  # 确保复制完成
    pyautogui.hotkey('ctrl', 'v')  # 这里保留hotkey因为是组合键
    time.sleep(0.1)  # 确保粘贴完成
    keyPress('enter')  # 使用自定义的keyPress函数

def findPicCenterPos(pic_name:str, find_times:int = 3, confidence: float = 0.8):
    """查找图片并返回其中心位置
    Args:
        pic_name (str): 图片名字
        find_times (int): 最大查找次数
        confidence (float): 置信度
    Returns:
        tuple: (bool, Point对象) - (是否找到图片, 图片中心坐标[未找到时为None])
    """
    # 组合绝对路径
    current_py_file_path = os.path.abspath(__file__)
    pic_path = os.path.join(os.path.dirname(current_py_file_path), "pics", pic_name)
    
    for _ in range(find_times):
        try:
            # locateCenterOnScreen 返回 Point(x, y) 或 None
            position = pyautogui.locateCenterOnScreen(pic_path, confidence=confidence)
            if position is not None:
                return True, position
        except Exception as e:
            print(f'查找图片{pic_path}失败：{str(e)}')
    
    return False, None

def test01():
    # 获取用户输入的文本
    user_input = pyautogui.prompt('请在方框内输入你想说的话, 如：/ 燕京啤酒 你好')
    # 测试代码1，处理用户输入
    if user_input is not None:
        # 处理用户输入
        mouse_position = pyautogui.Point(-1601, 136)
        mouseMoveAndOnceClicked(mouse_position.x, mouse_position.y)
        chatWithSomeone(user_input)
    else:
        print('用户取消了输入')

def test02(pic_name:str):
    # 查找图片并且点击
    find_pic_succ, pic_position = findPicCenterPos(pic_name, 1, 0.8)
    if find_pic_succ:
        print(f'找到路径为：{pic_name}的图片，位置为：{pic_position}')
    else:
        print(f'未找到路径为：{pic_name}的图片')
    if find_pic_succ:
        mouseMoveAndOnceClicked(pic_position.x, pic_position.y)
    


if __name__ == '__main__':
    # 获取当前鼠标位置
    for i in range(10):
        mouse_position = pyautogui.position()
        print(mouse_position)
        time.sleep(1)
    
    
    # 1. 变量定义
    kScreenSize = pyautogui.size()
    print(kScreenSize)
    # scene_dict: dict = {
    #     "number_8": "number_8.png",
    #     "person": "person.png",
    # }
    # test02(scene_dict["person"])
    
    
    
    
    

