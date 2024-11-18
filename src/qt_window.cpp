#include "qt_window.h"
#include <QFileDialog>
#include <QHBoxLayout>
#include <QMessageBox>
#include <QMouseEvent>
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
  setWindowFlags(windowFlags() & ~Qt::WindowMaximizeButtonHint); // 禁止最大化按钮
  int window_width = kMapWidth * kCellPixel;
  int window_height = kMapHeight * kCellPixel + 40; // 额外40像素用于菜单栏
  setFixedSize(window_width, window_height);

  // 创建主布局
  vbox_layout_ = std::make_unique<QVBoxLayout>(this);

  // Scene(场景)相关设置
  scene_ = std::make_unique<QGraphicsScene>(this);
  scene_->setSceneRect(0, 0, kMapWidth * kCellPixel, kMapHeight * kCellPixel); // 设置场景固定大小
  scene_->setBackgroundBrush(GridColors::kDark);                               // 设置黑色背景

  // View(视图)相关设置
  view_ = std::make_unique<QGraphicsView>(scene_.get());
  // 滚动条设置
  view_->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
  view_->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
  // 渲染设置
  view_->setViewportUpdateMode(QGraphicsView::FullViewportUpdate);
  view_->setRenderHint(QPainter::Antialiasing); // 抗锯齿
  // 交互设置
  view_->setDragMode(QGraphicsView::RubberBandDrag);               // 允许框选
  view_->setTransformationAnchor(QGraphicsView::AnchorUnderMouse); // 缩放以鼠标位置为中心

  // 初始化网格数据
  grid_map_.resize(kMapHeight, std::vector<GridValue>(kMapWidth, GridValue::kEmpty));

  // 初始化UI组件
  initializeGrid();
  createMenu();

  // 事件处理设置
  view_->viewport()->installEventFilter(this);
  vbox_layout_->addWidget(view_.get());

  // 创建状态栏
  status_label_ = std::make_unique<QLabel>("准备就绪...");
  vbox_layout_->addWidget(status_label_.get());

  // 确保视图在初始化时完整显示整个场景
  QTimer::singleShot(0, [this]() {
    view_->fitInView(scene_->sceneRect(), Qt::KeepAspectRatio);
  });
}

