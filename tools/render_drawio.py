# -*- coding: utf-8 -*-
"""无 draw.io 桌面版时的应急渲染器：把 .drawio 渲染成 PNG（几何与 draw.io 一致）。

正式流程仍然是 draw.io 命令行导出（见 docs/绘图规范.md 第 6 节）。
支持 跳线 样式：带 jumpStyle=arc 的连线在与其它线交叉处留缺口并画小半圆桥。本脚本只用于
没有安装 draw.io 的机器，保证"脚本 → .drawio → PNG"这条链路在任何机器上都能走通；
导出后统一跑 tools/postprocess_png.py 裁边。

用法：
    python tools/render_drawio.py docs/交付/xxx/images/*.drawio
    python tools/render_drawio.py 某张图.drawio --scale 3
"""
import argparse
import math
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_DIRS = [Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts",
             Path.home() / "AppData/Local/Microsoft/Windows/Fonts"]


def _font_path(bold):
    name = "msyhbd.ttc" if bold else "msyh.ttc"
    for d in FONT_DIRS:
        p = d / name
        if p.exists():
            return str(p)
    raise SystemExit("找不到 Microsoft YaHei 字体，请安装微软雅黑后再渲染。")


_font_cache = {}


def font(size_px, bold=False):
    key = (size_px, bold)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(_font_path(bold), int(size_px))
    return _font_cache[key]


def parse_style(s):
    kv = {}
    for item in s.split(";"):
        if "=" in item:
            k, v = item.split("=", 1)
            kv[k] = v
    return kv


def parse_dashed(kv):
    return kv.get("dashed") == "1"


def dashed_line(draw, p0, p1, fill, width, dash, gap):
    x0, y0 = p0
    x1, y1 = p1
    length = math.hypot(x1 - x0, y1 - y0)
    if length == 0:
        return
    dx, dy = (x1 - x0) / length, (y1 - y0) / length
    t = 0.0
    while t < length:
        t2 = min(t + dash, length)
        draw.line([(x0 + dx * t, y0 + dy * t), (x0 + dx * t2, y0 + dy * t2)],
                  fill=fill, width=width)
        t = t2 + gap


def dashed_poly(draw, pts, fill, width, dash, gap):
    for a, b in zip(pts, pts[1:]):
        dashed_line(draw, a, b, fill, width, dash, gap)


def rounded_rect_path(x, y, w, h, r, steps=6):
    """圆角矩形轮廓点（顺时针）。"""
    r = max(0, min(r, w / 2, h / 2))
    pts = []
    corners = [
        (x + w - r, y + r, -90), (x + w - r, y + h - r, 0),
        (x + r, y + h - r, 90), (x + r, y + r, 180),
    ]
    for cx, cy, a0 in corners:
        for i in range(steps + 1):
            t = math.radians(a0 + i * 90 / steps)
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    pts.append(pts[0])
    return pts


def draw_arrow(draw, prev, tip, color, width, kv, scale=1):
    style = kv.get("endArrow", "block")
    if style == "none":
        return
    size = float(kv.get("endSize", 8)) * scale
    ang = math.atan2(tip[1] - prev[1], tip[0] - prev[0])
    if style == "open" or kv.get("endFill") == "0":
        for s in (math.radians(26), -math.radians(26)):
            draw.line([tip, (tip[0] - size * math.cos(ang + s),
                             tip[1] - size * math.sin(ang + s))], fill=color, width=width)
    else:
        a = (tip[0] - size * math.cos(ang - math.radians(20)),
             tip[1] - size * math.sin(ang - math.radians(20)))
        b = (tip[0] - size * math.cos(ang + math.radians(20)),
             tip[1] - size * math.sin(ang + math.radians(20)))
        draw.polygon([tip, a, b], fill=color)


def wrap_text(text, fnt, max_w):
    lines = []
    for raw in text.split("\n"):
        cur = ""
        for ch in raw:
            if fnt.getlength(cur + ch) <= max_w or not cur:
                cur += ch
            else:
                lines.append(cur)
                cur = ch
        lines.append(cur)
    return lines


def seg_cross_t(p1, p2, p3, p4):
    """两线段是否真正相交；返回交点在线段 1 上的参数 t（0~1），不相交返回 None。"""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if abs(d) < 1e-9:
        return None
    t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d
    u = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d
    if 0.02 < t < 0.98 and 0.02 < u < 0.98:
        return t
    return None


def draw_jump_arc(draw, a, b, t, color, width, r):
    """在交叉点画跨越半圆：水平段向上拱，竖直段向右拱。"""
    cx = a[0] + t * (b[0] - a[0])
    cy = a[1] + t * (b[1] - a[1])
    box = [cx - r, cy - r, cx + r, cy + r]
    if abs(b[0] - a[0]) >= abs(b[1] - a[1]):
        draw.arc(box, 180, 360, fill=color, width=width)   # 上半圆
    else:
        draw.arc(box, 270, 90, fill=color, width=width)    # 右半圆


