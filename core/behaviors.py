import random
from PyQt6.QtCore import QObject, QTimer, pyqtSignal


class BehaviorController(QObject):
    behavior_triggered = pyqtSignal(str, dict)

    def __init__(self, interval: int = 18, parent=None):
        super().__init__(parent)
        self._interval = interval * 1000
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(self._interval)
        self._last_action = None
        self._paused = False

    def set_interval(self, seconds: int):
        self._interval = seconds * 1000
        self._timer.setInterval(self._interval)

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    def _tick(self):
        if self._paused:
            return
        # 每隔18秒随机向左或向右跑
        actions = [
            ("walk", 0.5),       # 向右跑 - 50%
            ("walk_left", 0.5),  # 向左跑 - 50%
        ]
        action = random.choices(
            [a[0] for a in actions],
            weights=[a[1] for a in actions],
            k=1,
        )[0]

        params = {}
        if action == "walk":
            params["direction"] = "right"
            params["distance"] = random.randint(80, 200)
        elif action == "walk_left":
            params["direction"] = "left"
            params["distance"] = random.randint(80, 200)

        self.behavior_triggered.emit(action, params)
