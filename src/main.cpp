#include <cassert>
#include <cmath>
#include <iostream>
#include <memory>
#include <thread>

#include "osqp.h"
#include <QApplication>
#include "qt_window.h"

void test01() {
  
}
int main(int argc, char** argv) {
  QApplication app(argc, argv);
  GridMapWindow window;
  window.show();
  return app.exec();
  // test01();
}
