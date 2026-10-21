"""v2.1 图稿的重复布局；业务文字由各模块生成脚本提供。"""
from pathlib import Path
import figstyle as fs


class Figure:
    def __init__(self, out, name):
        self.path = Path(out) / (name + '.drawio')
        self.cells = []
        self.nodes = {}
        self.i = 0

    def node(self, key, text, x, y, w=280, h=44, style=None):
        self.nodes[key] = (x, y, w, h)
        self.cells.append(fs.vertex(key, text, style or fs.SYS, x, y, w, h))

    def text(self, text, x, y, w=100, h=18, align='center'):
        self.i += 1
        # 独立白底标签：在 draw.io 与应急渲染器中都能衬白。
        st = (fs.TEXT if align == 'center' else fs.TEXT_L if align == 'left' else fs.TEXT_R)
        self.cells.append(fs.label('label'+str(self.i), text, x, y, w, h,
                                   style=st.replace('fillColor=none', 'fillColor=#FFFFFF')))

    def line(self, points, style=None):
        self.i += 1
        self.cells.append(fs.poly('edge'+str(self.i), points, style or fs.SEG_JUMP))

    def down(self, a, b, label=None):
        x, y, w, h = self.nodes[a]
        bx, by, bw, _ = self.nodes[b]
        self.line([(x+w/2, y+h), (bx+bw/2, by)])
        if label:
            self.text(label, x+w/2-30, y+h+5, 22)

    def end(self, key, x, y):
        self.node(key, '', x, y, 24, 24, fs.END)
        self.node(key+'_dot', '', x+6, y+6, 12, 12, fs.START)

    def start(self, x=152, y=24):
        self.node('start', '', x, y, 24, 24, fs.START)

    def decision(self, key, text, y):
        self.node(key, text, 74, y, 180, 76, fs.DIAMOND)

    def error(self, decision, text, back, yes='否', channel=604):
        _, y, _, h = self.nodes[decision]
        cy = y+h/2
        self.node(decision+'_err', text, 354, cy-26, 190, 52, fs.NOTE)
        self.line([(254, cy), (354, cy)])
        self.text(yes, 280, cy-26, 24)
        bx, by, bw, bh = self.nodes[back]
        self.line([(544, cy), (channel, cy), (channel, by+bh/2), (bx+bw, by+bh/2)])

    def save(self, w, h):
        fs.save(self.path, self.cells, w, h)


def usecases(out, name, cases, actors):
    f = Figure(out, name)
    f.node('boundary', '电子相册系统', 150, 24, 380, 320, fs.BOUNDARY)
    for i, name in enumerate(cases):
        f.node('uc'+str(i), name, 350, 86+i*170, 160, 52, fs.USECASE)
    for i, (name, indices) in enumerate(actors):
        center = sum(112+j*170 for j in indices)/len(indices)
        f.node('actor'+str(i), name, 60, center-30, 30, 60, fs.ACTOR)
        for j in indices:
            f.line([(90, center), (350, 112+j*170)], fs.SEG_NONE)
    f.save(554, 368)


ALBUM = ['相册编号', '相册名称', '类别编号', '公开/私有', '创建者编号', '创建时间']
PHOTO = ['照片编号', '文件路径', '缩略图路径', '所属相册', '上传者', '上传时间']
CATEGORY = ['类别编号', '类别名称']
COMMENT = ['评论编号', '评论内容', '评论时间', '用户编号', '照片编号']
USER = ['用户名', '密码', '邮箱', '角色']


def classes(out, name, nodes, relations):
    """节点为 (id,版型,名称,属性,方法,x,y)，关联为显式路径及三段标签。"""
    f = Figure(out, name)
    max_y = 0
    for key, kind, title, attrs, methods, x, y in nodes:
        cells, h = fs.classbox(key, kind, title, attrs, methods, x, y, 210)
        f.cells += cells
        f.nodes[key] = (x, y, 210, h)
        max_y = max(max_y, y+h)
    for points, labels in relations:
        f.line(points, fs.SEG_OPEN+'jumpStyle=arc;jumpSize=6;')
        for text, x, y, w in labels:
            f.text(text, x, y, w)
    f.save(668, max_y+24)


def horizontal(y, title, left='1', right='1'):
    return ([(234,y),(414,y)], [(left,244,y-27,28),(title,280,y-27,94),(right,376,y-27,30)])


def vertical(x, y1, y2, title, top='1', bottom='0..*'):
    return ([(x,y1),(x,y2)], [(top,x+12,y1+10,30),(title,x+12,(y1+y2)/2-9,96),(bottom,x+12,y2-28,40)])


def collaboration(out, name, actor, page, ctl, actor_messages, requests, entities):
    """样板骨架：参与者/页面在上，控制器/实体在下。

    requests: (编号,方向,文字)，实体消息同结构；方向 > 为请求、< 为返回。
    页面与控制器的多条消息各走独立竖线，标签分置外侧，保持完整编号。
    """
    f = Figure(out, name)
    f.node('actor', actor, 40, 80, 30, 60, fs.ACTOR)
    f.node('page', page, 220, 64, 150, 50)
    for i,(num,direction,text) in enumerate(actor_messages):
        # 两条用户交互消息分别在参与者上、下方标注。
        y = 84+i*22
        f.line([(70,y),(220,y)] if direction=='>' else [(220,y),(70,y)])
        f.text(f'{num}: {text}', 76, y-26 if i==0 else y+8, 140, 32)
    count = max((len(msgs) for _,msgs in entities), default=2)
    height = max(80, min(120, count*30))
    f.node('ctl', ctl, 220, 340, 150, height)
    downs = [m for m in requests if m[1]=='>']
    ups = [m for m in requests if m[1]=='<']
    for group, right in [(downs,False),(ups,True)]:
        for i,(num,_,text) in enumerate(group):
            x = (246 if not right else 314)+i*18
            f.line([(x,114),(x,340)] if not right else [(x,340),(x,114)])
            f.text(f'{num}: {text}', 84 if not right else 376, 174+i*48, 150, 36,
                   'right' if not right else 'left')
    bottom = 340+height
    for j,(entity,msgs) in enumerate(entities):
        y = 340+j*230
        h = max(50,len(msgs)*30)
        # 消息最多四条；不同实体纵向分排，避免挤成五列。
        f.node('entity'+str(j), entity, 550, y, 150, h, fs.BOX)
        bottom = max(bottom,y+h)
        for i,(num,direction,text) in enumerate(msgs):
            ey = y+25+i*30
            if j==0:
                sy = 340+25+i*30
                pts = [(370,sy),(550,ey)]
            else:
                # 从控制器底缘独立引出，先在两列之间下行。
                sx = 230+(j-1)*64+i*16
                channel_y = y+25+i*30
                pts = [(sx,340+height),(sx,channel_y),(550,ey)]
            if direction=='<': pts=pts[::-1]
            f.line(pts)
            f.text(f'{num}: {text}', 380, ey-24, 158, 20)
    f.save(724,bottom+24)
