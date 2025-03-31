cmake_minimum_required(VERSION 3.21)
project(test0618)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# find_package(yaml-cpp REQUIRED)
find_package(spdlog REQUIRED)
# 设置可执行文件的路径
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_CURRENT_SOURCE_DIR}/bin)

# 添加src目录下以及所有子目录下的.cpp
file(GLOB_RECURSE SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

add_executable(${PROJECT_NAME} ${SOURCES})

# 包含头文件
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/src)

# 包含库文件
target_link_libraries(${PROJECT_NAME} PRIVATE spdlog::spdlog)