---
name: reverse-game-to-triad
description: 逆向一款已上线游戏（前端代码 + 真实资产，可能另带 Figma/.art-meta 设计稿）产出可 1:1 复现的训练素材三件套 ADD/GDD/UI-灰盒。当用户要"从某真实游戏反推 ADD/GDD/界面设计"、"把游戏做成 agent 训练素材"、"提取下一款游戏"时使用。核心纪律：以上线 runtime（截图+代码）为唯一真值，设计稿/mock/注释只作补充，冲突一律 runtime 赢。产物喂回 auto-art / 代码 agent 即可复现该游戏。
---

# Reverse Game → Triad（逆向游戏 → 三件套）

把一款已交付的游戏（前端仓库 + `public/assets`）逆向成三份**可复现训练素材**。范例（按品类看差异）：
- `output/cg03a/`「Jeepney Glide」— 竖向逐站 crash，**自带 Figma 设计稿** `.art-meta/`（含设计↔上线差异速查范例）。
- `output/cg03r/`「Cluck Dash」— 横向车道 crash，**无** Figma，多币种（bet 档位随币种变）。
- `output/cg02a/`「榴莲派对」— 多人连续曲线（Aviator 类），**无长地图**（榴莲钉死、滚动 bg tile + 排行榜长列表才是"超屏"的东西）。

本 skill 把这套方法论固化，供逐款复用。

---

## ★ 0. 真值权威与可信度（贯穿全程的第一原则）

**复现目标是上线 runtime 的样子**，不是设计稿、不是 dev mock。任何来源冲突时，按下表高者赢：

| 优先级 | 来源 | 说明 |
|--:|---|---|
| ① 最高 | **真机截图（runtime）** | 玩家实际看到的。Spine 上屏尺寸/动画编排/语义色/服务端实际下发值的唯一硬证据。 |
| ② | **源码 runtime 路径** | 固定画布的渲染常量（坐标/尺寸/z/缓动）；`RealSocket`（服务端下发）；`LayoutZones` 等。固定画布坐标=1:1 真值，比截图精确。 |
| ③ | **Figma/.art-meta 设计稿** | 设计意图 + 截不到的屏的精确坐标。**但设计≠上线**（见 §2），与 shipped 冲突处以 shipped 为准。 |
| ④ | **mock/dummy socket** | `CluckDashSocket`/`DummySocket`（dev-bypass）。经济值多为**占位**，常与线上不同（见 §3 陷阱）。仅 laneMults/pHazard 这类"镜像 routes.json"的可信。 |
| ⑤ 最低 | **代码注释 / 旧文件名** | reskin 残留，最不可信（cg03a 注释写 "green/chicken/hop 0.2+0.4"，真值是紫/吉普尼/1.5s）。 |

**三态来源徽标**（HTML 灰盒每帧 + ADD 数值都标）：`validated`（截图核过）/ `figma`（设计稿坐标）/ `code-derived`（代码推定，未经截图）。冲突时永远 runtime 赢，设计稿降级为"差异"记录。

### 0.1 代码优先：结构也要在「没截图」时从代码定准
**关键现实**：用本 skill 跑新游戏是**代码优先**——阶段1 穷尽抽取在**完全没有截图**时做；阶段2 才按需向用户要图、且**只覆盖部分态**（飞行/结算/过场/异常/设置子页等很多态可能永远要不到 → 永远 `code-derived`）。所以**凡代码能定的（包括"结构"）必须在无图/缺图时就定准**；截图是**事后确认 + 揪残留 + 拿那几样代码真给不了的**，不是结构的主源、更不是"等截图再说"的借口。

| 属性 | 代码能定吗？无截图时怎么定 | 截图角色 |
|---|---|---|
| 静态坐标/尺寸 | **能**：读到常量**重算公式本身**（别信 `//=…` 注释/预填值——cg03a `56/-56/5` 实为 `33.5/-88.5/57`；连验证 agent 都被注释带偏把按钮算到越界） | 确认 |
| 运行时算出的位置（centerline 车/站牌、scroll/camera） | **能**：按代码数据**写脚本模拟**（如算各难度视口内站点数），别目测 | 确认 |
| 结构/gestalt（越界·数量·哪侧·填满还是顶对齐·谁压谁·漏件） | **能！** 越界/填满=§7 invariant 自检；数量/侧=模拟公式；层叠=读 addChild 序/z；漏件=grep 资产全集 + 逐元素 diff | 确认+兜底 |
| Spine/演员**上屏渲染尺寸**、命令式动画编排 | 部分（scale 常是常量，编排靠看） | **主源** |
| 服务端下发值（经济/曲线/bet 档位） | **不能**（mock 是占位） | **主源（+RealSocket）** |

