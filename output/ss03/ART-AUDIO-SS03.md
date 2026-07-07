# ART-AUDIO-SS03 · Mahjong Streak(麻将连莊)美术与音频设计文档(ADD)

> **版本锚定**:Unity 构建 `1.0.0-56`(CDN `dev-assets-hybergaming/ss03`,`version.json` 2026-03-26,2026-07-07 复核一致)。
> **信源**:资产由 UnityPy 从 `data.unity3d` + 29 个 localization bundle 全量导出后**亲自查看**归纳;尺寸=导出 PNG 真实像素,时长=AudioClip 元数据。零截图形态,徽标止于 extracted/derived。
> **定位**:本文是**设计文档**——讲清楚"长什么样、为什么这样设计、玩法在美术上如何落地",并附**主体资产清单**(§8,逻辑资产 258 行:尺寸/类型/分类/位置/说明;序列帧、图集页、多语言变体等组合件折叠为族行)。**逐物理文件机器清单(875 件)在 `elements-SS03.json.assets`**。玩法/数学 → `GDD-SS03.md`;屏坐标/层级 → `UI-GREYBOX-SS03.html`。

## 0. Style Bible

- **一句话美学**:翡翠赌桌上的鎏金麻将馆——白玉麻将牌为主角,金元宝与朱红漆木点缀,富贵吉庆的中式新春质感。
- **60-30-10 配色**:60% 深翡翠绿(桌面/背景);30% 象牙白+暖金(牌体/金符/元宝);10% 朱红/群青点缀(雕纹、底板、免费模式栏杆)。
- **材质族**:抛光白玉(牌面,柔高光+浅浮雕)、鎏金浮雕(金符/元宝/龙)、漆木描金(围栏/底板)、雾面绒布(桌面)。
- **不变量**:
  - 雕纹三原色语义固定:绿=發/条子系,红=中/万字系,蓝=白板/筒子系;白牌与金牌雕纹形状不变,只换牌体材质。
  - 文字不烧进美术,**例外全部是按语言出图的文字图**(9 语言分 bundle):游戏 logo、win 三级标题、免费公告套件、WILD/百搭、开始。
  - 特效(爆炸/光效/序列帧)独立资产,不与符号底图合并;运行时数值(余额/注额/赢分/单号)一律占位渲染。

## 1. 符号集设计(23 格牌网的主角;原生 184×224 = 单元格 1:1 上屏)

9 种麻将牌 × 白/金双版本 + 胡(Scatter)+ 百搭(Wild):

| 牌 | code(GDD) | 白版/金版代表件 | 设计要点 |
|---|---|---|---|
| 發 / 中 / 白 | 0/1/2(高赔三元牌) | `Symbol_0_fa_white`→`_gold` 等 | 大字浮雕居中,绿/红/蓝三色分明 |
| 八萬 | 3 | `Symbol_3_bawan_*` | 蓝"八"+红"萬"双色 |
| 五筒/五條/三筒/二筒/二條 | 4-8(低赔筒条) | `Symbol_4_wutong_*` 等 | 筒=同心圆点阵,条=竹节,红点缀区分档位 |
| 金版 GA-GI | 100-108 | `*_gold` ×9 | **白牌换鎏金牌体+底缘金元宝徽**;赔付与白牌相同(GDD §2.2),金的意义在"消除后变百搭" |
| 胡(Scatter) | 201 | `Symbol_Scatter_Hu`+`Symbol_Scatter_Bg` | 立体红金"胡"字+圆形鎏金纹章底,全牌网唯一非牌形符号 |
| 百搭(Wild) | 202 | `Icon_Wild` 192×215 | 金元宝+WILD/百搭立体字(中英两版文字图) |

配套派生:`SymbolPattern_[0-8]`(纯雕纹无牌体,供爆炸/Guide/听牌演出用);`white/gold_original_mahjong`(素牌底,爆炸序列基牌)。

## 2. 场景分层与三套模式皮

**背景不是一张图,是"全屏背景 + 转轮底板 + 上下延展条 + 双栏围栏"的分层系统**(挂点已用 SpriteRenderer→GameObject 父链核实):

- 全屏层:`Background_BaseGame`(1024²,翡翠桌面+金币元宝山,世界相机拉伸至全幅)。
- 底板层:`Back_<模式>`(576×1024,牌网正后方竖板)+ `_Top/BottomTexture` 延展条——**`Back_*` 不是全屏背景**。
- 围栏层:`Frame_TopFence`(1080×340,顶梁,**内嵌连莊倍率灯位**)+ `Frame_BottomFence`(1040×120),两端龙首衔珠。
- **三套模式皮整套联动切换**:Base(朱红底板+橙红栏)/ FreeGame(紫檀盘柱+群青栏)/ **PityFreeGame(紫青变体——构建存在第三套皮,服务端协议未见对应模式,标 server/config-gated 存在性)**。

## 3. 玩法 → 美术适配(本游戏最重要的设计逻辑)

每条玩法机制都有一条专属演出资产链(玩法定义见 GDD 对应节):

