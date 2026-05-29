from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QLabel,
    QCheckBox, QComboBox, QDateEdit, QApplication, QFrame,
    QHeaderView
)
from PyQt6.QtCore import Qt, QDate, QLocale, pyqtSignal, QPropertyAnimation, QEasingCurve, QRectF
from PyQt6.QtGui import QFont, QColor, QPainter, QPainterPath, QBrush, QPen, QRegion
from core.todo_manager import TodoManager


class TodoPanel(QWidget):
    def __init__(self, todo_manager: TodoManager, pet_window=None, parent=None):
        super().__init__(parent)
        self.todo_manager = todo_manager
        self.pet_window = pet_window
        self._drag_pos = None
        self._init_ui()
        self._connect_signals()
        self._refresh_list()

    def _init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(360, 520)

        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 内容容器
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(14)

        # 标题栏
        header = QHBoxLayout()
        header.setSpacing(12)

        icon_label = QLabel("\U0001f4cb")
        icon_label.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        header.addWidget(icon_label)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)

        title = QLabel("待办事项")
        title.setStyleSheet("color: #1a1a1a; font-size: 18px; font-weight: 600; border: none; background: transparent;")
        title_layout.addWidget(title)

        self.count_label = QLabel("共 0 项")
        self.count_label.setStyleSheet("color: #6b6b6b; font-size: 12px; border: none; background: transparent;")
        title_layout.addWidget(self.count_label)

        header.addLayout(title_layout)
        header.addStretch()

        close_btn = QPushButton("×")
        close_btn.setFixedSize(32, 32)
        close_btn.setStyleSheet("""
            QPushButton {
                color: #9a9a9a; background: transparent; border: none;
                font-size: 18px; border-radius: 10px; min-width: 28px; min-height: 28px;
            }
            QPushButton:hover { background: rgba(255, 59, 48, 0.1); color: #FF3B30; }
        """)
        close_btn.clicked.connect(self._close_with_animation)
        header.addWidget(close_btn)

        content_layout.addLayout(header)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background: rgba(0, 0, 0, 0.06); max-height: 1px;")
        content_layout.addWidget(separator)

        # 添加任务区域
        add_card = QWidget()
        add_card.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.50);
                border: 1px solid rgba(0, 0, 0, 0.06);
                border-radius: 14px;
            }
        """)
        add_layout = QVBoxLayout(add_card)
        add_layout.setContentsMargins(14, 12, 14, 12)
        add_layout.setSpacing(10)

        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("添加新任务...")
        self.task_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.50);
                border: 1.5px solid rgba(0, 0, 0, 0.08);
                border-radius: 10px; padding: 8px 12px; font-size: 13px; color: #1a1a1a;
            }
            QLineEdit:focus { border-color: #E87A2D; }
        """)
        input_row.addWidget(self.task_input)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["普通", "重要", "紧急"])
        self.priority_combo.setFixedWidth(80)
        self.priority_combo.setStyleSheet("""
            QComboBox {
                background: rgba(255, 255, 255, 0.50);
                border: 1.5px solid rgba(0, 0, 0, 0.08);
                border-radius: 10px; padding: 8px 12px; font-size: 13px; color: #1a1a1a;
            }
            QComboBox:focus { border-color: #E87A2D; }
            QComboBox::drop-down { border: none; width: 24px; }
            QComboBox::down-arrow { image: none; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 6px solid #9a9a9a; margin-right: 6px; }
            QComboBox QAbstractItemView {
                background: rgba(255, 255, 255, 0.95); border: 1px solid rgba(0, 0, 0, 0.08);
                border-radius: 10px; padding: 4px; outline: none;
            }
            QComboBox QAbstractItemView::item { padding: 8px 12px; border-radius: 6px; min-height: 24px; }
            QComboBox QAbstractItemView::item:selected { background: rgba(232, 122, 45, 0.1); }
        """)
        input_row.addWidget(self.priority_combo)

        add_layout.addLayout(input_row)

        date_row = QHBoxLayout()
        date_row.setSpacing(10)

        self.due_check = QCheckBox("截止日期")
        self.due_check.setStyleSheet("""
            QCheckBox { color: #1a1a1a; font-size: 13px; spacing: 10px; border: none; background: transparent; }
            QCheckBox::indicator { width: 18px; height: 18px; border: 2px solid rgba(0,0,0,0.15); border-radius: 5px; background: rgba(255,255,255,0.5); }
            QCheckBox::indicator:checked { background: #E87A2D; border-color: #E87A2D; }
        """)
        date_row.addWidget(self.due_check)

        self.due_date = QDateEdit()
        self.due_date.setCalendarPopup(True)
        self.due_date.setDate(QDate.currentDate().addDays(1))
        self.due_date.setDisplayFormat("MM-dd")
        self.due_date.setFixedWidth(100)
        self.due_date.setStyleSheet("""
            QDateEdit {
                background: rgba(255, 255, 255, 0.50);
                border: 1.5px solid rgba(0, 0, 0, 0.08);
                border-radius: 10px; padding: 8px 12px; font-size: 13px; color: #1a1a1a;
            }
            QDateEdit:focus { border-color: #E87A2D; }
            QDateEdit::drop-down { border: none; width: 24px; }
            QDateEdit::down-arrow { image: none; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 6px solid #9a9a9a; margin-right: 6px; }
        """)
        # 日历弹出框白色主题
        self.due_date.calendarWidget().setStyleSheet("""
            QCalendarWidget {
                background: white;
                border: 1px solid rgba(0, 0, 0, 0.08);
                border-radius: 12px;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background: rgba(245, 245, 245, 0.95);
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                padding: 6px;
            }
            QCalendarWidget QToolButton {
                color: #1a1a1a;
                background: transparent;
                border: none;
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 13px;
                font-weight: 600;
            }
            QCalendarWidget QToolButton:hover {
                background: rgba(0, 0, 0, 0.05);
            }
            QCalendarWidget QMenu {
                background: white;
                border: 1px solid rgba(0, 0, 0, 0.08);
                border-radius: 8px;
                padding: 4px;
            }
            QCalendarWidget QMenu::item {
                padding: 6px 16px;
                border-radius: 4px;
            }
            QCalendarWidget QMenu::item:selected {
                background: rgba(232, 122, 45, 0.1);
            }
            QCalendarWidget QAbstractItemView {
                background: white;
                border: none;
                outline: none;
                font-size: 12px;
            }
            QCalendarWidget QAbstractItemView::item {
                padding: 4px;
                color: #1a1a1a;
            }
            QCalendarWidget QAbstractItemView::item:selected {
                background: #E87A2D;
                color: white;
                border-radius: 4px;
            }
            QCalendarWidget QAbstractItemView::item:hover {
                background: rgba(232, 122, 45, 0.08);
                border-radius: 4px;
            }
            QCalendarWidget QSpinBox {
                background: white;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 4px;
                padding: 2px 4px;
                color: #1a1a1a;
            }
            QCalendarWidget QAbstractItemView QTableCornerButton::section {
                background: rgba(245, 245, 245, 0.95);
                border: none;
            }
            QCalendarWidget QHeaderView::section {
                background: rgba(245, 245, 245, 0.95);
                color: #1a1a1a;
                font-size: 12px;
                font-weight: 600;
                padding: 4px;
                border: none;
                border-bottom: 1px solid rgba(0, 0, 0, 0.06);
            }
        """)
        # 设置中文星期显示
        self.due_date.calendarWidget().setLocale(QLocale("zh_CN"))
        date_row.addWidget(self.due_date)

        date_row.addStretch()

        add_btn = QPushButton("添加")
        add_btn.setFixedSize(64, 36)
        add_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F09850, stop:1 #E87A2D);
                color: white; border: none; border-radius: 12px;
                padding: 10px 20px; font-size: 13px; font-weight: 600;
            }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E87A2D, stop:1 #C85A1A); }
        """)
        add_btn.clicked.connect(self._add_task)
        date_row.addWidget(add_btn)

        add_layout.addLayout(date_row)

        content_layout.addWidget(add_card)

        # 任务列表
        self.todo_list = QListWidget()
        self.todo_list.setStyleSheet("""
            QListWidget {
                background: rgba(255, 255, 255, 0.50);
                border: 1.5px solid rgba(0, 0, 0, 0.06);
                border-radius: 14px;
                padding: 6px;
                outline: none;
            }
            QListWidget::item { padding: 12px 14px; border-radius: 10px; margin: 2px 0; border: none; font-size: 14px; font-weight: 500; }
            QListWidget::item:selected { background: rgba(232, 122, 45, 0.15); color: #1a1a1a; }
            QListWidget::item:selected:hover { background: rgba(232, 122, 45, 0.2); }
            QListWidget::item:hover { background: rgba(0, 0, 0, 0.03); }
            QScrollBar:vertical { background: transparent; width: 6px; }
            QScrollBar::handle:vertical { background: rgba(0,0,0,0.15); border-radius: 3px; min-height: 30px; }
            QScrollBar::handle:vertical:hover { background: rgba(0,0,0,0.25); }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)
        content_layout.addWidget(self.todo_list)

        # 操作按钮
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.done_btn = QPushButton("✓ 完成选中")
        self.done_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.7); color: #1a1a1a;
                border: 1.5px solid rgba(0,0,0,0.1); border-radius: 12px;
                padding: 10px 20px; font-size: 13px; font-weight: 500;
            }
            QPushButton:hover { background: rgba(255,255,255,0.9); }
        """)
        self.done_btn.clicked.connect(self._toggle_selected)
        btn_row.addWidget(self.done_btn)

        self.del_btn = QPushButton("删除")
        self.del_btn.setStyleSheet("""
            QPushButton {
                background: transparent; color: #FF3B30;
                border: 1.5px solid rgba(255,59,48,0.3); border-radius: 12px;
                padding: 10px 20px; font-size: 13px; font-weight: 500;
            }
            QPushButton:hover { background: rgba(255,59,48,0.06); border-color: rgba(255,59,48,0.5); }
        """)
        self.del_btn.clicked.connect(self._delete_selected)
        btn_row.addWidget(self.del_btn)

        content_layout.addLayout(btn_row)

        layout.addWidget(content)

    def paintEvent(self, event):
        """绘制圆角毛玻璃背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        rect = QRectF(0, 0, self.width(), self.height())
        path.addRoundedRect(rect, 20, 20)
        painter.setClipPath(path)
        painter.fillPath(path, QBrush(QColor(255, 255, 255, 230)))
        pen = QPen(QColor(0, 0, 0, 30))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRoundedRect(rect.adjusted(0.5, 0.5, -0.5, -0.5), 20, 20)
        painter.end()

    def _disable_dwm_shadow(self):
        """用 DwmExtendFrameIntoClientArea 将 DWM 阴影推到窗口外部"""
        try:
            import ctypes
            hwnd = int(self.winId())

            class MARGINS(ctypes.Structure):
                _fields_ = [("cxLeftWidth", ctypes.c_int), ("cxRightWidth", ctypes.c_int),
                             ("cyTopHeight", ctypes.c_int), ("cyBottomHeight", ctypes.c_int)]

            margins = MARGINS(-1, -1, -1, -1)
            ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))
        except Exception:
            pass

    def _position_near_pet(self):
        """在桌宠旁边显示"""
        try:
            if self.pet_window:
                pet_pos = self.pet_window.pos()
                pet_size = self.pet_window.size()
                screen = QApplication.primaryScreen()
                if screen:
                    screen_rect = screen.geometry()
                    x = pet_pos.x() - self.width() - 16
                    y = pet_pos.y() - 40

                    if x < 20:
                        x = pet_pos.x() + pet_size.width() + 16

                    if y < 20:
                        y = 20
                    if y + self.height() > screen_rect.height() - 20:
                        y = screen_rect.height() - self.height() - 20

                    self.move(x, y)
        except Exception:
            pass

    def showEvent(self, event):
        """显示时播放淡入动画"""
        super().showEvent(event)
        self._disable_dwm_shadow()
        self._position_near_pet()
        self._play_enter_animation()

    def _play_enter_animation(self):
        """播放进入动画"""
        self._fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_anim.setDuration(250)
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._fade_anim.start()

    def _close_with_animation(self):
        """播放关闭动画"""
        self._fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_anim.setDuration(200)
        self._fade_anim.setStartValue(1.0)
        self._fade_anim.setEndValue(0.0)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self._fade_anim.finished.connect(self.close)
        self._fade_anim.start()

    def _connect_signals(self):
        self.task_input.returnPressed.connect(self._add_task)
        self.todo_manager.todo_added.connect(lambda _: self._refresh_list())
        self.todo_manager.todo_updated.connect(lambda _: self._refresh_list())
        self.todo_manager.todo_deleted.connect(lambda _: self._refresh_list())

    def _add_task(self):
        title = self.task_input.text().strip()
        if not title:
            return
        priority_map = {"普通": "normal", "重要": "important", "紧急": "urgent"}
        priority = priority_map.get(self.priority_combo.currentText(), "normal")
        due = ""
        if self.due_check.isChecked():
            due = self.due_date.date().toString("yyyy-MM-dd") + " 09:00"
        self.todo_manager.add(title, due, priority)
        self.task_input.clear()

    def _sort_key(self, t):
        done = t.get("done", False)
        due = t.get("due", "")
        priority_rank = {"urgent": 0, "important": 1, "normal": 2}.get(t.get("priority", "normal"), 2)
        # 没有截止日期的排在有日期的后面，用一个很远的日期兜底
        if not due:
            due = "9999-12-31 23:59"
        # 已完成的放最后
        return (done, due, priority_rank)

    def _refresh_list(self):
        self.todo_list.clear()
        sorted_todos = sorted(self.todo_manager.todos, key=self._sort_key)
        for t in sorted_todos:
            status = "✓" if t["done"] else "○"
            priority_color = {
                "urgent": "#FF3B30",
                "important": "#FF9500"
            }.get(t.get("priority", "normal"), "#3a3a3a")
            due_str = f'  ·  {t["due"][:10]}' if t.get("due") else ""

            text = f'{status}  {t["title"]}{due_str}'
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, t["id"])

            if t["done"]:
                item.setForeground(QColor("#9a9a9a"))
                font = item.font()
                font.setStrikeOut(True)
                item.setFont(font)
            else:
                item.setForeground(QColor(priority_color))

            self.todo_list.addItem(item)

        total = len(self.todo_manager.todos)
        pending = len(self.todo_manager.get_pending())
        self.count_label.setText(f"共 {total} 项 · 待办 {pending} 项")

    def _get_selected_id(self) -> str:
        item = self.todo_list.currentItem()
        if item:
            return item.data(Qt.ItemDataRole.UserRole)
        return ""

    def _toggle_selected(self):
        tid = self._get_selected_id()
        if tid:
            self.todo_manager.toggle(tid)

    def _delete_selected(self):
        tid = self._get_selected_id()
        if tid:
            self.todo_manager.delete(tid)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
