import json
import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QLabel, QFrame, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QRectF
from PyQt6.QtGui import QFont, QColor, QPainter, QPainterPath, QBrush, QPen, QRegion


class ChatWorker(QThread):
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, api_base, api_key, model, messages):
        super().__init__()
        self.api_base = api_base
        self.api_key = api_key
        self.model = model
        self.messages = messages

    def run(self):
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": self.model,
                "messages": self.messages,
                "max_tokens": 1024,
                "temperature": 0.7,
            }
            resp = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            self.response_ready.emit(content)
        except Exception as e:
            self.error_occurred.emit(str(e))


class ChatWindow(QWidget):
    def __init__(self, config: dict, pet_window=None, parent=None):
        super().__init__(parent)
        self.config = config
        self.pet_window = pet_window
        self.messages = [
            {"role": "system", "content": "你是 Claude，一个友好、有帮助的 AI 助手。请用中文回复。"}
        ]
        self._worker = None
        self._drag_pos = None
        self._init_ui()

    def _init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(380, 500)

        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 内容容器
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(12)

        # 标题栏
        header = QHBoxLayout()
        header.setSpacing(12)

        icon_label = QLabel("💬")
        icon_label.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        header.addWidget(icon_label)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)

        title = QLabel("Chat")
        title.setStyleSheet("color: #1a1a1a; font-size: 18px; font-weight: 600; border: none; background: transparent;")
        title_layout.addWidget(title)

        subtitle = QLabel("与 Claude 对话")
        subtitle.setStyleSheet("color: #6b6b6b; font-size: 12px; border: none; background: transparent;")
        title_layout.addWidget(subtitle)

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

        # 聊天区域
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.50);
                border: 1.5px solid rgba(0, 0, 0, 0.06);
                border-radius: 14px;
                padding: 12px;
                font-size: 13px;
                color: #1a1a1a;
            }
            QScrollBar:vertical { background: transparent; width: 6px; }
            QScrollBar::handle:vertical { background: rgba(0,0,0,0.15); border-radius: 3px; min-height: 30px; }
            QScrollBar::handle:vertical:hover { background: rgba(0,0,0,0.25); }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)
        content_layout.addWidget(self.chat_display)

        # 输入区域容器
        input_container = QWidget()
        input_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.50);
                border: 1.5px solid rgba(0, 0, 0, 0.08);
                border-radius: 16px;
            }
        """)
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(6, 6, 6, 6)
        input_layout.setSpacing(8)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入消息...")
        self.input_field.setStyleSheet("""
            QLineEdit { background: transparent; border: none; color: #1a1a1a; font-size: 13px; padding: 8px 10px; }
            QLineEdit::placeholder { color: #9a9a9a; }
        """)
        self.input_field.returnPressed.connect(self._send)
        input_layout.addWidget(self.input_field)

        self.send_btn = QPushButton("→")
        self.send_btn.setFixedSize(40, 40)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background: #E87A2D; color: white; border: none; border-radius: 12px;
                font-size: 18px; font-weight: 600;
            }
            QPushButton:hover { background: #C85A1A; }
            QPushButton:disabled { background: rgba(0,0,0,0.1); color: #9a9a9a; }
        """)
        self.send_btn.clicked.connect(self._send)
        input_layout.addWidget(self.send_btn)

        content_layout.addWidget(input_container)

        # 状态栏
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #9a9a9a; font-size: 11px; border: none; background: transparent;")
        content_layout.addWidget(self.status_label)

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
                    x = pet_pos.x() + pet_size.width() + 16
                    y = pet_pos.y() - 40

                    if x + self.width() > screen_rect.width() - 20:
                        x = pet_pos.x() - self.width() - 16

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

    def _send(self):
        text = self.input_field.text().strip()
        if not text:
            return

        self.input_field.clear()
        self._append_message("user", text)
        self.messages.append({"role": "user", "content": text})

        api_key = self.config.get("api_key", "")
        if not api_key:
            self._append_message("system", "请先在设置中配置 API Key")
            return

        self.send_btn.setEnabled(False)
        self.status_label.setText("思考中...")

        self._worker = ChatWorker(
            self.config.get("api_base_url", "https://api.deepseek.com/v1"),
            api_key,
            self.config.get("model", "deepseek-chat"),
            self.messages,
        )
        self._worker.response_ready.connect(self._on_response)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.start()

    def _on_response(self, text: str):
        self.messages.append({"role": "assistant", "content": text})
        self._append_message("assistant", text)
        self.send_btn.setEnabled(True)
        self.status_label.setText("就绪")

    def _on_error(self, err: str):
        self._append_message("system", f"错误: {err}")
        self.send_btn.setEnabled(True)
        self.status_label.setText("出错了")

    def _append_message(self, role: str, text: str):
        if role == "user":
            bubble_style = "background: rgba(232, 122, 45, 0.08); border-radius: 16px 16px 4px 16px; padding: 12px 16px; margin: 2px 0 6px 80px;"
            name_style = "color: #E87A2D; font-size: 11px; font-weight: 600; margin: 8px 4px 2px 0; text-align: right;"
            name = "你"
        elif role == "system":
            bubble_style = "background: rgba(255, 59, 48, 0.06); border-radius: 12px; padding: 10px 14px; margin: 6px 20px;"
            name_style = "color: #FF3B30; font-size: 11px; font-weight: 600; margin: 8px 20px 2px; text-align: center;"
            name = "系统"
        else:
            bubble_style = "background: rgba(245, 245, 245, 0.8); border: 1px solid rgba(0, 0, 0, 0.04); border-radius: 16px 16px 16px 4px; padding: 12px 16px; margin: 2px 80px 6px 0;"
            name_style = "color: #6b6b6b; font-size: 11px; font-weight: 600; margin: 8px 0 2px 4px; text-align: left;"
            name = "Claude"

        self.chat_display.append(
            f'''<div style="{name_style}">{name}</div>
            <div style="{bubble_style}">
                <div style="color: #1a1a1a; font-size: 13px; line-height: 1.5;">{text}</div>
            </div>'''
        )
        sb = self.chat_display.verticalScrollBar()
        sb.setValue(sb.maximum())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
