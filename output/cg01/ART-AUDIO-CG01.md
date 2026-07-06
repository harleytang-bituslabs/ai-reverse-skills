# ART & AUDIO DESIGN — cg01「Crash Game / 足球 Soccer Crash」

> **本文回答**：长什么样、用什么资产、什么声音。题材风格 + 资产清单&规格 + 动画意图 + 音频触发。
> **不回答**：玩法规则/状态机/经济（见 [GDD-CG01.md](GDD-CG01.md)）、每屏每态控件布局与坐标（见 [UI-GREYBOX-CG01.html](UI-GREYBOX-CG01.html)）。
> **来源**：`~/harley/cg01/crashgame-cg01-ui/cg01`（PixiJS v8，竖屏 1080×1920）全量代码 + 资产穷尽抽取。**无 `.art-meta`/Figma 设计稿** → 全部来自代码 + 资产文件实测。无截图 → 全 *code-derived*（固定画布 Pixi 代码即 1:1 真值，非阻塞）。

---

## 0. 一句话题材

**多人连续曲线 crash 游戏（Aviator 类），足球/体育场题材**。一颗足球被踢飞冲上夜场天空，倍率随之持续上涨；玩家须在**足球被拦截（crash）**之前点 **CASH OUT** 锁定收益。整局所有玩家共处一房间（实时排行榜 + 共享奖池）。胜利结算时升起**奖杯**。

> ⚠️ **换皮血统（铁律：信 runtime 不信旧文件）**：cg01 是这一系列的**题材源头之一**。`public/assets/texts/how-to-play.md` 写「足球被踢飞…被拦截前 CASHOUT」——**这里足球是真主角**（由 `CG01_scene2_soccer` spine + `soccer.png` + 火球/草屑特效佐证）。注意：**cg02a「榴莲派对」那份污染的"足球"how-to-play 其实就是从 cg01 继承的残留**（cg02a 把足球换皮成了榴莲）。cg01 = 足球，以本仓库资产为准。

风格关键词：**写实-绘画风夜场足球赛**（泛光灯 + 满座看台 + 绿茵）、金/绿/橙 + 火焰能量、足球 + 奖杯 hero、火球拖尾、速度线、镜头震动。

---

## 1. 画布 / 坐标系 / 全局色

| 项 | 值 | 说明 |
|---|---|---|
| 设计画布 | **1080 × 1920**（竖屏） | 固定画布，无相机/视口缩放 |
| 设计基准 | 390 × 744 → SCALE = 1920/744 ≈ **2.5807** | 老设计稿放大系数（同系列） |
| 布局分区 | `ZONES.middle` = (0,0,1080,**1156**) / `ZONES.bottom` = (0,**1056**,1080,**864**) | 两区在 y=1056–1156 **重叠 100px**（HUD 顶压住游戏区底） |
| 主背景（下注态） | `images/bg_normal.jpg` (390×744 源图，cover 铺满) | 夜场看台 + 绿茵 + 底部金/火能量 + 足球+双奖杯 hero |
| 主背景（飞行态） | `images/bg_flying.jpg` (390×744) | 同场景带**球门网**（球冲向球门）+ 底部 hero 区 |

**theme.json 配色**（`public/assets/theme/theme.json`，运行时取色）：
```
textPrimary #FFFFFF | textSecondary #8899AA | textMuted #667788
topBarBg #0D1B2E | hudOverlayBg #0A1628 (α0.5) | settingOverlayBg/TitleBarBg #112E60 (α0.85)
button normal/hover/pressed/disabled #444/#666/#222/#2A2A2A | tab tint #E5E5E5/#FFFFFF
fontFamily primary "Inter, sans-serif"
```
> TopBar 实绘 `rect fill #0B204A α0.3`；PrizePool/HistoryBar 等多为图片底。运行渲染以代码常量为准（见 [UI-GREYBOX-CG01.html](UI-GREYBOX-CG01.html)）。

UI 强调色族：奖励/盈利金渐变 `#FED027→#FFEF73`（描边 #DDA23C）；倍率数字蓝(<2x)/绿(2-10x)/橙(≥10x)/crashed/gold；历史条 normal 绿 #AEE5C5 / profit 白 / super 金 #FFF0A0(橘描边 #FF9500)；下注成功绿 #4DD498、撞毁红 #FF6161。

