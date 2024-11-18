#include "hybrid_a_star.h"
#include <algorithm>
#include <cmath>
#include <memory>
#include <queue>
#include <unordered_map>
HybridAStar::HybridAStar() : kParam_(Params::getInstance()) {
}

std::vector<STNode> HybridAStar::plan(const STNode& start, const STNode& goal,
                                      const std::vector<std::vector<bool>>& st_obstacles) {
  // 返回true时，a的优先级低于b
  auto cmp = [](const std::unique_ptr<STNode>& a, const std::unique_ptr<STNode>& b) {
    return (a->g + a->h) > (b->g + b->h);
  };
  std::priority_queue<std::unique_ptr<STNode>, std::vector<std::unique_ptr<STNode>>, decltype(cmp)> open_list(cmp);
  std::unordered_map<std::string, bool> closed_list;

  // 初始化起点
  auto start_node = std::make_unique<STNode>(start.s, start.l, start.theta, start.v, start.t);
  start_node->h = calHeuristic(*start_node, goal);
  open_list.push(std::move(start_node));

  STNode* final_node = nullptr;
  uint32_t iter_count = 0;
  while (!open_list.empty()) {
    iter_count++;
    if (iter_count > kParam_.astar.iter_max) {
      std::cout << "iter_count: " << iter_count << std::endl;
      break;
    }
    // 使用const_cast获取原始指针，然后从open_list中移除
    auto& mutable_top_node = const_cast<std::unique_ptr<STNode>&>(open_list.top());
    auto current = std::move(mutable_top_node);
    open_list.pop();

    // 检查是否到达目标(考虑时空距离)
    if (std::abs(current->s - goal.s) < kParam_.astar.ds && std::abs(current->l - goal.l) < kParam_.astar.ds && std::abs(current->t - goal.t) < kParam_.astar.dt) {
      final_node = current.get();
      break;
    }

    // 将当前节点加入已访问集合
    std::string current_index = getStateIndex(*current);
    if (closed_list[current_index]) {
      continue;
    }
    closed_list[current_index] = true;

    // 获取相邻节点
    auto neighbors = getNeighbors(*current);
    for (const auto& neighbor : neighbors) {
      if (!isStateValid(neighbor, st_obstacles)) {
        continue;
      }

      std::string neighbor_index = getStateIndex(neighbor);
      if (closed_list[neighbor_index]) {
        continue;
      }

      auto new_node = std::make_unique<STNode>(neighbor.s, neighbor.l,
                                               neighbor.theta, neighbor.v, neighbor.t);
      // 计算实际代价(考虑时间和控制代价)
      new_node->g = current->g + kParam_.astar.dt * (std::abs(neighbor.v - current->v) / kParam_.astar.max_accel + std::abs(neighbor.theta - current->theta) / kParam_.astar.max_steer);
      new_node->h = calHeuristic(*new_node, goal);
      new_node->parent = current.get();

      open_list.push(std::move(new_node));
    }
  }

  // 构建路径
  std::vector<STNode> path;
  if (final_node) {
    STNode* current = final_node;
    while (current) {
      path.push_back(*current);
      current = current->parent;
    }
    std::reverse(path.begin(), path.end());
  }

  return path;
}

double HybridAStar::calHeuristic(const STNode& current, const STNode& goal) {
  // 考虑时空距离的启发式函数
  double spatial_distance = std::hypot(current.s - goal.s, current.l - goal.l);
  double temporal_distance = std::abs(current.t - goal.t);

  // 归一化权重
  double w1 = 1.0, w2 = 0.5;
  return w1 * spatial_distance + w2 * temporal_distance;
}

bool HybridAStar::isStateValid(const STNode& state,
                               const std::vector<std::vector<bool>>& st_obstacles) {
  // 检查速度约束
  if (state.v < kParam_.astar.min_speed || state.v > kParam_.astar.max_speed) {
    return false;
  }

  // 转换为时空栅格坐标
  int s_idx = static_cast<int>(state.s / kParam_.astar.ds);
  int t_idx = static_cast<int>(state.t / kParam_.astar.dt);

  // 检查是否在地图范围内
  if (s_idx < 0 || s_idx >= st_obstacles.size() || t_idx < 0 || t_idx >= st_obstacles[0].size()) {
    return false;
  }

  // 检查是否与时空障碍物碰撞
  return !st_obstacles[s_idx][t_idx];
}

std::vector<STNode> HybridAStar::getNeighbors(const STNode& current) {
  std::vector<STNode> neighbors;

  // 速度采样
  const int v_samples = 5;
  double dv = 2 * kParam_.astar.max_accel * kParam_.astar.dt / (v_samples - 1);

  // 转向角采样
  const int theta_samples = 3;
  double dtheta = 2 * kParam_.astar.max_steer / (theta_samples - 1);

  for (int i = 0; i < v_samples; i++) {
    double v_new = current.v - kParam_.astar.max_accel * kParam_.astar.dt + i * dv;

    for (int j = 0; j < theta_samples; j++) {
      double theta_new = current.theta - kParam_.astar.max_steer + j * dtheta;

      // 使用自行车模型更新位置
      double ds = v_new * kParam_.astar.dt;
      double s_new = current.s + ds * std::cos(theta_new);
      double l_new = current.l + ds * std::sin(theta_new);
      double t_new = current.t + kParam_.astar.dt;

      neighbors.emplace_back(s_new, l_new, theta_new, v_new, t_new);
    }
  }

  return neighbors;
}

std::string HybridAStar::getStateIndex(const STNode& s) {
  // 将连续状态离散化用于哈希
  int s_idx = static_cast<int>(s.s / kParam_.astar.ds);
  int l_idx = static_cast<int>(s.l / kParam_.astar.ds);
  int t_idx = static_cast<int>(s.t / kParam_.astar.dt);
  int v_idx = static_cast<int>(s.v / (kParam_.astar.max_accel * kParam_.astar.dt));
  int theta_idx = static_cast<int>(s.theta / (kParam_.astar.max_steer * kParam_.astar.dt));

  return std::to_string(s_idx) + "_" + std::to_string(l_idx) + "_" + std::to_string(t_idx) + "_" + std::to_string(v_idx) + "_" + std::to_string(theta_idx);
}