| 玩法机制(GDD) | 美术落地 |
|---|---|
| 级联消除(§4) | 中奖牌爆炸序列帧两套:`MahjongExplode_Normal/Gold`(0001-0020 旋转爆裂);上方牌落下补位,落牌配逐符号语音 |
| 金符→百搭转化(§5) | `BaidaAppear/BaidaExplode`:金牌原位翻出金元宝序列(yuanbao00-11)+WILD 字样——金符不消失而"变身"的视觉锚点 |
| 连莊倍率(§4) | 倍率灯 x1/x2/x3/x5 **做在 TopFence 围栏顶梁里**(世界节点 MatchComboDisplay 挂 TopFence,非屏顶悬浮条);免费模式同位显示 x2/x4/x6/x10;每档配升档语音 |
| 胡触发免费(§6) | 胡三态 prefab:`Scatter_HuIdle/HuAppear/HuExplose`(待机脉光/现身/爆开)+"胡啦"语音;差一胡时 `NearMiss_*`:压暗幕+中排描边+慢转演出(6.43s 长音效配套) |
| 免费旋转(§6) | 开场 `FreeSpinNoticer`(金龙盘绕公告+You Have Won N Free Spins+START 钮);结算 `FreeSpinNoticer_EndFreeGame`(龙+元宝山+TOTAL WIN);过场幕布 ScreenCurtain 三片屏外平移入场;转轮框换 `FreeSpin_Prefab` 顶饰+高亮 |
| 免费 reel3 全金(§5) | Timeline 信号 `MidasMiddleReel_Signal` 驱动第 3 轮金化演出 |
| 中奖分级庆祝(§9) | 三级:大奖(`win_big_title`)→巨奖(`win_mega_title`)→超级巨奖(`win_super_title`),黑幕+白描龙纹环旋转+标题+数字滚动;**prefab 名与贴图交叉(SuperWin_Prefab 用 win_mega 图、MegaWin_Prefab 用 win_super 图),复现以贴图语义为准**;行内小奖另有 lv1-3 框与升级过场 |
| 长按查赔付(GDD §3) | 世界浮层 `SymbolDetailPanelManager` + 红木纹 `PlayerHUD_Symbol_DetailPanel(_Long)` |
| Spine 盘龙 | `dragon`/`skeleton` 两套骨骼(TextAsset:各带 .atlas),金龙盘绕大演出,配 `Dragon Appear` 2.68s |

## 4. UI chrome 设计要点(坐标全在灰盒,此处只讲设计语言)

- **HUD(竖屏底带)**:翡翠圆形 Spin 主钮(金框,Auto 态换方芯+局数),左右四小钮(设置/注额/自动/快速,快速钮带两颗档位灯);钱包条 Balance/Win 双栏+金币/钱袋 icon;**屏顶另有细提示条 TopHint**(HUD 子件锚屏顶,构建原值 y25);**屏外右侧驻留 PlayControlPanel(x1055)滑入面板**。免费模式 HUD 换深色变体+剩余次数大字计数。
- **菜单叠层**:一块 Canvas,底部 TabList 五键(Back/Setting/Guide/History/Exit,runtime 排布);设置页=分区卡(BGM/SFX 各 4 档拨钮、语言行、隐藏的画质三挡);History 页=Summary 三栏+Today/3日/周 tabs+滚动账单列(`BetItem` 行,win 态换金底);单注详情=回合复盘页(倍率 4 槽+ScenarioGrid 牌网复刻+公式行)。
- **弹窗族**:统一 960 宽深色面板+金字+单钮(Reconnecting 加载圈/Toast 条/Warning 面板);选注面板=底部滑入 4×3 档位钮阵;语言选择=Veil+800×960 面板 9 语言行。
- **Guide 长纸**(972 宽,~11.5k px):赔付特写(發 3|10 4|25 5|50)→ 全符号赔率 → 2000 Ways 示意 → 金符/免费/倍率插图 → 规则文与 UI 图例——插图 en/zh 双套。

## 5. 音频设计(41 clips:BGM 2 + SFX 39;全清单在 elements json)

- **双轨 BGM**:base `NormalGame`(98s 循环)/ free `FreeGame`(23s 循环,加速变奏)。
- **触发设计**(与玩法逐一对位):
  - 交互:Click Button/Spin/Mahjong、Start Button、Free Spin Confirm(0.16-0.81s 短促)。
  - 转轮:Mahjong Land(每列落定 0.12s)、Mahjong Shaking(听牌慢转 1.52s)、NearMiss(6.43s 全程)。
  - 结算:Mahjong Match(消除)、Winning Calculation(59.8s 赢分滚动循环,可中断)、Winning End、Total Win Message。
  - **逐符号落定语音**(9 支,0.45-1.24s):高赔牌落定时报牌名(Green/Red Dragon、Eight Man、Five Dots…)。
  - **倍率升档语音**:x1/x2/x3/x5(base 梯)+ x4/x6/x10(free 梯),数值越大越亢奋。
  - 免费流程:Scatter Appear、Ma Jiang Hu La(胡啦!)、Transition/Charge/Calculate/ComboDisplaySwap/End 成套。
  - 特效:Wild Yunbao Appear、Dragon Appear;彩蛋语音 Quan Zhong 男/女声(触发条件客户端资产层不可证,derived)。
- 触发关系为资产名+prefab 挂点推定(derived);时长为元数据(extracted)。

## 6. i18n 资产策略

9 语言(en/zh-hans/zh-hant/vi/id/ko/th/hi/ms),文字图按语言分 Addressables bundle(win 三级标题×2 尺寸 + 免费公告套件,典型 16 张/语言;id 与 ms 共用 `id_and_my` 套件,另有 shared 组 14 张跨语言共用);TMP 文案走 string-table(en 表 126 条,含全部规则文案);字体 AlibabaPuHuiTi。运行时按宿主注入的 LocaleKey 加载。

