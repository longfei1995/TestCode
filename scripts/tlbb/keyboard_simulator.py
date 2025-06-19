import win32api
import win32con
import win32gui
import time
import random
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
    
    def pressKey(self, key: Union[str, int], hwnd: int = 0) -> bool:
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
                time.sleep(random.uniform(0.05, 0.08))  # 异步模式延迟更短
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
        try:
            if hwnd <= 0:
                return False
            
            # 获取窗口矩形 && 获取原点坐标 && 获取当前鼠标位置
            window_rect = win32gui.GetWindowRect(hwnd) # 返回窗口矩形左上角坐标和右下角坐标（像素）
            window_origin_x, window_origin_y = window_rect[0], window_rect[1]
            
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
            time.sleep(random.uniform(0.03, 0.08))  # 减少点击间隔
            win32api.mouse_event(up_flag, 0, 0, 0, 0)
            
            return True
            
        except Exception as e:
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