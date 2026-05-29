from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRectF
from PyQt6.QtGui import QPainter, QPainterPath, QColor, QPen, QBrush


class ReminderPopup(QWidget):
    dismissed = pyqtSignal()

    def __init__(self, message: str, pet_window=None, parent=None):
        super().__init__(parent)
        self.pet_window = pet_window
        self._init_ui(message)
        self._play_enter_animation()

    def _init_ui(self, message: str):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(240, 100)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(12)

        msg_label = QLabel(message)
        msg_label.setStyleSheet("""
            QLabel {
                color: #1a1a1a;
                font-size: 13px;
                font-weight: 500;
                background: transparent;
                border: none;
            }
        """)
        msg_label.setWordWrap(True)
        layout.addWidget(msg_label)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        ok_btn = QPushButton("收到")
        ok_btn.setFixedSize(64, 32)
        ok_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F09850, stop:1 #E87A2D);
                color: white; border: none; border-radius: 10px;
                padding: 8px 16px; font-size: 13px; font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E87A2D, stop:1 #C85A1A);
            }
        """)
        ok_btn.clicked.connect(self._on_ok_clicked)
        btn_layout.addWidget(ok_btn)

        layout.addLayout(btn_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        rect = QRectF(0, 0, self.width(), self.height())
        path.addRoundedRect(rect, 16, 16)
        painter.setClipPath(path)
        painter.fillPath(path, QBrush(QColor(255, 255, 255, 235)))
        pen = QPen(QColor(0, 0, 0, 25))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRoundedRect(rect.adjusted(0.5, 0.5, -0.5, -0.5), 16, 16)
        painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        self._disable_dwm_shadow()
        self._position_near_pet()

    def _disable_dwm_shadow(self):
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
        try:
            if self.pet_window:
                pet_pos = self.pet_window.pos()
                pet_size = self.pet_window.size()
                screen = QApplication.primaryScreen()
                if screen:
                    screen_rect = screen.geometry()
                    x = pet_pos.x() + (pet_size.width() - self.width()) // 2
                    y = pet_pos.y() - self.height() - 12

                    if x < 20:
                        x = 20
                    if x + self.width() > screen_rect.width() - 20:
                        x = screen_rect.width() - self.width() - 20
                    if y < 20:
                        y = pet_pos.y() + pet_size.height() + 12

                    self.move(x, y)
        except Exception:
            pass

    def _play_enter_animation(self):
        self._fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_anim.setDuration(250)
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._fade_anim.start()

    def _close_with_animation(self):
        self._fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_anim.setDuration(200)
        self._fade_anim.setStartValue(1.0)
        self._fade_anim.setEndValue(0.0)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self._fade_anim.finished.connect(self._emit_dismissed)
        self._fade_anim.start()

    def _on_ok_clicked(self):
        self._close_with_animation()

    def _emit_dismissed(self):
        self.dismissed.emit()
        self.close()