---

## 2. Spine 角色（足球 + 待机 + 奖杯）

| Spine | 文件（json/atlas/png） | png 尺寸 | 骨架固有尺寸 / 动画 |
|---|---|---|---|
| **idle/kickoff**（下注态待机 + 开球） | `spines/idle-and-kickoff/cg01_scene1_REALMONEY.*`（+ `_2.png` 第 2 页） | 3000×3000 + 1568×1568(2页) | 固有 **780.42×927.12**；动画 `idle1`/`idle2`/`idle3`（随机不重复链）+ `start`(kickoff 起脚)；mix 0.2s。上屏 scale=1080/780≈**1.38** → ≈1080×1284，居中 (540,538) |
| **scene2 bg**（飞行背景，随倍率缩放） | `effects/gameplay-flying/cg01/CG01_scene2_bg.*` | 928×928 | 固有 **1023.19×928**；**bgLayer 随倍率 `calcBgScale(m)` 缩放**（控制点 m1→1.0/2→1.125/10→1.5/100→1.875/1000→2.25，150ms lerp，pivot 右上 (234,−269) 世界 (624,61)）——这就是"升空/拉近"错觉的来源，**非相机** |
| **scene2 soccer**（飞行足球，固定尺寸） | `effects/gameplay-flying/cg01/CG01_scene2_soccer.*` | 1316×1316 | 固有 **414.62×474.33**；动画 `entry`(起手)/`loop`(飞行循环)/`gameover`(撞毁)；spineContainer 固定中心 (390,330)；timeScale lv1/2=1.0、lv3=1.25 |
| **trophy**（结算奖杯） | `effects/gameplay-flying/trophyspine/skeleton.*` | 392×392 | 固有 **218.08×376.66**；仅 `animation`（无 idle，播完停末帧）；SettlementPanel 内 trophyGroup scale=**2.0** → 上屏 ≈436×753 |

> 上屏尺寸 = 固有尺寸 × 已知代码缩放（*code-derived*，几何可定）。**唯一需截图核对**的是足球各倍率档的实际升空轨迹/落点——由 soccer spine `entry/loop` 的 **bone15** 关键帧 baked 驱动（非代码常量），但 spine 资产已在仓库内、播同一骨架即可还原（非阻塞）。

---

## 3. 飞行场景特效（gameplay-flying，挂 spine 骨）

倍率 3 段（`EffectLevelManager` 阈值 2x/10x，只升不降）逐级强化：

| 别名 | 文件 | 尺寸 | 切片 | 用途 / 参数 |
|---|---|---|---|---|
| `gp-fly:fireball1/2/3` | `fireball1/2/3.png` | 1024×687 | 3×5 | **火球拖尾**（跟 soccer 的 bone15：x=+bone15.worldX−40 / y=+bone15.worldY+30），锚(0.78,0.45)，旋 −45°，blend add；lv1 scale×(0.425,0.75)@0.7fps / lv2 ×(1.7,2.0)@1fps / lv3 ×(2.2,2.6)@1.5fps |
| `gp-fly:fire` | `fire.png` | 512×512 | 4×4(16帧 128²) | **升级火焰爆裂**（升档瞬间），scale(4,3.5) blend add @0.6，左下漂移 |
| `gp-fly:speedline2/3/4` | `speedline*.png` | 512×512 | 单帧 | **速度线**（居中 390,339，blend add）：lv1 α0 / lv2 α1 speed0.3 scale×1.1 / lv3 α1 speed0.5 |
| `gp-fly:smoke` | `smoke.png` | 512×512 | 2×8(16) | crash 时烟雾（挂 human 骨，scale 1.5，α0.8 @0.4） |
| `gp-fly:grass` | `grassparticle.png` | 258×262 | 3×3(切9) | **草屑粒子**（挂 foot 骨，飞行时 30/s 持续喷，crash 时爆 15–20；上抛 angle −120°~−60°，speed 250–700，gravity 1200–2000） |
| `gp-fly:dust` | `dust.png` | 658×794 | 3×4(12) | crash 灰尘（固定 195,347，旋 45°，crash 后 300ms scale 0→4） |
| `gp-fly:lightstripe` | `lightstripe.png` | 512×512 | — | 结算光条（SettlementPanel 用） |

