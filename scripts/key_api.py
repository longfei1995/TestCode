# 设置OpenMP环境变量（解决多个OpenMP运行时的冲突问题）
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 操作系统和时间相关
import time
import glob
# 随机数生成
import random
# 屏幕操作相关
import pyautogui
import pyperclip
import keyboard
# 数据处理和OCR
import numpy as np
import easyocr
import cv2

# 指定搜索区域, 如果换了分辨率，还需用test01()重新获取， 见pics/example文件夹下的示例
kRegionAllScreen = (1, 24, 2550, 1366)          # 全屏
kRegionRightPosition = (2380, 26, 156, 50)      # 右上角的场景位置
kRegionMonsterWindow = (248, 25, 308, 216)      # 怪物选中后区域
kRegionBloodBarPosition = (271, 44, 139, 16)    # 血条区域
kRegionMiniMap = (2371, 78, 185, 154)           # 小地图区域
kRegionBBHappyBall = (1385, 1296, 36, 29)       # 珍兽快乐球位置
kRegionBBDrag = (1421, 1296, 37, 28)            # 珍兽吃药位置
kRegionAutoFind = (2357, 229, 196, 322)         # 自动寻路区域  
kRegionYiZhanLeftDiag = (1, 178, 282, 393)      # 驿站左侧框位置
# 按键
kKeyAutoAttack = 'e'
kKeyAutoSelect = 'q'
# 场景列表字典, confidence代表小地图是否有怪物的置信度
kYiZhanList = {
    "qi_ta_men_pai": "da_li\\4.png",
    "ming_jiao": "da_li\\5.png",
}

