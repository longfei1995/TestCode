#include <fstream>
#include <iostream>
void test01() {
  std::ofstream ofs("test.txt");
  ofs << "test" << std::endl;
  ofs.close();
}
int main(int argc, char** argv) {
  test01();
}
