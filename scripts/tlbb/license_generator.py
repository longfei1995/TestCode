"""
许可证生成工具
供软件作者使用，用于生成和管理用户许可证
"""
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QGroupBox, QTextEdit, QSpinBox, QComboBox,
                            QMessageBox, QTableWidget, QTableWidgetItem,
                            QHeaderView, QDateEdit, QFormLayout)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QIcon
import os
from datetime import datetime, timedelta
from license_manager import LicenseManager, generate_license_for_hardware


class LicenseGeneratorUI(QMainWindow):
    """许可证生成工具界面"""
    
    def __init__(self):
        super().__init__()
        self.license_manager = LicenseManager()
        self.initUI()
    
    def initUI(self):
        """初始化用户界面"""
        self.setWindowTitle('许可证生成工具 - 天龙八部助手')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 标题
        title_label = QLabel("许可证生成工具")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 硬件ID查询区域
        hardware_group = QGroupBox("硬件ID查询")
        hardware_layout = QVBoxLayout(hardware_group)
        
        hardware_info_layout = QHBoxLayout()
        hardware_info_layout.addWidget(QLabel("当前设备硬件ID:"))
        
        self.current_hardware_label = QLabel(self.license_manager.get_hardware_id())
        self.current_hardware_label.setStyleSheet("font-family: monospace; background-color: #f0f0f0; padding: 5px; border: 1px solid #ccc;")
        hardware_info_layout.addWidget(self.current_hardware_label)
        
        copy_current_btn = QPushButton("复制")
        copy_current_btn.clicked.connect(self.copyCurrentHardwareId)
        hardware_info_layout.addWidget(copy_current_btn)
        
        hardware_layout.addLayout(hardware_info_layout)
        main_layout.addWidget(hardware_group)
        
        # 许可证生成区域
        generate_group = QGroupBox("生成新许可证")
        generate_layout = QFormLayout(generate_group)
        
        # 硬件ID输入
        self.hardware_id_input = QLineEdit()
        self.hardware_id_input.setPlaceholderText("输入目标设备的硬件ID")
        self.hardware_id_input.setFont(QFont("monospace"))
        generate_layout.addRow("硬件ID:", self.hardware_id_input)
        
        # 用户信息
        self.user_info_input = QLineEdit()
        self.user_info_input.setText("Licensed User")
        generate_layout.addRow("用户信息:", self.user_info_input)
        
        # 有效期类型选择
        validity_layout = QHBoxLayout()
        self.validity_combo = QComboBox()
        self.validity_combo.addItem("指定天数", "days")
        self.validity_combo.addItem("指定日期", "date")
        self.validity_combo.currentIndexChanged.connect(self.onValidityTypeChanged)
        validity_layout.addWidget(self.validity_combo)
        
        # 天数输入
        self.days_spinbox = QSpinBox()
        self.days_spinbox.setRange(1, 3650)  # 1天到10年
        self.days_spinbox.setValue(365)  # 默认1年
        self.days_spinbox.setSuffix(" 天")
        validity_layout.addWidget(self.days_spinbox)
        
        # 日期选择
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate().addYears(1))  # 默认1年后
        self.date_edit.setVisible(False)
        validity_layout.addWidget(self.date_edit)
        
        validity_layout.addStretch()
        generate_layout.addRow("有效期:", validity_layout)
        
        # 生成按钮
        generate_btn_layout = QHBoxLayout()
        self.use_current_hardware_btn = QPushButton("使用当前设备ID")
        self.use_current_hardware_btn.clicked.connect(self.useCurrentHardwareId)
        generate_btn_layout.addWidget(self.use_current_hardware_btn)
        
        self.generate_btn = QPushButton("生成许可证")
        self.generate_btn.clicked.connect(self.generateLicense)
        self.generate_btn.setDefault(True)
        generate_btn_layout.addWidget(self.generate_btn)
        
        generate_btn_layout.addStretch()
        generate_layout.addRow("", generate_btn_layout)
        
        main_layout.addWidget(generate_group)
        
        # 生成结果显示区域
        result_group = QGroupBox("生成的许可证")
        result_layout = QVBoxLayout(result_group)
        
        self.license_output = QTextEdit()
        self.license_output.setMaximumHeight(100)
        self.license_output.setPlaceholderText("生成的许可证将显示在这里...")
        result_layout.addWidget(self.license_output)
        
        result_btn_layout = QHBoxLayout()
        self.copy_license_btn = QPushButton("复制许可证")
        self.copy_license_btn.clicked.connect(self.copyLicense)
        self.copy_license_btn.setEnabled(False)
        result_btn_layout.addWidget(self.copy_license_btn)
        
        self.test_license_btn = QPushButton("测试许可证")
        self.test_license_btn.clicked.connect(self.testLicense)
        self.test_license_btn.setEnabled(False)
        result_btn_layout.addWidget(self.test_license_btn)
        
        result_btn_layout.addStretch()
        result_layout.addLayout(result_btn_layout)
        
        main_layout.addWidget(result_group)
        
        # 许可证验证区域
        verify_group = QGroupBox("验证许可证")
        verify_layout = QVBoxLayout(verify_group)
        
        verify_input_layout = QHBoxLayout()
        verify_input_layout.addWidget(QLabel("许可证密钥:"))
        
        self.verify_input = QLineEdit()
        self.verify_input.setPlaceholderText("输入要验证的许可证密钥")
        verify_input_layout.addWidget(self.verify_input)
        
        self.verify_btn = QPushButton("验证")
        self.verify_btn.clicked.connect(self.verifyLicense)
        verify_input_layout.addWidget(self.verify_btn)
        
        verify_layout.addLayout(verify_input_layout)
        
        self.verify_result = QTextEdit()
        self.verify_result.setMaximumHeight(80)
        self.verify_result.setPlaceholderText("验证结果将显示在这里...")
        verify_layout.addWidget(self.verify_result)
        
        main_layout.addWidget(verify_group)
    
    def onValidityTypeChanged(self):
        """有效期类型改变时的处理"""
        is_date_mode = self.validity_combo.currentData() == "date"
        self.days_spinbox.setVisible(not is_date_mode)
        self.date_edit.setVisible(is_date_mode)
    
    def copyCurrentHardwareId(self):
        """复制当前硬件ID"""
        try:
            QApplication.clipboard().setText(self.current_hardware_label.text())
            QMessageBox.information(self, "提示", "当前设备硬件ID已复制到剪贴板")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"复制失败: {str(e)}")
    
    def useCurrentHardwareId(self):
        """使用当前设备的硬件ID"""
        self.hardware_id_input.setText(self.current_hardware_label.text())
    
    def generateLicense(self):
        """生成许可证"""
        try:
            # 获取输入参数
            hardware_id = self.hardware_id_input.text().strip()
            user_info = self.user_info_input.text().strip()
            
            if not hardware_id:
                QMessageBox.warning(self, "错误", "请输入硬件ID")
                return
            
            if not user_info:
                user_info = "Licensed User"
            
            # 计算过期日期
            if self.validity_combo.currentData() == "days":
                days = self.days_spinbox.value()
                expiry_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
            else:
                expiry_date = self.date_edit.date().toString("yyyy-MM-dd")
            
            # 生成许可证
            license_key = self.license_manager.generate_license_key(hardware_id, expiry_date, user_info)
            
            if license_key:
                self.license_output.setPlainText(license_key)
                self.copy_license_btn.setEnabled(True)
                self.test_license_btn.setEnabled(True)
                QMessageBox.information(self, "成功", f"许可证生成成功！\n\n用户: {user_info}\n过期日期: {expiry_date}")
            else:
                QMessageBox.warning(self, "错误", "许可证生成失败")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成许可证时出错:\n{str(e)}")
    
    def copyLicense(self):
        """复制生成的许可证"""
        try:
            license_text = self.license_output.toPlainText()
            if license_text:
                QApplication.clipboard().setText(license_text)
                QMessageBox.information(self, "提示", "许可证已复制到剪贴板")
            else:
                QMessageBox.warning(self, "错误", "没有可复制的许可证")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"复制失败: {str(e)}")
    
    def testLicense(self):
        """测试生成的许可证"""
        try:
            license_text = self.license_output.toPlainText()
            if not license_text:
                QMessageBox.warning(self, "错误", "没有可测试的许可证")
                return
            
            is_valid, message = self.license_manager.validate_license_key(license_text)
            
            if is_valid:
                QMessageBox.information(self, "测试结果", f"✓ 许可证有效\n\n{message}")
            else:
                QMessageBox.warning(self, "测试结果", f"✗ 许可证无效\n\n{message}")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"测试许可证时出错:\n{str(e)}")
    
    def verifyLicense(self):
        """验证输入的许可证"""
        try:
            license_key = self.verify_input.text().strip()
            if not license_key:
                QMessageBox.warning(self, "错误", "请输入许可证密钥")
                return
            
            is_valid, message = self.license_manager.validate_license_key(license_key)
            
            result_text = f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            result_text += f"验证结果: {'✓ 有效' if is_valid else '✗ 无效'}\n"
            result_text += f"详细信息: {message}"
            
            self.verify_result.setPlainText(result_text)
            
        except Exception as e:
            self.verify_result.setPlainText(f"验证出错: {str(e)}")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 检查是否有管理员权限的提示
    window = LicenseGeneratorUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main() 