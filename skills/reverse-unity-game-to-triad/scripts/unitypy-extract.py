#!/usr/bin/env python3
# 从 Unity 档(data.unity3d 或 Addressables 的 *.bundle)抽取三件套的原料:
#   贴图/精灵 -> PNG(art/), 音频 -> 文件(audio/), RectTransform/Canvas 树 -> JSON(布局),
#   MonoBehaviour -> JSON(玩法配置,best-effort), 列 TextAsset(Spine 图集/配置)。
# 依赖: pip install UnityPy   (音频可能需 pip install fsb5)
# 用: python3 unitypy-extract.py <data.unity3d 或 *.bundle> [outdir]
import UnityPy, sys, os, json, collections
src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "extract"
env = UnityPy.load(src)
os.makedirs(f"{out}/art", exist_ok=True)
os.makedirs(f"{out}/audio", exist_ok=True)

types = collections.Counter(o.type.name for o in env.objects)
print("=== 对象类型 ===")
for t, n in types.most_common(20): print(f"  {n:>5}  {t}")

def safe(s): return "".join(c if c.isalnum() or c in "-_" else "_" for c in (s or ""))[:48] or "unnamed"

art = au = 0
for o in env.objects:
    tn = o.type.name
    try:
        if tn in ("Sprite", "Texture2D"):
            d = o.read(); img = getattr(d, "image", None)
            if img:
                img.save(f"{out}/art/{safe(getattr(d,'m_Name',''))}_{art}.png"); art += 1
        elif tn == "AudioClip":
            d = o.read()
            for n, b in (getattr(d, "samples", {}) or {}).items():
                open(f"{out}/audio/{n}", "wb").write(b); au += 1
    except Exception:
        pass

# 布局: RectTransform 锚点/位置/尺寸 + 所属 GameObject 名(灰盒坐标的来源)
rt = []
for o in env.objects:
    if o.type.name == "RectTransform":
        try:
            d = o.read()
            go = d.m_GameObject.read() if getattr(d, "m_GameObject", None) else None
            v = lambda p: [round(p.x, 2), round(p.y, 2)]
            rt.append({"go": getattr(go, "m_Name", "") if go else "",
                       "anchorMin": v(d.m_AnchorMin), "anchorMax": v(d.m_AnchorMax),
                       "anchoredPos": v(d.m_AnchoredPosition), "sizeDelta": v(d.m_SizeDelta),
                       "pivot": v(d.m_Pivot)})
        except Exception:
            pass
json.dump(rt, open(f"{out}/rect_transforms.json", "w"), ensure_ascii=False, indent=0)

# MonoBehaviour 配置(下注/赔付/转轮等). WebGL release 常剥离 typetree -> 可能读不全,best-effort.
mb = []
for o in env.objects:
    if o.type.name == "MonoBehaviour":
        try:
            d = o.read_typetree()
            if d and d.get("m_Name"): mb.append(d)
        except Exception:
            pass
json.dump(mb, open(f"{out}/monobehaviours.json", "w"), ensure_ascii=False, indent=0, default=str)

ta = [o.read().m_Name for o in env.objects if o.type.name == "TextAsset"]
print(f"\nart={art}  audio={au}  rectTransforms={len(rt)}  monoBehaviours={len(mb)}(可读)")
print(f"textAssets({len(ta)}): {ta[:16]}")
print(f"=> {out}/art  {out}/audio  {out}/rect_transforms.json  {out}/monobehaviours.json")
if not mb:
    print("   注: MonoBehaviour 读不到 typetree(IL2CPP 剥离)。要读玩法配置需用 global-metadata.dat")
    print("   生成 typetree(UnityPy TypeTreeGenerator + Il2CppDumper),或玩法/数学转向服务端/截图。")
