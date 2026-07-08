---
name: reverse-game-to-upstream-pack
description: 逆向已上线游戏 → 产出 auto-art 上游文档包(<slug>-pack/:GDD.md+ADD.md+assets/+双 html),严格遵循 Archive/upstream-doc-pack-spec.md(v1.0 normative)。当用户要"按上游规范/doc pack/审签格式输出某游戏"、"重跑 XX-pack"时使用。数据采集复用两条既有逆向管线(ss/unity 或 cg/web,按游戏类型选);本 skill 定义产物 schema、证据→正向行文的转换纪律、参考图规范与 L1-L13 lint 门禁。与三件套(ADD/GDD/灰盒)是两种产物形态,互不替代。
---

# Reverse Game → Upstream Doc Pack(逆向游戏 → 上游文档包)

**规范即宪法**:产物逐字遵循 `Archive/upstream-doc-pack-spec.md`(下称 SPEC)。本 skill 是"如何用逆向管线把 SPEC 填实"的执行手册;SPEC 与本文冲突时 **SPEC 胜**。

**三份产物形态的关系**:三件套(训练素材,含灰盒/elements)⇢ 给复现 agent;**doc pack ⇢ 给美术审签 + auto-art 消费**。同一游戏两种产物共用同一份 `work/<code>/` 抽取物;已有三件套的游戏(如 ss03/cg03r)重跑 pack 时**数据直接复用 work 落盘物,勿重抽**(版本一致时)。

---

## ★ 0. 真值纪律与行文转换(本 skill 最重要的新增纪律)

数据层照旧执行两系列 skill 的 §0:**代码/构建是唯一真实信源;零截图部署形态照常出齐;绝不借旧产出骨架;未知绝不编造**。变化在**写出来的形态**:

### 0.1 证据等级 → SPEC 口径映射(写作时逐值执行)

| 内部证据等级(工作材料) | 写进 pack 的口径 |
|---|---|
| 构建/源码/服务端一手(原 extracted/一手 cite) | **直接以规格语气写定值**;备注列可写「实测 <值>」 |
| 推定/投影/运行时排布(原 derived) | 写结构 + 具体值挂 **TBC**(进 §6/§9 表,owner 按域) |
| 服务端权威未证(RTP/权重/价格) | 公式/机制写定,数值 **TBC(owner: 数学组)** |
| 借参考游戏/异主题素材 | §7 provenance=`foreign-theme` + 已知冲突列必填 |

### 0.2 行文禁用与替换(SPEC §5.4,lint 有 grep 门禁)

- **禁止字样**:逆向、还原、反推、抽取自、解包、评估、与旧稿差异、extracted、derived、validated、徽标、compose、UnityPy、灰盒。
- **允许字样**:实测、确证、依 <参考游戏> 同类实现、待定(TBC)。
- 口吻=**正向单次生成**:写"进度条填充采用 clip-path 推进",不写"逆向发现进度条是 clip-path"。
- 逆向对象在 GDD §1 以「参考游戏:<名>」合法登场;cite(file:line)**只留在 work/ 工作笔记**,不进 pack 正文。

### 0.3 TBC 纪律

- 未知值(数值/尺寸/hex/档位数)一律进 TBC 表,**owner 必填**,按域指派:数学组(赔付/RTP/触发/权重/价格)、美术(视觉终稿)、动效、音效、本地化、PM(范围/档期)、运营(币种)。
- 一手证据能定的**不许**挂 TBC(挂了=白丢信息,重跑的意义就在把上一版的 TBC 填实)。

---

## 1. 总流程(5 步)

```
步1 选型+采集(复用既有管线) → 步2 两轴判定+包骨架 → 步3 GDD 填实 → 步4 ADD 填实+assets 取图
  → 步5 双 html+lint 门禁+终检
```

### 步 1 — 数据采集(复用,勿重复造轮子)

- **选型判据**(同 CLAUDE.md):repo 依赖含 `react-unity-webgl` → 按 `skills/reverse-unity-game-to-triad` 阶段 0-3 采集(UnityPy 解包/源码工程直读);否则 web/JS → 按 `skills/reverse-game-to-triad` 阶段 0-2 采集。
- 产出照旧落 `work/<code>/`:导出资产、all_layout/结构树、string-tables、asset-manifest、服务端 cite 笔记。**同游戏已有本会话/往期完整 work 落盘且构建版本一致 → 直接复用,只补缺**。
- 版本锚照旧(线上 version.json 或 git HEAD),写进 GDD §1 与 changelog。

### 步 2 — 两轴判定 + 包骨架

- `interaction × board` 按**构建证据**判(SPEC §1.2 登记表):payline/ways/tumble 转轮 → `slot × reel`(玩法变体括号进 GDD §1 正文);逐站/车道 crash → `crash-step × lane-scene`;格子翻雷 → `crash-step × grid`(**不存在 mines 品类**)。新组合按 SPEC §4.3 先补登记表。
- 建 `output/<SLUG>-pack/`(SLUG 大写,如 SS03-pack):`GDD.md`/`ADD.md`/`assets/`;frontmatter 仅 SPEC §1.3 白名单字段,`owner` 未知填 `<role> (TBC)`。
- `ASSET-CHECKLIST.md` **不建**(消费方回填物)。

