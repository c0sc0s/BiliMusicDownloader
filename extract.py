"""
从 B 站视频提取纯音频。支持命令行和作为模块调用。
依赖: yt-dlp (支持 bilibili.com)
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

import yt_dlp


BILIBILI_URL_PATTERN = re.compile(
    r"https?://(?:www\.)?bilibili\.com/video/(BV[\w]+)",
    re.IGNORECASE,
)


def is_bilibili_video_url(url: str) -> bool:
    return bool(BILIBILI_URL_PATTERN.search(url))


def _is_valid_ffmpeg(path: str) -> bool:
    if not path or not os.path.isfile(path):
        return False
    try:
        result = subprocess.run(
            [path, "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2,
        )
        return result.returncode == 0
    except Exception:
        return False


def _iter_windows_app_paths() -> list[str]:
    try:
        import winreg
    except Exception:
        return []
    results = []
    for root in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        try:
            key = winreg.OpenKey(
                root, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\ffmpeg.exe"
            )
            value, _ = winreg.QueryValueEx(key, None)
            if value:
                results.append(value)
            try:
                base, _ = winreg.QueryValueEx(key, "Path")
                if base:
                    results.append(os.path.join(base, "ffmpeg.exe"))
            except Exception:
                pass
            winreg.CloseKey(key)
        except Exception:
            pass
    return results


def resolve_ffmpeg_path() -> str | None:
    env_path = os.environ.get("FFMPEG_PATH") or os.environ.get("BILI_MUSIC_FFMPEG")
    candidates = []
    if env_path:
        env_path = env_path.strip().strip('"').strip("'")
        if os.path.isdir(env_path):
            candidates.append(os.path.join(env_path, "ffmpeg.exe"))
        candidates.append(env_path)
    which_path = shutil.which("ffmpeg")
    if which_path:
        candidates.append(which_path)
    base_dirs = []
    if getattr(sys, "frozen", False):
        base_dirs.append(os.path.dirname(sys.executable))
    base_dirs.append(os.path.dirname(os.path.abspath(__file__)))
    for base in base_dirs:
        candidates.append(os.path.join(base, "ffmpeg.exe"))
        candidates.append(os.path.join(base, "bin", "ffmpeg.exe"))
    if os.name == "nt":
        candidates.extend(_iter_windows_app_paths())
        local_appdata = os.environ.get("LOCALAPPDATA")
        if local_appdata:
            candidates.append(os.path.join(local_appdata, "Microsoft", "WinGet", "Links", "ffmpeg.exe"))
            candidates.append(os.path.join(local_appdata, "Microsoft", "WindowsApps", "ffmpeg.exe"))
    candidates.extend(
        [
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\FFmpeg\bin\ffmpeg.exe",
            r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files (x86)\FFmpeg\bin\ffmpeg.exe",
            r"C:\ProgramData\chocolatey\bin\ffmpeg.exe",
        ]
    )
    seen = set()
    for path in candidates:
        if not path:
            continue
        norm = os.path.normpath(path)
        if norm in seen:
            continue
        seen.add(norm)
        if _is_valid_ffmpeg(norm):
            return norm
    return None


def extract_audio(
    url: str,
    output_dir: str = ".",
    audio_format: str = "mp3",
    audio_quality: int = 0,
) -> str:
    """
    从 B 站视频提取音频，返回输出文件路径。

    :param url: 视频页面 URL（如 https://www.bilibili.com/video/BVxxx）
    :param output_dir: 输出目录
    :param audio_format: 音频格式，如 mp3, m4a, aac
    :param audio_quality: 质量 0=最好 9=最小
    :return: 输出文件的绝对路径
    :raises ValueError: URL 不是有效的 B 站视频链接
    :raises yt_dlp.utils.DownloadError: 下载失败
    """
    if not is_bilibili_video_url(url):
        raise ValueError("请输入有效的 B 站视频链接，例如 https://www.bilibili.com/video/BVxxxxx")

    os.makedirs(output_dir, exist_ok=True)
    out_tmpl = os.path.join(output_dir, "%(title).100s [%(id)s].%(ext)s")

    opts = {
        "format": "bestaudio/best",
        "outtmpl": out_tmpl,
        "restrict_filename": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
                "preferredquality": str(audio_quality),
            }
        ],
        "quiet": False,
    }
    ffmpeg_path = resolve_ffmpeg_path()
    if ffmpeg_path:
        opts["ffmpeg_location"] = ffmpeg_path

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if not info:
            raise yt_dlp.utils.DownloadError("无法获取视频信息")
        video_id = info.get("id", "unknown")
        requested = info.get("requested_downloads") or []
        out_path = None
        if requested:
            out_path = requested[0].get("filepath")
        if not out_path or not os.path.isfile(out_path):
            for f in os.listdir(output_dir):
                if video_id in f and f.endswith(f".{audio_format}"):
                    out_path = os.path.join(output_dir, f)
                    break
        if not out_path or not os.path.isfile(out_path):
            raise yt_dlp.utils.DownloadError("未找到输出文件")
        return os.path.abspath(out_path)


def main():
    parser = argparse.ArgumentParser(description="从 B 站视频提取音频")
    parser.add_argument("url", help="B 站视频链接，如 https://www.bilibili.com/video/BVxxxxx")
    parser.add_argument("-o", "--output-dir", default=".", help="输出目录（默认当前目录）")
    parser.add_argument("-f", "--format", default="mp3", choices=["mp3", "m4a", "aac"], help="音频格式")
    parser.add_argument("-q", "--quality", type=int, default=0, help="质量 0=最好 9=最小")
    args = parser.parse_args()

    try:
        path = extract_audio(
            args.url,
            output_dir=args.output_dir,
            audio_format=args.format,
            audio_quality=args.quality,
        )
        print(f"已保存: {path}")
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"提取失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
