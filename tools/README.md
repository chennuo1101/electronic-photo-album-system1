# tools 目录说明（图稿工具 · 2026-10）

本目录是图稿生成、导出、检查的公共脚本，由组长维护。成员自己的画图脚本放在
`docs/交付/<编号-模块-姓名>/` 下（参考 `docs/交付/1-账户管理-钟标/gen_figures.py`）。

| 文件 | 作用 | 状态 |
|---|---|---|
| `figstyle.py` | 统一样式与拼装：色板、字号、线宽、类框、标签、折线、跨越符号；提供 `save / vertex / poly / label / classbox` | **v2.1，唯一正式样式源** |
| `render_drawio.py` | 没有 draw.io 时的应急渲染器，几何与 `.drawio` 一致，支持 `jumpStyle=arc` 跨越符号 | 可用 |
| `figure_layout.py` | 其余三个模块复用的活动图、类图、协作图布局；实体字段统一字典 | **v2.1** |
| `check_figure_delivery.py` | 本轮 23 张图的几何、文本高度、宽度/字号、消息编号、实体字段检查 | 自动检查，图义另做人工复核 |
| `postprocess_png.py` | PNG 统一裁边/补白，并打印内容宽、宽高比、满宽等效字号（v2.1 版面预算） | 可用 |
| `gen_drawio.py` | 图 2-1 系统体系结构图、图 2-2 功能框架图的生成脚本 | **v2.1，已重出** |
| `gen_login_demo.py` | 旧路径转发入口，等价于运行交付目录的 `gen_figures.py` | 兼容保留 |
| `draw_demo.py` | 早期 matplotlib 教学演示图（旧版黑白，不入报告） | 历史遗留，不再更新 |

## 常用命令（都在项目根目录执行）

```bash
# 1. 生成 .drawio（以账户管理模块为例）
python "docs/交付/1-账户管理-钟标/gen_figures.py"

# 2. 导出 PNG：有 draw.io 时用命令行（推荐）
drawio -x -f png --scale 2 -o "docs/交付/1-账户管理-钟标/images/用户登录_活动图.png" \
       "docs/交付/1-账户管理-钟标/images/用户登录_活动图.drawio"

# 2'. 没有 draw.io 时用应急渲染器
python tools/render_drawio.py "docs/交付/1-账户管理-钟标/images"

# 3. 统一裁边/补白，并检查字号预算
python tools/postprocess_png.py "docs/交付/1-账户管理-钟标/images"
```

完整规范见 [docs/绘图规范.md](../docs/绘图规范.md)（v2.1）；当前进度与待办见
[docs/交付/README.md](../docs/交付/README.md) 的"当前状态与接手说明"。

返修结果及逐图检查表见 [返修检查记录](../docs/图稿/返修检查记录.md)。
