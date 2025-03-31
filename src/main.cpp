#include <fstream>
#include <iostream>
#include "logger.h"
namespace {
void test01() {
  logger::init();
  float a = 1.23456789;
  logger::log_info("a = {:.2f}", a);
}
}
int main(int argc, char** argv) {
  test01();
}