**所以**：① 别把"结构对不对"推给截图——能用 compute/模拟/§7 自检在无图时解决的，**当场解决**。② 截图到手后只做**确认 + 揪残留**（它有 ±裁剪/缩放/DPI 误差，~±10–30px）；**误差内一致取代码值**，只有**结构性**冲突（越界/漏件/错侧/数量不符）才以截图推翻代码。③ **别用目测截图坐标覆盖能算的代码常量**（实战：曾用目测改掉本来对的代码值，又被源码公式纠回）。

---

## 1. 产物与分工契约（三件套，每份只答一个问题）

| 文件 | 只回答 | 受众 | 关键内容 |
|---|---|---|---|
| `ART-AUDIO-<CODE>.md` (ADD) | 长什么样、用什么资产、什么声音 | 美术/音频 agent | 题材 Style Bible(配色/材质/不变量)、逐资产表(target_path/type/dims/tier/mode/origin/prompt 锚点)、场景系统、spine、特效、音频触发、i18n、**设计↔上线差异速查表(若有 Figma)** |
| `GDD-<CODE>.md` (GDD) | 什么游戏、什么规则、什么状态流转 | 写前后端代码 agent | 回合状态机、难度/经济/数学表、bonus、派彩、输入锁、网络/断线状态机、时序。**经济值标 mock-vs-real + 服务端权威**。不含美术 |
| `UI-GREYBOX-<CODE>.html` | 每屏每态、东西摆哪、多大、哪一层 + UI 行为 | UI 复现 agent + 人 | 数据驱动灰盒：SCREENS(视口帧)+SCENES(超屏长卷)+渲染器+注释面板+三态徽标 |

**铁律**：三份交叉引用、互不重复。接缝处约定唯一权威——动画时长→HTML；玩法状态→GDD；资产 origin/派生规则→ADD；HTML/GDD 引用对方时只给指针不复制。

---

## 2. 总流程（5 阶段）

```
阶段0 定位+清点(inline,廉价) → 阶段1 穷尽抽取(1个workflow) → 阶段2 视觉+截图门(+Figma门)
  → 阶段3 产三件套 → 阶段4 校验(回查一手源)
```

### 阶段 0 — 定位 + 清点（inline，先做，便宜）
1. **定位仓库**：游戏前端目录（多为 `crashgame-<code>-ui/<code>`）、`public/assets/` 资产树、`src/`。
2. **检查设计稿**：有无 `.art-meta/`（`nodes.json`=Figma REST 导出 / `dev_book.md` / `manifest.json` / `decisions.json` / `rename_map.json`）？**多数游戏没有**——有则是金矿（§2 挖法），无则退回代码+截图。
3. **认 socket 权威**：组合根（如 `CrashGameplayManager`）按 `_devBypass` 选 **mock**(`CluckDashSocket`/`DummySocket`) vs **`RealSocket`**。记下哪个是真值源——经济值要从 RealSocket 看（§3）。
4. **取所有资产精确尺寸**（用 §7 `asset-dims.py`）——ADD 尺寸 + HTML 原生尺寸的依据。
5. **grep 资产路径全集**：`grep -rhoE "assets/[A-Za-z0-9_./-]+\.(png|jpg|jpeg|webp|json|mp3|atlas)" src | sort -u`，记总数（完整性基线）。
6. **读参考 ADD 格式**：上一款 `output/<prev>/` 作 frontmatter + 章节模板。
7. **判定品类与引擎 + "场景"形态**：crash/slot/其他？Pixi/Unity？玩法里"超一屏的东西"是什么（竖向路长卷 / 横向车道 / 滚动 bg tile / 长列表）——决定阶段 1 聚类 + SCENES 画廊放什么。

