# Auto-Art 上游文档包规范（GDD / ADD 正式 Schema）

- 版本：v1.0
- 日期：2026-07-02
- 状态：normative（正式规范，可据此生成与审签）
- 适用：auto-art 上游输入文档包（`<slug>-pack/`）
- 取代：`docs/upstream-art-input-contract.md`（AIP v0.1 提案，已归档）

---

## 0. 规范地位与三方职责

本文件是一份**契约**。它同时约束三方，任何一方都以本规范为唯一裁判：

| 角色 | 身份 | 对本规范的动作 | 负责产出/签署 |
|---|---|---|---|
| 外部生成 agent | 生产方（copyCat 探索参考游戏，或"参考游戏换皮 + 玩法改动"式概念输入） | **按本规范生成**整个文档包 | `GDD.md`、`ADD.md`（§1-§9 全部内容，其中 §9 签字表留空）、`assets/` 参考图、`GDD.html`/`ADD.html` |
| 美术团队 | 审签方 | **按本规范审签冻结** | 在 `ADD.md §9` 签字表签字；对 `ADD.md §3` 组件清单逐行审核；二审时对 `ASSET-CHECKLIST.md` 逐行开 ticket 并勾选验收 |
| auto-art | 消费方 | **按本规范解析** | 从 `ADD.md §3` + 品类模块段 + §7 图清单机械提取输入；生成后回填 `ASSET-CHECKLIST.md` |

职责边界（不得越界）：

- 生产方产出 ADD §1-§9 全部内容（含 §9 的 TBC 表与 changelog 段），但 §9 签字表**必须**留空，**不得**代签字。
- 审签方**只审签不改结构**：可改需求描述、驳回、要求补图，但章节结构与列定义按本规范固定。
- 消费方**只读不改上游**：ADD/GDD 冻结后为只读；auto-art 的产出仅写入 `ASSET-CHECKLIST.md`。
- 文本永远 normative（见 §3 图槽规则）；auto-art 与美术遇文图冲突时以文本 + changelog 为准。

本规范面向"要生成包的外部 agent"，全文用指令式表述（**必须 / 禁止 / 允许 TBC**）。文中所有示例值一律以 `<placeholder>` 形态给出，禁止照抄任何真实游戏的取值。

---

## 1. 包结构

生成方必须产出如下目录，文件名逐字固定：

```
<slug>-pack/
├── GDD.md            # 游戏设计：auto-art 上下文，美术只读参考，不设签字
├── ADD.md            # 美术设计：美术审签对象 + auto-art 视觉输入 ← 核心
├── assets/           # 参考图（生成方产出，取图是生成方职责，禁止要求人工截图）
├── GDD.html          # GDD.md 的浏览视图（内嵌图），md 为真相源
├── ADD.html          # ADD.md 的浏览视图（内嵌图），md 为真相源
└── ASSET-CHECKLIST.md  # auto-art 消费后回填的素材级验收单（生成方初始留空或不建）
```

形态规则：

- 形态**必须**是约定式 Markdown——固定章节 + 规范表格列，人机同源。**禁止**把正文信息外移到独立 yaml/json 文件；文头 frontmatter 仅限 §1.3 登记字段。
- **必须**同时产出 `.md` 与 `.html` 双份。`.md` 是真相源，`.html` 仅为美术浏览视图（图片内嵌）。html 由集中脚本 `prds/_tools/build_pack_html.py` 生成，各包**禁止**各带构建脚本副本。

### 1.1 自包含硬规则

- 包**必须**零外部依赖。
- 正文**禁止**出现任何裸链接（禁止 Google Sheet、Axure、Figma、以及任意 `http`/`https` 链接）。
- 需要的内容要么以表格进正文（如 bet options、倍率示例、多语言键表），要么显式进 §6/§9 的 TBC 表。
- **唯一允许**的外部引用是共用壳：`prds/_common/<module>.md` 形式的稳定相对路径 + 模块名（可解析、可寻址）。当前已注册模块（真实可引用路径，非游戏值，直接按此引用，不写占位符）：`params` / `currency` / `locale` / `session` / `history` / `exceptions` / `backoffice` / `telemetry`。

### 1.2 品类两轴

每个包由两轴共同定型，**必须**在 GDD §1 显式声明：

