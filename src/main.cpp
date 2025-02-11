#include "qt_window.h"
#include "utils/common.h"
#include <QApplication>
#include <cassert>
#include <cmath>
#include <iostream>
#include <memory>
#include <thread>
#include <unordered_map>


void test01() {
  Logger::init("log/log.txt");
  Logger::info("test01");

  std::unordered_map<int, std::string> map;
  map[1] = "1";
  map[2] = "2";
  map[3] = "3";
  map[4] = "4";
  map[5] = "5";
  for (const auto& pair : map) {
    Logger::info("key: {}, value: {}", pair.first, pair.second);
  }
}
int main(int argc, char** argv) {
  // Logger::init("log/log.txt");

  // QApplication app(argc, argv);
  // GridMapWindow window;
  // window.show();
  // return app.exec();
  test01();
}