## 7. 宿主壳美术(不在 Unity 构建;S3 `asset_v1` / 中间件 `ui-assets`)

loading 三件套(Track/Bar/Tip,进度用 clip-path)、`loadingBg_large` 2560² 全幅底、三语言 loading logo、开屏视频 `PA_logo_en.mp4`(仅平台 1)、Exit 钮、Notice 面板套件、字体 ttf。几何与 cite 见灰盒 §①⑥。

## 8. 主体资产清单(逻辑资产 258 行 / 875 件,分 10 子表)

> 行=**逻辑主体资产**;序列帧/图集页/多语言变体/同名双导出折叠为**族行**(说明列注 ×N 件);
> 逐物理文件(875 件含每帧/每语言/每页)见 `elements-SS03.json.assets`。尺寸=最大变体真实像素。

### 8.1 符号集(31 行 / 67 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| Icon_Wild | 图 | 192x215 | 符号·百搭 | 牌网 | Wild 元宝(中英文字版) |
| Icon_Wild_Zh | 图 | 192x224 | 符号·百搭 | 牌网 | Wild 元宝(中英文字版) |
| 符号纯雕纹版(9 种,演出/Guide 用) | 图 | 184x214(等2种) | 符号·雕纹 | 演出/Guide | ×9件 |
| Symbol_0_GreenDragon | 图 | 194x234(等2种) | 符号 | 牌网/演出 | 發·别名导出(GreenDragon)×2件 |
| Symbol_0_GreenDragon_Gold | 图 | 194x234(等2种) | 符号 | 牌网/演出 | 發·别名导出(GreenDragon)×2件 |
| Symbol_0_fa_gold | 图 | 184x224(等2种) | 符号·金牌 | 牌网 | 鎏金变体(消除后变百搭)×2件 |
| Symbol_0_fa_white | 图 | 184x224(等2种) | 符号·白牌 | 牌网 | 白玉麻将牌(消除主角)×2件 |
| Symbol_1_hongzhong_gold | 图 | 184x224(等2种) | 符号·金牌 | 牌网 | 鎏金变体(消除后变百搭)×2件 |
| Symbol_1_hongzhong_white | 图 | 184x224(等2种) | 符号·白牌 | 牌网 | 白玉麻将牌(消除主角)×2件 |
| Symbol_2_bai_gold | 图 | 184x224(等2种) | 符号·金牌 | 牌网 | 鎏金变体(消除后变百搭)×2件 |
| Symbol_2_bai_white | 图 | 184x224(等2种) | 符号·白牌 | 牌网 | 白玉麻将牌(消除主角)×2件 |
| Symbol_3_bawan_gold | 图 | 184x224(等2种) | 符号·金牌 | 牌网 | 鎏金变体(消除后变百搭)×2件 |
| Symbol_3_bawan_white | 图 | 184x224(等2种) | 符号·白牌 | 牌网 | 白玉麻将牌(消除主角)×2件 |
| Symbol_4_wutong_gold | 图 | 184x224(等2种) | 符号·金牌 | 牌网 | 鎏金变体(消除后变百搭)×2件 |
| Symbol_4_wutong_white | 图 | 184x224(等2种) | 符号·白牌 | 牌网 | 白玉麻将牌(消除主角)×2件 |
| Symbol_5_wutiao_gold | 图 | 184x224(等2种) | 符号·金牌 | 牌网 | 鎏金变体(消除后变百搭)×2件 |
| Symbol_5_wutiao_white | 图 | 184x224(等2种) | 符号·白牌 | 牌网 | 白玉麻将牌(消除主角)×2件 |
| Symbol_6_santong_gold | 图 | 184x224(等2种) | 符号·金牌 | 牌网 | 鎏金变体(消除后变百搭)×2件 |
| Symbol_6_santong_white | 图 | 184x224(等2种) | 符号·白牌 | 牌网 | 白玉麻将牌(消除主角)×2件 |
| Symbol_7_ertong_gold | 图 | 184x224(等2种) | 符号·金牌 | 牌网 | 鎏金变体(消除后变百搭)×2件 |
| Symbol_7_ertong_white | 图 | 184x224(等2种) | 符号·白牌 | 牌网 | 白玉麻将牌(消除主角)×2件 |
| Symbol_8_ertiao_gold | 图 | 184x224(等2种) | 符号·金牌 | 牌网 | 鎏金变体(消除后变百搭)×2件 |
| Symbol_8_ertiao_white | 图 | 184x224(等2种) | 符号·白牌 | 牌网 | 白玉麻将牌(消除主角)×2件 |
| Symbol_Scatter_Bg | 图 | 184x224 | 符号·胡 | 牌网 | Scatter:立体胡字/纹章底×2件 |
| Symbol_Scatter_Hu | 图 | 184x224(等2种) | 符号·胡 | 牌网 | Scatter:立体胡字/纹章底×2件 |
| Symbol_Wild | 图 | 192x224(等2种) | 符号·百搭 | 牌网 | WILD 中英版×2件 |
| Symbol_Wild_Zh | 图 | 192x224(等2种) | 符号·百搭 | 牌网 | WILD 中英版×2件 |
| gold_original_mahjong | 图 | 184x224(等2种) | 符号·底 | 演出 | 素牌底(爆炸基牌)×2件 |
| white_original_mahjong | 图 | 184x224(等2种) | 符号·底 | 演出 | 素牌底(爆炸基牌)×2件 |
| wild_text | 图 | 192x100 | 符号·百搭 | 演出 | WILD/百搭立体字×2件 |
| wild_text_zh | 图 | 192x100 | 符号·百搭 | 演出 | WILD/百搭立体字×2件 |

