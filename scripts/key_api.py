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

# 屏幕搜索区域
kScreenWidth = pyautogui.size().width
kScreenHeight = pyautogui.size().height
kRegionScreenFull = (0, 0, kScreenWidth, kScreenHeight)                                         # 全屏
kRegionScreenLeft = (0, 0, kScreenWidth//2, kScreenHeight)                                      # 左侧屏幕
kRegionScreenRight = (kScreenWidth//2, 0, kScreenWidth//2, kScreenHeight)                       # 右侧屏幕
kRegionScreenCenter = (kScreenWidth//4, kScreenHeight//4, kScreenWidth//2, kScreenHeight//2)    # 中间屏幕
kRegionScreenOneQuarter = (kScreenWidth//2, 0, kScreenWidth//2, kScreenHeight//2)                   # 第一象限屏幕
kRegionScreenTwoQuarter = (0, 0, kScreenWidth//2, kScreenHeight//2)                                 # 第二象限屏幕
kRegionScreenThreeQuarter = (0, kScreenHeight//2, kScreenWidth//2, kScreenHeight//2)                # 第三象限屏幕
kRegionScreenFourQuarter = (kScreenWidth//2, kScreenHeight//2, kScreenWidth//2, kScreenHeight//2)   # 第四象限屏幕
kPointScreenCenter = pyautogui.Point(x=kScreenWidth//2, y=kScreenHeight//2)               # 中心位置

# 按键
kKeyAutoSelect = 'q'
kKeyAutoAttack = 'e'
kKeyDingWeiFu = 'f9'
kKeyHorse = 'f10'
kKeyPetFight = 'f8'
kKeyTanXiaoZiRuo = 'f7'
# 背包中，各个项目相对于背包栏图标的像素：
@dataclass
class Bias:
    dao_ju: pyautogui.Point = pyautogui.Point(x=9, y=29)
    cai_liao: pyautogui.Point = pyautogui.Point(x=55, y=29)
    ren_wu: pyautogui.Point = pyautogui.Point(x=98, y=29)
    cell_0_0: pyautogui.Point = pyautogui.Point(x=6, y=60)
# 图片列表
@dataclass
class ImagePath:
    class Other:
        monster_target: str = "other\\monster_target.png"   # 怪物选中后区域
        monster_dot: str = "other\\monster_dot.png"         # 小地图怪物点
        fan_zei: str = "other\\fan_zei.png"                 # 反贼
        guang_tou: str = "other\\guang_tou.png"             # 光头
        auto_find_1 = "other\\auto_find_1.png"              # 自动寻路
        di_fu_1 = "other\\di_fu_1.png"                      # 右上角"地府"图片
        di_fu_2 = "other\\di_fu_2.png"                      # 地府光圈
        enter = "other\\que_ding.png"                       # 确认进入不加杀气场景
        bao_guo: str = "other\\bao_guo.png"                 # 背包栏图标
        ti_jiao_ling_yao: str = "other\\ti_jiao_ling_yao.png" # 提交灵药
        meng_po: str = "other\\meng_po.png"                   # 孟婆
        da_li: str = "other\\da_li.png"                       # 大理
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
    class KunWu:
        one: str = "kun_wu\\1.png"       # 昆吾长老
        
class GameHelper:
    def __init__(self):
        """初始化GameHelper类"""
        self.current_file_path_ = os.path.dirname(os.path.abspath(__file__))
    
    def mouseMoveToCenter(self):
        """移动鼠标到目标位置"""
        move_duration = random.uniform(0.2, 0.5)
        pyautogui.moveTo(kPointScreenCenter.x, kPointScreenCenter.y, duration=move_duration)
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
        kPointAutoFind = pyautogui.Point(x=2483, y=246)
        is_in_di_fu = self.isInScene(ImagePath.Other.di_fu_1, confidence=0.9)
        if is_in_di_fu:
            print(f"在地府，开始逃离")
            # 开始逃离地府
            self.mouseMoveAndOnceClicked(kPointAutoFind.x, kPointAutoFind.y)
            time.sleep(1)
            is_find_meng_po, region = self.findPicInRegion(ImagePath.Other.meng_po, kRegionScreenOneQuarter, confidence=0.8)
            if is_find_meng_po:
                region_pos = self.getRegionCenter(region)
                self.mouseMoveAndDoubleClicked(region_pos.x, region_pos.y)
                time.sleep(10)
                is_find_da_li, region = self.findPicInRegion(ImagePath.Other.da_li, kRegionScreenLeft, confidence=0.8)
                if is_find_da_li:
                    region_pos = self.getRegionCenter(region)
                    self.mouseMoveAndOnceClicked(region_pos.x, region_pos.y)
                    time.sleep(5)
                    print("找到大理, 逃离成功")
                    return True
            else:
                print("未找到孟婆, 逃离失败")      
        else:
            pass
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
    
    def isMonsterInMiniMap(self, confidence):
        """检查小地图是否存在怪物"""
        # 使用findPicInRegion方法来查找预先截取的绿色怪物点图像
        has_monster, _ = self.findPicInRegion(ImagePath.Other.monster_dot, kRegionScreenOneQuarter, confidence=confidence, is_need_save_debug_image=False)
        return has_monster
    
    def autoFightOnce(self, confidence:float = 0.7, max_fight_time:int = 1):
        """简化版自动战斗功能"""
        # 先选取怪物，看是不是选中了
        self.keyPress(kKeyAutoSelect)
        time.sleep(random.uniform(0.05, 0.06))
        has_select_target, _ = self.findPicInRegion(ImagePath.Other.monster_target, kRegionScreenTwoQuarter, confidence=confidence, is_need_save_debug_image=False)
        if has_select_target:
            # 超过最大战斗时间后退出
            start_time = time.time()
            self.keyPress(kKeyAutoAttack)
            print(f"有怪物目标，并且攻击一次{kKeyAutoAttack}")
            while time.time() - start_time > max_fight_time:
                print(f"战斗时间超过{max_fight_time}秒，退出本次战斗")
                return
        else:
            return
    
    def isInScene(self, scene_name:str, confidence:float = 0.8):
        """检查是否在场景"""
        is_in_scene, _ = self.findPicInRegion(scene_name, kRegionScreenOneQuarter, confidence=confidence, is_need_save_debug_image=False)
        return is_in_scene
    
    def autoFind(self, x:str, y:str, is_press_esc:bool = True):
        """场景内自动寻路"""
        # 打开自动寻路
        self.keyPress("`")  # 打开自动寻路~
        time.sleep(random.uniform(1, 1.5))
        has_find_pic, pic_region = self.findPicInRegion(ImagePath.Other.auto_find_1, kRegionScreenRight, confidence=0.8, is_need_save_debug_image=True)
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
        is_find, enter = self.findPicInRegion(ImagePath.Other.enter, kRegionScreenCenter, confidence=0.8)
        if is_find:
            enter_pos = self.getRegionCenter(enter)
            self.mouseMoveAndOnceClicked(enter_pos.x, enter_pos.y)
            print("点击确认进入不加杀气场景完成")
        else:
            print("未找到确认进入不加杀气场景")
        
    def fromDaliToMenPai(self, scene_name:str, x:str, y:str):
        """从大理到某个门派"""
        kPointCuiFengJiu = pyautogui.Point(x=1297, y=698)
        kPointXiaLaKuang = pyautogui.Point(x=246, y=504)
        kPointMenPaiFight = pyautogui.Point(71, 313)
        ## 1. 上坐骑 && 自动寻路中崔逢九 && 点击去其他门派
        self.rideHorse()
        self.autoFind("241", "137")
        time.sleep(5)
        self.mouseMoveAndOnceClicked(kPointCuiFengJiu.x, kPointCuiFengJiu.y)
        time.sleep(1)
        # 1.1 点击下拉框
        self.mouseMoveAndOnceClicked(kPointXiaLaKuang.x, kPointXiaLaKuang.y)
        time.sleep(1)
        # 1.2 点击其他门派
        _, qi_ta_men_pai = self.findPicInRegion(ImagePath.DaLi.four, kRegionScreenLeft, confidence=0.8)
        qi_ta_men_pai_pos = self.getRegionCenter(qi_ta_men_pai)
        self.mouseMoveAndOnceClicked(qi_ta_men_pai_pos.x, qi_ta_men_pai_pos.y)
        time.sleep(1)
        ## 2. 移动到门派打怪人 && 点击门派打怪人
        if scene_name == ImagePath.MingJiao.one:
            kPointShiGang = pyautogui.Point(x=1276, y=677)
            # 点击门派-明教
            _, region = self.findPicInRegion(ImagePath.DaLi.five, kRegionScreenLeft, confidence=0.8)
            region_pos = self.getRegionCenter(region)
            self.mouseMoveAndOnceClicked(region_pos.x, region_pos.y)
            time.sleep(5)
            # 移动到门派打怪人 && 点击门派打怪人
            self.autoFind("95", "161")
            if self.isPersonStop(max_wait_time=10):
                print("人物已到达目标位置")
            else:
                print("等待超时，强制继续后续动作")
            self.mouseMoveAndOnceClicked(kPointShiGang.x, kPointShiGang.y)
            time.sleep(2)
        elif scene_name == ImagePath.EMei.one:
            kPointLiuSanMei = pyautogui.Point(x=1293, y=677)
            # 点击门派-峨眉
            _, region = self.findPicInRegion(ImagePath.DaLi.six, kRegionScreenLeft, confidence=0.8)
            region_pos = self.getRegionCenter(region)
            self.mouseMoveAndOnceClicked(region_pos.x, region_pos.y)
            time.sleep(5)
            # 移动到门派打怪人 && 点击门派打怪人
            self.autoFind("94", "147")
            if self.isPersonStop(max_wait_time=30):
                print("人物已到达目标位置")
            else:
                print("等待超时，强制继续后续动作")
            self.mouseMoveAndOnceClicked(kPointLiuSanMei.x, kPointLiuSanMei.y)
            time.sleep(2)
        ## 3. 点击去打怪场景 && 自动寻路 && 下坐骑
        self.mouseMoveAndOnceClicked(kPointMenPaiFight.x, kPointMenPaiFight.y)
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
        self.keyPress(kKeyHorse)
        time.sleep(5)
        self.mouseMoveToCenter()
    
    def getDownHorse(self):
        """下坐骑"""
        self.keyPress(kKeyHorse)
        time.sleep(1)
        self.mouseMoveToCenter()

    def isPersonStop(self, max_wait_time=180, threshold=5.0):
        """持续监测直到人物停止移动，使用更简单的像素差异比较方法
        
        Args:
            max_wait_time (int): 最大等待时间(秒)，默认3分钟
            
        Returns:
            bool: 是否成功检测到人物静止
        """
        region = (1138, 1133, 239, 100)  # 人物周围区域
        start_time = time.time()
        
        print(f"开始持续监测人物是否静止，最长等待{max_wait_time}秒...")
        
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
                        except Exception as e:
                            print(f"删除检测图片时出错: {e}")
                
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
            print(f"已等待{elapsed_time:.1f}秒，平均差异: {avg_diff:.2f}，阈值: {threshold}")
            
            if avg_diff < threshold:
                print(f"检测到人物已静止！总用时: {elapsed_time:.1f}秒")
                return True
            
            # 等待1秒再开始下一轮检测
            time.sleep(1)
        
        print(f"等待超时({max_wait_time}秒)，人物仍未静止")
        return False

def autoFightMenPai(scene_name:str, confidence:float, x:str, y:str, gui=None):
    game_helper = GameHelper()
    # 执行前等待
    for i in range(5):
        time.sleep(1)
        print(f"剩余{5 - i}秒执行脚本....")
        # 检查停止标志
        if gui and gui.stop_flag:
            print("收到停止信号，取消执行")
            return
    iter:int = -1    # 监控循环次数
    while True:    
        # 检查停止标志
        if gui and gui.stop_flag:
            print("收到停止信号，结束任务")
            return
            
        iter += 1
        # 检查是否在地府
        if iter % 500 == 0:
            is_escape_di_fu = game_helper.isInDiFuAndEscape()
            # 检查是否在大理
            is_in_dali = game_helper.isInScene(ImagePath.DaLi.one, confidence=0.8)
            if is_in_dali:
                print(f"当前在大理")
                iter += 1
                if (scene_name == ImagePath.MingJiao.one):
                    print(f"从大理去明教")
                    game_helper.fromDaliToMenPai(ImagePath.MingJiao.one, x, y)
                elif (scene_name == ImagePath.EMei.one):
                    print(f"从大理去峨眉")
                    game_helper.fromDaliToMenPai(ImagePath.EMei.one, x, y)
        # 每2000次循环: 回到地点并重置iter
        if iter % 2000 == 0:
            iter = 0
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
                print(f"小地图有怪物")
                game_helper.autoFightOnce()
            else:
                print(f"小地图没有怪物")  
        else:
            print(f"不在场景中{scene_name}")
        # 休息间隔
        print(f"当前循环次数: {iter}次")
        time.sleep(0.2)

def autoFightFanZei(gui=None):
    game_helper = GameHelper()
    for i in range(5):
        time.sleep(1)
        print(f"剩余{5 - i}秒执行脚本....")
        # 检查停止标志
        if gui and gui.stop_flag:
            print("收到停止信号，取消执行")
            return
    while True:
        # 检查停止标志
        if gui and gui.stop_flag:
            print("收到停止信号，结束任务")
            return
            
        is_in_fan_zei, _ = game_helper.findPicInRegion(ImagePath.Other.fan_zei, kRegionScreenOneQuarter, confidence=0.8)
        is_in_guang_tou, _ = game_helper.findPicInRegion(ImagePath.Other.guang_tou, kRegionScreenOneQuarter, confidence=0.8)
        if is_in_fan_zei or is_in_guang_tou:
            if is_in_fan_zei:
                print(f"当前在反贼场景中, 正在打怪....")
            elif is_in_guang_tou:
                print(f"当前在光头场景中, 正在打怪....")
            game_helper.keyPress(kKeyAutoSelect)
            time.sleep(random.uniform(0.2, 0.3))
            game_helper.keyPress(kKeyAutoAttack)
            time.sleep(random.uniform(0.5, 0.6))
        else:
            print(f"当前不在反贼或光头场景中")
            time.sleep(1)

def autoDigSeed(iter:int = 1, seed_level:int = 1, gui=None, use_talk:bool = False):
    # 检查停止标志
    if gui and gui.stop_flag:
        print("收到停止信号，取消执行")
        return
    # 如果iter为奇数，则采集果实，否则打怪
    is_dig_red = True  
    if iter % 2 == 1:
        is_dig_red = True
    else:
        is_dig_red = False
    game_helper = GameHelper()
    # 固定坐标
    kPointLeftMission = pyautogui.Point(x=89, y=466)
    kPointAccept = pyautogui.Point(x=27, y=535)
    kPointComplete = pyautogui.Point(x=65, y=535) 
    kPointGuoShi = pyautogui.Point(x=1282, y=703)
    kPointPetLocation = pyautogui.Point(x=2390, y=411)
    kPointMonsterLocation = pyautogui.Point(x=149, y=259)
    kPointPackage = pyautogui.Point(x=1517, y=1377)
    kPointLevel = pyautogui.Point(x=116, y=279)
    auto_find_seed_pos: tuple[str, str] = ("57", "204")
    if seed_level == 1:
        kPointLevel = pyautogui.Point(x=116, y=279)
        auto_find_seed_pos = ("57", "204")
        kPointPetLocation = pyautogui.Point(x=2380, y=411)
    elif seed_level == 2:
        kPointLevel = pyautogui.Point(x=111, y=304)
        auto_find_seed_pos = ("152", "238") 
        kPointPetLocation = pyautogui.Point(x=2400, y=411)
    elif seed_level == 3:
        kPointLevel = pyautogui.Point(x=107, y=330)
        auto_find_seed_pos = ("73", "71")
        kPointPetLocation = pyautogui.Point(x=2390, y=411)
    # elif seed_level == 4:
    #     kPointLevel = pyautogui.Point(x=111, y=304)
    #     auto_find_seed_pos = ("152", "238")
        
    # 1. 通用流程：上坐骑 -> 双击乘黄长老 -> 点击左侧任务 -> 点击接受任务
    # 1.1 上坐骑
    print("上坐骑")
    game_helper.rideHorse()
    # 1.2 双击乘黄长老
    print("双击乘黄长老")
    game_helper.keyPress('`')
    _, region = game_helper.findPicInRegion(ImagePath.KunWu.one, kRegionScreenRight, confidence=0.8)
    region_pos = game_helper.getRegionCenter(region)
    game_helper.mouseMoveAndDoubleClicked(region_pos.x, region_pos.y)
    time.sleep(1)
    # 1.3 点击左侧任务 && 接受任务
    print("点击左侧任务 && 接受任务")
    game_helper.mouseMoveAndOnceClicked(kPointLeftMission.x, kPointLeftMission.y)
    time.sleep(1)
    game_helper.mouseMoveAndOnceClicked(kPointLevel.x, kPointLevel.y)
    time.sleep(1)
    game_helper.mouseMoveAndOnceClicked(kPointAccept.x, kPointAccept.y)
    time.sleep(3)
    game_helper.keyPress('esc')
    time.sleep(1)
    if is_dig_red:
        print("开始采集果实")
        # 寻路到果实为止
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
            game_helper.mouseMoveAndOnceClicked(kPointGuoShi.x, kPointGuoShi.y)
            time.sleep(5)
        # 2.2 上坐骑
        game_helper.rideHorse()
        # 2.3 选择任务框的宠物坐标
        game_helper.mouseMoveAndOnceClicked(kPointPetLocation.x, kPointPetLocation.y)
        print("开始等待人物移动到目标位置...")
        if game_helper.isPersonStop(max_wait_time=60):
            print("人物已到达目标位置")
        else:
            print("等待超时，强制继续后续动作")
        ## 3. 下坐骑 -> 点击提交灵药 -> 点击定位符
        # 3.1 下坐骑
        game_helper.getDownHorse()
        # 3.2 点击提交灵药
        _, region = game_helper.findPicInRegion(ImagePath.Other.ti_jiao_ling_yao, kRegionScreenLeft, confidence=0.8)      
        region_pos = game_helper.getRegionCenter(region)
        game_helper.mouseMoveAndOnceClicked(region_pos.x, region_pos.y)
        time.sleep(1)
        # 3.3 点击定位符
        game_helper.keyPress(kKeyDingWeiFu)
        time.sleep(8)
    else:
        print("开始打怪物")
        # 1. 点击背包栏 -> 点击任务栏 -> 右击任务栏第一格物品
        # 1.1 点击背包栏
        game_helper.mouseMoveAndOnceClicked(kPointPackage.x, kPointPackage.y)
        time.sleep(1)
        _, origin_region = game_helper.findPicInRegion(ImagePath.Other.bao_guo, kRegionScreenRight, confidence=0.8, is_need_save_debug_image=True)
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
        game_helper.mouseMoveAndOnceClicked(kPointMonsterLocation.x, kPointMonsterLocation.y)
        # 2.2 点击场景确认框
        game_helper.moveSceneConfirm()
        # 2.3 等待人物到达怪物位置
        if game_helper.isPersonStop(max_wait_time=120):
            print("人物已到达怪物位置")
        else:
            print("等待超时，强制继续后续动作")
        # 2.4 下坐骑
        game_helper.getDownHorse()
        # 如果启用了谈笑自若，则使用技能
        if use_talk:
            print("使用谈笑自若技能")
            game_helper.keyPress(kKeyTanXiaoZiRuo)
            time.sleep(1)
        # 2.5 召唤怪物 (点击背包栏 ->点击任务栏 -> 右击第一格)
        game_helper.mouseMoveAndOnceClicked(kPointPackage.x, kPointPackage.y)
        time.sleep(1)
        game_helper.mouseMoveAndOnceClicked(ren_wu_lan_pos.x, ren_wu_lan_pos.y)
        time.sleep(1)
        game_helper.mouseMoveAndOnceClicked(cell_0_0_pos.x, cell_0_0_pos.y, button='right')
        time.sleep(1)
        # 2.6 点击怪物
        game_helper.keyPress('l')
        time.sleep(10)
        game_helper.keyPress('l')
        time.sleep(3)
        # 2.7 点击定位符
        game_helper.keyPress(kKeyDingWeiFu)
        time.sleep(8)
    # 点击乘黄长老 -> 点击左侧任务 -> 点击完成
    # 1.2 双击乘黄长老
    game_helper.keyPress('`')
    _, region = game_helper.findPicInRegion(ImagePath.KunWu.one, kRegionScreenRight, confidence=0.8)
    region_pos = game_helper.getRegionCenter(region)
    game_helper.mouseMoveAndDoubleClicked(region_pos.x, region_pos.y)
    time.sleep(1)
    game_helper.mouseMoveAndOnceClicked(kPointLeftMission.x, kPointLeftMission.y)
    time.sleep(1)
    game_helper.mouseMoveAndOnceClicked(kPointComplete.x, kPointComplete.y)
    time.sleep(2)
    game_helper.keyPress('esc')
    time.sleep(1)

def initKey(init_list:list[str]):
    global kKeyAutoSelect
    global kKeyAutoAttack
    global kKeyDingWeiFu
    global kKeyHorse
    global kKeyPetFight
    global kKeyTanXiaoZiRuo
    if len(init_list) == 6:
        kKeyAutoSelect = init_list[0]
        kKeyAutoAttack = init_list[1]
        kKeyDingWeiFu = init_list[2]
        kKeyHorse = init_list[3]    
        kKeyPetFight = init_list[4]
        kKeyTanXiaoZiRuo = init_list[5]
        print(f"按键设置成功: 自动选择目标：{kKeyAutoSelect}, 自动攻击：{kKeyAutoAttack}")
        print(f"按键设置成功: 定位符：{kKeyDingWeiFu}, 骑马：{kKeyHorse}")
        print(f"按键设置成功: 宠物战斗：{kKeyPetFight}, 谈笑自若：{kKeyTanXiaoZiRuo}")
    else:
        print(f"init_list 长度必须为6")

def autoReturnSomewhere(scene_name:str, x:str, y:str, gui=None):
    kPointHuangLongDong = pyautogui.Point(x=1420, y=797)
    kPointMiaoRenDong = pyautogui.Point(x=1383, y=856)
    kPointShuiJingHu = pyautogui.Point(x=1290, y=331)
    kPointXueYuan = pyautogui.Point(x=1283, y=230)
    kPointSongShan = pyautogui.Point(x=1308, y=666)
    game_helper = GameHelper()
    # 剩余5s执行脚本
    for i in range(5):
        time.sleep(1)
        print(f"剩余{5 - i}秒执行脚本....")
    # 检查停止标志
    while True:
        if gui and gui.stop_flag:
            print("收到停止信号，取消执行")
            return
        # 判断是否在地府
        is_escape_di_fu = game_helper.isInDiFuAndEscape()
        # is_escape_di_fu = True
        if is_escape_di_fu:
            print("逃离地府成功")
            time.sleep(1)
            # 1.1 上马
            game_helper.rideHorse()
            # 1.2 点击世界地图
            game_helper.keyPress('m')
            time.sleep(1)
            # 1.3 点击对应场景
            if (scene_name == "黄龙洞"):
                game_helper.mouseMoveAndOnceClicked(kPointHuangLongDong.x, kPointHuangLongDong.y)
            elif (scene_name == "苗人洞"):
                game_helper.mouseMoveAndOnceClicked(kPointMiaoRenDong.x, kPointMiaoRenDong.y)
            elif (scene_name == "水晶湖"):
                game_helper.mouseMoveAndOnceClicked(kPointShuiJingHu.x, kPointShuiJingHu.y)
            elif (scene_name == "雪原"):
                game_helper.mouseMoveAndOnceClicked(kPointXueYuan.x, kPointXueYuan.y)
            elif (scene_name == "嵩山") :
                game_helper.mouseMoveAndOnceClicked(kPointSongShan.x, kPointSongShan.y)
            else:
                print(f"当前场景{scene_name}不支持自动回点")
            # 1.4 点击场景确认框
            time.sleep(1)
            game_helper.mouseMoveAndOnceClicked(kPointScreenCenter.x, kPointScreenCenter.y)
            time.sleep(1)
            game_helper.moveSceneConfirm()
            time.sleep(1)
            game_helper.keyPress('esc')
            # 1.5 从大理去对应场景
            print(f"大理到{scene_name}寻路中，等待人物静止, 最大等待时间500s...")
            game_helper.isPersonStop(max_wait_time=500, threshold=5.0)
            # 1.6 局部寻路到指定坐标
            game_helper.autoFind(x=x, y=y)
            print(f"寻路到指定坐标x={x}, y={y}中，等待人物静止, 最大等待时间120s...")
            game_helper.isPersonStop(max_wait_time=120, threshold=5.0)
            # 特殊场景需要特殊操作一下
            if (scene_name == "黄龙洞"):
                int_x = int(x)  
                int_y = int(y)
                if int_x > 100 and int_y > 190:
                    print("在黄龙洞下方区域，可以不穿越光洞")
                    pass
                else:
                    # 说明在上方区域，需要特殊操作
                    print("在黄龙洞上方区域，需要穿越光洞")
                    game_helper.autoFind("220", "205")
                    time.sleep(1)
                    game_helper.isPersonStop(max_wait_time=30, threshold=5.0)
                    game_helper.autoFind(x, y)
                    print(f"穿越光洞后，寻路到指定坐标x={x}, y={y}中，等待人物静止, 最大等待时间180s...")
                    game_helper.isPersonStop(max_wait_time=180, threshold=5.0)
            # 1.7 下马
            game_helper.getDownHorse()
            time.sleep(1)
            # 1.8 召唤宠物
            if scene_name == "雪原":
                print(f"在雪原，召唤宠物，不怕被人害刀.....其他场景不召唤")
                game_helper.keyPress(kKeyPetFight)
                time.sleep(1)
            # 1.9 开始战斗
            game_helper.keyPress('l')
            time.sleep(1)
        else:
            print(f"不在地府, 60s后重新检查")
        time.sleep(60)
        

if __name__ == '__main__':
    # 门派挂机
    # autoFight(ImagePath.MingJiao.one, confidence=0.8, x="77", y="147") 
    # autoFight(ImagePath.EMei.one, confidence=0.7, x="54", y="144") 
    
    # 刷反刷光头
    # autoFightOther(ImagePath.Other.fan_zei)
    # autoFightOther(ImagePath.EMei.one)
    
    # 获取屏幕区域
    game_helper = GameHelper()    
    region = game_helper.getScreenRegion()
    region_center = game_helper.getRegionCenter(region)
    print(region_center)
    
    # 自动回点    
    # autoReturnSomewhere(scene_name="雪原", x="129", y="189")
    
    # 保存图片
    # game_helper = GameHelper()    
      
    # 采集种子10次
    # for i in range(5):
    #     time.sleep(1)        
    #     print(f"剩余{5 - i}秒执行脚本....")
    # for i in range(2, 10):
    #     print(f"开始第{i}次采集")
    #     autoDigSeed(iter=i, seed_level=2)  
    #     print(f"第{i}次采集完成")
        
                  
  
          