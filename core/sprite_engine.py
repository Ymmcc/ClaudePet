from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QImage, QPainter, QColor, QPixmap, QFont, QFontMetrics, QPolygon
from enum import Enum
import os


class SpriteState(Enum):
    IDLE = "idle"
    WALK1 = "walk1"
    WALK2 = "walk2"
    SIT = "sit"
    SLEEP1 = "sleep1"
    SLEEP2 = "sleep2"
    HAPPY1 = "happy1"
    HAPPY2 = "happy2"
    CODING1 = "coding1"
    CODING2 = "coding2"
    DRAG = "drag"


# Clawd 精灵图配置 (8列 x 9行)
CLAWD_SPRITESHEET_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "clawd", "spritesheet.webp")

# 精灵图布局: 8列 x 9行
SPRITE_COLUMNS = 8
SPRITE_ROWS = 9

# 动画状态映射到精灵图行号
CLAWD_STATE_ROWS = {
    "idle": 0,      # 待机 - 6帧
    "run_right": 1, # 向右跑 - 8帧
    "run_left": 2,  # 向左跑 - 8帧
    "wave": 3,      # 挥手 - 4帧
    "jump": 4,      # 跳跃 - 5帧
    "fail": 5,      # 失败 - 7帧
    "wait": 6,      # 等待 - 6帧
    "sprint": 7,    # 奔跑 - 6帧
    "review": 8,    # 审阅 - 6帧
}

# 每个动画状态的帧数
CLAWD_FRAME_COUNTS = {
    "idle": 6,
    "run_right": 8,
    "run_left": 8,
    "wave": 4,
    "jump": 5,
    "fail": 7,
    "wait": 6,
    "sprint": 6,
    "review": 6,
}

# ClaudePet 状态到 Clawd 状态的映射
STATE_MAPPING = {
    SpriteState.IDLE: "idle",
    SpriteState.WALK1: "run_right",
    SpriteState.WALK2: "run_right",
    SpriteState.SIT: "wait",
    SpriteState.SLEEP1: "wait",
    SpriteState.SLEEP2: "wait",
    SpriteState.HAPPY1: "wave",
    SpriteState.HAPPY2: "jump",  # 跳跃动画
    SpriteState.CODING1: "review",
    SpriteState.CODING2: "review",
    SpriteState.DRAG: "fail",
}

# 精灵图缓存
_spritesheet_cache = {}


def load_spritesheet() -> QPixmap:
    """加载 Clawd 精灵图"""
    if "spritesheet" not in _spritesheet_cache:
        if os.path.exists(CLAWD_SPRITESHEET_PATH):
            _spritesheet_cache["spritesheet"] = QPixmap(CLAWD_SPRITESHEET_PATH)
        else:
            # 如果文件不存在，返回空 QPixmap
            _spritesheet_cache["spritesheet"] = QPixmap()
    return _spritesheet_cache["spritesheet"]


def get_frame_rect(state: str, frame_index: int) -> QRect:
    """获取精灵图中指定状态和帧的位置"""
    spritesheet = load_spritesheet()
    if spritesheet.isNull():
        return QRect()

    frame_width = spritesheet.width() // SPRITE_COLUMNS
    frame_height = spritesheet.height() // SPRITE_ROWS

    row = CLAWD_STATE_ROWS.get(state, 0)
    max_frames = CLAWD_FRAME_COUNTS.get(state, 1)
    col = frame_index % max_frames

    return QRect(col * frame_width, row * frame_height, frame_width, frame_height)


# 不同动画状态的缩放比例
STATE_SCALE = {
    "run_right": 0.28,
    "run_left": 0.28,
    "fail": 0.30,
    "sprint": 0.28,
}


def render_sprite(state: SpriteState, scale: float = 1.0, frame_index: int = 0) -> QPixmap:
    """渲染 Clawd 精灵"""
    spritesheet = load_spritesheet()

    if spritesheet.isNull():
        size = int(48 * scale)
        img = QImage(size, size, QImage.Format.Format_ARGB32)
        img.fill(QColor("#E87A2D"))
        return QPixmap.fromImage(img)

    clawd_state = STATE_MAPPING.get(state, "idle")
    frame_rect = get_frame_rect(clawd_state, frame_index)

    if frame_rect.isNull():
        return QPixmap()

    frame_pixmap = spritesheet.copy(frame_rect)

    # 根据动画状态使用不同缩放比例
    base_scale = STATE_SCALE.get(clawd_state, 0.35)
    target_size = frame_pixmap.size() * (base_scale * scale)
    frame_pixmap = frame_pixmap.scaled(
        target_size,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.FastTransformation
    )

    return frame_pixmap


def render_speech_bubble(text: str, scale: float = 1.0) -> QPixmap:
    """渲染语音气泡 - macOS 风格"""
    font = QFont("Segoe UI", max(7, int(8 * scale)))
    metrics = QFontMetrics(font)
    tw = metrics.horizontalAdvance(text) + 14
    th = metrics.height() + 10
    w = min(max(tw, 44), 120)  # 限制最大宽度
    h = max(th, 24)

    img = QImage(w, h, QImage.Format.Format_ARGB32)
    img.fill(Qt.GlobalColor.transparent)
    painter = QPainter(img)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # macOS 风格 - 白色背景 + 浅灰边框
    painter.setBrush(QColor(255, 255, 255, 230))
    painter.setPen(QColor(0, 0, 0, 25))  # 浅灰边框
    painter.drawRoundedRect(0, 0, w - 1, h - 1, 8, 8)

    # 文字
    painter.setPen(QColor("#1D1D1F"))
    painter.setFont(font)
    painter.drawText(7, 3, w - 14, h - 6, Qt.AlignmentFlag.AlignCenter, text)

    painter.end()
    return QPixmap.fromImage(img)


# 保留旧的颜色配置以兼容
C = {
    "_": None,
    "o": QColor("#E87A2D"),
    "O": QColor("#C45A1A"),
    "w": QColor("#FFFFFF"),
    "e": QColor("#1A1A1A"),
    "h": QColor("#FFB366"),
    "g": QColor("#374151"),
    "s": QColor("#6B7280"),
    "r": QColor("#EF4444"),
    "b": QColor("#3B82F6"),
    "p": QColor("#EC4899"),
    "c": QColor("#10B981"),
    "n": QColor("#FF8C42"),
    "i": QColor("#FFD699"),
    "t": QColor("#D97706"),
}
