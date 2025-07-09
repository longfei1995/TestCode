"""
许可证管理模块
实现软件授权、硬件绑定等功能
"""
import hashlib
import hmac
import json
import os
import platform
import subprocess
import uuid
from datetime import datetime, timedelta
from typing import Optional, Tuple
import base64


class LicenseManager:
    """许可证管理器"""
    
    def __init__(self, secret_key: str = "hyh_2025"):
        """
        初始化许可证管理器
        
        Args:
            secret_key: 用于加密的密钥（请修改为您自己的密钥）
        """
        self.secret_key = secret_key.encode('utf-8')
        self.license_file = "license.dat"
    
    def get_hardware_id(self) -> str:
        """
        获取硬件指纹（基于多个硬件信息生成唯一ID）
        
        Returns:
            硬件指纹字符串
        """
        try:
            # 收集硬件信息
            info_parts = []
            
            # CPU 信息
            try:
                import cpuinfo
                cpu_info = cpuinfo.get_cpu_info()
                info_parts.append(cpu_info.get('brand_raw', ''))
            except:
                # 如果cpuinfo不可用，使用platform信息
                info_parts.append(platform.processor())
            
            # 主板序列号
            try:
                result = subprocess.run(['wmic', 'baseboard', 'get', 'serialnumber'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        info_parts.append(lines[1].strip())
            except:
                pass
            
            # MAC 地址
            try:
                mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                               for ele in range(0, 8*6, 8)][::-1])
                info_parts.append(mac)
            except:
                pass
            
            # 硬盘序列号
            try:
                result = subprocess.run(['wmic', 'diskdrive', 'get', 'serialnumber'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        info_parts.append(lines[1].strip())
            except:
                pass
            
            # 计算机名
            info_parts.append(platform.node())
            
            # 合并所有信息并生成哈希
            hardware_info = '|'.join(filter(None, info_parts))
            hardware_id = hashlib.sha256(hardware_info.encode('utf-8')).hexdigest()[:16]
            
            return hardware_id.upper()
            
        except Exception as e:
            print(f"获取硬件ID时出错: {e}")
            # 备用方案：使用MAC地址
            try:
                mac = hex(uuid.getnode())[2:].upper()
                return hashlib.sha256(mac.encode()).hexdigest()[:16].upper()
            except:
                return "UNKNOWN_HARDWARE"
    
    def generate_license_key(self, hardware_id: str, expiry_date: str, 
                           user_info: str = "Licensed User") -> str:
        """
        生成许可证密钥（管理员使用）
        
        Args:
            hardware_id: 硬件指纹
            expiry_date: 过期日期（格式：YYYY-MM-DD）
            user_info: 用户信息
            
        Returns:
            许可证密钥
        """
        try:
            # 创建许可证数据
            license_data = {
                "hardware_id": hardware_id,
                "expiry_date": expiry_date,
                "user_info": user_info,
                "issued_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 转换为JSON字符串
            json_str = json.dumps(license_data, separators=(',', ':'))
            
            # 使用HMAC签名
            signature = hmac.new(self.secret_key, json_str.encode('utf-8'), hashlib.sha256).hexdigest()
            
            # 组合数据和签名
            combined = f"{json_str}|{signature}"
            
            # Base64编码
            license_key = base64.b64encode(combined.encode('utf-8')).decode('utf-8')
            
            # 格式化为易读的密钥格式（每4个字符一组）
            formatted_key = '-'.join([license_key[i:i+4] for i in range(0, len(license_key), 4)])
            
            return formatted_key
            
        except Exception as e:
            print(f"生成许可证密钥时出错: {e}")
            return ""
    
    def validate_license_key(self, license_key: str) -> Tuple[bool, str]:
        """
        验证许可证密钥
        
        Args:
            license_key: 许可证密钥
            
        Returns:
            (是否有效, 错误信息)
        """
        try:
            # 移除格式化字符
            clean_key = license_key.replace('-', '').replace(' ', '')
            
            # Base64解码
            try:
                combined = base64.b64decode(clean_key.encode('utf-8')).decode('utf-8')
            except:
                return False, "许可证密钥格式错误"
            
            # 分离数据和签名
            if '|' not in combined:
                return False, "许可证密钥格式错误"
            
            json_str, signature = combined.rsplit('|', 1)
            
            # 验证签名
            expected_signature = hmac.new(self.secret_key, json_str.encode('utf-8'), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(signature, expected_signature):
                return False, "许可证密钥无效"
            
            # 解析许可证数据
            try:
                license_data = json.loads(json_str)
            except:
                return False, "许可证数据格式错误"
            
            # 验证硬件ID
            current_hardware_id = self.get_hardware_id()
            if license_data.get("hardware_id") != current_hardware_id:
                return False, f"许可证与当前设备不匹配\n当前设备ID: {current_hardware_id}"
            
            # 验证过期时间
            try:
                expiry_date = datetime.strptime(license_data.get("expiry_date", ""), "%Y-%m-%d")
                if datetime.now() > expiry_date:
                    return False, f"许可证已过期（过期时间：{license_data.get('expiry_date')}）"
            except:
                return False, "许可证过期时间格式错误"
            
            return True, f"许可证验证成功\n用户: {license_data.get('user_info', 'Unknown')}\n过期时间: {license_data.get('expiry_date')}"
            
        except Exception as e:
            return False, f"验证许可证时出错: {str(e)}"
    
    def save_license(self, license_key: str) -> bool:
        """
        保存许可证到本地文件
        
        Args:
            license_key: 许可证密钥
            
        Returns:
            是否保存成功
        """
        try:
            # 加密保存
            encrypted_key = base64.b64encode(license_key.encode('utf-8')).decode('utf-8')
            with open(self.license_file, 'w') as f:
                f.write(encrypted_key)
            return True
        except Exception as e:
            print(f"保存许可证时出错: {e}")
            return False
    
    def load_license(self) -> Optional[str]:
        """
        从本地文件加载许可证
        
        Returns:
            许可证密钥或None
        """
        try:
            if not os.path.exists(self.license_file):
                return None
            
            with open(self.license_file, 'r') as f:
                encrypted_key = f.read().strip()
            
            # 解密
            license_key = base64.b64decode(encrypted_key.encode('utf-8')).decode('utf-8')
            return license_key
        except Exception as e:
            print(f"加载许可证时出错: {e}")
            return None
    
    def is_authorized(self) -> Tuple[bool, str]:
        """
        检查软件是否已授权
        
        Returns:
            (是否已授权, 状态信息)
        """
        # 检查许可证
        license_key = self.load_license()
        if license_key:
            is_valid, message = self.validate_license_key(license_key)
            if is_valid:
                return True, f"✓ 已授权 - {message}"
            else:
                return False, f"✗ 许可证无效 - {message}"
        
        return False, "✗ 未授权 - 需要输入有效的许可证密钥"


def generate_license_for_hardware(hardware_id: str, days: int = 365, user_info: str = "Licensed User") -> str:
    """
    为指定硬件ID生成许可证（管理员工具）
    
    Args:
        hardware_id: 硬件指纹
        days: 有效天数
        user_info: 用户信息
        
    Returns:
        许可证密钥
    """
    license_manager = LicenseManager()
    expiry_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    return license_manager.generate_license_key(hardware_id, expiry_date, user_info)


if __name__ == "__main__":
    # 测试代码
    lm = LicenseManager()
    
    print("=== 硬件信息 ===")
    hardware_id = lm.get_hardware_id()
    print(f"当前设备硬件ID: {hardware_id}")
    
    print("\n=== 生成许可证 ===")
    # 生成一个一年期的许可证
    license_key = generate_license_for_hardware(hardware_id, 365, "测试用户")
    print(f"许可证密钥: {license_key}")
    
    print("\n=== 验证许可证 ===")
    is_valid, message = lm.validate_license_key(license_key)
    print(f"验证结果: {is_valid}")
    print(f"信息: {message}") 