---
type: prd-split
audience: art / audio agents
product_code: ss02
product_name: "Beach Party / 沙滩派对"
genre: slot / 6×5 · multiplier-balloon wild
engine: Unity WebGL (IL2CPP, Addressables 2.8.x)
build: 1.0.0-71 (2026-03-16) — 当前 dev 线上实测版本
output_profile: obsidian_md
status: reverse-engineered (资产=UnityPy 导出 extracted/看图;编排=derived,未截图)
language: zh-CN
created: 2026-07-01
purpose: agent 训练素材 —— ss02 美术 / 音频规格
---

# ss02「Beach Party / 沙滩派对」— Art & Audio Doc（逆向·Unity）

> **分工**：只管长什么样、用什么资产、什么声音。玩法/数学见 [GDD-SS02.md](GDD-SS02.md)；布局/层级/坐标见 [UI-GREYBOX-SS02.html](UI-GREYBOX-SS02.html)。
>
> **来源**：资产 = UnityPy 解 `data.unity3d`（ss02 build 1.0.0-71）导出（288 图 / 26 音 / Spine 符号+乘数图集 / 4 AnimationClip）。尺寸=导出原生 px。**Addressables** catalog 另有 `common_fonts/shaders/textures` + locale bundle（`common_textures` 可能含额外美术，本轮未逐抽 → 完整性缺口）。
> **徽标**：`extracted`=导出资产实物；`derived`=命名/文档推定的编排/触发。**无 `validated`**（本轮未截图）。**双朝向**：横 1920×1080 + 竖 1080×1920 各有独立布局/视频。

---

## 0. Style Bible
- **一句话美学**：**热带沙滩夏日派对** —— 明快糖果色、霓虹灯招牌、3D 光泽质感的沙滩/水果/冰品道具，欢乐清凉。
- **60-30-10 配色**：**60 底**=青绿海水 + 天蓝(白天)/紫夜(免费)；**30 主体**=糖果多彩符号(粉/橙/蓝/彩虹)；**10 点缀**=霓虹灯管高光(摩天轮 Scatter/标题)、红气球乘数。
- **材质族**：3D 光泽塑料/充气质感(游艇/救生艇/气球)、玻璃罩(圣代)、霓虹灯管(Scatter/logo)、水花/泡沫粒子。
- **不变量**：chroma-key 透明底；符号为 **Spine 动画**(每符号 `*.atlas`)；数字用 `DigitNumber` 切图 + 气球专用 `BallonDigits`；特效独立层(水花/星光/彩虹)。
- **品牌**：`Title_Text_En`(470×242)「**Beach Party**」金字 + 霓虹 script + 沙滩球/沙堡。

## 1. 符号集（reel symbols）—— Spine 动画
每符号一个 Spine(`Symbol_N_*` + `*.atlas`)。原生贴图约 300+/336²。

| idx | 资产 | 符号 | 档 |
|--:|---|---|---|
| 1 | `Symbol_1_A_YACHT`（308×254） | 游艇(霓虹快艇) | 最高 |
| 2 | `Symbol_2_B_SEAPLANE` | 水上飞机 | |
| 3 | `Symbol_3_C_RAFT` | 充气救生艇 | |
| 4 | `Symbol_4_D_SUNDAE` | 圣代(玻璃罩) | |
| 5 | `Symbol_5_E_CONE` | 彩虹甜筒 | |
| 6 | `Symbol_6_F_POPSICLE` | 粉冰棍 | |
| 7 | `Symbol_7_G_MANGO` | 芒果 | |
| 8 | `Symbol_8_H_WATERMELON` | 西瓜 | |
| 9 | `Symbol_9_J_BLUEBERRY` | 蓝莓 | 最低 |
| Scatter | `Symbol_SCATTER`（336²）+ `SCATTER.atlas` + `2025_0717_SCATTER_ANIMATION`（1024²，SCATTER_2..15 帧） | **霓虹摩天轮** | — |
| Wild | `Symbol_Wild_X{2,3,5,10,20,30,50,100}`（336²） | **乘数气球**(红气球带乘数) | — |
- 每符号有 `Symbol_N_Bg` 背板;赔率见 GDD §3.3(值=server)。

## 2. 乘数气球 Wild（核心特色）
- **红气球 + 乘数数字**:`Symbol_Wild_X2..X100` + Spine `MULTIPLIER_X{2,3,5,10,20,30,50,100}`（256²，`*.atlas`）。
- **气球容器 + 数字**:`BallonContainer`（417×1024，半透明气球+吊绳）+ `BallonDigits`（1024×156）/ `BallonDigit_0..9` + `BallonDigit_X`（气球上显 "×N"）。
- 引爆特效:`explode`/`explo`/`water_explose`(水花爆 0..9 帧);音 `Big Balloon Bomb`/`Small Ballon Bomb`/`Fruit Bomb`。

## 3. 背景（每模式 1 套 · 2048²）
| 模式 | 背景 | 描述 |
|---|---|---|
| Base | `Background_Normal`（2048²） | 白天热带海滩:棕榈、绿松石泻湖、沙滩椅、救生圈 |
| Free Spin | `Background_FreeSpin`（2048²） | 夜晚/黄昏海滩:紫天、海星、发光水面 |
- 通用:`Background`、`blur_bg`、`bg_wave_mask`/`wavebg_mask`(波浪遮罩)、`BubblesWater`/`foam`/`water`/`Wave_Trail_Hor`(水面动态)。
- 转轮框:`Frame_Bg`（512×426）/ `Frame_Bg_FreeSpin`;`Frame_Fence`（1024²）;`GridBg`(网格底);`BaseGame_Strip_LeftUp/LeftMIddle/RightUp/RightMiddle`(框角条)。

