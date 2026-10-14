# -*- coding: utf-8 -*-
"""成员C（刘硕）图稿：相册管理模块用例图 + 创建相册/修改相册 活动图、类模型图、协作图。

用法：
    python "docs/交付/2-相册管理-刘硕/gen_album_diagrams.py"
    然后用本机 draw.io 命令行导出 PNG（各人路径不同，不要写进仓库文件）：
    drawio -x -f png --scale 2 -o images/xxx.png images/xxx.drawio

风格遵循 docs/绘图规范.md：白底、黑白线条、Microsoft YaHei、走线不穿框。
图编号不烤进图片，由组长整合排版时统一编号。

设计约定（对齐范例 1-账户管理-成员B/gen_login_diagrams.py 与 2026-09 返工版）：
- 活动图：主流程居中自上而下；调用 seg() 按绝对坐标画线，分支标签（是/否、回路名）
  用独立文字框紧贴对应线段；每条扩展流程都画成判断分支，错误分支拐回对应步骤。
- 类模型图：类框为"类名/属性/方法"三栏矩形拼接（不用 <hr> 灰色分隔线）；
  同一关联线上的文字（关联名 + 两端多重性）全部放在线的同一侧。
- 协作图：对象框内不写冒号；每条消息一根独立带箭头直线，"编号: 消息内容"
  紧贴自己那根线；双向消息画成两条平行线，不共线。
- 参与者标注 = 用例描述中的参与者名（本模块为"普通用户"）。
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

FONT = "fontFamily=Microsoft YaHei;fontSize=12;fontColor=#222222;"
BOX = "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#444444;" + FONT
NOTE = "rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#444444;dashed=1;" + FONT
DIAMOND = "rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#444444;" + FONT
ELLIPSE = "ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#444444;" + FONT
ACTOR = ("shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"
         "fillColor=#FFFFFF;strokeColor=#444444;" + FONT)
BOUND = ("rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#444444;"
         "verticalAlign=top;align=left;spacingLeft=12;spacingTop=8;" + FONT)
# 类框三栏：标题栏居中加粗，属性/方法栏左对齐
CLASS_TITLE = ("rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#444444;"
               "align=center;verticalAlign=middle;fontStyle=1;" + FONT)
CLASS_COMP = ("rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#444444;"
              "verticalAlign=top;align=left;spacingLeft=10;spacingTop=6;" + FONT)
TEXT = "text;html=1;align=center;verticalAlign=middle;fillColor=none;strokeColor=none;" + FONT
TEXT_L = TEXT.replace("align=center", "align=left")
TEXT_R = TEXT.replace("align=center", "align=right")
# 用例图参与者连线：无箭头实线
STRAIGHT = ("html=1;strokeColor=#444444;strokeWidth=1;"
            "fontFamily=Microsoft YaHei;fontSize=11;fontColor=#444444;labelBackgroundColor=#FFFFFF;"
            "startArrow=none;endArrow=none;")
# 活动图流程线：实心箭头
SEG_ARR = "html=1;rounded=0;strokeColor=#444444;strokeWidth=1;"
# 折线中间段：无箭头
SEG_NONE = "html=1;rounded=0;strokeColor=#444444;strokeWidth=1;startArrow=none;endArrow=none;"
# 关联线 / 协作图消息：开放箭头
SEG_OPEN = ("html=1;rounded=0;strokeColor=#444444;strokeWidth=1;"
            "startArrow=none;endArrow=open;endFill=0;")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "&#xa;")


def vertex(cid, value, style, x, y, w, h, parent="1"):
    return (f'<mxCell id="{cid}" value="{esc(value)}" style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')


def edge(eid, src, dst, style=STRAIGHT, parent="1"):
    return (f'<mxCell id="{eid}" value="" style="{style}" edge="1" parent="{parent}" '
            f'source="{src}" target="{dst}"><mxGeometry relative="1" as="geometry"/></mxCell>')


def seg(eid, x1, y1, x2, y2, style=SEG_ARR):
    """两端坐标写死的独立线段（不吸附图元，箭头方向 = (x1,y1) → (x2,y2)）。"""
    return (f'<mxCell id="{eid}" value="" style="{style}" edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry">'
            f'<mxPoint x="{x1}" y="{y1}" as="sourcePoint"/>'
            f'<mxPoint x="{x2}" y="{y2}" as="targetPoint"/>'
            f'</mxGeometry></mxCell>')


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
    print("written:", (OUT / f"{name}.drawio").name)


LINE_H, PAD = 24, 12   # 类框属性/方法栏：每行 24px，上下留白共 12px
START = "ellipse;html=1;fillColor=#444444;strokeColor=#444444;"
END_RING = "ellipse;html=1;fillColor=#FFFFFF;strokeColor=#444444;strokeWidth=2;"


def classbox(cid, stereotype, name, attrs, methods, x, y, w):
    """三栏类框：标题栏 + 属性栏 + 方法栏三个矩形拼接，栏间是共享黑边框。

    属性/方法为空时留空栏（高度按一行计），不放占位符。
    """
    h_title = 40
    h_attrs = max(1, len(attrs)) * LINE_H + PAD
    h_meth = max(1, len(methods)) * LINE_H + PAD
    return [
        vertex(cid + "_t", f"«{stereotype}» {name}", CLASS_TITLE, x, y, w, h_title),
        vertex(cid + "_a", "\n".join(attrs), CLASS_COMP, x, y + h_title, w, h_attrs),
        vertex(cid + "_m", "\n".join(methods), CLASS_COMP,
               x, y + h_title + h_attrs, w, h_meth),
    ], h_title + h_attrs + h_meth


# ================= 1. 相册管理模块用例图 =================
# 本模块（用户侧）两个用例共用一张用例图；「相册类别管理」属管理员端，
# 由模块 4 的用例图负责，这里不重复画。
save("相册管理模块用例图", [
    vertex("boundary", "电子相册系统", BOUND, 180, 40, 520, 400),
    vertex("actor_user", "普通用户", ACTOR, 60, 200, 30, 60),
    vertex("uc_create", "创建相册", ELLIPSE, 400, 110, 180, 60),
    vertex("uc_modify", "修改相册", ELLIPSE, 400, 290, 180, 60),
    edge("l1", "actor_user", "uc_create",
         style=STRAIGHT + "exitX=1;exitY=0.35;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"),
    edge("l2", "actor_user", "uc_modify",
         style=STRAIGHT + "exitX=1;exitY=0.65;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"),
], 760, 480)

# ================= 2. 创建相册_活动图 =================
# 主流程居中一列；扩展流程 4a 在右侧，处理后拐回步骤 3「填写相册信息并提交」。
save("创建相册_活动图", [
    vertex("start", "", START, 218, 24, 24, 24),
    vertex("a1", "进入“我的相册”页面，点击“创建相册”", BOX, 100, 70, 260, 44),
    vertex("a2", "系统显示创建表单\n（相册名称、类别、公开/私有）", BOX, 100, 150, 260, 60),
    vertex("a3", "填写相册信息并提交", BOX, 100, 246, 260, 44),
    vertex("d1", "名称为空或未选类别？", DIAMOND, 130, 326, 200, 90),
    vertex("err1", "提示错误信息", NOTE, 450, 341, 180, 60),
    vertex("a4", "系统创建相册并关联当前用户", BOX, 100, 456, 260, 44),
    vertex("a5", "提示创建成功，新相册显示在列表中", BOX, 100, 540, 260, 44),
    vertex("end", "", END_RING, 218, 624, 24, 24),
    vertex("end_in", "", START, 224, 630, 12, 12),

    # 主流程
    seg("f1", 230, 48, 230, 70),
    seg("f2", 230, 114, 230, 150),
    seg("f3", 230, 210, 230, 246),
    seg("f4", 230, 290, 230, 326),
    seg("f7", 230, 416, 230, 456),
    seg("f8", 230, 500, 230, 540),
    seg("f9", 230, 584, 230, 624),
    # 扩展流程 4a：否 → 提示错误 → 拐回步骤 3
    seg("f5", 330, 371, 450, 371),
    seg("f6a", 540, 341, 540, 268, SEG_NONE),
    seg("f6b", 540, 268, 360, 268),
    # 分支标签：紧贴各自线段
    vertex("l_no", "否", TEXT, 355, 345, 20, 20),
    vertex("l_yes", "是", TEXT, 196, 424, 24, 20),
    vertex("l_back", "返回重新填写", TEXT, 400, 242, 120, 20),
], 760, 700)

# ================= 3. 修改相册_活动图 =================
# 扩展流程 1a（相册不存在）在右侧就近结束；扩展流程 4a（名称为空）拐回步骤 3。
cells = [
    vertex("start", "", START, 218, 24, 24, 24),
    vertex("a1", "在相册列表中选择相册，点击“修改”", BOX, 100, 70, 260, 44),
    vertex("d1", "相册存在？", DIAMOND, 130, 154, 200, 90),
    vertex("err1", "提示“相册不存在或已被删除”", NOTE, 450, 169, 220, 60),
    vertex("end2", "", END_RING, 700, 187, 24, 24),
    vertex("end2_in", "", START, 706, 193, 12, 12),
    vertex("a2", "显示该相册的现有信息", BOX, 100, 284, 260, 44),
    vertex("a3", "修改名称、类别或公开/私有\n属性并提交", BOX, 100, 368, 260, 60),
    vertex("d2", "名称为空？", DIAMOND, 130, 468, 200, 90),
    vertex("err2", "提示名称为空", NOTE, 450, 485, 180, 56),
    vertex("a4", "系统更新相册信息", BOX, 100, 598, 260, 44),
    vertex("a5", "提示修改成功，返回相册列表", BOX, 100, 682, 260, 44),
    vertex("end", "", END_RING, 218, 766, 24, 24),
    vertex("end_in", "", START, 224, 772, 12, 12),

    # 主流程
    seg("f1", 230, 48, 230, 70),
    seg("f2", 230, 114, 230, 154),
    seg("f3", 230, 244, 230, 284),
    seg("f6", 230, 328, 230, 368),
    seg("f7", 230, 428, 230, 468),
    seg("f10", 230, 558, 230, 598),
    seg("f11", 230, 642, 230, 682),
    seg("f12", 230, 726, 230, 766),
    # 扩展流程 1a：否 → 提示不存在 → 就近结束
    seg("f4", 330, 199, 450, 199),
    seg("f5", 670, 199, 700, 199),
    # 扩展流程 4a：否 → 提示名称为空 → 拐回步骤 3
    seg("f8", 330, 513, 450, 513),
    seg("f9a", 540, 485, 540, 398, SEG_NONE),
    seg("f9b", 540, 398, 360, 398),
    # 分支标签：紧贴各自线段
    vertex("l_no1", "否", TEXT, 355, 173, 20, 20),
    vertex("l_yes1", "是", TEXT, 196, 252, 24, 20),
    vertex("l_no2", "否", TEXT, 355, 487, 20, 20),
    vertex("l_yes2", "是", TEXT, 196, 566, 24, 20),
    vertex("l_back", "返回修改", TEXT, 400, 372, 110, 20),
]
save("修改相册_活动图", cells, 800, 860)

# ================= 4. 创建相册_类模型图 =================
# 版式对齐范例：页面左上、控制器右上、相册右下、相册类别左下；
# 连线为"页面→控制器"（水平）、"控制器→相册"（垂直）、
# "控制器→相册类别"（查询类别列表，绕行折线）、"相册→相册类别"（属于，水平）。
cells = []
b, h_page = classbox("page", "boundary", "创建相册页面",
                     ["相册名称", "相册类别", "公开/私有"],
                     ["显示创建表单()", "读取表单输入()", "提示错误信息()", "返回相册列表()"],
                     60, 80, 240)
cells += b
b, h_ctl = classbox("ctl", "control", "相册控制器",
                    [],
                    ["校验相册信息()", "创建相册()", "关联当前用户()"],
                    460, 80, 240)
cells += b
b, h_cat = classbox("cat", "entity", "相册类别",
                    ["类别编号", "类别名称"],
                    ["查询类别列表()"],
                    60, 400, 240)
cells += b
b, h_alb = classbox("alb", "entity", "相册",
                    ["相册编号", "相册名称", "类别编号", "公开/私有", "创建者编号", "创建时间"],
                    ["保存()", "更新()"],
                    460, 400, 240)
cells += b

# 关联 1：创建相册页面 → 相册控制器（水平线，文字都在线上方）
cells += [
    seg("r1", 300, 152, 460, 152, SEG_OPEN),
    vertex("r1_m1", "1", TEXT, 308, 124, 24, 20),
    vertex("r1_name", "提交创建请求", TEXT, 338, 124, 84, 20),
    vertex("r1_m2", "1", TEXT, 428, 124, 24, 20),
]
# 关联 2：相册控制器 → 相册（垂直线，文字都在线右方）
cells += [
    seg("r2", 580, 80 + h_ctl, 580, 400, SEG_OPEN),
    vertex("r2_m1", "1", TEXT_L, 592, 252, 24, 20),
    vertex("r2_name", "创建并保存", TEXT_L, 592, 310, 90, 20),
    vertex("r2_m2", "1", TEXT_L, 592, 368, 24, 20),
]
# 关联 3：相册 → 相册类别（水平线，文字都在线上方）
cells += [
    seg("r3", 460, 468, 300, 468, SEG_OPEN),
    vertex("r3_m1", "0..*", TEXT, 415, 440, 40, 20),
    vertex("r3_name", "属于", TEXT, 350, 440, 50, 20),
    vertex("r3_m2", "1", TEXT, 306, 440, 20, 20),
]
# 关联 4：相册控制器 → 相册类别（查询类别列表，绕行折线；文字都在横段上方）
cells += [
    seg("r4a", 520, 80 + h_ctl, 520, 350, SEG_NONE),
    seg("r4b", 520, 350, 180, 350, SEG_NONE),
    seg("r4c", 180, 350, 180, 400, SEG_OPEN),
    vertex("r4_m1", "1", TEXT, 490, 322, 20, 20),
    vertex("r4_name", "查询类别列表", TEXT, 285, 322, 110, 20),
    vertex("r4_m2", "0..*", TEXT, 190, 322, 40, 20),
]
save("创建相册_类模型图", cells, 900, 760)

# ================= 5. 修改相册_类模型图 =================
# 与创建相册同构；差别是"控制器→相册"为查询并更新、多重性 0..1
# （相册可能不存在，对应扩展流程 1a）。
cells = []
b, h_page = classbox("page", "boundary", "修改相册页面",
                     ["相册信息", "修改表单"],
                     ["显示相册信息()", "读取修改内容()", "提示错误信息()", "返回相册列表()"],
                     60, 80, 240)
cells += b
b, h_ctl = classbox("ctl", "control", "相册控制器",
                    [],
                    ["查询相册()", "校验相册信息()", "更新相册信息()"],
                    460, 80, 240)
cells += b
b, h_cat = classbox("cat", "entity", "相册类别",
                    ["类别编号", "类别名称"],
                    ["查询类别列表()"],
                    60, 400, 240)
cells += b
b, h_alb = classbox("alb", "entity", "相册",
                    ["相册编号", "相册名称", "类别编号", "公开/私有", "创建者编号", "创建时间"],
                    ["保存()", "更新()"],
                    460, 400, 240)
cells += b

cells += [
    seg("r1", 300, 152, 460, 152, SEG_OPEN),
    vertex("r1_m1", "1", TEXT, 308, 124, 24, 20),
    vertex("r1_name", "提交修改请求", TEXT, 338, 124, 84, 20),
    vertex("r1_m2", "1", TEXT, 428, 124, 24, 20),
    seg("r2", 580, 80 + h_ctl, 580, 400, SEG_OPEN),
    vertex("r2_m1", "1", TEXT_L, 592, 252, 24, 20),
    vertex("r2_name", "查询并更新", TEXT_L, 592, 310, 90, 20),
    vertex("r2_m2", "0..1", TEXT_L, 592, 368, 40, 20),
    seg("r3", 460, 468, 300, 468, SEG_OPEN),
    vertex("r3_m1", "0..*", TEXT, 415, 440, 40, 20),
    vertex("r3_name", "属于", TEXT, 350, 440, 50, 20),
    vertex("r3_m2", "1", TEXT, 306, 440, 20, 20),
    seg("r4a", 520, 80 + h_ctl, 520, 350, SEG_NONE),
    seg("r4b", 520, 350, 180, 350, SEG_NONE),
    seg("r4c", 180, 350, 180, 400, SEG_OPEN),
    vertex("r4_m1", "1", TEXT, 490, 322, 20, 20),
    vertex("r4_name", "查询类别列表", TEXT, 285, 322, 110, 20),
    vertex("r4_m2", "0..*", TEXT, 190, 322, 40, 20),
]
save("修改相册_类模型图", cells, 900, 760)

# ================= 6. 创建相册_协作图 =================
# 布局：普通用户(左) — 创建相册页面 — 相册控制器 — 相册类别(右)；相册在控制器下方。
# 每条消息一根独立带箭头直线，编号标签紧贴自己那根线；双向消息画两条平行线。
# 参与者框留足高度，使其下方的名字标签不与最后一条消息（10）的标签挤在一起。
save("创建相册_协作图", [
    vertex("actor", "普通用户", ACTOR, 40, 100, 30, 180),
    vertex("page", "创建相册页面", BOX, 250, 100, 200, 180),
    vertex("ctl", "相册控制器", BOX, 560, 100, 200, 180),
    vertex("cat", "相册类别", BOX, 900, 100, 180, 180),
    vertex("alb", "相册", BOX, 560, 380, 200, 64),

    # 普通用户 ↔ 创建相册页面
    seg("m1", 70, 115, 250, 115, SEG_OPEN),
    vertex("t1", "1: 进入“我的相册”，点击创建", TEXT, 75, 87, 175, 22),
    seg("m2", 250, 155, 70, 155, SEG_OPEN),
    vertex("t2", "2: 显示创建表单", TEXT, 75, 161, 175, 22),
    seg("m3", 70, 195, 250, 195, SEG_OPEN),
    vertex("t3", "3: 填写信息并提交", TEXT, 75, 201, 175, 22),
    seg("m10", 250, 235, 70, 235, SEG_OPEN),
    vertex("t10", "10: 提示成功，新相册入列表", TEXT, 75, 241, 175, 22),

    # 创建相册页面 ↔ 相册控制器
    seg("m4", 450, 150, 560, 150, SEG_OPEN),
    vertex("t4", "4: 提交创建请求", TEXT, 455, 122, 105, 22),
    seg("m9", 560, 200, 450, 200, SEG_OPEN),
    vertex("t9", "9: 返回创建成功", TEXT, 455, 206, 105, 22),

    # 相册控制器 ↔ 相册类别
    seg("m5", 760, 150, 900, 150, SEG_OPEN),
    vertex("t5", "5: 查询类别列表", TEXT, 765, 122, 130, 22),
    seg("m6", 900, 200, 760, 200, SEG_OPEN),
    vertex("t6", "6: 返回类别信息", TEXT, 765, 206, 130, 22),

    # 相册控制器 ↔ 相册（竖直双线）
    seg("m7", 620, 280, 620, 380, SEG_OPEN),
    vertex("t7", "7: 创建并关联用户", TEXT_R, 490, 310, 120, 22),
    seg("m8", 700, 380, 700, 280, SEG_OPEN),
    vertex("t8", "8: 返回创建结果", TEXT_L, 712, 310, 120, 22),
], 1120, 460)

# ================= 7. 修改相册_协作图 =================
# 布局：普通用户 — 修改相册页面 — 相册控制器；相册在控制器下方，两组竖直双线。
save("修改相册_协作图", [
    vertex("actor", "普通用户", ACTOR, 40, 100, 30, 220),
    vertex("page", "修改相册页面", BOX, 250, 100, 200, 220),
    vertex("ctl", "相册控制器", BOX, 560, 100, 200, 220),
    vertex("alb", "相册", BOX, 560, 430, 200, 64),

    # 普通用户 ↔ 修改相册页面
    seg("m1", 70, 120, 250, 120, SEG_OPEN),
    vertex("t1", "1: 选择相册，点击修改", TEXT, 75, 126, 175, 22),
    seg("m6", 250, 165, 70, 165, SEG_OPEN),
    vertex("t6", "6: 显示现有信息与表单", TEXT, 75, 171, 175, 22),
    seg("m7", 70, 210, 250, 210, SEG_OPEN),
    vertex("t7", "7: 修改信息并提交", TEXT, 75, 216, 175, 22),
    seg("m12", 250, 255, 70, 255, SEG_OPEN),
    vertex("t12", "12: 提示成功，返回列表", TEXT, 75, 261, 175, 22),

    # 修改相册页面 ↔ 相册控制器
    seg("m2", 450, 130, 560, 130, SEG_OPEN),
    vertex("t2", "2: 提交修改请求", TEXT, 455, 136, 105, 22),
    seg("m5", 560, 180, 450, 180, SEG_OPEN),
    vertex("t5", "5: 返回相册信息", TEXT, 455, 186, 105, 22),
    seg("m8", 450, 230, 560, 230, SEG_OPEN),
    vertex("t8", "8: 提交修改内容", TEXT, 455, 236, 105, 22),
    seg("m11", 560, 280, 450, 280, SEG_OPEN),
    vertex("t11", "11: 返回修改成功", TEXT, 455, 286, 105, 22),

    # 相册控制器 ↔ 相册（两组竖直双线：先查询相册，再更新相册）
    # 排版要点：两条线一组，组间留出空档；标签只放在没有竖线的位置——
    # 查询组的标签在整组左侧，两个"返回"标签分别放在组间空档和最右侧，
    # 这样四条竖线都不会穿过任何标签文字。
    seg("m3", 580, 320, 580, 430, SEG_OPEN),
    vertex("t3", "3: 查询相册信息", TEXT_R, 450, 330, 120, 22),
    seg("m4", 604, 430, 604, 320, SEG_OPEN),
    vertex("t4", "4: 返回相册信息", TEXT, 608, 380, 100, 22),
    seg("m9", 716, 320, 716, 430, SEG_OPEN),
    vertex("t9", "9: 更新相册信息", TEXT_R, 618, 330, 90, 22),
    seg("m10", 740, 430, 740, 320, SEG_OPEN),
    vertex("t10", "10: 返回更新结果", TEXT_L, 752, 380, 110, 22),
], 1120, 560)

print(f"已生成 7 个 draw.io 源文件：{OUT}")