- `interaction`（交互模式）：如 `crash-step`、`slot`、…
- `board`（盘面类型）：如 `grid`、`lane-scene`、`reel`、…

轴值组合决定 ADD 的品类模块段（见 §4 品类模块登记表）。已登记组合：

| 代号形态 | interaction | board |
|---|---|---|
| `<crash-grid slug>` | `crash-step` | `grid` |
| `<crash-lane slug>` | `crash-step` | `lane-scene` |
| `<slot-reel slug>` | `slot` | `reel` |

注：`board` 轴值取 canonical 形式（如 `reel`）；`reel(tumble)` 等玩法变体**不写进轴值**，改在 GDD §1 正文括号说明（如 `board：reel（tumble 级联）`）。

注：`grid` 盘面的 crash 游戏是 `crash-step × grid` 组合，**不是**独立的 mines 品类；本规范不存在 mines 品类。

### 1.3 文头 frontmatter（必备）

每份 `GDD.md` / `ADD.md` **必须**带 YAML frontmatter 文头，仅作登记用途。字段限下列白名单，**禁止**出现白名单外字段：

| 字段 | 含义 | 取值 |
|---|---|---|
| `project` | 代号（slug） | `<slug>` |
| `doc` | 文档类型 | `GDD` \| `ADD` |
| `interaction` | 交互模式 | 与 GDD §1 声明一致 |
| `board` | 盘面类型 | 与 GDD §1 声明一致 |
| `status` | 文档状态 | `draft` \| `signed` \| … |
| `owner` | 负责人 | `<role-or-name>` |
| `source_version`（可选） | 来源版本 | `<v1.0.x>` |

- frontmatter **仅限**上述登记字段，**禁止**把正文信息（组件表、图清单、TBC 等）外移到 frontmatter 或任何独立 yaml/json 文件。
- `interaction` / `board` 两轴值**必须**与 GDD §1 声明逐字一致。

---

## 2. GDD Schema（固定章节 §1-§6）

GDD 是 auto-art 的游戏上下文来源，美术只读参考，**不设签字**。章节编号与标题固定，缺章即为不合格。

### GDD §1 项目定位

- 目的：一句话定位 + 两轴声明。
- 必填项：代号（slug）、`interaction`、`board`、参考游戏（若为换皮）、屏幕与适配（分辨率/朝向）、语言列表、货币、非目标。
- 示例片段：

```
- 代号：<slug>
- interaction：<crash-step | slot | ...>
- board：<grid | lane-scene | reel | ...>
- 参考游戏：<reference-game-name | 无>
- 屏幕与适配：<WxH>，<portrait | landscape>
- 语言：<lang-a>, <lang-b>, ...
- 货币：<currency-code>
- 非目标：<out-of-scope-item>
```

### GDD §2 游戏流程与状态机

- 目的：给设计层可 scope 的状态标识符。
- 必填项：状态表（状态 / 标识符 / 说明）+ ASCII 状态图。标识符**必须** snake_case。

```
| 状态 | 标识符 | 说明 |
|---|---|---|
| <state-label> | <state_identifier> | <what-happens> |
```

### GDD §3 核心玩法

- 目的：玩法参数。
- 必填项：参数表（参数 / 标识符 / 规格 / 默认值）。

```
| 参数 | 标识符 | 规格 | 默认值 |
|---|---|---|---|
| <param-label> | <param_identifier> | <spec-or-range> | <default | TBC> |
```

### GDD §4 数学框架

- 目的：数值与公式。
- 必填项：公式 + 示例值。精确表允许挂 TBC。**禁止编造数值**——未知即 TBC，进 §6。

```
| 项 | 公式/规格 | 示例值 |
|---|---|---|
| <math-item> | <formula> | <value | TBC> |
```

### GDD §5 系统边界（美术相关）

- 目的：只收会产生 UI 素材需求的系统边界。
- 必填项：单 session 行为 / 断线重连 / 错误态 UI。**禁止**收录不产生素材需求的纯后端边界。

```
| 边界 | 触发 | 是否产生 UI 素材 | 说明 |
|---|---|---|---|
| <boundary-label> | <trigger> | <yes | no> | <ui-need> |
```

### GDD §6 TBC 表

