#!/usr/bin/env python3
# 全量资产清单生成器:走一遍 UnityPy 抽取产物目录(可多个根,如 extract/ xb/),
# 给【每一个】资产文件出一行(PNG 解 IHDR 得真实宽高;音频尽量取时长;其余记大小),
# 按目录分组出 markdown 表 + JSON。
#
# 这是 "ADD 必须包含所有资产素材" 的机械保障(SKILL §3):ADD 附录直接嵌本脚本产出,
# 校验清单用 JSON 计数 对账 导出全集 vs ADD 清单行数。
#
# 用法: python3 asset-manifest.py <根目录...> [--out asset-manifest]
#   ->  asset-manifest.md + asset-manifest.json
import sys, os, json, struct, shutil, subprocess

argv = sys.argv[1:]
roots = []; out_base = "asset-manifest"
i = 0
while i < len(argv):
    if argv[i] == "--out": out_base = argv[i+1]; i += 2
    else: roots.append(argv[i]); i += 1
if not roots:
    print("用法: asset-manifest.py <根目录...> [--out asset-manifest]"); sys.exit(1)

AUDIO_EXT = {".m4a", ".wav", ".ogg", ".mp3", ".aif", ".aiff"}
FFPROBE = shutil.which("ffprobe")

def png_dims(fp):
    try:
        with open(fp, "rb") as f:
            head = f.read(26)
        if head[:8] != b"\x89PNG\r\n\x1a\n": return None
        w, h = struct.unpack(">II", head[16:24])
        return w, h
    except Exception:
        return None

def audio_dur(fp):
    if not FFPROBE: return None
    try:
        r = subprocess.run([FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
                            "-of", "csv=p=0", fp], capture_output=True, text=True, timeout=15)
        return round(float(r.stdout.strip()), 2)
    except Exception:
        return None

groups = {}   # group(相对目录) -> [row]
for root in roots:
    root = root.rstrip("/")
    parent = os.path.dirname(root) or "."
    for dirpath, _, files in os.walk(root):
        for fn in sorted(files):
            fp = os.path.join(dirpath, fn)
            grp = os.path.relpath(dirpath, parent)
            ext = os.path.splitext(fn)[1].lower()
            size = os.path.getsize(fp)
            row = {"file": fn, "bytes": size}
            if ext == ".png":
                d = png_dims(fp)
                if d: row["dims"] = f"{d[0]}x{d[1]}"
                row["type"] = "texture/sprite"
            elif ext in AUDIO_EXT:
                dur = audio_dur(fp)
                if dur: row["dur_s"] = dur
                row["type"] = "audio"
            elif ext in (".atlas", ".skel"):
                row["type"] = "spine"
            elif ext in (".json", ".txt", ".csv", ".bytes"):
                row["type"] = "textasset"
            else:
                row["type"] = ext.lstrip(".") or "file"
            groups.setdefault(grp, []).append(row)

def fmt_size(b):
    return f"{b/1024:.1f}KB" if b < 1024*1024 else f"{b/1024/1024:.2f}MB"

lines = ["# 全量资产清单(机器生成 · asset-manifest.py)", ""]
tot = {"png": 0, "audio": 0, "other": 0}
lines.append("## 分组统计")
lines.append("")
lines.append("| 组(来源目录) | 图 | 音频 | 其它 | 合计 |")
lines.append("|---|--:|--:|--:|--:|")
for grp in sorted(groups):
    rows = groups[grp]
    np = sum(1 for r in rows if r["type"] == "texture/sprite")
    na = sum(1 for r in rows if r["type"] == "audio")
    no = len(rows) - np - na
    tot["png"] += np; tot["audio"] += na; tot["other"] += no
    lines.append(f"| `{grp}` | {np} | {na} | {no} | {len(rows)} |")
lines.append(f"| **合计** | **{tot['png']}** | **{tot['audio']}** | **{tot['other']}** | **{tot['png']+tot['audio']+tot['other']}** |")
lines.append("")

for grp in sorted(groups):
    rows = groups[grp]
    lines.append(f"## {grp} ({len(rows)})")
    lines.append("")
    lines.append("| 文件 | 类型 | 尺寸/时长 | 大小 |")
    lines.append("|---|---|---|--:|")
    for r in rows:
        dim = r.get("dims") or (f"{r['dur_s']}s" if "dur_s" in r else "")
        lines.append(f"| `{r['file']}` | {r['type']} | {dim} | {fmt_size(r['bytes'])} |")
    lines.append("")

open(out_base + ".md", "w").write("\n".join(lines))
json.dump({"groups": groups, "totals": tot}, open(out_base + ".json", "w"), ensure_ascii=False, indent=0)
print(f"{out_base}.md / .json  ←  {tot['png']} 图 + {tot['audio']} 音频 + {tot['other']} 其它 = "
      f"{tot['png']+tot['audio']+tot['other']} 文件, {len(groups)} 组"
      + ("" if FFPROBE else "  (无 ffprobe,音频未取时长)"))
