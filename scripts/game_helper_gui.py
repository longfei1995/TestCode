import sys
import threading
import time
import os  # 添加 os 模块导入
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                            QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
                            QLineEdit, QPushButton, QFormLayout, QGroupBox, 
                            QMessageBox, QSpinBox, QTextEdit, QSplitter, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QColor, QTextCursor
import key_api  # 导入原始脚本
kButtonWidth = 100 # 按钮宽度
class LogStream(QObject):
    """用于重定向print输出到QTextEdit的类"""
    log_message = pyqtSignal(str)
    
    def __init__(self, text_widget, max_lines=100):
        super().__init__()
        self.text_widget = text_widget
        self.max_lines = max_lines
        self.log_message.connect(self.text_widget.append)
    
    def write(self, text):
        if text and not text.isspace():
            current_time = time.strftime("%H:%M:%S", time.localtime())
            self.log_message.emit(f"[{current_time}] {text}")
            
            # 检查日志行数并限制
            doc = self.text_widget.document()
            if doc.blockCount() > self.max_lines:
                cursor = QTextCursor(doc)
                cursor.movePosition(QTextCursor.Start)
                cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor, 0)
                cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                cursor.removeSelectedText()
                cursor.deleteChar()  # 删除换行符
    
    def flush(self):
        pass

