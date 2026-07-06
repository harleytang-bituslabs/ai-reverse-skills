---
type: prd-split
audience: art / audio agents
product_code: ss03
product_name: "Mahjong Streak / 麻将连莊"
genre: slot / 2000-ways
engine: Unity WebGL (IL2CPP, Addressables 2.x)
build: 1.0.0-56 (2026-03-26) — 当前 dev 线上实测版本
output_profile: obsidian_md
status: reverse-engineered (资产=UnityPy 导出 extracted/看图;runtime 动效编排=derived,未截图)
language: zh-CN
created: 2026-06-30
purpose: agent 训练素材 —— ss03 美术 / 音频规格
---

# ss03「Mahjong Streak / 麻将连莊」— Art & Audio Doc（逆向·Unity）

> **分工**：只管长什么样、用什么资产、什么声音。玩法/数学见 [GDD-SS03.md](GDD-SS03.md)；布局/层级/坐标见 [UI-GREYBOX-SS03.html](UI-GREYBOX-SS03.html)。
>
> **来源**：所有资产 = **UnityPy 解 `data.unity3d`（1.0.0-56）导出的 Texture2D/Sprite/AudioClip/AnimationClip**（704 图 / 41 音 / 49 动画 / 32 AnimatorController）。尺寸 = 导出原生 px。Addressables 包**仅本地化**（9 语 string/asset table），**无美术**。
> **徽标**：`extracted`=导出资产实物（看图确认题材/尺寸）；`derived`=由命名/动画名推定的编排/触发，未截图证实。**无 `validated`**（本轮未取真机截图；动效/编排待升级）。

---

## 0. Style Bible（美学基准）

- **一句话美学**：中式麻将贺岁风 —— **象牙白麻将牌 + 金龙盘绕 + 翡翠绿/朱红/鎏金**，喜庆、厚重、有金属反光与立体浮雕感。
- **60-30-10 配色**（看导出图提）：
  - **60 底**：深色木纹/暗红场景背景（`Back_BaseGame` 暖红木；`Back_FreeGame` 金；`Back_PityFreeGame` 另一换皮）。
  - **30 主体**：象牙白麻将牌面（牌底带木色斜切边，立体）。
  - **10 点缀**：**鎏金**（金龙 / 元宝 Wild / 金牌框 / 标题描金）+ 牌面色（發=翡翠绿、中/胡=朱红、八萬=靛蓝、筒=红绿蓝点、条=绿竹）。
- **材质族**：象牙陶瓷牌面（高光+投影）、鎏金 3D 金属（龙/元宝/标题）、翡翠玉质（免费框/分隔线）、木纹（背景/框）。
- **不变量**：
  - **chroma-key/透明底**：符号、龙、元宝、粒子均独立透明 PNG，运行时合成。
  - **不烧字**：数字用 `DigitNumber` 切图字体（非烧进位图）；多语文案走 i18n 美术或 TMP（标题/艺术字除外）。
  - **特效独立**：高光/光环/火花/光斑（`Highlight`/`Sparkle`/`Flare`/`Combo_LightAura`）为独立叠加层。
- **品牌**：标题 `GameEntry_Title`（En/Zh/Zht）= "MAHJONG STREAK / 麻将连莊" 鎏金立体字 + 盘绕金龙（512×450）。

---

## 1. 符号集（reel symbols）— 核心美术

每符号 **white（普通）+ gold（金牌）** 两态，**原生 184×224**（= `ScenarioGrid` 单元格尺寸，1:1 上屏）。code 对应 GDD §3.2 赔付表。

