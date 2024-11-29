#pragma once
#include <iostream>
#include <memory>
#include <spdlog/logger.h>
#include <spdlog/sinks/rotating_file_sink.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <spdlog/spdlog.h>
#include <string>
#include <vector>

namespace Logger {

class LoggerInstance {
private:
  std::shared_ptr<spdlog::logger> logger;
  static constexpr size_t kMaxSingleFileSize = 1024 * 1024 * 10; // 10MB
  static constexpr size_t kMaxFiles = 3;                         // 3个文件
  // 私有构造函数
  LoggerInstance() = default;

public:
  static LoggerInstance& getInstance() {
    static LoggerInstance instance;
    return instance;
  }
  // 删除拷贝构造和赋值操作
  ~LoggerInstance() = default;
  LoggerInstance(const LoggerInstance&) = delete;
  LoggerInstance(LoggerInstance&&) = delete;
  LoggerInstance& operator=(const LoggerInstance&) = delete;
  LoggerInstance& operator=(LoggerInstance&&) = delete;
  void init(const std::string& log_file_name) {
    if (logger) {
      return; // 已经初始化过了
    }
    try {
      // 创建sinks
      auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
      auto file_sink = std::make_shared<spdlog::sinks::rotating_file_sink_mt>(log_file_name, kMaxSingleFileSize, kMaxFiles);

      std::vector<spdlog::sink_ptr> sinks{console_sink, file_sink};

      // 创建多sink logger
      logger = std::make_shared<spdlog::logger>("multi_sink", sinks.begin(), sinks.end());

      // 设置日志格式
      logger->set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%^%l%$] [thread %t] %v");

      // 设置全局日志级别
      logger->set_level(spdlog::level::debug);

      // 注册为默认logger
      spdlog::register_logger(logger);
    } catch (const spdlog::spdlog_ex& ex) {
      std::cerr << "Logger initialization failed: " << ex.what() << std::endl;
    }
  }

  template<typename... Args>
  void info(spdlog::format_string_t<Args...> fmt, Args &&...args) {
    if (logger)
      logger->info(fmt, std::forward<Args>(args)...);
  }

  template<typename... Args>
  void debug(spdlog::format_string_t<Args...> fmt, Args &&...args) {
    if (logger)
      logger->debug(fmt, std::forward<Args>(args)...);
  }

  template<typename... Args>
  void error(spdlog::format_string_t<Args...> fmt, Args &&...args) {
    if (logger)
      logger->error(fmt, std::forward<Args>(args)...);
  }

  template<typename... Args>
  void warn(spdlog::format_string_t<Args...> fmt, Args &&...args) {
    if (logger)
      logger->warn(fmt, std::forward<Args>(args)...);
  }
};

// 为了方便使用提供的包装函数
inline void init(const std::string& logger_file_name) {
  LoggerInstance::getInstance().init(logger_file_name);
}

template<typename... Args>
inline void info(spdlog::format_string_t<Args...> fmt, Args &&...args) {
  LoggerInstance::getInstance().info(fmt, std::forward<Args>(args)...);
}

template<typename... Args>
inline void debug(spdlog::format_string_t<Args...> fmt, Args &&...args) {
  LoggerInstance::getInstance().debug(fmt, std::forward<Args>(args)...);
}

template<typename... Args>
inline void error(spdlog::format_string_t<Args...> fmt, Args &&...args) {
  LoggerInstance::getInstance().error(fmt, std::forward<Args>(args)...);
}

template<typename... Args>
inline void warn(spdlog::format_string_t<Args...> fmt, Args &&...args) {
  LoggerInstance::getInstance().warn(fmt, std::forward<Args>(args)...);
}

} // namespace Logger