镜头震动（升档触发，200ms：scale 1→1.15→1.05→1 + xy 抖）；运动模糊滤镜（`MotionBlurFilter` GLSL 径向：lv1 off / lv2/3 strength0.1，crash 时 radius→1.0 800ms 自关）。详时序见 [UI-GREYBOX-CG01.html](UI-GREYBOX-CG01.html) 注释面板②③。

---

## 4. Cashout / 结算资产

| 别名 | 文件 | 尺寸 | 用途 |
|---|---|---|---|
| `gp-fly:coin` | `coin.png` | 512×683 | 金币 3×4(12帧) 旋转：我方 cashout 爆发 + 结算金币雨（CoinRainEffect 3s @15/s） |
| `gp-fly:ribbon` | `ribbonelements.png` | 512×512 | 彩带 5×5(25变体)：他人 cashout 径向爆发 + 结算彩带（RibbonFallEffect 3s @8/s） |
| `gp-fly:co-banner` | `CashOut/banner.png` | 888×228 | 我方 cashout 横幅底（MyCashoutPanel 592×152 用） |
| `gp-fly:co-youwin` | `CashOut/youwin.png` | 476×110 | "YOU WIN" 字图（318×73 用） |
| `gp-fly:co-ratio` | `CashOut/ratio.png` | 497×110 | 倍率标签底（332×73 用） |
| `effects/gameplay-flying/coin.png` 等 | — | — | （同上 gp-fly:coin） |

