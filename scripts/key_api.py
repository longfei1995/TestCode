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
# 图片处理
import numpy as np
import cv2
# 数据类
from dataclasses import dataclass

# 指定搜索区域, 如果换了分辨率，还需重新获取， 见pics/example文件夹下的示例
kRegionAllScreen = (1, 24, 2550, 1366)          # 全屏
kRegionRightPosition = (2380, 26, 156, 50)      # 右上角的场景位置
kRegionMonsterWindow = (248, 25, 308, 216)      # 怪物选中后区域
kRegionBloodBarPosition = (271, 44, 139, 16)    # 血条区域
kRegionMiniMap = (2371, 78, 185, 154)           # 小地图区域
kRegionBBHappyBall = (1385, 1296, 36, 29)       # 珍兽快乐球位置
kRegionBBDrag = (1421, 1296, 37, 28)            # 珍兽吃药位置
kRegionAutoFind = (2357, 229, 196, 322)         # 自动寻路区域  
kRegionYiZhanLeftDiag = (1, 178, 282, 393)      # 驿站左侧框位置
kRegionEnter = (984, 460, 554, 404)             # 是否进入不加杀气场景  
kRegionPackage = (1887, 645, 649, 702)          # 背包栏位置
kRegionChengHuang = (0, 133, 409, 574)          # 乘黄对话框
kScreenCenterPoint = pyautogui.Point(x=pyautogui.size().width//2, y=pyautogui.size().height//2)               # 中心位置
# 背包中，各个项目相对于背包栏图标的像素：
@dataclass
class Bias:
    dao_ju: pyautogui.Point = pyautogui.Point(x=14, y=37)
    cai_liao: pyautogui.Point = pyautogui.Point(x=61, y=37)
    ren_wu: pyautogui.Point = pyautogui.Point(x=100, y=37)
    cell_0_0: pyautogui.Point = pyautogui.Point(x=7, y=62)
    cell_0_1: pyautogui.Point = pyautogui.Point(x=47, y=62)
    cell_0_2: pyautogui.Point = pyautogui.Point(x=87, y=62)
    cell_0_3: pyautogui.Point = pyautogui.Point(x=127, y=62)
    cell_0_4: pyautogui.Point = pyautogui.Point(x=167, y=62)
    cell_0_5: pyautogui.Point = pyautogui.Point(x=207, y=62)
    cell_0_6: pyautogui.Point = pyautogui.Point(x=247, y=62)
    cell_0_7: pyautogui.Point = pyautogui.Point(x=287, y=62)
    cell_0_8: pyautogui.Point = pyautogui.Point(x=327, y=62)
    cell_0_9: pyautogui.Point = pyautogui.Point(x=367, y=62)
    cell_0_10: pyautogui.Point = pyautogui.Point(x=407, y=62)
    cell_1_0: pyautogui.Point = pyautogui.Point(x=7, y=102)
    cell_1_1: pyautogui.Point = pyautogui.Point(x=47, y=102)
    cell_1_2: pyautogui.Point = pyautogui.Point(x=87, y=102)
    cell_1_3: pyautogui.Point = pyautogui.Point(x=127, y=102)    
    cell_1_4: pyautogui.Point = pyautogui.Point(x=167, y=102)
    cell_1_5: pyautogui.Point = pyautogui.Point(x=207, y=102)
    

# 按键
kKeyAutoAttack = 'e'
kKeyAutoSelect = 'q'
# 图片列表
@dataclass
class ImagePath:
    class Other:
        monster_target: str = "other\\monster_target.png"   # 怪物选中后区域
        monster_dot: str = "other\\monster_dot.png"         # 小地图怪物点
        fan_zei: str = "other\\fan_zei.png"                 # 反贼
        guang_tou: str = "other\\guang_tou.png"             # 光头
        auto_find_1 = "other\\auto_find_1.png"              # 自动寻路
        auto_find_2 = "other\\auto_find_2.png"              # 下拉框按钮
        di_fu_1 = "other\\di_fu_1.png"                      # 右上角"地府"图片
        di_fu_2 = "other\\di_fu_2.png"                      # 地府光圈
        enter = "other\\que_ding.png"                       # 确认进入不加杀气场景
        bao_guo: str = "other\\bao_guo.png"                 # 背包栏图标
        ti_jiao_ling_yao: str = "other\\ti_jiao_ling_yao.png" # 提交灵药
    class DaLi:
        one: str = "da_li\\1.png"       # 右上角"大理"图片
        two: str = "da_li\\2.png"       # 崔逢九传送
        three: str = "da_li\\3.png"     # todo, 暂无  
        four: str = "da_li\\4.png"      # 带我去其他门派
        five: str = "da_li\\5.png"      # 门派-明教
        six: str = "da_li\\6.png"       # 门派-峨眉
    class MingJiao:
        one: str = "ming_jiao\\1.png"   # 右上角"明教"图片
        two: str = "ming_jiao\\2.png"   # 石刚-打怪
        three: str = "ming_jiao\\3.png" # 去抵抗围剿
    class EMei:
        one: str = "e_mei\\1.png"       # 右上角"峨眉"图片
    class WuDang:
        one: str = "wu_dang\\1.png"     # 右上角"武当"图片
    class XiaoYao:
        one: str = "xiao_yao\\1.png"     # 右上角"逍遥"图片
        
class GameHelper:
    def __init__(self):
        """初始化GameHelper类"""
        self.current_file_path_ = os.path.dirname(os.path.abspath(__file__))
    
    def mouseMoveToCenter(self):
        """移动鼠标到目标位置"""
        move_duration = random.uniform(0.2, 0.5)
        pyautogui.moveTo(kScreenCenterPoint.x, kScreenCenterPoint.y, duration=move_duration)
        time.sleep(random.uniform(0.01, 0.05))
    
    def mouseMoveAndOnceClicked(self, screen_x, screen_y, button:str = 'left'):
        """模拟人类真实点击操作，在按下和抬起之间添加随机延迟
    
    Args:
        screen_x (int): 屏幕x坐标
        screen_y (int): 屏幕y坐标
    """
        # 移动鼠标到目标位置，使用高斯分布的随机时间
        move_duration = random.uniform(0.2, 0.5)
        pyautogui.moveTo(screen_x, screen_y, duration=move_duration)
        
        # 短暂停顿，模拟人类反应，使用高斯分布
        time.sleep(random.uniform(0.01, 0.05))
        
        # 按下鼠标左键
        pyautogui.mouseDown(button=button)
        
        # 随机按住时间，使用高斯分布
        time.sleep(random.uniform(0.05, 0.08))
        
        # 释放鼠标左键
        pyautogui.mouseUp(button=button)
        
        # 操作完成后的随机短暂停顿，使用高斯分布
        time.sleep(random.uniform(0.05, 0.15))

    def mouseMoveAndDoubleClicked(self, screen_x, screen_y):
        # 移动鼠标到目标位置
        move_duration = random.uniform(0.2, 0.5)
        pyautogui.moveTo(screen_x, screen_y, duration=move_duration)
        
        # 第一次点击
        pyautogui.mouseDown(button='left')
        time.sleep(0.02)  # 极短按下时间
        pyautogui.mouseUp(button='left')
        
        # 控制两次点击间间隔时间（非常短）
        time.sleep(random.uniform(0.05, 0.06))  # 50ms左右的间隔
        
        # 第二次点击
        pyautogui.mouseDown(button='left')
        time.sleep(0.02)  # 极短按下时间
        pyautogui.mouseUp(button='left')
        
        # 操作后随机延迟
        time.sleep(random.uniform(0.05, 0.15))

    def keyPress(self, key):
        pyautogui.press(key)
        time.sleep(random.uniform(0.05, 0.06))

    def typeNumber(self, number:str):
        """输入数字"""
        # 按数字前按三下删除
        for _ in range(3):
            pyautogui.press('backspace')
            time.sleep(random.uniform(0.05, 0.06))
        # 输入数字
        for char in number:
            pyautogui.typewrite(char)
            time.sleep(random.uniform(0.05, 0.06))

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
        is_in_di_fu = self.isInScene(ImagePath.Other.di_fu_1, confidence=0.9)
        if is_in_di_fu:
            print(f"现在时间是{time.strftime('%Y-%m-%d %H:%M:%S')}，在地府")
            # 开始逃离地府
            is_find_pic, pic_region = self.findPicInRegion(ImagePath.Other.di_fu_2, kRegionAllScreen, confidence=0.7)
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
        has_monster, _ = self.findPicInRegion(ImagePath.Other.monster_dot, kRegionMiniMap, confidence=confidence, is_need_save_debug_image=False)
        return has_monster
    
    def babyEat(self):
        """宝宝吃药，吃快乐球"""
        # 点击宝宝药
        self.mouseMoveAndOnceClicked(self.getRegionCenter(kRegionBBDrag).x, self.getRegionCenter(kRegionBBDrag).y)
        # self.save_region_debug_image(kRegionBBDrag)
        print("点击宝宝吃药")
        time.sleep(random.uniform(0.1, 0.2))
        # 点击快乐球
        self.mouseMoveAndOnceClicked(self.getRegionCenter(kRegionBBHappyBall).x, self.getRegionCenter(kRegionBBHappyBall).y)
        # self.save_region_debug_image(kRegionBBHappyBall)
        print("点击宝宝吃快乐球")
        time.sleep(random.uniform(0.1, 0.2))
    def autoFightOnce(self, confidence:float = 0.7):
        """简化版自动战斗功能 - 基于固定位置的血条检测
        """
        # 先选取怪物，看是不是选中了
        self.keyPress(kKeyAutoSelect)
        print(f"选择怪物{kKeyAutoSelect}")
        time.sleep(random.uniform(0.05, 0.06))
        has_select_target, _ = self.findPicInRegion(ImagePath.Other.monster_target, kRegionMonsterWindow, confidence=confidence, is_need_save_debug_image=False)
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
        time.sleep(random.uniform(1, 1.5))
        has_find_pic, pic_region = self.findPicInRegion(ImagePath.Other.auto_find_1, kRegionAutoFind, confidence=0.8, is_need_save_debug_image=True)
        if has_find_pic and pic_region is not None:
            print(f"自动寻路到坐标{x}, {y}")
            x1 = pic_region.left + pic_region.width * (3/8)
            x2 = pic_region.left + pic_region.width * (5/8)
            x3 = pic_region.left + pic_region.width * (7/8)
            y1 = pic_region.top + pic_region.height * (1/2)
            self.mouseMoveAndOnceClicked(x1, y1)
            time.sleep(random.uniform(0.1, 0.2))
            self.typeNumber(x)
            self.mouseMoveAndOnceClicked(x2, y1)
            time.sleep(random.uniform(0.1, 0.2))
            self.typeNumber(y)
            self.mouseMoveAndOnceClicked(x3, y1)
            time.sleep(random.uniform(0.1, 0.2))
            # 关闭自动寻路
            if is_press_esc:
                self.keyPress("ESC")
        else:
            print("未找到自动寻路区域")
        time.sleep(2)
        self.mouseMoveToCenter()
            
    def moveSceneConfirm(self):
        """移动场景确认"""
        is_find, enter = self.findPicInRegion(ImagePath.Other.enter, kRegionEnter, confidence=0.8, is_need_save_debug_image=True)
        if is_find:
            enter_pos = self.getRegionCenter(enter)
            self.mouseMoveAndOnceClicked(enter_pos.x, enter_pos.y)
            print("点击确认进入不加杀气场景完成")
        else:
            print("未找到确认进入不加杀气场景")
        
        
    def fromDaliToMenPai(self, scene_name:str, x:str, y:str):
        """从大理到某个门派"""
        cui_feng_jiu_pos = pyautogui.Point(x=1297, y=698)
        xia_la_kuang_pos = pyautogui.Point(x=246, y=504)
        fight_pos = pyautogui.Point(71, 313)
        ## 1. 上坐骑 && 自动寻路中崔逢九 && 点击去其他门派
        self.rideHorse()
        self.autoFind("241", "137")
        time.sleep(5)
        self.mouseMoveAndOnceClicked(cui_feng_jiu_pos.x, cui_feng_jiu_pos.y)
        time.sleep(1)
        # 1.1 点击下拉框
        self.mouseMoveAndOnceClicked(xia_la_kuang_pos.x, xia_la_kuang_pos.y)
        time.sleep(1)
        # 1.2 点击其他门派
        _, qi_ta_men_pai = self.findPicInRegion(ImagePath.DaLi.four, kRegionYiZhanLeftDiag, confidence=0.8, is_need_save_debug_image=True)
        qi_ta_men_pai_pos = self.getRegionCenter(qi_ta_men_pai)
        self.mouseMoveAndOnceClicked(qi_ta_men_pai_pos.x, qi_ta_men_pai_pos.y)
        time.sleep(1)
        ## 2. 移动到门派打怪人 && 点击门派打怪人
        if scene_name == ImagePath.MingJiao.one:
            shi_gang_pos = pyautogui.Point(x=1276, y=677)
            # 点击门派-明教
            _, region = self.findPicInRegion(ImagePath.DaLi.five, kRegionYiZhanLeftDiag, confidence=0.8, is_need_save_debug_image=True)
            region_pos = self.getRegionCenter(region)
            self.mouseMoveAndOnceClicked(region_pos.x, region_pos.y)
            time.sleep(5)
            # 移动到门派打怪人 && 点击门派打怪人
            self.autoFind("95", "161")
            if self.isPersonStop(max_wait_time=10):
                print("人物已到达目标位置")
            else:
                print("等待超时，强制继续后续动作")
            self.mouseMoveAndOnceClicked(shi_gang_pos.x, shi_gang_pos.y)
            time.sleep(2)
        elif scene_name == ImagePath.EMei.one:
            liu_san_mei_pos = pyautogui.Point(x=1293, y=677)
            # 点击门派-峨眉
            _, region = self.findPicInRegion(ImagePath.DaLi.six, kRegionYiZhanLeftDiag, confidence=0.8)
            region_pos = self.getRegionCenter(region)
            self.mouseMoveAndOnceClicked(region_pos.x, region_pos.y)
            time.sleep(5)
            # 移动到门派打怪人 && 点击门派打怪人
            self.autoFind("94", "147")
            if self.isPersonStop(max_wait_time=30):
                print("人物已到达目标位置")
            else:
                print("等待超时，强制继续后续动作")
            self.mouseMoveAndOnceClicked(liu_san_mei_pos.x, liu_san_mei_pos.y)
            time.sleep(2)
        ## 3. 点击去打怪场景 && 自动寻路 && 下坐骑
        self.mouseMoveAndOnceClicked(fight_pos.x, fight_pos.y)
        time.sleep(5)
        # 点击确认进入不加杀气场景
        self.moveSceneConfirm()
        time.sleep(2)
        self.autoFind(x, y)
        if self.isPersonStop(max_wait_time=60):
            print("人物已到达目标位置")
        else:
            print("等待超时，强制继续后续动作")
        self.getDownHorse()
    def rideHorse(self):
        """上坐骑"""
        # 点击坐骑
        screen_pos = pyautogui.Point(x=2534, y=478)
        self.mouseMoveAndOnceClicked(screen_pos.x, screen_pos.y)
        time.sleep(5)
        self.mouseMoveToCenter()
    
    def getDownHorse(self):
        """下坐骑"""
        # 点击坐骑
        screen_pos = pyautogui.Point(x=2534, y=478)
        self.mouseMoveAndOnceClicked(screen_pos.x, screen_pos.y)
        time.sleep(1)
        self.mouseMoveToCenter()

    def isPersonStop(self, max_wait_time=180, threshold=5.0):
        """持续监测直到人物停止移动，使用更简单的像素差异比较方法
        
        Args:
            max_wait_time (int): 最大等待时间(秒)，默认3分钟
            
        Returns:
            bool: 是否成功检测到人物静止
        """
        region = (1218, 445, 109, 88)  # 人物周围区域
        start_time = time.time()
        
        print(f"开始持续监测人物状态，最长等待{max_wait_time}秒...")
        
        while time.time() - start_time < max_wait_time:
            images = []
            
            # 连续截取3张图片，每次间隔2秒
            for i in range(3):
                current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
                screenshot = pyautogui.screenshot(region=region)
                img_array = np.array(screenshot)
                images.append(img_array)
                
                # 保存最新一组截图用于调试
                debug_dir = os.path.join(self.current_file_path_, "pics\\debug")
                if not os.path.exists(debug_dir):
                    os.makedirs(debug_dir)
                
                # 限制movement_开头的图片数量为最多3张
                movement_files = glob.glob(os.path.join(debug_dir, "movement_*.png"))
                if len(movement_files) >= 3:
                    # 按文件创建时间排序
                    movement_files.sort(key=os.path.getctime)
                    # 删除最早的文件，直到只剩2张(为了给即将保存的新图片腾出空间)
                    for old_file in movement_files[:-2]:
                        try:
                            os.remove(old_file)
                            print(f"删除旧的监测图片: {os.path.basename(old_file)}")
                        except Exception as e:
                            print(f"删除文件时出错: {e}")
                
                debug_path = os.path.join(debug_dir, f"movement_{current_time}_{i}.png")
                screenshot.save(debug_path)
                
                if i < 2:  # 最后一次不需要等待
                    time.sleep(2)  # 间隔缩短到2秒使检测更快响应
            
            # 计算图像间的平均绝对差异
            diff1_2 = np.mean(np.abs(images[0].astype(float) - images[1].astype(float)))
            diff2_3 = np.mean(np.abs(images[1].astype(float) - images[2].astype(float)))
            diff1_3 = np.mean(np.abs(images[0].astype(float) - images[2].astype(float)))
            
            avg_diff = (diff1_2 + diff2_3 + diff1_3) / 3
            elapsed_time = time.time() - start_time
            
            # 差异小于阈值视为静止
            print(f"已等待{elapsed_time:.1f}秒，图片平均差异: {avg_diff:.2f}，阈值: {threshold}")
            
            if avg_diff < threshold:
                print(f"检测到人物已静止！总用时: {elapsed_time:.1f}秒")
                return True
            
            # 等待1秒再开始下一轮检测
            time.sleep(1)
        
        print(f"等待超时({max_wait_time}秒)，人物仍未静止")
        return False

def autoFight(scene_name:str, confidence, x:str, y:str):
    game_helper = GameHelper()
    # 执行前等待
    for i in range(2):
        time.sleep(1)
        print(f"剩余{2 - i}秒执行脚本....")
    iter:int = -1    # 监控循环次数
    while True:    
        iter += 1
        # 检查是否在地府
        if iter % 500 == 0:
            is_escape_di_fu = game_helper.isInDiFuAndEscape()
            # 检查是否在大理
            is_in_dali = game_helper.isInScene(ImagePath.DaLi.one, confidence=0.8)
            if is_in_dali:
                iter += 1
                if (scene_name == ImagePath.MingJiao.one):
                    game_helper.fromDaliToMenPai(ImagePath.MingJiao.one, x, y)
                elif (scene_name == ImagePath.EMei.one):
                    game_helper.fromDaliToMenPai(ImagePath.EMei.one, x, y)
        # 每2000次循环: 吃药，回到地点并重置iter
        if iter % 2000 == 0:
            iter = 0
            # game_helper.babyEat()
            game_helper.autoFind(x, y)
            if game_helper.isPersonStop(max_wait_time=60):
                print("人物已到达目标位置") 
            else:
                print("等待超时，强制继续后续动作")
        # 检查是否在场景中
        is_in_scene = game_helper.isInScene(scene_name)
        if is_in_scene:
            # 只有小地图有怪物，才进行战斗
            is_monster_in_mini_map = game_helper.isMonsterInMiniMap(confidence=confidence)
            if is_monster_in_mini_map:
                print(f"当前时间{time.strftime('%Y-%m-%d %H:%M:%S')}, 小地图有怪物")
                game_helper.autoFightOnce()
            else:
                print(f"当前时间{time.strftime('%Y-%m-%d %H:%M:%S')}, 小地图没有怪物")  
        else:
            print(f"当前时间{time.strftime('%Y-%m-%d %H:%M:%S')}, 不在场景中{scene_name}")
        # 休息间隔
        print(f"当前循环次数: {iter}次")
        time.sleep(0.2)

def autoDigSeed(iter:int = 1, seed_level:int = 1):
    # 如果iter为奇数，则采集红果，否则采集种子
    is_dig_red = True
    if iter % 2 == 1:
        # 奇数次采集红果
        is_dig_red = True
    else:
        # 偶数次打怪
        is_dig_red = False
    game_helper = GameHelper()
    # 乘黄长老坐标
    cheng_huang_pos = pyautogui.Point(x=1160, y=707)
    kun_wu_sheng_wang_ren_wu_pos = pyautogui.Point(x=129, y=463)
    kun_wu_sheng_wang_ren_wu_pos2 = None
    auto_find_seed_pos: tuple[str, str] = ("57", "204")
    if seed_level == 1:
        kun_wu_sheng_wang_ren_wu_pos2 = pyautogui.Point(x=116, y=279)
        auto_find_seed_pos = ("57", "204")
    elif seed_level == 2:
        kun_wu_sheng_wang_ren_wu_pos2 = pyautogui.Point(x=111, y=304)
        auto_find_seed_pos = ("152", "238")
    accept_button_pos = pyautogui.Point(x=27, y=535)
    complete_button_pos = pyautogui.Point(x=65, y=535) 
    # 果实坐标
    guo_shi_pos = pyautogui.Point(x=1282, y=703)
    pet_pos = pyautogui.Point(x=2400, y=411)
    ding_wei_fu_pos = pyautogui.Point(x=1260, y=1358) # 放在D旁边
    # 打怪相关坐标
    package_pic_pos = pyautogui.Point(x=1517, y=1377)
    monster_pos = pyautogui.Point(x=149, y=259)
    # 通用流程：上坐骑 -> 点击乘黄长老 -> 点击左侧任务 -> 点击接受任务
    game_helper.rideHorse()  
    game_helper.mouseMoveAndOnceClicked(cheng_huang_pos.x, cheng_huang_pos.y)
    time.sleep(1)
    game_helper.mouseMoveAndOnceClicked(kun_wu_sheng_wang_ren_wu_pos.x, kun_wu_sheng_wang_ren_wu_pos.y)
    time.sleep(1)
    game_helper.mouseMoveAndOnceClicked(kun_wu_sheng_wang_ren_wu_pos2.x, kun_wu_sheng_wang_ren_wu_pos2.y)
    time.sleep(1)
    game_helper.mouseMoveAndOnceClicked(accept_button_pos.x, accept_button_pos.y)
    time.sleep(3)
    if is_dig_red:
        print("开始采集红果")
        ## 1. 寻路到果实位置(57, 204) -> 下坐骑  
        game_helper.autoFind(x=auto_find_seed_pos[0], y=auto_find_seed_pos[1])
        # 判断人物静止
        if game_helper.isPersonStop(max_wait_time=60):
            print("人物已到达目标位置")
        else:
            print("等待超时，强制继续后续动作")
        game_helper.getDownHorse()
        ## 2. 点击红果3次 -> 上坐骑 -> 选择任务框的第二个坐标
        # 2.1 点击红果3次
        for i in range(3):
            game_helper.mouseMoveAndOnceClicked(guo_shi_pos.x, guo_shi_pos.y)
            time.sleep(5)
        # 2.2 上坐骑
        game_helper.rideHorse()
        # 2.3 选择任务框的第二个坐标
        game_helper.mouseMoveAndOnceClicked(pet_pos.x, pet_pos.y)
        print("开始等待人物移动到目标位置...")
        if game_helper.isPersonStop(max_wait_time=60):
            print("人物已到达目标位置")
        else:
            print("等待超时，强制继续后续动作")
        ## 3. 下坐骑 -> 点击提交灵药 -> 点击定位符
        # 3.1 下坐骑
        game_helper.getDownHorse()
        # 3.2 点击提交灵药
        _, ti_jiao_ling_yao_region = game_helper.findPicInRegion(ImagePath.Other.ti_jiao_ling_yao, kRegionChengHuang, confidence=0.8, is_need_save_debug_image=True)
        ti_jiao_ling_yao_pos = game_helper.getRegionCenter(ti_jiao_ling_yao_region)
        game_helper.mouseMoveAndOnceClicked(ti_jiao_ling_yao_pos.x, ti_jiao_ling_yao_pos.y)
        time.sleep(1)
        # 3.3 点击定位符
        game_helper.mouseMoveAndOnceClicked(ding_wei_fu_pos.x, ding_wei_fu_pos.y)
        time.sleep(8)
    else:
        print("开始打怪物")
        # 1. 点击背包栏 -> 点击任务栏 -> 右击任务栏第一格物品
        # 1.1 点击背包栏
        game_helper.mouseMoveAndOnceClicked(package_pic_pos.x, package_pic_pos.y)
        time.sleep(1)
        _, origin_region = game_helper.findPicInRegion(ImagePath.Other.bao_guo, kRegionPackage, confidence=0.8, is_need_save_debug_image=True)
        origin_region_center = game_helper.getRegionCenter(origin_region)
        ren_wu_lan_pos = pyautogui.Point(x=origin_region_center.x + Bias.ren_wu.x, y=origin_region_center.y + Bias.ren_wu.y)
        cell_0_0_pos = pyautogui.Point(x=origin_region_center.x + Bias.cell_0_0.x, y=origin_region_center.y + Bias.cell_0_0.y)
        # 1.2 点击任务栏
        game_helper.mouseMoveAndOnceClicked(ren_wu_lan_pos.x, ren_wu_lan_pos.y)
        time.sleep(1)
        # 1.3 右击任务栏第一格物品
        game_helper.mouseMoveAndOnceClicked(cell_0_0_pos.x, cell_0_0_pos.y, button='right')
        time.sleep(1)
        ## 2. 寻路到怪物位置 -> 点击场景确认框 -> 等待人物到达怪物位置 -> 点击怪物
        # 2.1 点击怪物位置
        game_helper.mouseMoveAndOnceClicked(monster_pos.x, monster_pos.y)
        # 2.2 点击场景确认框
        game_helper.moveSceneConfirm()
        # 2.3 等待人物到达怪物位置
        if game_helper.isPersonStop(max_wait_time=120):
            print("人物已到达怪物位置")
        else:
            print("等待超时，强制继续后续动作")
        # 2.4 下坐骑
        game_helper.getDownHorse()
        # 2.5 召唤怪物 (点击背包栏 ->点击任务栏 -> 右击第一格)
        game_helper.mouseMoveAndOnceClicked(package_pic_pos.x, package_pic_pos.y)
        time.sleep(1)
        game_helper.mouseMoveAndOnceClicked(ren_wu_lan_pos.x, ren_wu_lan_pos.y)
        time.sleep(1)
        game_helper.mouseMoveAndOnceClicked(cell_0_0_pos.x, cell_0_0_pos.y, button='right')
        time.sleep(1)
        # 2.6 点击怪物
        # monster_pos_2 = pyautogui.Point(x=1276, y=761)
        # for i in range(3):
        #     game_helper.mouseMoveAndOnceClicked(monster_pos_2.x, monster_pos_2.y)
        #     time.sleep(5)
        game_helper.keyPress('l')
        time.sleep(10)
        game_helper.keyPress('l')
        time.sleep(3)
        # 2.7 点击定位符
        game_helper.mouseMoveAndOnceClicked(ding_wei_fu_pos.x, ding_wei_fu_pos.y)
        time.sleep(8)
    # 点击乘黄长老 -> 点击左侧任务 -> 点击完成
    game_helper.mouseMoveAndOnceClicked(cheng_huang_pos.x, cheng_huang_pos.y)
    time.sleep(1)
    game_helper.mouseMoveAndOnceClicked(kun_wu_sheng_wang_ren_wu_pos.x, kun_wu_sheng_wang_ren_wu_pos.y)
    time.sleep(1)
    game_helper.mouseMoveAndOnceClicked(complete_button_pos.x, complete_button_pos.y)
    time.sleep(2)

if __name__ == '__main__':
    # autoFight(ImagePath.MingJiao.one, confidence=0.8, x="97", y="76") 
    autoFight(ImagePath.EMei.one, confidence=0.7, x="54", y="144") 
    # test
    # game_helper = GameHelper()    
    # region = game_helper.getScreenRegion()
    # region_center = game_helper.getRegionCenter(region)
    # print(region_center)    
    # 采集种子20次
    # for i in range(5):
    #     time.sleep(1)    
    #     print(f"剩余{5 - i}秒执行脚本....")
    # for i in range(10, 11):
    #     print(f"开始第{i}次采集")
    #     autoDigSeed(iter=i, seed_level=2)  
    #     print(f"第{i}次采集完成")
        
                  
  
          