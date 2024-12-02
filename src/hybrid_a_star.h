#ifndef HYBRID_A_STAR_H
#define HYBRID_A_STAR_H
#include "utils/common.h"
#include <string>
#include <vector>
// 时空状态节点
struct STNode {
  double s;     // 纵向位置
  double l;     // 横向位置
  double theta; // 航向角
  double v;     // 速度
  double t;     // 时间
  double g;     // 实际代价
  double h;     // 启发值
  STNode* parent;
  STNode() : STNode(0, 0, 0, 0, 0) {}
  STNode(double s, double l, double theta, double v, double t)
      : s(s), l(l), theta(theta), v(v), t(t), g(0), h(0), parent(nullptr) {}
};

class HybridAStar {
public:
  HybridAStar();
  HybridAStar(const HybridAStar&) = delete;
  HybridAStar& operator=(const HybridAStar&) = delete;
  ~HybridAStar() = default;
  std::vector<STNode> plan(const STNode& start,
                           const STNode& goal,
                           const std::vector<std::vector<bool>>& st_obstacles);

private:
  // 计算启发式值(考虑时空距离)
  double calHeuristic(const STNode& current, const STNode& goal);

  // 检查节点是否有效(考虑动力学约束和时空障碍物)
  bool isStateValid(const STNode& state,
                    const std::vector<std::vector<bool>>& st_obstacles);

  // 获取相邻状态(考虑速度和转向采样)
  std::vector<STNode> getNeighbors(const STNode& current);

  // 离散化状态用于哈希
  std::string getStateIndex(const STNode& s);

  // 参数
  const VehParam& veh_param_;
  const AStarParam& astar_param_;
};

#endif