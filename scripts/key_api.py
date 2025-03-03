import pyautogui
import pyperclip
import random
import time
import os
import pygetwindow as gw  # 需要安装：pip install pygetwindow
from PIL import ImageGrab
import win32gui
import win32con
import win32ui
from ctypes import windll
import win32api
import win32process
import keyboard
import numpy as np
kRegionAllScreen = (1, 24, 2550, 1366)          # 全屏
kRegionRightPosition = (2288, 13, 262, 61)      # 右上角的场景位置
kRegionMonsterWindow = (248, 25, 308, 216)    # 怪物选中后区域
kRegionBloodBarPosition = (271, 44, 139, 16)    # 血条区域

# 按键
kKeyAutoAttack = 'w'
kKeyAutoSelect = 'q'

class GameHelper:
    def __init__(self):
        """初始化GameHelper类"""
        pass
        
    def mouseMoveAndOnceClicked(self, screen_x, screen_y):
        """模拟人类真实点击操作，在按下和抬起之间添加随机延迟
    
    Args:
        screen_x (int): 屏幕x坐标
        screen_y (int): 屏幕y坐标
    """
        # 使用高斯分布添加随机像素偏移，更接近人类行为
        screen_x += int(random.gauss(0, 2))
        screen_y += int(random.gauss(0, 2))
        
        # 移动鼠标到目标位置，使用高斯分布的随机时间
        move_duration = max(0.1, random.gauss(0.2, 0.05))
        pyautogui.moveTo(screen_x, screen_y, duration=move_duration)
        
        # 短暂停顿，模拟人类反应，使用高斯分布
        time.sleep(max(0.01, random.gauss(0.07, 0.02)))
        
        # 按下鼠标左键
        pyautogui.mouseDown(button='left')
        
        # 随机按住时间，使用高斯分布
        time.sleep(max(0.01, random.gauss(0.1, 0.03)))
        
        # 释放鼠标左键
        pyautogui.mouseUp(button='left')
        
        # 操作完成后的随机短暂停顿，使用高斯分布
        time.sleep(max(0.05, random.gauss(0.15, 0.03)))

    def keyPress(self, key):
        # 使用高斯分布的随机按键时间
        pyautogui.keyDown(key)
        time.sleep(max(0.02, random.gauss(0.1, 0.03)))
        pyautogui.keyUp(key)
        # 添加按键后的随机延迟
        time.sleep(max(0.01, random.gauss(0.05, 0.01)))

    def chatWithSomeone(self, message):
        pyperclip.copy(message)
        # 使用高斯分布的随机延迟替换固定延迟
        time.sleep(max(0.05, random.gauss(0.1, 0.02)))  # 确保复制完成
        
        # 模拟组合键的随机延迟
        pyautogui.keyDown('ctrl')
        time.sleep(max(0.01, random.gauss(0.05, 0.01)))
        pyautogui.keyDown('v')
        time.sleep(max(0.01, random.gauss(0.05, 0.01)))
        pyautogui.keyUp('v')
        time.sleep(max(0.01, random.gauss(0.03, 0.01)))
        pyautogui.keyUp('ctrl')
        
        # 确保粘贴完成后的随机延迟
        time.sleep(max(0.05, random.gauss(0.1, 0.02)))
        self.keyPress('enter')  # 使用自定义的keyPress函数

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
        
        for i in range(find_times):
            try:
                # 每次尝试之间添加随机延迟
                if i > 0:
                    time.sleep(max(0.1, random.gauss(0.3, 0.1)))
                    
                # 小幅度随机调整置信度以增加随机性
                actual_confidence = min(0.99, max(0.5, confidence + random.gauss(0, 0.02)))
                
                # locateCenterOnScreen 返回 Point(x, y) 或 None
                position = pyautogui.locateOnScreen(image=pic_path, confidence=actual_confidence, grayscale=False)
                if position is not None:
                    center_position = pyautogui.center(position)
                    print(f"找到图片{pic_path}，位置为：{center_position}")
                    return True, center_position
            except Exception as e:
                pass
        print(f"未找到图片{pic_path}")
        return False, None

    def findPicInRegion(self, pic_name:str, region:tuple, find_times:int = 3, confidence: float = 0.8, is_need_save_debug_image:bool = False):
        """在指定区域内查找图片并返回其中心位置
        Args:
            pic_name (str):     图片名字,如person.png
            region (tuple):     搜索区域 (left, top, width, height)
            find_times (int):   最大查找次数
            confidence (float): 置信度
        Returns:
            tuple: (bool, Point对象) - (是否找到图片, 图片中心坐标[未找到时为None])
        """
        # 先将搜索区域保存为debug.png用于调试
        if is_need_save_debug_image:
            self.save_region_debug_image(region)
            
        # 组合绝对路径
        current_py_file_path = os.path.abspath(__file__)
        pic_path = os.path.join(os.path.dirname(current_py_file_path), "pics", pic_name)
        
        for i in range(find_times):
            try:
                # 在指定区域内查找图片
                position = pyautogui.locateOnScreen(
                    image=pic_path, 
                    confidence=confidence, 
                    grayscale=False,
                    region=region  # 指定搜索区域
                )
                
                if position is not None:
                    center_position = pyautogui.center(position)
                    print(f"找到图片{pic_path}，位置为：{center_position}")
                    return True, center_position
            except Exception as e:
                pass
        
        print(f"在指定区域{region}内未找到图片{pic_path}")
        return False, None

    def getScreenRegion(self):
        """交互式获取屏幕区域
        用户可以通过鼠标选择区域的左上角和右下角
        Returns:
            tuple: 区域坐标 (left, top, width, height)
        """
        print("请将鼠标移动到要选择区域的左上角，然后按下空格键...")
        while True:
            if keyboard.is_pressed('space'):  # 需要安装keyboard库: pip install keyboard
                start_x, start_y = pyautogui.position()
                print(f"已选择左上角坐标: ({start_x}, {start_y})")
                time.sleep(0.5)  # 防止连续按键
                break
        
        print("请将鼠标移动到要选择区域的右下角，然后按下空格键...")
        while True:
            if keyboard.is_pressed('space'):
                end_x, end_y = pyautogui.position()
                print(f"已选择右下角坐标: ({end_x}, {end_y})")
                break
        
        width = end_x - start_x
        height = end_y - start_y
        region = (start_x, start_y, width, height)
        print(f"选择的区域: {region}")
        return region

    def isInDiFuAndEscape(self):
        # 判断是否在地府
        is_in_di_fu, pic_position = self.findPicInRegion("pos_di_fu.png", kRegionRightPosition, 3, 0.9)
        if is_in_di_fu:
            print(f"现在时间是{time.strftime('%Y-%m-%d %H:%M:%S')}，在地府")
            # 开始逃离地府
            is_find_pic, pic_position = self.findPicInRegion("di_fu.png", kRegionAllScreen, 3, 0.7)
            if is_find_pic and pic_position is not None:
                self.mouseMoveAndOnceClicked(pic_position.x, pic_position.y)
                print("逃离地府成功")
            else:
                print("未找到地府光圈, 逃离失败")
        else:
            print("不在地府")
        

    def listWindowsAndActivate(self):
        """列出所有活动窗口并允许用户选择一个激活到前台"""
        try:
            # 获取所有窗口
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                    windows.append((hwnd, win32gui.GetWindowText(hwnd)))
                return True
            
            windows = []
            win32gui.EnumWindows(callback, windows)
            active_windows = [(hwnd, title) for hwnd, title in windows if title.strip()]
            
            # 显示窗口列表
            print("\n可用窗口列表:")
            for i, (_, win_title) in enumerate(active_windows):
                print(f"{i+1}. {win_title}")
            
            # 让用户选择
            choice = int(input("\n请选择要激活的窗口编号: "))
            if 1 <= choice <= len(active_windows):
                hwnd, window_title = active_windows[choice-1]
                print(f"正在尝试激活窗口: {window_title}")
                
                # 增强的窗口激活方法，特别针对游戏窗口
                try:
                    # 方法1：尝试常规方式
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(hwnd)
                    print("窗口已通过常规方式激活")
                except Exception as e1:
                    print(f"常规激活方式失败: {e1}")
                    try:
                        # 方法2：使用AttachThreadInput方法
                        current_thread = win32api.GetCurrentThreadId()
                        target_thread = win32process.GetWindowThreadProcessId(hwnd)[0]
                        win32process.AttachThreadInput(current_thread, target_thread, True)
                        win32gui.BringWindowToTop(hwnd)
                        win32gui.SetForegroundWindow(hwnd)
                        win32process.AttachThreadInput(current_thread, target_thread, False)
                        print("窗口已通过线程附加方式激活")
                    except Exception as e2:
                        print(f"线程附加激活方式失败: {e2}")
                        try:
                            # 方法3：使用SendMessage模拟点击窗口标题栏
                            win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
                            win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
                            print("窗口已通过SendMessage方式激活")
                        except Exception as e3:
                            print(f"SendMessage激活方式失败: {e3}")
                            # 方法4：模拟Alt+Tab切换
                            print("尝试通过模拟Alt+Tab切换到目标窗口")
                            pyautogui.keyDown('alt')
                            time.sleep(0.2)
                            pyautogui.press('tab')
                            for _ in range(choice):  # 根据窗口编号按下对应次数的Tab
                                time.sleep(0.1)
                                pyautogui.press('tab')
                            time.sleep(0.2)
                            pyautogui.keyUp('alt')
                
                # 等待短暂时间确认窗口激活
                time.sleep(0.5)
                # 检查当前活动窗口是否是目标窗口
                try:
                    current_active_hwnd = win32gui.GetForegroundWindow()
                    active_title = win32gui.GetWindowText(current_active_hwnd)
                    if window_title in active_title or active_title in window_title:
                        print(f"确认窗口已激活: {active_title}")
                        return True
                    else:
                        print(f"警告：可能未成功激活目标窗口。当前活动窗口: {active_title}")
                        return True  # 仍然返回True，让程序继续执行
                except:
                    # 如果检查失败，仍然假设激活成功
                    print("无法确认窗口激活状态，继续执行")
                    return True
            else:
                print("无效的选择")
                return False
        except Exception as e:
            print(f"窗口操作过程中出错: {e}")
            return False
        
    def save_region_debug_image(self, region):
        """保存区域的截图用于调试
        
        Args:
            region (tuple): 要截图的区域 (left, top, width, height)
        """
        try:
            # 确保pics目录存在
            script_dir = os.path.dirname(os.path.abspath(__file__))
            pics_dir = os.path.join(script_dir, "pics")
            if not os.path.exists(pics_dir):
                os.makedirs(pics_dir)
            
            # 截取区域图像
            screenshot = pyautogui.screenshot(region=region)
            
            # 保存图像
            debug_file_path = os.path.join(pics_dir, "debug.png")
            screenshot.save(debug_file_path)
            print(f"已保存区域截图到: {debug_file_path}")
        except Exception as e:
            print(f"保存区域截图时出错: {e}")
    
    
    def is_monster_alive(self):
        # 检查怪物是否存活
        # 截取血条区域的图像
        screenshot = pyautogui.screenshot(region=kRegionBloodBarPosition)
        # self.save_region_debug_image(kRegionBloodBarPosition)
        # 转换为RGB数组进行分析
        img_array = np.array(screenshot)
        # 计算红色像素的数量 (R值高，G和B值低的像素)
        red_pixels = np.sum((img_array[:,:,0] > 150) & (img_array[:,:,1] < 80) & (img_array[:,:,2] < 80))
        # 设定阈值判断是否存在怪物
        is_monster_alive = red_pixels > 100  # 阈值可能需要调整
        return is_monster_alive

    def autoFight(self):
        """简化版自动战斗功能 - 基于固定位置的血条检测
        """
        while True:
            # 先选取怪物，看是不是选中了
            self.keyPress(kKeyAutoSelect)
            has_monster, pic_position = self.findPicInRegion("monster_target.png", kRegionMonsterWindow, 3, 0.7)
            if has_monster:
                attack_once = True
                while True:
                    is_monster_alive = self.is_monster_alive()
                    if is_monster_alive:
                        # 怪物存活，则进行自动攻击
                        if attack_once:
                            self.keyPress(kKeyAutoAttack)
                            print("有怪物 && 怪物有血量攻击一次")
                            attack_once = False
                    else:
                        break
            else:
                # 没有选中怪物，则进入下一次循环
                time.sleep(max(0.1, random.gauss(0.3, 0.1)))
                continue
        

def test02():
    # 获取屏幕区域
    game_helper = GameHelper()
    # game_helper.listWindowsAndActivate()
    region = game_helper.getScreenRegion()  
    print(region)
    
def test03():
    game_helper = GameHelper()
    is_find_pic, pic_position = game_helper.findPicInRegion("xiao_yao.png", kRegionRightPosition, 3, 0.9, True)
    if is_find_pic:
        time.sleep(5)
        game_helper.autoFight()
    else:
        print("不在战斗场景")
if __name__ == '__main__':
    test03()



    

