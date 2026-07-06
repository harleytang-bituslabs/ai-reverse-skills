#!/usr/bin/env python3
# 合成 Unity UI 的屏幕 px —— 把 RectTransform 锚点/pivot/sizeDelta 沿层级合成成
# 左上原点的绝对像素框。封装了两个必踩的坑(见 SKILL §5/§8):
#   坑①(中心 pivot 偏移): screen-space Canvas 的 RectTransform 自身锚在屏幕中心,
#       直接拿它当根会把所有子节点偏 −W/2,+H/2。正确做法 = 对每个顶层 Canvas,
#       把它的【直接子节点】放进干净的 (0,0,W,H) 帧从头合成。
#   坑②(可见性): IL2CPP 剥 typetree → Image/Text MonoBehaviour 读空,但
#       RectTransform + CanvasRenderer 照样可读。判"是否上屏可见"看 CanvasRenderer 存在,
#       不看 Image MB 能否读。输出每个节点都带 cr=(有无 CanvasRenderer) 与 act=(IsActive)。
#
# ⚠️ 仅对 Canvas(screen-space UI)有效。世界空间游戏板(转轮/连击徽标/盘龙)在 runtime
#    被 useGameScale/scale 链重排,静态世界坐标投影≠屏幕真值 —— 那些去找 UI 复刻件
#    (如帮助/单注详情页里的 ScenarioGrid)当权威,别用本脚本投影世界 Transform。
#
# 用法:
#   python3 compose-layout.py <data.unity3d>                      # 列出所有 Canvas
#   python3 compose-layout.py <data.unity3d> Canvas_PlayerHUD     # 合成某 Canvas 全树
#   python3 compose-layout.py <data.unity3d> --node ScenarioGrid  # 合成某具名子树(任意 RT 根)
#   python3 compose-layout.py <data.unity3d> Canvas_X 1080 1920   # 自定参考分辨率(默认 1080×1920)
import sys, json
import UnityPy

if len(sys.argv) < 2:
    print("用法: compose-layout.py <data.unity3d> [CanvasName | --node NodeName] [W H]"); sys.exit(1)
path = sys.argv[1]
args = sys.argv[2:]
node_mode = False
target = None
if args and args[0] == "--node":
    node_mode = True; target = args[1] if len(args) > 1 else None; args = args[2:]
elif args and not args[0].isdigit():
    target = args[0]; args = args[1:]
W = float(args[0]) if len(args) > 0 else 1080.0
H = float(args[1]) if len(args) > 1 else 1920.0

env = UnityPy.load(path)

def comps(go):
    out = []
    for p in (getattr(go, "m_Component", []) or []):
        try: out.append(p.component.read())
        except Exception: pass
    return out

def has_cr(go):
    return any(c.object_reader.type.name == "CanvasRenderer" for c in comps(go))

def name_of(rt):
    try: return rt.m_GameObject.read().m_Name
    except Exception: return "?"

def find_rt(pred):
    hits = []
    for o in env.objects:
        if o.type.name == "RectTransform":
            try:
                d = o.read()
                if pred(d): hits.append(d)
            except Exception: pass
    return hits

def walk(rt, pbx, pby, pw, ph, rh, depth, out):
    """pbx,pby = 父矩形左下角(Unity y 向上);pw,ph = 父矩形尺寸;rh = 根高(用于翻成左上 y)。"""
    go = rt.m_GameObject.read(); nm = go.m_Name
    try:
        a0, a1 = rt.m_AnchorMin, rt.m_AnchorMax
        ap, sd, pv = rt.m_AnchoredPosition, rt.m_SizeDelta, rt.m_Pivot
    except Exception:
        return
    w = (a1.x - a0.x) * pw + sd.x
    h = (a1.y - a0.y) * ph + sd.y
    rx = pbx + pw * (a0.x + (a1.x - a0.x) * pv.x)
    ry = pby + ph * (a0.y + (a1.y - a0.y) * pv.y)
    blx = rx + ap.x - pv.x * w           # 左下角 x
    bly = ry + ap.y - pv.y * h           # 左下角 y(Unity 系)
    top_y = rh - (bly + h)               # 翻成左上原点 y
    out.append({"depth": depth, "name": nm,
                "x": round(blx), "y": round(top_y), "w": round(w), "h": round(h),
                "cr": has_cr(go), "act": bool(go.m_IsActive)})
    for ch in (getattr(rt, "m_Children", []) or []):
        try: walk(ch.read(), blx, bly, w, h, rh, depth + 1, out)
        except Exception: pass

# 列出所有 Canvas
canvases = []
for o in env.objects:
    if o.type.name == "Canvas":
        try: canvases.append(name_of(o.read().m_GameObject.read().m_Component and o.read()))
        except Exception: pass
canvas_names = []
for o in env.objects:
    if o.type.name == "RectTransform":
        try:
            d = o.read(); go = d.m_GameObject.read()
            if any(c.object_reader.type.name == "Canvas" for c in comps(go)):
                canvas_names.append(go.m_Name)
        except Exception: pass

if not target:
    print(f"=== Canvas 列表(参考分辨率 {W:.0f}×{H:.0f}) ===")
    for n in sorted(set(canvas_names)):
        print(" ", n)
    print("\n再指定其一: compose-layout.py <data.unity3d> <CanvasName>")
    print("或具名子树: compose-layout.py <data.unity3d> --node <NodeName>")
    sys.exit(0)

roots = find_rt(lambda d: name_of(d) == target)
if not roots:
    print(f"未找到 RectTransform 名为 {target!r}"); sys.exit(2)

out = []
for root in roots:
    if node_mode:
        # 具名子树:把该节点自身放进干净 (0,0,W,H) 帧(它的 sizeDelta 即其帧)
        sd = root.m_SizeDelta
        fw = sd.x or W; fh = sd.y or H
        walk(root, 0, 0, fw, fh, fh, 0, out)
    else:
        # Canvas:跳过 Canvas RT 自身,从其直接子节点在干净 (0,0,W,H) 帧合成(避中心 pivot 偏移)
        for ch in (root.m_Children or []):
            try: walk(ch.read(), 0, 0, W, H, H, 1, out)
            except Exception: pass

print(f"=== {target}  (屏幕 px, 左上原点, 帧 {W:.0f}×{H:.0f}) ===")
print("   [x,y w×h]  cr=有CanvasRenderer(上屏可见)  act=IsActive")
for n in out:
    ind = "  " * min(n["depth"], 6)
    print(f"  {ind}{n['name'][:30]:30} [{n['x']},{n['y']} {n['w']}x{n['h']}] cr={n['cr']} act={n['act']}")
# 也吐 JSON 便于程序消费
import os
dst = os.path.join(os.path.dirname(path) or ".", f"layout_{target}.json")
json.dump(out, open(dst, "w"), ensure_ascii=False, indent=0)
print(f"\n=> {dst}  ({len(out)} 节点)")
