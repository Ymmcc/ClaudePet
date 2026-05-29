"""
ClaudePet UI Styles - Refined Glassmorphism
精致磨砂玻璃风格
"""

# 颜色系统
COLORS = {
    # 背景 - 多层半透明
    "bg_ultra_light": "rgba(255, 255, 255, 0.85)",
    "bg_light": "rgba(255, 255, 255, 0.72)",
    "bg_medium": "rgba(255, 255, 255, 0.58)",
    "bg_card": "rgba(255, 255, 255, 0.65)",
    "bg_input": "rgba(255, 255, 255, 0.50)",
    "bg_hover": "rgba(0, 0, 0, 0.03)",
    "bg_pressed": "rgba(0, 0, 0, 0.06)",
    "bg_accent": "rgba(232, 122, 45, 0.08)",
    "bg_accent_strong": "rgba(232, 122, 45, 0.15)",

    # 文字
    "text_primary": "#1a1a1a",
    "text_secondary": "#6b6b6b",
    "text_tertiary": "#9a9a9a",
    "text_inverse": "#ffffff",
    "text_accent": "#c85a1a",

    # 品牌色 - Claude 橙
    "accent": "#E87A2D",
    "accent_light": "#F09850",
    "accent_dark": "#C85A1A",
    "accent_subtle": "rgba(232, 122, 45, 0.12)",

    # 边框
    "border_light": "rgba(0, 0, 0, 0.06)",
    "border_medium": "rgba(0, 0, 0, 0.10)",
    "border_strong": "rgba(0, 0, 0, 0.15)",
    "border_accent": "rgba(232, 122, 45, 0.30)",

    # 阴影
    "shadow_sm": "0 2px 8px rgba(0, 0, 0, 0.04)",
    "shadow_md": "0 4px 16px rgba(0, 0, 0, 0.06)",
    "shadow_lg": "0 8px 32px rgba(0, 0, 0, 0.08)",
    "shadow_xl": "0 16px 48px rgba(0, 0, 0, 0.10)",
    "shadow_glow": "0 0 20px rgba(232, 122, 45, 0.15)",

    # 状态
    "success": "#34C759",
    "warning": "#FF9500",
    "error": "#FF3B30",
    "info": "#5AC8FA",
}


def get_main_stylesheet() -> str:
    """获取主窗口样式"""
    return f"""
        * {{
            font-family: "SF Pro Display", "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif;
        }}
    """


def get_card_stylesheet() -> str:
    """获取卡片容器样式 - 磨砂玻璃效果"""
    return f"""
        QWidget#card {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border_light']};
            border-radius: 20px;
        }}
    """


def get_title_stylesheet() -> str:
    """获取标题样式"""
    return f"""
        QLabel {{
            color: {COLORS['text_primary']};
            font-size: 18px;
            font-weight: 600;
            letter-spacing: -0.3px;
            border: none;
            background: transparent;
        }}
    """


def get_subtitle_stylesheet() -> str:
    """获取副标题样式"""
    return f"""
        QLabel {{
            color: {COLORS['text_secondary']};
            font-size: 12px;
            font-weight: 400;
            letter-spacing: 0.2px;
            border: none;
            background: transparent;
        }}
    """


def get_input_stylesheet() -> str:
    """获取输入框样式"""
    return f"""
        QLineEdit {{
            background: {COLORS['bg_input']};
            border: 1.5px solid {COLORS['border_medium']};
            border-radius: 12px;
            padding: 10px 14px;
            font-size: 13px;
            color: {COLORS['text_primary']};
            selection-background-color: {COLORS['accent_subtle']};
        }}
        QLineEdit:focus {{
            border-color: {COLORS['accent']};
            background: {COLORS['bg_ultra_light']};
        }}
        QLineEdit:hover {{
            border-color: {COLORS['border_strong']};
        }}
    """


def get_textarea_stylesheet() -> str:
    """获取文本区域样式"""
    return f"""
        QTextEdit {{
            background: {COLORS['bg_input']};
            border: 1.5px solid {COLORS['border_light']};
            border-radius: 14px;
            padding: 12px;
            font-size: 13px;
            color: {COLORS['text_primary']};
            selection-background-color: {COLORS['accent_subtle']};
        }}
        QTextEdit:focus {{
            border-color: {COLORS['accent']};
        }}
    """


def get_combobox_stylesheet() -> str:
    """获取下拉框样式"""
    return f"""
        QComboBox {{
            background: {COLORS['bg_input']};
            border: 1.5px solid {COLORS['border_medium']};
            border-radius: 10px;
            padding: 8px 12px;
            font-size: 13px;
            color: {COLORS['text_primary']};
            min-width: 80px;
        }}
        QComboBox:focus {{
            border-color: {COLORS['accent']};
        }}
        QComboBox::drop-down {{
            border: none;
            padding-right: 8px;
        }}
        QComboBox::down-arrow {{
            image: none;
            width: 0;
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid {COLORS['text_tertiary']};
        }}
        QComboBox QAbstractItemView {{
            background: {COLORS['bg_ultra_light']};
            border: 1px solid {COLORS['border_medium']};
            border-radius: 10px;
            padding: 4px;
            outline: none;
        }}
        QComboBox QAbstractItemView::item {{
            padding: 8px 12px;
            border-radius: 6px;
            min-height: 28px;
        }}
        QComboBox QAbstractItemView::item:selected {{
            background: {COLORS['accent_subtle']};
            color: {COLORS['text_primary']};
        }}
        QComboBox QAbstractItemView::item:hover {{
            background: {COLORS['bg_hover']};
        }}
    """