| code | 资产 base | 牌面 | 态 | 赔付档 |
|--:|---|---|---|---|
| 0 | `Symbol_0_fa_white` / `_gold` | **發**（翡翠绿 honor） | 白/金 | 最高 50/25/10 |
| 1 | `Symbol_1_hongzhong_white` / `_gold` | **中**（朱红 honor） | 白/金 | 40/20/8 |
| 2 | `Symbol_2_bai_white` / `_gold` | **白板**（靛蓝框 honor） | 白/金 | 30/15/6 |
| 3 | `Symbol_3_bawan_white` / `_gold` | **八萬**（靛蓝字） | 白/金 | 15/10/5 |
| 4 | `Symbol_4_wutong_white` / `_gold` | **五筒**（5 彩点） | 白/金 | 12/5/3 |
| 5 | `Symbol_5_wutiao_white` / `_gold` | **五条**（绿竹） | 白/金 | 12/5/3 |
| 6 | `Symbol_6_santong_white` / `_gold` | **三筒**（3 彩点） | 白/金 | 10/4/2 |
| 7 | `Symbol_7_ertong_white` / `_gold` | **二筒**（2 彩点） | 白/金 | 6/3/1 |
| 8 | `Symbol_8_ertiao_white` / `_gold` | **二条**（2 绿竹） | 白/金 | 6/3/1 |
| 202 | `Symbol_Wild` / `_Zh`（192×224）, `gold_yuanbao`（184×224） | **元宝 WILD**（鎏金，"WILD"/"百搭"字） | — | 百搭 |
| 201 | `Symbol_Scatter_Hu` + `Symbol_Scatter_Bg`（各 184×224） | **胡**（朱红描金，圆底） | — | Scatter |

- 另有 `SymbolPattern_0..8`（牌面图案分离件，用于动画/合成）；`white_original_mahjong` / `gold_original_mahjong`（空白牌底，白/金）。
- **金牌只在中 3 列**（GDD §3.3），中奖转 Wild → 配 `gold mahjong` / `wild_appear` 动画。

## 2. 转轮框 / 网格（reel frame）
- **可见窗 4-5-5-5-4**，单元格 184×224、列距 184（相邻无缝）、行距 204、外列垂直居中（坐标/几何见 HTML）。
- 框件（每模式换皮）：`Frame_TopFence`（1080×340）/ `Frame_TopFence_Free` / `Frame_TopFence_Pity`；`Frame_BottomFence`（1040×120）/ `_Free` / `_Pity` / `_BottomFenceBack*`；遮罩 `Frame_TopFence_ContentMask`（1080×118，+ `_Free`）、`Frame_BottomFenceMask`；底纹 `Frame_TopFence_BackTexture`（916×280）。
- `SlotMachine_Shadow` 转轮投影。

## 3. 背景（两层：场景背景 + 转轮底板）
> ⚠️ **`Back_*` 不是全屏背景，而是转轮框内的底板**（SpriteRenderer 实证：`Back_BaseGame`→`FrameBG`/`FrameBG_MaskedFrame`）。全屏**场景背景**是 `Background_BaseGame`（→`Bg_1`/`Block`/`Bg_MaskFrame`）。
| 层 | 资产 | 用途 |
|---|---|---|
| **场景背景（全屏）** | `Background_BaseGame`（1024×1024） | 翡翠绿径向光 + 底部金币/麻将/元宝堆 + 祥云。Free/Pity 无独立场景包 → 共用或运行时着色（`derived`） |
| **转轮底板（Base）** | `Back_BaseGame`（576×1024，红底金角） | 牌网后的框内底板（`FrameBG`）；`Back_BaseGame_TopTexture`（1024×195）/`_BottomTexture`（256×49）= 上/下延展条（`VerticalBlock_Back_Top/BottomTexture`） |
| **转轮底板（Free）** | `Back_FreeGame`（576×1024，金底） | 同上，Free 换皮 + `_Top/BottomTexture` |
| **转轮底板（Pity）** | `Back_PityFreeGame`（576×1024） | 同上，保底换皮 + `_Top/BottomTexture` |
| 框底纹 | `Frame_TopFence_BackTexture`（916×280）/`Frame_BottomFenceBack` | 顶/底栏背纹 |
| 通用小件 | `Background`（32²，UI 底）、`background_0`（288×512，暗底/dim） | — |

