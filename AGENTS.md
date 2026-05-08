# 项目级 Agent 指南（供 Codex 使用）

## 1. 项目概况

- 这是一个面向《天龙八部》的 Windows 自动化助手项目，技术栈以 `Python + PyQt5` 为主。
- 当前仓库的核心能力包括：自动按键、自动回点、系统关机管理，以及与这些能力相关的窗口激活、识图、颜色检测和键鼠模拟。
- 项目明显依赖 Windows API、真实桌面环境、屏幕截图和鼠标键盘事件，不是跨平台项目。
- 主程序入口是 `tlbb/src/start_ui.py`。
- 打包入口是 `tlbb/pkg_ui.spec`。

## 2. 先相信真实文件树，不要过度相信历史文档

- 当前仓库里存在 `.github/copilot-instructions.md`，可作为补充参考。
- 但如果历史文档与实际文件树冲突，以当前仓库中的真实文件为准。
- 例如：历史文档里提到过 `license_manager.py`、`license_dialog.py`、`license_generator.py`，但这些文件在当前仓库快照中并不存在，不要假定它们仍然是系统的一部分。

## 3. 目录与模块分工

- `requirements.txt`：项目依赖。
- `tlbb/src/start_ui.py`：主窗口、分页 UI、线程封装、日志展示，是项目主入口。
- `tlbb/src/game_param.py`：路径常量、坐标配置、默认按键、模板图路径。
- `tlbb/src/window_manager.py`：窗口枚举、激活、截图保存。
- `tlbb/src/keyboard_simulator.py`：按键发送、字符输入、鼠标点击与跨进程鼠标锁。
- `tlbb/src/img_match.py`：基于 `pyautogui.locateOnScreen` 的模板匹配。
- `tlbb/src/color_detector.py`：像素颜色检测，用于血条/蓝条等状态判断。
- `tlbb/src/auto_return.py`：自动回点流程。
- `tlbb/src/sys_manager.py`：定时关机与取消关机。
- `tlbb/res/`：样式、图标、版本记录、按键配置、模板图片资源。
- `tlbb/pkg_ui.spec`：PyInstaller 打包配置。

## 4. Codex 在这个仓库里的工作方式

- 先读现有实现，再动代码；优先沿用当前模式，不主动引入新框架。
- 变更尽量小而准，除非用户明确要求，否则不要顺手重构大段 UI 或重命名模块。
- `start_ui.py` 很大且承担中枢职责，改它时要控制范围，优先局部修改。
- 新增自动化能力时，优先遵循现有模式：
  1. 业务逻辑放到独立模块；
  2. 在 `start_ui.py` 中增加对应的 `QThread` 封装；
  3. 通过 `pyqtSignal` 回传日志和结束信号；
  4. 不要在工作线程里直接操作 Qt UI 组件。

## 5. 代码风格与约定

- 保持现有命名风格：
  - 类名使用 `PascalCase`
  - 方法和变量使用 `camelCase`
  - 全局常量/全局配置实例保持现有 `kCamelCase` 风格，例如 `kDefaultKey`
- 保持中文注释和中文运行日志风格，项目现有代码大量依赖这一习惯。
- 运行期日志优先继续使用 `print()`，因为 UI 已通过 `UILogStream` 捕获标准输出并显示到日志面板。
- 除非有明确收益，不要把现有日志体系整体替换为 `logging`。

## 6. 路径、坐标、资源的硬约束

- 所有运行时路径优先通过 `game_param.py` 中的 `getBasePath()`、`kBaseDir`、`kResDir`、`kPicDir`、`ImagePath` 获取。
- 不要硬编码开发机绝对路径。
- 大多数坐标都是相对目标游戏窗口的坐标，不要轻易改成绝对屏幕坐标。
- 修改识图模板时：
  - 资源放到 `tlbb/res/img_src/` 对应目录；
  - 同步更新 `game_param.py` 中的 `ImagePath`；
  - 如果是打包后也要用到的资源，确认 `tlbb/pkg_ui.spec` 的 `datas` 已覆盖。
- 修改固定血条、头像、按钮坐标时要格外谨慎，这类值通常与具体游戏 UI 布局和分辨率强绑定。

## 7. 线程与 UI 约束

- 后台任务必须通过 `QThread` 运行，避免阻塞 UI。
- 从工作线程回传信息时，优先使用已有的 `log_signal`、`finished_signal` 模式。
- 不要在工作线程中直接更新 Qt 控件。
- 停止线程时沿用当前的布尔标记位方案，不要尝试强杀线程。

## 8. 键鼠自动化与系统操作的安全边界

- 这个项目会操作真实桌面环境。任何会触发真实鼠标点击、键盘发送、窗口切换的验证动作，都应谨慎执行。
- `sys_manager.py` 会调用 `shutdown` 命令；除非用户明确要求，否则不要实际触发关机或取消关机动作来做“验证”。
- `keyboard_simulator.py`、`auto_return.py` 的运行可能干扰用户当前桌面，不要在未经说明的情况下直接长时间运行自动化流程。
- `tlbb/res/key_setting.yaml` 很可能承载用户本地按键配置。除非任务本身就是修改默认键位或配置持久化逻辑，否则不要随意覆盖它。

## 9. 编码与文本注意事项

- 仓库中包含中文注释、中文日志和中文资源文本。
- 在某些 PowerShell 编码页下，中文可能显示为乱码；遇到这种情况，先判断是终端显示问题还是文件本身编码损坏。
- 不要因为终端显示乱码就批量转换源码编码，除非已经确认文件真实编码有问题并且用户希望处理。

## 10. 运行、验证与打包命令

- 安装依赖：

```bash
pip install -r requirements.txt
```

- 启动主程序：

```bash
python tlbb/src/start_ui.py
```

- 做基础语法校验：

```bash
python -m compileall tlbb/src
```

- 打包：

```bash
cd tlbb
python -m PyInstaller --clean pkg_ui.spec
```

## 11. 验证策略

- 优先做静态验证和低风险验证，例如：
  - 语法检查
  - 导入检查
  - 打包配置检查
  - 资源路径检查
- 如果改动涉及识图、窗口激活、键鼠操作、回点流程，完整验证通常需要真实游戏窗口和桌面环境。
- 如果没有真实运行条件，要在最终说明里明确哪些内容已经验证，哪些只能做代码层判断。

## 12. 修改时的额外提醒

- 如果新增了运行时资源文件，记得检查 `tlbb/pkg_ui.spec` 是否需要补充 `datas`。
- 如果改动会影响用户可见功能，优先考虑是否同步更新 `tlbb/res/version_history.txt`。
- `tlbb/src/test.py` 当前只是一个极简示例文件，不要把它当成正式测试体系。
- 项目目前看不到成体系的自动化测试，不要假设存在 CI 兜底。

## 13. 给未来代理的简短决策原则

- 优先修具体问题，不做无关重构。
- 优先复用现有工具类，不平地起新抽象。
- 优先保持 Windows 桌面自动化项目的现实约束，而不是套用通用后端项目习惯。
- 对“会动真实鼠标、真实键盘、真实关机”的代码保持敬畏。
