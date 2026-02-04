"""
Web 界面：输入 B 站视频链接，提取并下载音频。
"""
import os
import shutil
import urllib.parse

from flask import Flask, jsonify, render_template, request, send_file, url_for

from extract import extract_audio, is_bilibili_video_url


def check_ffmpeg() -> bool:
    """检查系统是否安装了 FFmpeg"""
    return shutil.which("ffmpeg") is not None

app = Flask(__name__)
_root = os.environ.get("BILI_MUSIC_APP_ROOT") or os.path.dirname(os.path.abspath(__file__))
if os.environ.get("BILI_MUSIC_APP_ROOT"):
    app.root_path = _root
DOWNLOAD_DIR = os.environ.get("BILI_MUSIC_DOWNLOAD_DIR") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "downloads"
)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/check-env")
def check_env():
    """检查运行环境（FFmpeg 等）"""
    return jsonify({"ffmpeg": check_ffmpeg()})


@app.route("/extract", methods=["POST"])
def extract():
    url = (request.form.get("url") or "").strip()
    if not url:
        return jsonify({"error": "请输入视频链接"}), 400
    if not is_bilibili_video_url(url):
        return jsonify({"error": "请输入有效的 B 站视频链接"}), 400

    fmt = request.form.get("format", "mp3")
    if fmt not in ("mp3", "m4a", "aac"):
        fmt = "mp3"

    try:
        out_path = extract_audio(
            url,
            output_dir=DOWNLOAD_DIR,
            audio_format=fmt,
            audio_quality=0,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"提取失败: {e}"}), 500

    filename = os.path.basename(out_path)
    download_url = url_for("download", filename=filename)
    return jsonify({"download_url": download_url})


@app.route("/download/<path:filename>")
def download(filename):
    filename = urllib.parse.unquote(filename)
    path = os.path.normpath(os.path.join(DOWNLOAD_DIR, filename))
    if os.path.commonpath([path, DOWNLOAD_DIR]) != DOWNLOAD_DIR or not os.path.isfile(path):
        return "文件不存在或已清理", 404
    return send_file(
        path,
        as_attachment=True,
        download_name=filename,
        mimetype="audio/mpeg" if filename.lower().endswith(".mp3") else "audio/mp4",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
