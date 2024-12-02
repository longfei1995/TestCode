#pragma once

// 数学常量
static constexpr double kPi = 3.141592653;

// 地图相关的参数
static const int kGridPerMeter = 10; // 每米10个格子
static constexpr double kMeterPerCell = 1.0 / kGridPerMeter;
static const int kGridMapWidth = 25 * kGridPerMeter;  // 250格子
static const int kGridMapHeight = 15 * kGridPerMeter; // 150格子
static const int kCellPixel = 6;                      // 格子像素

template<class T>
struct Point2D {
  T x{};
  T y{};
};

template<class T>
struct Point3D : public Point2D<T> {
  T yaw{};
};