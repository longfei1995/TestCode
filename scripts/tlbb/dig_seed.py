"""
    挖种子      
"""

from img_match import ImageMatch
from keyboard_simulator import KeyboardSimulator
from window_manager import WindowManager
import time
import numpy as np
from game_param import ImagePath, Bbox

class DigSeed:
    def __init__(self, hwnd:int, stop_check_func=None):
        self.window_manager = WindowManager()
        self.keyboard_simulator = KeyboardSimulator()
        self.image_match = ImageMatch(hwnd)
        self.hwnd = hwnd
        self.kKeyDingWeiFu = "F9"
        self.kKeyHorse = "F10"
        self.stop_check_func = stop_check_func  # 停止检查函数
    
    def sleepAuto(self, seconds):
        """可中断的睡眠函数"""
        if seconds <= 0:
            return True
        
        # 将长时间睡眠分解为0.5秒的小段，每段都检查停止标志
        sleep_interval = 0.5
        total_slept = 0
        
        while total_slept < seconds:
            # 检查是否需要停止
            if self.stop_check_func and self.stop_check_func():
                print("收到停止信号，中断睡眠")
                return False
            
            # 计算本次睡眠时间
            remaining = seconds - total_slept
            current_sleep = min(sleep_interval, remaining)
            
            time.sleep(current_sleep)
            total_slept += current_sleep
        
        return True
    
    def getDownHorse(self):
        """下马"""
        self.keyboard_simulator.pressKey(self.kKeyHorse, self.hwnd)
        if not self.sleepAuto(1):
            return False
        print(f"下马, 等待1秒")
        return True
    
    def getUpHorse(self):
        """上马"""
        self.keyboard_simulator.pressKey(self.kKeyHorse, self.hwnd)
        print(f"上马, 等待7秒")
        if not self.sleepAuto(7):
            return False
        return True
    
    def moveSceneConfirm(self):
        """移动场景确认"""
        pic_move_scene_confirm_pos = self.image_match.getImageCenterPos(ImagePath.kun_wu.move_scene_confirm)
        if pic_move_scene_confirm_pos is not None:
            self.keyboard_simulator.mouseClick(pic_move_scene_confirm_pos.x, pic_move_scene_confirm_pos.y, self.hwnd)
            print(f"点击场景确认框完成....")
        else:
            print("未找到场景确认框")
            return False
    
    def selectSeedTask(self, seed_level:int = 1) -> bool:
        """选择种子任务"""
        # 先点击声望任务
        self.keyboard_simulator.mouseClick(105, 405, self.hwnd)
        if not self.sleepAuto(0.5):
            return False
        # 选择对应等级任务
        if seed_level == 1:
            self.keyboard_simulator.mouseClick(117, 216, self.hwnd)
            print(f"点击声望任务1完成....")
        elif seed_level == 2:
            self.keyboard_simulator.mouseClick(117, 244, self.hwnd)
            print(f"点击声望任务2完成....")
        elif seed_level == 3:
            self.keyboard_simulator.mouseClick(117, 269, self.hwnd)
            print(f"点击声望任务3完成....")
        elif seed_level == 4:
            self.keyboard_simulator.mouseClick(117, 297, self.hwnd)
            print(f"点击声望任务4完成....")
        else:
            print(f"这个等级的种子任务, 暂未实现: {seed_level}")
            return False
        if not self.sleepAuto(0.5):
            return False
        
        # 点击接受任务
        self.keyboard_simulator.mouseClick(30, 475, self.hwnd)
        print(f"点击接受任务完成....")
        if not self.sleepAuto(0.5):
            return False
        
        return True
    
    def isPersonStop(self, max_wait_time=180, threshold=5.0):
        """持续监测直到人物停止移动，使用window_manager截图功能
        
        Args:
            max_wait_time (int): 最大等待时间(秒)，默认3分钟
            threshold (float): 像素差异阈值，默认5.0
            
        Returns:
            bool: 是否成功检测到人物静止
        """
        # 定义人物周围区域 (相对于窗口的坐标)
        bbox_x = 660
        bbox_y = 200
        bbox = Bbox(bbox_x, bbox_y, bbox_x + 200, bbox_y + 100)  # 人物周围区域
        start_time = time.time()
        
        print(f"开始持续监测人物是否静止，最长等待{max_wait_time}秒...")
        
        while time.time() - start_time < max_wait_time:
            # 检查是否需要停止
            if self.stop_check_func and self.stop_check_func():
                print("收到停止信号，中断人物静止监测")
                return False
            
            images = []
            
            # 连续截取3张图片，每次间隔2秒
            for i in range(3):
                # 使用window_manager的saveBboxImage截图并保存
                screenshot = self.window_manager.saveBboxImage(self.hwnd, bbox)
                img_array = np.array(screenshot)
                images.append(img_array)
                
                if i < 2:  # 最后一次不需要等待
                    if not self.sleepAuto(2):
                        return False
            
            # 计算图像间的平均绝对差异
            if len(images) >= 2:
                diff1_2 = np.mean(np.abs(images[0].astype(float) - images[1].astype(float)))
                diff2_3 = np.mean(np.abs(images[1].astype(float) - images[2].astype(float)))
                diff1_3 = np.mean(np.abs(images[0].astype(float) - images[2].astype(float)))
                
                avg_diff = (diff1_2 + diff2_3 + diff1_3) / 3
                elapsed_time = time.time() - start_time
                
                # print(f"已等待{elapsed_time:.1f}秒，平均差异: {avg_diff:.2f}，阈值: {threshold}")
                
                # 差异小于阈值视为静止
                if avg_diff < threshold:
                    print(f"检测到人物已静止！总用时: {elapsed_time:.1f}秒")
                    return True
            
            # 等待1秒再开始下一轮检测
            if not self.sleepAuto(1):
                return False
        
        print(f"等待超时({max_wait_time}秒)，人物仍未静止")
        return False
    
    def selectSeedPos(self, seed_level:int = 1) -> bool:
        """选择种子位置"""
        if seed_level == 1:
            self.keyboard_simulator.mouseClick(845, 404, self.hwnd)
            print(f"正在去[57, 204].....")
        elif seed_level == 2:
            self.keyboard_simulator.mouseClick(864, 404, self.hwnd)
            print(f"正在去[152, 238].....")
        elif seed_level == 3:
            self.keyboard_simulator.mouseClick(855, 404, self.hwnd)
            print(f"正在去空桑[73, 71].....")
        else:
            print(f"这个等级的种子, 暂未实现: {seed_level}")
            return False
        return True
    
    def clickSeedAndPet(self, seed_level:int = 1):
        """点击果实3次 -> 上坐骑 -> 选择任务框的第二个坐标"""
        # 点击果实3次
        for i in range(3):
            self.keyboard_simulator.mouseClick(517, 426, self.hwnd)
            if not self.sleepAuto(5):
                return False
        # 上坐骑
        if not self.getUpHorse():
            return False
        if seed_level == 1:
            # 点击任务框的宠物坐标
            self.keyboard_simulator.mouseClick(856, 423, self.hwnd)
        elif seed_level == 2:
            self.keyboard_simulator.mouseClick(874, 423, self.hwnd)
        elif seed_level == 3:
            self.keyboard_simulator.mouseClick(852, 423, self.hwnd)
        else:
            print(f"这个等级的种子, 暂未实现: {seed_level}")
            return False
        return True
    
    def clickMiYingLingQuan(self):
        """点击觅影灵券"""
        # 点击背包栏 -> 点击任务栏 -> 右击任务栏第一格物品
        self.keyboard_simulator.mouseClick(755, 779, self.hwnd)
        if not self.sleepAuto(1):
            return False
        # 点击任务栏
        pic_ren_wu_button_pos = self.image_match.getImageCenterPos(ImagePath.kun_wu.ren_wu_button)
        if pic_ren_wu_button_pos is not None:
            self.keyboard_simulator.mouseClick(pic_ren_wu_button_pos.x, pic_ren_wu_button_pos.y, self.hwnd)
            print(f"点击任务栏完成....")
        else:
            print("未找到任务栏")
            return False
        if not self.sleepAuto(1):
            return False
        
        # 点击任务栏的第一个坐标
        pic_mi_yin_ling_qu_pos = self.image_match.getImageCenterPos(ImagePath.kun_wu.mi_yin_ling_qu)
        if pic_mi_yin_ling_qu_pos is not None:
            self.keyboard_simulator.mouseClick(pic_mi_yin_ling_qu_pos.x, pic_mi_yin_ling_qu_pos.y, self.hwnd, "right")
            print(f"右击觅影灵券完成....")
        else:
            print("未找到觅影灵券")
            return False
        if not self.sleepAuto(1):
            return False
        return True
    
    def digSeed(self, seed_level:int = 1, is_dig_seed:bool = True) -> bool:
        """挖种子"""
        ## 通用流程：上坐骑 -> 双击乘黄长老 -> 点击左侧任务 -> 点击接受任务
        # 上坐骑
        if not self.getUpHorse():
            return False
        # 双击乘黄长老
        self.keyboard_simulator.pressKey('`', self.hwnd)
        pic_cheng_huang_pos = self.image_match.getImageCenterPos(ImagePath.kun_wu.cheng_huang)
        if pic_cheng_huang_pos is not None:
            self.keyboard_simulator.mouseDoubleClick(pic_cheng_huang_pos.x, pic_cheng_huang_pos.y, self.hwnd)
            print(f"双击乘黄长老完成....")
        else:
            print("自动寻路里未找到乘黄长老")
            return False
        if not self.sleepAuto(2):
            return False
        
        # 点击对应等级的种子任务，并且接受任务
        if not self.selectSeedTask(seed_level):
            return False
        if not self.sleepAuto(1):
            return False
        self.keyboard_simulator.pressKey('esc', self.hwnd)
        if not self.sleepAuto(1):
            return False
        
        if is_dig_seed:
            ## 点击果实3次 -> 上坐骑 -> 选择任务框的第二个坐标
            self.selectSeedPos(seed_level)
            if not self.isPersonStop(max_wait_time=60):
                print("等待超时，强制继续后续动作")
            # 下坐骑
            if not self.getDownHorse():
                return False
            
            # 点击果实3次
            if not self.clickSeedAndPet(seed_level):
                return False
            if not self.isPersonStop(max_wait_time=60):
                print("等待超时，强制继续后续动作")
            # 下坐骑
            if not self.getDownHorse():
                return False
            # 点击提交灵药
            pic_ti_jiao_ling_yao_pos = self.image_match.getImageCenterPos(ImagePath.kun_wu.ti_jiao_ling_yao)
            if pic_ti_jiao_ling_yao_pos is not None:
                self.keyboard_simulator.mouseClick(pic_ti_jiao_ling_yao_pos.x, pic_ti_jiao_ling_yao_pos.y, self.hwnd)
                print(f"点击提交灵药完成....")
            else:
                print("未找到提交灵药")
                return False
            if not self.sleepAuto(1):
                return False
            self.keyboard_simulator.pressKey('esc', self.hwnd)
            if not self.sleepAuto(1):
                return False
            # 点击定位符
            self.keyboard_simulator.pressKey(self.kKeyDingWeiFu, self.hwnd)
            if not self.sleepAuto(8):
                return False
        else:
            # 点击觅影灵券
            if not self.clickMiYingLingQuan():
                return False
            if not self.sleepAuto(1):
                return False
            
            # 寻路到怪物位置 -> 点击场景确认框 -> 等待人物到达怪物位置 -> 点击怪物
            # 点击怪物位置
            self.keyboard_simulator.mouseClick(149, 198, self.hwnd)
            print(f"点击怪物位置完成....")
            if not self.sleepAuto(1):
                return False
            
            # 点击场景确认框
            self.moveSceneConfirm()
            if not self.sleepAuto(1):
                return False
            self.keyboard_simulator.pressKey('esc', self.hwnd)
            if not self.sleepAuto(1):
                return False
            
            # 等待人物到达怪物位置
            if not self.isPersonStop(max_wait_time=180):
                print("等待超时，强制继续后续动作")
                
            # 下坐骑
            if not self.getDownHorse():
                return False
            
            # 点击觅影灵券
            if not self.clickMiYingLingQuan():
                return False
            if not self.sleepAuto(1):
                return False
            
            # 开始打怪
            self.keyboard_simulator.pressKey('l', self.hwnd)
            if not self.sleepAuto(10):
                return False
            self.keyboard_simulator.pressKey('l', self.hwnd)
            if not self.sleepAuto(3):
                return False
            # 点击定位符
            self.keyboard_simulator.pressKey(self.kKeyDingWeiFu, self.hwnd)
            if not self.sleepAuto(8):
                return False
        
        ## 通用流程 点击乘黄长老 -> 点击左侧任务 -> 点击完成
        self.keyboard_simulator.pressKey('`', self.hwnd)
        pic_cheng_huang_pos = self.image_match.getImageCenterPos(ImagePath.kun_wu.cheng_huang)
        if pic_cheng_huang_pos is not None:
            self.keyboard_simulator.mouseDoubleClick(pic_cheng_huang_pos.x, pic_cheng_huang_pos.y, self.hwnd)
            print(f"双击乘黄长老完成....")
        else:
            print("未找到乘黄长老")
            return False
        if not self.sleepAuto(2):
            return False
        # 点击任务
        self.keyboard_simulator.mouseClick(105, 405, self.hwnd)
        print(f"点击声望任务完成....")
        if not self.sleepAuto(1):
            return False
        # 点击完成
        self.keyboard_simulator.mouseClick(68, 474, self.hwnd)
        print(f"点击完成按钮....")
        if not self.sleepAuto(1):
            return False
        # 按键ESC
        self.keyboard_simulator.pressKey('esc', self.hwnd)
        if not self.sleepAuto(1):
            return False
        
        return True
        
        


if __name__ == "__main__":
    window_manager = WindowManager()
    hwnd = window_manager.selectWindow()
    if hwnd is None:
        print("未选择窗口")
        exit()
    dig_seed = DigSeed(hwnd)
    dig_seed.digSeed(seed_level=2, is_dig_seed=True)
    # dig_seed.digSeed(seed_level=2, is_dig_seed=False)
    