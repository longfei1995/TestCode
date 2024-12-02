#pragma once
#include "util_type.h"
#include "logger.h"
#include <cmath>

inline double deg2rad(double deg) {
  return deg * kPi / 180.0;
}

inline double rad2deg(double rad) {
  return rad * 180.0 / kPi;
}

// 将角度限制到-pi到pi之间
inline double normalizeAngle(double angle) {
  return fmod(angle + kPi, 2 * kPi) - kPi;
}

// 将meter转换成像素
inline double meter2pixel(double meter) {
  return meter * kGridPerMeter * kCellPixel;
}

// 将像素转换成meter
inline double pixel2meter(double pixel) {
  return pixel / (kGridPerMeter * kCellPixel);
}

// 给定两个点，计算两点之间的单位方向向量，从start指向end
inline Point2D<double> calUnitVector(const Point2D<double>& start, const Point2D<double>& end) {
  Point2D<double> vec{end.x - start.x, end.y - start.y};
  double norm = std::sqrt(vec.x * vec.x + vec.y * vec.y);
  // 处理两点重合的情况
  if (norm < 1e-6) {
    Logger::warn("calUnitVector: two points are too close to each other, return zero vector");
    return {0, 0};
  }
  return {vec.x / norm, vec.y / norm};
}
