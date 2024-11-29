cmake_minimum_required(VERSION 3.21)
project(test0618)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(yaml-cpp REQUIRED)

# Qt预编译
find_package(Qt5 COMPONENTS Widgets REQUIRED)
set(CMAKE_AUTOMOC ON)
# qt5_wrap_cpp(MOC_FILES ${CMAKE_CURRENT_SOURCE_DIR}/inc/qt_window.h) # 自动MOC失败了，添加手动MOC
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# 设置可执行文件的路径
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_CURRENT_SOURCE_DIR}/bin)

# 添加src目录下以及所有子目录下的.cpp
file(GLOB_RECURSE SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

add_executable(${PROJECT_NAME} ${SOURCES} ${MOC_FILES})
# 生成可执行文件
# add_executable(${PROJECT_NAME} ${SOURCES})

# 包含头文件
target_include_directories(${PROJECT_NAME} PRIVATE ${YAML_CPP_INCLUDE_DIR} ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/src)

# 包含库文件
target_link_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/lib)
target_link_libraries(${PROJECT_NAME} PRIVATE yaml-cpp::yaml-cpp Qt5::Widgets)