# -*- coding: utf-8 -*-
"""成员B 演示图稿：账户管理模块用例图 + 用户登录活动图/类模型图/协作图。

用法（演示"组员指挥自己的 agent 画图"的标准流程）：
    python tools/gen_login_demo.py        # 生成 .drawio 到成员交付目录
    然后用各自本机安装的 draw.io 命令行导出 PNG，例如：
    drawio -x -f png --scale 2 -o 输出.png 输入.drawio

风格遵循 docs/绘图规范.md：白底、黑白线条、Microsoft YaHei、走线不穿框。
图编号不烤进图片，由组长整合排版时统一编号。
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "交付" / "成员B_账户管理" / "images"
OUT.mkdir(parents=True, exist_ok=True)

FONT = "fontFamily=Microsoft YaHei;fontSize=12;fontColor=#222222;"
BOX = "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#444444;" + FONT
GRAY = "rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#444444;" + FONT
NOTE = "rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#444444;dashed=1;" + FONT
DIAMOND = "rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#444444;" + FONT
ELLIPSE = "ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#444444;" + FONT
ACTOR = ("shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"
         "fillColor=#FFFFFF;strokeColor=#444444;" + FONT)
BOUND = ("rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#444444;"
         "verticalAlign=top;align=left;spacingLeft=12;spacingTop=8;" + FONT)
CLASSBOX = ("rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#444444;"
            "verticalAlign=top;align=left;spacingLeft=10;spacingTop=8;" + FONT)
TEXT = "text;html=1;align=center;verticalAlign=middle;fillColor=none;strokeColor=none;" + FONT
EDGE = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#444444;strokeWidth=1;"
        "fontFamily=Microsoft YaHei;fontSize=11;fontColor=#444444;labelBackgroundColor=#FFFFFF;")
LINE = EDGE + "startArrow=none;endArrow=none;"        # 无箭头实线（用例图）
STRAIGHT = ("html=1;strokeColor=#444444;strokeWidth=1;"
            "fontFamily=Microsoft YaHei;fontSize=11;fontColor=#444444;labelBackgroundColor=#FFFFFF;"
            "startArrow=none;endArrow=none;")          # 无箭头直线（用例图参与者连线）
OPEN = EDGE + "startArrow=none;endArrow=open;"        # 开放箭头（类图关联 / 协作图消息）


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "&#xa;")


def vertex(cid, value, style, x, y, w, h, parent="1", raw=False):
    v = value if raw else esc(value)
    return (f'<mxCell id="{cid}" value="{v}" style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')


def edge(eid, src, dst, label="", style=EDGE, parent="1", points=None, label_xy=None):
    val = f' value="{esc(label)}"' if label else ' value=""'
    if points:
        pts = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in points)
        geom = f'<mxGeometry relative="1" as="geometry"><Array as="points">{pts}</Array></mxGeometry>'
    elif label_xy is not None:
        # x = 沿线位置偏移（-1..1），y = 垂直于线的像素偏移
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


def save(name, cells, w, h):
    (OUT / f"{name}.drawio").write_text(mxfile(cells, w, h), encoding="utf-8")
    print("written:", OUT / f"{name}.drawio")


# ================= 1. 账户管理模块用例图 =================
cells = [
    vertex("boundary", "电子相册系统", BOUND, 180, 40, 520, 400),
    vertex("actor_user", "普通用户", ACTOR, 60, 100, 30, 60),
    vertex("actor_admin", "管理员", ACTOR, 60, 300, 30, 60),
    vertex("uc_reg", "用户注册", ELLIPSE, 400, 110, 170, 60),
    vertex("uc_login", "用户登录", ELLIPSE, 400, 290, 170, 60),
    edge("l1", "actor_user", "uc_reg", style=STRAIGHT + "exitX=1;exitY=0.4;entryX=0;entryY=0.5;"),
    edge("l2", "actor_user", "uc_login", style=STRAIGHT + "exitX=1;exitY=0.6;entryX=0;entryY=0.4;"),
    edge("l3", "actor_admin", "uc_login", style=STRAIGHT + "exitX=1;exitY=0.4;entryX=0;entryY=0.8;"),
]
save("账户管理模块用例图", cells, 760, 480)

# ================= 2. 用户登录活动图 =================
cells = [
    vertex("start", "", "ellipse;html=1;fillColor=#444444;strokeColor=#444444;", 218, 24, 24, 24),
    vertex("a1", "打开登录页面", BOX, 100, 70, 260, 44),
    vertex("a2", "输入用户名和密码", BOX, 100, 150, 260, 44),
    vertex("d1", "输入完整？", DIAMOND, 140, 234, 180, 90),
    vertex("err1", "提示补全输入", NOTE, 470, 250, 150, 56),
    vertex("a3", "系统验证用户名和密码", BOX, 100, 364, 260, 44),
    vertex("d2", "验证通过？", DIAMOND, 140, 448, 180, 90),
    vertex("err2", "提示“用户名或密码错误”", NOTE, 470, 464, 150, 56),
    vertex("d3", "账户角色？", DIAMOND, 140, 578, 180, 90),
    vertex("a4", "进入个人主页", BOX, 40, 708, 160, 44),
    vertex("a5", "进入后台管理页", BOX, 280, 708, 170, 44),
    vertex("end", "", "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#444444;strokeWidth=2;", 218, 792, 24, 24),
    vertex("end_in", "", "ellipse;html=1;fillColor=#444444;strokeColor=#444444;", 224, 798, 12, 12),
    edge("f1", "start", "a1"),
    edge("f2", "a1", "a2"),
    edge("f3", "a2", "d1"),
    edge("f4", "d1", "err1", "否", style=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
    edge("f5", "err1", "a2", "返回输入",
         style=EDGE + "exitX=0.5;exitY=0;entryX=1;entryY=0.5;", points=[(545, 172)]),
    edge("f6", "d1", "a3", "是"),
    edge("f7", "a3", "d2"),
    edge("f8", "d2", "err2", "否", style=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
    edge("f9", "err2", "a2", "返回重新输入",
         style=EDGE + "exitX=1;exitY=0.5;entryX=1;entryY=0.5;", points=[(700, 492), (700, 162)]),
    edge("f10", "d2", "d3", "是"),
    edge("f11", "d3", "a4", "普通用户", style=EDGE + "exitX=0.25;exitY=1;entryX=0.5;entryY=0;"),
    edge("f12", "d3", "a5", "管理员", style=EDGE + "exitX=0.75;exitY=1;entryX=0.5;entryY=0;"),
    edge("f13", "a4", "end", style=EDGE + "exitX=0.5;exitY=1;entryX=0;entryY=0.5;",
         points=[(120, 804)]),
    edge("f14", "a5", "end", style=EDGE + "exitX=0.5;exitY=1;entryX=1;entryY=0.5;",
         points=[(365, 804)]),
]
save("用户登录_活动图", cells, 780, 860)

# ================= 3. 用户登录类模型图 =================
def classbox(cid, stereotype, name, attrs, methods, x, y, w, h):
    # value 整体交给 esc 做 XML 转义，<hr>/<br> 标签会被存为 &lt;hr&gt;，drawio 按 HTML 渲染
    parts = [f"<b>{stereotype} {name}</b>", "<hr>"]
    parts += [a + "<br>" for a in attrs] if attrs else ["—"]
    parts.append("<hr>")
    parts += [m + "<br>" for m in methods] if methods else ["—"]
    return vertex(cid, "".join(parts), CLASSBOX, x, y, w, h)


cells = [
    classbox("page", "«boundary»", "登录页面",
             ["登录表单"],
             ["显示登录表单()", "读取用户输入()", "提示错误信息()", "按角色跳转页面()"],
             40, 60, 240, 170),
    classbox("ctl", "«control»", "登录控制器",
             [],
             ["校验输入完整性()", "验证账户()", "判断角色()"],
             380, 60, 240, 140),
    classbox("user", "«entity»", "用户",
             ["用户名", "密码", "邮箱", "角色"],
             ["验证密码()"],
             380, 320, 240, 170),
    edge("a1", "page", "ctl", "提交登录请求",
         style=OPEN + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
    edge("a2", "ctl", "user", "查找并验证",
         style=OPEN + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"),
    vertex("m1", "1", TEXT, 288, 106, 20, 20),
    vertex("m2", "1", TEXT, 348, 106, 20, 20),
    vertex("m3", "1", TEXT, 510, 226, 20, 20),
    vertex("m4", "0..1", TEXT, 506, 288, 30, 20),
]
save("用户登录_类模型图", cells, 700, 540)

# ================= 4. 用户登录协作图 =================
cells = [
    vertex("actor", "用户", ACTOR, 50, 170, 30, 60),
    vertex("page", ":登录页面", BOX, 200, 60, 170, 50),
    vertex("ctl", ":登录控制器", BOX, 470, 60, 170, 50),
    vertex("user", ":用户", BOX, 470, 250, 170, 50),
    edge("m1", "actor", "page", "1: 输入用户名、密码",
         style=OPEN + "exitX=1;exitY=0.2;entryX=0;entryY=0.8;", label_xy=(-0.38, -14)),
    edge("m2", "page", "ctl", "2: 提交登录（用户名、密码）",
         style=OPEN + "exitX=1;exitY=0.25;entryX=0;entryY=0.25;", label_xy=(0, -12)),
    edge("m3", "ctl", "user", "3: 验证账户",
         style=OPEN + "exitX=0.2;exitY=1;entryX=0.2;entryY=0;", label_xy=(-0.2, -45)),
    edge("m4", "user", "ctl", "4: 返回验证结果与角色",
         style=OPEN + "exitX=0.8;exitY=0;entryX=0.8;entryY=1;", label_xy=(0.2, 45)),
    edge("m5", "ctl", "page", "5: 按角色跳转页面",
         style=OPEN + "exitX=0;exitY=0.75;entryX=1;entryY=0.75;", label_xy=(0, 12)),
    edge("m6", "page", "actor", "6: 显示个人主页/后台管理页",
         style=OPEN + "exitX=0;exitY=0.2;entryX=1;entryY=0.8;", label_xy=(0.38, 14)),
]
save("用户登录_协作图", cells, 720, 380)
