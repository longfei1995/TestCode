# 豆子 - 天龙八部自动化助手 · Copilot Instructions

## 项目概述

本项目是一款专为《天龙八部》游戏设计的 Windows 自动化助手工具，使用 Python + PyQt5 构建。核心功能包括：循环自动按键（RAID 模式）、自动挖昆吾种子、死亡后自动回点、定时关机，以及基于硬件指纹的许可证授权系统。

---

## 技术栈

| 库 | 用途 |
|---|---|
| `PyQt5` | GUI 界面（主窗口、对话框、样式表） |
| `pywin32` (win32gui / win32con / win32api) | Windows 窗口管理、消息发送、键鼠模拟 |
| `pyautogui` | 图像识别（基于模板匹配） |
| `Pillow` / `opencv-python` / `numpy` | 图像处理与像素分析 |
| `PyInstaller` | 应用打包（配置见 `pkg_ui.spec`） |

运行环境：**Windows only**，需管理员权限以确保窗口激活和系统操作正常。

---

## 模块职责

### `start_ui.py` — 主程序入口 & UI 层
- `GameUI(QMainWindow)`：主窗口，含 6 个选项卡（按键配置、自动按键、挖种子、自动回点、系统管理、版本历史）。
- `RaidThread(QThread)`：执行循环按键序列，支持峨眉智能治疗逻辑（两级优先级：紧急治疗 → 预防性治疗）。
- `DigSeedThread(QThread)`：调用 `DigSeed` 完成挖种子流程。
- `AutoReturnThread(QThread)`：调用 `AutoReturn` 完成回点流程。
- `UILogStream`：将 `print()` 输出重定向到 UI 日志面板，带时间戳。
- 所有后台线程通过 `stop_flag` 标志位安全停止，通过 `pyqtSignal` 向主线程发送日志。

### `keyboard_simulator.py` — 键鼠模拟
- `KeyboardSimulator`：使用 `WM_KEYDOWN/UP` 消息向游戏窗口发送按键，使用 `WM_CHAR` 输入字符。
- **鼠标锁机制**：通过独占文件创建（`open(path, 'x')`）实现跨进程原子锁，防止多实例并发点击冲突，超时 10 秒后强制释放。
- `mouseClick(x, y, hwnd, button)`：点击前先激活标题栏，再获取锁后执行点击，`finally` 确保释放锁。

### `window_manager.py` — 窗口管理
- `WindowManager`：枚举所有可见窗口、激活指定窗口（三层降级策略）、获取窗口矩形、截图并保存（超过 100 张时自动清理旧截图）。

### `img_match.py` — 图像识别
- `ImageMatch`：调用 `pyautogui.locateOnScreen` 在窗口区域内匹配模板图片。
- 默认置信度 `0.8`，内置重试机制（最多 3 次，间隔 0.5 秒）。
- 返回相对于窗口的坐标，匹配结果自动截图保存用于调试。

### `color_detector.py` — 颜色检测
- `ColorDetector`：获取窗口内指定坐标的像素 RGB 值，用于判断血条（红色）和蓝条（空/非空）状态。

### `dig_seed.py` — 挖种子逻辑
- `DigSeed`：完整的昆吾种子任务流程（上马 → 接任务 → 挖种子或打怪 → 提交任务）。
- `isPersonStop()`：连续截取 3 帧计算平均像素差异，差异低于阈值则判定人物已停止移动。
- 支持外部 `stop_check_func` 回调以响应 UI 中断请求。

### `auto_return.py` — 自动回点
- `AutoReturn`：支持三种场景（雪原、四象天门阵、苗人洞），处理地府逃脱→传送→局部寻路→召唤宠物的完整流程。
- `_isInHell()` 等场景判断方法用于分支控制。

### `game_param.py` — 全局参数
- 定义血条/蓝条坐标（6 人队伍）、头像坐标、默认按键映射（`kDefaultKey`）、图片路径（`ImagePath`）。
- `getBasePath()` 兼容开发环境和 PyInstaller 打包后的路径（`sys._MEIPASS`）。

