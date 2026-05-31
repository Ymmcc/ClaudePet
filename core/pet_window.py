from PyQt6.QtWidgets import QWidget, QMenu, QApplication
from PyQt6.QtCore import Qt, QPoint, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QPainter, QPixmap, QCursor
from core.animation import AnimationController
from core.emotion import EmotionSystem
from core.behaviors import BehaviorController
from core.sprite_engine import render_speech_bubble
from core.todo_manager import TodoManager
from ui.reminder_popup import ReminderPopup


class FocusTimer(QObject):
    tick = pyqtSignal(int, str)
    finished = pyqtSignal(str)

    FOCUS_DURATION = 1500
    BREAK_DURATION = 300

    def __init__(self, parent=None):
        super().__init__(parent)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_tick)
        self._remaining = 0
        self._state = "idle"

    @property
    def state(self):
        return self._state

    @property
    def remaining(self):
        return self._remaining

    def start_focus(self):
        self._state = "focus"
        self._remaining = self.FOCUS_DURATION
        self._timer.start(1000)
        self.tick.emit(self._remaining, self._state)

    def start_break(self):
        self._state = "break"
        self._remaining = self.BREAK_DURATION
        self._timer.start(1000)
        self.tick.emit(self._remaining, self._state)

    def pause(self):
        self._timer.stop()

    def resume(self):
        if self._state != "idle":
            self._timer.start(1000)

    def stop(self):
        self._timer.stop()
        self._state = "idle"
        self._remaining = 0

    def _on_tick(self):
        self._remaining -= 1
        if self._remaining <= 0:
            self._timer.stop()
            finished_state = self._state
            self.finished.emit(finished_state)
        else:
            self.tick.emit(self._remaining, self._state)

    @staticmethod
    def format_time(seconds):
        m = seconds // 60
        s = seconds % 60
        return f"{m}:{s:02d}"