## 4. 倍率 / combo（cascade streak 件）
- **位置 = 转轮框顶栏（TopFence）上、牌网正上方**（world-space `MatchComboDisplay`，挂 `SlotMachine/Decorations/FrameFence/TopFence`）；**背景 = 顶栏横幅 `Frame_TopFence`**（1080×340，青绿描金，见 `Guide_Multipliers` 样式）。**非屏幕顶部悬浮条、非一条 bar**。
- **形态 = 一排 4 个方槽**（`ScenarioMutiplierDisplay/Slot_1..4`，各 **175×140**、pitch 224，实测自单注详情 UI 复刻件）；当前档 `LightSlot`+`Aura`(256×183 光环 `Combo_LightAura`)+`LightImage` 点亮。
- 槽面美术：Base `Combo_Base_x1/x2/x3/x5`（单件 160×160）+ 各 `_Light`；Free `Combo_Free_x2/x4/x6/x10`（单件 200×160）+ 各 `_Light`；Pity `Combo_PityFree_x2/x4/x6/x10`。
- 倍率梯=cascade 进档（GDD §2/§4）；动画 `lv2` / `lv2frame` / `lv2anim 1` / `lv2frameappear` / `lv23innergrow` / `innergrow`。

## 5. 中奖庆祝（win celebration）
- **三级标题**（hans，各另有 en/其它语言）：`win_big_title_hans`「**大奖**」（绿）→ `win_mega_title_hans`「**巨奖**」（蓝紫）→ `win_super_title_hans`「**超级巨奖**」（红）。
- 演出件：`bigwin_pattern`（512²）、`super_image`（675×477）、`superpattern`、`circlepattern`、`coin`（1024²）/ `coin_edge` / `ss03coin`（金币爆）、`totalwin_text` / `winnum_text` / `win_image` / `text2`。
- 本轮赢分横幅 `MessageBanner`（见 HTML，[20,1288,1040×140]，悬浮转轮底与 HUD 间，`Total Win Message` 音）。
- 动画：`win_image_anim` / `wintext_anim` / `text_explose` / `explose zoomin` / `superdragon`。

## 6. 免费游戏 / Scatter / 盘龙
- **进场公告**：`FreespinAnnounce_title`（en/hans，「赢得免费旋转」）、`freespin` / `freespin_bg`（1024²）/ `freespin_top` / `freespin_frame_highlight` / `freespinbg`；结束 `freespinending_bg`（2048²）。
- **胡 Scatter 演出**：`Symbol_Scatter_Hu` + `hu_explode`（864²，多帧 `hu_explode_0..11`）；音 `Scatter Appear` / `Ma Jiang Hu La`（麻将胡啦）。
- **盘龙（Spine）**：`dragon`（133×699）/ `dragon_1`（190×720）/ `dragon_highlight` / `dragontrail`；Spine 图集 `dragon.atlas` + `skeleton` / `skeleton.atlas`（256²）；AnimatorController `Spine GameObject (dragon) alpha`、动画 `dragon base blur` / `superdragon`；音 `Dragon Appear _ Fixed` / `Green Dragon` / `Red Dragon`。免费金列 `Guide_Free_Game` 示意。

