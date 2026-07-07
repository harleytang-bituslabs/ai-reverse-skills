---
name: reverse-unity-game-to-triad
description: 逆向 Unity WebGL 老虎机(ss 系列,如 ss03「MAHJONG STREAK」/ ss02「Beach Party」)产出可 1:1 复现的训练素材三件套 ADD/GDD/UI-灰盒。针对【编译构建】游戏:前端 repo 只是 React/Next 宿主,真游戏是 CDN(公开 S3)上的 Unity WebGL 包,**靠 UnityPy 解包**抽资产/布局/配置,数学去服务端 repo 直读(或运行时 Guide 页验证)。当用户要"提取/反推 ssXX 老虎机""把某 Unity 游戏做成 agent 训练素材"时使用。
---

# Reverse Unity Game → Triad（逆向 Unity 游戏 → 三件套）

**引擎决定抽取方式**。本 skill 针对 **Unity WebGL 编译构建**游戏(老虎机 ss 系列):前端 repo 只是 React/Next 宿主(依赖含 `react-unity-webgl`),**真游戏是 CDN 公开 S3 上的 Unity 构建**(`.data`/`.wasm` + Addressables),repo 里 0 张游戏图。抽取靠 **UnityPy 解包**(下 S3 构建 → 拆 UnityWebData → data.unity3d + 全部 bundle → 导资产/合成布局),数学去**服务端 repo 直读**,读不到用**运行时 Guide 帮助页**验证。

产出三件套 **ADD/GDD/UI-灰盒**(+伴生 `elements-<CODE>.json` 机器清单):ADD 是**精炼设计文档**(设计意图+玩法→美术适配;逐文件全量清单归 elements json),灰盒按**屏最小覆盖硬清单**(§5.0)出齐,全部标**三态可信度徽标**,跑**完整性对账 + jsdom 自检**。核心方法论见 §0★(最重要)。

---

## ★ 0. 真值权威与可信度

**复现目标 = 上线 runtime 的样子;但生成结果里的每个值永远从代码/构建取,截图只用于"理解与确认"。**

**按属性分权威**(该属性只认它的权威源,别串):

| 属性 | 权威源 | 次级(注明) | 绝不 |
|---|---|---|---|
| 几何(位置/尺寸/层级) | **构建 RectTransform 合成 px**(compose 脚本算出) | 世界空间件用 UI 复刻件定比例(§5.3) | **绝不量截图像素** |
| 美术/音频资产 | **UnityPy 导出文件**(名字/真实尺寸/时长) | — | 绝不凭截图描述资产 |
| 结构(有哪些屏/件/态) | **构建层级 + Addressables bundle + 宿主 repo** | 截图确认"存在性" | 绝不借旧草稿骨架 |
| 游戏数学(赔付/触发/RTP) | **服务端 repo 直读** cite file:line | **运行时 Guide 帮助页** = validated,注明"无一手 cite" | 绝不信换皮文档数值、绝不编 |
| runtime 动效/编排/语义色 | **真机截图/录屏** | AnimationClip `m_Length`(引擎类型,IL2CPP 剥不掉,**可读**→时长可 extracted) | — |
| 版本/模式存在性 | **线上 version.json + 当前构建** | — | 绝不信旧草稿/文档版本号 |

**截图的角色(硬规则,ss02 实录)**:**代码/构建是唯一真实信源;截图不是流程输入,是可选的外部反馈回路**——只用来 ①理解真实视觉 ②确认屏/功能/状态存在性 ③对已生成的结果做核对(升 validated 徽标、暴露盲区反馈回抽取)。生成结果里的每个值**一律回构建/代码取值并 cite**,绝不从截图推导。
**部署形态=零截图**:无任何截图时,全流程照常跑完、三件套照常出齐,徽标如实停在 extracted/derived——缺截图只降徽标等级,**不缺屏、不缺件、不降几何精度**(几何本来就不来自截图)。

**三态徽标**(灰盒每帧/每承重 box + ADD/GDD 数值都标):`validated`(该态自身有截图核过)/ `extracted`(UnityPy 解出/构建合成 px)/ `derived`(世界投影/布局组运行时排布/宿主设计空间估算/服务端未证)。
**代码是运行时的超集(ss02 实录)**:构建里有、运行时被配置关掉的(如 `AppConfig.ShowExitButton` 门控的 Exit tab)**照画**,注 `config-gated`;别因截图没有就删,也别因代码有就当必现。

### ★★ 方法论:即时回源抽取,勿靠长上下文召回,更勿借旧草稿骨架(最重要)
**每个承重值(坐标/尺寸/赔付/列数/资产名…)在落笔那一刻回源头抽取,立即写进产物或脚本,绝不靠"我之前读过"或"上一版这么写"。** 两个反面:
1. **长上下文召回失真**:中段遗忘 + compaction 把精确值压成散文,你以为记得的数其实已糊。
2. **旧草稿/上一版三件套是最不可信源**:可能基于过期 build、或本身凭印象填错。**绝不拿旧草稿的渲染器数据/坐标当新三件套骨架**。可复用的只有**通用工具**(本 skill scripts/)——数据每游戏重跑重导。
> 反面教训(ss03 实录):借上一版草稿骨架 → 连击倍率位置错(以为屏顶悬浮条,实为挂转轮框顶栏)、背景资产标错(`Back_*` 是转轮底板非全屏背景)、菜单捏造成常驻底部 5-nav(实为菜单叠层内 TabList)、赔付/设置格式错。根因全是"没在用时回源、借了旧骨架"。

