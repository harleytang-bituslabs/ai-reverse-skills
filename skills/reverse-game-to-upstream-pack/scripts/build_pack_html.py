#!/usr/bin/env python3
"""upstream doc pack 集中 html 构建器(SPEC §1:md 为真相源,html 为浏览视图,图内嵌)。
用法: python3 build_pack_html.py <pack目录>   → 就地生成 GDD.html / ADD.html
- 支持:frontmatter(渲染为登记块)、#~### 标题、管道表格、列表、引用、hr、粗体/行内码、
  ![](assets/x) 内嵌(base64);文档内未内嵌引用过的 assets/ 图片自动附「参考图预览」画廊。
- 纯标准库,无外部依赖;禁止各包自带副本(SPEC §1 形态规则)。"""
import base64, html, mimetypes, re, sys
from pathlib import Path

CSS = """body{font:15px/1.65 -apple-system,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
max-width:1080px;margin:24px auto;padding:0 20px;color:#1c2733}
h1{font-size:26px;border-bottom:2px solid #d8dee6;padding-bottom:8px}
h2{font-size:20px;margin-top:34px;border-left:4px solid #4a7dbd;padding-left:10px}
h3{font-size:16px;margin-top:24px}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:13.5px}
th,td{border:1px solid #c9d2dc;padding:6px 9px;text-align:left;vertical-align:top}
th{background:#eef2f7}tr:nth-child(even) td{background:#f7f9fb}
blockquote{margin:10px 0;padding:8px 14px;background:#f4f6ee;border-left:4px solid #a8b87a;color:#4c5a2f}
code{background:#eef1f4;padding:1px 5px;border-radius:3px;font-size:.92em}
img{max-width:100%;height:auto}
.meta{background:#f0f4f8;border:1px solid #d5dee8;border-radius:6px;padding:8px 14px;
font-size:13px;color:#42566b;margin-bottom:18px}
.gallery{display:flex;flex-wrap:wrap;gap:14px}.gallery figure{margin:0;width:230px}
.gallery img{border:1px solid #ccd;max-height:200px;object-fit:contain;background:#fafafa;width:100%}
.gallery figcaption{font-size:12px;color:#555;word-break:break-all}
hr{border:none;border-top:1px solid #d8dee6;margin:22px 0}"""

def b64(p: Path) -> str:
    mime = mimetypes.guess_type(p.name)[0] or 'image/png'
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"

def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    return s

def convert(md: str, pack: Path):
    lines = md.split('\n')
    out, i, fm, embedded = [], 0, {}, set()
    if lines and lines[0].strip() == '---':                      # frontmatter → 登记块
        j = 1
        while j < len(lines) and lines[j].strip() != '---':
            if ':' in lines[j]:
                k, v = lines[j].split(':', 1); fm[k.strip()] = v.strip()
            j += 1
        i = j + 1
        out.append('<div class="meta">' + ' · '.join(f'<b>{html.escape(k)}</b>: {html.escape(v)}'
                   for k, v in fm.items()) + '</div>')
    def img_sub(m):
        rel = m.group(2); p = pack / rel
        if p.exists():
            embedded.add(p.name)
            return f'<img src="{b64(p)}" alt="{html.escape(m.group(1))}">'
        return html.escape(m.group(0))
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|?\s*$', lines[i+1]):
            hdr = [c.strip() for c in ln.strip().strip('|').split('|')]
            out.append('<table><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in hdr) + '</tr>')
            i += 2
            while i < len(lines) and lines[i].startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                out.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in cells) + '</tr>')
                i += 1
            out.append('</table>'); continue
        ln2 = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', img_sub, ln)
        m = re.match(r'^(#{1,4}) (.*)', ln2)
        if m: out.append(f'<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>')
        elif ln2.strip() == '---': out.append('<hr>')
        elif ln2.startswith('> '): out.append(f'<blockquote>{inline(ln2[2:])}</blockquote>')
        elif re.match(r'^\s*[-*] ', ln2): out.append(f'<li>{inline(re.sub(r"^\s*[-*] ", "", ln2))}</li>')
        elif ln2.strip().startswith('<!--'): out.append(ln2)     # 模块段自声明注释原样保留
        elif ln2.strip(): out.append(f'<p>{inline(ln2)}</p>')
        i += 1
    return '\n'.join(out), embedded

def build(pack: Path):
    for doc in ('GDD', 'ADD'):
        src = pack / f'{doc}.md'
        if not src.exists(): continue
        body, embedded = convert(src.read_text(encoding='utf-8'), pack)
        assets = sorted((pack / 'assets').glob('*')) if (pack / 'assets').exists() else []
        rest = [p for p in assets if p.name not in embedded and not p.name.startswith('.')]
        if doc == 'ADD' and rest:                                 # 未内嵌的参考图附画廊
            body += '\n<hr><h2>参考图预览(assets/ 内嵌)</h2>\n<div class="gallery">'
            body += ''.join(f'<figure><img src="{b64(p)}"><figcaption>{html.escape(p.name)}</figcaption></figure>'
                            for p in rest)
            body += '</div>'
        (pack / f'{doc}.html').write_text(
            f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>{pack.name} {doc}</title>'
            f'<style>{CSS}</style></head><body>\n{body}\n</body></html>', encoding='utf-8')
        print(f'wrote {pack / (doc + ".html")}')

if __name__ == '__main__':
    build(Path(sys.argv[1]))