- 目的：登记 GDD 内一切未定项。
- 必填项：

```
| item | owner | 影响范围 |
|---|---|---|
| <unknown-item> | <owner-role> | <impact-scope> |
```

> GDD 文末**可选**附「Changelog」段（列：版本 / 日期 / delta），语义为版本记录（含签前修订）；属非固定章节，缺省不影响合规。

---

## 3. ADD Schema（固定章节 §1-§9）——美术审签对象

ADD 是核心：美术审签对象 + auto-art 视觉输入。章节编号固定，品类模块段插在 §3 之后（见 §4）。

### ADD §1 风格锚点

- 必填项：关键词 / 色板 / 气氛图槽。
- 规则：气氛图（风格锚点参考图）**必须 ≥1 张**；缺失是 **lint 警告级**（不阻断但必须记录）。

```
- 关键词：<style-keyword-a>, <style-keyword-b>
- 色板：<hex-a>, <hex-b>, ...
- 气氛图：<file-in-assets>（≥1，关联 §7 参考图清单）
```

### ADD §2 屏幕与区块布局

- 必填项：屏清单 + 每屏区块表（区块 / 位置 / 内容）。

```
| 屏幕 | 区块 | 位置 | 内容 |
|---|---|---|---|
| <screen-id> | <block-label> | <position> | <content-desc> |
```

### ADD §3 组件需求清单（审签对象主表）

ID 前缀 `ART-C-`。这是全规范的机器解析锚，列定义逐字固定，**禁止增删列或改名**：

```
| ID | 屏幕/区块 | 组件 | 需求描述 | 状态变体 | 优先级 | 参考图 | 备注 |
```

行示例：

```
| ART-C-<nnn> | <screen>/<block> | <component-name> | <requirement> | <idle | idle/hover/pressed> | <P0|P1|P2> | <file-in-assets | 无> | <note | TBC> |
```

规则条款：

- **状态变体为必填列**。**必须**写 `idle`（单态）或 `idle/hover/pressed`（多态）等显式取值，**禁止**空置或依赖默认。（按钮态数因项目而异，必须逐项声明。）
- `ART-C-<nnn>` 编号**必须**连续、无重复。
- "参考图"列填 `assets/` 内文件名或 `无`；填写的文件**必须**同时登记进 §7。
- 「组件」列**必须**写「中文名 + snake_case dev 名」双名（如 `开始按钮 start_button`）。

### ADD §4 动效需求清单

ID 前缀 `ART-M-`。列与 §3 组件表**相同**，唯一差异是把"状态变体"列换成"时长/触发"：

```
| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
```

- 规格停在需求清单级，**禁止**逐帧规格。

### ADD §5 音效需求清单

ID 前缀 `ART-S-`。列与 §3 组件表**相同**，"状态变体"列换成"时长/触发"：

```
| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
```

- 规格停在需求清单级，**禁止**逐轨规格。

### ADD §6 文案 / 本地化

- 必填项：多语言键表（进正文表格，禁止外链 Sheet）。
- **baked-text 政策必填**：每处 UI 文字**必须**声明 `baked`（烘焙进图片）或 `overlay`（运行时文本层叠加）；不确定填 `TBC`。缺此政策为不合格。

```
| key | <lang-a> | <lang-b> | baked/overlay |
|---|---|---|---|
| <text-key> | <text-a> | <text-b> | <baked | overlay | TBC> |
```

### ADD §7 参考图清单

登记 `assets/` 下全部参考图。列定义逐字固定，**禁止**增删或改名：

```
| 文件 | 关联章节/组件ID | provenance | caption | 已知冲突 |
```

行示例：

```
| <file-in-assets> | <ART-C-nnn | §n> | <normative|illustrative|foreign-theme|placeholder> | <caption> | <conflict | 无> |
```

规则条款：

- **provenance 四值**（仅此四值合法）：
  - `normative`：权威规格，视觉即需求。
  - `illustrative`：仅示意，不作精确依据。
  - `foreign-theme`：借自参考游戏/异主题，题材需替换。
  - `placeholder`：占位图槽，待补真图。
- **文图冲突时以文本 + changelog delta 胜**（这是写死的裁决规则；文本永远 normative）。
- `foreign-theme` 图的"已知冲突"列**必须**填写冲突点或显式填 `无`，**禁止**空置。
- 清单与 `assets/` 目录**必须**双向一致：清单里的文件都存在，目录里的文件都登记。

