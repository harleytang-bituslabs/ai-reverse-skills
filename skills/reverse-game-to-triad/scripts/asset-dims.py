#!/usr/bin/env python3
# 扫描资产真实尺寸 (PNG/JPG/WEBP, 无依赖)。ADD 尺寸 + HTML 原生尺寸的依据。
# 跑: python3 asset-dims.py <game>/public/assets
import os, struct
from pathlib import Path
def png(p):
    h=open(p,'rb').read(24)
    return struct.unpack('>II',h[16:24]) if h[:8]==b'\x89PNG\r\n\x1a\n' else None
def jpg(p):
    f=open(p,'rb');f.read(2);b=f.read(1)
    while b:
        while b and b!=b'\xff':b=f.read(1)
        m=f.read(1)
        while m==b'\xff':m=f.read(1)
        if m in b'\xc0\xc1\xc2\xc3\xc5\xc6\xc7\xc9\xca\xcb\xcd\xce\xcf':
            f.read(3);H,W=struct.unpack('>HH',f.read(4));return W,H
        f.read(struct.unpack('>H',f.read(2))[0]-2);b=f.read(1)
def webp(p):
    d=open(p,'rb').read(30)
    if d[:4]!=b'RIFF':return None
    fmt=d[12:16]
    if fmt==b'VP8 ':return struct.unpack('<H',d[26:28])[0]&0x3fff, struct.unpack('<H',d[28:30])[0]&0x3fff
    if fmt==b'VP8L':n=struct.unpack('<I',d[21:25])[0];return (n&0x3fff)+1,((n>>14)&0x3fff)+1
    if fmt==b'VP8X':return (struct.unpack('<I',d[24:27]+b'\0')[0]&0xffffff)+1,(struct.unpack('<I',d[27:30]+b'\0')[0]&0xffffff)+1
import sys
root=sys.argv[1] if len(sys.argv)>1 else '.'
for p in sorted(Path(root).rglob('*')):
    e=p.suffix.lower()
    if e in('.png','.jpg','.jpeg','.webp'):
        try:d=png(p) if e=='.png' else (webp(p) if e=='.webp' else jpg(p))
        except:d=None
        print(f"{(str(d[0])+'x'+str(d[1])) if d else '?':>12}  {os.path.getsize(p)//1024:>5}KB  {p}")
