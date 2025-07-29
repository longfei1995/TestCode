import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QGroupBox, QTextEdit, QSpinBox, QComboBox, QDoubleSpinBox,
                            QMessageBox, QCheckBox, QTabWidget, QFormLayout, QGridLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor, QCursor
from io import StringIO
import os
import time
from game_param import kHPBar, kMPBar, kDefaultKey, kProfilePhoto, kBaseDir
from window_manager import WindowManager
from color_detector import ColorDetector
from keyboard_simulator import KeyboardSimulator
from dig_seed import DigSeed
from auto_return import AutoReturn  # 导入AutoReturn类


class UILogStream:
    """自定义输出流，将print输出重定向到UI日志"""
    def __init__(self, log_callback):
        self.log_callback = log_callback
        self.buffer = StringIO()
    
    def write(self, text):
        if text.strip():  # 只有非空内容才记录
            self.log_callback(text.strip())
    
    def flush(self):
        pass


class RaidThread(QThread):
    """后台运行自动团本的线程"""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, hwnd: int, log_callback, key_interval: float, sleep_time: float, is_em: bool, key_sequence: str):
        super().__init__()
        self.hwnd = hwnd
        self.running = True
        self.log_callback = log_callback
        self.original_stdout = None
        
        # 从UI获取的参数
        self.key_interval = key_interval
        self.sleep_time = sleep_time
        self.is_em = is_em
        self.key_sequence = key_sequence
    
    def run(self):
        try:
            # 在线程中重定向stdout到UI日志
            self.original_stdout = sys.stdout
            sys.stdout = UILogStream(self.log_signal.emit)
            
            # 开始自动按键的主要逻辑
            self.autoKeyPress(self.hwnd)
        except Exception as e:
            self.log_signal.emit(f"错误：{str(e)}")
        finally:
            # 恢复原始stdout
            if self.original_stdout:
                sys.stdout = self.original_stdout
            self.finished_signal.emit()
            
    def autoKeyPress(self, hwnd: int):
        """自动按键的主要逻辑"""
        color_detector = ColorDetector()
        keyboard_simulator = KeyboardSimulator()
        
        # 解析按键序列
        keys = self.key_sequence.split()
        if not keys:
            print("按键序列为空，无法执行")
            return
        
        # 主循环
        cycle_count = 0
        while self.running:
            cycle_count += 1
            if cycle_count > 1e5:
                print("按键循环超过10w次，重置循环")
                cycle_count = 0
            print(f"=== 第 {cycle_count} 轮按键开始 ===")
            
            # 1. 执行设置的按键序列
            for i, key in enumerate(keys):
                if not self.running:  # 检查是否需要停止
                    print("收到停止信号，退出按键循环")
                    return
                keyboard_simulator.pressKey(key, hwnd)
                # 按键间隔等待
                if i < len(keys) - 1:  # 最后一个按键后不需要等待间隔
                    time.sleep(self.key_interval)
            
            # 2. 执行默认按键
            # 2.0 召唤宠物
            if cycle_count % 20 == 0:
                keyboard_simulator.pressKey(kDefaultKey.pet_attack, hwnd)
            keyboard_simulator.pressKey(kDefaultKey.pet_eat, hwnd)
            
            # 2.1 如果自己空蓝，点击血迹
            mp_color_p1 = color_detector.getPixelPosColorInWindow(hwnd, kMPBar.player1.x, kMPBar.player1.y)
            if color_detector.isEmpty(mp_color_p1):
                keyboard_simulator.pressKey(kDefaultKey.xue_ji, hwnd)
            
            # 2.1 峨眉
            if self.is_em:
                # p1相关条件
                is_p1_alive = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p1_low.x, kHPBar.p1_low.y))
                is_p1_mid_hp = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p1_mid.x, kHPBar.p1_mid.y))
                is_p1_high_hp = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p1_high.x, kHPBar.p1_high.y))
                
                # p2相关条件
                is_p2_alive = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p2_low.x, kHPBar.p2_low.y))
                is_p2_mid_hp = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p2_mid.x, kHPBar.p2_mid.y))
                is_p2_high_hp = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p2_high.x, kHPBar.p2_high.y))
                
                # p3相关条件
                is_p3_alive = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p3_low.x, kHPBar.p3_low.y))
                is_p3_mid_hp = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p3_mid.x, kHPBar.p3_mid.y))
                is_p3_high_hp = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p3_high.x, kHPBar.p3_high.y))
                
                # p4相关条件
                is_p4_alive = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p4_low.x, kHPBar.p4_low.y))
                is_p4_mid_hp = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p4_mid.x, kHPBar.p4_mid.y))
                is_p4_high_hp = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p4_high.x, kHPBar.p4_high.y))
                
                # p5相关条件
                is_p5_alive = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p5_low.x, kHPBar.p5_low.y))
                is_p5_mid_hp = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p5_mid.x, kHPBar.p5_mid.y))
                is_p5_high_hp = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p5_high.x, kHPBar.p5_high.y))
                
                # p6相关条件
                is_p6_alive = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p6_low.x, kHPBar.p6_low.y))
                is_p6_mid_hp = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p6_mid.x, kHPBar.p6_mid.y))
                is_p6_high_hp = color_detector.isRed(color_detector.getPixelPosColorInWindow(hwnd, kHPBar.p6_high.x, kHPBar.p6_high.y))
                
                # 峨眉治疗逻辑：两级优先级治疗系统
                healed = False  # 标记是否已经治疗了某个队友
                
                # 第一优先级：紧急治疗 - 检查血量不足中等水平的队友
                if not healed:
                    # 检查p1
                    if is_p1_alive and not is_p1_mid_hp:
                        print("p1血量不足中等水平，紧急治疗")
                        keyboard_simulator.mouseClick(kProfilePhoto.player1.x, kProfilePhoto.player1.y, hwnd)
                        keyboard_simulator.pressKey(kDefaultKey.qing_xin, hwnd)
                        healed = True
                    
                    # 检查p2
                    elif is_p2_alive and not is_p2_mid_hp:
                        print("p2血量不足中等水平，紧急治疗")
                        keyboard_simulator.mouseClick(kProfilePhoto.player2.x, kProfilePhoto.player2.y, hwnd)
                        keyboard_simulator.pressKey(kDefaultKey.qing_xin, hwnd)
                        healed = True
                    
                    # 检查p3
                    elif is_p3_alive and not is_p3_mid_hp:
                        print("p3血量不足中等水平，紧急治疗")
                        keyboard_simulator.mouseClick(kProfilePhoto.player3.x, kProfilePhoto.player3.y, hwnd)
                        keyboard_simulator.pressKey(kDefaultKey.qing_xin, hwnd)
                        healed = True
                    
                    # 检查p4
                    elif is_p4_alive and not is_p4_mid_hp:
                        print("p4血量不足中等水平，紧急治疗")
                        keyboard_simulator.mouseClick(kProfilePhoto.player4.x, kProfilePhoto.player4.y, hwnd)
                        keyboard_simulator.pressKey(kDefaultKey.qing_xin, hwnd)
                        healed = True
                    
                    # 检查p5
                    elif is_p5_alive and not is_p5_mid_hp:
                        print("p5血量不足中等水平，紧急治疗")
                        keyboard_simulator.mouseClick(kProfilePhoto.player5.x, kProfilePhoto.player5.y, hwnd)
                        keyboard_simulator.pressKey(kDefaultKey.qing_xin, hwnd)
                        healed = True
                    
                    # 检查p6
                    elif is_p6_alive and not is_p6_mid_hp:
                        print("p6血量不足中等水平，紧急治疗")
                        keyboard_simulator.mouseClick(kProfilePhoto.player6.x, kProfilePhoto.player6.y, hwnd)
                        keyboard_simulator.pressKey(kDefaultKey.qing_xin, hwnd)
                        healed = True
                
                # 第二优先级：预防性治疗 - 当所有人都有中等血量时，提升到高血量
                if not healed:
                    # 检查p1
                    if is_p1_alive and is_p1_mid_hp and not is_p1_high_hp:
                        print("p1血量中等，预防性加血到高血量")
                        keyboard_simulator.mouseClick(kProfilePhoto.player1.x, kProfilePhoto.player1.y, hwnd)
                        keyboard_simulator.pressKey(kDefaultKey.qing_xin, hwnd)
                        healed = True
                    
                    # 检查p2
                    elif is_p2_alive and is_p2_mid_hp and not is_p2_high_hp:
                        print("p2血量中等，预防性加血到高血量")
                        keyboard_simulator.mouseClick(kProfilePhoto.player2.x, kProfilePhoto.player2.y, hwnd)
                        keyboard_simulator.pressKey(kDefaultKey.qing_xin, hwnd)
                        healed = True
                    
                    # 检查p3
                    elif is_p3_alive and is_p3_mid_hp and not is_p3_high_hp:
                        print("p3血量中等，预防性加血到高血量")
                        keyboard_simulator.mouseClick(kProfilePhoto.player3.x, kProfilePhoto.player3.y, hwnd)
                        keyboard_simulator.pressKey(kDefaultKey.qing_xin, hwnd)
                        healed = True
                    
                    # 检查p4
                    elif is_p4_alive and is_p4_mid_hp and not is_p4_high_hp:
                        print("p4血量中等，预防性加血到高血量")
                        keyboard_simulator.mouseClick(kProfilePhoto.player4.x, kProfilePhoto.player4.y, hwnd)
                        keyboard_simulator.pressKey(kDefaultKey.qing_xin, hwnd)
                        healed = True
                    
                    # 检查p5
                    elif is_p5_alive and is_p5_mid_hp and not is_p5_high_hp:
                        print("p5血量中等，预防性加血到高血量")
                        keyboard_simulator.mouseClick(kProfilePhoto.player5.x, kProfilePhoto.player5.y, hwnd)
                        keyboard_simulator.pressKey(kDefaultKey.qing_xin, hwnd)
                        healed = True
                    
                    # 检查p6
                    elif is_p6_alive and is_p6_mid_hp and not is_p6_high_hp:
                        print("p6血量中等，预防性加血到高血量")
                        keyboard_simulator.mouseClick(kProfilePhoto.player6.x, kProfilePhoto.player6.y, hwnd)
                        keyboard_simulator.pressKey(kDefaultKey.qing_xin, hwnd)
                        healed = True
                
                # 如果没有人需要治疗，输出日志
                if not healed:
                    print("所有队友血量充足，无需治疗")
                time.sleep(0.8) # 清心普善咒是有CD的
            
            # 3. 休眠时间
            print(f"第 {cycle_count} 轮按键完成，开始休眠 {self.sleep_time} 秒...")
            time.sleep(self.sleep_time)
            
            if not self.running:
                print("**************休眠期间收到停止信号，脚本退出**************")
                return
        
        print("**************自动团本循环结束**************")
        
    def stop(self):
        self.running = False