源(构建/服务端)才是 single source of truth;通读代码只用来建**结构骨架**(有哪些屏/子系统),数值**永远 just-in-time 抽取并 cite**,落进三件套 + `work/<code>/` 落盘的脚本与数据(耐用、不随上下文衰减)。

---

## 1. 产物与分工契约(每份只答一个问题)

| 文件 | 只回答 | 受众 | 关键内容 |
|---|---|---|---|
| `ART-AUDIO-<CODE>.md` (ADD) | 长什么样、为何这样设计、玩法如何落到美术 | 美术/音频 agent | **精炼设计文档**:Style Bible、符号集设计、场景分层/模式皮、**玩法→美术适配表**、UI chrome 设计语言、音频触发设计、i18n 策略;只引代表件,**逐文件全量清单在 elements json(§3)** |
| `GDD-<CODE>.md` (GDD) | 什么游戏、什么规则、什么数学 | 写前后端代码 agent | 老虎机数学:**win 机制(payline/ways/pay-anywhere,§4 判定阶梯)**/转轮条/赔付表/scatter+免费触发/wild/倍率/cascade/RTP;回合时序、协议、断线。优先服务端 cite,读不到按 §4 回退。不含美术 |
| `UI-GREYBOX-<CODE>.html` | 每屏每态、东西摆哪、多大、哪一层 | UI 复现 agent + 人 | 数据驱动灰盒:**屏最小覆盖硬清单(§5.0)** + 超屏 SCENES + 三态徽标。坐标全部来自 RectTransform 合成 |
| (伴生,必出) `elements-<CODE>.json` | 机器可读全量:UI 元素 px + **资产逐文件清单** | 下游程序 | `ui_elements`(可见承重件 {x,y,w,h,badge,path})+ `assets`(asset-manifest 全量:file/type/dims/时长/大小/来源组)+ counts 对账 |

**铁律**:三份交叉引用、互不重复。动画时长→HTML;玩法/数学→GDD;资产 origin→ADD。

---

## 2. 总流程(6 阶段)

> **目标函数=最终结果准确**。§0 权威规则、§1 产物契约、§6 校验门禁是"完成"的定义(**不变量**);本节与 §5.1 的管线、§7 的脚本只是当前最优**工具**——可优化可替换,替换后仍须过同一套门禁。

```
阶段0 定位+找CDN+宿主壳屏 → 阶段1 拉包+拆容器+Addressables全量 → 阶段2 UnityPy抽取+穷尽合成
  → 阶段3 视觉+截图+完整性门 → 阶段4 产三件套 → 阶段5 校验
```

### 阶段 0 — 定位 + 找 CDN + 定版本 + 宿主壳屏
1. **认出 Unity 宿主**:`ls ~/harley/<code>` 常多个 repo;UI 判据=`package.json` 依赖含 **`react-unity-webgl`**。两个 UI repo 通常是 Vite 独立版+Next 平台版,都嵌同一个 Unity 包;其余是后端(socket/api/controller),**可能没有**(见 §4)。
2. **找 CDN base**:`bash scripts/find-cdn.sh https://game.<env>.hybergaming.com/<code>` 抓部署 chunk grep S3 base。**回退**:宿主用运行时 `indexConfig`(`public_config/index.config.js`,DevOps 注入)时,直接 `curl <live-host>/config/index.config.js`,或试同 bucket 的 `<code>` 路径。该 code 全 403/无 catalog → 变体可能未部署,记阻塞,别硬造。
3. **锁定线上实际 build(必做)**:`curl <CDN>/unity_game_package/gz/version.json`,以现在实际返回为准。不同 build 玩法/模式会增删——三件套标清版本。
4. **定朝向(易漏)**:grep 宿主 `useGameScale`/`isVertical`/`Background.tsx`;Unity 命名 `Canvas_*_Vertical/_Horizontal`。双朝向两种实现:①响应式重锚(同 Canvas,ss03)②两套独立 Canvas(都在构建,ss02)——compose 后看有没有孪生 Canvas。
5. **宿主壳屏(游戏体外的屏,一并纳入 §5.0 清单)**:**loading/维护 = 宿主 React 组件+CSS**(Unity 未加载时),几何从宿主代码设计空间取,标 host/derived;**入场 START GAME 屏常是平台中间件**(`@hg/middleware-facade` + `useEntry`),不在游戏 repo/Unity——bg/标题用宿主 `Background.tsx`,按钮标"中间件 runtime"(ss02 实录)。顺手记 socket/api 路径、asset_v1。