### ADD §8 共用壳引用

- 必填项：引用到的 `_common` 模块清单 + 本作差异（如 history 字段增删）。
- 唯一允许的外部引用形式：`../_common/<module>.md` 相对路径 + 模块名。**基准目录为本包目录**（`<slug>-pack/`），故以 `../_common/` 上溯到 `prds/_common/`。

```
| 模块 | 路径 | 本作差异 |
|---|---|---|
| <module> | ../_common/<module>.md | <delta | 无> |
```

### ADD §9 TBC + 签字区

- 必填项：TBC 表 + 签字表 + changelog 段。
- 生成方**必须**留空签字表（不得代签）。

TBC 表：

```
| item | owner | 影响范围 |
|---|---|---|
| <unknown-item> | <owner-role> | <impact-scope> |
```

签字表（列逐字固定）：

```
| 角色 | 姓名 | 日期 | 冻结范围 |
|---|---|---|---|
| <role> | <name> | <YYYY-MM-DD> | <frozen-scope> |
```

changelog 段（列逐字固定）：

```
| 版本 | 日期 | delta |
|---|---|---|
| <v1.0.x> | <YYYY-MM-DD> | <what-changed> |
```

- 签字冻结记 `v1`。签后一切改动**必须**走 changelog（`v1.0.x` delta）；机器**以最新 delta 为准**。

---

## 4. 品类模块段登记表

品类模块段插在 ADD §3 之后、§4 之前，编号用 `§3a`、`§3b`… 递增。段由 `interaction × board` 两轴共同决定。

### 4.1 自声明格式（强制）

每个模块段**必须**满足：

- 段头一行 HTML 注释声明轴值，供 lint 与 auto-art 定位：

```
<!-- module: board=grid -->
```

（board 段用 `board=<value>`，interaction 段用 `interaction=<value>`。）

- 紧接小节标题：`### §3a <模块段名称>`。

### 4.2 已登记模块段

| 轴值 | 模块段内容 |
|---|---|
| `board: grid` | 格子状态矩阵（tile 状态 × 标识符 × 视觉） |
| `board: lane-scene` | 场景分段表 / 难度变体表（目录级变体声明） |
| `board: reel` | 符号表（symbol × 语义 × Wild/Scatter）、赔付表屏视觉 |
| `interaction: slot` | win-tier 演出矩阵、Free Spin 层、locale × 换图矩阵 |
| `interaction: crash-step` | 步进/倍率条展示、cashout 按钮态（多态按钮，逐态声明） |

模块段示例骨架（以 `board: grid` 为例）：

```
<!-- module: board=grid -->
### §3a 格子状态矩阵

| tile 状态 | 标识符 | 视觉 |
|---|---|---|
| <tile-state> | <tile_state_identifier> | <visual-desc | file-in-assets> |
```

### 4.3 新品类扩展

新品类 = 核心骨架（ADD §1-§9）照写 + 新建模块段。新建模块段**必须**遵守 §4.1 自声明格式，并在本登记表补一行后方可使用。

---

## 5. 两段式清单流程 + ID 体系

素材清单分两段：上游签**组件级**（`ART-C-nnn`），auto-art 展开成**素材级** BOM 回填 `ASSET-CHECKLIST.md`。

### 5.1 流程

```
外部 AI agent 按本规范生成包
  → 美术审核（改需求描述 / 驳回 / 补风格锚点）→ 签字 v1 冻结（ADD §9）
  → auto-art 消费：ART-C / ART-M / ART-S 展开素材级 BOM
  → 回填 ASSET-CHECKLIST.md
  → 美术二审 → 按行开 ticket → 验收勾选
```

### 5.2 ASSET-CHECKLIST 列定义（auto-art 回填）

列逐字固定，**禁止**增删或改名：

```
| Asset ID | 文件名 | 来源组件ID | 尺寸 | 状态变体 | 格式 | 验收 |
```

行示例：

```
| A-<nnnn> | <name>.png | ART-C-<nnn> | <WxH> | <idle | idle/hover/...> | <png|...> | ☐ |
```

### 5.3 追溯链

