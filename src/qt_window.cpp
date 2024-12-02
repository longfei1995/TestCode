#include "qt_window.h"
#include "utils/util_func.h"
#include "utils/util_type.h"
#include <QFileDialog>
#include <QHBoxLayout>
#include <QMessageBox>
#include <QMouseEvent>
#include <QScrollBar>
#include <QTimer>
#include <QVBoxLayout>
#include <cmath>
#include <memory>
#include <qboxlayout.h>
#include <qcolor.h>
#include <qgraphicsscene.h>
#include <qgraphicsview.h>
#include <qmenubar.h>
#include <qnamespace.h>
#include <qpen.h>
#include <qwidget.h>

GridMapWindow::GridMapWindow(QWidget* parent) : QWidget(parent) {
  // 基础窗口设置
  setWindowTitle("Plan Simulator");
  setWindowFlags(windowFlags() & ~Qt::WindowMaximizeButtonHint);
  setFixedSize(kGridMapWidth * kCellPixel + 100, kGridMapHeight * kCellPixel + 100);

  // 创建主布局
  vbox_layout_ = std::make_unique<QVBoxLayout>(this);

  // Scene(场景)相关设置
  scene_ = std::make_unique<QGraphicsScene>(this);
  scene_->setSceneRect(0, 0, kGridMapWidth * kCellPixel, kGridMapHeight * kCellPixel);
  scene_->setBackgroundBrush(GridColors::kDark);

  // View(视图)相关设置
  view_ = std::make_unique<QGraphicsView>(scene_.get());
  // view_->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
  // view_->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
  view_->setViewportUpdateMode(QGraphicsView::FullViewportUpdate);
  view_->setRenderHint(QPainter::Antialiasing, false);
  view_->setDragMode(QGraphicsView::RubberBandDrag);
  view_->setTransformationAnchor(QGraphicsView::NoAnchor);
  view_->setInteractive(true);

  // 创建菜单栏（在translate之前）
  initMap();
  createMenu();

  // 设置视图变换（放在最后）
  view_->translate(50, 50); // 调整视图位置

  // 在视图变换之后绘制坐标系
  drawCoordinateSystem(Point2D<double>{0.0, 0.0}, 2.0, QPen(Qt::red, 2));

  // 事件处理设置
  view_->viewport()->installEventFilter(this);
  vbox_layout_->addWidget(view_.get());

  // 创建状态栏
  status_label_ = std::make_unique<QLabel>("请选择绘图工具，按下ctrl+鼠标滚轮缩放，按下鼠标中键拖动");
  vbox_layout_->addWidget(status_label_.get());
}

void GridMapWindow::initMap() {
  // 使用两种不同的画笔
  QPen major_pen(GridColors::kLightGray);
  major_pen.setWidthF(1.0); // 使用setWidthF设置精确的1像素宽度

  QPen minor_pen(GridColors::kDarkGray);
  minor_pen.setWidthF(1.0); // 使用setWidthF设置精确的1像素宽度

  // 绘制垂直线
  for (int x = 0; x <= kGridMapWidth; ++x) {
    if (x % kGridPerMeter == 0) { // 每米(10格)画一条主线
      scene_->addLine(x * kCellPixel, 0, x * kCellPixel, kGridMapHeight * kCellPixel, major_pen);
    }
    else { // 其他位置画次要线
      scene_->addLine(x * kCellPixel, 0, x * kCellPixel, kGridMapHeight * kCellPixel, minor_pen);
    }
  }

  // 绘制水平线
  for (int y = 0; y <= kGridMapHeight; ++y) {
    if (y % kGridPerMeter == 0) { // 每米(10格)画一条主线
      scene_->addLine(0, y * kCellPixel, kGridMapWidth * kCellPixel, y * kCellPixel, major_pen);
    }
    else { // 其他位置画次要线
      scene_->addLine(0, y * kCellPixel, kGridMapWidth * kCellPixel, y * kCellPixel, minor_pen);
    }
  }
  grid_map_.resize(kGridMapWidth, std::vector<GridValue>(kGridMapHeight, GridValue::kEmpty));
  // 允许视图接收鼠标事件
  view_->viewport()->installEventFilter(this);
}

