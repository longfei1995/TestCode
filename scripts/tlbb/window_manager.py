import win32gui
import win32con
import win32api
import ctypes
import os
import sys
from typing import List, Tuple, Optional
from game_param import Bbox, kBaseDir
from PIL import ImageGrab
from datetime import datetime
import glob

class WindowManager:
    """Windows窗口管理器"""
    
    def __init__(self):
        self.windows = []
        self.pic_save_dir = os.path.join(kBaseDir, "pics")
    
    def isAdmin(self) -> bool:
        """检查当前程序是否以管理员权限运行"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def getAllWindows(self) -> List[Tuple[int, str]]:
        """获取所有可见窗口的句柄和标题"""
        self.windows = []
        
        def enum_windows_callback(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                self.windows.append((hwnd, window_title))
            return True
        
        win32gui.EnumWindows(enum_windows_callback, 0)
        return self.windows
    
    def activateWindow(self, hwnd: int) -> bool:
        """激活指定窗口"""
        try:
            # 首先检查窗口句柄是否有效
            if not win32gui.IsWindow(hwnd):
                print("窗口句柄无效")
                return False
            
            # 检查窗口是否仍然存在
            try:
                window_title = win32gui.GetWindowText(hwnd)
                if not window_title:
                    print("窗口可能已关闭或无标题")
            except:
                print("无法获取窗口标题，窗口可能已关闭")
                return False
            
            # 如果窗口最小化，先恢复
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            
            # 尝试多种方法激活窗口（优先后台方式）
            success = False
            
            # 方法1: 使用ShowWindow显示窗口（后台激活，不抢夺焦点）
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                success = True
                print("使用ShowWindow成功显示窗口（后台激活）")
            except Exception as e1:
                print(f"ShowWindow失败: {e1}")
                
                # 方法2: 尝试发送激活消息（温和激活）
                try:
                    win32gui.PostMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
                    success = True
                    print("使用PostMessage成功发送激活消息（温和激活）")
                except Exception as e2:
                    print(f"PostMessage失败: {e2}")
                    
                    # 方法3: 直接设置前台窗口（强制激活，最后尝试）
                    try:
                        win32gui.SetForegroundWindow(hwnd)
                        success = True
                        print("使用SetForegroundWindow成功激活窗口（强制前台）")
                    except Exception as e3:
                        print(f"SetForegroundWindow失败: {e3}")
            
            # 尝试设置活动窗口（可能需要前台窗口权限）
            try:
                if success:
                    win32gui.SetActiveWindow(hwnd)
            except Exception as e:
                print(f"SetActiveWindow失败 (可忽略): {e}")
            
            return success
            
        except Exception as e:
            print(f"激活窗口发生未知错误: {e}")
            return False
    
    def getWindowRect(self, hwnd: int) -> Tuple[int, int, int, int]:
        """获取窗口位置和大小 (left, top, right, bottom)"""
        return win32gui.GetWindowRect(hwnd)
    
    def selectWindow(self) -> Optional[int]:
        """交互式选择窗口
        Returns:
            Optional[int]: 选中的窗口句柄, 如果取消则返回 None
        """
        # 显示权限状态
        if self.isAdmin():
            print("✓ 当前程序以管理员权限运行")
        else:
            print("⚠ 当前程序以普通用户权限运行，可能无法激活某些需要管理员权限的窗口")
        
        windows = self.getAllWindows()
        
        if not windows:
            print("未找到任何窗口")
            return None
        
        print(f"\n找到 {len(windows)} 个窗口:")
        print("-" * 80)
        
        # 显示窗口列表
        for i, (hwnd, title) in enumerate(windows, 1):
            print(f"{i:3d}. [{hwnd:8d}] {title}")
        
        print("-" * 80)
        
        # 让用户选择
        while True:
            try:
                choice = input(f"请输入要激活的窗口序号 (1-{len(windows)}, 0=取消): ").strip()
                
                if choice == '0':
                    print("已取消选择")
                    return None
                
                index = int(choice) - 1
                
                if 0 <= index < len(windows):
                    selected_hwnd, selected_title = windows[index]
                    print(f"您选择了: {selected_title} (句柄: {selected_hwnd})")
                    if self.activateWindow(selected_hwnd):
                        print(f"成功激活窗口: {selected_title}")
                        return selected_hwnd
                    else:
                        print(f"激活窗口失败: {selected_title}")
                        print("提示: 如果是权限问题，请尝试以管理员身份运行此程序")
                        return None
                else:
                    print(f"无效的序号，请输入 1-{len(windows)} 之间的数字")
                    
            except ValueError:
                print("请输入有效的数字")
            except KeyboardInterrupt:
                print("\n已取消选择")
                return None
            except Exception as e:
                print(f"发生错误: {e}")
                return None

    def saveBboxImage(self, hwnd:int, bbox:Bbox):
        """保存指定窗口的指定区域截图"""
        # 确保保存目录存在
        if not os.path.exists(self.pic_save_dir):
            os.makedirs(self.pic_save_dir)
        
        # 检查并清理目录中的PNG文件
        png_files = glob.glob(os.path.join(self.pic_save_dir, "*.png"))
        if len(png_files) >= 100:
            # 按文件创建时间排序
            png_files.sort(key=os.path.getctime)
            # 删除最老的50张文件
            files_to_delete = png_files[:50]
            for old_file in files_to_delete:
                try:
                    os.remove(old_file)
                except Exception as e:
                    pass
        
        window_rect = self.getWindowRect(hwnd)
        left = window_rect[0] + bbox.left
        top = window_rect[1] + bbox.top
        right = window_rect[0] + bbox.right
        bottom = window_rect[1] + bbox.bottom
        
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        screenshot.save(os.path.join(self.pic_save_dir, f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"))
        return screenshot

# 使用示例
if __name__ == "__main__":
    wm = WindowManager()
    # wm.list_windows()
    hwnd = wm.selectWindow()
    if hwnd is None:
        print("未选择窗口")
        exit()
    window_rect = wm.getWindowRect(hwnd)
    window_width = window_rect[2] - window_rect[0]
    window_height = window_rect[3] - window_rect[1]
    bbox = Bbox(0, 0, window_width, window_height)
    wm.saveBboxImage(hwnd, bbox)
    