class DigSeedThread(QThread):
    """后台运行挖种子的线程"""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, hwnd: int, seed_level: int, loop_count: int, is_dig_seed: bool):
        super().__init__()
        self.hwnd = hwnd
        self.seed_level = seed_level
        self.loop_count = loop_count
        self.is_dig_seed = is_dig_seed
        self.running = True
        self.original_stdout = None
    
    def run(self):
        try:
            # 在线程中重定向stdout到UI日志
            self.original_stdout = sys.stdout
            sys.stdout = UILogStream(self.log_signal.emit)
            
            # 开始挖种子的主要逻辑
            self.digSeedProcess()
        except Exception as e:
            self.log_signal.emit(f"错误：{str(e)}")
        finally:
            # 恢复原始stdout
            if self.original_stdout:
                sys.stdout = self.original_stdout
            self.finished_signal.emit()
    
    def digSeedProcess(self):
        """挖种子的主要逻辑"""
        import time
        
        print(f"开始任务...")
        print(f"种子等级: {self.seed_level}")
        print(f"循环次数: {self.loop_count}")
        
        start_task = "挖种子" if self.is_dig_seed else "打怪"
        print(f"任务模式: 从{start_task}开始，挖种子和打怪交替进行")
        
        # 传递停止检查函数给DigSeed类
        dig_seed = DigSeed(self.hwnd, stop_check_func=lambda: not self.running)
        
        for i in range(self.loop_count):
            if not self.running:
                print("收到停止信号，退出任务循环")
                return
            
            # 确定当前轮次应该执行的任务类型（根据起始任务和轮次决定）
            if self.is_dig_seed:
                # 选择挖种子开始：第1轮挖种子，第2轮打怪，第3轮挖种子...
                current_is_dig_seed = (i % 2 == 0)  # 偶数轮号(i=0,2,4...)挖种子，奇数轮号(i=1,3,5...)打怪
                task_name = "挖种子" if current_is_dig_seed else "打怪"
            else:
                # 选择打怪开始：第1轮打怪，第2轮挖种子，第3轮打怪...
                current_is_dig_seed = (i % 2 == 1)  # 偶数轮号(i=0,2,4...)打怪，奇数轮号(i=1,3,5...)挖种子
                task_name = "打怪" if (i % 2 == 0) else "挖种子"
            
            print(f"=== 第 {i+1}/{self.loop_count} 轮{task_name}开始 ===")
            
            try:
                success = dig_seed.digSeed(seed_level=self.seed_level, is_dig_seed=current_is_dig_seed)
                if success:
                    print(f"第 {i+1} 轮{task_name}完成")
                elif success is False:
                    # 如果返回False，可能是被中断了
                    if not self.running:
                        print(f"第 {i+1} 轮{task_name}被用户中断")
                        return
                    else:
                        print(f"第 {i+1} 轮{task_name}失败, 下马")
                        dig_seed.getDownHorse()
            except Exception as e:
                print(f"第 {i+1} 轮{task_name}出现异常: {str(e)}")
                if not self.running:
                    print("检测到停止信号，退出任务循环")
                    return
            
            # 每轮之间的间隔
            if i < self.loop_count - 1 and self.running:
                print("等待1秒后开始下一轮...")
                time.sleep(1)
        
        print("**************任务完成**************")
    
    def stop(self):
        self.running = False


