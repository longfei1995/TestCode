"""经典A*"""

import heapq
import math
from typing import List, Tuple, Optional, Set, Dict


class Node:
    """表示搜索空间中的一个节点"""
    
    def __init__(self, x: int, y: int, walkable: bool = True):
        self.x = x
        self.y = y
        self.walkable = walkable
        
        # A*算法相关属性
        self.g_score = float('inf')  # 从起点到当前节点的实际成本
        self.f_score = float('inf')  # g_score + 启发式估计成本
        self.parent = None  # 用于重构路径
    
    def __lt__(self, other):
        """为了在优先队列中比较节点"""
        return self.f_score < other.f_score
    
    def __eq__(self, other):
        """节点相等性比较"""
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        """使节点可以作为字典的键"""
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"Node({self.x}, {self.y})"


class Grid:
    """表示搜索空间的网格地图"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.nodes = [[Node(x, y) for x in range(width)] for y in range(height)]
    
    def get_node(self, x: int, y: int) -> Optional[Node]:
        """获取指定坐标的节点"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.nodes[y][x]
        return None
    
    def set_obstacle(self, x: int, y: int):
        """设置障碍物"""
        node = self.get_node(x, y)
        if node:
            node.walkable = False
    
    def get_neighbors(self, node: Node) -> List[Node]:
        """获取节点的所有可行走邻居"""
        neighbors = []
        
        # 8个方向的移动（包括对角线）
        # 按照坐标系统排列：x向右递增，y向下递增
        directions = [
            (-1, -1), (0, -1), (1, -1),  
            (-1, 0),           (1, 0),   
            (-1, 1),  (0, 1),  (1, 1)    
        ]
        
        for dx, dy in directions:
            x, y = node.x + dx, node.y + dy
            neighbor = self.get_node(x, y)
            
            if neighbor and neighbor.walkable:
                neighbors.append(neighbor)
        
        return neighbors


def heuristic(node1: Node, node2: Node) -> float:
    """启发式函数：计算两个节点之间的欧几里得距离"""
    dx = abs(node1.x - node2.x)
    dy = abs(node1.y - node2.y)
    return math.sqrt(dx * dx + dy * dy)


def distance(node1: Node, node2: Node) -> float:
    """计算两个相邻节点之间的实际距离"""
    dx = abs(node1.x - node2.x)
    dy = abs(node1.y - node2.y)
    
    # 对角线移动的距离是sqrt(2)，水平/垂直移动是1
    if dx == 1 and dy == 1:
        return math.sqrt(2)
    else:
        return 1.0


def reconstruct_path(current: Optional[Node]) -> List[Node]:
    """从终点开始重构路径"""
    path = []
    while current is not None:
        path.append(current)
        current = current.parent
    return path[::-1]  # 反转列表，从起点到终点


def a_star(grid: Grid, start: Node, goal: Node) -> Optional[List[Node]]:
    """
    A*算法主函数
    
    参数:
        grid: 搜索空间网格
        start: 起始节点
        goal: 目标节点
    
    返回:
        找到的路径（节点列表），如果没有路径则返回None
    """
    
    # 初始化起始节点
    start.g_score = 0
    start.f_score = heuristic(start, goal)
    
    # 开放集合（待评估的节点）- 使用优先队列
    open_set = []
    heapq.heappush(open_set, start)
    
    # 开放集合的辅助集合，用于快速查找
    open_set_hash = {start}
    
    # 封闭集合（已评估的节点）
    closed_set = set()
    
    while open_set:
        # 获取f_score最小的节点
        current = heapq.heappop(open_set)
        open_set_hash.remove(current)
        
        # 如果到达目标，重构并返回路径
        if current == goal:
            return reconstruct_path(current)
        
        # 将当前节点移至封闭集合
        closed_set.add(current)
        
        # 检查所有邻居
        for neighbor in grid.get_neighbors(current):
            # 忽略已经评估过的邻居
            if neighbor in closed_set:
                continue
            
            # 计算从起点到邻居的暂定g_score
            tentative_g_score = current.g_score + distance(current, neighbor)
            
            # 如果这个邻居不在开放集合中，则发现了新节点
            if neighbor not in open_set_hash:
                heapq.heappush(open_set, neighbor)
                open_set_hash.add(neighbor)
            elif tentative_g_score >= neighbor.g_score:
                # 这不是更好的路径
                continue
            
            # 这是到达邻居的最佳路径，记录它
            neighbor.parent = current
            neighbor.g_score = tentative_g_score
            neighbor.f_score = neighbor.g_score + heuristic(neighbor, goal)
    
    # 没有找到路径
    return None


def print_grid_with_path(grid: Grid, path: Optional[List[Node]] = None):
    """打印网格地图和路径"""
    print("\n地图显示 (. = 空地, # = 障碍, S = 起点, G = 终点, * = 路径):")
    
    path_coords = set()
    if path:
        path_coords = {(node.x, node.y) for node in path}
    
    for y in range(grid.height):
        for x in range(grid.width):
            node = grid.get_node(x, y)
            
            if node is None:
                continue
                
            if path and len(path) > 0:
                if (x, y) == (path[0].x, path[0].y):
                    print('S', end=' ')
                elif (x, y) == (path[-1].x, path[-1].y):
                    print('G', end=' ')
                elif (x, y) in path_coords:
                    print('*', end=' ')
                elif not node.walkable:
                    print('#', end=' ')
                else:
                    print('.', end=' ')
            else:
                if not node.walkable:
                    print('#', end=' ')
                else:
                    print('.', end=' ')
        print()


def test_a_star():
    """测试A*算法"""
    print("=== A*算法测试 ===")
    
    # 创建10x10的网格
    grid = Grid(10, 10)
    
    # 设置一些障碍物
    obstacles = [
        (2, 2), (2, 3), (2, 4), (2, 5),
        (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
        (3, 7), (4, 7), (5, 7), (6, 7)
    ]
    
    for x, y in obstacles:
        grid.set_obstacle(x, y)
    
    # 设置起点和终点
    start = grid.get_node(0, 0)
    goal = grid.get_node(9, 9)
    
    if start is None or goal is None:
        print("错误：起点或终点不存在！")
        return
    
    print("开始搜索路径...")
    print_grid_with_path(grid)
    
    # 运行A*算法
    path = a_star(grid, start, goal)
    
    if path:
        print(f"\n找到路径！路径长度: {len(path)}")
        print("路径坐标:", [(node.x, node.y) for node in path])
        print_grid_with_path(grid, path)
        
        # 计算路径总成本
        total_cost = 0
        for i in range(1, len(path)):
            total_cost += distance(path[i-1], path[i])
        print(f"路径总成本: {total_cost:.2f}")
        
    else:
        print("\n没有找到路径！")


if __name__ == "__main__":
    test_a_star()