## 4. 投注增强 UI
- **Buy Free Spin**:`BuyFeature_On`/`_Off`（92×36 开关）、`BuyFeature_Background`、`BuyFeature_Popup_Background`（518×376，紫霓虹框）、`BuyFeature_Popup_BuyButton`（330×103）、`BuyFeature_Popup_CloseButton`。
- **Double Chance**:`BetItem_Boost`(增强投注标) + 面板 Toggle(on/off)(节点 `DoubleChance/Toggle`)。

## 5. HUD / 控件（双朝向,坐标见 HTML）
- 主钮 `ButtonPanel_Play_Normal/Hover/Pressed`（220×255）+ `Icon_Play_Normal_HyberGame`/`_Universal`/`_Auto`/`_Holding`;自动 `AutoCount_TMP`、免费 `FreeSpin_TMP`。
- 圆钮 `ButtonPanel_Common_Normal/Hover/Pressed`（98×105）:设置 `Icon_OpenSetting`、下注 `Icon_BetSelector`、自动 `Icon_AutoSelector`/`_Inner`、加速 `Icon_SpeedLevel`/`ToggleIcon_SpeedLevel`(+ `Panel_SpeedLevel` 指示灯)、返回 `Icon_Back`、复制 `Icon_Duplicate`。
- 钱包栏 `Panel_Wallet`（600×223）+ `Icon_Balance`（56×66）/ `Icon_Profit`;下注 `Panel_BetAmount`。
- 切图数字 `DigitNumber`（1584×224，0-9+Comma+Dot）;字体 `AlibabaPuHuiTi`/`AlibabaSansSEA`/`NotoSansKhmer`(高棉语)。

## 6. 其它屏
- **设置**:`Setting_Background`（1024×576 横）/ `Setting_Background_Vertical`（576×1024 竖）;`UICheckMark`/`ToggleIcon`;`Line_Section`。
- **账单详情 BillDetailPage**(Canvas_BillDetailPageContainer):`BillDetailPage_BottomBlur`/`_DivideLine_RightToLeft`/`_Icon_FlipToRight`;明细段 `WinSymbolLine`/`ScatterLine`/`MultiplierLine`(赢分符号/scatter/乘数三段)。
- **弹窗/加载**:`RoastPopup_Loading`(维护/重连)。
- **入场**:`Title_Text_En`「Beach Party」。免费过场视频 `asset_v1/videos/freeSpin.mp4`(横/竖各一)。

## 7. 粒子 / 特效
`Sparkle`/`Light`/`highlight`/`lens`/`lens2`/`lensbg3`/`flare03`/`T_flare02`/`door_light`/`lightstripe_highres`/`beachstar`/`star`/`stars`/`star_trail`/`rainbow`/`ribbon_elements`/`smoke1`/`splash_1`/`foam`/`water_explose`(0..9)/`water_explose`/`bubbleswater`/`Wave_Trail_Hor`/`trail3`。AnimationClip:`explode_1` 等。

## 8. 音频触发表（26 AudioClip）
| 时机 | 音频 |
|---|---|
| **spin** | `Click Spin`、`Roulette Stop`(转停) |
| **符号中奖(逐类)** | `BoatMatch`(游艇)、`AirplaneMatch`(水上飞机)、`CruiseMatch`(救生艇)、`FruitMatch`(水果)、`LickIceCream`(冰品)、`ScatterMatch` |
| **乘数气球引爆** | `Big Balloon Bomb`、`Small Ballon Bomb`、`Fruit Bomb` |
| **结算** | `SS02_SFX_WinningCalculating`、`SS02_SFX_WinningEnd`、`SS02_SFX_SmallCoin` |
| **中奖分级** | `2_Big Win`、`3_Super Win`、`4_Mega Win`、`5_Epic Win`(阈值 ≥bet×5/20/50/100,GDD §6) |
| **Scatter / 免费** | `ScatterAppear`、`Enter Free Spin_Wheel`(摩天轮进场) |
| **近失** | `SFX_NearMiss_Fast`/`_Medium`/`_Slow`(临近触发免费) |
| **UI** | `Click Button`、`Click Empty`、`WelcomeDropdown_WaterSplash` |

> 触发精确编排(逐符号同步/乘数结算时序)=`derived`,待真机录屏 `validated`。

## 9. i18n
字体图集实证多语:英 `AlibabaPuHuiTi`/`AlibabaSansSEA` + 高棉 `NotoSansKhmer` + Emoji。标题 `Title_Text_En`(另应有其它语言版)。Addressables locale bundle:`english(en)` 等。

## 10. Sources
- ss02 构建 1.0.0-71 `data.unity3d`(UnityPy):288 图、26 音、Spine(符号/乘数/scatter)、双朝向 Canvas。
- 看图:符号集/气球乘数/背景/摩天轮 Scatter/Beach Party 标题。
- Addressables `aa/catalog.bin`:common_fonts/shaders/textures + locale(未全抽)。

---
**ADD 结束(逆向·Unity 1.0.0-71)。资产=导出实物;编排待截图升级。玩法见 GDD-SS02.md;布局见 UI-GREYBOX-SS02.html。**
