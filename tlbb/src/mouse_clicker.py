import time

from keyboard_simulator import KeyboardSimulator


class MouseClicker:
    """鼠标连点器"""

    def __init__(self, button: str, interval_ms: int, screen_x: int, screen_y: int):
        self.button = button
        self.interval_ms = max(1, interval_ms)
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.running = True
        self.keyboard_simulator = KeyboardSimulator()

    def run(self):
        """执行鼠标连点主循环"""
        click_count = 0
        button_name = "左键" if self.button == "left" else "右键"

        print("***************** 鼠标连点脚本开始启动 *****************")
        print(f"点击类型: {button_name}")
        print(f"点击间隔: {self.interval_ms} ms")
        print(f"点击坐标: ({self.screen_x}, {self.screen_y})")

        while self.running:
            click_count += 1
            success = self.keyboard_simulator.mouseClickScreenPos(
                self.screen_x,
                self.screen_y,
                self.button
            )
            if not success:
                print("鼠标连点本次执行失败，继续重试")
                self._sleepWithStopCheck(self.interval_ms / 1000.0)
                continue

            if click_count % 100 == 0:
                print(f"鼠标连点已执行 {click_count} 次")

            self._sleepWithStopCheck(self.interval_ms / 1000.0)

        print(f"鼠标连点已停止，共执行 {click_count} 次")

    def stop(self):
        """停止鼠标连点"""
        self.running = False

    def _sleepWithStopCheck(self, wait_seconds: float):
        """分段休眠，保证收到停止信号后可以尽快退出"""
        remaining = max(0.0, wait_seconds)
        while self.running and remaining > 0:
            sleep_step = min(0.01, remaining)
            time.sleep(sleep_step)
            remaining -= sleep_step
