import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from utils.config import load_config, save_config
from utils.autostart import is_autostart_enabled, enable_autostart
from core.pet_window import PetWindow
from core.todo_manager import TodoManager
from core.chat_window import ChatWindow
from ui.todo_panel import TodoPanel
from ui.tray import TrayManager
from ui.settings_dialog import SettingsDialog


class ClaudePetApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationName("ClaudePet")

        self.config = load_config()

        # 检查并设置自启动
        if self.config.get("autostart", False) and not is_autostart_enabled():
            enable_autostart()

        self.todo_manager = TodoManager()

        self.pet = PetWindow(self.config, self.todo_manager)
        self.chat_window = None
        self.todo_panel = None
        self.settings_dialog = None

        self.tray = TrayManager()
        self._connect_tray()
        self._connect_pet()

        self.tray.show()
        self.pet.show()

        # 启动后延迟1秒检查待办事项提醒
        QTimer.singleShot(1000, self.todo_manager.check_boot_reminders)

        self.app.aboutToQuit.connect(self._on_quit)

    def _connect_tray(self):
        self.tray.show_action.triggered.connect(self._show_pet)
        self.tray.hide_action.triggered.connect(self._hide_pet)
        self.tray.chat_action.triggered.connect(self._show_chat)
        self.tray.todo_action.triggered.connect(self._show_todos)
        self.tray.settings_action.triggered.connect(self._show_settings)
        self.tray.quit_action.triggered.connect(self.app.quit)

    def _connect_pet(self):
        self.pet.request_chat.connect(self._show_chat)
        self.pet.request_todos.connect(self._show_todos)
        self.pet.request_settings.connect(self._show_settings)
        # 使用定时器更新子窗口位置，而不是信号
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._update_child_windows_position)
        self._update_timer.start(100)  # 每100ms检查一次

    def _show_pet(self):
        self.pet.show_from_tray()

    def _hide_pet(self):
        self.pet.hide_to_tray()

    def _show_chat(self):
        if self.chat_window is None:
            self.chat_window = ChatWindow(self.config, self.pet)
        self.chat_window.show()
        self.chat_window.activateWindow()

    def _show_todos(self):
        if self.todo_panel is None:
            self.todo_panel = TodoPanel(self.todo_manager, self.pet)
        self.todo_panel.show()
        self.todo_panel.activateWindow()

    def _show_settings(self):
        if self.settings_dialog is None:
            self.settings_dialog = SettingsDialog(self.config, self.pet)
        self.settings_dialog.show()
        self.settings_dialog.activateWindow()

    def _update_child_windows_position(self):
        """更新所有子窗口的位置，跟随桌宠；子窗口打开时锁定桌宠"""
        try:
            any_visible = False

            if self.chat_window and self.chat_window.isVisible():
                self.chat_window._position_near_pet()
                any_visible = True

            if self.todo_panel and self.todo_panel.isVisible():
                self.todo_panel._position_near_pet()
                any_visible = True

            if self.settings_dialog and self.settings_dialog.isVisible():
                any_visible = True

            self.pet.set_behaviors_locked(any_visible)
        except Exception:
            pass

    def _on_quit(self):
        self.pet.save_position()
        save_config(self.config)

    def run(self):
        return self.app.exec()


if __name__ == "__main__":
    app = ClaudePetApp()
    sys.exit(app.run())