### `license_manager.py` — 许可证系统
- 硬件指纹：收集 CPU 型号、主板序列、MAC 地址、硬盘序列、计算机名，SHA256 哈希后取前 16 位。
- 许可证格式：`Base64(JSON数据 + "|" + HMAC-SHA256签名)`，每 4 字符用 `-` 分隔。
- 密钥：`"hyh_2025"`（HMAC 签名用）。
- 持久化：保存为 `license.dat`（内容为 Base64 编码）。

### `license_dialog.py` — 激活对话框
- `LicenseDialog(QDialog)`：显示硬件 ID（可复制）、许可证输入框、状态显示。
- `checkAndShowLicense(parent)`：启动时检查授权状态，未授权则弹出对话框。

### `license_generator.py` — 许可证生成工具
- 独立的 `LicenseGeneratorUI(QMainWindow)`，供作者生成、测试、验证许可证。

### `sys_manager.py` — 系统管理
- `shutdownPC(hours)`：执行 `shutdown /s /t {seconds}`。
- `cancelShutdown()`：执行 `shutdown /a`。

---

## 架构约定

### 线程安全
- **UI 更新必须在主线程**：后台线程通过 `pyqtSignal(str)` 发送日志，由主线程的 slot 写入日志面板，不得直接操作 UI 组件。
- 停止线程时只设置 `self._stop = True` 标志位，不强制 kill 线程。

### 窗口操作顺序
1. 通过 `window_manager.py` 获取游戏窗口 `hwnd`。
2. 所有坐标以**窗口客户区左上角为原点**（相对坐标），不使用绝对屏幕坐标。
3. 鼠标操作前必须获取鼠标锁，用 `try-finally` 确保释放。

### 图像资源
- 所有模板图片存放在 `img_src/` 下，路径通过 `game_param.ImagePath` 统一管理。
- `auto_return/` — 自动回点相关 UI 截图。
- `kun_wu/` — 挖种子相关 UI 截图。

### 路径兼容性
- **始终使用 `game_param.kBaseDir` 或 `game_param.kPicDir`** 构建文件路径，确保打包后路径正确，不得硬编码绝对路径。

### 错误处理
- 图像识别失败时记录日志并重试，超过最大重试次数后抛出异常或通过回调通知上层。
- 硬件信息获取失败时捕获异常并使用空字符串替代，保证硬件 ID 生成不崩溃。

---

## 代码风格

- **命名**：类名使用 `PascalCase`，方法和变量使用 `camelCase`，常量使用 `kCamelCase`（如 `kDefaultKey`、`kHPBar`）。
- **注释**：关键流程步骤用中文注释说明，便于维护。
- **日志**：通过 `print()` 输出运行信息，由 `UILogStream` 自动捕获到 UI 日志面板，格式为 `[HH:MM:SS] 消息内容`。
- **延迟**：使用 `time.sleep()` 实现步骤间等待，等待时间写为常量或有注释说明原因。

---

## 打包

```bash
# 使用 pkg_ui.spec 打包（含图片资源和样式表）
pyinstaller pkg_ui.spec
```

打包配置在 `pkg_ui.spec` 中，`datas` 字段包含 `img_src/` 和 `styles.qss`。详见 `how_to_package.txt`。

---

## 注意事项

1. 该项目**仅支持 Windows**，不应引入跨平台假设。
2. 游戏坐标（血条位置、头像位置等）均为固定值，修改时须同步更新 `game_param.py`。
3. 许可证密钥 `"hyh_2025"` 不得泄露或提交到公开仓库。
4. 新增自动化任务时，参照 `DigSeed` 和 `AutoReturn` 的模式：在独立模块中实现逻辑，在 `start_ui.py` 中创建对应的 `QThread` 子类调用，通过信号回传日志。
