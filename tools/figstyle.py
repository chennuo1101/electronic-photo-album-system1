# -*- coding: utf-8 -*-
"""统一绘图样式与 .drawio 拼装工具（绘图规范 v2）。

各成员脚本在自己交付目录下这样引用：

    import sys
    from pathlib import Path
    ROOT = Path(__file__).resolve().parents[3]      # 脚本 → 交付目录 → 交付 → docs → 项目根
    sys.path.insert(0, str(ROOT / "tools"))
    import figstyle as fs

坐标约定：画布四周留 24px 白边；两线交叉用 SEG_JUMP（jumpStyle=arc）画跨越符号；单张图内容宽度不超过 760px——正文 14px 时，
插入 Word 满宽 15.5cm 后等效字号仍不小于 8pt（详见 docs/绘图规范.md 第 3 节）。

改图流程：改脚本 → 重新生成 .drawio → 导出 PNG → 目检。导出方式见
docs/绘图规范.md 第 6 节（draw.io 命令行优先，无 draw.io 时用 tools/render_drawio.py，
再用 tools/postprocess_png.py 统一裁边）。
"""
from pathlib import Path

# ================= 色板（只承担"分类"，不承担"主次"） =================
MAIN = "#2F5D8A"            # 主色：框线、主流程、强调
MAIN_LIGHT = "#E9F0F8"      # 主色浅填充：系统处理、类名栏、页面/控制对象
CONTAINER_FILL = "#F5F8FB"  # 容器/系统边界填充
CONTAINER_STROKE = "#B7C7D6"
ACCENT = "#B4532A"          # 强调色：扩展/异常，只与虚线一起用
ACCENT_LIGHT = "#FBEFEA"
INK = "#1F2A35"             # 正文
MUTED = "#6B7C8C"           # 次要文字（容器标签、图注性文字）
EDGE = "#4A5A6A"            # 连线
WHITE = "#FFFFFF"

# ================= 字体与样式 =================
FONT = f"fontFamily=Microsoft YaHei;fontSize=14;fontColor={INK};"
FONT_S = f"fontFamily=Microsoft YaHei;fontSize=12;fontColor={INK};"
FONT_MUTED = f"fontFamily=Microsoft YaHei;fontSize=14;fontColor={MUTED};"

# 用户动作：白底 + 主色框
BOX = (f"rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor={WHITE};"
       f"strokeColor={MAIN};strokeWidth=1.5;" + FONT)
# 系统动作：浅主色填充
SYS = (f"rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor={MAIN_LIGHT};"
       f"strokeColor={MAIN};strokeWidth=1.5;" + FONT)
# 扩展/异常提示：浅强调色 + 虚线
NOTE = (f"rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor={ACCENT_LIGHT};"
        f"strokeColor={ACCENT};strokeWidth=1.2;dashed=1;" + FONT)
# 判断
DIAMOND = f"rhombus;whiteSpace=wrap;html=1;fillColor={WHITE};strokeColor={MAIN};strokeWidth=1.5;" + FONT
# 用例椭圆
USECASE = f"ellipse;whiteSpace=wrap;html=1;fillColor={WHITE};strokeColor={MAIN};strokeWidth=1.5;" + FONT
# 系统边界（框名 = 系统名，左上角）
BOUNDARY = ("rounded=0;whiteSpace=wrap;html=1;fillColor=" + CONTAINER_FILL +
            f";strokeColor={CONTAINER_STROKE};strokeWidth=1.5;align=left;verticalAlign=top;"
            f"spacingLeft=16;spacingTop=12;" + FONT_MUTED)
# 参与者：小人图形保持不变（只换线色，不换形状）
ACTOR = (f"shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"
         f"fillColor={WHITE};strokeColor={INK};strokeWidth=1.5;" + FONT)
# 开始 / 结束
START = f"ellipse;html=1;fillColor={MAIN};strokeColor={MAIN};"
END = f"ellipse;html=1;fillColor={WHITE};strokeColor={MAIN};strokeWidth=2.5;"

# 类模型图三栏：标题栏浅主色，属性/方法栏白底
CLASS_TITLE = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={MAIN_LIGHT};strokeColor={MAIN};"
               f"strokeWidth=1.5;align=center;verticalAlign=middle;fontStyle=1;"
               f"fontFamily=Microsoft YaHei;fontSize=14;fontColor={INK};")
