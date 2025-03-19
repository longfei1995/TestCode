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

# 指定搜索区域, 如果换了分辨率，还需用test01()重新获取， 见pics/example文件夹下的示例
kRegionAllScreen = (1, 24, 2550, 1366)          # 全屏
kRegionRightPosition = (2288, 13, 262, 61)      # 右上角的场景位置
kRegionMonsterWindow = (248, 25, 308, 216)      # 怪物选中后区域
kRegionBloodBarPosition = (271, 44, 139, 16)    # 血条区域
kRegionMiniMap = (2371, 78, 185, 154)           # 小地图区域
kRegionBBHappyBall = (1385, 1296, 36, 29)       # 珍兽快乐球位置
kRegionBBDrag = (1421, 1296, 37, 28)            # 珍兽吃药位置
# 按键
kKeyAutoAttack = 'e'
kKeyAutoSelect = 'q'

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

    def findPicInRegion(self, pic_name:str, region:tuple, confidence: float = 0.8, is_need_save_debug_image:bool = False):
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
            self.saveRegionImage(region)
            
        # 组合绝对路径
        pic_path = os.path.join(self.current_file_path_, "pics", pic_name)
        
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
                return True, center_position
        except Exception as e:
            pass
        
        # print(f"在指定区域{region}内未找到图片{pic_ath}")
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
        is_in_di_fu, pic_position = self.findPicInRegion("di_fu\\1.png", kRegionRightPosition, confidence=0.9)
        if is_in_di_fu:
            print(f"现在时间是{time.strftime('%Y-%m-%d %H:%M:%S')}，在地府")
            # 开始逃离地府
            is_find_pic, pic_position = self.findPicInRegion("di_fu\\2.png", kRegionAllScreen, confidence=0.7)
            if is_find_pic and pic_position is not None:
                self.mouseMoveAndOnceClicked(pic_position.x, pic_position.y)
                print("逃离地府成功")
                # 等待3s
                time.sleep(max(2, random.gauss(3, 1)))
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
        has_select_target, pic_position = self.findPicInRegion("monster_target.png", kRegionMonsterWindow, confidence=confidence, is_need_save_debug_image=False)
        if has_select_target:
            attack_once = True
            # 添加开始时间和最大战斗时间
            start_time = time.time()
            max_fight_time = 3  # 最多战斗15秒
            
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

    def getOCRText(self, image_path):
        """使用EasyOCR从图像中识别文本"""
        try:
            if not os.path.exists(image_path):
                print(f"错误：图像文件不存在 - {image_path}")
                return ""
            
            # 创建reader对象 - 首次运行会下载模型
            reader = easyocr.Reader(['ch_sim', 'en'])  # 支持简体中文和英文
            
            # 直接从文件路径读取并识别文本
            result = reader.readtext(image_path)
            
            # 提取所有识别到的文本
            text = ' '.join([item[1] for item in result])
            return text
        except Exception as e:
            print(f"OCR处理出错: {str(e)}")
            return ""
    
def autoFight(scene_name:str = "xiao_yao\\1.png", confidence:float = 0.6):
    game_helper = GameHelper()
    # 执行前等待5秒
    for i in range(5):
        time.sleep(1)
        print(f"剩余{5 - i}秒执行脚本....")
    iter:int = -1    # 监控循环次数
    while True:    
        # 每500次循环，检查是否在地府 && 宝宝吃药
        iter += 1
        if iter % 500 == 0:
            iter = 0
            is_escape_di_fu = game_helper.isInDiFuAndEscape()
            game_helper.babyEat()
            # todo 如果逃离地府成功，那么还要寻路到场景中
        # 检查是否在场景中
        is_in_scene, _ = game_helper.findPicInRegion(scene_name, kRegionRightPosition, 0.9, False)
        if is_in_scene:
            # 只有小地图有怪物，才进行战斗
            is_monster_in_mini_map = game_helper.isMonsterInMiniMap(confidence=confidence)
            is_monster_in_mini_map = True
            if is_monster_in_mini_map:
                print(f"当前时间{time.strftime('%Y-%m-%d %H:%M:%S')}, 小地图有怪物")
                game_helper.autoFightOnce()
            else:
                print(f"当前时间{time.strftime('%Y-%m-%d %H:%M:%S')}, 小地图没有怪物")  
        else:
            print(f"当前时间{time.strftime('%Y-%m-%d %H:%M:%S')}, 不在场景中{scene_name}")
            _, debug_file_path  = game_helper.saveRegionImage(kRegionRightPosition)
            if debug_file_path is not None:
                print(f"保存了当前的场景到：{debug_file_path}")
        # 休息间隔
        print(f"当前循环次数: {iter}次")
        time.sleep(max(0.1, random.gauss(0.3, 0.1)))
        
if __name__ == '__main__':
    autoFight(scene_name="fan_zei.png", confidence=0.6)
    # test
    # game_helper = GameHelper()
    # region = game_helper.getScreenRegion()
    # print(region) 
    # # 获取region的截图
    # screenshot, debug_file_path = game_helper.saveRegionImage(region)
    # # 识别截图中的文字
    # text = game_helper.getOCRText(debug_file_path)
    # if text is not None:
    #     if "百度" in text:
    #         print("识别到了百度热搜")
    #         print(text)  
    #     else:
    #         print(f"识别到其他的文字：{text}")  
    # else:  
    #     print("未识别到文字")
      
    

      