### 8.2 场景与世界板(29 行 / 89 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| Back_BaseGame | 图 | 576x1024 | 场景·转轮底板 | 牌网后 | 模式皮:Base/Free/Pity×2件 |
| Back_BaseGame_BottomTexture | 图 | 256x49 | 场景·转轮底板 | 牌网后 | 模式皮:Base/Free/Pity×2件 |
| Back_BaseGame_TopTexture | 图 | 1024x195 | 场景·转轮底板 | 牌网后 | 模式皮:Base/Free/Pity×2件 |
| Back_FreeGame | 图 | 576x1024 | 场景·转轮底板 | 牌网后 | 模式皮:Base/Free/Pity×2件 |
| Back_FreeGame_BottomTexture | 图 | 256x47 | 场景·转轮底板 | 牌网后 | 模式皮:Base/Free/Pity×2件 |
| Back_FreeGame_TopTexture | 图 | 1024x195 | 场景·转轮底板 | 牌网后 | 模式皮:Base/Free/Pity×2件 |
| Back_PityFreeGame | 图 | 576x1024 | 场景·转轮底板 | 牌网后 | 模式皮:Base/Free/Pity×2件 |
| Back_PityFreeGame_BottomTexture | 图 | 256x47 | 场景·转轮底板 | 牌网后 | 模式皮:Base/Free/Pity×2件 |
| Back_PityFreeGame_TopTexture | 图 | 1024x136 | 场景·转轮底板 | 牌网后 | 模式皮:Base/Free/Pity×2件 |
| Background | 图 | 32x32 | 场景·全屏背景 | 世界板后 | ×2件 |
| Background_BaseGame | 图 | 1024x1024 | 场景·全屏背景 | 世界板后 | ×2件 |
| 连莊倍率灯·Base(x1/x2/x3/x5,含亮版) | 图 | 160x160(等8种) | 世界板·倍率灯 | TopFence | 三模式各一套×16件 |
| 连莊倍率灯·Free(x2/x4/x6/x10,含亮版) | 图 | 200x160(等9种) | 世界板·倍率灯 | TopFence | 三模式各一套×16件 |
| Combo_LightAura | 图 | 256x183(等2种) | 世界板·倍率灯 | TopFence | 光环×2件 |
| 连莊倍率灯·PityFree(x2/x4/x6/x10) | 图 | 200x160(等5种) | 世界板·倍率灯 | TopFence | 三模式各一套×8件 |
| Frame_1320_0 | 图 | 60x61 | 场景·围栏件 | 世界板 | WIN 圆币 |
| Frame_BottomFenceBack | 图 | 1083x280(等2种) | 场景·围栏 | 世界板 | 顶/底栏(顶栏嵌倍率灯)×2件 |
| Frame_BottomFenceBack_Free | 图 | 1080x280(等2种) | 场景·围栏 | 世界板 | 顶/底栏(顶栏嵌倍率灯)×2件 |
| Frame_BottomFenceBack_Pity | 图 | 1024x265(等2种) | 场景·围栏 | 世界板 | 顶/底栏(顶栏嵌倍率灯)×2件 |
| Frame_BottomFenceMask | 图 | 1040x120 | 场景·围栏 | 世界板 | 顶/底栏(顶栏嵌倍率灯) |
| Frame_BottomFence | 图 | 1040x120(等2种) | 场景·围栏 | 世界板 | 顶/底栏(顶栏嵌倍率灯)×2件 |
| Frame_TopFence | 图 | 1080x340(等2种) | 场景·围栏 | 世界板 | 顶/底栏(顶栏嵌倍率灯)×2件 |
| Frame_TopFence_BackTexture | 图 | 916x280(等2种) | 场景·围栏 | 世界板 | 顶/底栏(顶栏嵌倍率灯)×2件 |
| Frame_TopFence_ContentMask | 图 | 1080x118 | 场景·围栏 | 世界板 | 顶/底栏(顶栏嵌倍率灯)×2件 |
| Frame_TopFence_ContentMask_Free | 图 | 1080x118 | 场景·围栏 | 世界板 | 顶/底栏(顶栏嵌倍率灯)×2件 |
| Frame_TopFence_Free | 图 | 1080x340(等2种) | 场景·围栏 | 世界板 | 顶/底栏(顶栏嵌倍率灯)×2件 |
| Frame_TopFence_Pity | 图 | 1080x340(等2种) | 场景·围栏 | 世界板 | 顶/底栏(顶栏嵌倍率灯)×2件 |
| SlotMachine_Shadow | 图 | 100x1920 | 场景·辅助 | 世界板 | 投影/遮罩×2件 |
| frame_bottomfence_inner_0 | 图 | 856x107 | 场景·围栏 | 世界板 |  |

