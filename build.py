"""
ClaudePet 打包脚本
使用 PyInstaller 将项目打包成 exe，不会显示终端窗口
"""
import subprocess
import sys
import os

def main():
    # 确保安装了 pyinstaller
    try:
        import PyInstaller
    except ImportError:
        print("正在安装 PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--windowed",               # 不显示终端窗口
        "--name", "ClaudePet",      # exe 名称
        "--clean",                  # 清理临时文件
        "main.py"
    ]

    print("开始打包 ClaudePet...")
    print(f"执行命令: {' '.join(cmd)}")
    subprocess.check_call(cmd)

    print("\n打包完成！")
    print(f"exe 文件位于: {os.path.join(os.getcwd(), 'dist', 'ClaudePet.exe')}")

if __name__ == "__main__":
    main()
