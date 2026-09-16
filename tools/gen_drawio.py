# -*- coding: utf-8 -*-
"""生成两张 .drawio 图：系统体系结构图、功能框架图（黑白统一风格）v3
修复：连线穿越矩形框的问题（树状图改走线：横线走上方、竖线走列间隙）；
照片存储分前期/后期两阶段表达。
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "图稿"
OUT.mkdir(parents=True, exist_ok=True)

FONT = "fontFamily=Microsoft YaHei;fontSize=12;fontColor=#222222;"
BOX = "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#444444;" + FONT
GRAY = "rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#444444;" + FONT
NOTE = "rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#444444;dashed=1;" + FONT
EDGE = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#444444;strokeWidth=1;"
        "fontFamily=Microsoft YaHei;fontSize=11;fontColor=#444444;labelBackgroundColor=#FFFFFF;")
LINE = EDGE + "startArrow=none;endArrow=none;"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "&#xa;")


def vertex(cid, value, style, x, y, w, h, parent="1"):
    return (f'<mxCell id="{cid}" value="{esc(value)}" style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')


def edge(eid, src, dst, label="", style=EDGE, parent="1", points=None, label_xy=None):
    val = f' value="{esc(label)}"' if label else ' value=""'
    if points:
        pts = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in points)
        geom = f'<mxGeometry relative="1" as="geometry"><Array as="points">{pts}</Array></mxGeometry>'
    elif label_xy is not None:
        geom = f'<mxGeometry relative="1" as="geometry" x="{label_xy[0]}" y="{label_xy[1]}"/>'
    else:
        geom = '<mxGeometry relative="1" as="geometry"/>'
    return (f'<mxCell id="{eid}"{val} style="{style}" edge="1" parent="{parent}" '
            f'source="{src}" target="{dst}">{geom}</mxCell>')


def mxfile(cells, page_w, page_h):
    body = "\n        ".join(cells)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
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


# ================= 图2-1 系统体系结构图 =================
cells = []
cells.append(vertex("client", "客户端：浏览器（Vue 3 + TypeScript）\n普通用户 / 管理员的操作入口", GRAY, 150, 24, 480, 64))
cells.append(vertex("srv",
                    '<b>Web 服务器（FastAPI + Uvicorn）</b>',
                    "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#444444;"
                    "verticalAlign=top;spacingTop=8;align=left;spacingLeft=14;" + FONT,
                    90, 148, 600, 270))
cells.append(vertex("ctl", "Controller 层（FastAPI 路由）\n接收并校验请求 → 调度业务 → 返回 JSON", BOX, 40, 56, 520, 76, parent="srv"))
cells.append(vertex("mdl", "Model 层（业务逻辑 + 数据访问）\nPydantic 数据模型 · 业务规则 · SQLAlchemy 操作数据库", BOX, 40, 168, 520, 76, parent="srv"))
# 照片存储：前期（实线框）
cells.append(vertex("photos", "照片文件存储（前期）\n本机 uploads/ 目录（文件系统）\n数据库只保存路径与元数据", BOX, 770, 230, 230, 100))
# 照片存储：后期（虚线框，待定）
cells.append(vertex("photos2", "照片文件存储（后期 · 待定）\n独立文件服务器 / 对象存储", NOTE, 770, 396, 230, 64))
cells.append(vertex("db", "数据库（PostgreSQL · Docker 容器）\n用户 / 相册 / 照片信息 / 评论 / 相册类别", GRAY, 150, 490, 480, 72))
cells.append(vertex("mvcnote", "MVC 对应关系\nV = 浏览器中的 Vue 页面\nC = FastAPI 路由层\nM = 业务逻辑与数据访问层", NOTE, 770, 486, 230, 110))
cells.append(edge("e1", "client", "ctl", "HTTP 请求 / JSON 响应", label_xy=(0.0, -14)))
cells.append(edge("e2", "mdl", "db", "SQL 查询（SQLAlchemy）", label_xy=(0.0, -14)))
cells.append(edge("e3", "mdl", "photos", "文件读写", label_xy=(0.0, -14)))
cells.append(edge("e4", "photos", "photos2", "可视需求演进", style=EDGE + "dashed=1;", label_xy=(0.0, -14)))
arch = mxfile(cells, 1100, 640)
(OUT / "图2-1_系统体系结构图.drawio").write_text(arch, encoding="utf-8")

# ================= 图2-2 功能框架图 =================
cells = []
cells.append(vertex("top", "电子相册系统", GRAY, 370, 24, 200, 48))
modules = [("m1", "账户管理", 40), ("m2", "相册管理", 270), ("m3", "照片管理", 500), ("m4", "评论管理", 730)]
modx = {cid: x for cid, _, x in modules}
for cid, name, x in modules:
    mc = x + 90
    cells.append(vertex(cid, name, BOX, x, 140, 180, 44))
    # 顶->模块：横线走 y=106（模块上方），竖直落到模块顶边中心
    cells.append(edge("t_" + cid, "top", cid, style=LINE + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;",
                      points=[(470, 106), (mc, 106)]))

TRUNK = 130  # 竖干线相对模块列左缘的偏移（落在列间隙中）
ucases = [
    ("m1", [("u11", "用户注册", 250, BOX), ("u12", "用户登录", 310, BOX)]),
    ("m2", [("u21", "创建相册", 250, BOX), ("u22", "修改相册", 310, BOX), ("u23", "相册类别管理（管理员）", 370, BOX)]),
    ("m3", [("u31", "上传图片", 250, BOX), ("u32", "浏览照片", 310, BOX)]),
    ("m4", [("u41", "对照片评论", 250, BOX), ("u42", "（扩展）删除自己的评论", 310, NOTE)]),
]
for mid, ulist in ucases:
    x = modx[mid]
    trunk_x = x + 180 + (TRUNK - 90)  # 右缘外 40px 的列间隙
    for uid, name, y, st in ulist:
        cy = y + 20
        cells.append(vertex(uid, name, st, x, y, 180, 40))
        # 模块->用例：从模块右边出来，沿列间隙竖干线向下，从右边进入用例
        cells.append(edge("e_" + uid, mid, uid, style=LINE + "exitX=1;exitY=0.5;entryX=1;entryY=0.5;",
                          points=[(trunk_x, 162), (trunk_x, cy)]))
tree = mxfile(cells, 1000, 460)
(OUT / "图2-2_功能框架图.drawio").write_text(tree, encoding="utf-8")

print("drawio files written:", [p.name for p in OUT.glob("*.drawio")])
