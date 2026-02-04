# BiliMusic

<p align="center">
  <img src="assets/icon.svg" width="128" height="128" alt="BiliMusic Logo">
</p>

<p align="center">
  <strong>从 B 站视频提取纯音频的桌面工具</strong>
</p>

<p align="center">
  <a href="https://github.com/c0sc0s/BiliMusicDownloader/releases/latest">
    <img src="https://img.shields.io/github/v/release/c0sc0s/BiliMusicDownloader?style=flat-square" alt="Release">
  </a>
  <a href="https://github.com/c0sc0s/BiliMusicDownloader/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/c0sc0s/BiliMusicDownloader?style=flat-square" alt="License">
  </a>
  <a href="https://github.com/c0sc0s/BiliMusicDownloader/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/c0sc0s/BiliMusicDownloader/release.yml?style=flat-square" alt="Build">
  </a>
</p>

---

## 功能特性

- 从 B 站视频提取纯音频（MP3 / M4A / AAC）
- Windows 桌面应用，单文件 exe，无需安装
- 所有处理在本地执行，无需联网到第三方服务器
- 现代深色 UI，简洁易用
- 支持命令行和 Web 界面
- FFmpeg 环境检测与安装引导

## 下载

前往 [Releases](https://github.com/c0sc0s/BiliMusicDownloader/releases/latest) 页面下载最新版本：

- **Windows**: `BiliMusic.exe`（单文件，双击运行）

## 使用前提

需要在系统中安装 **FFmpeg**（用于音频转码）：

```powershell
# Windows (推荐)
winget install FFmpeg

# 或从官网下载
# https://ffmpeg.org/download.html
```

安装后，打开新的终端窗口，运行 `ffmpeg -version` 确认安装成功。

## 使用方法

### 桌面应用

1. 双击运行 `BiliMusic.exe`
2. 粘贴 B 站视频链接（如 `https://www.bilibili.com/video/BVxxxxx`）
3. 选择音频格式（MP3 / M4A / AAC）
4. 点击「提取音频」
5. 完成后自动下载，文件保存在 exe 所在目录的 `downloads/` 文件夹

### 命令行

```bash
# 基本用法：提取为 MP3
python extract.py "https://www.bilibili.com/video/BVxxxxx"

# 指定输出目录和格式
python extract.py "https://www.bilibili.com/video/BVxxxxx" -o ./output -f m4a

# 参数说明
#   -o, --output-dir  输出目录（默认当前目录）
#   -f, --format      mp3 | m4a | aac（默认 mp3）
#   -q, --quality     0=最好 9=最小（默认 0）
```

### Web 界面（开发用）

```bash
pip install -r requirements.txt
python app.py
# 打开 http://127.0.0.1:5000
```

## 从源码构建

### 环境要求

- Python 3.10+
- FFmpeg（需加入 PATH）

### 安装依赖

```bash
git clone https://github.com/c0sc0s/BiliMusicDownloader.git
cd BiliMusicDownloader
pip install -r requirements.txt
```

### 运行桌面版

```bash
python desktop.py
```

### 打包为 exe

```bash
# Windows
build.bat

# 生成: dist/BiliMusic.exe
```

## 项目结构

```
BiliMusicDownloader/
├── app.py              # Flask Web 后端
├── desktop.py          # 桌面应用入口（pywebview）
├── extract.py          # 音频提取核心逻辑
├── build.bat           # Windows 打包脚本
├── requirements.txt    # Python 依赖
├── templates/
│   └── index.html      # 前端界面
├── assets/
│   ├── icon.svg        # 应用图标（源文件）
│   └── icon.ico        # 应用图标（Windows）
├── scripts/
│   └── convert_icon.py # SVG → ICO 转换脚本
├── .github/
│   └── workflows/
│       └── release.yml # GitHub Actions CI/CD
├── LICENSE             # MIT 协议
├── CHANGELOG.md        # 更新日志
└── README.md           # 本文件
```

## 技术栈

- **后端**: Python, Flask
- **桌面封装**: pywebview
- **视频下载**: yt-dlp
- **音频转码**: FFmpeg
- **打包**: PyInstaller
- **CI/CD**: GitHub Actions

## 常见问题

### 提取失败怎么办？

1. 检查 FFmpeg 是否正确安装：`ffmpeg -version`
2. 确认视频链接格式正确（需包含 `bilibili.com/video/BV...`）
3. 部分视频可能有地区限制或需要登录

### 如何配置 Cookie（登录后的视频）？

目前暂不支持 Cookie 配置，后续版本会添加。

### 支持其他平台吗？

目前仅提供 Windows 版本。macOS / Linux 可从源码运行。

## 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/xxx`
3. 提交更改：`git commit -m "Add xxx"`
4. 推送分支：`git push origin feature/xxx`
5. 提交 Pull Request

## 许可证

[MIT License](LICENSE)

## 免责声明

本工具仅供个人学习与备份使用。请勿用于侵犯版权的行为，用户需自行承担使用风险。本项目与 Bilibili 官方无任何关联。

---

<p align="center">
  Made with ❤️ for music lovers
</p>