### 8.3 HUD 与数字(48 行 / 127 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| AutoSelector 自动局数字/钮(10/20/50/100…) | 图 | 714x461(等4种) | HUD·自动局数 | Auto 面板 | ×8件 |
| 位图数字·世界板赢分套(0-9+逗点) | 图 | 1848x230(等13种) | 位图数字字模 | HUD/世界板 | ×13件 |
| 位图数字·FreeGameHUD 套(0-9) | 图 | 2060x234(等11种) | 位图数字字模 | HUD/世界板 | ×11件 |
| 位图数字·UI 套(0-9+逗点) | 图 | 2266x234(等13种) | 位图数字字模 | HUD/世界板 | ×13件 |
| Icon_Auto | 图 | 60x60 | HUD/菜单 icon | HUD/菜单 |  |
| Icon_Back | 图 | 140x140 | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_Bet | 图 | 60x60 | HUD/菜单 icon | HUD/菜单 | ×3件 |
| Icon_ChangeLanguage | 图 | 80x80 | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_Exit | 图 | 72x72 | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_Guide | 图 | 72x72 | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_History | 图 | 72x72 | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_Muted | 图 | 64x52 | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_Scatter | 图 | 192x224 | HUD/菜单 icon | HUD/菜单 |  |
| Icon_Setting | 图 | 72x72 | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_Settings | 图 | 80x81 | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_Spin | 图 | 100x101 | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_Stop | 图 | 100x101 | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_Turbo | 图 | 80x81(等2种) | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_Unmuted | 图 | 64x52 | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_Volume_Off | 图 | 161x50 | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_Volume_On | 图 | 160x50 | HUD/菜单 icon | HUD/菜单 | ×2件 |
| Icon_Wallet | 图 | 50x60 | HUD/菜单 icon | HUD/菜单 |  |
| Icon_Win | 图 | 60x60 | HUD/菜单 icon | HUD/菜单 |  |
| PlayerHUD_AutoBtn | 图 | 100x100 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_ButtonFrame | 图 | 100x100 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_ButtonTopMask | 图 | 160x160 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_PlayBtn_Frame | 图 | 240x240 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_PlayBtn_Frame_Auto | 图 | 240x240 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_PlayBtn_Icon_Hold_Gold | 图 | 163x163(等2种) | HUD | PlayerHUD | ×2件 |
| PlayerHUD_PlayBtn_Icon_Hold_Sliver | 图 | 163x163(等2种) | HUD | PlayerHUD | ×2件 |
| PlayerHUD_PlayBtn_Icon_Normal_HyberGame | 图 | 160x176(等2种) | HUD | PlayerHUD | ×2件 |
| PlayerHUD_PlayBtn_Icon_Normal_HyberGame_Sliver | 图 | 160x176(等2种) | HUD | PlayerHUD | ×2件 |
| PlayerHUD_PlayBtn_Icon_Normal_Universal | 图 | 180x148 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_PlayBtn_Icon_Normal_Universal_Sliver | 图 | 180x148 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_Pocket_Container | 图 | 480x84 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_Pocket_Win_Icon | 图 | 60x61 | HUD | PlayerHUD |  |
| PlayerHUD_SettingBtn | 图 | 100x100 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_SpeedBtn | 图 | 100x100(等2种) | HUD | PlayerHUD | ×2件 |
| PlayerHUD_SpeedBtn_FreeGame | 图 | 124x112(等2种) | HUD | PlayerHUD | ×2件 |
| PlayerHUD_SpeedIndicator_Light | 图 | 22x10 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_Symbol_DetailPanel | 图 | 398x244 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_Symbol_DetailPanel_Long | 图 | 624x244 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_TopHint_Icon | 图 | 36x36 | HUD | PlayerHUD | ×2件 |
| PlayerHUD__Pocket_Balance_Icon | 图 | 60x60(等2种) | HUD | PlayerHUD | ×2件 |
| Spin_0 | 图 | 242x242 | HUD/菜单 icon | HUD | 旋转箭头 |
| Spin | 图 | 256x256 | HUD/菜单 icon | HUD | 旋转箭头 |
| light_icon | 图 | 54x54(等2种) | HUD | SpeedPanel | 速度档位灯×2件 |
| light_icon_FreeGame | 图 | 54x54(等2种) | HUD | SpeedPanel | 速度档位灯×2件 |

