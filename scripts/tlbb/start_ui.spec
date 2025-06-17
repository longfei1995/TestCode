# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['start_ui.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 包含pics目录（如果存在图片资源）
        ('pics', 'pics'),
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
        # 其他可能需要的模块
        'numpy',
        'typing',
        'dataclasses',
        'datetime',
        'io',
        'time',
        'random',
        'ctypes',
        # 项目内部模块
        'game_param',
        'window_manager',
        'color_detector', 
        'keyboard_simulator',
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

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='tlbb_auto_raid_tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为False以创建Windows GUI应用
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # 添加图标（如果有的话）
    # icon='icon.ico',
) 