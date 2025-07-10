"""实现RS曲线"""

import numpy as np
import math
from typing import List, Tuple, Optional


class ReedsSheppPath:
    """Reeds-Shepp路径类"""
    
    def __init__(self, lengths: List[float], ctypes: List[str], cost: float):
        """
        初始化RS路径
        
        Args:
            lengths: 各段路径长度
            ctypes: 各段路径类型 ('L', 'R', 'S')
            cost: 总成本
        """
        self.lengths = lengths
        self.ctypes = ctypes
        self.cost = cost


class ReedsShepp:
    """Reeds-Shepp曲线计算类"""
    
    def __init__(self, turning_radius=1.0):
        """
        初始化Reeds-Shepp曲线计算器
        
        Args:
            turning_radius: 最小转弯半径
        """
        self.turning_radius = turning_radius
        
    def calc_optimal_path(self, start_state, goal_state):
        """
        计算两点间的最优Reeds-Shepp路径
        
        Args:
            start_state: 起始状态 [x, y, theta]
            goal_state: 目标状态 [x, y, theta]
            
        Returns:
            path: ReedsSheppPath对象，包含最优路径信息
        """
        # 坐标转换到标准形式
        dx = goal_state[0] - start_state[0]
        dy = goal_state[1] - start_state[1]
        dth = goal_state[2] - start_state[2]
        
        # 转换到单位圆坐标系
        c = math.cos(start_state[2])
        s = math.sin(start_state[2])
        
        x = (c * dx + s * dy) / self.turning_radius
        y = (-s * dx + c * dy) / self.turning_radius
        phi = self._normalize_angle(dth)
        
        # 计算所有可能的RS路径
        paths = []
        
        # CSC类型路径 (Curve-Straight-Curve)
        paths.extend(self._csc_paths(x, y, phi))
        
        # CCC类型路径 (Curve-Curve-Curve) 
        paths.extend(self._ccc_paths(x, y, phi))
        
        # CCCC类型路径
        paths.extend(self._cccc_paths(x, y, phi))
        
        # CCSC类型路径
        paths.extend(self._ccsc_paths(x, y, phi))
        
        # 选择成本最小的路径
        if not paths:
            return None
            
        best_path = min(paths, key=lambda p: p.cost)
        return best_path
    
    def calc_shortest_path_length(self, start_state, goal_state):
        """
        计算最短路径长度（用作启发式函数）
        
        Args:
            start_state: 起始状态 [x, y, theta]
            goal_state: 目标状态 [x, y, theta]
            
        Returns:
            length: 最短路径长度
        """
        path = self.calc_optimal_path(start_state, goal_state)
        if path is None:
            # 如果RS路径计算失败，返回欧几里得距离
            dx = goal_state[0] - start_state[0]
            dy = goal_state[1] - start_state[1]
            return math.sqrt(dx * dx + dy * dy)
        return path.cost * self.turning_radius
    
    def _csc_paths(self, x, y, phi):
        """计算CSC类型路径"""
        paths = []
        
        # LSL路径
        path = self._LSL(x, y, phi)
        if path:
            paths.append(path)
            
        # LSR路径  
        path = self._LSR(x, y, phi)
        if path:
            paths.append(path)
            
        # RSL路径
        path = self._RSL(x, y, phi)
        if path:
            paths.append(path)
            
        # RSR路径
        path = self._RSR(x, y, phi)
        if path:
            paths.append(path)
            
        return paths
    
    def _ccc_paths(self, x, y, phi):
        """计算CCC类型路径"""
        paths = []
        
        # LRL路径
        path = self._LRL(x, y, phi)
        if path:
            paths.append(path)
            
        # RLR路径  
        path = self._RLR(x, y, phi)
        if path:
            paths.append(path)
            
        return paths
    
    def _cccc_paths(self, x, y, phi):
        """计算CCCC类型路径"""
        paths = []
        
        # LRSL路径
        path = self._LRSL(x, y, phi)
        if path:
            paths.append(path)
            
        # LRSR路径
        path = self._LRSR(x, y, phi)
        if path:
            paths.append(path)
            
        # RLSL路径
        path = self._RLSL(x, y, phi)
        if path:
            paths.append(path)
            
        # RLSR路径
        path = self._RLSR(x, y, phi)
        if path:
            paths.append(path)
            
        return paths
    
    def _ccsc_paths(self, x, y, phi):
        """计算CCSC类型路径"""
        paths = []
        
        # LRSL路径变种
        path = self._LRSL_variant(x, y, phi)
        if path:
            paths.append(path)
            
        return paths
    
    def _LSL(self, x, y, phi):
        """计算LSL路径"""
        u, t = self._polar(x - math.sin(phi), y - 1.0 + math.cos(phi))
        if t >= 0.0:
            v = self._normalize_angle(phi - t)
            if v >= 0.0:
                cost = abs(t) + abs(u) + abs(v)
                return ReedsSheppPath([t, u, v], ['L', 'S', 'L'], cost)
        return None
    
    def _LSR(self, x, y, phi):
        """计算LSR路径"""
        u1, t1 = self._polar(x + math.sin(phi), y - 1.0 - math.cos(phi))
        u1 = u1 ** 2
        if u1 >= 4.0:
            u = math.sqrt(u1 - 4.0)
            theta = math.atan2(2.0, u)
            t = self._normalize_angle(t1 + theta)
            v = self._normalize_angle(t - phi)
            if t >= 0.0 and v <= 0.0:
                cost = abs(t) + abs(u) + abs(v)
                return ReedsSheppPath([t, u, v], ['L', 'S', 'R'], cost)
        return None
    
    def _RSL(self, x, y, phi):
        """计算RSL路径"""
        u1, t1 = self._polar(x - math.sin(phi), y - 1.0 + math.cos(phi))
        u1 = u1 ** 2
        if u1 >= 4.0:
            u = math.sqrt(u1 - 4.0)
            theta = math.atan2(u, 2.0)
            t = self._normalize_angle(t1 - theta)
            v = self._normalize_angle(phi - t)
            if t <= 0.0 and v >= 0.0:
                cost = abs(t) + abs(u) + abs(v)
                return ReedsSheppPath([t, u, v], ['R', 'S', 'L'], cost)
        return None
    
    def _RSR(self, x, y, phi):
        """计算RSR路径"""
        u, t = self._polar(x + math.sin(phi), y - 1.0 - math.cos(phi))
        if t <= 0.0:
            v = self._normalize_angle(-phi + t)
            if v <= 0.0:
                cost = abs(t) + abs(u) + abs(v)
                return ReedsSheppPath([t, u, v], ['R', 'S', 'R'], cost)
        return None
    
    def _LRL(self, x, y, phi):
        """计算LRL路径"""
        u1, t1 = self._polar(x - math.sin(phi), y - 1.0 + math.cos(phi))
        if u1 <= 4.0:
            u = -2.0 * math.asin(0.25 * u1)
            t = self._normalize_angle(t1 + 0.5 * u + math.pi)
            v = self._normalize_angle(phi - t + u)
            if t >= 0.0 and u <= 0.0:
                cost = abs(t) + abs(u) + abs(v)
                return ReedsSheppPath([t, u, v], ['L', 'R', 'L'], cost)
        return None
    
    def _RLR(self, x, y, phi):
        """计算RLR路径"""
        u1, t1 = self._polar(x + math.sin(phi), y - 1.0 - math.cos(phi))
        if u1 <= 4.0:
            u = 2.0 * math.asin(0.25 * u1)
            t = self._normalize_angle(t1 - 0.5 * u - math.pi)
            v = self._normalize_angle(-phi + t - u)
            if t <= 0.0 and u >= 0.0:
                cost = abs(t) + abs(u) + abs(v)
                return ReedsSheppPath([t, u, v], ['R', 'L', 'R'], cost)
        return None
    
    def _LRSL(self, x, y, phi):
        """计算LRSL路径"""
        xi = x + math.sin(phi)
        eta = y - 1.0 - math.cos(phi)
        rho, theta = self._polar(xi, eta)
        
        if rho >= 2.0:
            t = theta
            u = 2.0 - rho
            v = self._normalize_angle(t + 0.5 * math.pi - phi)
            if t >= 0.0 and u <= 0.0 and v <= 0.0:
                cost = abs(t) + abs(u) + abs(v) + abs(self._normalize_angle(0.5 * math.pi))
                return ReedsSheppPath([t, -0.5 * math.pi, u, v], ['L', 'R', 'S', 'L'], cost)
        return None
    
    def _LRSR(self, x, y, phi):
        """计算LRSR路径"""
        xi = x + math.sin(phi)
        eta = y - 1.0 - math.cos(phi)
        rho, theta = self._polar(-eta, xi)
        
        if rho >= 2.0:
            t = -theta
            u = 2.0 - rho
            v = self._normalize_angle(t - 0.5 * math.pi - phi)
            if t <= 0.0 and u <= 0.0 and v <= 0.0:
                cost = abs(t) + abs(u) + abs(v) + abs(self._normalize_angle(-0.5 * math.pi))
                return ReedsSheppPath([t, 0.5 * math.pi, u, v], ['L', 'R', 'S', 'R'], cost)
        return None
    
    def _RLSL(self, x, y, phi):
        """计算RLSL路径"""
        xi = x - math.sin(phi)
        eta = y - 1.0 + math.cos(phi)
        rho, theta = self._polar(xi, eta)
        
        if rho >= 2.0:
            t = theta
            u = 2.0 - rho
            v = self._normalize_angle(-t - 0.5 * math.pi + phi)
            if t >= 0.0 and u <= 0.0 and v >= 0.0:
                cost = abs(t) + abs(u) + abs(v) + abs(self._normalize_angle(-0.5 * math.pi))
                return ReedsSheppPath([t, -0.5 * math.pi, u, v], ['R', 'L', 'S', 'L'], cost)
        return None
    
    def _RLSR(self, x, y, phi):
        """计算RLSR路径"""
        xi = x - math.sin(phi)
        eta = y - 1.0 + math.cos(phi)
        rho, theta = self._polar(eta, -xi)
        
        if rho >= 2.0:
            t = -theta
            u = 2.0 - rho
            v = self._normalize_angle(t + 0.5 * math.pi + phi)
            if t <= 0.0 and u <= 0.0 and v >= 0.0:
                cost = abs(t) + abs(u) + abs(v) + abs(self._normalize_angle(0.5 * math.pi))
                return ReedsSheppPath([t, 0.5 * math.pi, u, v], ['R', 'L', 'S', 'R'], cost)
        return None
    
    def _LRSL_variant(self, x, y, phi):
        """LRSL路径变种"""
        # 这里可以添加更多的CCSC类型路径
        return None
    
    @staticmethod
    def _polar(x, y):
        """直角坐标转极坐标"""
        r = math.sqrt(x * x + y * y)
        theta = math.atan2(y, x)
        return r, theta
    
    @staticmethod
    def _normalize_angle(angle):
        """角度规范化到[-pi, pi]"""
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle
    
    def generate_path_points(self, start_state, path, step_size=0.1):
        """
        根据RS路径生成路径点
        
        Args:
            start_state: 起始状态 [x, y, theta]
            path: ReedsSheppPath对象
            step_size: 步长
            
        Returns:
            points: 路径点列表 [[x, y, theta], ...]
        """
        points = []
        current_state = start_state.copy()
        points.append(current_state.copy())
        
        for i, (length, ctype) in enumerate(zip(path.lengths, path.ctypes)):
            if ctype == 'S':  # 直线段
                steps = int(abs(length * self.turning_radius) / step_size)
                for j in range(steps):
                    current_state[0] += step_size * math.cos(current_state[2]) * (1 if length >= 0 else -1)
                    current_state[1] += step_size * math.sin(current_state[2]) * (1 if length >= 0 else -1)
                    points.append(current_state.copy())
            else:  # 圆弧段
                sign = 1 if ctype == 'L' else -1
                angular_step = step_size / self.turning_radius
                steps = int(abs(length) / angular_step)
                
                for j in range(steps):
                    current_state[2] += angular_step * sign * (1 if length >= 0 else -1)
                    current_state[0] += step_size * math.cos(current_state[2]) * (1 if length >= 0 else -1)
                    current_state[1] += step_size * math.sin(current_state[2]) * (1 if length >= 0 else -1)
                    current_state[2] = self._normalize_angle(current_state[2])
                    points.append(current_state.copy())
        
        return points


# 测试代码
if __name__ == "__main__":
    # 创建RS曲线计算器
    rs = ReedsShepp(turning_radius=1.0)
    
    # 测试路径计算
    start = [0.0, 0.0, 0.0]
    goal = [3.0, 2.0, math.pi/2]
    
    print(f"起始状态: {start}")
    print(f"目标状态: {goal}")
    
    # 计算最短路径
    path = rs.calc_optimal_path(start, goal)
    if path:
        print(f"路径类型: {path.ctypes}")
        print(f"路径长度: {path.lengths}")
        print(f"总成本: {path.cost:.3f}")
        print(f"实际长度: {rs.calc_shortest_path_length(start, goal):.3f}m")
        
        # 生成路径点
        points = rs.generate_path_points(start, path, step_size=0.2)
        print(f"生成路径点数: {len(points)}")
        print("前5个路径点:")
        for i, point in enumerate(points[:5]):
            print(f"  点{i}: x={point[0]:.3f}, y={point[1]:.3f}, theta={point[2]:.3f}")
    else:
        print("未找到有效路径")