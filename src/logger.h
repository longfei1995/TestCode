#ifndef LOGGER_H
#define LOGGER_H

#include <memory>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <spdlog/spdlog.h>
#include <string>

namespace logger {

// 初始化日志系统
inline void init(const std::string& logger_name = "main_logger") {
  auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
  auto logger = std::make_shared<spdlog::logger>(logger_name, console_sink);
  spdlog::register_logger(logger);
  spdlog::set_default_logger(logger);
  spdlog::set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%^%l%$] %v");
  spdlog::set_level(spdlog::level::debug);
}

// 清理日志系统
inline void shutdown() {
  spdlog::shutdown();
}

// 信息日志
template<typename... Args>
inline void log_info(const std::string& fmt, Args&&... args) {
  spdlog::info(fmt, std::forward<Args>(args)...);
}

// 调试日志
template<typename... Args>
inline void log_debug(const std::string& fmt, Args&&... args) {
  spdlog::debug(fmt, std::forward<Args>(args)...);
}

} // namespace logger

#endif // LOGGER_H
