#!/usr/bin/env python3
# 通用数据驱动灰盒生成器(SKILL §5.1):
#   all_layout.json(compose-all + compose-bundles 的穷尽合成) + 手写 manifest(游戏特定筛选/分区/注入)
#   → UI-GREYBOX-<CODE>.html
#
# 渲染器是【可复用件】;数据必须每游戏回源重导(all_layout 重跑,manifest 现写),
# 绝不复制上一游戏的 manifest 改数(SKILL §0★★ 借旧骨架之坑)。
#
# manifest(JSON,游戏特定)结构:
# {
#   "code":"SS02", "title":"Beach Party / 沙滩派对", "version":"1.0.0-71",
#   "source_note":"data.unity3d + 全部 UI/gameplay bundle;Loading=宿主 React",
#   "exclude":["Debug","ScreenEmptyClicker"],          // 屏 key 含这些子串则丢弃
#   "inject":{ "<屏key>":{"kind":"host|world|scene","ref":[W,H],"note":"…","nodes":[…]} },
#                                                      // 补代码合成之外的屏:宿主 React loading、
#                                                      // 世界空间实测复刻、超屏 scene 卡
#   "sections":[ ["① Loading(宿主壳)",["<屏key>",…]], … ],   // §5.0 硬清单顺序;未列 key 自动进"未归类"
#   "badges":{ "<屏key>":"validated|extracted|derived" },     // 覆盖默认(canvas/bundle/prefab=extracted,host/world=derived)
#   "scenes":["<屏key>",…],                            // 超屏卡:box 允许越出 ref(自检放行)
#   "bleed":["ScreenBoard","Veil","Mask","Strip_"],    // 游戏特定:名字/路径含这些子串的 box 标 bleed
#                                                      // (双朝向共用盖板/出血装饰,故意越界——逐条核实后才加)
#   "symbols":[["显示名","备注","资产名"],…],           // 可选:符号集条
#   "notes":["…",…]                                    // 可选:页脚注释(屏覆盖/分离/来源/缺口)
# }
#
# 用法: python3 gen-greybox.py --layout all_layout.json --manifest greybox-manifest.json --out UI-GREYBOX-XX.html
import json, html, sys

argv = sys.argv[1:]
layout_p, manifest_p, out_p = "all_layout.json", "greybox-manifest.json", None
i = 0
while i < len(argv):
    if argv[i] == "--layout": layout_p = argv[i+1]; i += 2
    elif argv[i] == "--manifest": manifest_p = argv[i+1]; i += 2
    elif argv[i] == "--out": out_p = argv[i+1]; i += 2
    else: i += 1

M = json.load(open(manifest_p))
scr = json.load(open(layout_p))
code = M.get("code", "GAME")
out_p = out_p or f"UI-GREYBOX-{code}.html"

exclude = M.get("exclude", [])
scr = {k: v for k, v in scr.items() if not any(e in k for e in exclude)}
for k, v in M.get("inject", {}).items():
    scr[k] = v

scene_keys = set(M.get("scenes", []))
badges = M.get("badges", {})
bleed_marks = M.get("bleed", [])
SCROLL_PAT = ("Viewport", "ScrollView", "ScrollContents", "ScrollPanel", "ScrollRect", "Scrollbar")

def role_of(n):
    """python 侧预计算 data-role:滚动内容自动 offscreen;manifest bleed 名单标 bleed。"""
    p = n.get("path", n["name"])
    tags = []
    if any(s in p for s in SCROLL_PAT): tags.append("offscreen:scroll")
    if any(b in n["name"] or b in p for b in bleed_marks): tags.append("bleed")
    return (";".join(tags) + ";" if tags else "") + p

for v in scr.values():
    for n in v["nodes"]:
        n["role"] = role_of(n)

SECTIONS = [tuple(s) for s in M.get("sections", [])]
placed = set()
for _, ks in SECTIONS: placed.update(ks)
misc = [k for k in scr if k not in placed]
if misc: SECTIONS.append(("其它 prefab / 特效 / 未归类", sorted(misc)))

def esc(s): return html.escape(str(s))

