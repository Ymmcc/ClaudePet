import json
import os
from pathlib import Path


CONFIG_DIR = Path.home() / ".claudepet"
CONFIG_FILE = CONFIG_DIR / "config.json"
TODOS_FILE = CONFIG_DIR / "todos.json"

DEFAULT_CONFIG = {
    "pet_x": -1,
    "pet_y": -1,
    "autostart": False,
    "api_provider": "deepseek",
    "api_key": "",
    "api_base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",
    "pet_name": "Claude",
    "language": "zh",
    "animation_speed": 100,
    "behavior_interval": 15,
}


def ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    ensure_config_dir()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            merged = {**DEFAULT_CONFIG, **saved}
            return merged
        except (json.JSONDecodeError, IOError):
            pass
    return dict(DEFAULT_CONFIG)


def save_config(config: dict):
    ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_todos() -> list:
    ensure_config_dir()
    if TODOS_FILE.exists():
        try:
            with open(TODOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []


def save_todos(todos: list):
    ensure_config_dir()
    with open(TODOS_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)
