# ClaudePet

一个 Windows 桌面宠物应用，使用像素风格的 Claude Code 猫咪吉祥物。基于 Python + PyQt6 构建，支持 AI 聊天和待办事项管理。

## 功能

- 像素动画桌宠，支持待机、行走、跳跃、挥手、编程等多种状态
- 右键菜单：聊天、待办事项、喂食、休息、设置、隐藏
- AI 聊天集成（兼容 OpenAI API 格式，支持 DeepSeek 等模型）
- 待办事项管理，支持优先级和到期提醒
- 拖拽交互，双击跳跃
- 系统托盘驻留
- 开机自启动

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

## 配置

首次运行后，在右键菜单 → 设置中配置 API Key 和模型参数。配置文件存储在用户主目录的 `~/.claudepet/config.json`，不会随项目泄露。

支持的 AI 模型（默认 DeepSeek）：
- DeepSeek：`https://api.deepseek.com/v1`
- 其他兼容 OpenAI 格式的 API

## 项目结构

```
ClaudePet/
├── main.py              # 应用入口
├── core/                # 核心逻辑
│   ├── pet_window.py    # 桌宠主窗口
│   ├── sprite_engine.py # 精灵图渲染引擎
│   ├── animation.py     # 动画状态机
│   ├── emotion.py       # 心情系统
│   ├── behaviors.py     # 随机行为控制器
│   ├── chat_window.py   # AI 聊天窗口
│   └── todo_manager.py  # 待办事项管理
├── ui/                  # UI 组件
│   ├── tray.py          # 系统托盘
│   ├── todo_panel.py    # 待办面板
│   ├── settings_dialog.py # 设置对话框
│   ├── reminder_popup.py # 提醒弹窗
│   ├── styles.py        # 全局样式
│   └── design_tokens.py # 设计规范
├── utils/               # 工具模块
│   ├── config.py        # 配置持久化
│   └── autostart.py     # 开机自启动
└── assets/              # 资源文件
    └── clawd/           # Clawd 精灵图
```

## 系统要求

- Windows 10+
- Python 3.10+
- PyQt6
