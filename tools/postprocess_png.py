# -*- coding: utf-8 -*-
"""PNG 统一后处理：裁掉多余白边、四周补统一白边、校验可读性预算。

对 draw.io 命令行导出（按内容包围盒裁剪）或应急渲染器（按整页渲染）的 PNG 都适用。
处理完所有图的四周留白一致，插入 Word 后不会一张大一张小。

用法：
    python tools/postprocess_png.py docs/交付/xxx/images/*.png
    python tools/postprocess_png.py images --margin 32 --scale 2
"""
import argparse
from pathlib import Path

from PIL import Image, ImageChops

WHITE = (255, 255, 255)
# A4 纵向、左右各 2.7cm 页边距时，正文满宽约 15.5cm = 439.4pt
FULL_WIDTH_PT = 439.4


def content_bbox(img):
    diff = ImageChops.difference(img, Image.new("RGB", img.size, WHITE))
    return diff.getbbox()


def process(path, margin=32, scale=2, font_size=14):
    img = Image.open(path).convert("RGB")
    box = content_bbox(img)
    if box is None:
        print(f"跳过（整张空白）: {path}")
        return
    img = img.crop(box)
    w, h = img.size
    canvas = Image.new("RGB", (w + margin * 2, h + margin * 2), WHITE)
    canvas.paste(img, (margin, margin))
    canvas.save(path, optimize=True)

    content_px = w / scale                      # 内容宽度的 drawio 坐标
    eff_pt = font_size * FULL_WIDTH_PT / content_px if content_px else 0
    ratio = (w + margin * 2) / (h + margin * 2)
    flag = "OK" if eff_pt >= 8 else "偏小"
    print(f"{Path(path).name}: {w + margin * 2}x{h + margin * 2}px  "
          f"内容 {content_px:.0f}px  宽高比 {ratio:.2f}  满宽等效字号 {eff_pt:.1f}pt  {flag}")


def main():
    ap = argparse.ArgumentParser(description="统一裁边/补白并检查字号预算")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--margin", type=int, default=32)
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--font-size", type=int, default=14)
    args = ap.parse_args()
    targets = []
    for p in args.paths:
        p = Path(p)
        targets.extend(sorted(p.glob("*.png")) if p.is_dir() else [p])
    for t in targets:
        process(t, args.margin, args.scale, args.font_size)


if __name__ == "__main__":
    main()
