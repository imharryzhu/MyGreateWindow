
import sys
import os
import subprocess
from pathlib import Path

script_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_path)

def build_mac_app():
    print("Building macOS application...")

    cmd = [
        sys.executable, 
        '-m', 'nuitka',
        '--mode=app',
        '--enable-plugin=pyside6',
        f'{project_root}/src/main.py',
        f'--output-dir={project_root}/build_mac_app',
    ]
    subprocess.run(cmd)

def build_win_app():
    print("Building Windows application...")

    cmd = [
        sys.executable, 
        '-m', 'nuitka',
        '--standalone',
        '--windows-console-mode=disable',
        '--enable-plugin=pyside6',
        f'{project_root}/src/main.py',
        f'--output-dir={project_root}/build_win_app',
    ]
    subprocess.run(cmd)


if __name__ == "__main__":
    print(project_root  )
    if sys.platform == "darwin":
        build_mac_app()
    if sys.platform == "win32":
        build_win_app()
