# ART & AUDIO DESIGN — cg02a「榴莲派对 / Durian Party」

> **本文回答**：长什么样、用什么资产、什么声音。资产清单 + 规格 + 题材风格 + 动画意图 + 音频触发。
> **不回答**：玩法规则 / 状态机（见 [GDD-CG02A.md](GDD-CG02A.md)）、每屏每态控件如何摆放（见 [UI-GREYBOX-CG02A.html](UI-GREYBOX-CG02A.html)）。
> **来源**：`~/harley/cg02/crashgame-cg02a-ui/cg02a`（PixiJS v8，竖屏 1080×1920）全量代码 + 资产穷尽抽取。标 *code-derived* 处为代码真值、未经截图复核（cg02a 暂无截图；固定画布 Pixi 代码即 1:1 真值，非阻塞）。

---

## 0. 一句话题材

**多人连续曲线 crash 游戏（Aviator 类）**，主角是一颗**亮泽糖果质感 3D 榴莲**。榴莲在粉彩天空中持续升空、倍率不断上涨；玩家须在 **UFO 拦截、榴莲被切开爆炸**之前 CASH OUT 锁定收益。整局所有玩家共处一个房间（实时排行榜 + 奖池 + 双注栏）。

> ⚠️ **换皮血统（铁律：信 runtime 不信注释/旧文件）**：cg02a 由前作 **CG02「直升机 Chopper」reskin 而来**。仓库内 `SCENE2_NOTES.md`（提到 chopper/直升机、bell/钟、GameOver、scene3）描述的是 **CG02 前作**，**不是 cg02a**；`public/assets/texts/how-to-play.md` 写「足球被踢飞」是**更早的足球题材前作 cg01 的残留**（cg01「Crash Game」足球 → … → cg02a 榴莲；已交叉确认）。cg02a 的真实主角是**榴莲**、拦截者是 **UFO**，以 `GamePlayAssets.ts` / `DurianManager.ts` / `UfoEffect.ts` 等真实在用文件为准。`GAME_GUIDE_RESKIN.md` 明确记录了 CG02→CG02A 的换皮差异（Chopper/撞钟 → 榴莲/UFO 抓走；UI 主色 蓝灰 → 橄榄绿）。

风格关键词：糖果光泽、粉彩渐变天空、橄榄绿 UI 主色族（#5D8219 系）、金色描边的奖励数字、3 段高度氛围（气球 → 热气球 → UFO）。

---

## 1. 画布 / 坐标系 / 全局色

| 项 | 值 | 说明 |
|---|---|---|
| 设计画布 | **1080 × 1920**（竖屏） | 固定画布，无相机/视口缩放 |
| 设计基准 | 390 × 744 → SCALE = 1920/744 ≈ **2.5807** | 老设计稿放大系数 |
| 布局分区 | `ZONES.middle` = (0,0,1080,**1075**) / `ZONES.bottom` = (0,**1005**,1080,**915**) | 两区在 y=1005–1075 **重叠 70px**（HUD 顶压住游戏区底） |
| 主背景 | `bg_normal.webp` (1080×1927) | 全屏静态底（`MainBackground`，cover） |

**theme.json 配色**（`public/assets/theme/theme.json`，运行时取色）：
```
textPrimary #FFFFFF | textSecondary #8899AA | textMuted #667788
topBarBg #0D1B2E | hudOverlayBg #0A1628 (α0.5) | settingOverlayBg #87A5C7 (α0.9) | settingTitleBarBg #5D8DD2
button normal/hover/pressed/disabled #444/#666/#222/#2A2A2A
tab tint normal/hover #E5E5E5/#FFFFFF | tabShadow #000 (α0.5)
fontFamily primary "Verdana, Tahoma" / secondary "Inter, sans-serif"
```
> 注：theme.json 的 topBarBg #0D1B2E 与代码里 TopBar 实绘 `rect fill #0B204A α0.3`、GameHistoryBar/PrizePool `#32574B α0.6` 略有出入——**实际渲染以代码常量为准**（见 [UI-GREYBOX-CG02A.html](UI-GREYBOX-CG02A.html) 各帧 data-fill）。