## 7. HUD / 控件美术（坐标见 HTML）
- 主钮 `PlayerHUD_PlayBtn_Frame`（240×240）+ 图标 `PlayerHUD_PlayBtn_Icon_Normal_*`（Universal/HyberGame/ Hold_Gold/Hold_Sliver/各 _Sliver）+ `_Frame_Auto`；自动剩余 `AutoCount_TMP`。
- 圆钮（各 100×100 底 `PlayerHUD_ButtonFrame` + `ButtonTopMask`）：设置 `Icon_Setting`（72²）、下注 `Icon_Bet`（60²）、自动 `Icon_Auto`（60²）/`AutoSelector_Infinity_Normal`、加速 `Icon_Turbo`（80²）+ `PlayerHUD_SpeedBtn` / `_FreeGame` / `PlayerHUD_SpeedIndicator_Light`、旋转 `Icon_Spin`（100²）/`Icon_Stop`。
- 口袋栏：`PlayerHUD_Pocket_Container` + `PlayerHUD__Pocket_Balance_Icon`（💰）+ `PlayerHUD_Pocket_Win_Icon`；顶提示 `PlayerHUD_TopHint_Icon`。
- 符号详情浮窗 `PlayerHUD_Symbol_DetailPanel`（398×244）/ `_Long`（点中奖符号看连线/计算 `WinSymbol_Calculations`）。
- 切图数字（3 套）：`DigitNumber`（游戏，1848×230）/ `DigitNumber_UI`（2266×234）/ `DigitNumber_FreeGameHUD`，含 0-9 + `_Comma` + `_Dot`。

## 8. 其它屏美术
> **菜单叠层结构（重要）**：设置 / 赔付(Guide) / 历史 **不是三个独立屏**，而是**一块 `Canvas_GameSetting_Vertical` + 底栏 `TabList`（返回·设置·赔付·历史·退出 5 tab）切换内容面板**（`SettingPanel` / `GuidePanel` / `BetPanel`）。TabList 底栏 `[0,1728,1080,192]`。tab 图标：`Icon_Back` / `Icon_Setting` / `Icon_Guide` / `Icon_History` / `Icon_Exit`；tab 态 `Setting_Tab_Hover/Press/Selected`。布局/坐标见 HTML ②。
- **入场**：`GameEntry_Background`（1024²）+ `GameEntry_Title_En/Zh/Zht`（512×450）+ `start_button`（620×136）/ `start_text` / `start_button_highlight`（音 `Start Button`）。宿主 React 壳。
- **设置面板（SettingPanel tab）**：`Setting_Bg`（288×512）/ `SettingUI_Background`；分区 声音(BGM/SFX 各一排开关)/语言/画质；开关 `Checkmark_On/Off` / `UICheckMark`；语言/画质选择器 `Image_Selector_Top/Middle/Bottom`。
- **赔付/规则长纸（GuidePanel tab → GuidePaperDisplay 可滚场景，972 宽）**：`Guide_Sample_Payout`（376×201，發 5/4/3=50/25/10 特写）/ `Guide_2000_Ways`（512×181）/ `Guide_Gold_Mahjong_Symbols_En/Zh`（~900×1024）/ `Guide_Free_Game`（1000×866）/ `Guide_Multipliers`（1000×144，青绿倍率横幅）/ `Guide_Hu`（100×115）/ `Guide_Sprites`（240×60）。段落 SymbolOdds→GameRules→GameUI×5→AdditionalInfo。
- **历史/注单（BetPanel tab + BillDetailPage 场景）**：`BetItem_*`（Bg_Win/Copy/OpenDetail_Icon/Status_Complete/InProgress/Refunded）；`BillDetail_*`（CalculationContainer/CloseButton/ContainerArrow/FlipButton_Icon/MoreInfo_Icon）；日期筛选 tab（Today/Week/3Day…）。
- **弹窗**：`ToastPopup_BG`（960×160）/ `ToastPopup_Reconnecting`；`WarningPopup_BG`（960×560）/ `WarningPopup_Button`。
- **图标集**：`Icon_Back/ChangeLanguage/Exit/Guide/History/Muted/Unmuted/Volume_On/Off/Wallet/Win/Wild/Wild_Zh/Scatter`。

