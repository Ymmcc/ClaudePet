import sys
import os
import subprocess


TASK_NAME = "ClaudePetAutoStart"


def get_executable_path() -> str:
    if getattr(sys, "frozen", False):
        return sys.executable
    else:
        main_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py"
        )
        return f'"{sys.executable}" "{main_path}"'


def is_autostart_enabled() -> bool:
    try:
        result = subprocess.run(
            ["schtasks", "/Query", "/TN", TASK_NAME],
            capture_output=True, text=True, creationflags=0x08000000
        )
        return result.returncode == 0
    except Exception:
        return False


def enable_autostart():
    exe_path = get_executable_path()
    work_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(
        [
            "schtasks", "/Create", "/F",
            "/TN", TASK_NAME,
            "/TR", f'cd /d "{work_dir}" && {exe_path}',
            "/SC", "ONLOGON",
            "/DELAY", "0000:30",
            "/RL", "LIMITED",
        ],
        capture_output=True, creationflags=0x08000000
    )


def disable_autostart():
    subprocess.run(
        ["schtasks", "/Delete", "/F", "/TN", TASK_NAME],
        capture_output=True, creationflags=0x08000000
    )
