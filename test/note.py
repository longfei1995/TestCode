## 轻量化的planner
# 1. 基于意图估计，结合地图拿到参考
# 2. 基于短时预测，确定局部运动趋势

## 基于Bezier曲线生成 长时轨迹
# 1. Bezier曲线的基本原理
# 通过设计控制点，从而生成参数化的曲线

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.special import comb

def bezierCurve(control_points, t):
    """
    计算Bezier曲线上的点
    control_points: 控制点数组 shape: (n+1, 2) n是曲线的阶数
    t: 参数值，范围[0,1]
    """
    n = len(control_points) - 1
    curve_points = np.zeros((len(t), 2))
    
    for i in range(n + 1):
        # Bernstein基函数
        bernstein = comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
        curve_points += np.outer(bernstein, control_points[i])
    
    return curve_points

def bezierDerivative(control_points, t):
    """计算Bezier曲线的一阶导数（切线方向）"""
    n = len(control_points) - 1
    if n == 0:
        return np.zeros((len(t), 2))
    
    # 构造导数的控制点
    derivative_points = n * (control_points[1:] - control_points[:-1])
    
    # 计算n-1阶Bezier曲线
    if len(derivative_points) == 1:
        return np.tile(derivative_points[0], (len(t), 1))
    
    return bezierCurve(derivative_points, t)

def objectiveFunction(control_points_flat, target_points, weights=None):
    """
    优化目标函数：使Bezier曲线尽可能接近目标点
    """
    # 重塑控制点
    control_points = control_points_flat.reshape(-1, 2)
    
    # 生成参数
    t = np.linspace(0, 1, len(target_points))
    
    # 计算曲线点
    curve_points = bezierCurve(control_points, t)
    
    # 计算误差
    error = np.sum((curve_points - target_points) ** 2)
    
    # 添加曲率平滑性约束
    if len(control_points) > 2:
        # 相邻控制点之间的距离变化应该平滑
        smoothness_penalty = 0
        for i in range(1, len(control_points) - 1):
            v1 = control_points[i] - control_points[i-1]
            v2 = control_points[i+1] - control_points[i]
            # 角度变化惩罚
            angle_diff = np.arccos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1, 1))
            smoothness_penalty += angle_diff ** 2
        
        error += 0.1 * smoothness_penalty
    
    return error

def main():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文显示
    plt.rcParams['axes.unicode_minus'] = False
    
    # 1. 确定初始控制点
    print("步骤1: 确定初始控制点")
    # 假设我们想要生成一条从(0,0)到(10,5)的曲线，中间有一些弯曲
    initial_control_points = np.array([
        [0, 0],      # 起点
        [3, 3],      # 第一个控制点
        [7, 2],      # 第二个控制点
        [10, 5]      # 终点
    ])
    
    # 2. 使用Bezier曲线公式计算出初始轨迹
    print("步骤2: 计算初始Bezier曲线轨迹")
    t_values = np.linspace(0, 1, 100)
    initial_curve = bezierCurve(initial_control_points, t_values)
    
    # 3. 定义目标轨迹点（这里模拟一些期望的轨迹点）
    print("步骤3: 定义目标轨迹并优化控制点")
    # 创建一些目标点，比如一条更平滑的路径
    target_t = np.linspace(0, 1, 20)
    target_points = np.column_stack([
        target_t * 10,  # x坐标
        2.5 + 2 * np.sin(target_t * np.pi)  # y坐标，正弦曲线
    ])
    
    # 优化控制点
    # 固定起点和终点，只优化中间的控制点
    def optimize_bezier(initial_points, target_points):
        # 只优化中间的控制点
        variable_points = initial_points[1:-1].flatten()
        fixed_start = initial_points[0]
        fixed_end = initial_points[-1]
        
        def objective_wrapper(var_points):
            # 重构完整的控制点数组
            full_points = np.vstack([
                fixed_start.reshape(1, -1),
                var_points.reshape(-1, 2),
                fixed_end.reshape(1, -1)
            ])
            return objectiveFunction(full_points.flatten(), target_points)
        
        # 执行优化
        result = minimize(objective_wrapper, variable_points, method='BFGS')
        
        # 重构优化后的控制点
        optimized_points = np.vstack([
            fixed_start.reshape(1, -1),
            result.x.reshape(-1, 2),
            fixed_end.reshape(1, -1)
        ])
        
        return optimized_points, result.success
    
    optimized_control_points, success = optimize_bezier(initial_control_points, target_points)
    print(f"优化{'成功' if success else '失败'}")
    
    # 计算优化后的曲线
    optimized_curve = bezierCurve(optimized_control_points, t_values)
    
    # 4. 使用matplotlib可视化曲线和控制点
    print("步骤4: 可视化结果")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 左图：优化前后对比
    ax1.plot(initial_curve[:, 0], initial_curve[:, 1], 'b-', label='初始Bezier曲线', linewidth=2)
    ax1.plot(optimized_curve[:, 0], optimized_curve[:, 1], 'r-', label='优化后Bezier曲线', linewidth=2)
    ax1.scatter(target_points[:, 0], target_points[:, 1], c='green', s=30, label='目标点', alpha=0.7)
    
    # 绘制控制点
    ax1.scatter(initial_control_points[:, 0], initial_control_points[:, 1], 
               c='blue', s=100, marker='s', label='初始控制点')
    ax1.plot(initial_control_points[:, 0], initial_control_points[:, 1], 'b--', alpha=0.5)
    
    ax1.scatter(optimized_control_points[:, 0], optimized_control_points[:, 1], 
               c='red', s=100, marker='s', label='优化后控制点')
    ax1.plot(optimized_control_points[:, 0], optimized_control_points[:, 1], 'r--', alpha=0.5)
    
    ax1.set_xlabel('X坐标')
    ax1.set_ylabel('Y坐标')
    ax1.set_title('Bezier曲线优化对比')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 右图：曲率分析
    # 计算曲线的曲率
    curve_derivative = bezierDerivative(optimized_control_points, t_values)
    speed = np.linalg.norm(curve_derivative, axis=1)
    
    ax2.plot(t_values, speed, 'g-', linewidth=2)
    ax2.set_xlabel('参数 t')
    ax2.set_ylabel('速度大小 |dx/dt|')
    ax2.set_title('曲线速度分布')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # 输出优化结果
    print("\n=== 优化结果 ===")
    print("初始控制点:")
    for i, point in enumerate(initial_control_points):
        print(f"  P{i}: ({point[0]:.2f}, {point[1]:.2f})")
    
    print("\n优化后控制点:")
    for i, point in enumerate(optimized_control_points):
        print(f"  P{i}: ({point[0]:.2f}, {point[1]:.2f})")
    
    # 计算拟合误差
    target_curve = bezierCurve(optimized_control_points, 
                              np.linspace(0, 1, len(target_points)))
    rmse = np.sqrt(np.mean((target_curve - target_points) ** 2))
    print(f"\n均方根误差 (RMSE): {rmse:.4f}")

if __name__ == "__main__":
    main()