UI 主色族（橄榄绿，源自换皮，散落各组件常量，非 theme.json）：`#5D8219`（设置/正文主色）、`#789743`（余额数字）、`#6B8B34`/`#D5E9B2`（双注 tab A/B 字色）、`#87A921`（设置底栏绿）、`#BFDF5D`/`#D0EAA8`（注单 cashout/crashed 底）。奖励/盈利数字渐变 `#FFF165→#FDA211` + 描边 `#E86000`。

---

## 2. Spine 角色（榴莲本体）

榴莲本体**全程是 Spine 骨骼动画**（不是静态图）；散件 durian_*.png 仅作 crash 碎块。

| Spine | 文件（atlas/json/png） | png 尺寸 | 骨架/皮肤/动画 |
|---|---|---|---|
| **scene1**（待机/下注态榴莲） | `spines/scene1/cg02A_scene1.*` | 872×872 | 动画 `idle1`/`idle2`/`idle3` 各 **2.0s**、`jump` **0.667s**（下注末尾起跳 kickoff） |
| **scene2and3**（飞行 + 撞毁榴莲，共用） | `spines/scene2/cg02A_scene2and3.*` | 1800×1800 | 骨架 ~**1314×3317**；皮肤 `default`/`lv1`/`lv2`/`lv3`（按倍率换皮）；动画 `loop` ~**0.667s**（飞行循环）、`end` ~**4.167s**（撞毁一次性）；含 `ufo`/`root` 骨用于挂特效 |

上屏尺寸（*code-derived*，几何可定）：飞行榴莲 = `DURIAN_SCALE 0.2 × panelScale 1.794`（Scene2Panel）；待机榴莲 = `IdleKickoffSpine` 根 scale **0.6**。
> **关键**：榴莲飞行时 **Y 坐标固定**（`DURIAN_Y=330`，仅开局有一次 0.6s、400px 的滑入 `ENTRY_OFFSET_Y`）。**没有"随倍率持续升空"、没有相机/视差**——"升空感"由背景滚动 + 氛围装饰下落 + 3 段换皮共同营造（详见 GDD §3、HTML 注释面板③）。`cameraShaking.ts` 是**死代码**（从不实例化）。

---

## 3. 飞行场景资产（Scene2 / Scene3）

### 3.1 滚动背景 tile（3 段，按倍率切换）
| 别名 | 文件 | 尺寸 | 用途 |
|---|---|---|---|
| `bg1` | `sprite/scene2/bg1.png` | **1080×2160** | lv1（倍率 < 2x） |
| `bg2` | `sprite/scene2/bg2.png` | **1080×2160** | lv2（2 ≤ 倍率 < 10x） |
| `bg3` | `sprite/scene2/bg3.png` | **1080×2160** | lv3（倍率 ≥ 10x） |

均为 **TilingSprite 竖直滚动**（`tilePosition.y += 2 px/帧 @60fps`，恒速，**无视差**）；切层用 600ms alpha 交叉淡化。bg 图高 2160 > 可视区，是"超过一屏的长卷"——见 [UI-GREYBOX-CG02A.html](UI-GREYBOX-CG02A.html) **画廊 B（场景长卷）**。

### 3.2 氛围装饰（背后从上往下飘，按 level 切换池）
| level | 别名 / 文件 | 尺寸 | 飘落参数(*code-derived*) |
|---|---|---|---|
| lv1 | `lv1-balloon-01/02/03`（气球 3 色）`.webp` | 170×390 / 250×572 / 273×624 | 间隔 1200–2800ms，scale 0.35–0.75，落速 2–4px/帧 |
| lv2 | `lv2-hotair-01/02`（热气球）`.webp` | 609×923 / 540×830 | 间隔 1500–3500ms，scale 0.2–0.45，落速 2–4 |
| lv3 | `lv3-ufo-01/02`（UFO）`.webp` | 396×177 / 315×205 | 间隔 1500–3500ms，scale 0.35–0.75，落速 2–4 |

