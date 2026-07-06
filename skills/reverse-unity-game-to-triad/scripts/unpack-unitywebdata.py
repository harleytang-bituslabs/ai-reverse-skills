#!/usr/bin/env python3
# 拆 Unity WebGL 的 <code>.data ("UnityWebData1.0" 容器) 为内文件。
# 用: python3 unpack-unitywebdata.py <code>.data [outdir]
# 关键产物: data.unity3d (主资产档,喂给 unitypy-extract.py)
import struct, os, sys
path = sys.argv[1]
outdir = sys.argv[2] if len(sys.argv) > 2 else "unpacked"
raw = open(path, "rb").read()
f = open(path, "rb")
hdr = b""; b = f.read(1)
while b not in (b"\0", b""): hdr += b; b = f.read(1)
assert hdr.startswith(b"UnityWebData"), f"非 UnityWebData 容器(magic={hdr!r})——可能不是 WebGL .data"
data_offset = struct.unpack("<I", f.read(4))[0]
files = []
while f.tell() < data_offset:
    off = struct.unpack("<I", f.read(4))[0]
    sz  = struct.unpack("<I", f.read(4))[0]
    nl  = struct.unpack("<I", f.read(4))[0]
    name = f.read(nl).decode(errors="replace")
    files.append((name, off, sz))
os.makedirs(outdir, exist_ok=True)
for name, off, sz in files:
    p = os.path.join(outdir, name.replace("/", "_"))
    open(p, "wb").write(raw[off:off + sz])
    print(f"  {sz:>10}  {name}")
print(f"=> {len(files)} 个内文件 -> {outdir}/")
print("   主资产档 = data.unity3d；sharedassets*.resource = 贴图/音频原始数据(同目录即可)；")
print("   global-metadata.dat = IL2CPP 元数据(还原 MonoBehaviour 字段名时用)。")