seen_disp = set()
def screen_card(name):
    v = scr.get(name)
    if not v: return ""
    disp = name.split("] ")[-1] if name.startswith("[") else name
    if disp in seen_disp: return ""      # 同 prefab 双源(data.unity3d + bundle)去重
    seen_disp.add(disp)
    W, H = v["ref"]; nodes = v["nodes"]; note = v.get("note", ""); kind = v.get("kind", "")
    pack = v.get("pack", ""); vis = sum(1 for n in nodes if n["cr"])
    bd = badges.get(name) or {"world": "derived", "host": "derived", "scene": "extracted"}.get(kind, "extracted")
    src = pack or kind
    scene_attr = ' data-scene="1"' if (name in scene_keys or kind == "scene") else ""
    js = json.dumps(nodes, ensure_ascii=False)
    return (f'<div class="frame"><div class="cap">{esc(disp)}<span class="tag">{esc(src)}</span>'
            f'<span class="badge {bd}">{bd}</span></div>'
            f'<div class="meta">{len(nodes)} 元素({vis} 可见) · 参考 {int(W)}×{int(H)}{" · " + esc(note) if note else ""}</div>'
            f'<div class="stage" data-w="{W}" data-h="{H}"{scene_attr} data-nodes=\'{esc(js)}\'></div></div>')

cards = ""
for title, keys in SECTIONS:
    inner = "".join(screen_card(k) for k in keys if k in scr)
    if inner: cards += f'<h2 class="gallery">{esc(title)}</h2><div class="grid">{inner}</div>'

syms = "".join(
    f'<div class="symc"><div class="symbox">{esc(n.split(" ")[0])}</div><div class="symcap">{esc(n)}<br><span>{esc(c)}·«{esc(a)}»</span></div></div>'
    for n, c, a in M.get("symbols", []))
sym_html = f'<h2 class="gallery">符号集(extracted 资产)</h2><div class="symrow">{syms}</div>' if syms else ""
notes = "".join(f"<li>{n}</li>" for n in M.get("notes", []))
notes_html = (f'<details open><summary>注释 — 屏覆盖 / HUD vs game content / 来源 / 缺口</summary>'
              f'<div class="body"><ul>{notes}</ul></div></details>') if notes else ""

