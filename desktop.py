"""
桌面应用入口：用 pywebview 包装 Flask，所有逻辑在本地执行。
运行: python desktop.py
打包: 见 README 或 build/ 下的说明。
"""
import os
import sys

import webview

# 打包成 exe 时，资源在 sys._MEIPASS；下载目录放在 exe 同目录下
if getattr(sys, "frozen", False):
    _base = sys._MEIPASS
    _app_dir = os.path.dirname(sys.executable)
else:
    _base = os.path.dirname(os.path.abspath(__file__))
    _app_dir = _base

# 在导入 app 前注入路径，供 app 使用
os.environ.setdefault("BILI_MUSIC_APP_ROOT", _base)
os.environ.setdefault("BILI_MUSIC_DOWNLOAD_DIR", os.path.join(_app_dir, "downloads"))

from app import app  # noqa: E402

if __name__ == "__main__":
    webview.create_window("B 站视频 → 音频", app, width=480, height=420, resizable=True)
    webview.start(debug=False)