def draw_edge(draw, pts, kv, scale, per_seg_gaps=None, r=0):
    color = kv.get("strokeColor", "#4A5A6A")
    width = max(2, round(float(kv.get("strokeWidth", 1.5)) * scale))
    if parse_dashed(kv):
        dashed_poly(draw, pts, color, width, 6 * scale, 4 * scale)
        return
    gaps = per_seg_gaps or [[] for _ in pts[1:]]
    for (a, b), ts in zip(zip(pts, pts[1:]), gaps):
        length = math.hypot(b[0] - a[0], b[1] - a[1])
        if length == 0:
            continue
        cur = 0.0
        for t in sorted(ts):
            ta = max(0.0, t - r / length)
            tb = min(1.0, t + r / length)
            if ta > cur:
                draw.line([(a[0] + cur * (b[0] - a[0]), a[1] + cur * (b[1] - a[1])),
                           (a[0] + ta * (b[0] - a[0]), a[1] + ta * (b[1] - a[1]))],
                          fill=color, width=width)
            draw_jump_arc(draw, a, b, t, color, width, r)
            cur = max(cur, tb)
        if cur < 1.0:
            draw.line([(a[0] + cur * (b[0] - a[0]), a[1] + cur * (b[1] - a[1])),
                       (b[0], b[1])], fill=color, width=width)
    draw_arrow(draw, pts[-2], pts[-1], color, width, kv, scale)


def draw_text(draw, text, x, y, w, h, kv, scale, bg=False):
    if not text:
        return
    size = float(kv.get("fontSize", 12)) * scale
    bold = kv.get("fontStyle") == "1"
    fnt = font(size, bold)
    color = kv.get("fontColor", "#222222")
    align = kv.get("align", "center")
    valign = kv.get("verticalAlign", "middle")
    pad_l = float(kv.get("spacingLeft", 0)) * scale
    pad_r = float(kv.get("spacingRight", 4)) * scale
    pad_t = float(kv.get("spacingTop", 0)) * scale
    lines = wrap_text(text, fnt, max(10, w - pad_l - pad_r))
    gap = size * 0.35
    heights = []
    for ln in lines:
        b = draw.textbbox((0, 0), ln or "　", font=fnt)
        heights.append(b[3] - b[1])
    line_h = max(heights) + gap if heights else size
    total = line_h * len(lines) - gap
    if valign == "top":
        ty = y + pad_t
    elif valign == "bottom":
        ty = y + h - total
    else:
        ty = y + (h - total) / 2
    if bg:
        bx0, by0 = x + 2, ty - 3
        bx1, by1 = x + w - 2, ty + total + 3
        draw.rectangle([bx0, by0, bx1, by1], fill="white")
    for ln in lines:
        b = draw.textbbox((0, 0), ln or "　", font=fnt)
        tw = b[2] - b[0]
        if align == "left":
            tx = x + pad_l
        elif align == "right":
            tx = x + w - pad_r - tw
        else:
            tx = x + (w - tw) / 2
        draw.text((tx - b[0], ty - b[1]), ln or "　", font=fnt, fill=color)
        ty += line_h


def draw_actor(draw, x, y, w, h, kv, scale):
    stroke = kv.get("strokeColor", "#1F2A35")
    width = max(2, round(float(kv.get("strokeWidth", 1.5)) * scale))
    cx = x + w / 2
    r = w * 0.24
    cy = y + r + 1
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=stroke, width=width, fill="white")
    body_top = cy + r
    body_bot = y + h * 0.74
    draw.line([(cx, body_top), (cx, body_bot)], fill=stroke, width=width)
    arm_y = y + h * 0.40
    draw.line([(cx - w * 0.38, arm_y), (cx + w * 0.38, arm_y)], fill=stroke, width=width)
    draw.line([(cx, body_bot), (cx - w * 0.32, y + h)], fill=stroke, width=width)
    draw.line([(cx, body_bot), (cx + w * 0.32, y + h)], fill=stroke, width=width)
    draw_text(draw, kv.get("value", ""), x - 40 * scale, y + h + 2 * scale,
              160 * scale, 22 * scale,
              dict(kv, align="center", verticalAlign="top", fontSize="14"), scale)