### 阶段 1 — 穷尽抽取（一个 workflow，ultracode）
源码是固定画布游戏的 1:1 坐标真值。用一个工作流把**全部布局/逻辑源文件按子系统并行读全文**，再完整性校验 + 可行性判定。
1. `find src -type f \( -name '*.ts' -o -name '*.tsx' -o -name '*.css' \)` 列全文件，**按实际结构聚类**（cg03a 用过 11 类：app-flow / dom-screens / scene-core / topbar-content / gameview-core / scene-effects / playerHUD / settings / popups / ui-widgets / theme-config——按各游戏增删）。
2. 跑 §7 的 workflow 模板：每 cluster 一个 Explore extractor（schema 化）→ 完整性 critic（grep 全资产对照覆盖）→ feasibility judge（逐项说哪需截图、是否阻塞）。
3. 结果落盘 scratch（可能数百 KB），写文档时按 cluster 取常量。
4. **workflow 容错**：若 AbortError / 输出空，用 `resumeFromRunId` 重跑——已完成 agent 走缓存秒回（cg02a 实战靠此救回）。
5. ⚠️ **抽取 agent 会出错**：它读 mock socket 会把占位当真值上报、会算错计数。其结论是**线索不是结论**，阶段 4 必须回查一手源。

### 阶段 2 — 视觉门 + 截图门 + Figma 门
1. **亲自看关键图**（Read 图片）：logo/背景/各场景/主角 sprite/按钮/特效——提题材/材质/配色（Style Bible 只能靠看图）。
2. **判定盲区**：固定画布游戏，静态屏/HUD 代码即 1:1；**仅 Spine 上屏尺寸 + 命令式动画编排**靠截图最稳。
3. **截图门（向用户要图）**：列出精确需要哪几张（中局含全 HUD 态 / 结算-大奖 / 过场 / 设置各 tab / 异常 / 弹窗），每张说明验证什么。没截图的态按代码**定准**（算公式 / 模拟运行时位 / §7 自检——不是粗略 best-effort）、打 `code-derived` 徽标，拿到图再升 validated。
   - 实战教训：截图揪出过"PLAY 紫非绿"、"货币=星币"、bet 档位随币种变(coin 4/PHP 5)、撞车=车冻结+烟+红闪(无大横幅) 等硬错。
4. **Figma 门（若阶段 0 发现 `.art-meta/nodes.json`）**：这是截不到的屏（异常/断线弹窗）的精确坐标来源。挖法：每 screen frame 自带 `absoluteBoundingBox`（所有 frame 均 1:1 于画布尺寸），**子节点坐标 = 子 bbox − frame 原点**；遍历取 name/type/局部 x,y,w,h/fills/characters。**产出后标 `figma` 徽标**，且与 shipped 资产/代码逐一对照——分叉处记入差异速查表、以 shipped 为准。

### 阶段 3 — 产三件套
按 §1 分工 + 阶段 1/2 数据写。骨架直接复制范例（cg03a/cg03r/cg02a 任一最近似品类的）改数据最快。

### 阶段 4 — 校验（§6 清单，**不可省**）
本阶段的存在意义：初次生成会混入 mock 值、抽取 agent 的错、臆造的计数。**逐条承重数值回查一手源**。

---

## 3. ADD 要点（art/audio）
- **Step 0 Style Bible**：一句话美学 + 60-30-10 配色(theme.json + 看图) + chrome 材质族 + 不变量(chroma-key 色 / 不烧字除 logo+艺术字 / effect 独立资产)。
- **逐资产表**：每行 `target_path | type | dims | tier | mode(regen/full_bleed/sheet) | origin(generate/derive) | 描述`。path 即写回 public/assets 的路径。
- **标注**：原生尺寸 vs 运行渲染尺寸（两者都给）；占位/孤儿/未部署（**判孤儿前先 grep `.atlas` 看多页**——cg03a `chara9_2.webp` 曾被误判孤儿，实为 `chara9.atlas` 第 2 页）；按钮"仅出 idle，hover/pressed/disabled=tint 派生"。
- **场景系统**：滚动/平铺玩法给 start/middle/end 段尺寸 + 无缝契约；spine：辨清"一套骨架多动画" vs "按难度多套骷架"（设计稿常说 1 套，shipped 可能 N 套——以 `ls public/assets/spine/` 为准）。
- **设计↔上线差异速查表（若有 Figma/.art-meta）**：置顶一块表，列出设计与 shipped 分叉项（命名 / 控件数 / spine 结构 / 按钮文案 / 数值），每条注"以 shipped 为准"。范例见 `output/cg03a/ART-AUDIO-CG03A.md` 顶部。

