@echo off
REM 打包成 Windows 单文件 exe
REM 生成的 exe 在 dist\ 目录；运行前请确保本机已安装 FFmpeg 并加入 PATH。

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM 检查图标文件，若不存在则尝试生成
if not exist "assets\icon.ico" (
    echo 正在生成图标...
    pip install cairosvg pillow -q
    python scripts\convert_icon.py
)

REM 设置图标参数
set ICON_ARG=
if exist "assets\icon.ico" (
    set ICON_ARG=--icon "assets\icon.ico"
)

echo 正在打包...
pyinstaller --noconfirm ^
  --onefile ^
  --windowed ^
  --name "BiliMusic" ^
  %ICON_ARG% ^
  --add-data "templates;templates" ^
  --add-data "assets;assets" ^
  --hidden-import=webview ^
  --hidden-import=yt_dlp ^
  --collect-all pywebview ^
  desktop.py

echo.
echo ========================================
echo 完成！exe 位置: dist\BiliMusic.exe
echo.
echo 使用前请安装 FFmpeg:
echo   winget install FFmpeg
echo ========================================
pause
