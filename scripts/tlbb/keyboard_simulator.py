import win32api
import win32con
import win32gui
import time
from typing import Union, List

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
        
        # 其他常用键
        'CAPSLOCK': 0x14, 'NUMLOCK': 0x90, 'SCROLLLOCK': 0x91,
        'PAUSE': 0x13, 'PRINTSCREEN': 0x2C,
    }
    
    def __init__(self):
        pass
    
    def getVirtualKeyCode(self, key: str) -> int:
        """获取按键的虚拟键码"""
        key = key.upper()
        return self.kVirtualKeyCode.get(key, 0)
    
    def pressKey(self, key: Union[str, int], hwnd: int = 0, mode: str = "async") -> bool:
        """按下并释放一个键
        Args:
            key: 按键（字符串或虚拟键码）
            hwnd: 目标窗口句柄
            mode: 发送模式
                - "sync": 同步模式，使用SendMessage（默认，可靠）
                - "async": 异步模式，使用PostMessage（快速，适合游戏后台）
                - "global": 全局按键模式，使用keybd_event
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
                
            # 根据模式发送按键
            if mode == "sync":
                return self._sendKeySync(key, vk_code, hwnd)
            elif mode == "async":
                return self._sendKeyAsync(key, vk_code, hwnd)
            elif mode == "global":
                return self._sendKeyGlobal(key, vk_code)
            else:
                print(f"未知模式: {mode}")
                return False
                
        except Exception as e:
            print(f"按键失败: {e}")
            return False
    
    def _sendKeySync(self, key: Union[str, int], vk_code: int, hwnd: int) -> bool:
        """同步发送按键（SendMessage）"""
        try:
            # 对于单个字母和数字字符，直接发送字符消息
            if isinstance(key, str) and len(key) == 1 and key.isalnum():
                char_code = ord(key.upper())
                win32gui.SendMessage(hwnd, win32con.WM_CHAR, char_code, 0)
            elif isinstance(key, str) and key.upper() == 'SPACE':
                # 特殊处理空格
                win32gui.SendMessage(hwnd, win32con.WM_CHAR, ord(' '), 0)
            else:
                # 对于特殊键（功能键等），发送完整的按键序列
                win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 0)
                time.sleep(0.01)
                win32gui.SendMessage(hwnd, win32con.WM_KEYUP, vk_code, 0)
            return True
        except Exception as e:
            print(f"同步发送失败: {e}")
            return False
    
    def _sendKeyAsync(self, key: Union[str, int], vk_code: int, hwnd: int) -> bool:
        """异步发送按键（PostMessage）"""
        try:
            # 对于单个字母和数字字符，直接发送字符消息
            if isinstance(key, str) and len(key) == 1 and key.isalnum():
                char_code = ord(key.upper())
                win32api.PostMessage(hwnd, win32con.WM_CHAR, char_code, 0)
            elif isinstance(key, str) and key.upper() == 'SPACE':
                # 特殊处理空格
                win32api.PostMessage(hwnd, win32con.WM_CHAR, ord(' '), 0)
            else:
                # 对于特殊键（功能键等），发送完整的按键序列
                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 0)
                time.sleep(0.005)  # 异步模式延迟更短
                win32api.PostMessage(hwnd, win32con.WM_KEYUP, vk_code, 0)
            return True
        except Exception as e:
            print(f"异步发送失败: {e}")
            return False
    
    def _sendKeyGlobal(self, key: Union[str, int], vk_code: int) -> bool:
        """全局发送按键（keybd_event）"""
        try:
            win32api.keybd_event(vk_code, 0, 0, 0)  # 按下
            time.sleep(0.02)
            win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放
            return True
        except Exception as e:
            print(f"全局按键失败: {e}")
            return False
    
    def pressKeys(self, keys: str, hwnd: int = 0, delay: float = 0.05, mode: str = "async") -> bool:
        """发送一串按键
        Args:
            keys: 要发送的字符串
            hwnd: 目标窗口句柄
            delay: 按键间延迟（秒）
            mode: 发送模式（sync/async/global）
        """
        try:
            for char in keys:
                if char == ' ':
                    self.pressKey('SPACE', hwnd, mode)
                elif char.isalnum():
                    self.pressKey(char, hwnd, mode)
                else:
                    print(f"跳过特殊字符: {char}")
                
                if delay > 0:
                    time.sleep(delay)
            
            return True
        except Exception as e:
            print(f"发送按键序列失败: {e}")
            return False

# 使用示例
if __name__ == "__main__":
    from window_manager import WindowManager
    
    print("=== 键盘模拟器测试 ===")
    window1 = WindowManager()
    hwnd1 = window1.selectWindow()
    if hwnd1 is None:
        print("未选择窗口")
        exit()
    ks = KeyboardSimulator()
    ks.pressKeys('Hello World', hwnd1, delay=0.05, mode='global')
    # ks.pressKeys('Hello World', hwnd1, delay=0.05, mode='async')
    # ks.pressKeys('Hello World', hwnd1, delay=0.05, mode='sync')
    