x 随机 ∈[50,730]，y 从屏顶外 -h/2 入场落到底销毁；开局预铺 2 个。`FlyingItems` 用 `Math.random` 生成，**装饰性、非固定布局**。

### 3.3 榴莲周身特效（精灵表，挂在 spine 骨上）
| 别名 | 文件 | 尺寸 | 切片(列×行,帧) | 用途 / 参数 |
|---|---|---|---|---|
| `smoke` | `effect/scene2/smoke.png` | 512×509 | 4×4, 16 | 飞行时持续冒烟，间隔 200–400ms，scale 0.4–0.8，tint #e8e8e8，角度 210° |
| `smoke2` | `effect/scene2/smoke2.png` | 1024×349 | 10×2, 19 | **液体飞溅**（DurianLiquid），24fps 循环，scale(0.7,-0.7) 镜像 |
| `emotion1/2/3` | `effect/scene2/emotion*.png` | 512×649 | 4×4, 16 | 榴莲头顶情绪气泡，lv1/2/3 各一张；24fps，脉动 scale 0.5↔0.7 yoyo |
| `explode`(指向)`explode2` | `effect/scene2/explode2.png` | 1145×428 | 5×2, 10 | **升级爆裂**（lv1→2、lv2→3），18fps，scale 1.8，blend screen |
| `spark1` | `effect/scene2/spark1.png` | 1024×512 | 4×2, 8 | 升级火花，24fps，scale 1.5，blend screen |
| `spark` | `effect/scene2/spark.png` | 1080×608 | 5×5, 25 | 背景闪烁（SparkEffect），间隔 100–300ms，blend add |
| `speedline` | `effect/scene2/speedline.png` | **6240×1980** | 8×3, 24 | 全屏速度线，居中(390,330)，24fps，blend add，tint #88b4ff，α0.7 |

> **孤儿**：`effect/scene2/explode.png`(2560×1920) 已废弃（代码注释「原 explode.png 已不再使用」，实际指向 explode2）。

### 3.4 Crash / UFO 拦截效果
| 别名 | 文件 | 尺寸 | 切片 | 用途 / 参数 |
|---|---|---|---|---|
| `ufo` | `effect/crash/ufo.png` | 1024×614 | 5×3, 15 | UFO 飞掠，24fps，scale 1.76，blend screen，挂 `ufo` 骨 +200y |
| `light` | `effect/crash/light.png` | 256×256 | — | 拦截光柱，挂 `ufo` 骨 +246y，blend add，纵向拉伸 scale(1.65, 0→2.2)；**色随 level**：lv1 #ffa500(α0.7) / lv2 #62e8f0(α0.5) / lv3 #ff0099(α1.0) |
| `roundlight` | `effect/crash/roundlight.png` | 524×524 | — | 圆形脉冲，crash 时 **4 连击**（间隔 200ms），scale 0→2.2 + α 1→0，0.6s |
| `dot` | `effect/crash/dot.png` | 128×128 | — | 掉落碎块拖尾粒子，blend add |
| `durian-fruit` | `sprite/scene2/durian_fruit.png` | 674×282 | — | 整榴莲散件 |
| `durian-half` | `sprite/scene2/durian_half.png` | 671×739 | — | 半切榴莲 |
| `durian-slice` | `sprite/scene2/durian_slice.png` | 744×375 | — | 榴莲切片（升级时抛撒：lv1→2 抛 3 片、lv2→3 抛 2 片） |
| `durian-sliceempty` | `sprite/scene2/durian_sliceempty.png` | 894×479 | — | 空切片壳 |

crash 序列（`CrashManager`，2000ms）：spine 切 `end` 动画 + 背景 600ms 缓停 + 烟/液/情绪淡出 + roundlight×4 + UFO 光柱(100ms 延迟) + UFO 飞掠。详时序见 [UI-GREYBOX-CG02A.html](UI-GREYBOX-CG02A.html) 注释面板②。

---

## 4. 倍率数字（SpriteDigits，5 色图集）

倍率/盈利数字全部用**图集数字**渲染（不是字体）。5 张 **1530×181** webp，字符布局完全一致：

