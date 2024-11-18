#include <iostream>
#include <sys/types.h>
#include "yaml-cpp/yaml.h"
template<class T>
struct Point2D {
  T x{};
  T y{};
};

template<class T>
struct Point3D : public Point2D<T> {
  T yaw{};
};



struct VehParam {
  double wheel_base{};
  VehParam() { init(); }
  void init() {
    wheel_base = 2.8;
  }
  void readYaml(const std::string& filename) {
    try {
      YAML::Node config = YAML::LoadFile(filename);
      if (config["wheel_base"]) wheel_base = config["wheel_base"].as<double>();
    } catch (const YAML::Exception& e) {
      std::cerr << "读取配置文件失败: " << e.what() << std::endl; 
    }
  }
};

struct AstarParam {
public:
  double dt{};
  double ds{};
  double max_speed{};
  double min_speed{};
  double max_accel{};
  double max_steer{};
  uint32_t iter_max{};
  AstarParam() { init(); }
  void init() {
    dt = 0.1;
    ds = 0.1;
    max_speed = 20.0;
    min_speed = 0.0;
    max_accel = 2.0;
    max_steer = 0.6;
    iter_max = 100000;
  }
  void readYaml(const std::string& filename) {
    try {
      YAML::Node config = YAML::LoadFile(filename);
      if (config["dt"]) dt = config["dt"].as<double>();
      if (config["ds"]) ds = config["ds"].as<double>();
      if (config["max_speed"]) max_speed = config["max_speed"].as<double>();
      if (config["min_speed"]) min_speed = config["min_speed"].as<double>();
      if (config["max_accel"]) max_accel = config["max_accel"].as<double>();
      if (config["max_steer"]) max_steer = config["max_steer"].as<double>();
      if (config["iter_max"]) iter_max = config["iter_max"].as<uint32_t>();
    } catch (const YAML::Exception& e) {
      std::cerr << "读取配置文件失败: " << e.what() << std::endl;
    }
  }
};

struct Params {
private:
  Params() { init(); }
public:
  Params(const Params&) = delete;
  Params& operator=(const Params&) = delete;
  static Params& getInstance() {
    static Params instance;
    return instance;
  }

  VehParam veh;
  AstarParam astar;

  void init() {
    veh.init();
    astar.init();
  }

  void readYaml(const std::string& filename) {
    veh.readYaml(filename);
    astar.readYaml(filename);
  }
};