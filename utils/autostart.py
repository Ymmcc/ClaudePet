import sys
import os
import subprocess
from pathlib import Path


STARTUP_DIR = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
SHORTCUT_PATH = STARTUP_DIR / "ClaudePet.lnk"


def get_executable_path() -> str:
    if getattr(sys, "frozen", False):
        return sys.executable
    else:
        # 开发模式下返回 exe 路径（假设已打包）
        dist_exe = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "dist" / "ClaudePet.exe"
        if dist_exe.exists():
            return str(dist_exe)
        # 如果没有打包，返回 python 命令
        main_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py"
        )
        return f'"{sys.executable}" "{main_path}"'


def is_autostart_enabled() -> bool:
    return SHORTCUT_PATH.exists()


def enable_autostart():
    exe_path = get_executable_path()
    work_dir = os.path.dirname(exe_path)

    # 使用 PowerShell 创建快捷方式
    ps_script = f'''
    $ws = New-Object -ComObject WScript.Shell
    $s = $ws.CreateShortcut('{SHORTCUT_PATH}')
    $s.TargetPath = '{exe_path}'
    $s.WorkingDirectory = '{work_dir}'
    $s.Save()
    '''
    subprocess.run(
        ["powershell", "-Command", ps_script],
        capture_output=True, creationflags=0x08000000
    )


def disable_autostart():
    if SHORTCUT_PATH.exists():
        SHORTCUT_PATH.unlink()
