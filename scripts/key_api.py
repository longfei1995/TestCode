import pyautogui
import pyperclip
import random
import time
import os

class GameHelper:
    def __init__(self):
        """初始化GameHelper类"""
        self.scene_dict = {
            "number_8": "number_8.png",
            "person": "person.png",
            "sea": "sea.png",
        }
        
    def mouseMoveAndOnceClicked(self, screen_x, screen_y):
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

    def keyPress(self, key):
        pyautogui.keyDown(key)
        time.sleep(random.uniform(0.05, 0.15))
        pyautogui.keyUp(key)

    def chatWithSomeone(self, message):
        pyperclip.copy(message)
        time.sleep(0.1)  # 确保复制完成
        pyautogui.hotkey('ctrl', 'v')  # 这里保留hotkey因为是组合键
        time.sleep(0.1)  # 确保粘贴完成
        self.keyPress('enter')  # 使用自定义的keyPress函数

    def findPicCenterPos(self, pic_name:str, find_times:int = 3, confidence: float = 0.8):
        """查找图片并返回其中心位置
        Args:
            pic_name (str):     图片名字,如person.png
            find_times (int):   最大查找次数
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
                position = pyautogui.locateOnScreen(image=pic_path, confidence=confidence, grayscale=False)
                if position is not None:
                    center_position = pyautogui.center(position)
                    print(f"找到图片{pic_path}，位置为：{center_position}")
                    return True, center_position
            except Exception as e:
                pass
        print(f"未找到图片{pic_path}")
        return False, None

        
if __name__ == '__main__':
    game_helper = GameHelper()
    is_find_pic, pic_position = game_helper.findPicCenterPos(game_helper.scene_dict["sea"], 1, 0.8)
    if is_find_pic and pic_position is not None:
        game_helper.mouseMoveAndOnceClicked(pic_position.x, pic_position.y)
    




    

