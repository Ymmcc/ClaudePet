"""
ClaudePet Design Tokens
macOS-inspired light theme with frosted glass effect
"""

# Color Palette - macOS Light
class Colors:
    # Backgrounds
    BG_PRIMARY = "rgba(246, 246, 246, 0.95)"      # 主背景 - 浅灰白
    BG_SECONDARY = "rgba(255, 255, 255, 0.90)"     # 次级背景 - 白色
    BG_TERTIARY = "rgba(240, 240, 240, 0.85)"      # 三级背景
    BG_GLASS = "rgba(255, 255, 255, 0.70)"          # 毛玻璃背景
    BG_HOVER = "rgba(0, 0, 0, 0.04)"                # 悬停状态
    BG_PRESSED = "rgba(0, 0, 0, 0.08)"              # 按下状态

    # Text
    TEXT_PRIMARY = "#1D1D1F"                         # 主文本 - 近黑
    TEXT_SECONDARY = "#86868B"                       # 次级文本 - 灰色
    TEXT_TERTIARY = "#AEAEB2"                        # 三级文本 - 浅灰
    TEXT_INVERSE = "#FFFFFF"                         # 反色文本 - 白色

    # Accent
    ACCENT = "#007AFF"                               # macOS 蓝
    ACCENT_HOVER = "#0056CC"
    ACCENT_PRESSED = "#004099"
    ACCENT_LIGHT = "rgba(0, 122, 255, 0.12)"        # 浅蓝背景

    # Semantic
    SUCCESS = "#34C759"                              # 成功 - 绿色
    WARNING = "#FF9500"                              # 警告 - 橙色
    ERROR = "#FF3B30"                                # 错误 - 红色
    INFO = "#5AC8FA"                                 # 信息 - 浅蓝

    # Borders
    BORDER = "rgba(0, 0, 0, 0.10)"                  # 边框
    BORDER_LIGHT = "rgba(0, 0, 0, 0.06)"            # 浅边框
    BORDER_FOCUS = ACCENT                            # 聚焦边框

    # Shadows - macOS style
    SHADOW_SM = "0 1px 3px rgba(0, 0, 0, 0.08)"
    SHADOW_MD = "0 4px 12px rgba(0, 0, 0, 0.10)"
    SHADOW_LG = "0 8px 24px rgba(0, 0, 0, 0.12)"
    SHADOW_XL = "0 16px 48px rgba(0, 0, 0, 0.16)"

    # Pet brand color
    BRAND = "#E87A2D"                                # Claude 橙色
    BRAND_LIGHT = "rgba(232, 122, 45, 0.15)"


# Typography - SF Pro inspired
class Typography:
    FONT_FAMILY = '"Segoe UI", "SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif'
    FONT_MONO = '"SF Mono", "Cascadia Code", "Consolas", monospace'

    # Font sizes
    SIZE_XS = "11px"
    SIZE_SM = "12px"
    SIZE_BASE = "13px"
    SIZE_MD = "14px"
    SIZE_LG = "16px"
    SIZE_XL = "20px"
    SIZE_2XL = "24px"

    # Font weights
    WEIGHT_REGULAR = "400"
    WEIGHT_MEDIUM = "500"
    WEIGHT_SEMIBOLD = "600"
    WEIGHT_BOLD = "700"

    # Line heights
    LINE_HEIGHT_TIGHT = "1.2"
    LINE_HEIGHT_NORMAL = "1.4"
    LINE_HEIGHT_RELAXED = "1.6"


# Spacing - 4px base grid
class Spacing:
    XS = "4px"
    SM = "8px"
    MD = "12px"
    LG = "16px"
    XL = "20px"
    XXL = "24px"
    XXXL = "32px"


# Border Radius - macOS style
class Radius:
    SM = "6px"
    MD = "8px"
    LG = "12px"
    XL = "16px"
    FULL = "9999px"


# Animation - Apple HIG timing
class Animation:
    DURATION_FAST = "150ms"
    DURATION_NORMAL = "200ms"
    DURATION_SLOW = "300ms"

    EASING_DEFAULT = "cubic-bezier(0.25, 0.1, 0.25, 1.0)"  # macOS default
    EASING_EASE_OUT = "cubic-bezier(0.16, 1, 0.3, 1)"      # 入场
    EASING_EASE_IN = "cubic-bezier(0.7, 0, 0.84, 0)"       # 退场
    EASING_SPRING = "cubic-bezier(0.34, 1.56, 0.64, 1)"    # 弹性


