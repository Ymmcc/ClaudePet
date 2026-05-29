from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QCheckBox, QPushButton,
    QLabel, QApplication, QFrame, QWidget
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRectF
from PyQt6.QtGui import QFont, QColor, QPainter, QPainterPath, QBrush, QPen, QRegion
from utils.config import save_config
from utils.autostart import is_autostart_enabled, enable_autostart, disable_autostart


class SettingsDialog(QDialog):
    def __init__(self, config: dict, pet_window=None, parent=None):
        super().__init__(parent)
        self.config = config
        self.pet_window = pet_window
        self._drag_pos = None
        self._init_ui()

    def _init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(420, 660)

        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 内容容器
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 16, 24, 16)
        content_layout.setSpacing(10)

        # 标题栏
        header = QHBoxLayout()
        header.setSpacing(12)

        icon_label = QLabel("⚙️")
        icon_label.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        header.addWidget(icon_label)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)

        title = QLabel("设置")
        title.setStyleSheet("color: #1a1a1a; font-size: 18px; font-weight: 600; border: none; background: transparent;")
        title_layout.addWidget(title)

        subtitle = QLabel("自定义你的桌宠")
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
        close_btn.clicked.connect(self.close)
        header.addWidget(close_btn)

        content_layout.addLayout(header)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background: rgba(0, 0, 0, 0.06); max-height: 1px;")
        content_layout.addWidget(separator)

        # 常规设置
        general_label = QLabel("常规设置")
        general_label.setStyleSheet("color: #6b6b6b; font-size: 11px; font-weight: 600; letter-spacing: 1px; border: none; background: transparent;")
        content_layout.addWidget(general_label)

        general_card = QWidget()
        general_card.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.50);
                border: 1px solid rgba(0, 0, 0, 0.06);
                border-radius: 14px;
            }
        """)
        general_form = QFormLayout(general_card)
        general_form.setContentsMargins(16, 10, 16, 10)
        general_form.setSpacing(8)
        general_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        general_form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.pet_name_input = QLineEdit(self.config.get("pet_name", "Claude"))
        self.pet_name_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.50);
                border: 1.5px solid rgba(0, 0, 0, 0.08);
                border-radius: 10px; padding: 8px 12px; font-size: 13px; color: #1a1a1a;
            }
            QLineEdit:focus { border-color: #E87A2D; }
        """)
        name_label = QLabel("名称")
        name_label.setMinimumWidth(48)
        name_label.setStyleSheet("color: #6b6b6b; font-size: 13px; border: none; background: transparent;")
        general_form.addRow(name_label, self.pet_name_input)

        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["慢速", "正常", "快速"])
        speed_map = {150: 0, 100: 1, 60: 2}
        self.speed_combo.setCurrentIndex(speed_map.get(self.config.get("animation_speed", 100), 1))
        self.speed_combo.setStyleSheet("""
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
        speed_label = QLabel("速度")
        speed_label.setMinimumWidth(48)
        speed_label.setStyleSheet("color: #6b6b6b; font-size: 13px; border: none; background: transparent;")
        general_form.addRow(speed_label, self.speed_combo)

        self.autostart_check = QCheckBox("开机自启动")
        self.autostart_check.setChecked(is_autostart_enabled())
        self.autostart_check.setStyleSheet("""
            QCheckBox { color: #1a1a1a; font-size: 13px; spacing: 10px; border: none; background: transparent; }
            QCheckBox::indicator { width: 18px; height: 18px; border: 2px solid rgba(0,0,0,0.15); border-radius: 5px; background: rgba(255,255,255,0.5); }
            QCheckBox::indicator:checked { background: #E87A2D; border-color: #E87A2D; }
        """)
        general_form.addRow(self.autostart_check)

        content_layout.addWidget(general_card)

        # API 设置
        api_label = QLabel("AI API")
        api_label.setStyleSheet("color: #6b6b6b; font-size: 11px; font-weight: 600; letter-spacing: 1px; border: none; background: transparent;")
        content_layout.addWidget(api_label)

        api_card = QWidget()
        api_card.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.50);
                border: 1px solid rgba(0, 0, 0, 0.06);
                border-radius: 14px;
            }
        """)
        api_form = QFormLayout(api_card)
        api_form.setContentsMargins(16, 10, 16, 10)
        api_form.setSpacing(8)
        api_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        api_form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["DeepSeek", "OpenAI", "自定义"])
        provider_map = {"deepseek": 0, "openai": 1}
        self.provider_combo.setCurrentIndex(provider_map.get(self.config.get("api_provider", "deepseek"), 2))
        self.provider_combo.currentIndexChanged.connect(self._on_provider_change)
        self.provider_combo.setStyleSheet("""
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
        provider_label = QLabel("服务商")
        provider_label.setMinimumWidth(48)
        provider_label.setStyleSheet("color: #6b6b6b; font-size: 13px; border: none; background: transparent;")
        api_form.addRow(provider_label, self.provider_combo)

        self.api_key_input = QLineEdit(self.config.get("api_key", ""))
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("sk-...")
        self.api_key_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.50);
                border: 1.5px solid rgba(0, 0, 0, 0.08);
                border-radius: 10px; padding: 8px 12px; font-size: 13px; color: #1a1a1a;
            }
            QLineEdit:focus { border-color: #E87A2D; }
        """)
        key_label = QLabel("Key")
        key_label.setMinimumWidth(48)
        key_label.setStyleSheet("color: #6b6b6b; font-size: 13px; border: none; background: transparent;")
        api_form.addRow(key_label, self.api_key_input)

        self.api_base_input = QLineEdit(self.config.get("api_base_url", ""))
        self.api_base_input.setPlaceholderText("https://api.deepseek.com/v1")
        self.api_base_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.50);
                border: 1.5px solid rgba(0, 0, 0, 0.08);
                border-radius: 10px; padding: 8px 12px; font-size: 13px; color: #1a1a1a;
            }
            QLineEdit:focus { border-color: #E87A2D; }
        """)
        base_label = QLabel("Base")
        base_label.setMinimumWidth(48)
        base_label.setStyleSheet("color: #6b6b6b; font-size: 13px; border: none; background: transparent;")
        api_form.addRow(base_label, self.api_base_input)

        self.model_input = QLineEdit(self.config.get("model", "deepseek-chat"))
        self.model_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.50);
                border: 1.5px solid rgba(0, 0, 0, 0.08);
                border-radius: 10px; padding: 8px 12px; font-size: 13px; color: #1a1a1a;
            }
            QLineEdit:focus { border-color: #E87A2D; }
        """)
        model_label = QLabel("模型")
        model_label.setMinimumWidth(48)
        model_label.setStyleSheet("color: #6b6b6b; font-size: 13px; border: none; background: transparent;")
        api_form.addRow(model_label, self.model_input)

        content_layout.addWidget(api_card)
        content_layout.addStretch()

        # 按钮
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.7); color: #1a1a1a;
                border: 1.5px solid rgba(0,0,0,0.1); border-radius: 12px;
                padding: 10px 20px; font-size: 13px; font-weight: 500;
            }
            QPushButton:hover { background: rgba(255,255,255,0.9); }
        """)
        cancel_btn.clicked.connect(self.close)
        btn_row.addWidget(cancel_btn)

        save_btn = QPushButton("保存")
        save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F09850, stop:1 #E87A2D);
                color: white; border: none; border-radius: 12px;
                padding: 10px 20px; font-size: 13px; font-weight: 600;
            }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E87A2D, stop:1 #C85A1A); }
        """)
        save_btn.clicked.connect(self._save)
        btn_row.addWidget(save_btn)

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

            # -1 表示扩展到整个窗口，DWM 阴影被推到窗口边界之外
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
                    y = pet_pos.y() - 60

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

    def _on_provider_change(self, index):
        presets = {
            0: ("https://api.deepseek.com/v1", "deepseek-chat"),
            1: ("https://api.openai.com/v1", "gpt-3.5-turbo"),
        }
        if index in presets:
            base, model = presets[index]
            self.api_base_input.setText(base)
            self.model_input.setText(model)

    def _save(self):
        self.config["pet_name"] = self.pet_name_input.text().strip() or "Claude"
        self.config["api_key"] = self.api_key_input.text().strip()
        self.config["api_base_url"] = self.api_base_input.text().strip()
        self.config["model"] = self.model_input.text().strip()

        provider_map = {0: "deepseek", 1: "openai", 2: "custom"}
        self.config["api_provider"] = provider_map.get(self.provider_combo.currentIndex(), "custom")

        speed_map = {0: 150, 1: 100, 2: 60}
        self.config["animation_speed"] = speed_map.get(self.speed_combo.currentIndex(), 100)

        if self.autostart_check.isChecked():
            enable_autostart()
            self.config["autostart"] = True
        else:
            disable_autostart()
            self.config["autostart"] = False

        save_config(self.config)
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