void GridMapWindow::createMenu() {
  menu_bar_ = std::make_unique<QMenuBar>(this);
  // Map菜单
  auto* map_menu = menu_bar_->addMenu("地图编辑");
  auto* clear_action = map_menu->addAction("清空地图");
  auto* save_action = map_menu->addAction("保存地图");
  auto* load_action = map_menu->addAction("加载地图");

  connect(clear_action, &QAction::triggered, this, &GridMapWindow::clearMap);
  connect(save_action, &QAction::triggered, this, &GridMapWindow::saveMap);
  connect(load_action, &QAction::triggered, this, &GridMapWindow::loadMap);

  // 绘图工具菜单
  QMenu* draw_menu = menu_bar_->addMenu("绘图工具");

  // Point子菜单
  auto* point_menu = draw_menu->addMenu("单点");
  QAction* high_point_action = point_menu->addAction("高障碍物点");
  QAction* low_point_action = point_menu->addAction("低障碍物点");

  // Line子菜单
  auto* line_menu = draw_menu->addMenu("线段");
  QAction* high_line_action = line_menu->addAction("高障碍物线段");
  QAction* low_line_action = line_menu->addAction("低障碍物线段");

  // Circle子菜单
  auto* circle_menu = draw_menu->addMenu("圆");
  QAction* high_circle_action = circle_menu->addAction("高障碍物圆");
  QAction* low_circle_action = circle_menu->addAction("低障碍物圆");

  // 连接信号槽
  connect(high_point_action, &QAction::triggered, [this]() {
    setDrawMode(DrawMode::kHighGridPoint);
  });
  connect(low_point_action, &QAction::triggered, [this]() {
    setDrawMode(DrawMode::kLowGridPoint);
  });
  connect(high_line_action, &QAction::triggered, [this]() {
    setDrawMode(DrawMode::kHighObsLine);
  });
  connect(low_line_action, &QAction::triggered, [this]() {
    setDrawMode(DrawMode::kLowObsLine);
  });
  connect(high_circle_action, &QAction::triggered, [this]() {
    setDrawMode(DrawMode::kHighObsCircle);
  });
  connect(low_circle_action, &QAction::triggered, [this]() {
    setDrawMode(DrawMode::kLowObsCircle);
  });

  vbox_layout_->setMenuBar(menu_bar_.get());
}

const QColor& GridMapWindow::getColor(DrawMode mode) {
  switch (mode) {
    case DrawMode::kNone:
      return GridColors::kDark;
    case DrawMode::kHighGridPoint:
      return GridColors::kDarkGreen;
    case DrawMode::kLowGridPoint:
      return GridColors::kBlue;
    case DrawMode::kHighObsLine:
      return GridColors::kGreen;
    case DrawMode::kLowObsLine:
      return GridColors::kBlue;
    case DrawMode::kHighObsCircle:
      return GridColors::kGreen;
    case DrawMode::kLowObsCircle:
      return GridColors::kBlue;
    default:
      return GridColors::kDark;
  }
}

void GridMapWindow::setDrawMode(DrawMode mode) {
  // 设置绘图模式
  draw_mode_ = mode;
  is_draw_second_point_ = false;
  QString mode_msg;
  // 根据绘图模式更新状态栏信息
  switch (mode) {
    case DrawMode::kHighGridPoint:
    case DrawMode::kLowGridPoint:
      mode_msg = "点绘制模式";
      break;
    case DrawMode::kHighObsLine:
    case DrawMode::kLowObsLine:
      mode_msg = "请点选线段的第一个点";
      break;
    case DrawMode::kHighObsCircle:
    case DrawMode::kLowObsCircle:
      mode_msg = "请点选圆心位置";
      break;
      // todo ... 其他模式
  }
  updateStatusLabel(mode_msg);
}