### 8.4 菜单 / 历史 / 账单(26 行 / 61 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| BetItem_Bg_Win | 图 | 990x123 | 历史/账单 | History/BillDetail | ×2件 |
| BetItem_Copy | 图 | 28x28 | 历史/账单 | History/BillDetail | ×2件 |
| BetItem_OpenDetail_Icon | 图 | 16x32 | 历史/账单 | History/BillDetail | ×2件 |
| BetItem_Status_Complete | 图 | 160x40 | 历史/账单 | History/BillDetail | ×2件 |
| BetItem_Status_InProgress | 图 | 160x40 | 历史/账单 | History/BillDetail | ×2件 |
| BetItem_Status_Refunded | 图 | 160x40 | 历史/账单 | History/BillDetail | ×2件 |
| BillDetail_CalculationContainer | 图 | 960x168 | 历史/账单 | History/BillDetail | ×2件 |
| BillDetail_CloseButton | 图 | 72x66 | 历史/账单 | History/BillDetail | ×2件 |
| BillDetail_ContainerArrow | 图 | 28x14 | 历史/账单 | History/BillDetail | ×2件 |
| BillDetail_FlipButton_Icon | 图 | 120x120 | 历史/账单 | History/BillDetail | ×2件 |
| BillDetail_MoreInfo_Icon | 图 | 36x36 | 历史/账单 | History/BillDetail | ×2件 |
| Checkmark_Off | 图 | 30x30 | 菜单 | GameSetting | ×2件 |
| Checkmark_On | 图 | 30x30 | 菜单 | GameSetting | ×2件 |
| History 日期 tab 四态(Hover/Press/Selected/Unselected) | 图 | 316x100 | 历史/账单 | History | ×8件 |
| 选择器九宫格(Top/Middle/Bottom) | 图 | 268x92(等2种) | 菜单/选择器 | GameSetting | 9-slice×6件 |
| Language_Option_Button | 图 | 548x116(等2种) | 菜单·语言 | LanguageSelector | ×2件 |
| Language_selector_Panel | 图 | 800x960 | 菜单·语言 | LanguageSelector | ×2件 |
| Line_GuideSectionHeader | 图 | 124x4 | 菜单 | GameSetting | ×2件 |
| Line_HeaderDecoration | 图 | 604x12 | 菜单 | GameSetting | ×2件 |
| Line_SectionHearderDecoration | 图 | 124x4 | 菜单 | GameSetting | ×2件 |
| Line_Section | 图 | 1024x4 | 菜单 | GameSetting | ×2件 |
| Line_Tab_Horizontal | 图 | 276x4 | 菜单 | GameSetting | ×2件 |
| Setting_Bg | 图 | 288x512 | 菜单 | GameSetting | tab 态/底 |
| Setting_Tab_Hover | 图 | 216x168 | 菜单 | GameSetting | tab 态/底×2件 |
| Setting_Tab_Press | 图 | 216x168 | 菜单 | GameSetting | tab 态/底×2件 |
| Setting_Tab_Selected | 图 | 216x168 | 菜单 | GameSetting | tab 态/底×2件 |

### 8.5 入场页(9 行 / 14 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| GameEntry_Background | 图 | 1024x1024 | 入场页 | EntryPage | logo/背景/按钮容器×2件 |
| GameEntry_ButtonContainer | 图 | 256x56 | 入场页 | EntryPage | logo/背景/按钮容器 |
| GameEntry_Title_En | 图 | 512x467 | 入场页 | EntryPage | logo/背景/按钮容器×2件 |
| GameEntry_Title_Zh | 图 | 512x450 | 入场页 | EntryPage | logo/背景/按钮容器×2件 |
| GameEntry_Title_Zht | 图 | 512x450 | 入场页 | EntryPage | logo/背景/按钮容器×2件 |
| start_button_0 | 图 | 620x136 | 入场页 | EntryPage | 开始钮/开始字 |
| start_button | 图 | 620x136 | 入场页 | EntryPage | 开始钮/开始字 |
| start_button_highlight | 图 | 634x150 | 入场页 | EntryPage | 开始钮/开始字 |
| start_text | 图 | 196x99 | 入场页 | EntryPage | 开始钮/开始字×2件 |

