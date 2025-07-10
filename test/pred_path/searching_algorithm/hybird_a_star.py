"""实现混合A*算法"""

import numpy as np
import math
import heapq
from typing import List, Tuple, Optional, Dict, Set
import time

from veh_kinematics import VehicleKinematics
from reeds_shepp import ReedsShepp
from a_star import a_star, Grid, Node


class HybridState:
    """Hybrid A*算法中的状态节点"""
    
    def __init__(self, x: float, y: float, theta: float, g_cost: float = 0.0, parent=None):
        """
        初始化状态节点
        
        Args:
            x: x坐标
            y: y坐标  
            theta: 航向角 (弧度)
            g_cost: 从起点到当前节点的实际成本
            parent: 父节点
        """
        self.x = x
        self.y = y
        self.theta = theta
        self.g_cost = g_cost
        self.h_cost = 0.0  # 启发式成本
        self.f_cost = 0.0  # 总成本 f = g + h
        self.parent = parent
        
        # 离散化索引（用于快速查找）
        self.grid_x = 0
        self.grid_y = 0
        self.grid_theta = 0
        
    def __lt__(self, other):
        """用于优先队列比较"""
        return self.f_cost < other.f_cost
    
    def __eq__(self, other):
        """状态相等性判断"""
        return (self.grid_x == other.grid_x and 
                self.grid_y == other.grid_y and 
                self.grid_theta == other.grid_theta)
    
    def __hash__(self):
        """用于集合和字典"""
        return hash((self.grid_x, self.grid_y, self.grid_theta))
    
    def distance_to(self, other):
        """计算到另一个状态的距离"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


class HybridAStarPlanner:
    """Hybrid A*路径规划器"""
    
    def __init__(self, 
                 grid_size: float = 1.0,
                 theta_resolution: int = 72,
                 max_iter: int = 10000,
                 goal_tolerance: float = 2.0,
                 angle_tolerance: float = math.pi/6):
        """
        初始化Hybrid A*规划器
        
        Args:
            grid_size: 网格大小 (m)
            theta_resolution: 角度分辨率 (等分数)
            max_iter: 最大迭代次数
            goal_tolerance: 目标容差距离 (m)
            angle_tolerance: 目标角度容差 (rad)
        """
        self.grid_size = grid_size
        self.theta_resolution = theta_resolution
        self.theta_step = 2 * math.pi / theta_resolution
        self.max_iter = max_iter
        self.goal_tolerance = goal_tolerance
        self.angle_tolerance = angle_tolerance
        
        # 初始化组件
        self.vehicle = VehicleKinematics()
        self.rs_calculator = ReedsShepp(turning_radius=self.vehicle.get_turning_radius(self.vehicle.max_steer))
        
        # 地图相关
        self.obstacle_map = None
        self.heuristic_map = None
        self.map_width = 0
        self.map_height = 0
        self.map_min_x = 0
        self.map_min_y = 0
        
        # 搜索相关
        self.open_set = []
        self.closed_set = set()
        self.visited = {}  # 记录访问过的节点
        
        # 统计信息
        self.search_stats = {
            'nodes_expanded': 0,
            'search_time': 0.0,
            'path_length': 0.0
        }
    
    def set_obstacle_map(self, obstacle_map: np.ndarray, map_min_x: float, map_min_y: float):
        """
        设置障碍物地图
        
        Args:
            obstacle_map: 障碍物地图 (0=自由空间, 1=障碍物)
            map_min_x: 地图最小x坐标
            map_min_y: 地图最小y坐标
        """
        self.obstacle_map = obstacle_map
        self.map_height, self.map_width = obstacle_map.shape
        self.map_min_x = map_min_x
        self.map_min_y = map_min_y
        
        # 预计算启发式地图 (使用A*算法)
        self._precompute_heuristic_map()
    
    def plan(self, start_state: List[float], goal_state: List[float]) -> Optional[List[List[float]]]:
        """
        规划从起点到终点的路径
        
        Args:
            start_state: 起始状态 [x, y, theta]
            goal_state: 目标状态 [x, y, theta]
            
        Returns:
            path: 路径点列表 [[x, y, theta], ...] 或 None
        """
        start_time = time.time()
        
        # 初始化搜索
        self._reset_search()
        
        # 创建起始节点
        start_node = HybridState(start_state[0], start_state[1], start_state[2])
        goal_node = HybridState(goal_state[0], goal_state[1], goal_state[2])
        
        # 计算起始节点的网格索引
        self._calc_grid_index(start_node)
        self._calc_grid_index(goal_node)
        
        # 计算启发式成本
        start_node.h_cost = self._calc_heuristic_cost(start_node, goal_node)
        start_node.f_cost = start_node.g_cost + start_node.h_cost
        
        # 将起始节点加入开放集
        heapq.heappush(self.open_set, start_node)
        self.visited[self._get_state_key(start_node)] = start_node
        
        # 开始搜索
        while self.open_set and self.search_stats['nodes_expanded'] < self.max_iter:
            # 从开放集中取出最优节点
            current_node = heapq.heappop(self.open_set)
            
            # 检查是否达到目标
            if self._is_goal_reached(current_node, goal_node):
                path = self._reconstruct_path(current_node)
                self.search_stats['search_time'] = time.time() - start_time
                self.search_stats['path_length'] = self._calc_path_length(path)
                return path
            
            # 将当前节点移至闭合集
            self.closed_set.add(self._get_state_key(current_node))
            
            # 扩展邻居节点
            neighbors = self._get_neighbors(current_node)
            
            for neighbor in neighbors:
                # 计算网格索引
                self._calc_grid_index(neighbor)
                
                # 检查是否已在闭合集中
                neighbor_key = self._get_state_key(neighbor)
                if neighbor_key in self.closed_set:
                    continue
                
                # 检查碰撞
                if self._is_collision(neighbor):
                    continue
                
                # 计算成本
                movement_cost = self._calc_movement_cost(current_node, neighbor)
                tentative_g_cost = current_node.g_cost + movement_cost
                
                # 检查是否找到更好的路径
                if neighbor_key in self.visited:
                    existing_neighbor = self.visited[neighbor_key]
                    if tentative_g_cost >= existing_neighbor.g_cost:
                        continue
                
                # 更新邻居节点
                neighbor.parent = current_node
                neighbor.g_cost = tentative_g_cost
                neighbor.h_cost = self._calc_heuristic_cost(neighbor, goal_node)
                neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                
                # 加入开放集
                heapq.heappush(self.open_set, neighbor)
                self.visited[neighbor_key] = neighbor
            
            self.search_stats['nodes_expanded'] += 1
        
        # 搜索失败
        self.search_stats['search_time'] = time.time() - start_time
        return None
    
    def _get_neighbors(self, current_node: HybridState) -> List[HybridState]:
        """
        获取当前节点的邻居节点
        
        Args:
            current_node: 当前节点
            
        Returns:
            neighbors: 邻居节点列表
        """
        neighbors = []
        
        # 获取运动基元
        motion_primitives = self.vehicle.get_motion_primitives(speed=2.0, dt=1.0)
        
        for speed, steer in motion_primitives:
            # 使用车辆运动学模型计算下一个状态
            current_state = [current_node.x, current_node.y, current_node.theta]
            control = [speed, steer]
            next_state = self.vehicle.update_state(current_state, control, dt=1.0)
            
            # 创建邻居节点
            neighbor = HybridState(next_state[0], next_state[1], next_state[2])
            neighbors.append(neighbor)
        
        return neighbors
    
    def _calc_heuristic_cost(self, current: HybridState, goal: HybridState) -> float:
        """
        计算启发式成本
        
        Args:
            current: 当前状态
            goal: 目标状态
            
        Returns:
            h_cost: 启发式成本
        """
        # 方法1: Reeds-Shepp距离 (非完整约束，无障碍物)
        current_state = [current.x, current.y, current.theta]
        goal_state = [goal.x, goal.y, goal.theta]
        rs_cost = self.rs_calculator.calc_shortest_path_length(current_state, goal_state)
        
        # 方法2: A*距离 (完整约束，有障碍物)
        astar_cost = self._get_astar_heuristic(current, goal)
        
        # 取两者的最大值作为启发式成本
        return max(rs_cost, astar_cost)
    
    def _get_astar_heuristic(self, current: HybridState, goal: HybridState) -> float:
        """
        获取A*启发式成本 (从预计算的启发式地图中)
        
        Args:
            current: 当前状态
            goal: 目标状态
            
        Returns:
            astar_cost: A*启发式成本
        """
        # 将坐标转换为网格索引
        grid_x = self._world_to_grid_x(current.x)
        grid_y = self._world_to_grid_y(current.y)
        
        # 检查边界
        if (0 <= grid_x < self.map_width and 0 <= grid_y < self.map_height and 
            self.heuristic_map is not None):
            return self.heuristic_map[grid_y, grid_x]
        else:
            # 如果超出边界，使用欧几里得距离
            return current.distance_to(goal)
    
    def _calc_movement_cost(self, from_node: HybridState, to_node: HybridState) -> float:
        """
        计算运动成本
        
        Args:
            from_node: 起始节点
            to_node: 目标节点
            
        Returns:
            cost: 运动成本
        """
        # 基础距离成本
        distance_cost = from_node.distance_to(to_node)
        
        # 转向惩罚
        angle_diff = abs(self.vehicle.calc_angle_diff(to_node.theta, from_node.theta))
        steering_penalty = 0.5 * angle_diff
        
        # 倒车惩罚（如果支持倒车）
        reverse_penalty = 0.0
        
        return distance_cost + steering_penalty + reverse_penalty
    
    def _is_collision(self, state: HybridState) -> bool:
        """
        检查状态是否与障碍物碰撞
        
        Args:
            state: 状态节点
            
        Returns:
            collision: True表示碰撞
        """
        if self.obstacle_map is None:
            return False
        
        # 获取车辆四个角点
        vehicle_corners = self.vehicle.get_vehicle_corners([state.x, state.y, state.theta])
        
        # 检查每个角点是否在障碍物中
        for corner_x, corner_y in vehicle_corners:
            grid_x = self._world_to_grid_x(corner_x)
            grid_y = self._world_to_grid_y(corner_y)
            
            # 检查边界
            if (grid_x < 0 or grid_x >= self.map_width or 
                grid_y < 0 or grid_y >= self.map_height):
                return True
                
            # 检查障碍物
            if self.obstacle_map[grid_y, grid_x] == 1:
                return True
        
        return False
    
    def _is_goal_reached(self, current: HybridState, goal: HybridState) -> bool:
        """
        检查是否到达目标
        
        Args:
            current: 当前状态
            goal: 目标状态
            
        Returns:
            reached: True表示到达目标
        """
        distance = current.distance_to(goal)
        angle_diff = abs(self.vehicle.calc_angle_diff(current.theta, goal.theta))
        
        return (distance <= self.goal_tolerance and 
                angle_diff <= self.angle_tolerance)
    
    def _calc_grid_index(self, state: HybridState):
        """
        计算状态的网格索引
        
        Args:
            state: 状态节点
        """
        state.grid_x = self._world_to_grid_x(state.x)
        state.grid_y = self._world_to_grid_y(state.y)
        state.grid_theta = int((state.theta + math.pi) / self.theta_step) % self.theta_resolution
    
    def _world_to_grid_x(self, x: float) -> int:
        """世界坐标x转网格索引"""
        return int((x - self.map_min_x) / self.grid_size)
    
    def _world_to_grid_y(self, y: float) -> int:
        """世界坐标y转网格索引"""
        return int((y - self.map_min_y) / self.grid_size)
    
    def _get_state_key(self, state: HybridState) -> Tuple[int, int, int]:
        """获取状态的唯一键值"""
        return (state.grid_x, state.grid_y, state.grid_theta)
    
    def _reconstruct_path(self, goal_node: HybridState) -> List[List[float]]:
        """
        重构路径
        
        Args:
            goal_node: 目标节点
            
        Returns:
            path: 路径点列表
        """
        path = []
        current = goal_node
        
        while current is not None:
            path.append([current.x, current.y, current.theta])
            current = current.parent
        
        return path[::-1]  # 反转路径
    
    def _calc_path_length(self, path: List[List[float]]) -> float:
        """
        计算路径长度
        
        Args:
            path: 路径点列表
            
        Returns:
            length: 路径长度
        """
        if not path or len(path) < 2:
            return 0.0
        
        length = 0.0
        for i in range(1, len(path)):
            dx = path[i][0] - path[i-1][0]
            dy = path[i][1] - path[i-1][1]
            length += math.sqrt(dx*dx + dy*dy)
        
        return length
    
    def _precompute_heuristic_map(self):
        """预计算启发式地图"""
        # 这里可以预计算从每个网格点到目标的A*距离
        # 为了简化，暂时使用欧几里得距离
        self.heuristic_map = np.zeros_like(self.obstacle_map, dtype=float)
        
        # 实际实现中应该使用A*算法计算每个点到目标的最短距离
        # 这里简化处理
        pass
    
    def _reset_search(self):
        """重置搜索状态"""
        self.open_set = []
        self.closed_set = set()
        self.visited = {}
        self.search_stats = {
            'nodes_expanded': 0,
            'search_time': 0.0,
            'path_length': 0.0
        }


# 便利函数
def create_obstacle_map(width: int, height: int, obstacles: List[Tuple[int, int, int, int]]) -> np.ndarray:
    """
    创建障碍物地图
    
    Args:
        width: 地图宽度
        height: 地图高度  
        obstacles: 障碍物列表 [(x, y, w, h), ...] (左上角坐标和宽高)
        
    Returns:
        obstacle_map: 障碍物地图
    """
    obstacle_map = np.zeros((height, width), dtype=int)
    
    for x, y, w, h in obstacles:
        x1, y1 = max(0, x), max(0, y)
        x2, y2 = min(width, x + w), min(height, y + h)
        obstacle_map[y1:y2, x1:x2] = 1
    
    return obstacle_map


# 测试代码
if __name__ == "__main__":
    print("测试Hybrid A*算法...")
    
    # 创建简单的测试环境
    map_width, map_height = 50, 50
    obstacles = [(10, 10, 5, 15), (25, 20, 10, 5), (35, 5, 8, 20)]
    obstacle_map = create_obstacle_map(map_width, map_height, obstacles)
    
    # 创建规划器
    planner = HybridAStarPlanner(
        grid_size=1.0,
        theta_resolution=36,  # 10度分辨率
        max_iter=5000,
        goal_tolerance=2.0
    )
    
    # 设置地图
    planner.set_obstacle_map(obstacle_map, map_min_x=0, map_min_y=0)
    
    # 规划路径
    start_state = [5.0, 5.0, 0.0]  # x, y, theta
    goal_state = [45.0, 45.0, math.pi/2]
    
    print(f"起始状态: {start_state}")
    print(f"目标状态: {goal_state}")
    
    path = planner.plan(start_state, goal_state)
    
    if path:
        print(f"路径规划成功!")
        print(f"路径长度: {planner.search_stats['path_length']:.2f}m")
        print(f"搜索时间: {planner.search_stats['search_time']:.3f}s")
        print(f"扩展节点数: {planner.search_stats['nodes_expanded']}")
        print(f"路径点数: {len(path)}")
        
        # 打印前几个路径点
        print("前5个路径点:")
        for i, point in enumerate(path[:5]):
            print(f"  点{i}: x={point[0]:.2f}, y={point[1]:.2f}, theta={point[2]:.3f}")
    else:
        print("路径规划失败!")
        print(f"搜索时间: {planner.search_stats['search_time']:.3f}s")
        print(f"扩展节点数: {planner.search_stats['nodes_expanded']}")