class PetWindow(QWidget):
    request_chat = pyqtSignal()
    request_todos = pyqtSignal()
    request_settings = pyqtSignal()

    def __init__(self, config: dict, todo_manager: TodoManager, parent=None):
        super().__init__(parent)
        self.config = config
        self.todo_manager = todo_manager
        self._pixmap = QPixmap()
        self._bubble_pixmap = QPixmap()
        self._bubble_timer = QTimer(self)
        self._bubble_timer.timeout.connect(self._hide_bubble)
        self._dragging = False
        self._drag_offset = QPoint()
        self._walk_target = None
        self._locked = False
        self._walk_timer = QTimer(self)
        self._walk_timer.timeout.connect(self._walk_step)
        self._hidden = False
        self._reminder_popup = None
        self._focus_timer = FocusTimer(self)
        self._focus_timer.tick.connect(self._on_focus_tick)
        self._focus_timer.finished.connect(self._on_focus_finished)

        self._init_window()
        self._init_animation()
        self._init_emotion()
        self._init_behaviors()
        self._connect_signals()
        self._restore_position()

    def _init_window(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(80, 100)
        self.setAcceptDrops(True)

    def _init_animation(self):
        speed = self.config.get("animation_speed", 100)
        self._anim = AnimationController(speed, self)
        self._anim.frame_changed.connect(self._on_frame)
        self._anim.set_state("idle")

    def _init_emotion(self):
        self._emotion = EmotionSystem(self)
        self._emotion.emotion_changed.connect(self._on_emotion_change)

    def _init_behaviors(self):
        interval = self.config.get("behavior_interval", 15)
        self._behaviors = BehaviorController(interval, self)
        self._behaviors.behavior_triggered.connect(self._on_behavior)

    def show_from_tray(self):
        """从托盘恢复显示"""
        self._hidden = False
        self.show()
        self._anim.set_state("idle")

    def hide_to_tray(self):
        """隐藏到托盘"""
        self._hidden = True
        self.hide()

    def _connect_signals(self):
        self.todo_manager.todo_reminder.connect(self._show_reminder_popup)

    def _restore_position(self):
        x = self.config.get("pet_x", -1)
        y = self.config.get("pet_y", -1)
        if x < 0 or y < 0:
            screen = QApplication.primaryScreen().geometry()
            x = screen.width() - 200
            y = screen.height() - 250
        self.move(x, y)

    def _on_frame(self, pixmap: QPixmap):
        self._pixmap = pixmap
        self.update()

    def _on_emotion_change(self, mood: str):
        anim_state = self._emotion.get_animation_state()
        self._anim.set_state(anim_state)

    def _on_behavior(self, action: str, params: dict):
        if self._dragging or self._locked:
            return
        if action in ["walk", "walk_left", "sprint"]:
            direction = params.get("direction", "right")
            distance = params.get("distance", 100)
            self._start_walk(direction, distance, action)
        else:
            self._anim.set_state(action)

    def _start_walk(self, direction: str, distance: int, action: str = "walk"):
        anim_state = "walk" if direction == "right" else "walk_left"
        self._anim.set_state(anim_state)
        dx = distance if direction == "right" else -distance
        screen = QApplication.primaryScreen().geometry()
        target_x = max(0, min(self.x() + dx, screen.width() - self.width()))
        self._walk_target = target_x
        self._walk_timer.start(30)

    def _walk_step(self):
        if self._walk_target is None:
            self._walk_timer.stop()
            self._anim.set_state("idle")
            return
        cx = self.x()
        tx = self._walk_target
        if abs(cx - tx) < 3:
            self.move(tx, self.y())
            self._walk_target = None
            self._walk_timer.stop()
            self._anim.set_state("idle")
            return
        step = 3 if tx > cx else -3
        self.move(cx + step, self.y())

    def show_bubble(self, text: str, duration: int = 3000):
        self._bubble_pixmap = render_speech_bubble(text)
        self._bubble_timer.start(duration)
        self.update()

    def _show_reminder_popup(self, msg: str):
        """显示提醒弹出窗口，切换到等待动画"""
        if self._reminder_popup is not None:
            self._reminder_popup.close()
            self._reminder_popup = None

        self._anim.set_state("wait")

        self._reminder_popup = ReminderPopup(msg, self)
        self._reminder_popup.dismissed.connect(self._on_reminder_dismissed)
        self._reminder_popup.show()

    def _on_reminder_dismissed(self):
        """用户点击'收到'后，回到待机动画"""
        self._reminder_popup = None
        self._anim.set_state("idle")

    def _hide_bubble(self):
        self._bubble_pixmap = QPixmap()
        self._bubble_timer.stop()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # 绘制气泡在顶部
        if not self._bubble_pixmap.isNull():
            bubble_width = min(self._bubble_pixmap.width(), self.width() - 10)
            bubble_height = min(self._bubble_pixmap.height(), 30)
            scaled_bubble = self._bubble_pixmap.scaled(
                bubble_width, bubble_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            bx = (self.width() - scaled_bubble.width()) // 2
            by = 2
            painter.drawPixmap(bx, by, scaled_bubble)

        # 绘制精灵图在底部
        px = (self.width() - self._pixmap.width()) // 2
        py = self.height() - self._pixmap.height() - 2
        painter.drawPixmap(px, py, self._pixmap)
        painter.end()

    def set_behaviors_locked(self, locked: bool):
        """锁定/解锁自动行为（行走等）"""
        self._locked = locked
        if locked and self._walk_target is not None:
            # 停止当前行走
            self._walk_target = None
            self._walk_timer.stop()
            self._anim.set_state("idle")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._drag_offset = event.globalPosition().toPoint() - self.pos()
            self._anim.set_state("idle")
            self._emotion.interact()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging:
            new_pos = event.globalPosition().toPoint() - self._drag_offset
            self.move(new_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            self._emotion.interact()
            self._anim.set_state("idle")
            self.config["pet_x"] = self.x()
            self.config["pet_y"] = self.y()
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._anim.set_state("jump")
            self.show_bubble("嘿嘿~", 2000)
            QTimer.singleShot(3000, lambda: self._anim.set_state("idle"))
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("""
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

        chat_action = menu.addAction("聊天")
        chat_action.triggered.connect(self._open_chat)

        todo_action = menu.addAction("待办事项")
        todo_action.triggered.connect(self._open_todos)

        menu.addSeparator()

        if self._focus_timer.state == "idle":
            focus_action = menu.addAction("🍅 开始专注")
            focus_action.triggered.connect(self._start_focus)
        elif self._focus_timer.state == "focus" or self._focus_timer._state == "focus_paused":
            if self._focus_timer._state == "focus_paused":
                pause_action = menu.addAction("▶ 恢复")
            else:
                remaining = FocusTimer.format_time(self._focus_timer.remaining)
                pause_action = menu.addAction(f"⏸ 暂停 ({remaining})")
            pause_action.triggered.connect(self._toggle_focus_pause)
            stop_action = menu.addAction("✋ 放弃本次")
            stop_action.triggered.connect(self._stop_focus)
        elif self._focus_timer.state == "break":
            skip_action = menu.addAction("⏭ 跳过休息")
            skip_action.triggered.connect(self._stop_focus)

        menu.addSeparator()

        feed_action = menu.addAction("喂食")
        feed_action.triggered.connect(self._feed)

        rest_action = menu.addAction("休息")
        rest_action.triggered.connect(self._rest)

        menu.addSeparator()

        settings_action = menu.addAction("设置")
        settings_action.triggered.connect(lambda: self.request_settings.emit())

        menu.addSeparator()

        hide_action = menu.addAction("隐藏")
        hide_action.triggered.connect(self._hide_pet)

        menu.addSeparator()

        quit_action = menu.addAction("退出")
        quit_action.triggered.connect(QApplication.quit)

        menu.exec(event.globalPos())

    def _open_chat(self):
        """打开聊天 - 显示审阅状态"""
        self._anim.set_state("review")
        self.show_bubble("聊天中...", 3000)
        self.request_chat.emit()

    def _open_todos(self):
        """打开待办事项 - 显示等待状态"""
        self._anim.set_state("wait")
        self.show_bubble("查看待办", 3000)
        self.request_todos.emit()

    def _feed(self):
        """喂食 - 显示待机动画"""
        self._emotion.feed()
        self.show_bubble("好吃！", 2000)
        self._anim.set_state("idle")
        QTimer.singleShot(3000, lambda: self._anim.set_state("idle"))

    def _rest(self):
        """休息 - 显示失败状态后回到待机"""
        self._emotion.rest()
        self.show_bubble("休息一下~", 2000)
        self._anim.set_state("fail")
        QTimer.singleShot(5000, lambda: self._anim.set_state("idle"))

    def _start_focus(self):
        self._focus_timer.start_focus()
        self._anim.set_state("coding")
        self._behaviors.pause()

    def _stop_focus(self):
        self._focus_timer.stop()
        self._anim.set_state("idle")
        self._behaviors.resume()
        self._hide_bubble()

    def _toggle_focus_pause(self):
        if self._focus_timer.state == "focus":
            self._focus_timer.pause()
            self._focus_timer._state = "focus_paused"
            self.show_bubble("⏸ 已暂停", 2000)
        elif self._focus_timer._state == "focus_paused":
            self._focus_timer._state = "focus"
            self._focus_timer.resume()

    def _on_focus_tick(self, remaining, state):
        time_str = FocusTimer.format_time(remaining)
        if state == "focus":
            self.show_bubble(f"🍅 {time_str}", 2000)
        elif state == "break":
            self.show_bubble(f"☕ {time_str}", 2000)

    def _on_focus_finished(self, state):
        if state == "focus":
            self.show_bubble("✅ 专注完成！", 3000)
            self._anim.set_state("idle")
            QTimer.singleShot(3000, self._start_break_timer)
        elif state == "break":
            self.show_bubble("💪 开始下一轮！", 3000)
            self._anim.set_state("idle")
            self._behaviors.resume()

    def _start_break_timer(self):
        self._focus_timer.start_break()
        self._anim.set_state("sit")

    def _hide_pet(self):
        """隐藏桌宠 - 显示挥手动画后隐藏"""
        self._anim.set_state("wave")
        self.show_bubble("拜拜~", 1500)
        QTimer.singleShot(2000, self.hide_to_tray)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            name = path.split("/")[-1].split("\\")[-1]
            self.show_bubble(f"文件: {name}", 4000)
            self._emotion.interact()

    def save_position(self):
        self.config["pet_x"] = self.x()
        self.config["pet_y"] = self.y()
