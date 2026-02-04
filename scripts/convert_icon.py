"""
将 SVG 图标转换为 Windows ICO 格式。
需要安装: pip install cairosvg pillow
"""
import io
import sys
from pathlib import Path

try:
    import cairosvg
    from PIL import Image
except ImportError:
    print("请先安装依赖: pip install cairosvg pillow")
    sys.exit(1)


def svg_to_ico(svg_path: Path, ico_path: Path, sizes: list[int] | None = None):
    """将 SVG 转换为包含多种尺寸的 ICO 文件"""
    if sizes is None:
        sizes = [16, 32, 48, 64, 128, 256]

    images = []
    for size in sizes:
        png_data = cairosvg.svg2png(url=str(svg_path), output_width=size, output_height=size)
        img = Image.open(io.BytesIO(png_data))
        images.append(img)

    images[0].save(ico_path, format="ICO", sizes=[(s, s) for s in sizes], append_images=images[1:])
    print(f"已生成: {ico_path}")


if __name__ == "__main__":
    root = Path(__file__).parent.parent
    svg_path = root / "assets" / "icon.svg"
    ico_path = root / "assets" / "icon.ico"

    if not svg_path.exists():
        print(f"找不到 SVG 文件: {svg_path}")
        sys.exit(1)

    svg_to_ico(svg_path, ico_path)