- **MyCashoutPanel**（飞行中点 cashout 的即时反馈）：594×272，居中 (540, viewH·2/3−224)，youwin+banner+ratio 三层 + 金额 SpriteDigits（scale≈0.71）；fade-in 200/hold 1000/out 200，scale 0→1.33→1。
- **SettlementPanel**（crash 后全屏庆祝）：黑幕 vignette(α→0.75) + **trophy spine**(中心 scale2) + 8 条光条(lightstripe，金 #FFE15D/#FFC126 add，各 2s 循环) + youwin/banner/ratio + 金额(SpriteDigits 64px) + 金币雨 + 彩带。

---

## 5. 倍率数字（SpriteDigits，5 色图集）

倍率/盈利数字全部用**图集数字**（非字体）。`images/content-view/game-view/sprite-digits/`：

| 别名 | 文件 | 尺寸 | 字符规格 | 何时用 |
|---|---|---|---|---|
| `digits_normal`（蓝） | `digits_normal.png` | 600×75 | digit 50 / special(. , x→特殊?) 25，高75 | 倍率 < 2.0x |
| `digits_profit`（绿） | `digits_profit.png` | 600×71 | digit 50 / 25，高71 | 2.0 ≤ 倍率 < 10x |
| `digits_super`（橙） | `digits_super.png` | 600×71 | digit 50 / 25 | 倍率 ≥ 10x |
| `digits_crashed` | `digits_crashed.png` | 600×75 | digit 50 / 25 | 撞毁瞬间 |
| `digits_gold`（金，**2×高清**） | `digits_gold.png` | 1200×124 | digit 100 / 50，高124 | 系统预留（主流程未激活；可用于大额结算） |

字符集 `0-9 / x / . / ,`（CHAR_INDEX 0-12），MAX 13 字符（"9,999,999.99x"），锚(0,1) 底对齐、水平居中 x=−totalW/2；可选黑色阴影(α0.55)。`text_crashed.png`(342×68) 是单独 "CRASHED" 字图（撞毁横幅）。

---

## 6. 底部多人 HUD 资产（PlayerHUD，ZONES.bottom）

> ⚠️ **cg01 是单注栏**（一局一注）：只有 **BetSwitcher(±) + 一个 PlayButton + 一个 AutoCashout**，**无双注 A/B、无快捷投注 quick-bet 行**（与 cg02a/cg03 不同）。

| 别名 | 文件 | 尺寸 | 用途 |
|---|---|---|---|
| `playerhud_bg_header` | `player-hud/playerhud_bg_header.png` | 540×50（实测）/ 拼装 1080×100 | HUD 顶图（不拉伸） |
| `playerhud_bg_body` | `player-hud/playerhud_bg_body.png` | 540×382 / 拼装 1080×764 | HUD 身图（纵向拉伸补满） |
| `money_container` | `player-hud/money_container.png` | 174×62 | 余额/总注显示底（MoneyContainer 430×134 用 2 个） |
| `bet_switcher_container` | `player-hud/bet-switcher/bet-switcher_container.png` | 720×120 | 加减注框（中央显示当前注额） |
| `btn_lower_bet` / `btn_raise_bet` | `player-hud/bet-switcher/…` | 106×106 | 减注 / 加注（按下 0.95 缩放 + y 翻转 + tint） |
| `auto-cashout_container` | `player-hud/auto-cashout/auto-cashout_container.png` | 354×36 / 用 1008×93 | 自动套现框（输入 1.01~1000，默认 2.00 + 开关） |
| `icon_auto-cashout` | `player-hud/auto-cashout/icon_auto-cashout.png` | 46×46 | 自动套现图标 |
| `toggle_on` / `toggle_off` | `player-hud/auto-cashout/…` | 180×72 | 自动套现开关（开=绿 tint #80FF80） |
| `btn_bet` / `btn_cancel` / `btn_cashout` / `btn_wait` | `player-hud/play-button/…` | 546×136 | PlayButton 五态共用 4 图（bet/cancel/cashout/wait+next-round）；标签 64px 白+灰描边 #7B8779 |
| `tab_my_info_on/off` / `tab_all_player_on/off` | `player-hud/tabs/…` | 195×44 | HUD 底栏双 tab（我的 / 全部玩家） |
| `icon_player` | `player-hud/total-prize/icon_player.png` | 56×56 | 奖池条玩家数图标 |
| `bg_all-players` | `player-hud/all-players/bg_all-players.png` | 380×280 | ⚠️ **孤儿**（无引用，见 §9） |

PlayerHUD 结构：PrizePoolBar(顶,100h:左玩家数+右奖池) + TabPanel(中:MyBetPanel 或 AllPlayersPanel) + TabBar(底,100h)。AllPlayersPanel：1056×637，行 972×82(stride 98)，top50，profit 降序，盈利行金渐变发光。

---

## 7. 下注/倒计时/顶栏/历史/设置/弹窗资产

**下注态/倒计时**：`content-view/game-view/bet-phase_next-game.png`(678×124，"NEXT GAME"——⚠️ 实际已被动态绿渐变文字替代，见 §9)、`content-view/progress_container.png`(658×68) + `progress_fill.png`(650×69) + `progress_fill_mask.png`(636×50)（倒计时进度条）。
**顶栏/历史**：`content-view/btn_setting.png`(90×90 容器，实素材小) 右上齿轮；`content-view/history/history_container_bg.png`(390×35) + `_normal/_win/_loss.png`(146×64，对应 normal/profit/super) + `has-more.png`(18×24)（近 20 局历史倍率条）。
**设置面板**（全屏 z999）：`setting-page/` 下 tab 图标 `tab_icon_back`(108×72)/`setting/guide/history/exit`(72×72)、`tab_selected_aura`(216×168)、`toggle_icon_on/off`(63×63 画质)、`volume_icon_mute`(64×52)、`button_icon_language-selector`(80×80)、`history_tab_container`(314×100)、`history_divider_line`(847×7)、`section_header_line`(208×12)、`history-item_icon_copy`(28×28)。
**教程面板** `tutorial-panel/`（首次进入，5 步）：`tutorial_logo_{en,zh,tr}.png`(580×300)、`sample.bet-selector.png`(546×91)、`sample.multipliers.png`(689×46)、`branch.left/right.png`(369/371×228)、`arrow.flow.png`(26×50)、`arrow.branch.png`(64×54)、`icon.money-bag.png`(64×64)。
**弹窗** `popup/button_popup_confirm.png`(342×98)。Toast/Warning/Language 面板边框是 **canvas 程序绘制**（对角渐变 #65F4FA→#FEF988 描边 + #101E35α0.8 底）。

> **程序化绘制**（非图片，运行时 Graphics/Canvas 按 theme 画）：TopBar 底色、toast/warning/language 渐变描边框、设置分割线、各面板裁切 mask、SettlementPanel 黑幕 vignette + 光条 tint。

---

## 8. 音频（2 BGM + 8 SFX）

`public/assets/audios/`，别名见 `SoundDefs.ts`：

| 别名 | 文件 | gain | 触发时机 |
|---|---|---|---|
| `BGM.NORMAL` | `bgm/bgm.mp3` | 0.8 loop | 主背景乐（ENTER_GAME + 教程 gate 后播） |
| `BGM.CHEERING` | `bgm/bgm_crowded_cheering_loop.mp3` | 1.0 loop（SFX 通道） | **看台欢呼 loop**，套现后并行叠播 |
| `SFX.CLICK` | `sfx/click_normal.mp3` | — | 通用 UI 点击 |
| `SFX.BET` | `sfx/click_bet.mp3` | — | 下注 |
| `SFX.COUNTDOWN` | `sfx/effect_count-down.mp3` | — | 下注倒计时 5→1s（每秒） |
| `SFX.GAME_START` | `sfx/effect_game-start.mp3` | — | 开球（kickoff 序列 100ms） |
| `SFX.KICK_RUN` | `sfx/effect_soccer-kick-run.mp3` | **4.0** | 开球助跑（kickoff 0ms） |
| `SFX.KICK` | `sfx/effect_soccer-kick.mp3` | **2.0** | 踢球瞬间 |
| `SFX.GAME_OVER` | `sfx/effect_game-over.mp3` | — | 撞毁（未套现） |
| `SFX.CASHOUT` | `sfx/effect_cashout.mp3` | — | 套现成功 |

BGM 走独占通道；SFX overlay；`AudioManager` fadeIn 0.5s、iOS 可见性自恢复。

---

## 9. 复现注意（踩坑铁律 + 孤儿）

1. **信 runtime 不信旧文件**：how-to-play 足球=真主角（非污染）；cg02a 的"足球"才是从 cg01 继承的残留。
2. **固定画布无相机**：足球飞行靠 **bgLayer `calcBgScale(m)` 对数缩放 + 火球拖尾 + 速度线/模糊升级**营造升空，**非相机/视差**。复现按 calcBgScale 控制点 + 150ms lerp 还原。
3. **原生尺寸 ≠ 上屏尺寸**：spine 按 §2 代码 scale 还原（idle ×1.38、soccer panelScale≈1.63、trophy ×2.0、digits 图集）。
4. **单注栏**：无 A/B 双注、无 quick-bet 行（区别于 cg02a/cg03）；只有 BetSwitcher ±。
5. **mock ≠ real**：倍率曲线/crash 点/AC 阈值/bet 档位由服务端下发；`DummySocket` 的值（曲线随机[1,1000]、AC 分层、VP 500-1000）是 dev 占位（见 GDD §2）。
6. **孤儿/未用**（复现勿生成）：`effects/gameplay-flying/particle.png`、`content-view/game-view/bet-phase_next-game.png`（已被动态绿渐变文字替代）、`player-hud/all-players/bg_all-players.png`、`CashOut/soccer.png`（cashout 用 banner/ratio/youwin，不用 soccer）；**音频** `sfx/effect_soccer-catch.mp3`（未在 SoundDefs 接线，疑孤儿）。`digits_gold` 系统预留未激活。

---

## 10. 交叉引用
- 玩法/状态机/经济（相位/下注/套现/倍率/排行榜）→ [GDD-CG01.md](GDD-CG01.md)
- 每屏每态布局/坐标/UI 行为/动画时序 → [UI-GREYBOX-CG01.html](UI-GREYBOX-CG01.html)
- 本系列方法论 → [../skills/reverse-game-to-triad/SKILL.md](../skills/reverse-game-to-triad/SKILL.md)
