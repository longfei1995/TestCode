#pragma once

#include "base.h"
#include <QAction>
#include <QGraphicsScene>
#include <QGraphicsView>
#include <QGridLayout>
#include <QLabel>
#include <QMenu>
#include <QMenuBar>
#include <QPushButton>
#include <QWidget>
#include <memory>
#include <qaction.h>
#include <qcolor.h>

namespace GridColors {
const QColor kDark = qRgb(20, 20, 20);
const QColor kDarkGray = qRgb(60, 60, 60);
const QColor kGray = qRgb(100, 100, 100);
const QColor kLightGray = qRgb(160, 160, 160);
const QColor kDarkGreen = qRgb(0, 105, 0);
const QColor kLightYellow = qRgb(200, 200, 0);
const QColor kPink = qRgb(255, 170, 200);
const QColor kBlue = qRgb(0, 130, 250);
const QColor kOrange = qRgb(255, 185, 0);
const QColor kMagenta = qRgb(180, 0, 255);
const QColor kRosy = qRgb(255, 80, 200);
const QColor kGreen = qRgb(10, 254, 30);
const QColor kWhite = qRgb(255, 255, 255);
}; // namespace GridColors

enum class GridValue {
  kEmpty = 0,
  kHighGridPoint = 1,
  kLowGridPoint = 2,
  kHighObsLine = 3,
  kLowObsLine = 4,
  kHighObsCircle = 5,
  kLowObsCircle = 6,
  kVehicle = 7,
  kCustomShape = 8
};

enum class DrawMode {
  kHighGridPoint,
  kLowGridPoint,
  kHighObsLine,
  kLowObsLine,
  kHighObsCircle,
  kLowObsCircle,
};

class GridMapWindow : public QWidget {
  Q_OBJECT

public:
  explicit GridMapWindow(QWidget* parent = nullptr);
  GridMapWindow& operator=(const GridMapWindow&) = delete;
  GridMapWindow(const GridMapWindow&) = delete;
  GridMapWindow(GridMapWindow&&) = delete;
  GridMapWindow& operator=(GridMapWindow&&) = delete;
  ~GridMapWindow() override {}
  bool eventFilter(QObject* obj, QEvent* event) override;

private slots:
  void clearMap();
  void saveMap();
  void loadMap();
  void setDrawMode(DrawMode mode);

private:
  void initializeGrid();
  void createMenu();
  void createDrawingTools();
  static const QColor& setColor(GridValue grid_value);
  // 绘图函数
  void drawGrid(const Point2D<int>& point, const QColor& color);      // point 为grid坐标
  void drawPoint(const Point2D<double>& point, const QColor& color);  // point 为meter坐标
  void drawLine(const Point2D<double>& start, const Point2D<double>& end, const QColor& color); // start, end 为meter坐标
  void drawCircle(const Point2D<double>& circle_center, double radius, const QColor& color);    // circle_center 为meter坐标
  // 鼠标事件处理函数
  bool handlePointDrawing(QMouseEvent* event, const QColor& color);
  bool handleLineDrawing(QMouseEvent* event, const QColor& color);
  bool handleCircleDrawing(QMouseEvent* event, const QColor& color);
  void updateStatusLabel(const QString& message);

  bool isValidMousePos(const QPointF& mouse_pos_pixel);
  void clearCurrentDrawing();

  // 格子定义
  static const int kGridPerMeter = 10;              // 每米10个格子
  static constexpr double kMeterPerCell = 1.0 / kGridPerMeter;
  static const int kMapWidth = 25 * kGridPerMeter;  // 250格子
  static const int kMapHeight = 15 * kGridPerMeter; // 150格子
  static const int kCellPixel = 6;                  // 格子像素
  DrawMode draw_mode_ = DrawMode::kHighGridPoint;
  bool wait_second_point_ = false;
  // 鼠标位置
  QPointF mouse_pos_pixel_;
  Point2D<int> mouse_pos_grid_;
  Point2D<double> mouse_pos_meter_;
  // UI组件
  std::unique_ptr<QGraphicsScene> scene_;
  std::unique_ptr<QGraphicsView> view_;
  std::unique_ptr<QVBoxLayout> vbox_layout_;
  std::unique_ptr<QLabel> status_label_;
  std::unique_ptr<QMenuBar> menu_bar_;
  // 格子数据
  std::vector<std::vector<GridValue>> grid_map_;
};