### 8.6 玩法演出与庆祝(53 行 / 390 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| 爆炸旋转序列帧(0001-0020×4 组) | 图 | 256x256(等17种) | 消除爆炸 | 演出 | 序列帧×80件 |
| 通用光效/引擎默认件 | 图 | 1079x1080(等6种) | 通用光效 | 演出 | ×12件 |
| 免费公告·规则行文字图 | 图 | 985x163(等14种) | 文字图(多语言) | 演出 | 9 语言×18件 |
| 免费公告·开始钮文字图 | 图 | 256x85(等8种) | 文字图(多语言) | 演出 | 9 语言×16件 |
| 免费公告·标题文字图 | 图 | 512x192(等10种) | 文字图(多语言) | 演出 | 9 语言×22件 |
| 免费公告·累计标签文字图 | 图 | 452x268(等9种) | 文字图(多语言) | 演出 | 9 语言×16件 |
| 免费结算·确认钮文字图 | 图 | 236x107(等8种) | 文字图(多语言) | 演出 | 9 语言×16件 |
| 粒子/光效图集杂件 | 图 | 512x512(等14种) | 通用光效 | 演出 | ×46件 |
| ScreenEffect_BlackInOut | 图 | 1080x1080 | 过场 | ScreenEffect |  |
| 演出小件(金币/元宝/白板字) | 图 | 1024x1024(等6种) | 演出小件 | 多处 | ×7件 |
| bigwin_pattern | 图 | 512x512 | 庆祝 | Win 演出 | ×2件 |
| circlepattern | 图 | 512x512 | 庆祝 | Win 演出 | ×2件 |
| dragon_1 | 图 | 190x720 | Spine 盘龙 | 大演出 | 两套骨骼图集页 |
| dragon | 图 | 133x699 | Spine 盘龙 | 大演出 | 两套骨骼图集页 |
| dragon_highlight | 图 | 133x699 | Spine 盘龙 | 大演出 | 两套骨骼图集页 |
| dragontrail | 图 | 256x256 | Spine 盘龙 | 大演出 | 两套骨骼图集页 |
| 爆裂 sprite 序列 | 图 | 1600x800(等2种) | 消除爆炸 | 演出 | 序列帧×2件 |
| frame_top_0 | 图 | 1021x110 | 免费流程 | FreeSpin 演出 |  |
| freespin | 图 | 1040x140 | 免费流程 | FreeSpin 演出 | ×2件 |
| freespin_bg_0 | 图 | 1024x1024 | 免费流程 | FreeSpin 演出 |  |
| freespin_bg | 图 | 1024x1024 | 免费流程 | FreeSpin 演出 |  |
| freespin_frame_highlight | 图 | 1017x110 | 免费流程 | FreeSpin 演出 | ×2件 |
| freespin_top | 图 | 1040x110 | 免费流程 | FreeSpin 演出 |  |
| freespinbg | 图 | 512x512 | 免费流程 | FreeSpin 演出 |  |
| freespinending_bg | 图 | 2048x2048 | 免费流程 | FreeSpin 演出 | ×2件 |
| get_text | 图 | 205x95 | 文字图(多语言) | FreeSpin 结算 | 领取×2件 |
| 胡爆炸序列帧 | 图 | 864x864(等11种) | 胡演出 | Scatter 爆开 | 序列帧×11件 |
| 免费公告装饰序列(image_3) | 图 | 28x30(等8种) | 文字图(多语言) | 演出 | 9 语言×8件 |
| lv1 | 图 | 1040x120(等2种) | 庆祝 | Win 演出 | ×2件 |
| lv1_top | 图 | 1040x120(等2种) | 庆祝 | Win 演出 | ×2件 |
| lv1frame | 图 | 1040x120 | 庆祝 | Win 演出 | ×2件 |
| lv1frameblur | 图 | 1040x120 | 庆祝 | Win 演出 |  |
| lv23innergrow | 图 | 853x106 | 庆祝 | Win 演出 | ×2件 |
| lv2 | 图 | 1120x153 | 庆祝 | Win 演出 | ×2件 |
| lv2_top | 图 | 1120x153 | 庆祝 | Win 演出 | ×2件 |
| lv2frame | 图 | 1120x153 | 庆祝 | Win 演出 | ×2件 |
| lv2frameblur | 图 | 1120x153 | 庆祝 | Win 演出 |  |
| lv3 | 图 | 1120x153 | 庆祝 | Win 演出 | ×2件 |
| lv3_top | 图 | 1084x152(等2种) | 庆祝 | Win 演出 | ×2件 |
| rectangle_0 | 图 | 25x120 | 听牌演出 | NearMiss |  |
| skeleton | 图 | 256x256 | Spine 盘龙 | 大演出 | 两套骨骼图集页 |
| super_image_0 | 图 | 675x477 | 庆祝 | Win 演出 |  |
| super_image | 图 | 675x477 | 庆祝 | Win 演出 |  |
| superpattern | 图 | 512x512 | 庆祝 | Win 演出 | ×2件 |
| text2_0 | 图 | 747x98 | 文字图(多语言) | FreeSpin 公告 |  |
| text2 | 图 | 747x98 | 文字图(多语言) | FreeSpin 公告 |  |
| textblur | 图 | 512x512 | 庆祝 | Win 演出 | ×2件 |
| totalwin_text | 图 | 508x198 | 庆祝 | Win 演出 | ×2件 |
| win 三级标题文字图(大奖/巨奖/超级巨奖) | 图 | 512x217(等23种) | 文字图(多语言) | 演出 | 9 语言×54件 |
| win_image_0 | 图 | 1080x696 | 庆祝 | Win 演出 |  |
| win_image | 图 | 1080x696 | 庆祝 | Win 演出 |  |
| winnum_text | 图 | 941x209 | 庆祝 | Win 演出 | ×2件 |
| 元宝翻转序列(yuanbao00-11) | 图 | 256x256(等13种) | 消除爆炸 | 演出 | 序列帧×24件 |

### 8.7 Guide 插图(8 行 / 15 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| Guide_2000_Ways | 图 | 512x181 | Guide 插图 | Guide 长纸 | en/zh 双套×2件 |
| Guide_Free_Game | 图 | 1000x866 | Guide 插图 | Guide 长纸 | en/zh 双套×2件 |
| Guide_Gold_Mahjong_Symbols_En | 图 | 887x1024(等2种) | Guide 插图 | Guide 长纸 | en/zh 双套×2件 |
| Guide_Gold_Mahjong_Symbols_Zh | 图 | 900x1024(等2种) | Guide 插图 | Guide 长纸 | en/zh 双套×2件 |
| Guide_Hu | 图 | 100x115 | Guide 插图 | Guide 长纸 | en/zh 双套×2件 |
| Guide_Multipliers | 图 | 1000x144 | Guide 插图 | Guide 长纸 | en/zh 双套×2件 |
| Guide_Sample_Payout | 图 | 376x201 | Guide 插图 | Guide 长纸 | en/zh 双套×2件 |
| Guide_Sprites | 图 | 240x60 | Guide 插图 | Guide 长纸 | en/zh 双套 |

