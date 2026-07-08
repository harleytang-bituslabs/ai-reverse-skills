#!/usr/bin/env python3
"""upstream doc pack lint(SPEC §6 L1-L13 可执行化 + 本 skill 行文门禁)。
用法: python3 pack-lint.py <pack目录>    exit 0=通过(warn 不阻断)。"""
import re, sys
from pathlib import Path

FAILS, WARNS = [], []
def fail(tag, msg): FAILS.append(f'[{tag}] {msg}')
def warn(tag, msg): WARNS.append(f'[{tag}] {msg}')

pack = Path(sys.argv[1])
gdd_p, add_p = pack / 'GDD.md', pack / 'ADD.md'
if not gdd_p.exists() or not add_p.exists():
    fail('L1', 'GDD.md / ADD.md 缺失'); print('\n'.join(FAILS)); sys.exit(1)
gdd, add = gdd_p.read_text(encoding='utf-8'), add_p.read_text(encoding='utf-8')

def frontmatter(txt, name):
    m = re.match(r'^---\n(.*?)\n---', txt, re.S)
    if not m: fail('L13', f'{name} 缺 frontmatter'); return {}
    d = {}
    for ln in m.group(1).splitlines():
        if ':' in ln: k, v = ln.split(':', 1); d[k.strip()] = v.strip()
    return d

WHITELIST = {'project', 'doc', 'interaction', 'board', 'status', 'owner', 'source_version'}
fm_g, fm_a = frontmatter(gdd, 'GDD'), frontmatter(add, 'ADD')
for name, fm in (('GDD', fm_g), ('ADD', fm_a)):
    extra = set(fm) - WHITELIST
    if extra: fail('L13', f'{name} frontmatter 白名单外字段: {extra}')
for ax in ('interaction', 'board'):
    if fm_g.get(ax) != fm_a.get(ax):
        fail('L13', f'两文档 {ax} 不一致: GDD={fm_g.get(ax)} ADD={fm_a.get(ax)}')
    if fm_g.get(ax) and fm_g[ax] not in gdd:
        fail('L13', f'GDD §1 正文未见 {ax} 声明值 {fm_g[ax]}')

# L1 章节存在性
for n in range(1, 7):
    if not re.search(rf'^## §{n}\b', gdd, re.M): fail('L1', f'GDD 缺 §{n}')
for n in range(1, 10):
    if not re.search(rf'^## §{n}\b', add, re.M): fail('L1', f'ADD 缺 §{n}')

# L2 模块段轴值
axes = {fm_g.get('interaction'), fm_g.get('board')}
for m in re.finditer(r'<!--\s*module:\s*(board|interaction)=([\w-]+)\s*-->', add):
    if m.group(2) not in axes:
        fail('L2', f'模块段轴值 {m.group(1)}={m.group(2)} 与 GDD 两轴 {axes} 不符')
if not re.search(r'<!--\s*module:', add): fail('L2', 'ADD 无任何品类模块段自声明注释')

# 表提取工具:返回 §n 段内所有表(每表=列表[行cells])
def section(txt, hdr_pat):
    m = re.search(hdr_pat, txt, re.M)
    if not m: return ''
    nxt = re.search(r'^## ', txt[m.end():], re.M)
    return txt[m.end(): m.end() + nxt.start() if nxt else len(txt)]

def tables(seg):
    tbls, cur = [], []
    for ln in seg.splitlines():
        if ln.startswith('|'):
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if re.match(r'^[\s:|-]+$', ''.join(cells)): continue
            cur.append(cells)
        elif cur: tbls.append(cur); cur = []
    if cur: tbls.append(cur)
    return tbls

# L3 固定表头
C3 = ['ID', '屏幕/区块', '组件', '需求描述', '状态变体', '优先级', '参考图', '备注']
C7 = ['文件', '关联章节/组件ID', 'provenance', 'caption', '已知冲突']
s3, s7 = section(add, r'^## §3\b'), section(add, r'^## §7\b')
t3 = [t for t in tables(s3) if t and t[0][:1] == ['ID']]
if not t3 or t3[0][0] != C3: fail('L3', f'ADD §3 表头不符: {t3[0][0] if t3 else "无表"}')
t7 = tables(s7)
if not t7 or t7[0][0] != C7: fail('L3', f'ADD §7 表头不符: {t7[0][0] if t7 else "无表"}')

