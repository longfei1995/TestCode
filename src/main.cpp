#include <fstream>
#include <iostream>
#include "logger.h"
void test01() {
  logger::init();
  logger::log_info("hello, world!");
  logger::log_info("程序启动");
}
int main(int argc, char** argv) {
  test01();
}