class WorkerSignals(QObject):
    """定义信号类，用于线程和GUI通信"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    message = pyqtSignal(str)

class GameHelperGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口标题 && 大小
        self.setWindowTitle("GameHelper By: 豆子")
        self.setGeometry(100, 100, 500, 600)  # 调整窗口更大一些
        
        # 创建主布局
        self.main_widget_ = QWidget()
        self.setCentralWidget(self.main_widget_)
        self.main_layout_ = QVBoxLayout(self.main_widget_)
        
        # 创建垂直分割器
        self.splitter_ = QSplitter(Qt.Orientation.Vertical)
        self.main_layout_.addWidget(self.splitter_)
        
        # 设置选项卡和日志区域
        self.setTabs()
        self.setLog()
        
        # 添加组件到分割器 && 设置分割器初始大小
        self.splitter_.addWidget(self.tabs_widget_)
        self.splitter_.addWidget(self.log_group_)
        self.splitter_.setSizes([300, 300])
        
        # 用于存储当前运行的任务线程
        self.current_thread = None
        # 添加终止标志
        self.stop_flag = False
        
        # 重定向标准输出到日志区域
        self.log_stream = LogStream(self.log_text)
        sys.stdout = self.log_stream
        
        # 打印欢迎信息
        print("游戏辅助工具已启动，请选择功能开始...")
        
    def setTabs(self):
        """设置选项卡窗口部件及标签页"""
        # 1. 创建选项卡窗口
        self.tabs_widget_ = QWidget()
        self.tabs_layout_ = QVBoxLayout(self.tabs_widget_)
        self.tabs_ = QTabWidget()
        self.tabs_layout_.addWidget(self.tabs_)
        
        # 2. 创建三个选项卡
        self.tab_men_pai_ = QWidget()
        self.tab_fan_zei_ = QWidget()
        self.tab_dig_seed_ = QWidget()
        self.tabs_.addTab(self.tab_men_pai_, "门派挂机")
        self.tabs_.addTab(self.tab_fan_zei_, "刷反贼/光头")
        self.tabs_.addTab(self.tab_dig_seed_, "采集种子")
        
        # 初始化各选项卡的布局
        self.setMenPaiTab()
        self.setFanZeiTab()
        self.setDigSeedTab()
        
    def setLog(self):
        """设置日志区域"""
        # 创建日志区域
        self.log_group_ = QGroupBox("日志输出")
        self.log_layout = QVBoxLayout(self.log_group_)
        
        ## 0. 创建日志文本框
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.NoWrap)
        self.log_text.setStyleSheet("background-color: #f0f0f0; font-family: Consolas, monospace;")
        self.log_layout.addWidget(self.log_text)
        
        ## 1. 按钮的布局
        # 1.1 创建网格布局
        log_btn_grid = QGridLayout()
        
        # 1.2 设置网格的外边距
        log_btn_grid.setContentsMargins(10, 10, 10, 10)
        
        # 1.3 设置列伸缩因子，使按钮均匀分布
        log_btn_grid.setColumnStretch(0, 1)  # 第1列(索引0)的拉伸因子
        log_btn_grid.setColumnStretch(1, 1)  # 第2列(索引1)的拉伸因子
        
        ## 2. 按钮的添加
        # 2.1 添加清除日志按钮 - 第1列
        self.log_clear_btn_ = QPushButton("清除日志")
        self.log_clear_btn_.clicked.connect(self.clearLog)
        self.log_clear_btn_.setFixedWidth(kButtonWidth)
        log_btn_grid.addWidget(self.log_clear_btn_, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        
        # 2.2 添加保存日志按钮 - 第2列
        self.log_save_btn_ = QPushButton("保存日志")
        self.log_save_btn_.clicked.connect(self.saveLog)
        self.log_save_btn_.setFixedWidth(kButtonWidth)
        log_btn_grid.addWidget(self.log_save_btn_, 0, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        
        # 2.4 将网格布局添加到主布局
        self.log_layout.addLayout(log_btn_grid)
    
    def setMenPaiTab(self):
        """设置门派挂机选项卡"""
        layout = QVBoxLayout()
        
        ## 1. 门派选择
        # 设置布局
        form_layout = QFormLayout()
        
        # 设置选择框
        men_pai_combo = QComboBox()
        men_pai_combo.addItems(["明教", "峨眉"])
        form_layout.addRow("选择门派:", men_pai_combo)
        
        ## 2. 门派坐标
        coord_layout = QGridLayout()
        # 设置列的伸缩因子（相对宽度比例）
        coord_layout.setColumnStretch(0, 1)    # X: 标签占比较小
        coord_layout.setColumnStretch(1, 2)    # X坐标输入框占比较大
        coord_layout.setColumnStretch(2, 1)    # Y: 标签占比较小
        coord_layout.setColumnStretch(3, 2)    # Y坐标输入框占比较大
        
        # 创建x,y坐标输入
        x_label = QLabel("X:")
        x_coord_input = QLineEdit("77")
        y_label = QLabel("Y:")
        y_coord_input = QLineEdit("147")
        
        # 添加到布局
        coord_layout.addWidget(x_label, 0, 0, Qt.AlignmentFlag.AlignCenter)   # 0， 0代表放在第0行第0列
        coord_layout.addWidget(x_coord_input, 0, 1, Qt.AlignmentFlag.AlignCenter)
        coord_layout.addWidget(y_label, 0, 2, Qt.AlignmentFlag.AlignCenter)
        coord_layout.addWidget(y_coord_input, 0, 3, Qt.AlignmentFlag.AlignCenter)
        form_layout.addRow("挂机回点坐标:", coord_layout)
        
        ## 3. 打怪置信度
        confidence_input = QLineEdit("0.8")
        form_layout.addRow("怪物置信度:", confidence_input)
        
        # 添加启动按钮，使用lambda传递参数
        start_btn = QPushButton("开始挂机")
        start_btn.setFixedWidth(kButtonWidth)
        start_btn.clicked.connect(lambda: self.startMenPai(
            men_pai_combo.currentText(),
            x_coord_input.text(),
            y_coord_input.text(),
            confidence_input.text()
        ))
        
        # 添加停止按钮
        stop_btn = QPushButton("停止")
        stop_btn.setFixedWidth(kButtonWidth)
        stop_btn.clicked.connect(self.stopCurrentTask)
        
        # 组织布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(start_btn)
        btn_layout.addWidget(stop_btn)
        
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.tab_men_pai_.setLayout(layout)
    
    def setFanZeiTab(self):
        """设置刷反贼/光头选项卡"""
        layout = QVBoxLayout()
        
        # 添加选择下拉框
        form_layout = QFormLayout()
        fan_zei_combo = QComboBox()
        fan_zei_combo.addItems(["反贼", "光头"])
        form_layout.addRow("刷反/光头:", fan_zei_combo)
        
        # 添加启动按钮
        start_btn = QPushButton("开始刷怪")
        start_btn.setFixedWidth(kButtonWidth)
        start_btn.clicked.connect(lambda: self.startFanZei(
            fan_zei_combo.currentText()
        ))
        
        # 添加停止按钮
        stop_btn = QPushButton("停止")
        stop_btn.setFixedWidth(kButtonWidth)
        stop_btn.clicked.connect(self.stopCurrentTask)
        
        # 组织布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(start_btn)
        btn_layout.addWidget(stop_btn)
        
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.tab_fan_zei_.setLayout(layout)
        
    def setDigSeedTab(self):
        """设置采集种子选项卡"""
        layout = QVBoxLayout()
        
        # 添加选择下拉框
        form_layout = QFormLayout()
        
        # 采集次数选择
        iter_spin = QSpinBox()
        iter_spin.setRange(1, 10)
        iter_spin.setValue(1)
        form_layout.addRow("当前任务环数:", iter_spin)
        
        # 选择种子等级
        seed_level_combo = QComboBox()
        seed_level_combo.addItems(["1", "2"])
        form_layout.addRow("采集种子等级:", seed_level_combo)
        seed_level = 1 
        if seed_level_combo.currentText() == "1":
            seed_level = 1
        elif seed_level_combo.currentText() == "2":
            seed_level = 2
            
        # 添加启动按钮
        start_btn = QPushButton("开始采集")
        start_btn.setFixedWidth(kButtonWidth)
        start_btn.clicked.connect(lambda: self.startDigSeed(
            iter_spin.value(),
            seed_level
        ))
        
        # 添加停止按钮
        stop_btn = QPushButton("停止")
        stop_btn.setFixedWidth(kButtonWidth)
        stop_btn.clicked.connect(self.stopCurrentTask)
        
        # 组织布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(start_btn)
        btn_layout.addWidget(stop_btn)
        
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.tab_dig_seed_.setLayout(layout)
    
    def clearLog(self):
        """清除日志"""
        self.log_text.clear()
        print("日志已清除")
    
    def saveLog(self):
        """保存日志到文件"""
        try:
            # 获取脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # 创建log目录
            log_dir = os.path.join(script_dir, "log")
            os.makedirs(log_dir, exist_ok=True)
            
            # 创建日志文件名和完整路径
            current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            filename = f"game_helper_log_{current_time}.txt"
            filepath = os.path.join(log_dir, filename)
            
            # 保存日志文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.log_text.toPlainText())
            print(f"日志已保存至文件: {filepath}")
        except Exception as e:
            print(f"保存日志失败: {str(e)}")
    
    def startMenPai(self, men_pai:str, x_coord:str, y_coord:str, confidence:str):
        """开始门派挂机任务
        Args:
            men_pai (str): 门派名称
            x_coord (str): X坐标值
            y_coord (str): Y坐标值
            confidence_str (str): 识别信心度
        """
        try:
            # 转换信心度为浮点数
            confidence_float = float(confidence)
            
            # 根据选择的门派获取相应的图片路径
            scene_name = ""
            if men_pai == "明教":
                scene_name = key_api.ImagePath.MingJiao.one
            elif men_pai == "峨眉":
                scene_name = key_api.ImagePath.EMei.one
            
            # 重置停止标志
            self.stop_flag = False
            
            # 创建并启动线程
            def run_task():
                try:
                    print(f"开始在{men_pai}挂机，坐标({x_coord}, {y_coord})")
                    key_api.autoFight(scene_name, confidence_float, x_coord, y_coord, self)
                    print("挂机任务已结束")
                except Exception as e:
                    print(f"执行门派挂机时出错: {e}")
            
            if self.current_thread and self.current_thread.is_alive():
                print("警告: 有任务正在运行，请先停止当前任务")
                return
                
            self.current_thread = threading.Thread(target=run_task)
            self.current_thread.daemon = True
            self.current_thread.start()
            
        except Exception as e:
            print(f"错误: 启动挂机任务失败: {str(e)}")
    
    def startFanZei(self, monster_type):
        """开始刷反贼/光头任务"""
        try:
            # 根据选择的类型获取相应的图片路径
            scene_name = ""
            if monster_type == "反贼":
                scene_name = key_api.ImagePath.Other.fan_zei
            elif monster_type == "光头":
                scene_name = key_api.ImagePath.Other.guang_tou
            
            # 重置停止标志
            self.stop_flag = False
            
            # 创建并启动线程
            def run_task():
                try:
                    print(f"开始刷{monster_type}")
                    key_api.autoFightOther(scene_name, self)
                    print(f"刷{monster_type}任务已结束")
                except Exception as e:
                    print(f"执行刷{monster_type}时出错: {e}")
            
            if self.current_thread and self.current_thread.is_alive():
                print("警告: 有任务正在运行，请先停止当前任务")
                return
                
            self.current_thread = threading.Thread(target=run_task)
            self.current_thread.daemon = True
            self.current_thread.start()
            
        except Exception as e:
            print(f"错误: 启动刷怪任务失败: {str(e)}")
    
    def startDigSeed(self, iter_val, seed_level):
        """开始采集种子任务"""
        try:
            # 重置停止标志
            self.stop_flag = False
            # 创建并启动线程
            def run_task():
                try:
                    for i in range(5):
                        print(f"等待{5 - i}秒执行脚本....")
                        time.sleep(1)
                    for i in range(iter_val, 11):
                        print(f"开始第{i}次采集，种子等级{seed_level}")
                        key_api.autoDigSeed(iter=i, seed_level=seed_level, gui=self)
                    print("采集种子任务已结束")
                except Exception as e:
                    print(f"执行采集种子时出错: {e}")
            if self.current_thread and self.current_thread.is_alive():
                print("警告: 有任务正在运行，请先停止当前任务")
                return
            self.current_thread = threading.Thread(target=run_task)
            self.current_thread.daemon = True
            self.current_thread.start()
        except Exception as e:
            print(f"错误: 启动采集种子任务失败: {str(e)}")
    
    def stopCurrentTask(self):
        """停止当前任务"""
        if self.current_thread and self.current_thread.is_alive():
            # 设置停止标志
            self.stop_flag = True
            print("已发送停止信号，任务将在下一个循环结束")
        else:
            print("当前没有运行中的任务")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameHelperGUI()
    window.show()
    sys.exit(app.exec_()) 