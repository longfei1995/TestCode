import win32api
import win32con
import win32gui
import time
import random
import os
import tempfile
from typing import Union, List
from pathlib import Path
import msvcrt

class KeyboardSimulator:
    """键盘模拟器"""
    # 虚拟键码映射表
    kVirtualKeyCode = {
        # 字母键
        'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45, 'F': 0x46,
        'G': 0x47, 'H': 0x48, 'I': 0x49, 'J': 0x4A, 'K': 0x4B, 'L': 0x4C,
        'M': 0x4D, 'N': 0x4E, 'O': 0x4F, 'P': 0x50, 'Q': 0x51, 'R': 0x52,
        'S': 0x53, 'T': 0x54, 'U': 0x55, 'V': 0x56, 'W': 0x57, 'X': 0x58,
        'Y': 0x59, 'Z': 0x5A,
        
        # 数字键
        '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
        '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
        
        # 功能键
        'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73, 'F5': 0x74, 'F6': 0x75,
        'F7': 0x76, 'F8': 0x77, 'F9': 0x78, 'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B,
        
        # 特殊键
        'SPACE': 0x20, 'ENTER': 0x0D, 'TAB': 0x09, 'ESC': 0x1B, 'BACKSPACE': 0x08,
        'DELETE': 0x2E, 'INSERT': 0x2D, 'HOME': 0x24, 'END': 0x23,
        'PAGEUP': 0x21, 'PAGEDOWN': 0x22,
        
        # 方向键
        'LEFT': 0x25, 'UP': 0x26, 'RIGHT': 0x27, 'DOWN': 0x28,
        
        # 修饰键
        'SHIFT': 0x10, 'CTRL': 0x11, 'ALT': 0x12, 'WIN': 0x5B,
        'LSHIFT': 0xA0, 'RSHIFT': 0xA1, 'LCTRL': 0xA2, 'RCTRL': 0xA3,
        'LALT': 0xA4, 'RALT': 0xA5,
        
        # 小键盘
        'NUMPAD0': 0x60, 'NUMPAD1': 0x61, 'NUMPAD2': 0x62, 'NUMPAD3': 0x63,
        'NUMPAD4': 0x64, 'NUMPAD5': 0x65, 'NUMPAD6': 0x66, 'NUMPAD7': 0x67,
        'NUMPAD8': 0x68, 'NUMPAD9': 0x69, 'MULTIPLY': 0x6A, 'ADD': 0x6B,
        'SUBTRACT': 0x6D, 'DECIMAL': 0x6E, 'DIVIDE': 0x6F,
        
        # 符号键
        '`': 0xC0, '~': 0xC0,  # 反引号/波浪号键 (VK_OEM_3)
        
        # 其他常用键
        'CAPSLOCK': 0x14, 'NUMLOCK': 0x90, 'SCROLLLOCK': 0x91,
        'PAUSE': 0x13, 'PRINTSCREEN': 0x2C,
    }
    
    def __init__(self):
        # 初始化鼠标锁相关属性
        self.lock_file = Path(tempfile.gettempdir()) / "tlbb_mouse_lock.txt"
        self.lock_timeout = 10  # 10秒超时
        self.lock_file_handle = None  # 锁文件句柄
    
    def _getMouseLock(self) -> bool:
        """获取鼠标锁 - 使用文件独占锁定机制确保原子性
        Returns:
            bool: 总是返回True（一直等待直到获取成功）
        """
        while True:  # 无限循环，直到获取到锁
            try:
                # 尝试以独占方式创建锁文件
                # 使用 'x' 模式：独占创建，如果文件已存在则失败
                lock_file_handle = open(str(self.lock_file), 'x')
                
                # 成功创建文件，获取了锁
                self.lock_file_handle = lock_file_handle
                
                # 写入时间戳
                lock_file_handle.write(str(time.time()))
                lock_file_handle.flush()
                
                print(f"[鼠标锁] 成功获取锁 - 进程ID: {os.getpid()}")
                return True
                
            except FileExistsError:
                # 文件已存在，说明锁被其他进程占用
                print(f"[鼠标锁] 锁被占用，等待释放 - 进程ID: {os.getpid()}")
                # 检查锁是否超时
                if self._checkLockTimeout():
                    continue  # 锁已释放，重新尝试获取
                else:
                    time.sleep(0.1)  # 等待一段时间后重试
                    continue
                    
            except Exception:
                # 其他错误，短暂等待后重试
                time.sleep(0.05)
                continue
    
    def _checkLockTimeout(self) -> bool:
        """检查锁是否超时，如果超时则强制释放
        Returns:
            bool: True表示锁已释放，False表示锁仍有效
        """
        try:
            if not self.lock_file.exists():
                return True
            
            # 读取锁文件中的时间戳
            with open(self.lock_file, 'r') as f:
                lock_time_str = f.read().strip()
                if not lock_time_str:
                    # 空文件，强制删除
                    self._forceReleaseLock()
                    return True
                    
                lock_time = float(lock_time_str)
                current_time = time.time()
                
                if current_time - lock_time > self.lock_timeout:
                    print(f"[鼠标锁] 检测到锁超时（{self.lock_timeout}秒），强制释放 - 进程ID: {os.getpid()}")
                    self._forceReleaseLock()
                    return True
                    
            return False
            
        except Exception:
            # 读取失败，可能文件损坏，强制释放
            self._forceReleaseLock()
            return True
    
    def _forceReleaseLock(self):
        """强制释放锁文件"""
        try:
            if self.lock_file.exists():
                # 尝试删除锁文件
                os.remove(str(self.lock_file))
                print(f"[鼠标锁] 强制释放锁文件成功 - 进程ID: {os.getpid()}")
        except Exception:
            pass  # 删除失败也没关系，可能已被其他进程删除
    
    def _releaseMouseLock(self) -> None:
        """释放鼠标锁"""
        try:
            if self.lock_file_handle:
                self.lock_file_handle.close()
                self.lock_file_handle = None
        except Exception:
            pass  # 关闭失败不影响程序运行
        
        # 删除锁文件
        try:
            if self.lock_file.exists():
                os.remove(str(self.lock_file))
                print(f"[鼠标锁] 释放锁成功 - 进程ID: {os.getpid()}")
        except Exception:
            pass  # 删除失败不影响程序运行
    
    def getVirtualKeyCode(self, key: str) -> int:
        """获取按键的虚拟键码"""
        key = key.upper()
        return self.kVirtualKeyCode.get(key, 0)
    
    def pressKey(self, key: Union[str, int], hwnd) -> bool:
        """按下并释放一个键
        Args:
            key: 按键（字符串或虚拟键码）
            hwnd: 目标窗口句柄
        """
        try:
            # 获取虚拟键码
            if isinstance(key, str):
                vk_code = self.getVirtualKeyCode(key)
                if vk_code == 0:
                    print(f"未知按键: {key}")
                    return False
            else:
                vk_code = key
            try:
                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 0)
                time.sleep(random.uniform(0.08, 0.12))  # 增加按键持续时间，更真实
                win32api.PostMessage(hwnd, win32con.WM_KEYUP, vk_code, 0)
                return True
            except Exception as e:
                print(f"异步发送失败: {e}")
                return False     
        except Exception as e:
            print(f"按键失败: {e}")
            return False
    
    def mouseClick(self, x: int, y: int, hwnd: int = 0, button: str = 'left') -> bool:
        """全局鼠标点击 - 使用SetCursorPos和mouse_event模拟真实鼠标
        Args:
            x: 相对于窗口原点的X坐标
            y: 相对于窗口原点的Y坐标  
            hwnd: 目标窗口句柄
            button: 点击类型 ('left', 'right', 'middle')
        Returns:
            bool: 是否成功
        """
        # 获取鼠标锁（一直等待直到获取成功）
        self._getMouseLock()
        
        try:
            return self._mouceClick(x, y, hwnd, button)
        finally:
            # 确保锁总是被释放
            self._releaseMouseLock()
    
    def _mouceClick(self, x: int, y: int, hwnd: int = 0, button: str = 'left') -> bool:
        """执行鼠标点击的具体逻辑"""
        try:
            if hwnd <= 0:
                return False
            
            # 获取窗口矩形 && 获取原点坐标 && 计算窗口宽度
            window_rect = win32gui.GetWindowRect(hwnd) # 返回窗口矩形左上角坐标和右下角坐标（像素）
            window_origin_x, window_origin_y = window_rect[0], window_rect[1]
            window_width = window_rect[2] - window_rect[0]
            
            # 先点击标题栏以确保窗口获得焦点
            title_bar_x = window_origin_x + window_width // 2  # 标题栏中央位置
            title_bar_y = window_origin_y + 15  # 标题栏通常在顶部15像素左右
            
            # 移动鼠标到标题栏并点击
            win32api.SetCursorPos((title_bar_x, title_bar_y))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)  # 减少单次点击持续时间
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.3)  # 减少等待窗口焦点时间，但保持足够安全
            
            # 计算目标位置在屏幕坐标系中的坐标
            target_screen_x = window_origin_x + x
            target_screen_y = window_origin_y + y
            
            # 移动鼠标到目标位置（瞬间完成）
            win32api.SetCursorPos((target_screen_x, target_screen_y))
            
            # 根据按钮类型选择mouse_event标志
            if button.lower() == 'left':
                down_flag = win32con.MOUSEEVENTF_LEFTDOWN
                up_flag = win32con.MOUSEEVENTF_LEFTUP
            elif button.lower() == 'right':
                down_flag = win32con.MOUSEEVENTF_RIGHTDOWN
                up_flag = win32con.MOUSEEVENTF_RIGHTUP
            elif button.lower() == 'middle':
                down_flag = win32con.MOUSEEVENTF_MIDDLEDOWN
                up_flag = win32con.MOUSEEVENTF_MIDDLEUP
            else:
                return False
            
            # 执行鼠标点击
            win32api.mouse_event(down_flag, 0, 0, 0, 0)
            time.sleep(0.1)  # 减少单次点击持续时间
            win32api.mouse_event(up_flag, 0, 0, 0, 0)
            
            return True
            
        except Exception as e:
            return False
    
    def mouseDoubleClick(self, x: int, y: int, hwnd: int = 0, button: str = 'left') -> bool:
        """全局鼠标双击 - 使用SetCursorPos和mouse_event模拟真实鼠标
        Args:
            x: 相对于窗口原点的X坐标
            y: 相对于窗口原点的Y坐标  
            hwnd: 目标窗口句柄
            button: 点击类型 ('left', 'right', 'middle')
        Returns:
            bool: 是否成功
        """
        # 获取鼠标锁（一直等待直到获取成功）
        self._getMouseLock()
        
        try:
            return self._mouseDoubleClick(x, y, hwnd, button)
        finally:
            # 确保锁总是被释放
            self._releaseMouseLock()
    
    def _mouseDoubleClick(self, x: int, y: int, hwnd: int = 0, button: str = 'left') -> bool:
        """执行鼠标双击的具体逻辑"""
        try:
            if hwnd <= 0:
                return False
            
            # 获取窗口矩形 && 获取原点坐标 && 计算窗口宽度
            window_rect = win32gui.GetWindowRect(hwnd) # 返回窗口矩形左上角坐标和右下角坐标（像素）
            window_origin_x, window_origin_y = window_rect[0], window_rect[1]
            window_width = window_rect[2] - window_rect[0]
            
            # 先点击标题栏以确保窗口获得焦点
            title_bar_x = window_origin_x + window_width // 2  # 标题栏中央位置
            title_bar_y = window_origin_y + 15  # 标题栏通常在顶部15像素左右
            
            # 移动鼠标到标题栏并点击
            win32api.SetCursorPos((title_bar_x, title_bar_y))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)  # 减少单次点击持续时间
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.3)  # 减少等待窗口焦点时间
            
            # 计算目标位置在屏幕坐标系中的坐标
            target_screen_x = window_origin_x + x
            target_screen_y = window_origin_y + y
            
            # 移动鼠标到目标位置（瞬间完成）
            win32api.SetCursorPos((target_screen_x, target_screen_y))
            
            # 根据按钮类型选择mouse_event标志
            if button.lower() == 'left':
                down_flag = win32con.MOUSEEVENTF_LEFTDOWN
                up_flag = win32con.MOUSEEVENTF_LEFTUP
            elif button.lower() == 'right':
                down_flag = win32con.MOUSEEVENTF_RIGHTDOWN
                up_flag = win32con.MOUSEEVENTF_RIGHTUP
            elif button.lower() == 'middle':
                down_flag = win32con.MOUSEEVENTF_MIDDLEDOWN
                up_flag = win32con.MOUSEEVENTF_MIDDLEUP
            else:
                return False
            
            # 执行第一次点击
            win32api.mouse_event(down_flag, 0, 0, 0, 0)
            time.sleep(0.1) # 20ms
            win32api.mouse_event(up_flag, 0, 0, 0, 0)
            
            # 双击间隔时间（较短，模拟真实双击）
            time.sleep(0.18)  # 缩短双击间隔，更真实
            
            # 执行第二次点击
            win32api.mouse_event(down_flag, 0, 0, 0, 0)
            time.sleep(0.1) # 20ms
            win32api.mouse_event(up_flag, 0, 0, 0, 0)
            
            return True
            
        except Exception as e:
            return False

    def typeChar(self, char: str, hwnd) -> bool:
        """输入字符 - 使用WM_CHAR消息
        Args:
            char: 要输入的字符
            hwnd: 目标窗口句柄
        """
        try:
            if len(char) != 1:
                print(f"typeChar只能输入单个字符，收到: {char}")
                return False
            
            # 获取字符的ASCII码
            char_code = ord(char)
            
            # 发送WM_CHAR消息
            win32api.PostMessage(hwnd, win32con.WM_CHAR, char_code, 0)
            time.sleep(random.uniform(0.05, 0.08))  # 短暂延迟
            return True
            
        except Exception as e:
            print(f"字符输入失败: {e}")
            return False

# 使用示例
if __name__ == "__main__":
    # 测试全局鼠标点击方法
    from window_manager import WindowManager
    window1 = WindowManager()
    hwnd1 = window1.selectWindow()
    if hwnd1 is None:
        print("未选择窗口")
        exit()
    # 打印窗口的size
    print(f"窗口的size: {window1.getWindowRect(hwnd1)}")
    ks = KeyboardSimulator()
    test_x, test_y = 50, 50
    
    print("测试全局鼠标点击方法...")
    print("=" * 50)
    
    while True:
        print("执行鼠标点击测试...")
        if ks.mouseClick(test_x, test_y, hwnd1, 'left'):
            print("   ✓ 鼠标点击成功")
        else:
            print("   ✗ 鼠标点击失败")
        
        print("=" * 50)
        time.sleep(2)