def get_checkbox_stylesheet() -> str:
    """获取复选框样式"""
    return f"""
        QCheckBox {{
            color: {COLORS['text_primary']};
            font-size: 13px;
            spacing: 10px;
            border: none;
            background: transparent;
        }}
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border: 2px solid {COLORS['border_strong']};
            border-radius: 6px;
            background: {COLORS['bg_input']};
        }}
        QCheckBox::indicator:hover {{
            border-color: {COLORS['accent']};
        }}
        QCheckBox::indicator:checked {{
            background: {COLORS['accent']};
            border-color: {COLORS['accent']};
        }}
    """


def get_btn_primary_stylesheet() -> str:
    """获取主要按钮样式"""
    return f"""
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 {COLORS['accent_light']},
                                        stop:1 {COLORS['accent']});
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.2px;
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 {COLORS['accent']},
                                        stop:1 {COLORS['accent_dark']});
        }}
        QPushButton:pressed {{
            background: {COLORS['accent_dark']};
        }}
        QPushButton:disabled {{
            background: {COLORS['border_medium']};
            color: {COLORS['text_tertiary']};
        }}
    """


def get_btn_secondary_stylesheet() -> str:
    """获取次要按钮样式"""
    return f"""
        QPushButton {{
            background: {COLORS['bg_light']};
            color: {COLORS['text_primary']};
            border: 1.5px solid {COLORS['border_medium']};
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background: {COLORS['bg_ultra_light']};
            border-color: {COLORS['border_strong']};
        }}
        QPushButton:pressed {{
            background: {COLORS['bg_pressed']};
        }}
    """


def get_btn_danger_stylesheet() -> str:
    """获取危险按钮样式"""
    return f"""
        QPushButton {{
            background: transparent;
            color: {COLORS['error']};
            border: 1.5px solid rgba(255, 59, 48, 0.3);
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background: rgba(255, 59, 48, 0.06);
            border-color: rgba(255, 59, 48, 0.5);
        }}
        QPushButton:pressed {{
            background: rgba(255, 59, 48, 0.10);
        }}
    """


def get_btn_close_stylesheet() -> str:
    """获取关闭按钮样式"""
    return f"""
        QPushButton {{
            color: {COLORS['text_tertiary']};
            background: transparent;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 400;
            min-width: 28px;
            min-height: 28px;
        }}
        QPushButton:hover {{
            background: rgba(255, 59, 48, 0.1);
            color: {COLORS['error']};
        }}
        QPushButton:pressed {{
            background: rgba(255, 59, 48, 0.15);
        }}
    """


def get_list_stylesheet() -> str:
    """获取列表样式"""
    return f"""
        QListWidget {{
            background: {COLORS['bg_input']};
            border: 1.5px solid {COLORS['border_light']};
            border-radius: 14px;
            padding: 6px;
            outline: none;
        }}
        QListWidget::item {{
            padding: 12px 14px;
            border-radius: 10px;
            margin: 2px 0;
            border: none;
        }}
        QListWidget::item:selected {{
            background: {COLORS['accent_subtle']};
            color: {COLORS['text_primary']};
        }}
        QListWidget::item:hover {{
            background: {COLORS['bg_hover']};
        }}
    """


def get_scrollbar_stylesheet() -> str:
    """获取滚动条样式"""
    return f"""
        QScrollBar:vertical {{
            background: transparent;
            width: 8px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: rgba(0, 0, 0, 0.15);
            border-radius: 4px;
            min-height: 40px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: rgba(0, 0, 0, 0.25);
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


def get_section_label_stylesheet() -> str:
    """获取分组标签样式"""
    return f"""
        QLabel {{
            color: {COLORS['text_secondary']};
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            border: none;
            background: transparent;
        }}
    """


def get_status_stylesheet() -> str:
    """获取状态栏样式"""
    return f"""
        QLabel {{
            color: {COLORS['text_tertiary']};
            font-size: 11px;
            font-weight: 400;
            border: none;
            background: transparent;
        }}
    """


def get_chat_bubble_user() -> str:
    """获取用户消息气泡样式"""
    return f"""
        background: {COLORS['accent_subtle']};
        border-radius: 16px 16px 4px 16px;
        padding: 12px 16px;
        margin: 4px 0;
    """


def get_chat_bubble_ai() -> str:
    """获取 AI 消息气泡样式"""
    return f"""
        background: {COLORS['bg_light']};
        border: 1px solid {COLORS['border_light']};
        border-radius: 16px 16px 16px 4px;
        padding: 12px 16px;
        margin: 4px 0;
    """


def get_shadow_effect(blur_radius: int = 40, offset_y: int = 8, opacity: int = 25):
    """获取阴影效果参数"""
    return {
        "blur_radius": blur_radius,
        "color": f"rgba(0, 0, 0, {opacity / 100:.2f})",
        "offset_y": offset_y,
    }