class GameHelper:
    def __init__(self):
        """初始化GameHelper类"""
        self.current_file_path_ = os.path.dirname(os.path.abspath(__file__))
                
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
        time.sleep(max(0.01, random.gauss(0.05, 0.03)))
        
        # 释放鼠标左键
        pyautogui.mouseUp(button='left')
        
        # 操作完成后的随机短暂停顿，使用高斯分布
        time.sleep(max(0.05, random.gauss(0.15, 0.03)))

    def mouseMoveAndDoubleClicked(self, screen_x, screen_y):
        # 添加随机偏移
        screen_x += int(random.gauss(0, 2))
        screen_y += int(random.gauss(0, 2))
        
        # 移动鼠标到目标位置
        move_duration = max(0.1, random.gauss(0.2, 0.05))
        pyautogui.moveTo(screen_x, screen_y, duration=move_duration)
        
        # 第一次点击
        pyautogui.mouseDown(button='left')
        time.sleep(0.01)  # 极短按下时间
        pyautogui.mouseUp(button='left')
        
        # 控制两次点击间间隔时间（非常短）
        time.sleep(max(0.01, random.gauss(0.05, 0.01)))  # 50ms左右的间隔
        
        # 第二次点击
        pyautogui.mouseDown(button='left')
        time.sleep(0.01)  # 极短按下时间
        pyautogui.mouseUp(button='left')
        
        # 操作后随机延迟
        time.sleep(max(0.05, random.gauss(0.15, 0.03)))

    def keyPress(self, key):
        # 使用高斯分布的随机按键时间
        # pyautogui.keyDown(key)
        # time.sleep(max(0.01, random.gauss(0.1, 0.03)))
        # pyautogui.keyUp(key)
        # # 添加按键后的随机延迟
        # time.sleep(max(0.01, random.gauss(0.05, 0.01)))
        pyautogui.press(key)
        time.sleep(max(0.01, random.gauss(0.05, 0.01)))

    def typeNumber(self, number:str):
        """输入数字"""
        # 按数字前按三下删除
        for _ in range(3):
            pyautogui.press('backspace')
            time.sleep(max(0.01, random.gauss(0.05, 0.01)))
        # 输入数字
        for char in number:
            pyautogui.typewrite(char)
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

    def findPicInRegion(self, pic_name:str, region:tuple, confidence: float = 0.8, is_need_save_debug_image:bool = False):
        """在指定区域内查找图片并返回其Region
        Args:
            pic_name (str):     图片名字,如person.png
            region (tuple):     搜索区域 (left, top, width, height)
            confidence (float): 置信度
        Returns:
            tuple: (bool, Region对象) - (是否找到图片, 图片Region[未找到时为None])
        """
        # 先将搜索区域保存为debug.png用于调试
        if is_need_save_debug_image:
            self.saveRegionImage(region)
            
        # 组合绝对路径
        pic_path = os.path.join(self.current_file_path_, "pics", pic_name)
        
        try:
            # 在指定区域内查找图片
            pic_region = pyautogui.locateOnScreen(
                image=pic_path, 
                confidence=confidence, 
                grayscale=False,
                region=region  # 指定搜索区域
            )
            
            if pic_region is not None:
                return True, pic_region
        except Exception as e:
            pass
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
        is_in_di_fu = self.isInScene("di_fu\\1.png", confidence=0.9)
        if is_in_di_fu:
            print(f"现在时间是{time.strftime('%Y-%m-%d %H:%M:%S')}，在地府")
            # 开始逃离地府
            is_find_pic, pic_region = self.findPicInRegion("di_fu\\2.png", kRegionAllScreen, confidence=0.7)
            if is_find_pic and pic_region is not None:
                pic_center_position = self.getRegionCenter(pic_region)
                self.mouseMoveAndOnceClicked(pic_center_position.x, pic_center_position.y)
                print("逃离地府成功")
                # 等待15s
                time.sleep(15)
                return True
            else:
                print("未找到地府光圈, 逃离失败")      
        else:
            print("不在地府")
        return False
    
    def getRegionCenter(self, region):
        """获取区域的中心坐标"""
        return pyautogui.center(region)
    
    def saveRegionImage(self, region):
        """保存区域的截图
        Args:
            region (tuple): 要截图的区域 (left, top, width, height)
        Returns:
            PIL.Image.Image: 截图的PIL Image对象
        """
        try:
            # 确保pics目录存在
            save_pics_dir = os.path.join(self.current_file_path_, "pics\\debug")
            if not os.path.exists(save_pics_dir):
                os.makedirs(save_pics_dir)
            
            # 截取区域图像
            screenshot = pyautogui.screenshot(region=region)
            
            # 保存图像
            current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            debug_file_path = os.path.join(save_pics_dir, f"debug_{current_time}.png")
            screenshot.save(debug_file_path)
            
            # 检查并限制图片数量为10张
            debug_files = glob.glob(os.path.join(save_pics_dir, "debug_*.png"))
            
            # 如果图片超过10张，则删除最早的图片
            if len(debug_files) > 10:
                # 按文件创建时间排序
                debug_files.sort(key=os.path.getctime)
                # 删除最早的文件(们)，直到剩下10张
                for old_file in debug_files[:-10]:
                    os.remove(old_file)
            return screenshot, debug_file_path
                    
        except Exception as e:
            print(f"保存区域截图时出错: {e}")
            return None, None

    def isMonsterAlive(self):
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
    
    def isMonsterInMiniMap(self, confidence):
        """检查小地图是否存在怪物"""
        # 使用findPicInRegion方法来查找预先截取的绿色怪物点图像
        has_monster, _ = self.findPicInRegion("monster_dot.png", kRegionMiniMap, confidence=confidence, is_need_save_debug_image=False)
        return has_monster
    
    def babyEat(self):
        """宝宝吃药，吃快乐球"""
        # 点击宝宝药
        self.mouseMoveAndOnceClicked(self.getRegionCenter(kRegionBBDrag).x, self.getRegionCenter(kRegionBBDrag).y)
        # self.save_region_debug_image(kRegionBBDrag)
        print("点击宝宝吃药")
        time.sleep(max(0.1, random.gauss(0.2, 0.05)))
        # 点击快乐球
        self.mouseMoveAndOnceClicked(self.getRegionCenter(kRegionBBHappyBall).x, self.getRegionCenter(kRegionBBHappyBall).y)
        # self.save_region_debug_image(kRegionBBHappyBall)
        print("点击宝宝吃快乐球")
        time.sleep(max(0.1, random.gauss(0.2, 0.05)))

    def autoFightOnce(self, confidence:float = 0.7):
        """简化版自动战斗功能 - 基于固定位置的血条检测
        """
        # 先选取怪物，看是不是选中了
        self.keyPress(kKeyAutoSelect)
        print(f"选择怪物{kKeyAutoSelect}")
        time.sleep(max(0.1, random.gauss(0.2, 0.05)))
        has_select_target, _ = self.findPicInRegion("monster_target.png", kRegionMonsterWindow, confidence=confidence, is_need_save_debug_image=False)
        if has_select_target:
            attack_once = True
            # 添加开始时间和最大战斗时间
            start_time = time.time()
            max_fight_time = 3  # 最多战斗3秒
            
            while time.time() - start_time < max_fight_time:
                is_monster_alive = self.isMonsterAlive()
                if is_monster_alive:
                    # 怪物存活，则进行自动攻击
                    if attack_once:
                        self.keyPress(kKeyAutoAttack)
                        print(f"攻击一次{kKeyAutoAttack}")
                        attack_once = False
                else:
                    print("怪物已死亡，退出战斗循环")
                    break
                
            # 如果超时，打印日志
            if time.time() - start_time >= max_fight_time:
                print(f"战斗时间超过{max_fight_time}秒，强制退出战斗循环")
                return
        else:
            return
    
    def isInScene(self, scene_name:str, confidence:float = 0.8):
        """检查是否到达场景"""
        is_in_scene, _ = self.findPicInRegion(scene_name, kRegionRightPosition, confidence=confidence, is_need_save_debug_image=False)
        return is_in_scene
    
    def autoFind(self, x:str, y:str, is_press_esc:bool = True):
        """场景内自动寻路"""
        # 打开自动寻路
        self.keyPress("`")  # 打开自动寻路~
        time.sleep(max(1, random.gauss(2, 0.05)))
        has_find_pic, pic_region = self.findPicInRegion("auto_find\\1.png", kRegionAutoFind, confidence=0.8, is_need_save_debug_image=True)
        if has_find_pic and pic_region is not None:
            print(f"自动寻路到坐标{x}, {y}")
            x1 = pic_region.left + pic_region.width * (3/8)
            x2 = pic_region.left + pic_region.width * (5/8)
            x3 = pic_region.left + pic_region.width * (7/8)
            y1 = pic_region.top + pic_region.height * (1/2)
            self.mouseMoveAndOnceClicked(x1, y1)
            time.sleep(max(0.1, random.gauss(0.2, 0.05)))
            self.typeNumber(x)
            self.mouseMoveAndOnceClicked(x2, y1)
            time.sleep(max(0.1, random.gauss(0.2, 0.05)))
            self.typeNumber(y)
            self.mouseMoveAndOnceClicked(x3, y1)
            time.sleep(max(0.1, random.gauss(0.2, 0.05)))
            # 关闭自动寻路
            if is_press_esc:
                self.keyPress("ESC")
        else:
            print("未找到自动寻路区域")
    
    def fromDaliToSomeWhere(self, scene_name:str, x:str, y:str):
        """从大理到某个地方"""
        print(f"当前时间{time.strftime('%Y-%m-%d %H:%M:%S')}, 在大理")
        # 打开自动寻路
        self.keyPress("`")  # 打开自动寻路~
        time.sleep(1)
        # 自动寻路中点击崔逢九 && 双击
        _, pic_region = self.findPicInRegion("da_li\\2.png", kRegionAutoFind, confidence=0.8, is_need_save_debug_image=True)
        pic_center_position = self.getRegionCenter(pic_region)
        self.mouseMoveAndDoubleClicked(pic_center_position.x, pic_center_position.y)
        time.sleep(3)
        print("点击崔逢九完成")
        # 点击下拉框
        _, down_pic_ming_jiao = self.findPicInRegion("auto_find\\2.png", kRegionYiZhanLeftDiag, confidence=0.6, is_need_save_debug_image=True)
        down_pic_center_position = self.getRegionCenter(down_pic_ming_jiao)
        self.mouseMoveAndOnceClicked(down_pic_center_position.x, down_pic_center_position.y)
        print("点击下拉框完成")
        time.sleep(1)
        if scene_name == "ming_jiao":
            # 点击其他门派
            _, qi_ta_men_pai = self.findPicInRegion(kYiZhanList["qi_ta_men_pai"], kRegionYiZhanLeftDiag, confidence=0.8, is_need_save_debug_image=True)
            qi_ta_men_pai_pos = self.getRegionCenter(qi_ta_men_pai)
            self.mouseMoveAndOnceClicked(qi_ta_men_pai_pos.x, qi_ta_men_pai_pos.y)
            print("点击其他门派完成")
            # 点击明教
            _, ming_jiao = self.findPicInRegion(kYiZhanList["ming_jiao"], kRegionYiZhanLeftDiag, confidence=0.8, is_need_save_debug_image=True)
            ming_jiao_pos = self.getRegionCenter(ming_jiao)
            self.mouseMoveAndOnceClicked(ming_jiao_pos.x, ming_jiao_pos.y)
            print("点击明教完成")
            time.sleep(2)   # 2s中过场景
            # 点击明教打怪的人, 95, 161
            # self.autoFind(x="95", y="161", is_press_esc=False)
            shi_gang = pyautogui.Point(1148, 513)
            self.mouseMoveAndOnceClicked(shi_gang.x, shi_gang.y)
            print("点击石刚完成")
            time.sleep(3)
            # 点击抵抗围剿
            di_kang_wei_jiu = pyautogui.Point(71, 313)
            self.mouseMoveAndOnceClicked(di_kang_wei_jiu.x, di_kang_wei_jiu.y)
            print("点击抵抗围剿完成")
            time.sleep(2) # 过场景
            # 去到坐标
            self.autoFind(x, y)
            time.sleep(20)
        