class AutoReturnThread(QThread):
    """后台运行自动回点的线程"""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, hwnd: int, scene_type: str, x: str, y: str, is_return_immediately: bool, interval_time: int):
        super().__init__()
        self.hwnd = hwnd
        self.scene_type = scene_type
        self.x = x
        self.y = y
        self.is_return_immediately = is_return_immediately
        self.interval_time = interval_time
        self.running = True
        self.original_stdout = None
    
    def run(self):
        try:
            # 在线程中重定向stdout到UI日志
            self.original_stdout = sys.stdout
            sys.stdout = UILogStream(self.log_signal.emit)
            
            # 开始自动回点的主要逻辑
            self.autoReturnProcess()
        except Exception as e:
            self.log_signal.emit(f"错误：{str(e)}")
        finally:
            # 恢复原始stdout
            if self.original_stdout:
                sys.stdout = self.original_stdout
            self.finished_signal.emit()
    
    def autoReturnProcess(self):
        """自动回点的主要逻辑"""
        print(f"开始自动回点任务...")
        print(f"场景: {self.scene_type}")
        print(f"坐标: ({self.x}, {self.y})")
        print(f"死亡后立即起身: {'是' if self.is_return_immediately else '否'}")
        print(f"循环间隔: {self.interval_time}秒")
        
        # 创建AutoReturn实例
        auto_return = AutoReturn(self.hwnd)
        
        cycle_count = 0
        while self.running:
            cycle_count += 1
            print(f"=== 第 {cycle_count} 轮自动回点开始，休眠时间 {self.interval_time} 秒 ===")
            
            try:
                if self.scene_type == "雪原":
                    auto_return.toXueYuan(self.x, self.y, self.is_return_immediately)
                elif self.scene_type == "四象":
                    # 上马
                    if cycle_count == 1:
                        auto_return._getUpHorse()
                        time.sleep(1)
                    auto_return.toSiXiang()
                else:
                    print(f"暂不支持场景: {self.scene_type}")
                    
            except Exception as e:
                print(f"第 {cycle_count} 轮回点出现异常: {str(e)}")
                if not self.running:
                    print("检测到停止信号，退出回点循环")
                    return
            
            # 循环间隔等待
            if self.running:
                print(f"第 {cycle_count} 轮回点完成，等待 {self.interval_time} 秒后开始下一轮...")
                for i in range(self.interval_time):
                    if not self.running:
                        print("**************等待期间收到停止信号，脚本退出**************")
                        return
                    time.sleep(1)
        
        print("**************自动回点循环结束**************")
    
    def stop(self):
        self.running = False


class GameUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.raid_thread = None
        self.window_list = None
        self.hwnd: int = -1         # -1 表示未选择窗口
        self.window_manager = WindowManager()
        self.original_stdout = sys.stdout  # 保存原始stdout
        
        # 1. 创建临时日志收集器
        temp_logs = []
        def tempLog(message):
            temp_logs.append(message)  # 先把消息存到列表里

        # 2. 先重定向到临时收集器
        sys.stdout = UILogStream(tempLog)

        # 3. 创建UI（这个过程中可能有print输出）
        self.initUI()

        # 4. UI创建完成后，把临时收集的日志添加到真正的UI日志窗口
        for log in temp_logs:
            self.addLog(log)  # 现在self.log_text已经存在了

        # 5. 将stdout重定向到真正的UI日志系统
        sys.stdout = UILogStream(self.addLog)
    
    def initUI(self):
        self.setWindowTitle('豆子')
        self.setGeometry(100, 100, 500, 400)
        
        # 设置窗口图标（如果图标文件存在）
        icon_path = os.path.join(kBaseDir, "icon.ico")
        if icon_path and os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 添加窗口选择区域（共用）
        main_layout.addWidget(self.createWindowSelectionArea())
        
        # 创建选项卡
        self.tab_widget = QTabWidget()
        
        # 第一个选项卡：按键配置
        key_config_tab = QWidget()
        key_config_layout = QVBoxLayout(key_config_tab)
        key_config_layout.addWidget(self.createKeyConfigArea())
        self.tab_widget.addTab(key_config_tab, "按键配置")
        
        # 第二个选项卡：自动按键
        auto_key_tab = QWidget()
        auto_key_layout = QVBoxLayout(auto_key_tab)
        auto_key_layout.addWidget(self.createControlArea())
        self.tab_widget.addTab(auto_key_tab, "自动按键")
        
        # 第三个选项卡：挖种子
        dig_seed_tab = QWidget()
        dig_seed_layout = QVBoxLayout(dig_seed_tab)
        dig_seed_layout.addWidget(self.createDigSeedArea())
        self.tab_widget.addTab(dig_seed_tab, "挖种子")
        
        # 第四个选项卡：自动回点
        auto_return_tab = QWidget()
        auto_return_layout = QVBoxLayout(auto_return_tab)
        auto_return_layout.addWidget(self.createAutoReturnArea())
        self.tab_widget.addTab(auto_return_tab, "自动回点")
        
        # 第五个选项卡：版本历史
        update_log_tab = QWidget()
        update_log_layout = QVBoxLayout(update_log_tab)
        update_log_layout.addWidget(self.createUpdateLogArea())
        self.tab_widget.addTab(update_log_tab, "版本历史")
        
        # 添加共享的日志区域
        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.createLogArea())
        
        # 初始状态：禁用除按键配置外的其他选项卡
        self.keys_configured = False
        self.updateTabStates()
        
        # 检查是不是由管理员运行
        if self.window_manager.isAdmin():
            print("✓ 当前程序以管理员权限运行")
        else:
            print("⚠ 当前程序以普通用户权限运行，部分功能无法启用，请重新以管理员身份运行...")
    
    def createWindowSelectionArea(self):
        """创建窗口选择区域"""
        group = QGroupBox("选择游戏窗口")
        layout = QVBoxLayout(group)
        
        # layout_1
        layout_1 = QHBoxLayout()
        show_btn = QPushButton("刷新窗口列表")
        show_btn.clicked.connect(self.showAllWindows)
        layout_1.addWidget(show_btn)
        
        # layout_2：窗口选择下拉框和激活按钮
        layout_2 = QHBoxLayout()
        layout_2.addWidget(QLabel("选择窗口:"))
        
        self.window_combobox = QComboBox()
        self.window_combobox.addItem("请先刷新窗口列表", -1)  # 默认项
        self.window_combobox.setMinimumWidth(300)  # 设置最小宽度以显示完整标题
        layout_2.addWidget(self.window_combobox)
        
        # 激活窗口按钮
        self.activate_btn = QPushButton("激活选中窗口")
        self.activate_btn.clicked.connect(self.activateWindow)
        self.activate_btn.setEnabled(False)  # 初始状态禁用
        layout_2.addWidget(self.activate_btn)
        
        # 当前窗口状态显示
        layout.addLayout(layout_1)
        layout.addLayout(layout_2)
        self.window_status_label = QLabel("当前窗口: 未选择")
        self.window_status_label.setStyleSheet("color: gray;")
        layout.addWidget(self.window_status_label)
        
        return group
    
    def createControlArea(self):
        """创建自动团本控制区域"""
        control_group = QGroupBox("自动按键控制")
        control_layout = QVBoxLayout(control_group)
        # 1. 按键序列布局
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("按键序列:"))
        
        # 按键序列输入
        self.key_sequence_input = QLineEdit()
        self.key_sequence_input.setText("Q E")  # 默认值
        key_layout.addWidget(self.key_sequence_input)
        
        # 按键序列帮助图标
        help_label = QLabel("❓")
        help_label.setFixedSize(20, 20)
        help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        help_label.setToolTip("点击查看详细帮助说明")
        help_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  # 设置鼠标指针为手型
        help_label.mousePressEvent = lambda ev: self.showHelpDialog()  # 点击事件
        key_layout.addWidget(help_label)
        
        # 2. spinbox 布局
        spinbox_layout = QHBoxLayout()
        
        # 按键间隔
        spinbox_layout.addWidget(QLabel("按键间隔(秒):"))
        self.time_key_interval_spinbox = QDoubleSpinBox()
        self.time_key_interval_spinbox.setRange(0.0, 10.0)
        self.time_key_interval_spinbox.setValue(0.1)
        self.time_key_interval_spinbox.setSingleStep(0.1)  # 设置步长为0.1
        self.time_key_interval_spinbox.setDecimals(1)       # 设置小数位数为1位
        self.time_key_interval_spinbox.setSuffix("秒")
        spinbox_layout.addWidget(self.time_key_interval_spinbox)
        
        # 休眠时间
        spinbox_layout.addWidget(QLabel("休眠时间(秒):"))
        self.time_to_sleep_spinbox = QDoubleSpinBox()
        self.time_to_sleep_spinbox.setRange(0.0, 10.0)
        self.time_to_sleep_spinbox.setValue(1.0)
        self.time_to_sleep_spinbox.setSingleStep(0.1)  # 设置步长为0.1
        self.time_to_sleep_spinbox.setDecimals(1)       # 设置小数位数为1位
        self.time_to_sleep_spinbox.setSuffix("秒")
        spinbox_layout.addWidget(self.time_to_sleep_spinbox)
        
        # 是否是em
        self.is_em_checkbox = QCheckBox("是否是峨眉") 
        spinbox_layout.addWidget(self.is_em_checkbox)

        
        # 3. 按钮布局
        button_layout = QHBoxLayout()
        
        # 开始按钮
        self.start_btn = QPushButton("开始自动按键")
        self.start_btn.clicked.connect(self.startRaidThread)
        self.start_btn.setEnabled(False)  # 初始状态禁用
        button_layout.addWidget(self.start_btn)
        
        # 停止按钮
        self.stop_btn = QPushButton("停止")
        self.stop_btn.clicked.connect(self.stopThread)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        control_layout.addLayout(key_layout)
        control_layout.addLayout(spinbox_layout)
        control_layout.addLayout(button_layout)
        return control_group
    
    def createLogArea(self):
        """创建统一的运行日志区域"""
        log_group = QGroupBox("运行日志")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #f5f5f5; border: 1px solid #ddd;")
        log_layout.addWidget(self.log_text)
        
        # 清除日志按钮
        clear_log_btn = QPushButton("清除日志")
        clear_log_btn.clicked.connect(self.clearLog)
        log_layout.addWidget(clear_log_btn)
        
        return log_group
    
    def createKeyConfigArea(self):
        """创建按键配置区域"""
        group = QGroupBox("脚本按键设置")
        layout = QVBoxLayout(group)
        
        # 说明文字
        info_label = QLabel("请先设置游戏中的按键，并且在游戏中打开非聊天模式：")
        info_label.setStyleSheet("color: #666; font-size: 12px; padding: 5px; font-weight: bold;")
        layout.addWidget(info_label)
        
        # 按键配置表单布局
        grid_layout = QGridLayout()
        
        # 创建按键输入控件
        key_configs = [
            ("召唤珍兽", "pet_attack", kDefaultKey.pet_attack),
            ("珍兽药品", "pet_eat", kDefaultKey.pet_eat),
            ("血迹", "xue_ji", kDefaultKey.xue_ji),
            ("清心普善咒", "qing_xin", kDefaultKey.qing_xin),
            ("定位符", "ding_wei_fu", kDefaultKey.ding_wei_fu),
            ("骑马", "horse", kDefaultKey.horse)
        ]
        
        self.key_inputs = {}  # 存储按键输入控件
        
        for i, (display_name, attr_name, default_value) in enumerate(key_configs):
            # 计算网格位置：每行放2个配置项
            row = i // 3
            col = (i % 3) * 2  # 每个配置项占2列：标签、输入框
            
            # 标签
            label = QLabel(f"{display_name}:")
            label.setMaximumWidth(100)
            grid_layout.addWidget(label, row, col)
            
            # 输入框
            input_field = QLineEdit()
            input_field.setText(default_value)
            input_field.setMaximumWidth(40)
            input_field.setPlaceholderText("按键")
            self.key_inputs[attr_name] = input_field
            grid_layout.addWidget(input_field, row, col + 1)
            
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 重置为默认值按钮
        reset_btn = QPushButton("重置为默认值")
        reset_btn.clicked.connect(self.resetKeyConfig)
        button_layout.addWidget(reset_btn)
        
        # 保存配置按钮
        save_btn = QPushButton("保存按键配置")
        save_btn.clicked.connect(self.saveKeyConfig)
        save_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        button_layout.addWidget(save_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        
        # 配置状态显示
        self.config_status_label = QLabel("状态：未配置，请先配置按键后才能使用其他功能")
        self.config_status_label.setStyleSheet("color: #f44336; font-weight: bold;")
        
        layout.addLayout(grid_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.config_status_label)
        
        return group
    
    def createDigSeedArea(self):
        """创建挖种子控制区域"""
        dig_seed_group = QGroupBox("挖种子控制")
        dig_seed_layout = QVBoxLayout(dig_seed_group)
        
        # 1. 参数设置布局
        param_layout = QHBoxLayout()
        
        # 种子等级
        param_layout.addWidget(QLabel("种子等级:"))
        self.seed_level_spinbox = QSpinBox()
        self.seed_level_spinbox.setRange(1, 4)
        self.seed_level_spinbox.setValue(2)
        param_layout.addWidget(self.seed_level_spinbox)
        
        # 循环次数
        param_layout.addWidget(QLabel("循环次数:"))
        self.loop_count_spinbox = QSpinBox()
        self.loop_count_spinbox.setRange(1, 20)
        self.loop_count_spinbox.setValue(10)
        param_layout.addWidget(self.loop_count_spinbox)
        
        # 任务类型
        param_layout.addWidget(QLabel("起始任务:"))
        self.task_type_combo = QComboBox()
        self.task_type_combo.addItem("挖种子", True)
        self.task_type_combo.addItem("打怪", False)
        param_layout.addWidget(self.task_type_combo)
        
        # 帮助图标
        dig_seed_help_label = QLabel("❓")
        dig_seed_help_label.setFixedSize(20, 20)
        dig_seed_help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dig_seed_help_label.setToolTip("点击查看挖种子使用说明")
        dig_seed_help_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        dig_seed_help_label.mousePressEvent = lambda ev: self.showDigSeedHelpDialog()
        param_layout.addWidget(dig_seed_help_label)
        
        # 2. 按钮布局
        button_layout = QHBoxLayout()
        
        # 开始按钮
        self.dig_seed_start_btn = QPushButton("开始挖种子")
        self.dig_seed_start_btn.clicked.connect(self.startDigSeedThread)
        self.dig_seed_start_btn.setEnabled(False)  # 初始状态禁用
        button_layout.addWidget(self.dig_seed_start_btn)
        
        # 停止按钮
        self.dig_seed_stop_btn = QPushButton("停止")
        self.dig_seed_stop_btn.clicked.connect(self.stopDigSeedThread)
        self.dig_seed_stop_btn.setEnabled(False)
        button_layout.addWidget(self.dig_seed_stop_btn)
        
        dig_seed_layout.addLayout(param_layout)
        dig_seed_layout.addLayout(button_layout)
        
        return dig_seed_group
    
    def createAutoReturnArea(self):
        """创建自动回点控制区域"""
        auto_return_group = QGroupBox("自动回点控制")
        auto_return_layout = QVBoxLayout(auto_return_group)
        
        # 1. 场景选择布局
        scene_layout = QHBoxLayout()
        scene_layout.addWidget(QLabel("选择场景:"))
        self.scene_combo = QComboBox()
        self.scene_combo.addItem("雪原", "雪原")
        self.scene_combo.addItem("四象回点", "四象")
        # 可以在这里添加更多场景选项
        # self.scene_combo.addItem("其他场景", "其他场景")
        self.scene_combo.currentTextChanged.connect(self.onSceneChanged)
        scene_layout.addWidget(self.scene_combo)
        
        # 帮助图标
        auto_return_help_label = QLabel("❓")
        auto_return_help_label.setFixedSize(20, 20)
        auto_return_help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        auto_return_help_label.setToolTip("点击查看自动回点使用说明")
        auto_return_help_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        auto_return_help_label.mousePressEvent = lambda ev: self.showAutoReturnHelpDialog()
        scene_layout.addWidget(auto_return_help_label)
        
        scene_layout.addStretch()  # 添加弹性空间
        
        # 2. 坐标输入布局
        coord_layout = QHBoxLayout()
        self.x_coord_label = QLabel("X坐标:")
        coord_layout.addWidget(self.x_coord_label)
        self.x_coord_input = QLineEdit()
        self.x_coord_input.setText("107")  # 默认值
        self.x_coord_input.setMaximumWidth(100)
        coord_layout.addWidget(self.x_coord_input)
        
        self.y_coord_label = QLabel("Y坐标:")
        coord_layout.addWidget(self.y_coord_label)
        self.y_coord_input = QLineEdit()
        self.y_coord_input.setText("109")  # 默认值
        self.y_coord_input.setMaximumWidth(100)
        coord_layout.addWidget(self.y_coord_input)
        coord_layout.addStretch()  # 添加弹性空间
        
        # 3. 选项设置布局
        option_layout = QHBoxLayout()
        self.return_immediately_checkbox = QCheckBox("死亡后立即起身")
        option_layout.addWidget(self.return_immediately_checkbox)
        
        option_layout.addWidget(QLabel("循环间隔(秒):"))
        self.return_interval_spinbox = QSpinBox()
        self.return_interval_spinbox.setRange(1, 3600)
        self.return_interval_spinbox.setValue(20)  # 默认20秒
        self.return_interval_spinbox.setSuffix("秒")
        option_layout.addWidget(self.return_interval_spinbox)
        option_layout.addStretch()  # 添加弹性空间
        
        # 4. 按钮布局
        button_layout = QHBoxLayout()
        
        # 开始按钮
        self.auto_return_start_btn = QPushButton("开始自动回点")
        self.auto_return_start_btn.clicked.connect(self.startAutoReturnThread)
        self.auto_return_start_btn.setEnabled(False)  # 初始状态禁用
        button_layout.addWidget(self.auto_return_start_btn)
        
        # 停止按钮
        self.auto_return_stop_btn = QPushButton("停止")
        self.auto_return_stop_btn.clicked.connect(self.stopAutoReturnThread)
        self.auto_return_stop_btn.setEnabled(False)
        button_layout.addWidget(self.auto_return_stop_btn)
        
        auto_return_layout.addLayout(scene_layout)
        auto_return_layout.addLayout(coord_layout)
        auto_return_layout.addLayout(option_layout)
        auto_return_layout.addLayout(button_layout)
        
        return auto_return_group
    
    def createUpdateLogArea(self):
        """创建版本历史区域"""
        update_log_group = QGroupBox("版本历史")
        update_log_layout = QVBoxLayout(update_log_group)
        
        # 版本历史显示区域
        self.update_log_text = QTextEdit()
        self.update_log_text.setReadOnly(True)
        self.update_log_text.setStyleSheet("background-color: #f5f5f5; border: 1px solid #ddd;")
        update_log_layout.addWidget(self.update_log_text)
        
        # 刷新按钮
        refresh_btn = QPushButton("刷新版本历史")
        refresh_btn.clicked.connect(self.loadVersionHistory)
        update_log_layout.addWidget(refresh_btn)
        
        # 加载版本历史
        self.loadVersionHistory()
        
        return update_log_group
    
    def showAllWindows(self):
        """展示所有窗口"""
        self.window_list = self.window_manager.getAllWindows()
        if not self.window_list:
            print("未找到任何窗口")
            self.window_combobox.clear()
            self.window_combobox.addItem("未找到窗口", -1)
            self.activate_btn.setEnabled(False)
            return
        
        # 清空下拉框并重新填充
        self.window_combobox.clear()
        
        for i, (hwnd, title) in enumerate(self.window_list):
            # 限制标题长度，避免下拉框过宽
            display_title = title[:50] + "..." if len(title) > 50 else title
            display_text = f"[{i+1}] [{hwnd}] {display_title}"
            self.window_combobox.addItem(display_text, hwnd)  # hwnd作为数据存储
        
        # 启用激活按钮
        self.activate_btn.setEnabled(True)
        print(f"窗口列表已更新，请从下拉框中选择要激活的窗口")
    
    def activateWindow(self):
        """激活指定的游戏窗口"""
        # 获取当前选中的窗口句柄
        current_index = self.window_combobox.currentIndex()
        if current_index < 0:
            self.addLog("请先选择一个窗口")
            return
        
        hwnd = self.window_combobox.currentData()  # 获取存储的hwnd
        if hwnd == -1:
            self.addLog("请先刷新窗口列表并选择有效窗口")
            return
        
        try:
            success = self.window_manager.activateWindow(hwnd)
            if success:
                self.hwnd = hwnd
                self.window_status_label.setText(f"当前窗口: [{hwnd}] {self.window_combobox.currentText().split('] ', 1)[1] if '] ' in self.window_combobox.currentText() else ''}")
                self.window_status_label.setStyleSheet("color: green;")
                self.start_btn.setEnabled(True)
                self.dig_seed_start_btn.setEnabled(True)  # 同时启用挖种子按钮
                self.auto_return_start_btn.setEnabled(True)  # 同时启用自动回点按钮
            else:
                self.window_status_label.setText("当前窗口: 激活失败")
                self.window_status_label.setStyleSheet("color: red;")
                self.start_btn.setEnabled(False)
                self.dig_seed_start_btn.setEnabled(False)
                self.auto_return_start_btn.setEnabled(False)
                
        except Exception as e:
            self.addLog(f"激活窗口时出错: {str(e)}")
            self.window_status_label.setText("当前窗口: 错误")
            self.window_status_label.setStyleSheet("color: red;")
    
    def startRaidThread(self):
        """触发团本线程"""
        hwnd = self.hwnd
        if hwnd == -1:
            self.addLog("请先选择有效的窗口")
            return
        
        # 从UI获取参数
        key_interval: float = self.time_key_interval_spinbox.value()
        sleep_time: float = self.time_to_sleep_spinbox.value()
        is_em: bool = self.is_em_checkbox.isChecked()
        key_sequence: str = self.key_sequence_input.text().strip()
        
        # 验证参数
        if not key_sequence:
            self.addLog("请输入按键序列")
            return
        
        # 显示启动信息
        print(f"***************** 脚本开始启动 *****************")
        
        # 创建线程时传递参数
        self.raid_thread = RaidThread(hwnd, self.addLog, key_interval, sleep_time, is_em, key_sequence)
        self.raid_thread.log_signal.connect(self.addLog)
        # 无论线程是如何结束的（正常完成、异常退出、或被停止），
        # run() 方法的 finally 块都会执行，发出 finished_signal 信号。
        self.raid_thread.finished_signal.connect(self.afterThreadFinished)
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.activate_btn.setEnabled(False)
        
        self.raid_thread.start()    # 启动线程，会调用self.raid_thread.run()方法
    
    def stopThread(self):
        """停止自动团本线程"""
        if self.raid_thread and self.raid_thread.isRunning():
            self.raid_thread.stop()        # 设置停止标志
            self.raid_thread.wait()        # 等待线程真正结束
    
    def afterThreadFinished(self):
        """线程结束后的处理"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.activate_btn.setEnabled(True)
    
    def addLog(self, message: str):
        """添加日志信息（统一的日志方法）"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        
        # 自动滚动到底部
        scrollbar = self.log_text.verticalScrollBar()
        if scrollbar:
            scrollbar.setValue(scrollbar.maximum())
    
    def clearLog(self):
        """清除日志（统一的日志清除方法）"""
        self.log_text.clear()
        self.addLog("日志已清除")
    
    def closeEvent(self, event):
        """窗口关闭时恢复原始stdout"""
        if self.original_stdout:
            sys.stdout = self.original_stdout
        event.accept()
    
    def showHelpDialog(self):
        """显示帮助对话框"""
        help_text = ""
        help_text += """
1. 按键序列：
    • 格式：用空格分隔多个按键，如：F1 F2 Q W E
    • 支持的按键：
        - 字母键：A-Z
        - 数字键：0-9
        - 功能键：F1-F10
        - 特殊键：SPACE, ENTER, TAB, ESC等
2. 时间设置：
    • 按键间隔：每个按键之间的等待时间
    • 休眠时间：一轮按键完成后的休息时间
    • 建议值：按键间隔0.1-0.5秒，休眠时间1-3秒
3. 是否是峨眉
    • 如果勾选，则会自动判断队友的血条，当需要加血时，会使用清心加血
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("帮助文档")
        msg.setText(help_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.resize(500, 400)  # 设置对话框大小
        msg.exec_()

    def saveKeyConfig(self):
        """保存按键配置"""
        # 获取所有按键的当前值
        saved_keys = {}
        for attr_name, input_field in self.key_inputs.items():
            key_value = input_field.text().strip()
            if not key_value:
                QMessageBox.warning(self, "警告", f"请为 {attr_name} 设置一个按键值！")
                return
            saved_keys[attr_name] = key_value
        
        # 更新kDefaultKey中的值
        kDefaultKey.pet_attack = saved_keys.get("pet_attack", kDefaultKey.pet_attack)
        kDefaultKey.pet_eat = saved_keys.get("pet_eat", kDefaultKey.pet_eat)
        kDefaultKey.xue_ji = saved_keys.get("xue_ji", kDefaultKey.xue_ji)
        kDefaultKey.qing_xin = saved_keys.get("qing_xin", kDefaultKey.qing_xin)
        kDefaultKey.ding_wei_fu = saved_keys.get("ding_wei_fu", kDefaultKey.ding_wei_fu)
        kDefaultKey.horse = saved_keys.get("horse", kDefaultKey.horse)

        # 启用其他选项卡
        self.keys_configured = True
        self.updateTabStates()
        
        # 更新配置状态标签
        self.config_status_label.setText("状态：按键配置已保存，其他功能已启用")
        self.config_status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")

        QMessageBox.information(self, "提示", "按键配置已保存，其他功能已启用！")

    def resetKeyConfig(self):
        """重置按键配置为默认值"""
        # 直接设置默认值
        default_values = {
            "pet_attack": "F5",
            "pet_eat": "F6", 
            "xue_ji": "F7",
            "qing_xin": "F8",
            "ding_wei_fu": "F9",
            "horse": "F10"
        }
        
        # 更新kDefaultKey对象
        kDefaultKey.pet_attack = default_values["pet_attack"]
        kDefaultKey.pet_eat = default_values["pet_eat"]
        kDefaultKey.xue_ji = default_values["xue_ji"]
        kDefaultKey.qing_xin = default_values["qing_xin"]
        kDefaultKey.ding_wei_fu = default_values["ding_wei_fu"]
        kDefaultKey.horse = default_values["horse"]
        
        # 更新UI输入框
        for attr_name, input_field in self.key_inputs.items():
            input_field.setText(default_values[attr_name])
            
        self.config_status_label.setText("状态：已重置为默认值")
        self.config_status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        QMessageBox.information(self, "提示", "按键配置已重置为默认值！")

    def updateTabStates(self):
        """根据按键配置状态更新选项卡的启用/禁用状态"""
        self.tab_widget.setTabEnabled(1, self.keys_configured) # 自动按键
        self.tab_widget.setTabEnabled(2, self.keys_configured) # 挖种子
        self.tab_widget.setTabEnabled(3, self.keys_configured) # 自动回点
        self.tab_widget.setTabEnabled(4, True) # 版本历史

    def startDigSeedThread(self):
        """开始挖种子线程"""
        hwnd = self.hwnd
        if hwnd == -1:
            self.addLog("请先选择有效的窗口")
            return
        
        # 从UI获取参数
        seed_level = self.seed_level_spinbox.value()
        loop_count = self.loop_count_spinbox.value()
        is_dig_seed = self.task_type_combo.currentData()
        
        # 显示启动信息
        self.addLog("***************** 挖种子脚本开始启动 *****************")
        
        # 创建线程
        self.dig_seed_thread = DigSeedThread(hwnd, seed_level, loop_count, is_dig_seed)
        self.dig_seed_thread.log_signal.connect(self.addLog)
        self.dig_seed_thread.finished_signal.connect(self.afterDigSeedThreadFinished)
        
        self.dig_seed_start_btn.setEnabled(False)
        self.dig_seed_stop_btn.setEnabled(True)
        self.activate_btn.setEnabled(False)
        
        self.dig_seed_thread.start()
    
    def stopDigSeedThread(self):
        """停止挖种子线程"""
        if hasattr(self, 'dig_seed_thread') and self.dig_seed_thread and self.dig_seed_thread.isRunning():
            self.dig_seed_thread.stop()
            self.dig_seed_thread.wait()
    
    def afterDigSeedThreadFinished(self):
        """挖种子线程结束后的处理"""
        self.dig_seed_start_btn.setEnabled(True)
        self.dig_seed_stop_btn.setEnabled(False)
        self.activate_btn.setEnabled(True)
    
    def startAutoReturnThread(self):
        """开始自动回点线程"""
        hwnd = self.hwnd
        if hwnd == -1:
            self.addLog("请先选择有效的窗口")
            return
        
        # 从UI获取参数
        scene_type = self.scene_combo.currentData()
        x = self.x_coord_input.text().strip()
        y = self.y_coord_input.text().strip()
        is_return_immediately = self.return_immediately_checkbox.isChecked()
        interval_time = self.return_interval_spinbox.value()
        
        # 验证参数 - 只有非四象场景才需要验证坐标
        if scene_type != "四象":
            if not x or not y:
                self.addLog("请输入有效的X和Y坐标")
                return
            
            try:
                # 验证坐标是否为数字
                int(x)
                int(y)
            except ValueError:
                self.addLog("X和Y坐标必须是数字")
                return
        
        # 显示启动信息
        self.addLog("***************** 自动回点脚本开始启动 *****************")
        
        # 创建线程
        self.auto_return_thread = AutoReturnThread(hwnd, scene_type, x, y, is_return_immediately, interval_time)
        self.auto_return_thread.log_signal.connect(self.addLog)
        self.auto_return_thread.finished_signal.connect(self.afterAutoReturnThreadFinished)
        
        self.auto_return_start_btn.setEnabled(False)
        self.auto_return_stop_btn.setEnabled(True)
        self.activate_btn.setEnabled(False)
        
        self.auto_return_thread.start()
    
    def stopAutoReturnThread(self):
        """停止自动回点线程"""
        if hasattr(self, 'auto_return_thread') and self.auto_return_thread and self.auto_return_thread.isRunning():
            self.auto_return_thread.stop()
            self.auto_return_thread.wait()
    
    def afterAutoReturnThreadFinished(self):
        """自动回点线程结束后的处理"""
        self.auto_return_start_btn.setEnabled(True)
        self.auto_return_stop_btn.setEnabled(False)
        self.activate_btn.setEnabled(True)
    
    def loadVersionHistory(self):
        """加载版本历史"""
        try:
            version_history_file = os.path.join(kBaseDir, 'version_history.txt')
            
            if os.path.exists(version_history_file):
                with open(version_history_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.update_log_text.setPlainText(content)
            else:
                self.update_log_text.setPlainText("未找到version_history.txt文件")
                
        except Exception as e:
            self.update_log_text.setPlainText(f"读取版本历史失败：{str(e)}")

    def onSceneChanged(self, scene_text):
        """场景选择变化时的处理"""
        scene_data = self.scene_combo.currentData()
        if scene_data == "四象":
            # 四象回点不需要坐标，隐藏坐标输入框
            self.x_coord_label.setVisible(False)
            self.x_coord_input.setVisible(False)
            self.y_coord_label.setVisible(False)
            self.y_coord_input.setVisible(False)
            self.return_immediately_checkbox.setVisible(False)
        else:
            # 其他场景需要坐标，显示坐标输入框
            self.x_coord_label.setVisible(True)
            self.x_coord_input.setVisible(True)
            self.y_coord_label.setVisible(True)
            self.y_coord_input.setVisible(True)
            self.return_immediately_checkbox.setVisible(True)

    def showDigSeedHelpDialog(self):
        """显示挖种子帮助对话框"""
        help_text = f"""
1. 当前按键：
    定位符 = {kDefaultKey.ding_wei_fu} 骑马 = {kDefaultKey.horse}
2. 任务追踪：
    确保任务追踪打开，且只有种子任务。
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("挖种子帮助")
        msg.setText(help_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.resize(500, 400)
        msg.exec_()

    def showAutoReturnHelpDialog(self):
        """显示自动回点帮助对话框"""
        help_text = f"""
1. 当前按键：
    定位符 = {kDefaultKey.ding_wei_fu} 骑马 = {kDefaultKey.horse}
2. 坐标输入：
    需要输入回点的X和Y坐标。
    在四象场景中，坐标输入框会自动隐藏。
3. 死亡后立即起身：
    勾选后，死亡后会立即尝试起身。
4. 循环间隔：
    采用默认值即可，每隔"循环间隔"检查是否在地府。
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("自动回点帮助")
        msg.setText(help_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.resize(500, 400)
        msg.exec_()


# 自定义样式
def loadStylesheet():
    """加载样式表文件"""
    try:
        # 获取样式文件路径
        style_path = os.path.join(kBaseDir, 'styles.qss')
        
        # 读取样式文件
        if os.path.exists(style_path):
            with open(style_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            print(f"样式文件不存在: {style_path}")
            return ""
    except Exception as e:
        print(f"加载样式文件失败: {e}")
        return ""

def main():
    app = QApplication(sys.argv)    
    # 应用样式
    stylesheet = loadStylesheet()
    if stylesheet:
        app.setStyleSheet(stylesheet)
        print("样式文件加载成功")
    
    # 许可证检查 - 在显示主界面前验证授权
    try:
        from license_dialog import LicenseDialog
        
        # 检查授权状态，如果未授权则显示激活对话框
        is_authorized = LicenseDialog.checkAndShowLicense()
        
        if not is_authorized:
            print("软件未授权，程序将退出")
            sys.exit(0)
            
    except ImportError:
        print("警告：许可证检查模块未找到，跳过授权验证")
    except Exception as e:
        print(f"许可证检查时出错: {e}")
        # 可以选择是否继续运行
        # sys.exit(1)  # 取消注释此行以在授权检查失败时退出
    
    window = GameUI()
    window.show()
    
    try:
        result = app.exec_()
    finally:
        # 确保退出时恢复stdout
        if hasattr(window, 'original_stdout') and window.original_stdout:
            sys.stdout = window.original_stdout
    
    sys.exit(result)


if __name__ == '__main__':
    main()



