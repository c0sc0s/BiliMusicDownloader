"""
生成 Windows ICO 图标。
仅依赖 Pillow，无需 cairo 库。
"""
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("请先安装依赖: pip install pillow")
    sys.exit(1)


def create_icon(ico_path: Path, sizes: list[int] | None = None):
    """创建 BiliMusic 图标（程序化生成，无需 SVG）"""
    if sizes is None:
        sizes = [16, 32, 48, 64, 128, 256]

    images = []
    for size in sizes:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 背景圆形 - B站蓝色渐变效果用纯色代替
        margin = int(size * 0.0625)
        draw.ellipse(
            [margin, margin, size - margin, size - margin],
            fill=(0, 161, 214, 255),  # B站蓝
        )

        # 中心白色矩形（电视机主体）
        tv_left = int(size * 0.27)
        tv_top = int(size * 0.31)
        tv_right = int(size * 0.73)
        tv_bottom = int(size * 0.62)
        tv_radius = int(size * 0.03)
        draw.rounded_rectangle(
            [tv_left, tv_top, tv_right, tv_bottom],
            radius=tv_radius,
            fill=(255, 255, 255, 255),
        )

        # 天线
        antenna_width = max(2, int(size * 0.04))
        # 左天线
        draw.line(
            [(int(size * 0.35), tv_top), (int(size * 0.29), int(size * 0.21))],
            fill=(255, 255, 255, 255),
            width=antenna_width,
        )
        # 右天线
        draw.line(
            [(int(size * 0.65), tv_top), (int(size * 0.71), int(size * 0.21))],
            fill=(255, 255, 255, 255),
            width=antenna_width,
        )

        # 眼睛（B站 logo 风格）
        eye_ry = int(size * 0.055)
        eye_rx = int(size * 0.04)
        eye_y = int(size * 0.47)
        # 左眼
        left_eye_x = int(size * 0.39)
        draw.ellipse(
            [left_eye_x - eye_rx, eye_y - eye_ry, left_eye_x + eye_rx, eye_y + eye_ry],
            fill=(0, 161, 214, 255),
        )
        # 右眼
        right_eye_x = int(size * 0.61)
        draw.ellipse(
            [right_eye_x - eye_rx, eye_y - eye_ry, right_eye_x + eye_rx, eye_y + eye_ry],
            fill=(0, 161, 214, 255),
        )

        # 音符（粉色）- 简化版
        note_color = (251, 114, 153, 255)  # B站粉
        note_x = int(size * 0.62)
        note_y = int(size * 0.70)
        note_r = int(size * 0.08)
        # 音符头
        draw.ellipse(
            [note_x - note_r, note_y - note_r // 2, note_x + note_r, note_y + note_r // 2 + note_r],
            fill=note_color,
        )
        # 音符杆
        stem_width = max(2, int(size * 0.025))
        stem_x = note_x + note_r - stem_width // 2
        stem_top = int(size * 0.52)
        draw.rectangle(
            [stem_x, stem_top, stem_x + stem_width, note_y],
            fill=note_color,
        )
        # 音符旗
        flag_points = [
            (stem_x + stem_width, stem_top),
            (stem_x + stem_width + int(size * 0.08), stem_top + int(size * 0.06)),
            (stem_x + stem_width, stem_top + int(size * 0.12)),
        ]
        draw.polygon(flag_points, fill=note_color)

        images.append(img)

    # 保存为 ICO
    images[0].save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[1:],
    )
    print(f"已生成: {ico_path}")


if __name__ == "__main__":
    root = Path(__file__).parent.parent
    ico_path = root / "assets" / "icon.ico"
    ico_path.parent.mkdir(parents=True, exist_ok=True)
    create_icon(ico_path)