## 4. GDD 要点（game logic）
- 回合状态机 + 信号名；难度/经济**数学表**；bonus 经济（概率/delta/cap/角色映射）；派彩公式；输入锁；断线/idle/错误状态机；时序（结算/hop 时长）。**不写美术长相**。
- ⚠️ **mock-vs-real 陷阱（必守）**：数学表从源码抽，但 **mock socket 的经济值多是 dev 占位**。
  - laneMults / pHazard（注释"镜像 routes.json"的）：mock 通常 = real，截图首两项可验。
  - **bonus delta / 曲线 / RTP / AC 阈值**：mock 常 ≠ real（cg03a mock bonus 0.2/0.5/1.5，真值≈0.1/0.3/0.5）。真值在 `RealSocket`（`parseDecimal(ret.xxx)`=服务端下发，客户端无公式）。**标"真服务端值=X（依据：截图累计 + 跨游戏 parity），mock 占位=Y 勿作真值"**。
- **服务端权威 + 配置可变**：客户端只有硬编码兜底；`NET_BET_CONFIG` 等运行时覆盖。**bet 档位数量+值按币种/场次变**（coin 4 档[1,2,5,10] / PHP 5 档[100,500,1000,5000,10000]）——别断言固定档数，标"服务端下发，兜底=…，按 count 自适应"。倍率曲线/crash/RTP 标"服务端权威、客户端无公式"。

## 5. UI-GREYBOX HTML 规格（核心产物）
单文件自包含（内联 CSS/JS，零外链）。**数据驱动**：两个 JSON 数组 + 内联 JS 渲染成绝对定位灰盒，`transform:scale()` 缩放预览。**纯灰盒**（不画美术、不叠截图）。复制最近似品类范例当骨架最快。

- **关键区分：屏 vs 场景**。屏=玩家当下看到的视口（如 1080×1920）；场景=**远超一屏、滚动穿过视口的东西**——按品类不同：竖向路长卷(cg03a) / 横向车道(cg03r) / 竖向滚动 bg tile(cg02a) / 长列表(排行榜/注单)。**两个画廊分开**，屏内固定的别塞进场景画廊；屏放不下的别塞进一屏。
- **按原生代码分层拆画廊（若组件按信号域解耦）**：若 MainScene 把内容层(如 `ContentView`，相位驱动)与 HUD 层(如 `PlayerHUD`，钱包驱动)写成**独立组件、订阅互不相交的信号域**，就把灰盒也**按层拆成独立画廊**（各自一套状态机），更贴原生代码、更便于 agent 理解。配套两件：① **合成契约**（一张表：层序/z/分区 y/驱动信号，说明如何拼回整屏）；② **典型合成屏**（content 帧 + HUD 帧叠成整屏，给人/截图比对）。**跨层元素**（如难度弹层从 HUD 升入内容区）按该卡单独裁 ghost 占位高度，别让它悬在斜纹占位上。范例：`output/cg03a/UI-GREYBOX-CG03A.html`（②内容/③HUD/④合成 三画廊 + 合成契约）。
- **SCREENS**（视口帧）：`{id,cap,badge,meta, layers:[{role,asset,x,y,w,h(左上绝对px),anchor,z,k(tier),label,sub}]}`。每屏×每**态**一帧（loading↔ready、bet↔cashout、selector 开合、各 overlay、设置 tab、弹窗、撞毁/结算）。
- **SCENES**（超屏长卷）：`{id,stage:{w,h:<tall>},segments/tiles,centerline(真数据降采样),viewport:{y,h},anchor,notes}`。渲染：段竖/横排 + SVG 画真 centerline + 视口窗矩形 + 主角锚 + 滚动箭头。
- **三态徽标**：`validated`(截图,绿) / `figma`(设计稿,蓝) / `code-derived`(代码推定,橙)。渲染器按 `badge` 上色 + 文案；图例 + 表头说明来源。冲突时 runtime 赢，设计稿差异在注释面板记。
- **渲染器**：layer→`position:absolute` div、z-index、可见标签(role+dims+asset)、`data-*`(尤其 `data-box`=x,y,w,h、`data-role`，供 §7 自检) 全量元数据。哑灰填充 + 细边，按 tier 上色(bg/chrome/featured/hero/fx/data/overlay)。
- **CSS 堆叠隔离**（实战 bug）：页面有 sticky 顶栏时，卡片内 box 的高 z-index(分区线 z200/overlay z50+) 会跑进根堆叠上下文与顶栏比大小——滚动时内部 box **穿到顶栏前面**。修：每张 `.stage` 加 `isolation:isolate` 自成堆叠上下文(把内部 z 全封进卡片)，顶栏 z-index 给足(如 1000)。
- **注释面板**（折叠 `<details>`，装非空间信息）：① 屏幕流/状态机(触发引用 GDD) ② 动画时长/缓动表(HTML 为权威) ③ 滚动/场景机制 ④ 控件渲染约定(idle→tint 派生/toggle 双图/文字 runtime 叠) ⑤ 资产/差异注记(含设计↔上线、mock-vs-real、服务端配置可变)。
- **锚点换算**：Pixi 常 anchor(0.5,0.5)/center-pivot；CSS 默认左上。box 存左上 x,y,w,h，anchor 写进 `data-anchor`/标签。