```
素材行（A-nnnn）→ 来源组件 ID（ART-C-nnn）→ ADD 章节
```

- 每个素材行的"来源组件ID"**必须**能回溯到 §3（或 §4/§5）中一个存在的 ID。
- 签后改动一律走 changelog（`v1.0.x` delta），机器以最新 delta 为准。

### 5.4 行文纪律（生成方必守）

- 用正向时态、单次生成口吻。**禁止**出现"逆向 / 还原 / 评估 / 与旧稿差异"等痕迹字样。
- 未知值一律进 TBC 表，**禁止编造**（数值、尺寸、色值皆然）。

### 5.5 表格语法约定

规范表格中已实践的写法约定（生成方须遵，lint 与 auto-art 按此解析）：

- **参考图列多文件**：一格多张图用 ` / ` 分隔（如 `a.png / b.png / c.png`）。
- **复合状态变体**：一个组件含多组独立状态时，用 `<part>: 态/态; <part>: 态/态` 语法（如 `date_range: idle/active; container: idle/highlighted`）。
- **§7 文件列模式名**：`placeholder` 行的「文件」列允许填模式名 `xxx_{var}.png（待补）`（仅 placeholder 行，代表待补图槽，非实文件）。
- **优先级列**：允许填 `TBC`（优先级尚未定时）。

---

## 6. 附录：Lint 清单（声明，不实现）

本清单是机器可校验项的声明。**工具实现不在本规范范围**；此处只定义每条的检查方法。

| # | 检查项 | 检查方法 |
|---|---|---|
| L1 | 必填章节存在性 | grep 章节标题：GDD 需匹配 `§1`-`§6`，ADD 需匹配 `§1`-`§9`；缺任一为失败 |
| L2 | 品类模块段与两轴一致 | grep `<!-- module: (board|interaction)=... -->` 段头，比对 GDD §1 声明的两轴；不一致为失败 |
| L3 | 规范表格列名与列数匹配 | 提取三张固定表表头行，逐字比对本规范「ADD §3 组件需求清单」表头、「ADD §7 参考图清单」表头、「5.2 ASSET-CHECKLIST 列定义」 |
| L4 | ID 连续无重复 | 抽取 `ART-C-`/`ART-M-`/`ART-S-` 编号，检查各自序列连续且唯一 |
| L5 | 来源组件 ID 可回溯 | ASSET-CHECKLIST 每行"来源组件ID"必须在 ADD §3/§4/§5 的 ID 集合内 |
| L6 | 图清单 ↔ assets 双向一致 | §7"文件"列集合与 `assets/` 目录 listing 求对称差，差集非空为失败；provenance=`placeholder` 的行为待补图槽（无实体文件），不参与本项比对 |
| L7 | provenance 值合法 | §7"provenance"列取值必须 ∈ {`normative`,`illustrative`,`foreign-theme`,`placeholder`} |
| L8 | foreign-theme 必填冲突 | §7 中 provenance=`foreign-theme` 的行"已知冲突"列非空（含显式 `无`） |
| L9 | TBC 项有 owner | GDD §6 / ADD §9 的 TBC 表每行"owner"列非空 |
| L10 | 正文无裸外链 | `grep -nE 'https?://'` 全文，仅 `prds/_common/` 相对路径豁免；命中裸链接为失败 |
| L11 | 风格锚点气氛图 ≥1 | ADD §1 气氛图槽计数 ≥1；为 0 是**警告级**（不阻断） |
| L12 | baked-text 政策存在 | ADD §6 必须含 baked/overlay 声明列且每行有取值（含 `TBC`） |
| L13 | frontmatter 字段合法 | GDD/ADD 文头 frontmatter 字段集 ⊆ §1.3 白名单；且 `interaction`/`board` 与 GDD §1 两轴声明逐字一致；否则失败 |

---

## 7. 验收标准（本规范生效条件）

1. 一个没看过设计过程的外部 agent 能照本规范生成结构合格的包。
2. 生成的包能通过 §6 Lint 清单人工走查（除显式声明的 pending 项）。
3. 美术团队能只凭 ADD §3 / §9 完成"审→签"，无需读其它材料。
4. auto-art 能从 ADD §3 表 + 品类模块段 + §7 图清单机械提取输入。
