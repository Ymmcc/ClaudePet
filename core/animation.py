from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap
from core.sprite_engine import SpriteState, render_sprite


# 动画配置：映射 ClaudePet 行为到 Clawd 动画状态
ANIMATION_FRAMES = {
    "idle": {"state": SpriteState.IDLE, "frames": 6, "clawd_state": "idle"},
    "walk": {"state": SpriteState.WALK1, "frames": 8, "clawd_state": "run_right"},
    "walk_left": {"state": SpriteState.WALK2, "frames": 8, "clawd_state": "run_left"},
    "sit": {"state": SpriteState.SIT, "frames": 6, "clawd_state": "wait"},
    "sleep": {"state": SpriteState.SLEEP1, "frames": 6, "clawd_state": "wait"},
    "happy": {"state": SpriteState.HAPPY1, "frames": 4, "clawd_state": "wave"},
    "coding": {"state": SpriteState.CODING1, "frames": 6, "clawd_state": "review"},
    "drag": {"state": SpriteState.DRAG, "frames": 7, "clawd_state": "fail"},
    "jump": {"state": SpriteState.HAPPY2, "frames": 5, "clawd_state": "jump"},
    "sprint": {"state": SpriteState.WALK2, "frames": 6, "clawd_state": "sprint"},
    "wave": {"state": SpriteState.HAPPY1, "frames": 4, "clawd_state": "wave"},
    "review": {"state": SpriteState.CODING1, "frames": 6, "clawd_state": "review"},
    "wait": {"state": SpriteState.SIT, "frames": 6, "clawd_state": "wait"},
    "fail": {"state": SpriteState.DRAG, "frames": 7, "clawd_state": "fail"},
}


class AnimationController(QObject):
    frame_changed = pyqtSignal(QPixmap)

    def __init__(self, speed: int = 100, parent=None):
        super().__init__(parent)
        self._state = "idle"
        self._state_config = ANIMATION_FRAMES["idle"]
        self._frame_index = 0
        self._speed = speed
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._next_frame)
        self._timer.start(self._speed)

    @property
    def state(self) -> str:
        return self._state

    def set_state(self, state: str):
        if state == self._state:
            return
        if state not in ANIMATION_FRAMES:
            return
        self._state = state
        self._state_config = ANIMATION_FRAMES[state]
        self._frame_index = 0
        self._emit_frame()

    def set_speed(self, ms: int):
        self._speed = ms
        self._timer.setInterval(ms)

    def _next_frame(self):
        max_frames = self._state_config["frames"]
        self._frame_index = (self._frame_index + 1) % max_frames
        self._emit_frame()

    def _emit_frame(self):
        state = self._state_config["state"]
        pixmap = render_sprite(state, frame_index=self._frame_index)
        self.frame_changed.emit(pixmap)

    def current_pixmap(self) -> QPixmap:
        state = self._state_config["state"]
        return render_sprite(state, frame_index=self._frame_index)
