"""Hybrid A*算法可视化程序"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from matplotlib.animation import FuncAnimation
import math
from typing import List, Tuple, Optional, Union
import os

from hybird_a_star import HybridAStarPlanner, create_obstacle_map
from veh_kinematics import VehicleKinematics


def setup_matplotlib_backend():
    """设置matplotlib后端，处理无显示环境的情况"""
    try:
        # 检查是否有显示环境
        if os.environ.get('DISPLAY') is None:
            print("检测到无显示环境，使用Agg后端保存图片...")
            matplotlib.use('Agg')
            return False
        else:
            # 尝试使用TkAgg后端，如果失败则使用Agg
            try:
                matplotlib.use('TkAgg')
                # 额外检查：尝试创建一个简单的图形来验证显示功能
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(1, 1, figsize=(1, 1))
                plt.close(fig)
                return True
            except:
                print("TkAgg后端不可用，使用Agg后端保存图片...")
                matplotlib.use('Agg')
                return False
    except Exception as e:
        print(f"设置matplotlib后端时出错: {e}")
        matplotlib.use('Agg')
        return False


class HybridAStarVisualizer:
    """Hybrid A*算法可视化器"""
    
    def __init__(self, figsize=(12, 10)):
        """
        初始化可视化器
        
        Args:
            figsize: 图形大小
        """
        self.has_display = setup_matplotlib_backend()
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.vehicle = VehicleKinematics()
        
        # 可视化配置
        self.vehicle_color = 'red'
        self.path_color = 'blue'
        self.obstacle_color = 'black'
        self.start_color = 'green'
        self.goal_color = 'orange'
        
        # 车辆可视化相关
        self.vehicle_patch = None
        self.path_line = None
        
        # 设置图形属性（处理中文字体问题）
        try:
            plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 中文字体
            plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号
        except:
            # 如果字体设置失败，使用默认字体
            pass
    
    def visualize_planning_result(self, 
                                planner: HybridAStarPlanner,
                                start_state: List[float],
                                goal_state: List[float],
                                path: Optional[List[List[float]]] = None,
                                title: str = "Hybrid A*路径规划结果",
                                save_path: str = "hybrid_astar_result.png"):
        """
        可视化路径规划结果
        
        Args:
            planner: Hybrid A*规划器
            start_state: 起始状态 [x, y, theta]
            goal_state: 目标状态 [x, y, theta]
            path: 规划的路径
            title: 图形标题
            save_path: 保存路径（无显示环境时使用）
        """
        self.ax.clear()
        
        # 绘制障碍物地图
        if planner.obstacle_map is not None:
            self._draw_obstacle_map(planner.obstacle_map, planner.map_min_x, planner.map_min_y, planner.grid_size)
        
        # 绘制起点和终点
        self._draw_start_goal(start_state, goal_state)
        
        # 绘制路径
        if path:
            self._draw_path(path)
            # 绘制车辆在终点的姿态
            self._draw_vehicle(goal_state)
        
        # 绘制车辆在起点的姿态
        self._draw_vehicle(start_state, color='green', alpha=0.7)
        
        # 设置图形属性
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('X (m)')
        self.ax.set_ylabel('Y (m)')
        self.ax.set_title(title)
        
        # 添加图例
        self._add_legend(planner, path)
        
        plt.tight_layout()
        
        # 总是先保存图片
        try:
            print(f"保存图片到: {save_path}")
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"图片保存成功: {save_path}")
        except Exception as e:
            print(f"保存图片失败: {e}")
        
        # 如果有显示环境，尝试显示
        if self.has_display:
            try:
                plt.show()
            except Exception as e:
                print(f"显示图形时出错: {e}")
    
    def animate_path_following(self, 
                             planner: HybridAStarPlanner,
                             start_state: List[float],
                             goal_state: List[float],
                             path: List[List[float]],
                             interval: int = 200,
                             save_path: str = "hybrid_astar_animation.gif"):
        """
        动态显示车辆沿路径移动的过程
        
        Args:
            planner: Hybrid A*规划器
            start_state: 起始状态
            goal_state: 目标状态
            path: 规划的路径
            interval: 动画间隔(ms)
            save_path: 动画保存路径
        """
        if not self.has_display:
            print("无显示环境，跳过动画...")
            return None
            
        self.ax.clear()
        
        # 绘制静态元素
        if planner.obstacle_map is not None:
            self._draw_obstacle_map(planner.obstacle_map, planner.map_min_x, planner.map_min_y, planner.grid_size)
        self._draw_start_goal(start_state, goal_state)
        self._draw_path(path)
        
        # 设置图形属性
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('X (m)')
        self.ax.set_ylabel('Y (m)')
        self.ax.set_title('Hybrid A*路径跟踪动画')
        
        # 存储车辆patch的引用
        vehicle_patches = []
        
        # 创建动画
        def animate(frame):
            # 清除之前的车辆
            for patch in vehicle_patches:
                if patch in self.ax.patches:
                    patch.remove()
            vehicle_patches.clear()
            
            if frame < len(path):
                state = path[frame]
                patch = self._draw_vehicle(state, return_patch=True)
                if patch:
                    vehicle_patches.append(patch)
                self.ax.set_title(f'Hybrid A*路径跟踪动画 - 步骤 {frame+1}/{len(path)}')
            
            return vehicle_patches
        
        try:
            # 启动动画
            anim = FuncAnimation(self.fig, animate, frames=len(path), 
                               interval=interval, blit=False, repeat=True)
            
            plt.tight_layout()
            plt.show()
            return anim
        except Exception as e:
            print(f"动画显示失败: {e}")
            return None
    
    def _draw_obstacle_map(self, obstacle_map: np.ndarray, min_x: float, min_y: float, grid_size: float):
        """绘制障碍物地图"""
        height, width = obstacle_map.shape
        
        for y in range(height):
            for x in range(width):
                if obstacle_map[y, x] == 1:
                    rect = patches.Rectangle(
                        (min_x + x * grid_size, min_y + y * grid_size),
                        grid_size, grid_size,
                        linewidth=0.5,
                        edgecolor='gray',
                        facecolor=self.obstacle_color,
                        alpha=0.8
                    )
                    self.ax.add_patch(rect)
    
    def _draw_start_goal(self, start_state: List[float], goal_state: List[float]):
        """绘制起点和终点"""
        # 起点
        self.ax.plot(start_state[0], start_state[1], 'o', 
                    color=self.start_color, markersize=12, label='起点')
        self.ax.arrow(start_state[0], start_state[1], 
                     2*math.cos(start_state[2]), 2*math.sin(start_state[2]),
                     head_width=0.5, head_length=0.5, fc=self.start_color, ec=self.start_color)
        
        # 终点
        self.ax.plot(goal_state[0], goal_state[1], 's', 
                    color=self.goal_color, markersize=12, label='终点')
        self.ax.arrow(goal_state[0], goal_state[1], 
                     2*math.cos(goal_state[2]), 2*math.sin(goal_state[2]),
                     head_width=0.5, head_length=0.5, fc=self.goal_color, ec=self.goal_color)
    
    def _draw_path(self, path: List[List[float]]):
        """绘制路径"""
        if not path:
            return
            
        x_coords = [state[0] for state in path]
        y_coords = [state[1] for state in path]
        
        self.ax.plot(x_coords, y_coords, '-', 
                    color=self.path_color, linewidth=2, label='规划路径')
        
        # 绘制路径方向箭头
        for i in range(0, len(path), max(1, len(path)//10)):
            state = path[i]
            self.ax.arrow(state[0], state[1], 
                         math.cos(state[2]), math.sin(state[2]),
                         head_width=0.3, head_length=0.3, 
                         fc=self.path_color, ec=self.path_color, alpha=0.7)
    
    def _draw_vehicle(self, state: List[float], color: Optional[str] = None, alpha: float = 1.0, return_patch: bool = False):
        """绘制车辆"""
        if color is None:
            color = self.vehicle_color
            
        # 获取车辆角点
        corners = self.vehicle.get_vehicle_corners(state)
        
        # 创建车辆多边形
        vehicle_polygon = patches.Polygon(corners, closed=True, 
                                        facecolor=color, edgecolor='black',
                                        alpha=alpha, linewidth=1.5)
        
        self.ax.add_patch(vehicle_polygon)
        
        # 绘制车辆前方向指示
        x, y, theta = state
        arrow_length = 1.5
        self.ax.arrow(x, y, arrow_length*math.cos(theta), arrow_length*math.sin(theta),
                     head_width=0.3, head_length=0.3, fc='white', ec='black', alpha=alpha)
        
        if return_patch:
            return vehicle_polygon
        return None
    
    def _add_legend(self, planner: HybridAStarPlanner, path: Optional[List[List[float]]]):
        """添加图例和统计信息"""
        # 基本图例
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor=self.start_color, 
                      markersize=10, label='起点'),
            Line2D([0], [0], marker='s', color='w', markerfacecolor=self.goal_color, 
                      markersize=10, label='终点'),
            patches.Patch(color=self.obstacle_color, alpha=0.8, label='障碍物'),
        ]
        
        if path:
            legend_elements.append(
                Line2D([0], [0], color=self.path_color, linewidth=2, label='规划路径')
            )
        
        self.ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
        
        # 添加统计信息
        if path:
            stats_text = f"路径长度: {planner.search_stats['path_length']:.2f}m\n"
            stats_text += f"搜索时间: {planner.search_stats['search_time']:.3f}s\n"
            stats_text += f"扩展节点: {planner.search_stats['nodes_expanded']}\n"
            stats_text += f"路径点数: {len(path)}"
            
            self.ax.text(0.02, 0.98, stats_text, transform=self.ax.transAxes,
                        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def compare_algorithms(self, 
                          results: List[Tuple[str, HybridAStarPlanner, List[List[float]]]],
                          start_state: List[float],
                          goal_state: List[float],
                          save_path: str = "algorithm_comparison.png"):
        """
        比较不同算法的结果
        
        Args:
            results: [(算法名称, 规划器, 路径), ...]
            start_state: 起始状态
            goal_state: 目标状态
            save_path: 保存路径
        """
        n_algorithms = len(results)
        fig, axes = plt.subplots(1, n_algorithms, figsize=(6*n_algorithms, 6))
        
        if n_algorithms == 1:
            axes = [axes]
        
        for i, (name, planner, path) in enumerate(results):
            ax = axes[i]
            
            # 绘制障碍物地图
            if planner.obstacle_map is not None:
                self._draw_obstacle_map_on_ax(ax, planner.obstacle_map, planner.map_min_x, 
                                            planner.map_min_y, planner.grid_size)
            
            # 绘制起点和终点
            self._draw_start_goal_on_ax(ax, start_state, goal_state)
            
            # 绘制路径
            if path:
                self._draw_path_on_ax(ax, path)
            
            # 设置图形属性
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('X (m)')
            ax.set_ylabel('Y (m)')
            ax.set_title(f'{name}算法结果')
            
            # 添加统计信息
            if path:
                stats_text = f"路径长度: {planner.search_stats['path_length']:.2f}m\n"
                stats_text += f"搜索时间: {planner.search_stats['search_time']:.3f}s\n"
                stats_text += f"扩展节点: {planner.search_stats['nodes_expanded']}"
                
                ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                       verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        
        # 总是先保存图片
        try:
            print(f"保存图片到: {save_path}")
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"图片保存成功: {save_path}")
        except Exception as e:
            print(f"保存图片失败: {e}")
        
        # 如果有显示环境，尝试显示
        if self.has_display:
            try:
                plt.show()
            except Exception as e:
                print(f"显示图形时出错: {e}")
    
    def _draw_obstacle_map_on_ax(self, ax, obstacle_map: np.ndarray, min_x: float, min_y: float, grid_size: float):
        """在指定坐标轴上绘制障碍物地图"""
        height, width = obstacle_map.shape
        
        for y in range(height):
            for x in range(width):
                if obstacle_map[y, x] == 1:
                    rect = patches.Rectangle(
                        (min_x + x * grid_size, min_y + y * grid_size),
                        grid_size, grid_size,
                        linewidth=0.5,
                        edgecolor='gray',
                        facecolor=self.obstacle_color,
                        alpha=0.8
                    )
                    ax.add_patch(rect)
    
    def _draw_start_goal_on_ax(self, ax, start_state: List[float], goal_state: List[float]):
        """在指定坐标轴上绘制起点和终点"""
        # 起点
        ax.plot(start_state[0], start_state[1], 'o', 
               color=self.start_color, markersize=12)
        ax.arrow(start_state[0], start_state[1], 
                2*math.cos(start_state[2]), 2*math.sin(start_state[2]),
                head_width=0.5, head_length=0.5, fc=self.start_color, ec=self.start_color)
        
        # 终点
        ax.plot(goal_state[0], goal_state[1], 's', 
               color=self.goal_color, markersize=12)
        ax.arrow(goal_state[0], goal_state[1], 
                2*math.cos(goal_state[2]), 2*math.sin(goal_state[2]),
                head_width=0.5, head_length=0.5, fc=self.goal_color, ec=self.goal_color)
    
    def _draw_path_on_ax(self, ax, path: List[List[float]]):
        """在指定坐标轴上绘制路径"""
        if not path:
            return
            
        x_coords = [state[0] for state in path]
        y_coords = [state[1] for state in path]
        
        ax.plot(x_coords, y_coords, '-', 
               color=self.path_color, linewidth=2)


def demo_hybrid_astar():
    """演示Hybrid A*算法"""
    print("开始Hybrid A*算法演示...")
    
    # 创建测试环境
    map_width, map_height = 50, 50
    obstacles = [
        (10, 10, 5, 15),   # 障碍物1
        (25, 20, 10, 5),   # 障碍物2
        (35, 5, 8, 20),    # 障碍物3
        (15, 35, 20, 5),   # 障碍物4
    ]
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
    
    # 定义起点和终点
    start_state = [5.0, 5.0, 0.0]  # x, y, theta
    goal_state = [45.0, 45.0, math.pi/2]
    
    print(f"起始状态: {start_state}")
    print(f"目标状态: {goal_state}")
    
    # 规划路径
    path = planner.plan(start_state, goal_state)
    
    # 创建可视化器
    visualizer = HybridAStarVisualizer()
    
    if path:
        print(f"路径规划成功!")
        print(f"路径长度: {planner.search_stats['path_length']:.2f}m")
        print(f"搜索时间: {planner.search_stats['search_time']:.3f}s")
        print(f"扩展节点数: {planner.search_stats['nodes_expanded']}")
        
        # 静态可视化
        visualizer.visualize_planning_result(planner, start_state, goal_state, path)
        
        # 询问用户是否要看动画（仅在有显示环境时）
        if visualizer.has_display:
            try:
                show_animation = input("是否显示路径跟踪动画？(y/n): ").lower() == 'y'
                if show_animation:
                    visualizer.animate_path_following(planner, start_state, goal_state, path, interval=300)
            except (KeyboardInterrupt, EOFError):
                print("\n用户中断操作")
        else:
            print("无显示环境，已保存静态图片")
        
    else:
        print("路径规划失败!")
        # 仍然显示环境
        visualizer.visualize_planning_result(planner, start_state, goal_state, None, 
                                           title="Hybrid A*路径规划失败")


def simple_test():
    """简单测试，不使用GUI"""
    print("运行简单测试（无GUI）...")
    
    # 创建测试环境
    map_width, map_height = 30, 30
    obstacles = [(10, 10, 5, 10), (20, 5, 5, 15)]
    obstacle_map = create_obstacle_map(map_width, map_height, obstacles)
    
    # 创建规划器
    planner = HybridAStarPlanner(
        grid_size=1.0,
        theta_resolution=18,  # 20度分辨率，减少计算量
        max_iter=2000,
        goal_tolerance=2.0
    )
    
    # 设置地图
    planner.set_obstacle_map(obstacle_map, map_min_x=0, map_min_y=0)
    
    # 定义起点和终点
    start_state = [2.0, 2.0, 0.0]
    goal_state = [25.0, 25.0, math.pi/4]
    
    print(f"起始状态: {start_state}")
    print(f"目标状态: {goal_state}")
    
    # 规划路径
    path = planner.plan(start_state, goal_state)
    
    if path:
        print(f"路径规划成功!")
        print(f"路径长度: {planner.search_stats['path_length']:.2f}m")
        print(f"搜索时间: {planner.search_stats['search_time']:.3f}s")
        print(f"扩展节点数: {planner.search_stats['nodes_expanded']}")
        print(f"路径点数: {len(path)}")
        
        # 打印路径的前几个点
        print("路径前5个点:")
        for i, point in enumerate(path[:5]):
            print(f"  点{i}: x={point[0]:.2f}, y={point[1]:.2f}, theta={point[2]:.3f}")
            
        # 保存简单的可视化结果
        try:
            visualizer = HybridAStarVisualizer()
            visualizer.visualize_planning_result(planner, start_state, goal_state, path,
                                               save_path="test_result.png")
            print("结果已保存到: test_result.png")
        except Exception as e:
            print(f"保存可视化结果时出错: {e}")
    else:
        print("路径规划失败!")


if __name__ == "__main__":
    try:
        # 首先尝试完整的演示
        demo_hybrid_astar()
    except Exception as e:
        print(f"演示程序出错: {e}")
        print("运行简单测试...")
        simple_test() 