### 阶段 1 — 拉包 + 拆容器 + Addressables 全量
1. `bash scripts/download-build.sh <CDN_BASE> <code>` → loader/data/wasm/framework + version,gunzip。
2. `python3 scripts/unpack-unitywebdata.py build_<code>/<code>.data` → `.data` 是 `UnityWebData1.0` 容器,拆出 **`data.unity3d`** + `sharedassets*.resource` + `global-metadata.dat` 等。
3. **Addressables 全量(必做,勿抽样)**:`bash scripts/addressables-probe.sh <CDN_BASE> <code>` 拿 catalog(S3 LIST 被拒,catalog 是唯一全集来源,名带 hash)→ **逐 bundle 从两条 base 路径 fallback 下载**:本地包 `<cdn>/addressables_assets/aa/WebGL/<bundle>` 与远程包 `<cdn>/addressables_assets/ServerData/WebGL/<bundle>`,同一游戏两者混用(catalog 里 `{RuntimePath}/WebGL` + `ServerData/WebGL` 两个模板即线索)。
4. **403 存根检测**:下载失败常把 AccessDenied XML(约 240~300 B)存成 `.bundle` 静默混进目录——**<2KB 或含 `AccessDenied`/非 `Unity` 魔数 = 未取到**,记入缺口清单(compose-bundles.py 会自动报警)。ss02 的 localization 包即如此,赔付文案因此无一手 cite(→§4 回退)。
5. **别只凭 data.unity3d 判"屏不在构建"(ss02 重大教训)**:运行时实例化的 UI(设置/弹窗/免费过场/语言/账单)常按**功能 pack** 分 bundle:`ui_settingpage_pack`(设置+Guide+语言+账单)/`ui_popuppage_pack`(Reconnecting/Toast/Warning)/`gameplay_freegame_noticerpack`/`gameplay_winreward_effectpack`/`gameplay_introanim`/`gameplay_decoration(_character_pack)`/`common_textures|shaders|fonts`。**必须拉全+抽全后才能下"在不在构建"的结论**;catalog 也可能全是本地化包(ss03)——两种都见过,别预设。

### 阶段 2 — UnityPy 抽取 + 穷尽合成(核心引擎)
1. `python3 scripts/unitypy-extract.py unpacked/data.unity3d`(**对每个 bundle 同样跑**,各自出目录)→ `art/`(Texture2D/Sprite→PNG)、`audio/`(AudioClip;FMOD 另需 `pip install fsb5`)、`rect_transforms.json`、`monobehaviours.json`(IL2CPP release 常剥 typetree→读空,数学转 §4)、TextAsset(Spine `.atlas/.skel`、csv/json)。
2. **穷尽合成(灰盒数据底座)**:`python3 scripts/compose-all.py unpacked/data.unity3d` 合成**全部 Canvas + 全部独立 prefab 根**→ `all_layout.json`;再 `python3 scripts/compose-bundles.py <bundles目录>` 把全部 bundle 的根并入。**宁可多合成再筛,不可漏**——"未归类"的照进灰盒兜底区(§5.0 ⑧)。
3. **全量资产清单**:`python3 scripts/asset-manifest.py <extract目录> <bundle-extract根>` → `asset-manifest.md/.json`(每文件一行:PNG 真实宽高/音频时长/大小,按来源包分组+计数)。这是 `elements-<CODE>.json.assets` 段与 §6 对账的机械保障(ADD 只引对账数字,§3)。
4. **对象类型普查**作完整性基线:按类型计数 Texture2D/Sprite/AudioClip/AnimationClip/Font/TextAsset/VideoClip/Material——阶段 5 回查"抽了多少/漏了什么"。注意 **Texture2D 可能是图集页,逻辑资产数=Sprite 数**,两者都记。

### 阶段 3 — 视觉门 + 反馈门(可选) + 完整性门
1. **亲自看导出的图**(Read PNG):符号/标题/转轮框/赔付/bonus → 提题材/材质/配色(Style Bible 只能靠看图)。**看 Guide/帮助页贴图与文案**——常含赔付样例/规则真值(这是构建内资产,不是截图)。
2. **反馈门(可选,不阻塞)**:仅当用户能提供真机截图/录屏时,列清单请求(base 旋转态/中奖/大奖/免费触发+进行中/bonus/赔付表/菜单/弹窗,每张说明核对什么),用于**核对已生成结果+升 validated+暴露盲区**。**没有截图不等待、不阻塞**,照常产出(§0 零截图部署)。
3. **完整性门**:catalog 全部 bundle 状态表(下载成功/403 存根/未试);未抽的 bundle 明确"可能含额外美术/屏"。

### 阶段 4 — 产三件套
按 §1 分工。灰盒走 §5.1 数据驱动管线(manifest 驱动生成,勿手写 HTML 逐 box)。数据逐条回源(§0★★)。

### 阶段 5 — 校验(§6,不可省)

---

## 3. ADD 要点(slot art/audio)