### 步 3 — GDD §1-§6 填实(来源映射)

| 章 | 数据来源(work 抽取物) | 要点 |
|---|---|---|
| §1 定位 | 版本锚/宿主+构建朝向证据/locale 表/币种(服务端或宿主) | 两轴显式声明;**参考游戏=逆向对象名**;非目标写实(如"不含 jackpot") |
| §2 状态机 | spin 流程 C#/协议/回合时序 | 状态表(snake_case 标识符)+ ASCII 图;态名与 ADD §2 屏名可对齐 |
| §3 玩法参数 | 网格/线数/触发阈值/档位/倍率梯(一手) | 参数表(参数/标识符/规格/默认值);未证默认值填 TBC |
| §4 数学框架 | 服务端 repo 一手 > Guide 贴图/string-tables > 构建暗示 | 公式写定+示例值;RTP/权重/价格 TBC;**禁编造** |
| §5 系统边界 | 弹窗文案表/断线/闲置/余额不足/维护 | 只收**产 UI 素材**的边界(是否产素材列必填) |
| §6 TBC | 汇总 §1-5 未定项 | owner 必填 |

文末可选 Changelog 段(与 ADD §9 同格式)。

### 步 4 — ADD §1-§9 填实(核心;来源映射)

| 章 | 数据来源 | 要点 |
|---|---|---|
| §1 风格锚点 | 视觉门结论(Style Bible) | 关键词/色板(hex 从导出主视觉取色,取不准挂 TBC)/**气氛图≥1**(主视觉入 assets) |
| §2 屏幕区块 | 屏清单+结构树 | 屏=玩家视口态(loading/main/win_present/…/exception);区块给相对位置,精确 px 进 §3 需求描述 |
| §3 组件清单 | 承重件+资产族(elements/manifest) | **列逐字固定**;ID 连续;组件双名(中文+snake_case);**状态变体必填**(按钮三态有资产证据才写三态);参考图列 ↔ §7 双向 |
| §3a.. 品类模块段 | 见下「模块段填法」 | 段头 `<!-- module: board|interaction=… -->` + `### §3x 名称`,插 §3 后 §4 前 |
| §4 动效 ART-M | AnimationClip/Timeline/序列帧族/宿主 CSS 动画 | 需求级(时长/触发列);**禁逐帧规格**;一手时长可写「实测 Ns」 |
| §5 音效 ART-S | 音频全清单(名/时长/分包) | 需求级(禁逐轨);有全清单时**按触发域分组成行**(BGM/交互/结算/演出…),别学单行全 TBC |
| §6 文案/本地化 | string-tables + 文字图族 | 键表进正文(样例语言 en+zh-hant 起,余语言注"与键一一对应");**baked/overlay 政策每行必填**(文字图=baked;运行时文本=overlay) |
| §7 参考图清单 | assets/ 选图(见 §4 取图规范) | 列逐字固定;provenance 四值;`foreign-theme` 冲突列必填;**与 assets/ 双向一致**(placeholder 行=待补槽,不参与比对,文件列写 `xxx_{var}.png(待补)` 模式名) |
| §8 共用壳引用 | 客户端形态 | 仅 `../_common/<module>.md` 形式;unity 壳窄引用(locale/exceptions/session/params),cg 全框架可另引 history/currency/…;**本作差异列写实** |
| §9 TBC+签字+changelog | 汇总 | 签字表**留空**;changelog `v1.0.0 初版:<一句话范围>` |

**模块段填法**(轴值→内容→数据源):

| 轴值 | 段内容 | 我方数据源 |
|---|---|---|
| `board: reel` | §3a 符号表(符号/标识符/语义/Wild­-Scatter/视觉)+ §3b 赔付表屏视觉 | SymbolConfig·资产族·服务端 symbol 表·Guide 赔付贴图 |
| `interaction: slot` | win-tier 演出矩阵(档×命名×语言键)、Free Spin 层(流程屏×命名)、locale×换图矩阵 | win 标题文字图族·noticer 族·localization bundle 结构 |
| `board: grid` | 格子状态矩阵(tile 状态/标识符/视觉) | tile 资产族+状态机 |
| `board: lane-scene` | 场景分段表/难度变体表 | 场景 seg 资产+难度配置 |
| `interaction: crash-step` | 步进/倍率条展示、cashout 按钮逐态 | 倍率条资产+按钮三态资产 |

### 步 5 — 双 html + lint + 终检

```
python3 skills/reverse-game-to-upstream-pack/scripts/build_pack_html.py output/<SLUG>-pack/   # md→html(图内嵌)
python3 skills/reverse-game-to-upstream-pack/scripts/pack-lint.py     output/<SLUG>-pack/   # L1-L13+行文门禁
```
通过标准:**lint 0 fail**(L11 气氛图缺失为 warn);终检清单见 §6。

---

## 4. assets/ 取图规范(取图是生成方职责,禁止要求人工截图)

- **来源=管线导出物**(extract/art、宿主 repo 静态图、work 蒙太奇);逆向对象自身的图 → `normative`;借其它游戏/异主题 → `foreign-theme`(冲突列必填);示意草图 → `illustrative`;拿不到 → `placeholder` 模式名行(caption 注 `pending: <原因>`)。
- **参考图是锚点不是素材库**:优先覆盖 §1 气氛图 + P0 组件 + 各品类模块段主证图;单组件≤3 张,整包一般 8~30 张。全量素材枚举是 auto-art 下游(ASSET-CHECKLIST)的事,pack 不做。
- 文件名:沿用资产原名(可读)或 `<语义>_<变体>.png`;动图可用 GIF;入包前肉眼过一遍(视觉门产物直接可用)。
- 尺寸如实写进 §7 caption 或 §3 备注(「实测 WxH」),**禁止编尺寸**。

## 5. 品类两轴速查(已登记组合 + 已做游戏映射)

| interaction×board | 模块段 | 已做参照(work 可复用) |
|---|---|---|
| slot × reel | §3a 符号表 / §3b 赔付屏 / §3c win-tier / §3d FreeSpin / §3e locale×换图 | ss03(麻将,tumble)、ss02(pay-anywhere)、ss01b(payline,源码工程) |
| crash-step × lane-scene | §3a 场景分段/难度 / §3b 步进倍率条+cashout 态 | cg03a/cg03r |
| crash-step × grid | §3a 格子状态矩阵 / §3b 步进倍率条+cashout 态 | cg05(MineBeach 类) |

## 6. 终检清单(lint 之外的人工项)

- [ ] frontmatter 白名单内、两轴与 GDD §1 逐字一致(L13 也查,先自检)。
- [ ] **一手证据未挂 TBC**(逐 TBC 行问:work 里真没有吗?)——重跑存量 pack 时,把上一版 placeholder/TBC 能填实的全部填实,并记 changelog delta。
- [ ] 行文禁用词 grep 零命中(`逆向|还原|反推|解包|extracted|derived|灰盒|compose`)。
- [ ] ART-C/M/S 编号连续;组件双名;状态变体逐行显式。
- [ ] §7 ↔ assets/ 双向一致(placeholder 行除外);foreign-theme 冲突列非空。
- [ ] §6 每行 baked/overlay 有值;§9 签字表空;changelog 至少 v1.0.0 一行。
- [ ] 正文零裸链接(唯 `../_common/` 相对路径豁免)。
- [ ] 与三件套互检(若同游戏已有):数值/结构不得互相矛盾;发现旧错在 work 笔记记录,pack 只写对的。
- [ ] 到可提交节点停下告知用户,不自行 commit。

## 7. 脚本表(本 skill scripts/,通用件;数据采集脚本用各系列 skill 自带的)

| 脚本 | 用途 | 跑法 |
|---|---|---|
| `build_pack_html.py` | GDD/ADD md→html(标题/表格/图 base64 内嵌),集中唯一实现 | `python3 …/build_pack_html.py <pack目录>` |
| `pack-lint.py` | SPEC §6 L1-L13 + 行文禁用词 + ID 连续 + §7↔assets 对称差 | `python3 …/pack-lint.py <pack目录>`(exit 0=过;L11 warn) |

## 8. 坑(首批,来自样例鉴别与规范推演)

1. **逆向字样泄漏**:正文/备注写出"逆向/解包/derived"→ lint 直接 fail;备注用「实测」。
2. **一手数据挂 TBC**(样例通病):上一版拿不到 Unity 层就全 TBC;重跑必须用抽取物填实,否则重跑无意义。
3. **编造 hex/尺寸**:色板取不准就 TBC,尺寸一律实测;禁照抄 SPEC 示例值。
4. **§7 与 assets 目录漂移**:加图忘登记/登记忘拷贝;placeholder 行文件列必须是模式名+(待补),不能指向实文件。
5. **状态变体空置**:每行显式 idle 或多态;复合态用 `part: 态/态; part: 态/态` 语法。
6. **模块段忘自声明注释**或轴值与 GDD §1 不一致(L2)。
7. **裸链接**(含 Figma/Sheet)混入 → 内容表格化进正文或进 TBC。
8. **frontmatter 私加字段**(如 version/date)→ 只许白名单;版本进 changelog。
9. **音效单行全 TBC**:有全清单证据时按触发域分组;真没有才整表 TBC。
10. **品类误判**:格子翻雷写成"mines 品类"——SPEC 明文不存在,必须 `crash-step × grid`。
11. **签字表代填**:生成方永远留空。
12. **把 pack 当三件套写**:不出灰盒/elements/徽标;坐标只在需求描述里以"实测"出现,不做逐 box 清单。

## 9. 输出位置 & 命名

`output/<SLUG>-pack/`(SLUG 大写,如 `SS03-pack`);工作材料照旧 `work/<code>*/`(gitignored)。重跑存量 pack:旧包先整体移入 `output/<SLUG>-pack/_archive/`(只移不删)或按用户指示处理,changelog 以 `v1.1.0 重跑:<范围>` 续接旧版历史。
