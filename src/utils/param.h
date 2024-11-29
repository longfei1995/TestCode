#pragma once
#include "utils/base_type.h"
#include "utils/logger.h"
#include "yaml-cpp/yaml.h"



struct VehParam {
  double wheel_base{};
  std::string veh_type{"a02"};
private:
  VehParam() { init(); }
public:
  static VehParam& getInstance() {
    static VehParam instance;
    return instance;
  }
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
    if (config["wheel_base"]) wheel_base = config["wheel_base"].as<double>();
  }
};