- **Step 0 Style Bible**:一句话美学 + 60-30-10 配色(看导出图提) + 材质族 + 不变量(chroma-key/不烧字除 logo/effect 独立)。
- **★ 资产清单分两层(硬规则,2026-07-07 修订)**:①**ADD 内=主体资产清单**——**逻辑资产**逐行(资产|类型|尺寸或时长|分类|位置|说明),覆盖全部主体件(各类图/音/视频);**组合类非主体信息折叠为族行**(序列帧、图集页、多语言变体、同名双导出→一行+说明×N 件),分清主次:不漏主体、不过度抓取(逐帧/逐语言罗列=不合格,ss03 首版 935 行即反例);**按类拆子表呈现**(符号/场景与世界板/HUD/菜单历史/入场/演出庆祝/Guide/弹窗通用/引擎内部/音频…),勿一张大表,各子表带行数与件数小计。②**elements json `assets` 段=逐物理文件机器全量**(asset-manifest 原样)。**对账**:主体族行 member 合计 == elements assets 行数 == manifest 机扫,差一个都要解释(§6)。ADD 正文另必配**「玩法→美术适配」**一章(每条玩法机制 ↔ 演出资产链)——穷尽阅读是为了理解设计。抽取工件(rect/mono json)不是资产,哪里都不进;引擎内部纹理(LUT/SMAA/字体图集页)归"引擎内部"族一行带过。
- **slot 资产分类**:符号集(高低分+wild+scatter+金牌)、转轮框/网格、**背景分层**(见下)、赔付表 UI、免费/bonus 场景、倍率/combo/anticipation、中奖庆祝分级、Spine(`.atlas/.skel`+图集页,判孤儿前看 `.atlas`)、粒子、**字体**(common_fonts/TMP 图集)、UI 九宫格件。
- **背景是分层的,别当一张全屏图(ss03 实录)**:场景背景(全屏 `Background_*`)+ 转轮底板(`Back_*`=FrameBG,牌网后)+ 上/下延展条 + 世界 VisualMask。用 **SpriteRenderer→sprite→GameObject 映射**核实每张图挂在哪。**超视口的全幅背景(如 2048² 对 1080×1920)在灰盒单独出 SCENE 卡**(§5.0 ⑦)。
- **来源标注**:in-build(data.unity3d) vs 哪个 Addressables bundle;原生尺寸 vs 上屏渲染尺寸。
- **音频**:全部 AudioClip 入清单;触发表(spin/reel-stop(可能逐符号)/win-tier/anticipation/free-spin 流程/UI click/BGM base+free)。触发关系取自 AnimatorController/MonoBehaviour 或截图录屏;**时长可从 AudioClip 与 AnimationClip(引擎类型,可读)直接抽,标 extracted**;精确编排无源时标 derived。

## 4. GDD 要点(slot math)

- 内容:win 机制、转轮条、符号权重、赔付表(每符号×档位→倍率)、scatter 触发免费(几个触发/给几转/retrigger)、wild/金牌/倍率/cascade、Buy/Double-Chance 价格、回合时序。**不写美术**。
- **★ win 机制判定阶梯(ss02 实录)**:payline vs ways vs **pay-anywhere(scatter-pays,任意位置同符号计数,如 8-9/10-11/12+ 档)**——①服务端 repo(最优)②**运行时 Guide 帮助页**(明示计数方式/公式/档位 → validated)③构建暗示(有无 payline 渲染节点等,只够 derived 方向)。别拍脑袋。
- **★ 服务端 repo 常能一手直读(优先,别默认黑箱)**:数学往往完整躺在 socket/api repo——`symbol.json`(赔付)、`Const`(行列/倍率梯/scatter→免费映射)、`SpinUtils`(可见窗/金牌列限)、`SpinService`(派彩公式/cascade)、`*.proto`、`BetConfig`。逐条 cite file:line。只有二进制加密(如 `*.script` 转轮序列)才标"未解密,server 权威"。
- **★ 无 server repo / 本地化不可达的回退(ss02 实录)**:`~/harley/<code>` 只有 UI 宿主、且赔付文案在 localization bundle(403)→ 若恰有运行时 Guide 页截图可用,数学值以它为 validated 依据,并明确"localization/server 未取到一手 cite";**零截图运行时,该分支输出"结构完整 + 数值标 server-authoritative 未证",宁缺勿编**。RTP/权重/概率永远标 server-authoritative。**几何照旧只从构建 compose,绝不量截图。**
- **换皮(reskin)文档只可信"机制结构"**:变体 repo 的 `ai/*.md` 可参考机制骨架(触发数/bet 档/win 分级/协议事件),但**具体数值/网格/赔付常是母游戏遗留**(ss02a 文档写 5×3/25-line + SS03 赔付,实测 ss02 构建是 6×5 pay-anywhere)。网格/符号/赔付一律以目标 code 自己的构建为准。
- **config-gated 功能**:客户端代码里有、被 AppConfig 关掉的功能(Exit tab 等)在 GDD 注明存在性与门控条件。
- ⚠️ mock-vs-real:客户端只演出下发 result;别把 mock/占位当真值。MonoBehaviour 读不到时别硬啃 typetree(除非必要),数学走上面阶梯。

## 5. UI-GREYBOX 规格(slot,自包含)

单文件自包含**数据驱动灰盒**:全部 box 从 `all_layout.json`(构建合成)渲染,带标注彩色矩形(线框,不贴位图),用于标位置/尺寸/层级。