def draw_vertex(draw, value, kv, x, y, w, h, scale):
    stroke = kv.get("strokeColor", "#444444")
    fill = kv.get("fillColor", "#FFFFFF")
    width = max(2, round(float(kv.get("strokeWidth", 1)) * scale))
    dashed = parse_dashed(kv)
    outline = None if stroke == "none" else stroke
    fill_color = None if fill in ("none", "") else fill
    raw = kv.get("_raw", "")
    shape = kv.get("shape", "")
    if shape == "umlActor":
        draw_actor(draw, x, y, w, h, dict(kv, value=value), scale)
        return
    if "ellipse" in raw or "ellipse" in shape:
        draw.ellipse([x, y, x + w, y + h], outline=outline, width=width, fill=fill_color)
    elif "rhombus" in raw or shape == "rhombus":
        draw.polygon([(x + w / 2, y), (x + w, y + h / 2), (x + w / 2, y + h), (x, y + h / 2)],
                     outline=outline, width=width, fill=fill_color)
    elif kv.get("rounded") == "1":
        r = max(2, min(w, h) * 0.12)
        if dashed:
            pts = rounded_rect_path(x, y, w, h, r)
            dashed_poly(draw, pts, stroke, width, 6 * scale, 4 * scale)
        else:
            draw.rounded_rectangle([x, y, x + w, y + h], radius=r, outline=outline,
                                   width=width, fill=fill_color)
    else:
        if dashed:
            dashed_poly(draw, [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)],
                        stroke, width, 6 * scale, 4 * scale)
        else:
            draw.rectangle([x, y, x + w, y + h], outline=outline, width=width,
                           fill=fill_color)
    draw_text(draw, value, x, y, w, h, kv, scale)


def render(src, scale=2):
    model = ET.parse(src).getroot().find(".//mxGraphModel")
    W = int(model.get("pageWidth")) * scale
    H = int(model.get("pageHeight")) * scale
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    vertices, edges = [], []
    for cell in model.iter("mxCell"):
        geo = cell.find("mxGeometry")
        if geo is None:
            continue
        if cell.get("vertex") == "1":
            vertices.append((
                cell.get("value") or "",
                dict(parse_style(cell.get("style") or ""),
                     _raw=cell.get("style") or ""),
                float(geo.get("x", 0)) * scale, float(geo.get("y", 0)) * scale,
                float(geo.get("width", 0)) * scale, float(geo.get("height", 0)) * scale,
            ))
        elif cell.get("edge") == "1":
            sp = geo.find("mxPoint[@as='sourcePoint']")
            tp = geo.find("mxPoint[@as='targetPoint']")
            arr = geo.find("Array")
            way = [(float(p.get("x")) * scale, float(p.get("y")) * scale)
                   for p in arr] if arr is not None else []
            edges.append((parse_style(cell.get("style") or ""),
                          (float(sp.get("x")) * scale, float(sp.get("y")) * scale) if sp is not None else None,
                          (float(tp.get("x")) * scale, float(tp.get("y")) * scale) if tp is not None else None,
                          way, cell.get("source"), cell.get("target")))

    def is_text(kv):
        return kv.get("fillColor") == "none" and kv.get("strokeColor") == "none"

    # 1) 图形（底板、框、类框、小人……）
    for value, kv, x, y, w, h in vertices:
        if is_text(kv):
            continue
        draw_vertex(draw, value, kv, x, y, w, h, scale)

    # 2) 连线：普通线先画；带 jumpStyle 的线后画（交叉处留缺口 + 画跨越半圆）
    edge_data = [(kv, [sp] + way + [tp]) for kv, sp, tp, way, _, _ in edges
                 if sp is not None and tp is not None]
    normal_segs = []
    for kv, pts in edge_data:
        if not kv.get("jumpStyle"):
            normal_segs.extend(list(zip(pts, pts[1:])))
    for kv, pts in edge_data:
        if not kv.get("jumpStyle"):
            draw_edge(draw, pts, kv, scale)
    for kv, pts in edge_data:
        if not kv.get("jumpStyle"):
            continue
        r = float(kv.get("jumpSize", 6)) * scale
        per_seg = []
        for a, b in zip(pts, pts[1:]):
            ts = []
            for c, d in normal_segs:
                t = seg_cross_t(a, b, c, d)
                if t is not None:
                    ts.append(t)
            per_seg.append(ts)
        draw_edge(draw, pts, kv, scale, per_seg, r)

    # 3) 纯文字标签（最后画，白底衬字压住连线）
    for value, kv, x, y, w, h in vertices:
        if not is_text(kv):
            continue
        draw_text(draw, value, x, y, w, h, kv, scale, bg=True)

    out = Path(src).with_suffix(".png")
    img.save(out)
    print(f"rendered: {out} ({W}x{H})")


def main():
    ap = argparse.ArgumentParser(description="把 .drawio 渲染为 PNG（无 draw.io 时的应急方案）")
    ap.add_argument("files", nargs="+", help=".drawio 文件或目录")
    ap.add_argument("--scale", type=int, default=2)
    args = ap.parse_args()
    targets = []
    for f in args.files:
        p = Path(f)
        targets.extend(sorted(p.glob("*.drawio")) if p.is_dir() else [p])
    for t in targets:
        render(t, args.scale)


if __name__ == "__main__":
    sys.exit(main())