| 别名 | 文件 | 何时用 |
|---|---|---|
| `digits_normal`（蓝） | `…/sprite-digits/digits_normal.webp` | 倍率 < 2.0x（飞行 lv1） |
| `digits_profit`（绿） | `digits_profit.webp` | 2.0 ≤ 倍率 < 10x（lv2） |
| `digits_super`（金） | `digits_super.webp` | 倍率 ≥ 10x（lv3） |
| `digits_crashed` | `digits_crashed.webp` | 撞毁瞬间显示 |
| `digits_win` | `digits_win.webp` | 结算盈利金额 |

字符规格（每张图集）：`0-9` 宽 127.5、`x` 宽 127.5、`.`/`,` 宽 63.75，高 181，字距 -10，基线锚点 (0,1)。字符集 `0123456789x.,`，MAX 12 字符（"10000.00x"）。逐字「弹跳」动画 slot bob 12px / 150ms。
> 这是 **2x 高清图集**，上屏默认 scale ≈ 0.994（180/181）；倍率 ≥ 6 时整体 ×1.10（紧张感）。`text_crashed.png`(600×102) 是单独的 "CRASHED" 字图。

---

## 5. 底部多人 HUD 资产（PlayerHUD，ZONES.bottom）

| 别名 | 文件 | 尺寸 | 用途 |
|---|---|---|---|
| `playerhud_bg` | `player-hud/playerhud_bg.webp` | 1080×845 | 我的下注面板底 |
| `playerhud_list_bg` | `player-hud/playerhud_list_bg.webp` | 1080×845 | 全部玩家列表面板底 |
| `balance_container` | `player-hud/balance_container.png` | 940×80 | 余额条（左:Balance / 右:Total Bet） |
| `bet_switcher_bg` | `bet-switcher/bet-switcher_bg.png` | 392×107 | 加减注显示框 |
| `btn_lower_bet_1/2/3` | `bet-switcher/…` | 107×107 | 减注按钮 normal/hover/click |
| `btn_raise_bet_1/2/3` | `bet-switcher/…` | 107×107 | 加注按钮 normal/hover/click |
| `btn_quickbet`(+`_hover`/`_click`) | `quick-bet/…` | 168×102 | 快捷投注（$1 / $5 / $15） |
| `auto-cashout_container` | `auto-cashout/auto-cashout_container.png` | 467×94 | 自动套现框 |
| `icon_auto-cashout` | `auto-cashout/icon_auto-cashout.png` | 26×26 | 自动套现图标 |
| `toggle_on` / `toggle_off` | `auto-cashout/…` | 182×74 | 自动套现开关 |
| `btn_bet` | `play-button/btn_bet.png` | 417×120 | 下注（单键，绿描边 #22D37B） |
| `btn_cancel` | `play-button/btn_cancel.png` | 417×120 | 取消（红描边 #d03232） |
| `btn_wait` | `play-button/btn_wait.png` | 417×120 | 等待（灰描边 #848484） |
| `btn_cashout`(+`_hover`) | `play-button/…` | 229×120 | 全额套现（金描边 #C49029） |
| `btn_50-cashout`(+`_hover`) | `play-button/…` | 229×120 | 50% 套现（橙描边 #D8755B） |
| `player_cards` | `all-players/player_cards.png` | 948×216 | 排行榜单卡底（用 940×208） |
| `icon-triangle` | `all-players/icon-triangle.png` | 72×42 | 排行榜滚动提示三角（弹跳 amp 8 / cycle 3000ms） |
| `tab_on` / `tab_off` | `tabs/tab_on.png` … | 540×100 | HUD 底栏双 tab（我的注 / 全部玩家） |

PlayButton 七态：`bet / cancel / cashout / cashout-no-half / cashout-half-done / wait / next-round`。套现态拆成左 50% + 右 FULL 双键（gap 20）。字号 locale-aware（EN 66 / CN 54）。

> **孤儿/未用**（13 个，截图无需复现）：`icon_auto-cashout_blue.png`、`total-prize/icon_player.png`(56×56)、`tabs/tab_all_player_*` + `tab_my_info_*`（4 个自定义 tab 变体，代码只用 tab_on/off）、`play-button/hover/btn_bet_hover.png` + `btn_cancel_hover.png`（仅 cashout/50 有 hover）。