### 5.0 屏最小覆盖硬清单(缺一类=不合格)
① **Loading**(宿主 React 壳;来源=宿主 repo CSS,badge host/derived)
② **入场/START GAME**(平台中间件,若存在;bg/标题=宿主,按钮=中间件 runtime)
③ **玩法主页面以【屏】为单位,别切碎 UI**:全部 UI 层(HUD/横幅/屏顶提示等各 UI Canvas)按 z 序**合成一帧整屏**,每**态**一帧(base/free spins/…);**只有 game content(世界空间板/独立渲染域,如 ss02 世界 `GameBoard`、ss03 世界转轮)按代码分离单独出卡**(几何走 §5.3),并在整屏帧里以轮廓 ghost 标出其占位——HUD/按钮/弹窗不要各自成卡;**朝向按构建证据定**:有 `_Horizontal` 孪生 Canvas 才双朝向各一套(ss02);竖屏设计游戏(UI 全是固定竖版 board、无孪生 Canvas,如 ss03)只出竖屏帧,横屏行为**按该游戏实际证据如实描述**(board 如何摆、两侧/上下由什么填充——背景拉伸/黑边/裁切,各游戏不同)写 notes,勿造横屏投影帧
④ **玩法衍生态**:free spins(过场 noticer + 进行中计数/倍率)、bonus、大奖庆祝
⑤ **Settings 及衍生**:设置各 tab 内容、Guide/赔付、历史、语言选择
⑥ **弹窗/辅助窗口**:Reconnecting/Toast/Warning/退出确认/选注面板/账单详情
⑦ **超屏 SCENES(任何"比视口大/超出显示"的内容单独成卡,data-scene)**:滚动长纸(如 Guide 12800px 高)、账单详情折叠下方内容、**滚动/全幅背景**(全幅画出+叠一个视口示意框)、reel strip 全条、全符号集
⑧ **其它 prefab/特效兜底区**:穷尽合成里没被分区认领的自动归"未归类"——**宁可多不可漏**

### 5.1 数据驱动管线(标准做法,勿手写 HTML 逐 box)
```
compose-all.py → compose-bundles.py → all_layout.json(穷尽)
  → 手写 greybox-manifest.json(游戏特定:exclude/分区 sections/inject/badges/scenes/bleed 名单)
  → gen-greybox.py → UI-GREYBOX-<CODE>.html → greybox-check.js → 越界分诊循环(见下)
```
- **manifest(游戏特定,每游戏现写,勿抄上一游戏)**:`inject` 补合成之外的屏(宿主 loading、世界空间实测复刻、超屏 scene 卡);`sections` 按 §5.0 排;`badges` 覆盖默认;`scenes`/`bleed` 见分诊。
- **★ inject 节点几何必须带换算式并复算**:注入节点是灰盒里唯一不经 compose 保护的坐标,且 greybox-check 抓不到"界内放错位"。CSS 中心锚(`left:X% + translate(-50%,-50%)`)最易错——X% 是**中心**不是左缘,x/y 两轴都要减自身一半(ss03 实录:y 轴减了、x 轴没减,loading 条整体右偏 390px);`right:` 定位、`transform-origin`+scale 同理。每个 inject 节点在构建脚本里写明换算式,交付前逐节点对照源码 CSS 重算(§6)。
- **渲染器契约**:每 box 写 `data-box="x,y,w,h"` + `data-role`(含 offscreen/bleed 标记);每 `.stage` 带 `data-w/data-h`(逐帧参考分辨率,竖横混排逐帧判);scene 卡 `data-scene="1"`。控件:结构容器/非激活态/尺寸/名称开关。**占位**:余额/赢分/注额/订单号等运行时值一律 `<占位>`,别烧截图数字。
- **★ 越界分诊循环(每个越界必须归入且仅归入一类,有依据)**:
  - (a) **滚动内容**:祖先链含 Viewport/ScrollView/ScrollContents/Scrollbar → 自动 `offscreen:scroll` 放行(要求 compose 存**完整路径**——截断路径会漏判祖先,已内置);
  - (b) **双朝向共用盖板/巨型 Mask**:`ScreenBoard`(1920×1080 居中于竖屏)/`Veil`/10000² `Mask` 等 → 逐个核实后加进 manifest `bleed` 名单;
  - (c) **出血装饰**:底边 Strip 等故意越出 → `bleed`;
  - (d) **布局组塌陷**:0 尺寸件自动跳过(其静态位置无意义,单件 px 标 derived);
  - (e) **真问题**:以上都不是 → 回构建核查(挂错父?合成 bug?屏外驻留的滑入面板?)——修数据或注明"待截图核实",**不许无依据放行**。
- **假阴性防护**:`data-box` 总数=0 → 检查器直接 FAIL(说明渲染器没写检查属性,越界检查在空转。ss02 曾因此"0 越界"实为"0 检查")。

### 5.2 SCREENS vs SCENES —— 按【代码结构】判定,别拍脑袋(ss03 实录)
- **屏(SCREENS)= 一块 Canvas / 一个视口态**:主玩法(base/free 常共用 Canvas)、菜单叠层、弹窗;宿主壳另有 loading/入场/维护。
- **菜单常不是"多个屏",而是【一块 Canvas + TabList tab 切换内容】**:设置/赔付/历史 = 同一 `Canvas_GameSetting_*` 里 `TabList` 切 `ContensPanel`。**nav 从 TabList 子节点找**(如 Back/Setting/Guide/History/Exit,Exit 可能 config-gated),别捏造常驻底部 nav;菜单叠层的 nav 不在主玩法 Canvas 上(grep 确认)。
- **场景(SCENES)= 超屏可滚内容 或 按需实例化 prefab**:赔付长纸、单注详情(经历史 tab 进入)、reel strip 全条、全幅背景。**按需 prefab 的根不在静态 Canvas 下**(运行时实例化)——查入口路径(⚙→历史→点注单)+服务端支撑(BetHistory API)佐证,归 SCENES 标清。

