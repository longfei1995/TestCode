import os
import subprocess


def shutdownPC(hours):
    """
    设置Windows系统在指定小时后关机
    
    参数:
        hours (float): 关机延迟时间（小时），支持小数，如3.5表示3小时30分钟
    
    返回:
        bool: 成功返回True，失败返回False
    """
    try:
        # 将小时转换为秒数
        seconds = int(hours * 3600)
        
        # 构建shutdown命令
        # /s 表示关机，/t 表示延迟时间（秒）
        cmd = f"shutdown /s /t {seconds}"
        
        # 执行命令
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"系统将在 {hours} 小时后关机")
            return True
        else:
            print(f"设置关机失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"设置关机时发生错误: {e}")
        return False


def cancelShutdown():
    """
    取消Windows系统当前的关机计划
    
    返回:
        bool: 成功返回True，失败返回False
    """
    try:
        # 使用 /a 参数取消关机
        cmd = "shutdown /a"
        
        # 执行命令
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("已成功取消关机计划")
            return True
        else:
            # 如果没有关机计划，Windows会返回错误
            if "没有要中止的关机" in result.stderr or "There is no shutdown" in result.stderr:
                print("当前没有关机计划需要取消")
                return True
            else:
                print(f"取消关机失败: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"取消关机时发生错误: {e}")
        return False


# 使用示例
if __name__ == "__main__":
    # 示例：设置3.5小时后关机
    # shutdownPC(3.5)
    
    # 示例：取消关机
    # cancelShutdown()
    pass