void GridMapWindow::initializeGrid() {
  // 使用两种不同的画笔
  QPen major_pen(GridColors::kLightGray);
  major_pen.setWidthF(1.0); // 使用setWidthF设置精确的1像素宽度

  QPen minor_pen(GridColors::kDarkGray);
  minor_pen.setWidthF(1.0); // 使用setWidthF设置精确的1像素宽度

  // 绘制垂直线
  for (int x = 0; x <= kMapWidth; ++x) {
    if (x % kGridPerMeter == 0) { // 每米(10格)画一条主线
      scene_->addLine(x * kCellPixel, 0, x * kCellPixel, kMapHeight * kCellPixel, major_pen);
    }
    else { // 其他位置画次要线
      scene_->addLine(x * kCellPixel, 0, x * kCellPixel, kMapHeight * kCellPixel, minor_pen);
    }
  }

  // 绘制水平线
  for (int y = 0; y <= kMapHeight; ++y) {
    if (y % kGridPerMeter == 0) { // 每米(10格)画一条主线
      scene_->addLine(0, y * kCellPixel, kMapWidth * kCellPixel, y * kCellPixel, major_pen);
    }
    else { // 其他位置画次要线
      scene_->addLine(0, y * kCellPixel, kMapWidth * kCellPixel, y * kCellPixel, minor_pen);
    }
  }

  // 设置场景大小
  scene_->setSceneRect(0, 0, kMapWidth * kCellPixel, kMapHeight * kCellPixel);

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

const QColor& GridMapWindow::setColor(GridValue grid_value) {
  switch (grid_value) {
    case GridValue::kEmpty:
      return GridColors::kDark;
    case GridValue::kHighGridPoint:
      return GridColors::kDarkGreen;
    case GridValue::kLowGridPoint:
      return GridColors::kBlue;
    case GridValue::kHighObsLine:
      return GridColors::kGreen;
    case GridValue::kLowObsLine:
      return GridColors::kBlue;
    case GridValue::kHighObsCircle:
      return GridColors::kMagenta;
    case GridValue::kLowObsCircle:
      return GridColors::kBlue;
    default:
      return GridColors::kDarkGreen;
  }
}

void GridMapWindow::setDrawMode(DrawMode mode) {
  // 设置绘图模式
  draw_mode_ = mode;
  wait_second_point_ = false;
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
  QPen pen(Qt::transparent, 0);
  scene_->addRect(
    grid_point.x * kCellPixel + 0.5,
    grid_point.y * kCellPixel + 0.5,
    kCellPixel - 1.0,
    kCellPixel - 1.0,
    pen,
    color);
}

void GridMapWindow::drawLine(const Point2D<double>& start, const Point2D<double>& end, const QColor& color) {
  // 每隔0.2m画一个点
  // 计算直线的方向向量
  double dx = end.x - start.x;
  double dy = end.y - start.y;
  double length = std::sqrt(dx * dx + dy * dy);

  // 归一化方向向量
  dx /= length;
  dy /= length;

  // 每0.2米(2个格子)画一个点
  double current_dist = 0.0;
  while (current_dist <= length) {
    Point2D<double> current_point{start.x + dx * current_dist, start.y + dy * current_dist};
    drawPoint(current_point, color);
    current_dist += 0.2;
  }
  // 确保终点被画上
  drawPoint(end, color);
}

void GridMapWindow::drawCircle(const Point2D<double>& circle_center, double radius, const QColor& color) {
  // 米 转换成 像素坐标
  auto scene_x = circle_center.x * kGridPerMeter * kCellPixel;
  auto scene_y = circle_center.y * kGridPerMeter * kCellPixel;
  auto scene_radius = radius * kGridPerMeter * kCellPixel;
  // 画一个圆
  scene_->addEllipse(scene_x - scene_radius, scene_y - scene_radius, 2 * scene_radius, 2 * scene_radius, QPen(Qt::NoPen), QBrush(color));
}

void GridMapWindow::updateStatusLabel(const QString& message) {
  if (status_label_) {
    status_label_->setText(message);
  }
}

bool GridMapWindow::isValidMousePos(const QPointF& mouse_pos_pixel) {
  auto max_mouse_x = kMapWidth * kCellPixel;
  auto max_mouse_y = kMapHeight * kCellPixel;
  return mouse_pos_pixel.x() > 0 && mouse_pos_pixel.x() < max_mouse_x &&
         mouse_pos_pixel.y() > 0 && mouse_pos_pixel.y() < max_mouse_y;
}

void GridMapWindow::clearCurrentDrawing() {
  wait_second_point_ = false;
  updateStatusLabel("绘制已取消");
}

void GridMapWindow::clearMap() {
  scene_->clear();
  initializeGrid();
  grid_map_ = std::vector<std::vector<GridValue>>(
    kMapHeight, std::vector<GridValue>(kMapWidth, GridValue::kEmpty));
  updateStatusLabel("地图已清空");
}

bool GridMapWindow::eventFilter(QObject* obj, QEvent* event) {
  if (obj == view_->viewport()) {
    if (event->type() == QEvent::MouseButtonPress) {
      auto* mouse_event = dynamic_cast<QMouseEvent*>(event);
      mouse_pos_pixel_ = view_->mapToScene(mouse_event->pos());
      if (isValidMousePos(mouse_pos_pixel_)) {
        mouse_pos_grid_.x = static_cast<int>(mouse_pos_pixel_.x() / kCellPixel);
        mouse_pos_grid_.y = static_cast<int>(mouse_pos_pixel_.y() / kCellPixel);
        mouse_pos_meter_.x = mouse_pos_grid_.x * kMeterPerCell;
        mouse_pos_meter_.y = mouse_pos_grid_.y * kMeterPerCell;
        switch (draw_mode_) {
        case DrawMode::kHighGridPoint:
          return handlePointDrawing(mouse_event, setColor(GridValue::kHighGridPoint));
        case DrawMode::kLowGridPoint:
          return handlePointDrawing(mouse_event, setColor(GridValue::kLowGridPoint));
        case DrawMode::kHighObsLine:
          return handleLineDrawing(mouse_event, setColor(GridValue::kHighObsLine));
        case DrawMode::kLowObsLine:
          return handleLineDrawing(mouse_event, setColor(GridValue::kLowObsLine));
        case DrawMode::kHighObsCircle:
          return handleCircleDrawing(mouse_event, setColor(GridValue::kHighObsCircle));
        case DrawMode::kLowObsCircle:
          return handleCircleDrawing(mouse_event, setColor(GridValue::kLowObsCircle));
          // todo ... 其他模式的处理
        }
      }
      else {
        updateStatusLabel("请在地图范围内绘制");
      }
    }
    else if (event->type() == QEvent::Wheel) {
      auto* wheelEvent = dynamic_cast<QWheelEvent*>(event);
      if (wheelEvent->modifiers() & Qt::ControlModifier) {
        double scaleFactor = wheelEvent->angleDelta().y() > 0 ? 1.15 : 1.0 / 1.15;
        view_->scale(scaleFactor, scaleFactor);
        return true;
      }
    }
  }
  return QWidget::eventFilter(obj, event);
}

bool GridMapWindow::handlePointDrawing(QMouseEvent* event, const QColor& input_color) {
  const auto& grid_point = mouse_pos_grid_;
  auto current_color = setColor(grid_map_[grid_point.y][grid_point.x]);
  if (current_color == input_color) {
    // 当前格子的颜色与输入颜色相同，则画空
    drawGrid(grid_point, setColor(GridValue::kEmpty));
  }
  else {
    drawGrid(grid_point, input_color);
  }
  return true;
}

bool GridMapWindow::handleLineDrawing(QMouseEvent* event, const QColor& color) {
  static Point2D<double> first_point; // 使用static保持状态
  if (!wait_second_point_) {
    first_point = mouse_pos_meter_;
    wait_second_point_ = true;
    updateStatusLabel("请点选线段的第二个点");
  }
  else {
    drawLine(first_point, mouse_pos_meter_, color);
    wait_second_point_ = false;
    updateStatusLabel("请点选线段的第一个点");
  }

  return true;
}

bool GridMapWindow::handleCircleDrawing(QMouseEvent* event, const QColor& color) {
  static Point2D<double> circle_center; // 使用static保持状态
  auto mouse_pos = view_->mapToScene(event->pos());
  Point2D<double> mouse_point{mouse_pos.x(), mouse_pos.y()};
  if (isValidMousePos(mouse_pos)) {
    if (!wait_second_point_) {
      // 画第一个点
      circle_center = mouse_point;
      wait_second_point_ = true;
      drawPoint(circle_center, color);
      updateStatusLabel("请点选圆上一点以确定半径");
    }
    else {
      // 计算半径
      auto radius = std::hypot(circle_center.x - mouse_point.x, circle_center.y - mouse_point.y);
      drawCircle(circle_center, radius, color);
      wait_second_point_ = false;
      updateStatusLabel("请点选圆心位置");
    }
  } else {
    updateStatusLabel("请在地图范围内绘制");
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

void GridMapWindow::drawPoint(const Point2D<double>& meter_point, const QColor& color) {
  // 米 转换成 像素坐标
  double scene_x = meter_point.x * kGridPerMeter * kCellPixel;
  double scene_y = meter_point.y * kGridPerMeter * kCellPixel;
  // 创建一个实心圆
  scene_->addEllipse(
    scene_x - kCellPixel / 2.0, // x坐标（左上角）
    scene_y - kCellPixel / 2.0, // y坐标（左上角）
    kCellPixel,                 // 宽度
    kCellPixel,                 // 高度
    QPen(Qt::NoPen),          // 无边框
    QBrush(color)           // 填充颜色
  );
}