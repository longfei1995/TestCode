"""实现车辆运动学模型"""

import numpy as np
import math


class VehicleKinematics:
    """车辆运动学模型类 - 基于自行车模型"""
    
    def __init__(self, wheelbase=2.5, max_steer=np.pi/4, min_speed=0.1, max_speed=10.0):
        """
        初始化车辆参数
        
        Args:
            wheelbase: 轴距 (m)
            max_steer: 最大转向角 (rad)
            min_speed: 最小速度 (m/s)
            max_speed: 最大速度 (m/s)
        """
        self.wheelbase = wheelbase  # L - 车辆轴距
        self.max_steer = max_steer  # 最大前轮转向角
        self.min_speed = min_speed
        self.max_speed = max_speed
        
        # 车辆几何参数
        self.vehicle_length = 4.5
        self.vehicle_width = 2.0
        self.rear_to_center = 1.0  # 后轴到车辆中心的距离
        
    def update_state(self, state, control, dt):
        """
        基于自行车模型更新车辆状态
        
        Args:
            state: 当前状态 [x, y, theta] (位置x, y, 航向角theta)
            control: 控制输入 [speed, steer] (速度, 转向角)
            dt: 时间步长
            
        Returns:
            new_state: 新状态 [x, y, theta]
        """
        x, y, theta = state
        speed, steer = control
        
        # 限制控制输入
        speed = np.clip(speed, self.min_speed, self.max_speed)
        steer = np.clip(steer, -self.max_steer, self.max_steer)
        
        # 自行车模型运动学方程
        # dx/dt = v * cos(theta)
        # dy/dt = v * sin(theta)  
        # dtheta/dt = v * tan(steer) / L
        
        x_new = x + speed * np.cos(theta) * dt
        y_new = y + speed * np.sin(theta) * dt
        theta_new = theta + speed * np.tan(steer) / self.wheelbase * dt
        
        # 规范化角度到 [-pi, pi]
        theta_new = self.normalize_angle(theta_new)
        
        return [x_new, y_new, theta_new]
    
    def get_motion_primitives(self, speed=1.0, dt=1.0):
        """
        获取运动基元集合
        
        Args:
            speed: 运动速度
            dt: 时间步长
            
        Returns:
            motion_primitives: 运动基元列表，每个元素为 [speed, steer]
        """
        # 生成不同转向角的运动基元
        steer_angles = np.linspace(-self.max_steer, self.max_steer, 7)
        motion_primitives = []
        
        for steer in steer_angles:
            motion_primitives.append([speed, steer])
            
        return motion_primitives
    
    def get_turning_radius(self, steer):
        """
        计算转弯半径
        
        Args:
            steer: 转向角 (rad)
            
        Returns:
            radius: 转弯半径 (m)，直行时返回无穷大
        """
        if abs(steer) < 1e-6:
            return float('inf')
        return self.wheelbase / np.tan(abs(steer))
    
    def get_vehicle_corners(self, state):
        """
        获取车辆四个角点的坐标（用于碰撞检测）
        
        Args:
            state: 车辆状态 [x, y, theta]
            
        Returns:
            corners: 四个角点坐标 [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        """
        x, y, theta = state
        
        # 车辆中心到四个角点的相对坐标（车辆坐标系）
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        
        # 车辆几何中心相对于后轴中心的偏移
        center_x = x + self.rear_to_center * cos_theta
        center_y = y + self.rear_to_center * sin_theta
        
        # 四个角点相对于车辆几何中心的位置
        half_length = self.vehicle_length / 2.0
        half_width = self.vehicle_width / 2.0
        
        # 局部坐标系中的四个角点
        local_corners = [
            [half_length, half_width],   # 右前
            [-half_length, half_width],  # 右后  
            [-half_length, -half_width], # 左后
            [half_length, -half_width]   # 左前
        ]
        
        # 转换到全局坐标系
        corners = []
        for lx, ly in local_corners:
            gx = center_x + lx * cos_theta - ly * sin_theta
            gy = center_y + lx * sin_theta + ly * cos_theta
            corners.append([gx, gy])
            
        return corners
    
    @staticmethod
    def normalize_angle(angle):
        """
        将角度规范化到 [-pi, pi] 范围
        
        Args:
            angle: 输入角度 (rad)
            
        Returns:
            normalized_angle: 规范化后的角度 (rad)
        """
        while angle > np.pi:
            angle -= 2 * np.pi
        while angle < -np.pi:
            angle += 2 * np.pi
        return angle
    
    @staticmethod
    def calc_distance(state1, state2):
        """
        计算两个状态之间的欧几里得距离
        
        Args:
            state1: 状态1 [x, y, theta] 
            state2: 状态2 [x, y, theta]
            
        Returns:
            distance: 欧几里得距离
        """
        return np.sqrt((state1[0] - state2[0])**2 + (state1[1] - state2[1])**2)
    
    @staticmethod
    def calc_angle_diff(angle1, angle2):
        """
        计算两个角度之间的差值
        
        Args:
            angle1: 角度1 (rad)
            angle2: 角度2 (rad)
            
        Returns:
            angle_diff: 角度差值 (rad)，范围 [-pi, pi]
        """
        diff = angle1 - angle2
        return VehicleKinematics.normalize_angle(diff)


# 测试代码
if __name__ == "__main__":
    # 创建车辆运动学对象
    vehicle = VehicleKinematics()
    
    # 测试状态更新
    initial_state = [0.0, 0.0, 0.0]  # 起始状态：原点，航向向东
    control = [2.0, 0.3]  # 速度2m/s，转向角0.3rad
    dt = 0.1  # 时间步长0.1s
    
    print("初始状态:", initial_state)
    print("控制输入 [速度, 转向角]:", control)
    
    # 模拟10步
    state = initial_state.copy()
    for i in range(10):
        state = vehicle.update_state(state, control, dt)
        print(f"第{i+1}步: x={state[0]:.3f}, y={state[1]:.3f}, theta={state[2]:.3f}")
    
    # 测试运动基元
    primitives = vehicle.get_motion_primitives()
    print(f"\n运动基元数量: {len(primitives)}")
    
    # 测试车辆角点
    corners = vehicle.get_vehicle_corners([1.0, 2.0, np.pi/4])
    print(f"\n车辆角点: {corners}")