### 5.3 坐标合成(必踩的坑,脚本已封装)
- **坐标 = RectTransform 锚点(相对父级)+anchoredPos+sizeDelta+pivot 沿层级合成**,受 CanvasScaler 参考分辨率约束。**用 scripts(compose-all/compose-layout),别手算别目测**。参考分辨率:CanvasScaler MB 常被剥,按 Canvas 名后缀(`_Vertical`=1080×1920/`_Horizontal`=1920×1080)+宿主 CSS 定,能读 MB 时以 MB 为准。
- **从 Canvas 的【直接子节点】在干净 (0,0,W,H) 帧合成**——别拿 Canvas RT 自身当根(中心 pivot,会带 −W/2,+H/2 偏移)。
- **可见性看 CanvasRenderer 存在性,不看 Image/Text MB**(IL2CPP 剥 typetree→MB 读空,但 RT+CR 照样可读,全套布局都在构建);**有效可见还要求自身与全部祖先 act=true**——act=false 的默认隐藏态照画(半透),别当可见断言。
- **z 序**:同 Canvas 内=兄弟顺序(后画者在上);跨 Canvas=Canvas sortingOrder(可读时);灰盒 z 引用此,不拍脑袋。
- **布局组(Horizontal/Vertical/GridLayoutGroup)驱动的子件静态读 0×0**:tab 项/列表行单件 px 是运行时排布;容器框可 extract,单件按均分示意标 derived,别捏造精确 px。
- **世界空间游戏板(转轮/连击/倍率横幅/盘龙)= runtime 重排,静态世界坐标≠屏幕 px**:相机正交、板件静态坐标远超视野,`useGameScale` runtime 重定位。**别投影世界 Transform 当屏幕真值**:①优先找 **UI 复刻件**(帮助/单注详情页常有 `ScenarioGrid` 的 RectTransform 版=屏幕真值)定块宽/边距/错列/单元格;②世界 feature 件**先查父链定挂点**(如连击显示挂 `FrameFence/TopFence`=转轮框顶栏,非屏顶悬浮条),on-screen 形态用 UI 复刻件,屏幕 y 标 derived;③其余按比例摆标"投影估算 derived"。

### 5.4 slot 专项
- **可见窗未必规整 N×M——先查错列**:每列可见格数从 UI 复刻件 `ScenarioGrid/Reel_n/SymbolCell_*` 数(世界 `Reels/Reel_n` 只给列数);服务端 `Const`/`SpinUtils` 也给。ways=各列可见数之积(如 4·5·5·5·4=2000),与 banner/服务端互证。
- **符号原生尺寸常=单元格尺寸**(1:1 上屏),核对 `ScenarioGrid` 单元格 vs `Symbol_*` PNG。
- **赔付长纸格式**:First Symbol 特写 + Symbol×Odds 行×N + 规则段;赔率值走 §4 阶梯(服务端>Guide)。

### 5.5 jsdom 自检契约
`NODE_PATH=<jsdom所在> node scripts/greybox-check.js <html> [默认W] [默认H]`:渲染+报 JS 错/data-box 计数/越界(逐帧 data-w/h 判)/放行数/0 尺寸数。**通过标准:0 JS 错 + data-box>0 + 越界全部分诊完(§5.1)**。

---

## 6. 校验清单(阶段 5,逐条回查)
- [ ] **每个承重数值能 cite 到来源**:坐标→compose 某节点;资产→导出文件;数学→服务端 file:line 或 Guide(注明无一手 cite)。cite 不出的标 derived。
- [ ] **未借旧草稿骨架**:承重值全部本次回源重导(§0★★)。
- [ ] **资产对账(全量在 elements)**:`asset-manifest.json` 游戏资产计数(图/音频,分 data.unity3d 与每个 bundle)== `elements-<CODE>.json.assets` 行数 == ADD 对账小节所引数字;Sprite vs Texture2D 计数都留;抽取工件(rect/mono json)不入清单;背景/连击/菜单等易错件用 SpriteRenderer/父链核实过。
- [ ] **Addressables 对账**:catalog 全部 bundle 状态表(成功/403 存根/未试);存根与未抽的明确记缺口"可能含额外美术/屏"。
- [ ] **屏覆盖对账**:§5.0 ①~⑧ 逐项打勾;UI 以整屏为单位、每态一帧(勿切碎);game content 代码分离则单独出卡+主屏内 ghost 占位;朝向按构建证据(孪生 Canvas 才出横屏,竖屏游戏只出竖屏+notes 如实描述);超屏内容都有 SCENE 卡。
- [ ] **布局抽查**:关键帧坐标对照 compose 输出重算;世界件查过父链;布局组子件标 derived 未捏造。
- [ ] **inject 节点逐个复算**:每个注入节点对照源码 CSS/常量重算(中心锚 translate(-50%)/right 定位/scale origin 逐项过,§5.1★)——检查器抓不到界内错位,只能靠这一条。
- [ ] **数学走了判定阶梯**:服务端直读优先;Guide validated 注明;换皮文档数值未采信;config-gated 已注明。
- [ ] **jsdom 自检过**:0 JS 错 + data-box>0(防空转假阴性)+ 越界全分诊(每条放行有依据)。
- [ ] **重写/重构后 diff 旧元素清单**(防静默丢件)。
- [ ] **徽标严格自洽**:validated 仅当该态有截图;解出未截图=extracted;投影/运行时排布/未证=derived。**零截图运行=全 extracted/derived,不因此缺屏缺件**。
- [ ] 三件套交叉引用无悬挂、无重复;build 版本标清。