# Component Styles
class Components:
    # Button
    BTN_PADDING = "8px 16px"
    BTN_RADIUS = Radius.MD
    BTN_FONT_SIZE = SIZE_BASE = Typography.SIZE_BASE
    BTN_MIN_HEIGHT = "32px"

    # Input
    INPUT_PADDING = "8px 12px"
    INPUT_RADIUS = Radius.MD
    INPUT_HEIGHT = "36px"

    # Card
    CARD_PADDING = Spacing.LG
    CARD_RADIUS = Radius.XL

    # Dialog
    DIALOG_PADDING = Spacing.XXL
    DIALOG_RADIUS = Radius.XL


def get_stylesheet(component: str = "global") -> str:
    """获取组件样式表"""

    base = f"""
        * {{
            font-family: {Typography.FONT_FAMILY};
            font-size: {Typography.SIZE_BASE};
            color: {Colors.TEXT_PRIMARY};
        }}
    """

    # 预定义 scrollbar 样式
    scrollbar_style = f"""
        QScrollBar:vertical {{
            background: transparent;
            width: 8px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {Colors.TEXT_TERTIARY};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {Colors.TEXT_SECONDARY};
        }}
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {{
            background: transparent;
        }}
    """

    styles = {
        "global": f"""
            QWidget {{
                background: {Colors.BG_PRIMARY};
                color: {Colors.TEXT_PRIMARY};
            }}
        """,

        "dialog": f"""
            QWidget#dialog-container {{
                background: {Colors.BG_GLASS};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {Radius.XL};
            }}
        """,

        "title": f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: {Typography.SIZE_LG};
                font-weight: {Typography.WEIGHT_SEMIBOLD};
                border: none;
            }}
        """,

        "subtitle": f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: {Typography.SIZE_SM};
                font-weight: {Typography.WEIGHT_REGULAR};
                border: none;
            }}
        """,

        "text": f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: {Typography.SIZE_BASE};
                border: none;
            }}
        """,

        "text-secondary": f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: {Typography.SIZE_SM};
                border: none;
            }}
        """,

        "input": f"""
            QLineEdit {{
                background: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER};
                border-radius: {Radius.MD};
                padding: {Components.INPUT_PADDING};
                color: {Colors.TEXT_PRIMARY};
                font-size: {Typography.SIZE_BASE};
                min-height: {Components.INPUT_HEIGHT};
            }}
            QLineEdit:focus {{
                border-color: {Colors.ACCENT};
                border-width: 2px;
            }}
            QLineEdit:hover {{
                border-color: {Colors.TEXT_TERTIARY};
            }}
        """,

        "combobox": f"""
            QComboBox {{
                background: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER};
                border-radius: {Radius.MD};
                padding: {Components.INPUT_PADDING};
                color: {Colors.TEXT_PRIMARY};
                font-size: {Typography.SIZE_BASE};
                min-height: {Components.INPUT_HEIGHT};
            }}
            QComboBox:focus {{
                border-color: {Colors.ACCENT};
                border-width: 2px;
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 8px;
            }}
            QComboBox QAbstractItemView {{
                background: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER};
                border-radius: {Radius.MD};
                padding: 4px;
                selection-background-color: {Colors.ACCENT_LIGHT};
                selection-color: {Colors.TEXT_PRIMARY};
            }}
        """,

        "checkbox": f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
                font-size: {Typography.SIZE_BASE};
                spacing: 8px;
                border: none;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {Colors.BORDER};
                border-radius: 4px;
                background: {Colors.BG_SECONDARY};
            }}
            QCheckBox::indicator:hover {{
                border-color: {Colors.ACCENT};
            }}
            QCheckBox::indicator:checked {{
                background: {Colors.ACCENT};
                border-color: {Colors.ACCENT};
            }}
        """,

        "btn-primary": f"""
            QPushButton {{
                background: {Colors.ACCENT};
                color: {Colors.TEXT_INVERSE};
                border: none;
                border-radius: {Radius.MD};
                padding: {Components.BTN_PADDING};
                font-size: {Typography.SIZE_BASE};
                font-weight: {Typography.WEIGHT_MEDIUM};
                min-height: {Components.BTN_MIN_HEIGHT};
            }}
            QPushButton:hover {{
                background: {Colors.ACCENT_HOVER};
            }}
            QPushButton:pressed {{
                background: {Colors.ACCENT_PRESSED};
            }}
            QPushButton:disabled {{
                background: {Colors.TEXT_TERTIARY};
                color: {Colors.BG_SECONDARY};
            }}
        """,

        "btn-secondary": f"""
            QPushButton {{
                background: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER};
                border-radius: {Radius.MD};
                padding: {Components.BTN_PADDING};
                font-size: {Typography.SIZE_BASE};
                font-weight: {Typography.WEIGHT_MEDIUM};
                min-height: {Components.BTN_MIN_HEIGHT};
            }}
            QPushButton:hover {{
                background: {Colors.BG_HOVER};
                border-color: {Colors.TEXT_TERTIARY};
            }}
            QPushButton:pressed {{
                background: {Colors.BG_PRESSED};
            }}
        """,

        "btn-ghost": f"""
            QPushButton {{
                background: transparent;
                color: {Colors.TEXT_SECONDARY};
                border: none;
                border-radius: {Radius.MD};
                padding: 6px 10px;
                font-size: {Typography.SIZE_BASE};
            }}
            QPushButton:hover {{
                background: {Colors.BG_HOVER};
                color: {Colors.TEXT_PRIMARY};
            }}
            QPushButton:pressed {{
                background: {Colors.BG_PRESSED};
            }}
        """,

        "btn-icon": f"""
            QPushButton {{
                background: transparent;
                color: {Colors.TEXT_SECONDARY};
                border: none;
                border-radius: {Radius.SM};
                padding: 4px;
                font-size: 16px;
                min-width: 24px;
                min-height: 24px;
            }}
            QPushButton:hover {{
                background: {Colors.BG_HOVER};
                color: {Colors.TEXT_PRIMARY};
            }}
            QPushButton:pressed {{
                background: {Colors.BG_PRESSED};
            }}
        """,

        "list": f"""
            QListWidget {{
                background: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {Radius.LG};
                padding: 4px;
                outline: none;
            }}
            QListWidget::item {{
                padding: 10px 12px;
                border-radius: {Radius.MD};
                margin: 2px 0;
            }}
            QListWidget::item:selected {{
                background: {Colors.ACCENT_LIGHT};
                color: {Colors.TEXT_PRIMARY};
            }}
            QListWidget::item:hover {{
                background: {Colors.BG_HOVER};
            }}
        """,

        "scrollbar": scrollbar_style,

        "chat-display": f"""
            QTextEdit {{
                background: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {Radius.LG};
                padding: 12px;
                font-size: {Typography.SIZE_BASE};
                color: {Colors.TEXT_PRIMARY};
                selection-background-color: {Colors.ACCENT_LIGHT};
            }}
            {scrollbar_style}
        """,

        "card": f"""
            QWidget {{
                background: {Colors.BG_GLASS};
                border: 1px solid {Colors.BORDER_LIGHT};
                border-radius: {Radius.XL};
            }}
        """,

        "close-btn": f"""
            QPushButton {{
                color: {Colors.TEXT_TERTIARY};
                background: transparent;
                border: none;
                font-size: 18px;
                border-radius: {Radius.SM};
                min-width: 24px;
                min-height: 24px;
            }}
            QPushButton:hover {{
                background: {Colors.ERROR};
                color: {Colors.TEXT_INVERSE};
            }}
        """,

        "section-label": f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: {Typography.SIZE_SM};
                font-weight: {Typography.WEIGHT_MEDIUM};
                text-transform: uppercase;
                letter-spacing: 0.5px;
                border: none;
            }}
        """,

        "status": f"""
            QLabel {{
                color: {Colors.TEXT_TERTIARY};
                font-size: {Typography.SIZE_XS};
                border: none;
            }}
        """,
    }

    return styles.get(component, "")
