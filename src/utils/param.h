#pragma once
#include "utils/logger.h"
#include "yaml-cpp/yaml.h"
struct VehParam {
  double wheel_base{};
  std::string veh_type;

private:
  VehParam() { init(); }

public:
  static VehParam& getInstance() {
    static VehParam instance;
    return instance;
  }
  ~VehParam() = default;
  VehParam(const VehParam&) = delete;
  VehParam& operator=(const VehParam&) = delete;
  VehParam(VehParam&&) = delete;
  VehParam& operator=(VehParam&&) = delete;
  void init() {
    readYaml("config/setting.yaml");
    if (veh_type == "a02") {
      wheel_base = 2.8;
    }
    else {
      Logger::warn("Unknown vehicle type: {}", veh_type);
    }
  }
  void readYaml(const std::string& filename) {
    YAML::Node config = YAML::LoadFile(filename);
    if (config["veh_param"]) {
      if (config["veh_param"]["wheel_base"]) {
        wheel_base = config["veh_param"]["wheel_base"].as<double>();
      }
      if (config["veh_param"]["veh_type"]) {
        veh_type = config["veh_param"]["veh_type"].as<std::string>();
      }
    }
    else {
      Logger::warn("key [veh_param] not found in {}", filename);
    }
  }
};

struct AStarParam {
  double ds{};
  double dt{};
  double min_speed{};
  double max_speed{};
  double max_accel{};
  double max_steer{};
  int max_iter{};

private:
  AStarParam() { init(); }

public:
  static AStarParam& getInstance() {
    static AStarParam instance;
    return instance;
  }
  // 禁止拷贝、移动
  ~AStarParam() = default;
  AStarParam(const AStarParam&) = delete;
  AStarParam& operator=(const AStarParam&) = delete;
  AStarParam(AStarParam&&) = delete;
  AStarParam& operator=(AStarParam&&) = delete;
  // 初始化参数
  void init() {
    readYaml("config/setting.yaml");
  }
  // 读取yaml文件
  void readYaml(const std::string& filename) {
    YAML::Node config = YAML::LoadFile(filename);
    if (config["astar"]) {
      ds = config["astar"]["ds"].as<double>();
      dt = config["astar"]["dt"].as<double>();
      min_speed = config["astar"]["min_speed"].as<double>();
      max_speed = config["astar"]["max_speed"].as<double>();
      max_accel = config["astar"]["max_accel"].as<double>();
      max_steer = config["astar"]["max_steer"].as<double>();
      max_iter = config["astar"]["max_iter"].as<int>();
    }
    else {
      Logger::warn("key [astar] not found in {}", filename);
    }
  }
};