void GridMapWindow::drawGrid(const Point2D<int>& grid_point, const QColor& color) {
  QPen pen(Qt::NoPen);
  QBrush brush(color);
  // 留出栅格线的空间
  scene_->addRect(
    grid_point.x * kCellPixel + 0.5,
    grid_point.y * kCellPixel + 0.5,
    kCellPixel - 1.0,
    kCellPixel - 1.0,
    pen,
    brush);
}

void GridMapWindow::drawLine(const Point2D<double>& start, const Point2D<double>& end, const QColor& color, double pixel_size) {
  // 每0.2米画一个点
  const double line_length = hypot(end.x - start.x, end.y - start.y);
  const Point2D<double> line_vector = calUnitVector(start, end);
  double current_dist = 0.0;
  Point2D<double> curr_draw_point;
  while (current_dist <= line_length) {
    curr_draw_point.x = start.x + line_vector.x * current_dist;
    curr_draw_point.y = start.y + line_vector.y * current_dist;
    drawPoint(curr_draw_point, color, pixel_size);
    current_dist += 0.2;
  }
  // 确保终点被画上
  drawPoint(end, color, pixel_size);
}

void GridMapWindow::drawCircle(const Point2D<double>& circle_center, double radius, const QColor& color) {
  // 米 转换成 像素坐标
  auto pixel_x = meter2pixel(circle_center.x);
  auto pixel_y = meter2pixel(circle_center.y);
  auto scene_radius = meter2pixel(radius);
  QPen pen(color);
  QBrush brush(Qt::NoBrush);
  // 画一个圆
  scene_->addEllipse(
    pixel_x - scene_radius,
    pixel_y - scene_radius,
    2 * scene_radius,
    2 * scene_radius,
    pen,
    brush);
}

void GridMapWindow::drawCoordinateSystem(const Point2D<double>& origin, double axis_length, const QPen& pen) {
  // 将米单位转换为像素单位
  Point2D<double> origin_pixel{meter2pixel(origin.x), meter2pixel(origin.y)};
  double axis_length_pixel{meter2pixel(axis_length)};

  // 箭头参数
  const double arrow_size = 10.0;       // 箭头大小（像素）
  const double arrow_angle = kPi / 6.0; // 箭头角度 (30度)

  // 绘制X轴主线
  scene_->addLine(origin_pixel.x, origin_pixel.y, origin_pixel.x + axis_length_pixel, origin_pixel.y, pen);
  // 绘制Y轴主线
  scene_->addLine(origin_pixel.x, origin_pixel.y, origin_pixel.x, origin_pixel.y + axis_length_pixel, pen);

  // 绘制X轴箭头
  QPolygonF x_arrow;
  x_arrow << QPointF(origin_pixel.x + axis_length_pixel, origin_pixel.y) // 箭头尖端
          << QPointF(origin_pixel.x + axis_length_pixel - arrow_size * cos(arrow_angle),
                     origin_pixel.y + arrow_size * sin(arrow_angle)) // 箭头右上角
          << QPointF(origin_pixel.x + axis_length_pixel - arrow_size * cos(arrow_angle),
                     origin_pixel.y - arrow_size * sin(arrow_angle)); // 箭头右下角
  scene_->addPolygon(x_arrow, pen, QBrush(pen.color()));

  // 绘制Y轴箭头
  QPolygonF y_arrow;
  y_arrow << QPointF(origin_pixel.x, origin_pixel.y + axis_length_pixel) // 箭头尖端
          << QPointF(origin_pixel.x + arrow_size * sin(arrow_angle),
                     origin_pixel.y + axis_length_pixel - arrow_size * cos(arrow_angle)) // 箭头右下角
          << QPointF(origin_pixel.x - arrow_size * sin(arrow_angle),
                     origin_pixel.y + axis_length_pixel - arrow_size * cos(arrow_angle)); // 箭头左下角
  scene_->addPolygon(y_arrow, pen, QBrush(pen.color()));
}

void GridMapWindow::updateStatusLabel(const QString& message) {
  if (status_label_) {
    status_label_->setText(message);
  }
}

