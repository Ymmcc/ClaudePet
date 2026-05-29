import random
from PyQt6.QtCore import QObject, QTimer, pyqtSignal


class EmotionState:
    HAPPY = "happy"
    NEUTRAL = "neutral"
    SLEEPY = "sleepy"
    BORED = "bored"
    EXCITED = "excited"


class EmotionSystem(QObject):
    emotion_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._mood = EmotionState.NEUTRAL
        self._energy = 100
        self._happiness = 70
        self._interactions = 0

        self._decay_timer = QTimer(self)
        self._decay_timer.timeout.connect(self._decay)
        self._decay_timer.start(30000)

    @property
    def mood(self) -> str:
        return self._mood

    @property
    def energy(self) -> int:
        return self._energy

    @property
    def happiness(self) -> int:
        return self._happiness

    def interact(self):
        self._interactions += 1
        self._happiness = min(100, self._happiness + 10)
        self._energy = max(0, self._energy - 2)
        self._update_mood()

    def feed(self):
        self._happiness = min(100, self._happiness + 15)
        self._energy = min(100, self._energy + 10)
        self._update_mood()

    def rest(self):
        self._energy = min(100, self._energy + 30)
        self._update_mood()

    def _decay(self):
        self._energy = max(0, self._energy - 1)
        self._happiness = max(0, self._happiness - 1)
        self._update_mood()

    def _update_mood(self):
        old = self._mood
        if self._energy < 20:
            self._mood = EmotionState.SLEEPY
        elif self._happiness > 80:
            self._mood = EmotionState.HAPPY
        elif self._happiness > 60:
            self._mood = EmotionState.NEUTRAL
        else:
            self._mood = EmotionState.BORED

        if self._mood != old:
            self.emotion_changed.emit(self._mood)

    def get_animation_state(self) -> str:
        mapping = {
            EmotionState.HAPPY: "happy",
            EmotionState.EXCITED: "happy",
            EmotionState.NEUTRAL: "idle",
            EmotionState.BORED: "sit",
            EmotionState.SLEEPY: "sleep",
        }
        return mapping.get(self._mood, "idle")
