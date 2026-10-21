"""系统图 v2.1：分层职责与部署边界、系统到用例的功能分解。

样式全部引用 figstyle；图号与图名由报告排版添加。
"""
from pathlib import Path
import figstyle as fs
from figure_layout import Figure

OUT = Path(__file__).resolve().parent.parent / 'docs' / '图稿'
BOTH = fs.SEG_JUMP + 'startArrow=block;startFill=1;'
BOLD = fs.SYS + 'fontStyle=1;'

# 体系结构：按 MVC 展开职责；开发期仍全在本机，后期文件存储单独标为待定。
f = Figure(OUT, '图2-1_系统体系结构图')
f.node('view', '表现层 · View  |  Vue 3 + TypeScript', 24, 24, 720, 176, fs.BOUNDARY)
f.node('entry', '公共入口：注册 / 登录（管理员复用登录）', 48, 72, 672, 36, fs.SYS)
f.node('user_ui', '普通用户页面\n相册 · 照片 · 评论', 48, 132, 408, 44, fs.SYS)
f.node('admin_ui', '管理员页面\n相册类别维护', 480, 132, 240, 44, fs.SYS)
f.line([(252, 108), (252, 132)])
f.line([(600, 108), (600, 132)])

f.node('service', '应用服务（本机 FastAPI + Uvicorn）', 24, 248, 720, 430, fs.BOUNDARY)
f.node('control', '控制层 · Controller  |  FastAPI 路由', 48, 304, 672, 100, fs.BOUNDARY)
for key, title, x in [('request', '接收请求', 64), ('validate', '输入校验', 284), ('response', '返回 JSON', 504)]:
    f.node(key, title, x, 356, 200, 32, fs.SYS)

f.node('model', '模型层 · Model  |  业务逻辑与数据访问', 48, 476, 672, 176, fs.BOUNDARY)
for i, title in enumerate(['账户逻辑', '相册与类别逻辑', '照片逻辑', '评论逻辑']):
    f.node('business' + str(i), title, 64 + i * 164, 528, 148, 44, fs.SYS)
f.node('data_access', '数据访问（ORM 倾向 SQLAlchemy）', 64, 604, 400, 32, fs.BOX)
f.node('file_access', '图片文件处理', 488, 604, 216, 32, fs.BOX)

# 请求/响应与业务调用/结果分别画线，均通过边界指定入口。
f.line([(354, 200), (354, 248)])
f.text('HTTP 请求', 244, 214, 96)
f.line([(414, 248), (414, 200)])
f.text('JSON 响应', 428, 214, 96)
f.line([(354, 404), (354, 476)])
f.text('调度业务', 256, 428, 84)
f.line([(414, 476), (414, 404)])
f.text('处理结果', 428, 428, 84)

f.node('storage', '持久化存储（开发阶段均位于本机）', 24, 766, 720, 152, fs.BOUNDARY)
f.node('database', 'PostgreSQL · Docker 容器\n用户、相册、照片元数据、评论、类别', 48, 822, 408, 72, fs.BOX)
f.node('files', '本机 uploads/ 目录\n原图与缩略图文件', 480, 822, 240, 72, fs.BOX)
f.line([(264, 678), (264, 766)], BOTH)
f.text('SQL 读写', 154, 710, 96)
f.line([(600, 678), (600, 766)], BOTH)
f.text('文件读写', 614, 710, 96)

f.node('future', '后期文件存储（待定）：独立文件服务器 / 对象存储', 24, 1006, 720, 60, fs.BOX + 'dashed=1;')
f.line([(600, 918), (600, 1006)], fs.SEG_JUMP + 'dashed=1;')
f.text('按需求演进', 614, 950, 108)
f.save(768, 1090)

# 功能框架：三层树，扩展为用例的下一层，不与八个用例平级。
f = Figure(OUT, '图2-2_功能框架图')
f.node('system', '电子相册\n系统', 24, 464, 128, 72, BOLD)
modules = [
    ('account', '账户管理', 120, [
        ('register', '用户注册\n用户名、密码、邮箱', 40),
        ('login', '用户登录\n验证账户，按角色进入', 136)]),
    ('album', '相册管理', 376, [
        ('create', '创建相册\n名称、类别、公开/私有', 256),
        ('modify', '修改相册\n更新本人相册信息', 344),
        ('category', '相册类别管理\n管理员：添加、修改、删除', 432)]),
    ('photo', '照片管理', 656, [
        ('upload', '上传图片\n格式/大小校验，生成缩略图', 580),
        ('browse', '浏览照片\n公开相册及本人全部相册', 668)]),
    ('comment', '评论管理', 848, [
        ('publish', '对照片评论\n内容校验，按时间倒序展示', 816)]),
]
f.line([(152, 500), (200, 500)], fs.SEG_NONE)
f.line([(200, 120), (200, 848)], fs.SEG_NONE)
for key, title, cy, cases in modules:
    f.node(key, title, 232, cy - 26, 164, 52, BOLD)
    f.line([(200, cy), (232, cy)], fs.SEG_NONE)
    if len(cases) == 1:
        f.line([(396, cy), (488, cy)], fs.SEG_NONE)
    else:
        f.line([(396, cy), (440, cy)], fs.SEG_NONE)
        f.line([(440, cases[0][2] + 32), (440, cases[-1][2] + 32)], fs.SEG_NONE)
    for cid, text, y in cases:
        f.node(cid, text, 488, y, 256, 64, fs.BOX)
        if len(cases) > 1:
            f.line([(440, y + 32), (488, y + 32)], fs.SEG_NONE)

f.node('delete_comment', '删除自己的评论\n（评论用例扩展，确认后删除）', 488, 952, 256, 64, fs.NOTE)
f.line([(616, 880), (616, 952)], fs.SEG_JUMP + 'dashed=1;')
f.save(768, 1040)