bool GridMapWindow::isValidMousePos(const Point2D<double>& mouse_pos_pixel) {
  auto max_mouse_x = kGridMapWidth * kCellPixel;
  auto max_mouse_y = kGridMapHeight * kCellPixel;
  return mouse_pos_pixel.x > 0 && mouse_pos_pixel.x < max_mouse_x && mouse_pos_pixel.y > 0 && mouse_pos_pixel.y < max_mouse_y;
}

void GridMapWindow::clearCurrentDrawing() {
  is_draw_second_point_ = false;
  updateStatusLabel("绘制已取消");
}

void GridMapWindow::clearMap() {
  scene_->clear();
  initMap();
  grid_map_.assign(kGridMapWidth, std::vector<GridValue>(kGridMapHeight, GridValue::kEmpty));
}

// return true 表示完全由这个函数处理事件，return false 表示将剩下的交给父类处理
bool GridMapWindow::eventFilter(QObject* obj, QEvent* event) {
  static bool is_mouse_middle_pressed = false;
  static QPoint last_mouse_pos;

  if (obj != view_->viewport()) {
    return false;
  }

  if (event->type() == QEvent::MouseButtonPress) {
    auto* mouse_event = dynamic_cast<QMouseEvent*>(event);
    if (mouse_event->button() == Qt::MiddleButton) {
      is_mouse_middle_pressed = true;
      last_mouse_pos = mouse_event->pos();
      view_->viewport()->setCursor(Qt::ClosedHandCursor);
      // 临时改变拖动模式
      view_->setDragMode(QGraphicsView::ScrollHandDrag);
      return true;
    }
    // 左键或者右键按下事件
    mouse_pos_pixel_.x = view_->mapToScene(mouse_event->pos()).x();
    mouse_pos_pixel_.y = view_->mapToScene(mouse_event->pos()).y();
    mouse_pos_meter_.x = pixel2meter(mouse_pos_pixel_.x);
    mouse_pos_meter_.y = pixel2meter(mouse_pos_pixel_.y);
    mouse_pos_grid_.x = static_cast<int>(mouse_pos_meter_.x * kGridPerMeter);
    mouse_pos_grid_.y = static_cast<int>(mouse_pos_meter_.y * kGridPerMeter);
    if (isValidMousePos(mouse_pos_pixel_)) { // 在地图范围内
      switch (draw_mode_) {
        case DrawMode::kHighGridPoint:
        case DrawMode::kLowGridPoint:
          return handlePointDrawing(mouse_event);
        case DrawMode::kHighObsLine:
        case DrawMode::kLowObsLine:
          return handleLineDrawing(mouse_event);
        case DrawMode::kHighObsCircle:
        case DrawMode::kLowObsCircle:
          return handleCircleDrawing(mouse_event);
        default:
          return false;
      }
    }
    else {
      updateStatusLabel("请在地图内绘制");
    }
  }
  else if (event->type() == QEvent::MouseButtonRelease) {
    auto* mouse_event = dynamic_cast<QMouseEvent*>(event);
    if (mouse_event->button() == Qt::MiddleButton) {
      is_mouse_middle_pressed = false;
      view_->viewport()->setCursor(Qt::ArrowCursor);
      // 恢复原来的拖动模式
      view_->setDragMode(QGraphicsView::RubberBandDrag);
      return true;
    }
  }
  else if (event->type() == QEvent::MouseMove) {
    if (is_mouse_middle_pressed) {
      auto* mouse_event = dynamic_cast<QMouseEvent*>(event);
      QPoint delta = mouse_event->pos() - last_mouse_pos;
      // 使用 translate 直接移动视图
      view_->translate(delta.x(), delta.y());
      last_mouse_pos = mouse_event->pos();
      return true;
    }
  }
  else if (event->type() == QEvent::Wheel) {
    auto* wheel_event = dynamic_cast<QWheelEvent*>(event);
    if (wheel_event->modifiers() & Qt::ControlModifier) { // 鼠标滚轮缩放 + ctrl 键
      double scaleFactor = wheel_event->angleDelta().y() > 0 ? 1.15 : 1.0 / 1.15;
      view_->scale(scaleFactor, scaleFactor);
      return true;
    }
  }

  return false;
}