## 7. 复用脚本(在 `scripts/`,按路径直接跑,不读进上下文)

| 脚本 | 用途 | 跑法 |
|---|---|---|
| `find-cdn.sh` | 从线上部署 chunk 找 CDN(S3)base | `bash scripts/find-cdn.sh https://game.<env>.hybergaming.com/<code>` |
| `download-build.sh` | 拉+gunzip Unity 包 | `bash scripts/download-build.sh <CDN_BASE> <code>` |
| `unpack-unitywebdata.py` | 拆 `.data`(UnityWebData1.0)→data.unity3d 等 | `python3 scripts/unpack-unitywebdata.py <code>.data` |
| `addressables-probe.sh` | 探 catalog,枚举全部 bundle | `bash scripts/addressables-probe.sh <CDN_BASE> <code>` |
| `unitypy-extract.py` | 解 data.unity3d/bundle→贴图/音频/RT/MB/TextAsset | `python3 scripts/unitypy-extract.py <档>` |
| `compose-layout.py` | 单 Canvas/子树交互式合成(探查用) | `python3 scripts/compose-layout.py <档> [Canvas名 \| --node 节点名] [W H]` |
| `compose-all.py` | **穷尽合成**全部 Canvas+prefab 根→all_layout.json | `python3 scripts/compose-all.py <data.unity3d> [--ref W H] [--out …]` |
| `compose-bundles.py` | 全部 bundle 根并入 all_layout(**含 403 存根检测**) | `python3 scripts/compose-bundles.py <bundles目录> [--master …]` |
| `asset-manifest.py` | **全量资产清单**(逐文件尺寸/时长/大小,分组计数) | `python3 scripts/asset-manifest.py <extract根…> [--out …]` |
| `gen-greybox.py` | manifest 驱动生成灰盒 HTML(渲染器契约内置) | `python3 scripts/gen-greybox.py --layout … --manifest … --out …` |
| `greybox-check.js` | jsdom 自检:JS错/越界(逐帧)/放行/0尺寸/**假阴性防护** | `node scripts/greybox-check.js <html> [默认W] [默认H]`(需 jsdom,可 `NODE_PATH=` 指) |

> 依赖:`pip install UnityPy`(音频 FMOD 另需 `fsb5`;注意装进实际使用的 python 版本);`npm i jsdom`;`ffprobe` 可选(音频时长)。小抄:找世界件挂点/背景归属,用 UnityPy 走 Transform 父链或建 SpriteRenderer→sprite→GO 映射。

## 8. 踩过的坑(按主题分组;【源】= 实录出处)

**A. 定位与来源**
1. 前端 repo 不含游戏——React/Next+`react-unity-webgl` 宿主,0 张游戏图;真游戏在 CDN Unity 构建。
2. CDN 在部署 chunk 硬编码或运行时 indexConfig(两种都有,§2 阶段0)。
3. 以线上 version.json 现值锁 build;模式随 build 增删。【ss03】
4. 双朝向别默认单屏:响应式重锚(ss03)或两套 Canvas(ss02),compose 后看孪生。
5. reskin 家族(ssNN+ssNNa/b):同框架换皮,先出基底完整三件套,变体做 delta;**换皮文档只可信机制结构,数值/网格是母游戏遗留**(ss02a 写 5×3 实为 6×5)。【ss02】
6. 无 server repo 的 code:数学标 server-authoritative,走 §4 Guide 回退,数值别编。【ss02】
7. loading=宿主 React、入场 START GAME=平台中间件:都不在 Unity 构建,屏清单要含,来源标宿主/中间件。【ss02】

**B. 容器与 Addressables**
8. `.data` 是 UnityWebData 容器,先拆再喂 UnityPy。
9. S3 LIST 被拒,bundle 全集只能靠 catalog(名带 hash)。
10. **bundle 两条 base 路径**(aa/WebGL 与 ServerData/WebGL)逐个 fallback;**403 存根**(~250B AccessDenied XML)会静默混进目录,必检。【ss02】
11. **别只凭 data.unity3d 判"不在构建"**:运行时 UI 按功能 pack 分 bundle(settingpage/popuppage/freegame_noticer…),必须拉全抽全;catalog 也可能全是本地化(ss03)——两种都见过,别预设。【ss02 重大】
12. Addressables 可能有真美术包(common_textures/shaders/fonts),抽或标缺口。【ss02】

**C. 布局合成**
13. 布局=锚点相对值沿层级合成(脚本算,勿目测);Canvas 中心 pivot 偏移已封装。
14. 可见性看 CanvasRenderer,别因 Image/Text MB 读空判"UI 纯 runtime"(IL2CPP 剥 typetree)。
15. 布局组子件静态 0×0:单件 px 运行时,标 derived 别捏造;其非零子孙可能停在无意义静态位。
16. 世界板 runtime 重排:别投影世界 Transform;用 UI 复刻件(ScenarioGrid 等)定比例;世界件先查父链定挂点(连击挂 TopFence 非屏顶)。【ss03】
17. 可见窗先查错列(SymbolCell 逐列数),ways=各列之积。【ss03】
18. **compose 要存完整路径**:滚动祖先(Viewport/ScrollContents)判定沿全链;截断路径会漏判,越界误报。【本轮】

**D. 屏与场景**
19. 菜单=一块 Canvas+TabList 切换,nav 从 TabList 子节点找(可能 config-gated);别捏造常驻 nav。【ss03】
20. 屏 vs 场景按代码结构:按需 prefab 根不在静态 Canvas 下,查入口路径+服务端佐证。【ss03】
21. **超屏内容显式建模**:滚动长纸/折叠内容/全幅背景/双朝向盖板(ScreenBoard/Veil/巨 Mask)/出血装饰——每类在灰盒有明确处理(scene 卡/offscreen/bleed),越界分诊不许无依据放行(§5.1)。【本轮】
22. game content(世界空间/独立渲染域)与 UI 分离时:game content 单独出卡(几何走 §5.3),UI 整体仍以屏合成、不互拆(§5.0③)。【ss02/ss03】

**E. 资产**
23. 背景分层,`Back_*`≠全屏背景(是转轮底板);SpriteRenderer→GO 映射核实挂点。【ss03】
24. Texture2D 可能是图集页:逻辑资产=Sprite;两个计数都留。
25. AnimationClip/AudioClip 是引擎类型,IL2CPP 剥不掉——时长/事件**可读可 cite**,别全推给截图。
26. **全量清单进 elements json,ADD 保持设计文档**:705 张图只列 27 行=不合格(ss02),935 行全贴进 ADD 附录也不合格(ss03)——机器清单归 `elements.assets`(asset-manifest 机械保障+计数对账),ADD 精讲设计意图+玩法→美术适配。【ss02/ss03】

**F. 数学**
27. 老虎机数学/RTP 几乎都在服务端,客户端只演出;mock 别当真值。
28. 服务端 repo 能直读就逐条 cite;win 机制走判定阶梯(服务端>Guide>构建暗示)。【ss02】

**G. 方法论与诚实**
29. 即时回源+落盘,勿靠长上下文召回、勿借旧草稿骨架(§0★★)。返工根因几乎都是"凭印象/借旧骨架"。【ss03】
30. 谁都会错且会过期:脚本会漏、注释会旧、上一版更正也会过期——回一手源重核,跑 §6。
31. 徽标诚实:解出≠核过(extracted≠validated);代码是运行时超集,config-gated 注明。【ss02】
32. **自检要防"空转"**:检查器跑通≠检查生效(data-box=0 时"0 越界"是假阴性);任何门禁先验证它真的在咬合。【本轮】
33. **代码是唯一真实信源**:截图只是可选反馈回路(核对结果/升徽标/暴露盲区),生成结果永远回代码;几何绝不量图;**部署形态=零截图,无截图必须照常出齐全部产物**。【ss02 用户硬规则】
34. **朝向按构建证据**:竖屏设计游戏(固定竖版 board、无 `_Horizontal` 孪生)勿造"横屏投影帧"——横屏行为按该游戏实际证据描述(填充方式各游戏不同,勿把某一款的"背景拉伸"当通则),notes 说明即可;硬投影出的帧全是越界噪声。【ss03】
35. **"怪位置"先复核 anchor 再怀疑 compose**:HUD 子件锚屏顶(aPos.y 大偏移把件推到 y25)、屏外驻留滑入面板(anchor+aPos 停在 x>W)都可能是真实设计——回原始 RectTransform 手算确认,别当 bug 修、也别急着 bleed 掩盖。【ss03】
36. **UI 勿切碎,以屏为单位**:HUD/横幅/提示各自成卡=碎片化不直观;UI 层合成整屏、每态一帧,只有 game content/场景按代码分离(§5.0③)。数据全对仍可能"看着不对劲",根因常是缺整屏视图。【ss03】
37. **inject 手算几何=高危区**:CSS 中心锚 `left:X%+translate(-50%,-50%)` 的 X% 是中心不是左缘,两轴都要减半宽/半高——漏一轴就整体偏移且检查器不报(界内);inject 节点必须带换算式+逐个对照源码复算(§5.1★/§6)。【ss03 实录:loading 条右偏 390px】

## 9. 输出位置 & 命名
本 repo(`~/harley/ai_whole_pipeline/ai-reverse-skills`)根下 `output/<code>/`:`ART-AUDIO-<CODE>.md` / `GDD-<CODE>.md` / `UI-GREYBOX-<CODE>.html`(+必出 `elements-<CODE>.json`:`ui_elements`+`assets` 两段)。`<CODE>` 大写。**`output/` 是交付物,git 跟踪**;中间产物(build 下载/unpacked/extract/bundles/all_layout/manifest)放 `work/<code>/`(gitignored,可由 scripts 从 CDN 重新推导)。

> 安装为可 `/` 调用的 skill:把本目录复制到 `.claude/skills/reverse-unity-game-to-triad/`;或直接让 Claude "按 skills/reverse-unity-game-to-triad/SKILL.md 提取 <游戏>"(本 skill 家在 `~/harley/ai_whole_pipeline/ai-reverse-skills/`)。判据:repo 依赖含 `react-unity-webgl` → 本 skill(Unity 编译构建游戏)。
