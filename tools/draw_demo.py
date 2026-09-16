# -*- coding: utf-8 -*-
"""演示图：账户管理模块用例图 + 用户注册活动图（教学示意图）v2"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon, Circle, FancyArrowPatch

setup_plot()

OUT = Path(__file__).resolve().parent.parent / "docs" / "图稿" / "教学演示"
OUT.mkdir(parents=True, exist_ok=True)

EDGE = "#444444"


def actor(ax, x, y, label, scale=1.0):
    r = 0.22 * scale
    ax.add_patch(Circle((x, y + 1.05 * scale), r, fill=False, lw=1.6, edgecolor=EDGE))
    ax.plot([x, x], [y + 0.83 * scale, y + 0.25 * scale], lw=1.6, color=EDGE)
    ax.plot([x - 0.35 * scale, x + 0.35 * scale], [y + 0.62 * scale, y + 0.62 * scale], lw=1.6, color=EDGE)
    ax.plot([x, x - 0.28 * scale], [y + 0.25 * scale, y - 0.35 * scale], lw=1.6, color=EDGE)
    ax.plot([x, x + 0.28 * scale], [y + 0.25 * scale, y - 0.35 * scale], lw=1.6, color=EDGE)
    ax.text(x, y - 0.75 * scale, label, ha="center", va="top", fontsize=13)


def line(ax, p1, p2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-", lw=1.4, color=EDGE))


def arrow(ax, p1, p2, label=None, rad=0.0, label_off=(0.12, 0.12)):
    a = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=16, lw=1.4,
                        color=EDGE, connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a)
    if label:
        mx, my = (p1[0] + p2[0]) / 2 + label_off[0], (p1[1] + p2[1]) / 2 + label_off[1]
        ax.text(mx, my, label, fontsize=10.5, color=EDGE)


# ============ 图 1：账户管理模块用例图 ============
fig, ax = plt.subplots(figsize=(9, 6))
ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")

ax.add_patch(FancyBboxPatch((4.2, 1.0), 6.8, 6.0, boxstyle="round,pad=0.05",
                            fill=False, lw=1.6, edgecolor=EDGE))
ax.text(4.45, 6.75, "电子相册系统", fontsize=13, va="center", color=EDGE)

ax.add_patch(Ellipse((7.6, 4.9), 3.4, 1.15, fill=False, lw=1.6, edgecolor=EDGE))
ax.add_patch(Ellipse((7.6, 2.3), 3.4, 1.15, fill=False, lw=1.6, edgecolor=EDGE))
ax.text(7.6, 4.9, "用户注册", ha="center", va="center", fontsize=13)
ax.text(7.6, 2.3, "用户登录", ha="center", va="center", fontsize=13)

actor(ax, 1.6, 4.0, "普通用户")
actor(ax, 1.6, 1.2, "管理员")

line(ax, (2.0, 4.6), (5.85, 4.9))
line(ax, (2.0, 4.0), (5.85, 2.45))
line(ax, (2.0, 1.55), (5.85, 2.15))

ax.text(6.0, 0.35, "图 3-1 账户管理模块用例图", ha="center", fontsize=11)
fig.savefig(OUT / "图3-1_账户管理模块用例图.png", bbox_inches="tight", dpi=150)
plt.close(fig)

# ============ 图 2：用户注册活动图 ============
fig, ax = plt.subplots(figsize=(8.5, 12))
ax.set_xlim(0, 11); ax.set_ylim(0, 16); ax.axis("off")

CX = 4.2  # 主流中线


def step(y, text, w=4.4, h=0.85):
    ax.add_patch(FancyBboxPatch((CX - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.06", fill=False, lw=1.5, edgecolor=EDGE))
    ax.text(CX, y, text, ha="center", va="center", fontsize=11.5)


def decision(y, text, w=3.4, h=1.9):
    ax.add_patch(Polygon([(CX, y + h / 2), (CX + w / 2, y), (CX, y - h / 2), (CX - w / 2, y)],
                         fill=False, lw=1.5, edgecolor=EDGE))
    ax.text(CX, y, text, ha="center", va="center", fontsize=11)


def errbox(x0, y0, text):
    ax.add_patch(FancyBboxPatch((x0, y0), 1.6, 1.4, boxstyle="round,pad=0.06",
                                fill=False, lw=1.4, linestyle="--", edgecolor=EDGE))
    ax.text(x0 + 0.8, y0 + 0.7, text, ha="center", va="center", fontsize=10.5)


def seg(p1, p2):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], lw=1.4, color=EDGE)


# 起点
ax.add_patch(Circle((CX, 15.2), 0.14, color=EDGE))
step(14.2, "打开注册页面")
step(12.7, "输入用户名、密码、确认密码、邮箱")
decision(10.7, "信息完整且\n两次密码一致？")
step(8.6, "系统检查用户名是否已被注册", w=5.0)
decision(6.4, "用户名\n已存在？")
step(4.4, "创建新账户")
step(2.9, "提示注册成功，跳转登录页面")
ax.add_patch(Circle((CX, 1.62), 0.24, fill=False, lw=1.6, edgecolor=EDGE))
ax.add_patch(Circle((CX, 1.62), 0.1, color=EDGE))

# 错误提示框（右侧泳道）
errbox(7.8, 10.0, "提示错误\n信息")
errbox(7.8, 5.5, "提示用户名\n已被占用")

arrow(ax, (CX, 15.06), (CX, 14.65))
arrow(ax, (CX, 13.77), (CX, 13.15))
arrow(ax, (CX, 12.22), (CX, 11.66))
arrow(ax, (CX, 9.74), (CX, 9.15), label="是")
arrow(ax, (CX, 8.02), (CX, 7.42))
arrow(ax, (CX, 5.44), (CX, 4.85), label="否")
arrow(ax, (CX, 3.97), (CX, 3.35))
arrow(ax, (CX, 2.42), (CX, 1.92))

# 分支：信息不完整 → 提示错误信息
arrow(ax, (5.9, 10.7), (7.8, 10.7), label="否")
seg((8.6, 11.4), (8.6, 13.5))
arrow(ax, (8.6, 13.5), (6.45, 12.75))          # 回到"输入"框

# 分支：用户名已存在 → 提示已被占用 → 回到"输入"
arrow(ax, (5.9, 6.4), (7.8, 6.2), label="是")
seg((8.6, 5.5), (8.6, 4.6))
seg((8.6, 4.6), (10.1, 4.6))
seg((10.1, 4.6), (10.1, 12.4))
arrow(ax, (10.1, 12.4), (6.42, 12.65))         # 回到"输入"框

ax.text(CX, 0.45, "图 3-2 用户注册活动图", ha="center", fontsize=11)
fig.savefig(OUT / "图3-2_用户注册活动图.png", bbox_inches="tight", dpi=150)
plt.close(fig)

print("saved:", list(OUT.iterdir()))