## 6. 校验清单（阶段 4，逐条回查一手源）
- [ ] **每个承重数值能 cite 到源码行**——cite 不出来的当**臆造删掉**（实战删过臆造的 `middle 数 7/5/4/3`）。
- [ ] **经济值追到 `RealSocket` 而非 mock**；bonus delta/曲线/RTP 标 mock-vs-real。
- [ ] **资产文件名/数量用 `ls` 实核**，别凭记忆/抽取（实战修过 `bgm_normal`→`bgm.mp3`）。
- [ ] **判孤儿前 grep `.atlas` 多页**（多页图集的 page2 webp 看着像没引用，其实是第 2 页）。
- [ ] **抽取/子 agent 结论不全信**——以 grep/ls/读文件复核；尤其"计数类"(控件数/段数/SFX 数)最易错；agent 还会**信过期注释、把算式算错**（cg03a 验证 agent 把 MAX 键算到 x1103 越界）。
- [ ] **读到的常量重算公式**，不信 `//=…` 注释、不信预填常量值（cg03a 多处注释过期：56/-56/5 实为 33.5/-88.5/57）。
- [ ] **设计稿数值不直接采信**——与 shipped 冲突的入差异表、不进正表。
- [ ] **复核自己过往的"更正"批注**——旧更正会过期变错（cg03a GDD §4 脚注把**正确**的 middle 7/5/4/3 误标"臆测已删"，源码 `ensureRoadCoverage` 实为 `(totalLanes−startHops)/4`）。别假定上次改对了。
- [ ] `node --check` 抽取的 HTML `<script>` 无语法错（§7）。
- [ ] **跑 jsdom 渲染自检（§7）**：零 JS 报错 + 帧数对 + **所有 box 在画布内**（自动揪"飞出屏外"——cg03a 历史页 Recent Week 因间距算错越界到 x1162>1080，肉眼看代码看不出）。
- [ ] **运行时算出的位置用脚本模拟核对**（如各难度起始视口内站点数应恒为同值），别只靠目测——曾把站点钉死在单 tile 绝对坐标，致 medium/hard/hardcore 视口只剩 1 站。
- [ ] **重写/重构后 diff 旧元素清单**——重写最易**静默丢对称/次要件**（cg03a 重写漏过 BGM 静音、Language 分区头、音量分区头）。
- [ ] HTML 预览下注态帧 ≈ 截图；坐标抽查对照源码常量。
- [ ] 三件套交叉引用无悬挂、无重复同一事实：`grep -rn "UI-DESIGN\|<旧名>"` 应为空。
- [ ] 完整性：阶段 0 的资产路径全集都在 ADD 或 HTML 有归属。
- [ ] **徽标严格自洽**：`validated` 仅当**该状态本身**有截图——用相邻态(如下注态)验证了路/皮 **≠** 验证了别的态(飞行/结算/过场/设置 guide/loading)，后者仍 `code-derived`（曾把 fly/win/boarding/cashout/guide/loading 错标 validated）。设计稿来源标 figma。

