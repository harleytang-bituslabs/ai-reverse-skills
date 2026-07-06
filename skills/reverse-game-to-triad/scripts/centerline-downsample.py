#!/usr/bin/env python3
# centerline 降采样到 ~45 点, 给 HTML SVG 画 S 弯用 (仅滚动/路径类游戏)。
# 跑: python3 centerline-downsample.py <game>/public/assets/.../centerline.json
import json,sys
d=json.load(open(sys.argv[1]));a=d['anchors'];step=max(1,len(a)//45)
ds=[{"iy":a[i]['iy'],"ix":round(a[i]['ix'],1)} for i in range(0,len(a),step)]
print("CENTERLINE =",json.dumps(ds))