CLASS_COMP = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={WHITE};strokeColor={MAIN};"
              f"strokeWidth=1.5;align=left;verticalAlign=top;spacingLeft=10;spacingTop=6;"
              f"fontFamily=Microsoft YaHei;fontSize=13;fontColor={INK};")

# 纯文字标签（默认白底衬字，压线时不会糊）
TEXT = (f"text;html=1;align=center;verticalAlign=middle;fillColor=none;strokeColor=none;"
        f"fontFamily=Microsoft YaHei;fontSize=12;fontColor={INK};")
TEXT_L = TEXT.replace("align=center", "align=left")
TEXT_R = TEXT.replace("align=center", "align=right")
TEXT_S = TEXT.replace("fontSize=12", "fontSize=11")

# 直线段：消息/流程用实心箭头，关联用开放箭头，无箭头用于参与者—用例
SEG = (f"html=1;rounded=0;strokeColor={EDGE};strokeWidth=1.5;startArrow=none;"
       f"endArrow=block;endFill=1;endSize=7;")
SEG_OPEN = (f"html=1;rounded=0;strokeColor={EDGE};strokeWidth=1.5;startArrow=none;"
            f"endArrow=open;endFill=0;endSize=9;")
SEG_NONE = (f"html=1;rounded=0;strokeColor={EDGE};strokeWidth=1.5;"
            f"startArrow=none;endArrow=none;")
# 与其它线交叉时画跨越符号（小半圆桥），避免"裸交叉"看起来像连在一起
SEG_JUMP = SEG + "jumpStyle=arc;jumpSize=6;"
# 拆段后仅作过渡、没有箭头的那一段（箭头由后续段负责）
SEG_JUMP_NONE = (f"html=1;rounded=0;strokeColor={EDGE};strokeWidth=1.5;"
                 f"startArrow=none;endArrow=none;jumpStyle=arc;jumpSize=6;")


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace("\n", "&#xa;"))


def vertex(cid, value, style, x, y, w, h, parent="1"):
    return (f'<mxCell id="{cid}" value="{esc(value)}" style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')


def label(cid, value, x, y, w, h=18, align="center", style=None):
    """纯文字标签。align: center / left / right。"""
    st = style or (TEXT if align == "center" else TEXT_L if align == "left" else TEXT_R)
    return vertex(cid, value, st, x, y, w, h)


def poly(eid, pts, style=SEG):
    """多段折线（两端坐标写死，不吸附图元），箭头画在最后一段末端。"""
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    mids = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in pts[1:-1])
    arr = f'<Array as="points">{mids}</Array>' if mids else ""
    geom = (f'<mxGeometry relative="1" as="geometry">{arr}'
            f'<mxPoint x="{x1}" y="{y1}" as="sourcePoint"/>'
            f'<mxPoint x="{x2}" y="{y2}" as="targetPoint"/></mxGeometry>')
    return f'<mxCell id="{eid}" value="" style="{style}" edge="1" parent="1">{geom}</mxCell>'


def classbox(cid, stereotype, name, attrs, methods, x, y, w, line_h=24, pad=16, title_h=40):
    """三栏类框：标题栏 + 属性栏 + 方法栏三个矩形拼接，栏间共享边框。

    高度按内容自适应（属性/方法为空时保留一行高度），避免出现大片空白。
    """
    h_attrs = max(1, len(attrs)) * line_h + pad
    h_methods = max(1, len(methods)) * line_h + pad
    title = f"«{stereotype}» {name}"
    cells = [
        vertex(cid + "_t", title, CLASS_TITLE, x, y, w, title_h),
        vertex(cid + "_a", "\n".join(attrs), CLASS_COMP, x, y + title_h, w, h_attrs),
        vertex(cid + "_m", "\n".join(methods), CLASS_COMP,
               x, y + title_h + h_attrs, w, h_methods),
    ]
    return cells, title_h + h_attrs + h_methods


def save(out_path, cells, page_w, page_h):
    """写出 .drawio：page_w/page_h 为画布尺寸（内容四周已留 24px 白边）。"""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bg = vertex("page_bg", "",
                "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=none;",
                0, 0, page_w, page_h)
    body = "\n        ".join([bg] + list(cells))
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" type="device" version="24.7.5">
  <diagram name="第1页" id="p1">
    <mxGraphModel dx="1000" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{page_w}" pageHeight="{page_h}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        {body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''
    out_path.write_text(xml, encoding="utf-8")
    print("written:", out_path)