### 8.8 弹窗与通用件(12 行 / 15 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| AlibabaPuHuiTi TMP 字体图集 | 图 | 1x1 | 字体图集 | 全局 |  |
| Mask01 | 图 | 128x128 | 弹窗/通用 | Popups |  |
| 通用小件(光点/箭头/滑块等) | 图 | 303x303(等2种) | 通用小件 | 多处 | ×3件 |
| ToastPopup_BG_0 | 图 | 960x160 | 弹窗/通用 | Popups |  |
| ToastPopup_BG | 图 | 960x160 | 弹窗/通用 | Popups |  |
| ToastPopup_Reconnecting_0 | 图 | 100x100 | 弹窗/通用 | Popups |  |
| ToastPopup_Reconnecting | 图 | 100x100 | 弹窗/通用 | Popups |  |
| WarningPopup_BG_0 | 图 | 960x560 | 弹窗/通用 | Popups |  |
| WarningPopup_BG | 图 | 960x560 | 弹窗/通用 | Popups |  |
| WarningPopup_Button_0 | 图 | 342x98 | 弹窗/通用 | Popups |  |
| WarningPopup_Button | 图 | 342x98 | 弹窗/通用 | Popups |  |
| loading | 图 | 100x100 | 弹窗/通用 | Loading 圈 | ×2件 |

### 8.9 引擎内部(非美术主体)(1 行 / 56 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| 引擎/字体图集内部纹理(非美术主体) | 图 | 1024x1024(等12种) | 引擎内部 | — | 非美术主体,详见 elements×56件 |

### 8.10 音频(41 行 / 41 件:BGM 2 + 语音/SFX 39)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| Click Button | 音频·SFX | 0.16s | 音频 | — |  |
| Click Mahjong | 音频·SFX | 0.34s | 音频 | — |  |
| Click Spin | 音频·SFX | 0.28s | 音频 | — |  |
| Dragon Appear _ Fixed | 音频·SFX | 2.68s | 音频 | — |  |
| Eight Man | 音频·语音 | 0.52s | 音频 | — |  |
| Five Bamboo | 音频·语音 | 0.45s | 音频 | — |  |
| Five Dots | 音频·语音 | 1.24s | 音频 | — |  |
| Free Spin Calculate | 音频·SFX | 4.08s | 音频 | — |  |
| Free Spin Charge Jump Text | 音频·SFX | 0.98s | 音频 | — |  |
| Free Spin ComboDisplaySwap | 音频·SFX | 2.08s | 音频 | — |  |
| Free Spin Confirm Button | 音频·SFX | 0.81s | 音频 | — |  |
| Free Spin End | 音频·SFX | 3.04s | 音频 | — |  |
| Free Spin Transition | 音频·SFX | 1.73s | 音频 | — |  |
| FreeGame | 音频·BGM | 23.09s | 音频 | — |  |
| Green Dragon | 音频·语音 | 0.52s | 音频 | — |  |
| Ma Jiang Hu La | 音频·语音 | 1.89s | 音频 | — |  |
| Mahjong Land | 音频·SFX | 0.12s | 音频 | — |  |
| Mahjong Match | 音频·SFX | 0.96s | 音频 | — |  |
| Mahjong Shaking | 音频·SFX | 1.52s | 音频 | — |  |
| NearMiss | 音频·SFX | 6.43s | 音频 | — |  |
| NormalGame_Compressed_2 | 音频·BGM | 97.97s | 音频 | — |  |
| Quan Zhong Female | 音频·语音 | 1.02s | 音频 | — |  |
| Quan Zhong Male | 音频·语音 | 1.0s | 音频 | — |  |
| Red Dragon | 音频·语音 | 0.73s | 音频 | — |  |
| Scatter Appear | 音频·SFX | 0.74s | 音频 | — |  |
| Start Button | 音频·SFX | 0.38s | 音频 | — |  |
| Three Dots | 音频·语音 | 0.8s | 音频 | — |  |
| Total Win Message | 音频·SFX | 2.66s | 音频 | — |  |
| Two Bamboo | 音频·语音 | 0.52s | 音频 | — |  |
| Two Dots | 音频·语音 | 0.57s | 音频 | — |  |
| White Bamboo | 音频·语音 | 0.66s | 音频 | — |  |
| Wild Yunbao Appear | 音频·SFX | 0.8s | 音频 | — |  |
| Winning Calculation | 音频·SFX | 59.76s | 音频 | — |  |
| Winning End | 音频·SFX | 6.45s | 音频 | — |  |
| x1 | 音频·语音 | 0.82s | 音频 | — |  |
| x10 | 音频·语音 | 1.36s | 音频 | — |  |
| x2 | 音频·语音 | 0.83s | 音频 | — |  |
| x3 | 音频·语音 | 1.21s | 音频 | — |  |
| x4 | 音频·语音 | 0.85s | 音频 | — |  |
| x5 | 音频·语音 | 1.39s | 音频 | — |  |
| x6 | 音频·语音 | 1.19s | 音频 | — |  |

> 子表件数合计 834(图)+ 41(音频)= 875 == elements-SS03.json.assets 875。

## 9. 计数对账(机器清单指针)

- **全量资产 = 875**(图 834 + 音频 41)= `elements-SS03.json.assets` 行数 = asset-manifest 机扫结果;来源:data.unity3d 745(704 图+41 音)+ localization bundle 130 图。
- 对象普查(data.unity3d):Texture2D 387 + Sprite 324(同名图集页/裁切去重后落盘 704——两计数都保留,逻辑资产以文件名为准)、AudioClip 41=落盘 41、AnimationClip 49(时长唯一权威在灰盒注释面板)、TextAsset 8(Spine 4 + 引擎配置 4,未单独落盘)、Font 7、VideoClip 0。
- Addressables:catalog 89 名义条目=29 实名组,**全部下载成功**(带 hash 变体名是 catalog 内部引用,非缺口)。
