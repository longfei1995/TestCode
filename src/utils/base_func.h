#pragma once

#include "base_type.h"
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

// 