#include <cassert>
#include <cmath>
#include <iostream>
#include <memory>
#include <thread>
#include "utils/common.h"
#include <QApplication>
#include "qt_window.h"

void test01() {
  Logger::init("log/log.txt");
  Logger::info("test01");
}
int main(int argc, char** argv) {
  // Logger::init("log/log.txt");
  // QApplication app(argc, argv);
  // GridMapWindow window;
  // window.show();
  // return app.exec();
  test01();
}
