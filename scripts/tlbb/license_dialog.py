"""
许可证激活对话框
用户界面部分，处理许可证输入
"""
import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QTextEdit, QGroupBox,
                            QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
import os
from game_param import kBaseDir
from license_manager import LicenseManager


class LicenseDialog(QDialog):
    """许可证激活对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.license_manager = LicenseManager()
        self.initUI()
        
        # 检查当前授权状态
        self.checkCurrentStatus()
    
    def initUI(self):
        """初始化用户界面"""
        self.setWindowTitle('软件激活 - 天龙八部助手')
        self.setFixedSize(500, 500)
        self.setModal(True)
        
        # 设置窗口图标
        icon_path = os.path.join(kBaseDir, "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 主布局
        main_layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("软件激活，纯免费软件，仅供自己使用！")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 硬件信息显示
        hardware_group = QGroupBox("设备信息")
        hardware_layout = QVBoxLayout(hardware_group)
        
        self.hardware_id = self.license_manager.get_hardware_id()
        hardware_info = QLabel(f"设备ID: {self.hardware_id}")
        hardware_info.setStyleSheet("font-family: monospace; background-color: #f0f0f0; padding: 5px; border: 1px solid #ccc;")
        hardware_info.setWordWrap(True)
        hardware_layout.addWidget(hardware_info)
        
        copy_btn = QPushButton("复制设备ID")
        copy_btn.clicked.connect(self.copyHardwareId)
        hardware_layout.addWidget(copy_btn)
        
        main_layout.addWidget(hardware_group)
        
        # 许可证输入区域
        license_group = QGroupBox("许可证密钥")
        license_layout = QVBoxLayout(license_group)
        
        license_label = QLabel("请输入许可证密钥:")
        license_layout.addWidget(license_label)
        
        self.license_input = QTextEdit()
        self.license_input.setMaximumHeight(80)
        self.license_input.setPlaceholderText("在此输入您的许可证密钥...")
        license_layout.addWidget(self.license_input)
        
        main_layout.addWidget(license_group)
        
        # 状态信息显示
        status_group = QGroupBox("当前状态")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("检查中...")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("padding: 10px; background-color: #f9f9f9; border: 1px solid #ddd;")
        status_layout.addWidget(self.status_label)
        
        main_layout.addWidget(status_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.activate_btn = QPushButton("激活")
        self.activate_btn.clicked.connect(self.activateSoftware)
        self.activate_btn.setDefault(True)
        button_layout.addWidget(self.activate_btn)
        
        self.close_btn = QPushButton("退出")
        self.close_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(button_layout)
        
        # 说明文字
        info_text = QLabel(
            "说明:\n"
            "• 请提供上方的设备ID给作者以获取许可证\n"
            "• 软件非商业软件，仅供作者及好友娱乐，不收取任何费用，不得用于任何商业用途.\n"
        )
        info_text.setStyleSheet("color: #666; font-size: 11px; padding: 10px;")
        info_text.setWordWrap(True)
        main_layout.addWidget(info_text)
    
    def copyHardwareId(self):
        """复制硬件ID到剪贴板"""
        try:
            from PyQt5.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText(self.hardware_id)
                QMessageBox.information(self, "提示", "设备ID已复制到剪贴板")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"复制失败: {str(e)}")
    
    def checkCurrentStatus(self):
        """检查当前授权状态"""
        try:
            is_authorized, status_message = self.license_manager.is_authorized()
            
            if is_authorized:
                self.status_label.setText(status_message)
                self.status_label.setStyleSheet("padding: 10px; background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724;")
                self.activate_btn.setText("关闭")
                self.activate_btn.clicked.disconnect()
                self.activate_btn.clicked.connect(self.accept)
            else:
                self.status_label.setText(status_message)
                self.status_label.setStyleSheet("padding: 10px; background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24;")
                
        except Exception as e:
            self.status_label.setText(f"状态检查失败: {str(e)}")
            self.status_label.setStyleSheet("padding: 10px; background-color: #fff3cd; border: 1px solid #ffeaa7; color: #856404;")
    
    def activateSoftware(self):
        """激活软件"""
        try:
            # 使用许可证激活
            license_key = self.license_input.toPlainText().strip()
            if not license_key:
                QMessageBox.warning(self, "错误", "请输入许可证密钥")
                return
            
            # 验证许可证
            is_valid, message = self.license_manager.validate_license_key(license_key)
            
            if is_valid:
                # 保存许可证
                if self.license_manager.save_license(license_key):
                    QMessageBox.information(self, "成功", f"许可证激活成功!\n\n{message}")
                    self.accept()
                else:
                    QMessageBox.warning(self, "错误", "许可证保存失败")
            else:
                QMessageBox.warning(self, "激活失败", message)
                        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"激活过程中发生错误:\n{str(e)}")
    
    @staticmethod
    def checkAndShowLicense(parent=None) -> bool:
        """
        检查授权状态，如果未授权则显示激活对话框
        
        Args:
            parent: 父窗口
            
        Returns:
            是否已授权
        """
        license_manager = LicenseManager()
        is_authorized, _ = license_manager.is_authorized()
        
        if is_authorized:
            return True
        
        # 显示激活对话框
        dialog = LicenseDialog(parent)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            # 重新检查授权状态
            is_authorized, _ = license_manager.is_authorized()
            return is_authorized
        
        return False


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # 测试对话框
    dialog = LicenseDialog()
    dialog.show()
    
    sys.exit(app.exec_()) 