#!/usr/bin/env python3
# 穷尽合成:把 data.unity3d 里【所有 Canvas + 所有独立 prefab 根】沿 RectTransform
# 合成为屏幕 px,写进一份 master JSON(默认 all_layout.json)。这是数据驱动灰盒的
# 数据底座(SKILL §5.1):先穷尽 dump,再人工筛屏,保证"不漏件"。
#
# 与 compose-layout.py 的关系:compose-layout 是单 Canvas/单子树的交互式探查;
# 本脚本是一次性全量 dump。两个坑(中心 pivot / CanvasRenderer 可见性)同样封装。
#
# 朝向 heuristic:节点名含 Horizontal → 1920×1080;含 Vertical → 1080×1920;
# 否则用 --ref 默认(竖 1080×1920)。游戏特定的例外(如某世界 UI 板)自行改名单。
#
# 用法: python3 compose-all.py <data.unity3d> [--ref W H] [--out all_layout.json]
import sys, json
import UnityPy

argv = sys.argv[1:]
if not argv:
    print("用法: compose-all.py <data.unity3d> [--ref W H] [--out all_layout.json]"); sys.exit(1)
path = argv[0]; ref_w, ref_h = 1080.0, 1920.0; out_path = "all_layout.json"
i = 1
while i < len(argv):
    if argv[i] == "--ref": ref_w, ref_h = float(argv[i+1]), float(argv[i+2]); i += 3
    elif argv[i] == "--out": out_path = argv[i+1]; i += 2
    else: i += 1

env = UnityPy.load(path)

def comps(go):
    out = []
    for p in (getattr(go, "m_Component", []) or []):
        try: out.append(p.component.read())
        except Exception: pass
    return out
def has_cr(go): return any(c.object_reader.type.name == "CanvasRenderer" for c in comps(go))
def has_canvas(go): return any(c.object_reader.type.name == "Canvas" for c in comps(go))
def name_of(rt):
    try: return rt.m_GameObject.read().m_Name
    except Exception: return "?"

def walk(rt, pbx, pby, pw, ph, rh, depth, out, path_names):
    try:
        go = rt.m_GameObject.read(); nm = go.m_Name
        a0, a1 = rt.m_AnchorMin, rt.m_AnchorMax
        ap, sd, pv = rt.m_AnchoredPosition, rt.m_SizeDelta, rt.m_Pivot
    except Exception:
        return
    w = (a1.x - a0.x) * pw + sd.x; h = (a1.y - a0.y) * ph + sd.y
    rx = pbx + pw * (a0.x + (a1.x - a0.x) * pv.x)
    ry = pby + ph * (a0.y + (a1.y - a0.y) * pv.y)
    blx = rx + ap.x - pv.x * w; bly = ry + ap.y - pv.y * h
    top_y = rh - (bly + h)
    pn = path_names + [nm]
    out.append({"depth": depth, "name": nm, "path": "/".join(pn),
                "x": round(blx), "y": round(top_y), "w": round(w), "h": round(h),
                "cr": has_cr(go), "act": bool(go.m_IsActive)})
    for ch in (getattr(rt, "m_Children", []) or []):
        try: walk(ch.read(), blx, bly, w, h, rh, depth + 1, out, pn)
        except Exception: pass

def father(rt):
    f = getattr(rt, "m_Father", None)
    try: return f.read() if f and f.path_id != 0 else None
    except Exception: return None

def ref_for(nm):
    if "Horizontal" in nm: return (1920.0, 1080.0)
    if "Vertical" in nm: return (1080.0, 1920.0)
    return (ref_w, ref_h)

all_rts = []
for o in env.objects:
    if o.type.name == "RectTransform":
        try: all_rts.append(o.read())
        except Exception: pass

canvas_rts = [rt for rt in all_rts if has_canvas(rt.m_GameObject.read())]
root_rts = [rt for rt in all_rts if father(rt) is None]
prefab_roots = [rt for rt in root_rts if not has_canvas(rt.m_GameObject.read())
                and len(getattr(rt, "m_Children", []) or []) > 0]

screens = {}
for rt in canvas_rts:
    nm = name_of(rt); W, H = ref_for(nm)
    out = []
    for ch in (rt.m_Children or []):     # Canvas 直接子节点从干净 (0,0,W,H) 帧起(避中心 pivot 偏移)
        try: walk(ch.read(), 0, 0, W, H, H, 1, out, [nm])
        except Exception: pass
    if out: screens[nm] = {"kind": "canvas", "ref": [W, H], "nodes": out}

for rt in prefab_roots:                  # 按需实例化 prefab 根(不在任何 Canvas 下,运行时挂载)
    nm = name_of(rt)
    if nm in screens: continue
    sd = rt.m_SizeDelta; fw = sd.x or ref_w; fh = sd.y or ref_h
    if fw < 10 or fh < 10: fw, fh = ref_for(nm)
    out = []; walk(rt, 0, 0, fw, fh, fh, 0, out, [])
    if len(out) >= 3:
        screens["[prefab] " + nm] = {"kind": "prefab", "ref": [round(fw), round(fh)], "nodes": out}

json.dump(screens, open(out_path, "w"), ensure_ascii=False, indent=0)
print("screens dumped:", len(screens), "->", out_path)
for k, v in sorted(screens.items(), key=lambda kv: -len(kv[1]["nodes"])):
    vis = sum(1 for n in v["nodes"] if n["cr"])
    print(f"  {len(v['nodes']):>4} nodes ({vis:>3} cr) ref={v['ref']}  {k}")