TPL = r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__CODE__「__TITLE__」UI 灰盒(逆向·Unity·__VER__)</title>
<!-- 数据驱动:每元素 x/y/w/h = UnityPy 沿 RectTransform 合成屏幕 px。绝不由截图推导。会话数值一律占位。 -->
<style>
:root{--bg:#0b1220;--card:#131c2a;--bd:#26364a;--fg:#cdd9e6;--mut:#7d8ea6;--acc:#4fc3d0}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:13px/1.5 -apple-system,"PingFang SC","Segoe UI",sans-serif}
header{padding:16px 22px;border-bottom:1px solid var(--bd);position:sticky;top:0;background:var(--bg);z-index:1000}
h1{margin:0 0 4px;font-size:19px}.sub{color:var(--mut);font-size:12px}
.controls{margin-top:8px;font-size:12px}.controls label{margin-right:14px;cursor:pointer}
main{padding:20px}h2.gallery{font-size:15px;margin:26px 0 8px;border-left:3px solid var(--acc);padding-left:10px}
.grid{display:flex;flex-wrap:wrap;gap:22px;align-items:flex-start}
.frame{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:10px}
.cap{font-size:12px;font-weight:600}.tag{font-size:9px;color:var(--mut);margin-left:6px}
.badge{font-size:9px;padding:1px 6px;border-radius:3px;margin-left:6px}
.badge.validated{background:#11324a;color:#5db6e8}.badge.extracted{background:#14361f;color:#67d98a}.badge.derived{background:#3a2a12;color:#e0a44a}
.meta{font-size:10.5px;color:var(--mut);margin:2px 0 8px;max-width:380px}
.stage{position:relative;background:#060b12;border:1px solid #1a2432;overflow:hidden}
.box{position:absolute;overflow:hidden}.box.vis{border:1px solid rgba(120,200,255,.5)}.box.struct{border:1px dashed rgba(160,140,90,.4)}.box.inact{opacity:.32}
.box .bl{font-size:8px;line-height:1.1;padding:1px 2px;color:#e7edf5;text-shadow:0 1px 2px #000;white-space:nowrap}
.box .bd{font-size:7px;line-height:1;padding:0 2px;color:#9fb0c4;white-space:nowrap}
.d0{background:rgba(40,90,120,.30)}.d1{background:rgba(50,110,90,.30)}.d2{background:rgba(120,90,50,.32)}.d3{background:rgba(100,70,120,.30)}.d4{background:rgba(120,60,70,.30)}.d5{background:rgba(60,80,110,.30)}
.symrow{display:flex;flex-wrap:wrap;gap:12px}.symc{width:118px}.symbox{height:74px;border:1px dashed #3a4658;border-radius:6px;display:flex;align-items:center;justify-content:center;color:#8fd0a0;font-size:11px}
.symcap{font-size:10px;margin-top:3px}.symcap span{color:var(--mut)}
details{margin:14px 0;border:1px solid var(--bd);border-radius:6px}summary{cursor:pointer;padding:10px 14px;font-weight:600}.body{padding:0 16px 14px;font-size:12px;color:#c2ccdb}code{background:#0a0e15;padding:1px 4px;border-radius:3px;color:#8fd0a0}
</style></head><body>
<header><h1>__CODE__「__TITLE__」— UI 灰盒（逆向·Unity·__VER__）</h1>
<div class="sub">每元素 x/y/w/h = UnityPy 沿 RectTransform 合成屏幕 px。源: <b>__SRC__</b>。<b>__NS__ 屏 / __NN__ 元素</b>。三件套:ADD/GDD/本 HTML</div>
<div class="controls"><label><input type="checkbox" id="cStruct" checked> 结构容器</label><label><input type="checkbox" id="cInact" checked> 非激活态</label><label><input type="checkbox" id="cDims" checked> 尺寸</label><label><input type="checkbox" id="cLbl" checked> 名称</label></div></header>
<main>__CARDS__
__SYMS__
__NOTES__</main>
<script>
const PAL=n=>'d'+Math.min(n,5);
function render(){const S=document.getElementById('cStruct').checked,I=document.getElementById('cInact').checked;
 document.querySelectorAll('.stage').forEach(st=>{st.innerHTML='';const W=+st.dataset.w,H=+st.dataset.h,CW=(W>=H?430:330),s=CW/W;
  const sc=st.dataset.scene?'offscreen:':'';
  st.style.width=CW+'px';st.style.height=(H*s)+'px';
  JSON.parse(st.dataset.nodes).forEach(n=>{if(!n.cr&&!S)return;if(!n.act&&!I)return;
   const d=document.createElement('div');d.className='box '+(n.cr?('vis '+PAL(n.depth)):'struct')+(n.act?'':' inact');
   d.style.left=(n.x*s)+'px';d.style.top=(n.y*s)+'px';d.style.width=(n.w*s)+'px';d.style.height=(n.h*s)+'px';d.style.zIndex=n.depth+(n.cr?10:0);
   d.setAttribute('data-box',n.x+','+n.y+','+n.w+','+n.h);
   d.setAttribute('data-role',sc+(n.role||n.path||n.name));
   d.title=n.path+'  ['+n.x+','+n.y+' '+n.w+'×'+n.h+']  cr='+n.cr+' act='+n.act;
   if(n.w*s>24&&n.h*s>8){const l=document.createElement('div');l.className='bl lbl';l.textContent=n.name;d.appendChild(l);
    if(n.h*s>18){const b=document.createElement('div');b.className='bd dim';b.textContent=n.x+','+n.y+' '+n.w+'×'+n.h;d.appendChild(b);}}
   st.appendChild(d);});});
 document.querySelectorAll('.dim').forEach(e=>e.style.display=document.getElementById('cDims').checked?'':'none');
 document.querySelectorAll('.lbl').forEach(e=>e.style.display=document.getElementById('cLbl').checked?'':'none');}
['cStruct','cInact','cDims','cLbl'].forEach(id=>document.getElementById(id).addEventListener('change',render));render();
</script></body></html>'''

nn = sum(len(v["nodes"]) for v in scr.values())
html_out = (TPL.replace("__CODE__", esc(code)).replace("__TITLE__", esc(M.get("title", "")))
            .replace("__VER__", esc(M.get("version", "?"))).replace("__SRC__", esc(M.get("source_note", "Unity 构建")))
            .replace("__CARDS__", cards).replace("__SYMS__", sym_html).replace("__NOTES__", notes_html)
            .replace("__NS__", str(len(seen_disp))).replace("__NN__", str(nn)))
open(out_p, "w").write(html_out)
print("wrote", out_p, "| screens:", len(seen_disp), "| nodes:", nn)
