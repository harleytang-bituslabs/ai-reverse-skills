#!/usr/bin/env python3
# 把 Addressables bundle 里的 prefab/canvas 根合成为屏幕 px,并入 compose-all.py 产出的
# master JSON。运行时实例化的 UI(设置/弹窗/免费过场…)常只在 bundle 里 —— 不跑本脚本
# 会误判"不在构建"(SKILL §8 坑)。
#
# ★ 内置 403 存根检测:S3 下载失败常把 AccessDenied XML(约 240~300 B)存成 .bundle,
#   静默混进目录。本脚本发现即报警并跳过 —— 这些 bundle 要记入"未取到"缺口清单。
#
# 用法: python3 compose-bundles.py [bundles目录=bundles] [--master all_layout.json]
import json, glob, os, sys
import UnityPy

argv = sys.argv[1:]
bdir = "bundles"; master_path = "all_layout.json"
i = 0
while i < len(argv):
    if argv[i] == "--master": master_path = argv[i+1]; i += 2
    else: bdir = argv[i]; i += 1

master = json.load(open(master_path)) if os.path.exists(master_path) else {}

def comps(go):
    out = []
    for p in (getattr(go, "m_Component", []) or []):
        try: out.append(p.component.read())
        except Exception: pass
    return out
def has_cr(go): return any(c.object_reader.type.name == "CanvasRenderer" for c in comps(go))
def has_canvas(go): return any(c.object_reader.type.name == "Canvas" for c in comps(go))
def nm_of(rt):
    try: return rt.m_GameObject.read().m_Name
    except Exception: return "?"

def walk(rt, pbx, pby, pw, ph, rh, depth, out, pn):
    try:
        go = rt.m_GameObject.read(); nm = go.m_Name
        a0, a1 = rt.m_AnchorMin, rt.m_AnchorMax
        ap, sd, pv = rt.m_AnchoredPosition, rt.m_SizeDelta, rt.m_Pivot
    except Exception: return
    w = (a1.x - a0.x) * pw + sd.x; h = (a1.y - a0.y) * ph + sd.y
    rx = pbx + pw * (a0.x + (a1.x - a0.x) * pv.x); ry = pby + ph * (a0.y + (a1.y - a0.y) * pv.y)
    blx = rx + ap.x - pv.x * w; bly = ry + ap.y - pv.y * h; top_y = rh - (bly + h)
    p = pn + [nm]
    out.append({"depth": depth, "name": nm, "path": "/".join(p), "x": round(blx), "y": round(top_y),
                "w": round(w), "h": round(h), "cr": has_cr(go), "act": bool(go.m_IsActive)})
    for ch in (getattr(rt, "m_Children", []) or []):
        try: walk(ch.read(), blx, bly, w, h, rh, depth + 1, out, p)
        except Exception: pass

def father(rt):
    f = getattr(rt, "m_Father", None)
    try: return f.read() if f and f.path_id != 0 else None
    except Exception: return None

def ref_for(nm):
    if "Horizontal" in nm: return (1920.0, 1080.0)
    return (1080.0, 1920.0)

added = 0; stubs = []
for bundle in sorted(glob.glob(os.path.join(bdir, "*.bundle"))):
    base = os.path.basename(bundle)
    pack = base.split("_assets_all_")[0]
    # 403 存根检测:太小 / 内容是 S3 错误 XML → 不是 bundle
    if os.path.getsize(bundle) < 2048:
        head = open(bundle, "rb").read(512)
        if b"AccessDenied" in head or b"<Error>" in head or not head.startswith(b"Unity"):
            stubs.append(base); continue
    try:
        env = UnityPy.load(bundle)
    except Exception as e:
        print(f"  !! 载入失败(跳过): {base}: {e}"); stubs.append(base); continue
    rts = []
    for o in env.objects:
        if o.type.name == "RectTransform":
            try: rts.append(o.read())
            except Exception: pass
    roots = [rt for rt in rts if father(rt) is None]
    for rt in roots:
        nm = nm_of(rt)
        if "Debug" in nm: continue
        is_canvas = has_canvas(rt.m_GameObject.read())
        W, H = ref_for(nm)
        out = []
        if is_canvas:
            for ch in (rt.m_Children or []):
                try: walk(ch.read(), 0, 0, W, H, H, 1, out, [nm])
                except Exception: pass
        else:
            sd = rt.m_SizeDelta; fw = sd.x or W; fh = sd.y or H
            if fw < 10 or fh < 10: fw, fh = W, H
            if "Horizontal" in nm: fw, fh = 1920.0, 1080.0
            elif "Vertical" in nm: fw, fh = 1080.0, 1920.0
            walk(rt, 0, 0, fw, fh, fh, 0, out, [])
            W, H = round(fw), round(fh)
        if len(out) >= 4:
            key = f"[{pack}] {nm}"
            if key in master: continue
            master[key] = {"kind": "bundle", "pack": pack, "ref": [W, H], "nodes": out}
            added += 1

json.dump(master, open(master_path, "w"), ensure_ascii=False, indent=0)
print("added bundle screens:", added, "total screens:", len(master))
if stubs:
    print(f"\n  ⚠ {len(stubs)} 个文件是 403/AccessDenied 存根或坏包(未取到,记入缺口清单):")
    for s in stubs: print("    -", s)
for k, v in sorted(master.items()):
    if v.get("kind") == "bundle":
        vis = sum(1 for n in v["nodes"] if n["cr"])
        print(f"  {len(v['nodes']):>4} ({vis:>3} cr) ref={v['ref']}  {k}")
