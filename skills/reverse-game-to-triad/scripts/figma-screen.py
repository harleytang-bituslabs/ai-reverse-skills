#!/usr/bin/env python3
# 从 .art-meta/nodes.json 抽某个 Figma 屏的子节点局部坐标 (截不到的屏的精确来源)。
# 每 frame 的 absoluteBoundingBox 即 1:1 画布; 子坐标 = 子 bbox - frame 原点。
# 跑: python3 figma-screen.py .art-meta/nodes.json loading_screen_login_expired
import json,sys
d=json.load(open(sys.argv[1]))                      # .art-meta/nodes.json
node=list(d['nodes'].values())[0]['document']
frames={}
for sec in node.get('children',[]):                 # SECTION 层
    for fr in sec.get('children',[]): frames[fr['name']]=fr
fr=frames[sys.argv[2]]; ox,oy=fr['absoluteBoundingBox']['x'],fr['absoluteBoundingBox']['y']
def rec(n,dep=0):
    b=n.get('absoluteBoundingBox')
    if b and n['type']!='SECTION':
        x,y=b['x']-ox,b['y']-oy                      # 屏内局部坐标
        t=('“'+n.get('characters','')[:30]+'” ') if n['type']=='TEXT' else ''
        print(f"{'  '*dep}[{n['type']}] {n['name'][:30]:30} {x:.0f},{y:.0f} {b['width']:.0f}×{b['height']:.0f} {t}")
    for c in n.get('children',[]): rec(c,dep+1)
rec(fr)