def autoFight(scene_name:str, confidence, x:str, y:str):
    game_helper = GameHelper()
    # 执行前等待5秒
    for i in range(2):
        time.sleep(1)
        print(f"剩余{2 - i}秒执行脚本....")
    iter:int = -1    # 监控循环次数
    while True:    
        # 每500次循环，检查是否在地府 && 宝宝吃药
        iter += 1
        # 每500次循环检查是否在地府
        if iter % 500 == 0:
            is_escape_di_fu = game_helper.isInDiFuAndEscape()
            # 检查是否在大理
            is_in_dali = game_helper.isInScene("da_li\\1.png", confidence=0.8)
            if is_in_dali:
                game_helper.fromDaliToSomeWhere("ming_jiao", x, y)
        # 每2000次循环，吃药，回到地点并重置iter
        if iter % 2000 == 0:
            game_helper.autoFind(x, y)
            time.sleep(5)
            iter = 0
            game_helper.babyEat()
        # 检查是否在场景中
        is_in_scene = game_helper.isInScene(scene_name)
        if is_in_scene:
            # 只有小地图有怪物，才进行战斗
            is_monster_in_mini_map = game_helper.isMonsterInMiniMap(confidence=confidence)
            # is_monster_in_mini_map = True
            if is_monster_in_mini_map:
                print(f"当前时间{time.strftime('%Y-%m-%d %H:%M:%S')}, 小地图有怪物")
                game_helper.autoFightOnce()
            else:
                print(f"当前时间{time.strftime('%Y-%m-%d %H:%M:%S')}, 小地图没有怪物")  
        else:
            print(f"当前时间{time.strftime('%Y-%m-%d %H:%M:%S')}, 不在场景中{scene_name}")
            # _, debug_file_path  = game_helper.saveRegionImage(kRegionRightPosition)
            # if debug_file_path is not None:
            #     print(f"保存了当前的场景到：{debug_file_path}")
        # 休息间隔
        print(f"当前循环次数: {iter}次")
        time.sleep(max(0.1, random.gauss(0.2, 0.1)))
        
if __name__ == '__main__':
       
    # autoFight(scene_name=kSceneList["xiao_yao"]["scene_name"], confidence=kSceneList["xiao_yao"]["confidence"])
    autoFight("ming_jiao\\1.png", confidence=0.8, x="115", y="143")  
    # test
    # for i in range(3):
    #     time.sleep(1)
    #     print(f"剩余{3 - i}秒执行脚本....")
    # game_helper = GameHelper()
    # game_helper.autoFind(x="115", y="143")  
    # test get region
    # game_helper = GameHelper()
    # region = game_helper.getScreenRegion()
    # center = game_helper.getRegionCenter(region)
    # print(center)  
  
        

  