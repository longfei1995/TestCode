[Setup]
; 应用基本信息
AppName=天龙八部助手
AppVersion=1.0.0
AppPublisher=Your Name
AppPublisherURL=https://your-website.com
AppSupportURL=https://your-website.com
AppUpdatesURL=https://your-website.com
DefaultDirName={autopf}\TLBB Assistant
DefaultGroupName=天龙八部助手
AllowNoIcons=yes
; 安装程序输出
OutputDir=dist\installer
OutputBaseFilename=tlbb_assistant_setup
; 压缩设置
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; 权限设置
PrivilegesRequired=admin

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; 包含 PyInstaller 生成的整个文件夹
Source: "dist\tlbb_assistant\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; 创建开始菜单快捷方式
Name: "{group}\天龙八部助手"; Filename: "{app}\tlbb_assistant.exe"
Name: "{group}\{cm:UninstallProgram,天龙八部助手}"; Filename: "{uninstallexe}"
; 创建桌面快捷方式（如果用户选择）
Name: "{autodesktop}\天龙八部助手"; Filename: "{app}\tlbb_assistant.exe"; Tasks: desktopicon

[Run]
; 安装完成后询问是否运行程序
Filename: "{app}\tlbb_assistant.exe"; Description: "{cm:LaunchProgram,天龙八部助手}"; Flags: nowait postinstall skipifsilent 