## 9. 粒子 / 通用特效
`coin`/`Sparkle`(256×252)/`Flare`(256²)/`Flare_blur`/`Highlight`(256²)/`Default-Particle`/`BlurBall`/`light2`/`LightDot`/`LightStripe`/`spark_round`/`circle`/`circlepattern`/`bloom`/`lighting`/`Dounut`/`Noise05`/`GradientCenter01/02`/`T_flare02`/`explose_sprite_1`(1600×800)。元宝动画帧 `yuanbao00..11`（256²×12）。AnimationClip：`appear`/`appear_bloom`/`explode`/`explode_wild_text`/`explode_yuanbao`/`yuanbao_appear`/`wild_appear`/`frame appear/disappear anim`/`lightstripe_fadein`/`particle_fadein`/`textblur_fadein`/`nearmissoverlay`。

## 10. 音频触发表（41 AudioClip，导出 .m4a）
| 触发时机 | 音频 |
|---|---|
| **BGM** | `NormalGame_Compressed_2`（base 循环）、`FreeGame`（免费循环） |
| **spin** | `Click Spin`、`Mahjong Shaking`（转动）、`Mahjong Land`（落定） |
| **符号落定/中奖逐符号** | `Mahjong Match`；逐牌：`Green Dragon`(發)、`Red Dragon`(中)、`White Bamboo`、`Eight Man`(八萬)、`Five Dots`(五筒)、`Five Bamboo`(五条)、`Three Dots`(三筒)、`Two Dots`(二筒)、`Two Bamboo`(二条)、`Quan Zhong Female/Male`（全中人声） |
| **结算** | `Winning Calculation`、`Winning End`、`Total Win Message` |
| **cascade 倍率** | `x1`/`x2`/`x3`/`x4`/`x5`/`x6`/`x10`（按当前 cascade 档） |
| **Wild** | `Wild Yunbao Appear`（元宝百搭出现） |
| **Scatter / 胡** | `Scatter Appear`、`Ma Jiang Hu La`（麻将胡啦）、`Dragon Appear _ Fixed` |
| **近失** | `NearMiss`（差一个 Scatter，纯演出） |
| **免费游戏流程** | `Free Spin Transition`→`Free Spin Charge Jump Text`→`Free Spin Confirm Button`→`Free Spin Calculate`→`Free Spin ComboDisplaySwap`→`Free Spin End` |
| **UI** | `Click Button`、`Click Mahjong`、`Start Button` |

> 触发时机的精确编排（逐 cascade 同步音/动画）= `derived`，由 AudioClip/AnimationClip/AnimatorController 命名推定，待真机录屏 `validated`。

## 11. i18n（Addressables 本地化，9 语）
catalog 实证 9 语：英 `en` / 简中 `zh-hans` / 繁中 `zh-hant` / 印地 `hi` / 印尼 `id` / 韩 `ko` / 马来 `malaysian` / 泰 `th` / 越 `vi`。每语 string-tables + asset-tables + locales bundle。多语美术：标题 `GameEntry_Title_En/Zh/Zht`、`win_*_title_hans`、`FreespinAnnounce_title_en/hans`、`Guide_Gold_Mahjong_Symbols_En/Zh`、`wild_text` / `wild_text_zh` / `Symbol_Wild` / `_Zh`。字体图集：`AlibabaPuHuiTi` / `AlibabaSans*` / `NotoSansDevanagari`（印地）/ `LiberationSans_SDF` / `ZiKuXingQiuFeiYangTi_Digits`（艺术数字）。

## 12. Sources
- Unity 构建 1.0.0-56 `data.unity3d`（UnityPy）：704 Texture2D/Sprite、41 AudioClip、49 AnimationClip、32 AnimatorController、126 ParticleSystem、Spine（dragon/skeleton）。
- 帮助页 `Guide_*` 看图：题材/赔付/倍率/免费/金牌规则。
- Addressables `aa/catalog.bin`：9 语本地化（无美术包）。

---
**ADD 结束（逆向·Unity 1.0.0-56）。资产=导出实物；编排/触发待截图升级。玩法见 GDD-SS03.md；布局见 UI-GREYBOX-SS03.html。**