# L4 ID 连续唯一(全文抽取)
for prefix in ('ART-C-', 'ART-M-', 'ART-S-'):
    ids = [int(m) for m in re.findall(rf'{prefix}(\d+)', add)]
    uniq = sorted(set(ids))
    if not uniq: warn('L4', f'{prefix} 无条目'); continue
    if uniq != list(range(1, uniq[-1] + 1)):
        fail('L4', f'{prefix} 编号不连续: {uniq}')

# L6/L7/L8 §7 各行
listed, ph = set(), 0
if t7:
    for row in t7[0][1:]:
        if len(row) < 5: fail('L3', f'§7 行列数不足: {row}'); continue
        f, prov, conflict = row[0], row[2], row[4]
        if prov not in ('normative', 'illustrative', 'foreign-theme', 'placeholder'):
            fail('L7', f'provenance 非法: {prov} ({f})')
        if prov == 'foreign-theme' and not conflict:
            fail('L8', f'foreign-theme 行冲突列空置: {f}')
        if prov == 'placeholder' or '待补' in f: ph += 1; continue
        for part in re.split(r'\s*/\s*', re.sub(r'`', '', f)):
            if part: listed.add(part.strip())
assets_dir = pack / 'assets'
actual = {p.name for p in assets_dir.glob('*') if p.is_file() and not p.name.startswith('.')} if assets_dir.exists() else set()
if listed - actual: fail('L6', f'§7 登记但 assets/ 缺文件: {sorted(listed - actual)}')
if actual - listed: fail('L6', f'assets/ 有文件未登记 §7: {sorted(actual - listed)}')

# L9 TBC owner
for name, txt, pat in (('GDD §6', gdd, r'^## §6\b'), ('ADD §9', add, r'^## §9\b')):
    seg = section(txt, pat)
    for t in tables(seg):
        if t[0][:2] == ['item', 'owner']:
            for row in t[1:]:
                if len(row) < 2 or not row[1]: fail('L9', f'{name} TBC 行缺 owner: {row[:1]}')

# L10 裸链接
for name, txt in (('GDD', gdd), ('ADD', add)):
    for m in re.finditer(r'https?://\S+', txt):
        fail('L10', f'{name} 裸链接: {m.group(0)[:60]}')

# L11 气氛图(warn)
s1 = section(add, r'^## §1\b')
if not re.search(r'气氛图', s1) or re.search(r'气氛图[::]\s*(无|TBC)', s1):
    warn('L11', 'ADD §1 气氛图槽疑似为 0(警告级)')

# L12 baked/overlay
s6 = section(add, r'^## §6\b')
if 'baked/overlay' not in s6: fail('L12', 'ADD §6 缺 baked/overlay 政策列')
else:
    for t in tables(s6):
        if t[0][-1] == 'baked/overlay':
            for row in t[1:]:
                if row[-1] not in ('baked', 'overlay', 'TBC'):
                    fail('L12', f'§6 行 baked/overlay 取值非法: {row[0]}={row[-1]!r}')

# 行文禁用词(本 skill 纪律,SPEC §5.4)
BAN = r'逆向|还原|反推|解包|与旧稿|extracted|derived|validated|徽标|灰盒|compose|UnityPy'
for name, txt in (('GDD', gdd), ('ADD', add)):
    for m in re.finditer(BAN, txt):
        fail('WORD', f'{name} 行文禁用词「{m.group(0)}」@ 偏移 {m.start()}')

# 签字表留空(按表头精确定位)
s9 = section(add, r'^## §9\b')
for t in tables(s9):
    if t[0] == ['角色', '姓名', '日期', '冻结范围']:
        for r in t[1:]:
            if len(r) >= 3 and (r[1] or r[2]): fail('SIGN', f'签字表被代填: {r}')

print(f'== pack-lint {pack.name}: {len(FAILS)} fail / {len(WARNS)} warn (placeholder 行 {ph})')
for x in FAILS: print('FAIL', x)
for x in WARNS: print('warn', x)
sys.exit(1 if FAILS else 0)