---

## 6. 下注态 / 倒计时 / 顶栏 / 历史资产

| 别名 | 文件 | 尺寸 | 用途 |
|---|---|---|---|
| `game_s1_bg` | `images/cg02a_mobile_S1_bg_3.webp` | 1080×1123 | 下注态游戏区背景（betting 时 y=-40） |
| `bet-phase:next-game` | `…/game-view/bet-phase_next-game.png` | 528×111 | "下一局"提示图 |
| `progress_container` | `content-view/progress_container.png` | 608×39 | 倒计时进度槽 |
| `progress_fill` | `content-view/progress_fill.png` | 591×27 | 倒计时填充 |
| `progress_durian` | `content-view/progress_durian.png` | 63×59 | 进度条上的榴莲游标（随填充右移） |
| `btn_setting_gameview` | `content-view/btn_setting_gameview.png` | 84×84 | 右上设置齿轮（GameView 内，~x1017 y111） |
| `history_container_normal/profit/super` | `content-view/history/…` | 165×68 | 历史倍率条目底（<2x 灰字 / 2–10x 绿 / ≥10x 红，用 146×64） |
| `history_has-more` | `content-view/history/history_has-more.png` | 47×68 | 历史条左右"更多"箭头 |
| `text_crashed` | `…/game-view/text_crashed.png` | 600×102 | "CRASHED" 字图（撞毁横幅，用 545×100） |
| `lose_container` | `…/game-view/lose_container.png` | 496×110 | 亏损结算底（**已加载但当前关闭**，A1 不显示亏损） |

---

## 7. 加载 / 异常 / 设置 / 弹窗资产

**加载屏**（React DOM，非 Pixi）：`loading_frame`(914×134)、`loading_fill`(884×77)、logo 按语言 `logo_en.webp`(1000×424)/`logo_zh_hans.webp`(1584×672)/`logo_zh_hant.webp`(1584×670)、`btn_start.png`(882×225)。
> 孤儿：`btn_start_click/hover/en.webp`（加载只用 btn_start.png 单态）。

**设置面板**（Pixi，全屏 overlay）：`setting_background.webp`(1080×1920)、`select_language_bg.webp`(800×960)、`btn_back`(140×140)、`btn_setting/guide/bet_history/exit`(72×72)、`btn_setting_switch`(80×80)、`btn_selected/unselected`(63×63)、`btn_setting_selected.webp`(216×168)、`setting_voice_mute/unmute`(64×52)、`setting_frame`(200×4)、`history_divider_line`(847×7)、`history_tab_container`(310×100)/`_unselected`(314×100)、`history-item_icon_copy`(28×28)。
**Guide 教程图标**：`guide/arrow-down`(28×53)、`double-arrow`(69×57)、`guide-red-arrow`(200×95)、`icon-success/icon-fail`(46×46)。Guide 卡片大量用 **canvas 渐变/Graphics 绘制**（tilted-olive 橄榄绿斜置卡、奶白渐变、横线、六角星），非图片资产。

**弹窗**：`button_popup_confirm.png`(342×98)。Toast / Warning 面板的渐变描边边框是 **canvas 程序绘制**（`gradientFrame.ts`）：Toast 对角 #65F4FA→#FEF988、Warning 竖向浅绿 + #FAE92A 描边 + 绿渐变确认键。

> **程序化渲染**（~17 文件，非资产文件，运行时按 theme 画）：toast/warning 边框、设置分割线、tab 底、popup 蒙层、各面板裁切 mask、guide 卡渐变与星。复现时按对应组件常量用 Canvas/Graphics 重绘（详见 HTML data-fill 注记）。

---

## 8. 音频（1 BGM + 15 SFX）

`public/assets/audios/`，别名见 `SoundDefs.ts`：

