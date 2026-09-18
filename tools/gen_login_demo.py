# -*- coding: utf-8 -*-
"""兼容入口：成员B 演示图稿的维护版本已迁移到交付目录。

    docs/交付/1-账户管理-成员B/gen_login_diagrams.py

2026-09 修订内容：协作图对象框去冒号、双向消息画成两条平行带箭头线、
编号标签紧贴所属线段；类模型图改为三栏矩形拼接（去掉 <hr> 灰色分隔线）、
同一关联线上的文字统一在线的同侧。组员请以交付目录里的脚本为参考，
本文件仅作为旧路径的转发入口保留。

用法：
    python tools/gen_login_demo.py    # 等价于运行交付目录下的 gen_login_diagrams.py
"""
import runpy
from pathlib import Path

TARGET = (Path(__file__).resolve().parent.parent
          / "docs" / "交付" / "1-账户管理-成员B" / "gen_login_diagrams.py")
print(f"已迁移，转发执行：{TARGET.relative_to(Path(__file__).resolve().parent.parent)}")
runpy.run_path(str(TARGET), run_name="__main__")
