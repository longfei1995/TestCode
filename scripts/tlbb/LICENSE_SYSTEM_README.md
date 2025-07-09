# 天龙八部助手 - 许可证系统说明

## 🔐 系统概述

本软件采用**许可证密钥 + 硬件绑定**的授权方案，确保软件的合法使用。

### 主要特点

- ✅ **安全可靠**：基于 HMAC-SHA256 加密算法
- ✅ **硬件绑定**：许可证与设备硬件信息绑定，无法转移
- ✅ **离线验证**：无需联网即可验证许可证
- ✅ **防篡改**：许可证文件经过加密保护

## 📋 用户使用流程

### 1. 首次启动
程序启动时会自动检查授权状态：
- 如果有有效许可证 → 直接进入主程序
- 如果未授权 → 显示激活对话框

### 2. 激活方式

#### 使用许可证密钥
1. 联系软件作者获取许可证密钥
2. 在激活对话框中输入许可证密钥
3. 点击"激活"完成授权

### 3. 许可证购买流程
1. 运行软件，在激活对话框中复制"设备ID"
2. 联系软件作者，提供设备ID
3. 购买后获得专属许可证密钥
4. 输入许可证密钥完成激活

## 🛠️ 管理员工具

### 许可证生成工具
位置：`license_generator.py`

**功能：**
- 查看当前设备硬件ID
- 为指定设备生成许可证
- 测试和验证许可证
- 设置许可证有效期

**使用方法：**
```bash
python license_generator.py
```

### 生成许可证步骤
1. 获取用户的设备ID
2. 在工具中输入设备ID和用户信息
3. 设置有效期（天数或具体日期）
4. 点击"生成许可证"
5. 复制生成的许可证密钥发送给用户

## 🔧 技术细节

### 硬件指纹算法
基于以下硬件信息生成唯一ID：
- CPU信息
- 主板序列号
- MAC地址
- 硬盘序列号
- 计算机名

### 文件说明
- `license.dat` - 存储用户许可证信息（加密）

### 安全机制
1. **HMAC签名**：防止许可证被伪造
2. **硬件绑定**：防止许可证被复制到其他电脑
3. **时间验证**：自动检查许可证是否过期
4. **文件保护**：敏感信息经过Base64编码和加密

## ⚙️ 配置选项

### 修改加密密钥
在 `license_manager.py` 中修改：
```python
def __init__(self, secret_key: str = "您的专属密钥"):
```

**⚠️ 注意：修改密钥后，之前生成的所有许可证将失效**

## 🚀 集成到现有项目

### 1. 添加许可证检查
在主程序的 `main()` 函数中添加：
```python
from license_dialog import LicenseDialog

# 检查授权状态
is_authorized = LicenseDialog.checkAndShowLicense()
if not is_authorized:
    sys.exit(0)  # 未授权则退出

# 继续执行主程序
window = YourMainWindow()
window.show()
```

### 2. 运行时检查（可选）
在关键功能中添加授权检查：
```python
from license_manager import LicenseManager

def important_function():
    lm = LicenseManager()
    is_authorized, message = lm.is_authorized()
    if not is_authorized:
        QMessageBox.warning(None, "授权失败", message)
        return
    
    # 继续执行功能
```

## 📦 打包配置

在 `pkg_ui.spec` 文件中确保包含许可证模块：
```python
hiddenimports=[
    # ... 其他模块
    'license_manager',
    'license_dialog',
],
```

## 🔍 故障排除

### 常见问题

**Q: 许可证提示"与当前设备不匹配"**
A: 硬件信息发生变化，需要重新生成许可证

**Q: 许可证密钥格式错误**
A: 检查密钥是否完整，注意不要有多余的空格或换行

**Q: 程序启动时提示"许可证检查模块未找到"**
A: 确保 `license_manager.py` 和 `license_dialog.py` 文件存在

### 重置许可证（仅开发测试）
删除以下文件可重置许可证：
```bash
del license.dat
```

## 📞 技术支持

如有问题，请联系软件作者并提供：
1. 错误截图
2. 设备硬件ID
3. 详细的错误描述

---

**免责声明**：本许可证系统仅用于软件保护，请根据实际需求调整安全级别。 