## 7. 复用脚本（在 `scripts/`，按路径直接跑，**不读进上下文**）

| 脚本 | 用途 | 跑法 |
|---|---|---|
| `scripts/asset-dims.py` | 扫资产真实尺寸(PNG/JPG/WEBP，无依赖)——ADD 尺寸 + HTML 原生尺寸依据 | `python3 scripts/asset-dims.py <game>/public/assets` |
| `scripts/figma-screen.py` | 从 `.art-meta/nodes.json` 抽某屏子节点局部坐标(截不到的屏的精确源) | `python3 scripts/figma-screen.py <nodes.json> <frame名>` |
| `scripts/extract-workflow.js` | 阶段1 穷尽抽取 workflow 模板(改 REPO+CLUSTERS) | `Workflow({scriptPath})`；中断 `resumeFromRunId` 续跑 |
| `scripts/centerline-downsample.py` | centerline 降采样给 HTML SVG(仅滚动/路径类) | `python3 scripts/centerline-downsample.py <centerline.json>` |
| `scripts/greybox-check.js` | 灰盒 jsdom 自检：JS错/漏件/越界一次抓(改 W/H) | `node scripts/greybox-check.js UI-GREYBOX-<CODE>.html`(需 `npm i jsdom`) |

两个一行命令（无需成文件）：
- **atlas 多页核查**（判孤儿前先跑）：`grep -rHE '\.(webp|png)$' $(find <game>/public/assets -name '*.atlas')`
- **HTML JS 语法快检**：`python3 -c "import re;open('/tmp/_gb.js','w').write(re.search(r'<script>(.*)</script>',open('UI-GREYBOX-<CODE>.html').read(),re.S).group(1))" && node --check /tmp/_gb.js`

> `greybox-check.js` 读 box 的 `data-box`(x,y,w,h)/`data-role`，故灰盒渲染器须把这两项写进每个 box；它只查屏帧(SCENES 长卷另算)。

## 8. 踩过的坑（概念性陷阱；机械检查清单见 §6）
1. **代码优先**：静态坐标 + 结构都在**无截图**时从代码定准（算公式不信注释 / 模拟 / §7 自检 / grep 完整性，见 §0.1）；截图只事后确认 + 拿代码给不了的（Spine 上屏/动画/服务端值）。
2. **设计稿 ≠ 上线**：Figma 补截不到的屏，冲突一律 shipped 赢、分叉记差异表（§3）。
3. **mock ≠ real**：dev socket 经济值（bonus/曲线/RTP）是占位，真值在 RealSocket（§4）——连验证 agent 都会拿 mock 当真。
4. **服务端可变**：bet 档位 / 曲线 / RTP 服务端权威、客户端无公式，别断言固定值。
5. **跨游戏污染**：reskin 残留的注释/命名/旧文件名，一律以 runtime 为准。
6. **三组「≠」**：屏 ≠ 场景；资产原生尺寸 ≠ 上屏渲染尺寸；状态 ≠ 屏（每态一帧）。
7. **谁都会错、且会过期**：抽取/验证 agent 会错、代码注释会过期、连**自己的"更正"**也会过期——一律回一手源重算、跑 §6 自检。
8. **三份分工互斥 + 交叉引用**；动画时长唯一权威在 HTML。

## 9. 输出位置 & 命名
本 repo（`~/harley/ai_whole_pipeline/ai-reverse-skills`）根下 `output/<code>/`：`ART-AUDIO-<CODE>.md` / `GDD-<CODE>.md` / `UI-GREYBOX-<CODE>.html`（`<CODE>` 大写，如 CG03A）。**`output/` 是交付物，git 跟踪**；逆向工作材料（源构建/解包/分析件）放 `work/<code>*/`（gitignored）。

> 安装为可 `/` 调用的 skill：把本目录复制到 `.claude/skills/reverse-game-to-triad/`；或直接让 Claude "按 skills/reverse-game-to-triad/SKILL.md 提取 <游戏>"（本 skill 家在 `~/harley/ai_whole_pipeline/ai-reverse-skills/`）。
