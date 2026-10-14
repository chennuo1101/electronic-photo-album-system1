# -*- coding: utf-8 -*-
"""兼容入口：账户管理模块示例图稿的维护版本在交付目录。

    docs/交付/1-账户管理-钟标/gen_figures.py

2026-10 修订：原 `docs/交付/1-账户管理-成员B/` 演示目录（占位姓名、内容与钟标交付重复）
已从 main 删除，转发目标改为钟标交付的账户管理模块画图脚本（用户注册、用户登录）。
组员请以交付目录里的脚本为参考，本文件仅作为旧路径的转发入口保留。

用法：
    python tools/gen_login_demo.py    # 等价于运行交付目录下的 gen_figures.py
"""
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "docs" / "交付" / "1-账户管理-钟标" / "gen_figures.py"
print(f"转发执行：{TARGET.relative_to(ROOT)}")
runpy.run_path(str(TARGET), run_name="__main__")