bool GridMapWindow::handlePointDrawing(QMouseEvent* event) {
  QColor color = getColor(draw_mode_);
  if (draw_mode_ == DrawMode::kHighGridPoint) {
    // 左键添加，其他键删除
    if (event->button() == Qt::LeftButton) {
      grid_map_[mouse_pos_grid_.x][mouse_pos_grid_.y] = GridValue::kHighGridPoint;
    }
    else {
      grid_map_[mouse_pos_grid_.x][mouse_pos_grid_.y] = GridValue::kEmpty;
      color = getColor(DrawMode::kNone);
    }
  }
  else if (draw_mode_ == DrawMode::kLowGridPoint) {
    if (event->button() == Qt::LeftButton) {
      grid_map_[mouse_pos_grid_.x][mouse_pos_grid_.y] = GridValue::kLowGridPoint;
    }
    else {
      grid_map_[mouse_pos_grid_.x][mouse_pos_grid_.y] = GridValue::kEmpty;
      color = getColor(DrawMode::kNone);
    }
  }
  else {
    updateStatusLabel("绘制模式错误");
    return false;
  }
  drawGrid(mouse_pos_grid_, color);
  return true;
}

bool GridMapWindow::handleLineDrawing(QMouseEvent* event) {
  QColor color = getColor(draw_mode_);
  static Point2D<double> first_point; // 使用static保持状态
  if (!is_draw_second_point_) {
    first_point = mouse_pos_meter_;
    is_draw_second_point_ = true;
    drawPoint(first_point, color, 3.0);
    updateStatusLabel("请点选线段的第二个点");
  }
  else {
    drawLine(first_point, mouse_pos_meter_, color, 3.0);
    is_draw_second_point_ = false;
    updateStatusLabel("请点选线段的第一个点");
  }
  return true;
}

bool GridMapWindow::handleCircleDrawing(QMouseEvent* event) {
  static Point2D<double> circle_center; // 使用static保持状态
  QColor color = getColor(draw_mode_);
  if (!is_draw_second_point_) {
    // 画第一个点
    circle_center = mouse_pos_meter_;
    is_draw_second_point_ = true;
    drawPoint(circle_center, color, 2.0);
    updateStatusLabel("请点选圆上一点以确定半径");
  }
  else {
    // 计算半径
    auto radius = std::hypot(circle_center.x - mouse_pos_meter_.x, circle_center.y - mouse_pos_meter_.y);
    drawCircle(circle_center, radius, color);
    is_draw_second_point_ = false;
    updateStatusLabel("请点选圆心位置");
  }
  return true;
}

void GridMapWindow::saveMap() {
  QString fileName = QFileDialog::getSaveFileName(this, "保存地图", "", "地图文件 (*.map)");
  if (fileName.isEmpty())
    return;

  // 这里可以实现保存地图的逻辑
  QMessageBox::information(this, "提示", "地图保存成功！");
}

void GridMapWindow::loadMap() {
  QString fileName = QFileDialog::getOpenFileName(this, "加载地图", "", "地图文件 (*.map)");
  if (fileName.isEmpty())
    return;

  // 这里可以实现加载地图的逻辑
  QMessageBox::information(this, "提示", "地图加载成功！");
}

void GridMapWindow::drawPoint(const Point2D<double>& meter_point, const QColor& color, double pixel_size) {
  // 米 转换成 像素坐标
  double pixel_x = meter2pixel(meter_point.x);
  double pixel_y = meter2pixel(meter_point.y);
  QPen pen(Qt::NoPen); // 无边框
  QBrush brush(color); // 填充颜色
  // 画一个矩形
  scene_->addRect(
    pixel_x - pixel_size / 2.0,
    pixel_y - pixel_size / 2.0,
    pixel_size,
    pixel_size,
    pen,
    brush);
}