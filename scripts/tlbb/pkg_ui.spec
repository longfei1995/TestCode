# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['start_ui.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 包含图标文件到根目录
        ('icon.ico', '.'),
        # 包含样式文件到根目录
        ('styles.qss', '.'),
        # 包含版本历史文件到根目录
        ('version_history.txt', '.'),
        # 包含图片资源文件夹
        ('img_src', 'img_src'),
    ],
    hiddenimports=[
        # PyQt5相关模块
        'PyQt5.QtCore',
        'PyQt5.QtWidgets', 
        'PyQt5.QtGui',
        # Windows API相关模块
        'win32gui',
        'win32con',
        'win32api',
        'win32ui',
        # PIL/Pillow相关
        'PIL.Image',
        'PIL.ImageGrab',
        # OpenCV相关
        'cv2',
        'cv2.cv2',
        # 图像处理和自动化相关
        'pyautogui',
        'pyautogui._pyautogui_win',
        'pymsgbox',
        'pytweening',
        'pyscreeze',
        # 其他可能需要的模块
        'numpy',
        'typing',
        'dataclasses',
        'datetime',
        'io',
        'time',
        'random',
        'ctypes',
        'threading',
        'queue',
        'logging',
        # 项目内部模块
        'game_param',
        'window_manager',
        'color_detector', 
        'keyboard_simulator',
        'dig_seed',  # 新增的挖种子模块
        'img_match',  # 图像匹配模块
        'auto_return',  # 自动回点模块
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的模块以减小体积
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'IPython',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# onedir模式：分离exe和资源文件
exe = EXE(
    pyz,
    a.scripts,
    [],  # 不包含 a.binaries
    exclude_binaries=True,  # 关键：排除二进制文件，使其分离
    name='tlbb_assistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 设置为False以创建Windows GUI应用
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)

# 创建包含所有文件的目录
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='tlbb_assistant'
) 