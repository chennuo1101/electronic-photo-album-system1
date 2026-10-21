"""检查本轮 23 张图的尺寸、文本、消息编号、实体字段及连线穿框。

运行：python tools/check_figure_delivery.py
这是静态几何检查，人工图义与视觉检查另记在 docs/图稿/返修检查记录.md。
"""
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from PIL import Image
from render_drawio import parse_style, font, wrap_text
from postprocess_png import content_bbox

ROOT = Path(__file__).resolve().parent.parent


def targets():
    return sorted(p for p in (ROOT/'docs/交付').glob('*/images/*.drawio')
                  if not p.parent.parent.name.startswith('1-')) + sorted((ROOT/'docs/图稿').glob('图2-*.drawio'))


def overlaps(a, b, inset=0):
    x,y,w,h=a; X,Y,W,H=b
    return min(x+w,X+W)-max(x,X)>inset and min(y+h,Y+H)-max(y,Y)>inset


def main():
    errors=[]; schemas={}; rows=[]
    paths=targets()
    assert len(paths)==23, len(paths)
    for p in paths:
        root=ET.parse(p).getroot(); boxes=[]; labels=[]; edges=[]; cells={}
        for c in root.iter('mxCell'):
            st=parse_style(c.get('style','')); g=c.find('mxGeometry')
            if g is None: continue
            key=c.get('id');value=c.get('value','');cells[key]=c
            if c.get('vertex'):
                r=tuple(float(g.get(n,0)) for n in ('x','y','width','height'))
                if st.get('shape')=='umlActor':
                    if r[2:]!=(30,60):errors.append((p.name,key,'参与者尺寸'))
                if st.get('shape')=='text':labels.append((key,value,r))
                elif st.get('strokeColor')!='none' and 'verticalAlign=top;spacingLeft=16' not in c.get('style',''):
                    boxes.append((key,r))
                if value and st.get('shape')!='umlActor':
                    size=int(st.get('fontSize',14)); f=font(size)
                    # 与渲染器同一换行口径；检查显示文字是否会超过框高。
                    available=r[2]-float(st.get('spacingLeft',0))-float(st.get('spacingRight',0))-8
                    lines=wrap_text(value,f,max(available,1))
                    needed=len(lines)*(24 if key.endswith(('_a','_m')) else size*1.25)
                    if needed>r[3]+2:errors.append((p.name,key,'文字高度超框',round(needed),r[3]))
            if c.get('edge'):
                start=g.find("mxPoint[@as='sourcePoint']");end=g.find("mxPoint[@as='targetPoint']")
                if start is None or end is None:errors.append((p.name,key,'缺少显式端点'));continue
                pts=[start]+list(g.findall('Array/mxPoint'))+[end]
                edges.append((key,[(float(q.get('x')),float(q.get('y'))) for q in pts],st))
        for key,pts,st in edges:
            for a,b in zip(pts,pts[1:]):
                x,y=a;X,Y=b
                if x!=X and y!=Y:
                    if '用例图' not in p.name:errors.append((p.name,key,'非正交线'))
                    continue
                for other,(bx,by,bw,bh) in boxes:
                    hit=(y==Y and by+.1<y<by+bh-.1 and min(max(x,X),bx+bw-.1)>max(min(x,X),bx+.1)) or (x==X and bx+.1<x<bx+bw-.1 and min(max(y,Y),by+bh-.1)>max(min(y,Y),by+.1))
                    if hit:errors.append((p.name,key,'连线穿框',other))
        for i,(key,value,r) in enumerate(labels):
            for other,rr in boxes:
                if overlaps(r,rr,1):errors.append((p.name,key,'标签碰框',other))
            for other,_,rr in labels[i+1:]:
                if overlaps(r,rr,1):errors.append((p.name,key,'标签互相重叠',other))
        if '协作图' in p.name:
            nums=sorted(int(m.group(1)) for _,v,_ in labels if (m:=re.match(r'^(\d+)\*?:',v)))
            if nums!=list(range(1,len(nums)+1)):errors.append((p.name,'消息编号不连续',nums))
        if '类模型图' in p.name:
            for key,c in cells.items():
                title=c.get('value','')
                if title.startswith('«entity»'):
                    entity=title.split('»',1)[1].strip()
                    attrs=cells[key[:-2]+'_a'].get('value','')
                    if entity in schemas and schemas[entity]!=attrs:errors.append((p.name,entity,'实体字段不一致'))
                    schemas[entity]=attrs
        im=Image.open(p.with_suffix('.png')).convert('RGB');bbox=content_bbox(im)
        w=(bbox[2]-bbox[0])/2;h=(bbox[3]-bbox[1])/2
        limit=600 if '用例图' in p.name else 660 if '活动图' in p.name else 700 if '协作图' in p.name else 760
        if w>limit+2:errors.append((p.name,'内容宽超标',w,limit))
        body=13 if '类模型图' in p.name else 14
        if body*439.4/w<8 or 12*439.4/w<7:errors.append((p.name,'满宽字号偏小'))
        if '活动图' in p.name and w/h>1.3:errors.append((p.name,'活动图宽高比'))
        if '协作图' in p.name and w/h>2.8:errors.append((p.name,'协作图宽高比'))
        rows.append((p.name,round(w,1),round(body*439.4/w,1),round(12*439.4/w,1)))
    for row in rows:print(*row,sep=' | ')
    for error in errors:print('FAIL',error)
    print(f'{len(paths)} 张图；{len(errors)} 项待修正。')
    if errors:raise SystemExit(1)


if __name__=='__main__':main()
