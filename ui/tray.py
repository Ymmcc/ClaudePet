from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QAction, QFont
from PyQt6.QtCore import Qt


def create_tray_icon() -> QPixmap:
    size = 64
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Claude 橙色圆形图标
    painter.setBrush(QColor("#E87A2D"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(4, 4, size - 8, size - 8)

    # 白色字母
    painter.setPen(QColor("white"))
    font = painter.font()
    font.setPixelSize(28)
    font.setWeight(QFont.Weight.DemiBold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "C")

    painter.end()
    return pixmap


class TrayManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.tray = QSystemTrayIcon(parent)
        self.tray.setIcon(QIcon(create_tray_icon()))
        self.tray.setToolTip("ClaudePet - 双击显示")

        self.menu = QMenu()
        self.menu.setStyleSheet("""
            QMenu {
                background: rgba(255, 255, 255, 0.92);
                color: #1a1a1a;
                border: 1px solid rgba(0, 0, 0, 0.08);
                border-radius: 14px;
                padding: 8px;
            }
            QMenu::item {
                padding: 10px 24px;
                border-radius: 8px;
                font-size: 13px;
            }
            QMenu::item:selected {
                background: rgba(232, 122, 45, 0.1);
                color: #c85a1a;
            }
        """)

        self.show_action = self.menu.addAction("显示桌宠")
        self.hide_action = self.menu.addAction("隐藏桌宠")
        self.menu.addSeparator()
        self.chat_action = self.menu.addAction("聊天")
        self.todo_action = self.menu.addAction("待办事项")
        self.menu.addSeparator()
        self.settings_action = self.menu.addAction("设置")
        self.menu.addSeparator()
        self.quit_action = self.menu.addAction("退出")

        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self._on_activated)

    def show(self):
        self.tray.show()

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.parent:
                self.parent.show()
                self.parent.activateWindow()