| 别名(SoundDefs) | 文件 | 触发时机 |
|---|---|---|
| `BGM.MAIN` = `main:bgm` | `bgm/BGM.mp3` | 全程背景乐（失焦/隐藏时静音） |
| `SFX.CLICK` = `sfx:click_normal` | `sfx/sfx_click_normal.mp3` | 通用 UI 点击 |
| `SFX.BET` = `sfx:click_bet` | `sfx/sfx_click_bet.mp3` | 下注/快捷投注点击 |
| `SFX.COUNTDOWN` = `sfx:countdown` | `sfx/sfx_effect_countdown.mp3` | 下注倒计时最后几秒（每秒） |
| `SFX.GAME_START` = `sfx:game_start` | `sfx/sfx_effect_game_start.mp3` | 进入 RUNNING 飞行态 |
| `SFX.JUMP` = `sfx:scene1_jump` | `sfx/sfx_effect_scene1_jump.mp3` | 下注末尾榴莲起跳 kickoff |
| `SFX.SCENE1_IDLE_1/2/3` = `sfx:scene1_idle1/2/3` | `sfx/scene1_idle1/2/3.mp3` | 待机 idle 序列 |
| `SFX.SPIN_LV12` = `sfx:spin_lv12` | `sfx/effect_spin1.mp3` | lv1+lv2 飞行循环音 |
| `SFX.SPIN_LV3` = `sfx:spin_lv3` | `sfx/effect_spin2.mp3` | lv3 飞行循环音 |
| `SFX.WOOSH` = `sfx:woosh` | `sfx/effect_woosh.mp3` | 飞行中每 2s 一次（crash 停） |
| `SFX.LEVEL_UP_2` = `sfx:level_up_2` | `sfx/effect_level_up_2.mp3` | lv1→lv2 升级 |
| `SFX.LEVEL_UP_3` = `sfx:level_up_3` | `sfx/effect_level_up_3.mp3` | lv2→lv3 升级 |
| `SFX.CASHOUT` = `sfx:cashout` | `sfx/sfx_effect_cash_out.mp3` | 套现成功（`overlap=true`，多人同时可叠播） |
| `SFX.CRASH_END_UFO` = `sfx:crash_end_ufo` | `sfx/effect_crash_end_ufo.mp3` | UFO 拦截 / 撞毁 |

BGM 走 HTMLAudioElement，SFX 走 @pixi/sound；`AudioManager` 支持 fade / tag 批量 / overlap。

---

## 9. 复现注意（踩坑铁律，本作命中）

1. **信 runtime 不信注释/旧文件**：`SCENE2_NOTES.md`(chopper/钟/scene3)、`how-to-play.md`(足球) 都是前作残留；以 `GamePlayAssets.ts`+真实 scene2 目录为准（榴莲/UFO）。
2. **固定画布无相机**：榴莲飞行 Y 固定、bg 恒速滚动、无视差、无缩放——"升空"是错觉。`cameraShaking.ts` 死代码。复现勿加相机动画。
3. **原生尺寸 ≠ 上屏尺寸**：spine 0.2×1.794、idle 0.6、digits 0.994、bg tile 1080×2160 滚动——按代码 scale 还原，别用 PNG 原尺寸直接贴。
4. **状态 ≠ 屏**：PlayButton 七态、digits 5 色、bg/skin 3 段都是同一区域的状态切换，不是不同屏。
5. **余额在底部 HUD 不在顶栏**（cg02a 与 cg03a/cg03r 不同）：顶栏只有历史条 + 齿轮，余额/总注在 BalanceBar。
6. **数学/经济为服务端**：倍率曲线、crash 点、RTP、AC 触发都来自服务端 tick，客户端无公式（见 GDD §2）。
7. **孤儿资产不复现**：§5/§7 列的 13 个未用资产 + explode.png 不必生成。

---

## 10. 交叉引用

- 玩法 / 回合状态机 / 经济（下注/套现/倍率/排行榜）→ [GDD-CG02A.md](GDD-CG02A.md)
- 每屏每态布局 / 控件坐标 / UI 行为 / 动画时序 → [UI-GREYBOX-CG02A.html](UI-GREYBOX-CG02A.html)
- 本系列方法论 → [../skills/reverse-game-to-triad/SKILL.md](../skills/reverse-game-to-triad/SKILL.md)
