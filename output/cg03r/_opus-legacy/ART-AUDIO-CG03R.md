---
type: prd-split
audience: art_audio
product_code: cg03r
product_name: "Cluck Dash / 小鸡狂奔"
genre: crash / step-progression (real-money)
output_profile: obsidian_md
status: reverse-engineered
triad: ART-AUDIO-CG03R.md (本文档·资产) · GDD-CG03R.md (玩法/状态) · UI-GREYBOX-CG03R.html (布局)
language: zh-CN
canvas: 1080x1920 (portrait mobile)
created: 2026-06-22
purpose: agent 训练素材 —— 喂回 auto-art 应能复现 cg03r 全套美术与音频资产
---

# cg03r「Cluck Dash / 小鸡狂奔」— Art & Audio 美术与音频文档（逆向）

> **本文档定位 / 分工**：三件套之一，只管**美术/音频资产本身**。**界面布局/坐标**见 [UI-GREYBOX-CG03R.html](UI-GREYBOX-CG03R.html)；**玩法规则/经济/网络状态**见 [GDD-CG03R.md](GDD-CG03R.md)。三份交叉引用、互不重复。
>
> **关系注记**：cg03r 是**原版**，cg03a「Jeepney Glide」是它的 reskin 衍生（cg03a 代码里 chicken/HOP 0.2+0.4 等残留注释即来自本作）。两者**同一 crash 数学/状态机框架**（难度梯、回合状态机一致），但**题材、场景系统、英雄、美术风格完全不同**。
>
> **数据来源**：`crashgame-cg03r-ui/cg03/src` 源码穷尽抽取 + `public/assets` 真实资产视觉审查。无 `.art-meta`。

---

## 1. Summary 摘要

**Cluck Dash / 小鸡狂奔** 是**逐车道递进式 crash** 真金游戏：一只体素小鸡**横向**逐车道前进（每条车道一个井盖落脚点），赔率台阶逐站上升；途中有横穿的车辆当 hazard（撞到即归零），玩家随时 **CASHOUT 套现**或 **GO 继续**。到达终点车道触发 Super Win 自动结算。

**核心循环**（数学同 cg03a，见 GDD）：
```
下注(选额+选难度路线) → PLACE BET 开局
  └→ 飞行循环: GO 跳下一车道(赔率↑/碰撞 roll) → [可能乘客 bonus 翻牌] → 抉择 CASHOUT or GO
       ├ CASHOUT → 派彩 = bet × 当前赔率 × (1+累计bonus)
       ├ 撞车(被车撞) → 归零
       └ 到终点车道 → Super Win 自动结算(ultimate)
```

## 2. 题材方向 / Style Bible

> **Step 0** 先确立并 `set_style_bible`。

### 2.1 美学方向（一句话）
**"Crossy Road 体素过马路"** —— 明亮高饱和的**低多边形 / 体素（voxel）像素块**风：方块小鸡、方块车辆、方块农场。签名记忆点：**白色体素小鸡（红冠 + 橙喙橙腿）跳过车道**。与 cg03a 的画意菲律宾+金色霓虹是**完全相反**的风格。

### 2.2 配色系统
来源：`theme/theme.json`（runtime tint，与 cg03a 同一份通用底）+ 资产视觉提取。
- **场景**：明亮日景 —— 蓝天 `#5BB8F0`、草绿 `#5BC85B`/`#3CA53C`、水蓝 `#7FC8E8`、沥青灰 `#4A4A52`、农舍红/黄。高饱和卡通。
- **底图 bg_normal**：深夜蓝 `#0E2A52` + 暗块纹理（玩法时垫底，很素）。
- **HUD chrome**：扁平**体素块** + **蓝色描边**；语义色 —— **GO/PLACE BET = 绿块**(`#3FC85A`/边 `#2B6FE0`)、**CASHOUT = 黄块**(`#F5C842`)、**当前倍率横幅 = 青块**(`#3FB8C8`)。
- 文字：HUD 主 `#DAEAFF`(浅蓝白)；YOU WIN 黄 `#FFFF00`；Grand Prize 金渐变 `#FFECA1→#E0B736`。

### 2.3 材质族（**关键签名，复现必守**）
**单一体素族**：所有块（按钮/横幅/井盖/车）都是**像素台阶边 + 蓝/深色描边 + 平涂多色块面**的 voxel/8-bit 质感，**非** cg03a 的描金 bevel/霓虹。按钮是纯色块（绿/黄/青）+ 描边，text-free（文字 runtime 叠）。

### 2.4 场景美术风格（横向车道）
- **视角**：轻 2.5D 俯视，体素卡通。
- **结构**：一条**横向车道序列** —— `tile_start`(672×1188 起步) → `tile_road_strip`(316×1188 重复车道条) ×N → `tile_end_superwin`(1440×1188 终点)。**每车道 316px 宽**，沿 X 轴排列，玩法时整条路**向左滚**（小鸡原地跳）。
- **两侧 landscape**：`bg_pixelLandscapeTile`(654×1188 草地+树+花)、`decor_water_tile`、`building-silhouette` 拼出路两旁的草地/水渠/远景。
- **难度**：4 难度共用同一套 tile/英雄美术（**不像 cg03a 每难度换皮**）；差异在数学（站数/赔率/碰撞率，见 GDD）。
- **隔离背景**：抠图 sprite 用纯品红 #FF00FF chroma-key；scene/landscape tile 与 bg 为 full-bleed。

### 2.5 不变量
- **不烧文字**：除 `logo`（每语一张）外全 text-free；倍率/金额/余额 runtime 文本叠（注：`SpriteDigits` 用 atlas 切数字，见 §6）。
- **动态特效（烟花/金币雨/彩带/红闪）是独立资产**，运行时合成。

---

## 3. 资产按屏归组

| 屏幕 | 主要资产组 |
|---|---|
| **Loading 加载** | loading bg(体素农场)、logo(×3语)、进度条(container+filled)、START 按钮(3态)、error/message 面板 |
| **Main Game 主玩法** | bg_normal、横向车道 tile(start/road_strip/end_superwin)+landscape pool、decor(车/卡车/巴士/井盖/路障/桶)、chicken/finishline/flag/manhole spine、top-bar、win/当前倍率横幅、bonus banner、player-hud 全套 |
| **Result 结算** | label_youWinBanner、Grand Prize 文字、烟花/金币雨/彩带特效 |
| **Difficulty Selector** | selector_base、icon_collapsed/expand、popup_background、popup_selected |
| **Settings 设置** | bottom-buttons、decorators、language-selector、image-quality toggle、sound-controll、back |
| **Error/Disconnect 弹窗** | error-panel/background + btn_reload(3态)、message_panel |

---

## 4. 逐资产清单（target_path / type / dims / tier / mode / origin / 描述）

### 4.1 loading/
| target_path | type | dims | tier | mode | origin | 描述 |
|---|---|---|---|---|---|---|
| `loading/game-view/background.jpg` | bg | 1080×1936 | bg | full_bleed | generate | 体素 Crossy-Road 场景：蓝天+体素云、红谷仓+风车+黄房、车道(体素车)、河流+木筏、草地、前景白体素小鸡。明亮饱和。 |
| `loading/game-title-logo/logo_cluckDash_en.png` | logo | 1356×490 | hero | regen | generate | 字标 "CLUCK DASH"（金奶油立体块字+红描边+体素小鸡+尘迹 >>>>）。 |
| `loading/game-title-logo/logo_cluckDash_zh.png` | logo | 1318×526 | hero | regen | generate | 简中 **"小鸡狂奔"**（同风格）。 |
| `loading/game-title-logo/logo_cluckDash_tr.png` | logo | 1324×536 | hero | regen | generate | 繁中字标变体。 |
| `loading/progress-bar/progress_bar_container.png` | bar(container) | 734×74 | featured | regen | generate | 进度条空轨道。 |
| `loading/progress-bar/progress_bar_filled.png` | bar(filled) | 713×51 | featured | regen | generate | 左锚点可拉伸填充条。 |
| `loading/start-button/btn_gamestart_{idle,hover,pressed}.png` | button | 719×305 | featured | regen | generate | START 按钮**三态**（体素块）；text-free。 |
| `loading/error-panel/background.png` | panel | 975×574 | support | regen | generate | 通用错误面板底。 |
| `loading/error-panel/btn_reload_{idle,hover,clicked}.png` | button | 294×103 | chrome | regen | generate | reload 按钮三态。 |
| `loading/message_panel_background.png` / `_deepened.png` | panel | 878×184 / 878×238 | support | regen | generate | 消息面板底(常/加深)。 |

### 4.2 content-view/（顶栏 + 玩法横幅）
| target_path | type | dims | tier | mode | origin | 描述 |
|---|---|---|---|---|---|---|
| `content-view/top-bar/background.png` | panel | 1080×131 | chrome | regen | generate | 顶栏底条。 |
| `content-view/top-bar/icon_currency_{USD,CNY,PHP,symbol}.png` | icon | 72×72/73 | chrome | regen | generate | **多币种货币图标**（按 currencyCode 切换；symbol=兜底）。 |
| `content-view/top-bar/icon_settings.png` | icon | 90×90 | chrome | regen | generate | 设置齿轮。 |
| `content-view/game-view/win-banner/label_youWinBanner.png` | fx/hero word | 634×175 | hero | regen | generate | YOU WIN 横幅：**绿色体素圆角 banner**，内叠黄字 "YOU WIN" 60px + 金额 70px 白 + 金币(结算用)。 |
| `content-view/game-view/win-banner/current_multiplier_banner.png` | panel | 189×123 | featured | regen | generate | **当前倍率横幅**（青块，飞行时显于小鸡下方，叠 x_k 40px）。cg03a 无此件。 |
| `content-view/game-view/decor/decor_bonus_banner.png` | panel | 291×119 | featured | regen | generate | 累计 bonus 横幅（顶部右侧 292×110）。 |

### 4.3 main-game 场景（横向车道 —— 详见 §5）
| target_path | type | dims | tier | mode | origin | 描述 |
|---|---|---|---|---|---|---|
| `content-view/game-view/tile_start.png` | scene | 672×1188 | bg | full_bleed | generate | 起步段（车道起点，含 START）。 |
| `content-view/game-view/tile_road_strip.png` | scene | 316×1188 | bg | full_bleed | generate | **重复车道条**（每条=一车道，宽 316，X 向无缝平铺）。 |
| `content-view/game-view/tile_end_superwin.png` | scene | 1440×1188 | bg | full_bleed | generate | 终点 Super Win 段。 |
| `tile-asset-pool/landscape-tile/bg_pixelLandscapeTile.png` | scene | 654×1188 | bg | full_bleed | generate | 路侧草地+树+花 landscape 条。 |
| `tile-asset-pool/water-tile/decor_water_tile.png` | scene | 234×126 | bg | tile | generate | 水渠 tile。 |
| `tile-asset-pool/building-silhouette/decor_building_silhouette.png` | decor | 263×251 | bg | regen | generate | 远景楼影。 |
| `images/bg_normal.png` | bg | 1080×1920 | bg | full_bleed | generate | 玩法垫底深夜蓝体素纹（很素，在 landscape 之后）。 |

### 4.4 decor / hazard（车辆/井盖/障碍）
| target_path | type | dims | origin | 描述 |
|---|---|---|---|---|
| `tile-asset-pool/game-view/decor_pixelCar{Pink,Yellow}.png` | decor | 235×423 | generate | 体素小车（hazard，纵向横穿）。 |
| `content-view/game-view/decor/decor_pixelTruck{Green,Orange}.png` | decor | 245×443/445 | generate | 体素卡车 hazard。 |
| `content-view/game-view/decor/decor_pixelBus.png` | decor | 231×388 | generate | 体素巴士 hazard。 |
| `content-view/game-view/decor/decor_roadBarrier.png` | decor | 337×175 | generate | 路障(safe 段弹起，298×154 渲染)。 |
| `content-view/game-view/decor/decor_barrelGray.png` | decor | 257×245 | generate | 灰桶装饰。 |
| `content-view/game-view/decor/decor_manholeGold.png` | icon | 257×245 | generate | 金井盖(落脚/倍率站静态件)。 |
| `content-view/game-view/decor/decor_manhole_chicken.png` | decor | 309×222 | generate | 金色烤鸡井盖装饰(bonus/特殊标记)。 |
| `content-view/game-view/decor/decor_chicken_character_front.png` | icon | 274×312 | generate | 小鸡正面静态件(非 spine 处用)。 |

### 4.5 spine / sprite（动效源）—— 见 §6
chicken(`cg03_chara` 1356)、finishline(up/down 448)、flag(748)、manhole_cover(1088) 各 `.json+.atlas+.png`；sprite/chicken/{dollar 162×264, goldcoin 512×256}。

### 4.6 effect/（独立特效）
| target_path | dims | 描述 |
|---|---|---|
| `effect/coin.png` | 512×427 | 金币雨贴图(3×3 sheet)。 |
| `effect/ribbonelements.png` | 512×512 | 彩带贴图(5×5 sheet)。 |
| `effect/pixelDot.png` / `pixelexplode.png` / `trail.png` | 512/256/256 | 粒子(点/爆裂/拖尾)。 |

### 4.7 player-hud/（HUD 控件）
| target_path | type | dims | tier | origin | 描述 |
|---|---|---|---|---|---|
| `player-hud/background.png` | panel | 1080×869 | bg | generate | HUD 整面底图。 |
| `player-hud/buttons/btn_playGreen_{idle,hover,pressed}.png` | button | 1011×195 | featured | generate | **PLACE BET 绿块**(下注态);text-free。 |
| `player-hud/buttons/btn_cashout_{idle,hover,pressed}.png` | button | 494×372 | featured | generate | **CASHOUT 黄块**(飞行态);文字 #4D3131。 |
| `player-hud/buttons/btn_go_{idle,hover,pressed}.png` | button | 494×372 | featured | generate | **GO 绿块**(飞行态);文字 #0F6254 + 下一站倍率子行。 |
| `player-hud/buttons/btn_minAdjust/maxAdjust_{idle,hover,pressed}.png` | button | 174×161 | chrome | generate | 减/加注按钮三态。 |
| `player-hud/buttons/btn_quickBetAmount_{idle,hover,pressed}.png` | button | 234×126 | chrome | generate | 快捷投注按钮(一行 5,渲染 185×126)。 |
| `player-hud/bet-input/bet_amount_input_container.png` | panel | 997×134 | chrome | generate | 投注额输入容器(渲染 761×134)。 |
| `player-hud/difficulty_selector/selector_base.png` | panel | 761×134 | support | generate | 难度器闭合底(渲染 997×134)。 |
| `player-hud/difficulty_selector/popup_background.png` | panel | 997×506 | support | generate | 难度弹层(向上)。 |
| `player-hud/difficulty_selector/popup_selected.png` | panel | 885×124 | support | generate | 选中行高亮。 |
| `player-hud/difficulty_selector/icon_collapsed/expand.png` | icon | 56×40 | generate | chevron 收/展。 |

> ⚠️ **按钮三态多为冗余**：虽 ship idle/hover/pressed PNG，但 `ImageButton` 运行时**只用 idle + tint 派生** hover/pressed/disabled（normal#E5E5E5/hover#FFF/pressed#CCC/disabled#7F7F7F；`HudImageButton` disabled 仅变 tint 不降 alpha）。复现出 idle 即可，hover/pressed art 实为死件。

### 4.8 settings-panel/
bottom-buttons{back 140、settings/guide/history/exit 72、buttons-container 1080×180、hover_overlay 216×168}；decorators{header 左右/divider}；game-history{date_range idle/active 314×100、container idle/highlighted 990×120、icon_copy 28、icon_down_arrow 50×26}；image-quality{toggle_off/on 63}；language-selector{icon_switch 80、popup-panel 801×960、container 560×100、option-bg top/mid/bottom 548×114}；sound-controll{icon_mute/unmute 64×52、slider_off/on 160×50}。多为 <1KB 占位 stub —— **复现按真实结构重出，勿照抄空文件**。

---

## 5. 场景系统 —— 横向车道（与 cg03a 竖向 centerline 不同）

> **运行机制**（滚动/小鸡跳/车辆/碰撞/特效）见 [UI-GREYBOX-CG03R.html](UI-GREYBOX-CG03R.html) 画廊 B + 机制注释。本节只交付**要产出什么**。

- **轴向**：横向。车道沿 X 轴排列，**每车道 316px** 宽；玩法时整条路 `-=316px` 左滚一跳。
- **构成**：`tile_start`(672宽) + `tile_road_strip`(316宽)×N + `tile_end_superwin`(1440宽，含 finishline/flag spine)。两侧叠 landscape(草/水/楼影)。
- **每车道一个井盖** `manhole_cover`(spine 205×195 渲染) = 落脚/倍率站；前方井盖显**预览倍率**(54px)，落定时翻金(turning-gold anim)。
- **难度不换皮**：4 难度共用同一套 tile + 小鸡，仅数学不同。
- **复现**：路条 X 向无缝；井盖按车道间距 316 摆；终点段含升旗(flag raise)+finishline。

---

## 6. Spine / 动效源

| spine | 文件 | 上屏尺寸 | 动画/语义 |
|---|---|---|---|
| **chicken** `spine/chicken/cg03_chara` | json/atlas/png(1356) | **312×312**(pivot.y=156 脚对齐,钉死) | idle1(循环)/jump/die(碎玻璃)/win;胜利时 goldcoin 眼部脉冲 |
| **manhole_cover** `spine/manhole/` | (1088) | 205×195 | base 显倍率 / turning-gold 落定 / 金件+bonus 翻出 |
| **finishline** `spine/finishline/{up,down}` | (448) | — | 终点线 'finish' 动画(x=-366,y=-40) |
| **flag** `spine/flag/` | (748) | — | 终点旗 'raise'(x=228,y=-200) |

sprite：`goldcoin`(512×256, 4×2 sheet, 眼部脉冲)、`dollar`(162×264)。

---

## 7. 音效与 BGM

> 接线 `SoundDefs.ts`；BGM 1 + SFX 11（`audio/`，channel bgm/sfx，tag `scene:main`，loop SFX 音量 0.4）。响度建议 SFX -16 / BGM -19 LUFS。

### 7.1 BGM
| 文件 | 场景 | loop | 时长 | 描述 |
|---|---|---|---|---|
| `audio/bgm/bgm.mp3` | 主玩法(进入即播) | ✓ | 长循环(估) | 轻快卡通过马路调性。 |

### 7.2 SFX（触发取自代码）
| 别名/文件 | 触发 | 描述 |
|---|---|---|
| `sfx_click` | UI 点击 | 短促 |
| `sfx_chick_jump` | 小鸡起跳(GO) | 跳跃音 |
| `sfx_chick_land` | 小鸡落定下一井盖 | 落地音 |
| `sfx_chick_die` | 撞车死亡 | 失败音 |
| `sfx_chick_win` | 胜利/结算 | 小鸡欢呼 |
| `sfx_cashout` | CASHOUT 结算(NET_CASHOUT_DONE) | 套现音 |
| `sfx_car_pass_by1/2` | 撞车(NET_ROUND_CRASH，**50% 随机二选一**) | 车呼啸而过 |
| `sfx_car_brake1/2/3` | 车辆刹停(safe 近身/路障) | 刹车音 |

> 比 cg03a 多了**小鸡专属 jump/land/die/win + 车刹车/经过**一组。复现按触发分类制作。

---

## 8. 多语言 / 多币种
- **3 语**：en / zh(简中) / tr(繁中)。logo 每语一张烧字(`logo_cluckDash_{en,zh,tr}`)；其余 runtime 文本叠。
- **多币种**：USD/CNY/PHP（+symbol 兜底），顶栏货币图标按 `currentCurrencyCode()` 切换；金额符号 `$`，计价 **USDT**。
- **快捷投注真机为 [1,2,5,10] 4 键**（服务端 config；代码 fallback 5 键 [0.1,0.5,1,5,10]）。
- **设置-画质**：Graphics Quality 三档 Low/Med/High（`image-quality/toggle_off/on` 复选,默认 High）。

## 9. 复现说明
1. Step 0：用 §2 Style Bible `set_style_bible`（体素族 + 语义色 + 不换皮 + 品红 chroma-key + 不烧字）。
2. DESIGN：§3/§4 逐资产 design.json；scene 按 §5 横向车道 + 井盖间距 316；spine 按 §6（chicken 312×312 钉死）。
3. GENERATE：scene/landscape full_bleed；sprite 品红 chroma-key + clean_cutout；按钮只出 idle(hover/pressed 死件可省)；多币种图标各一。
4. 校验：对照本表 dims 与 `public/assets`；spine 动画名；占位件须真出。

## 10. Non-Goals
- 不做每难度换皮场景（4 难度共用 tile/英雄）；不做老虎机；不做横版独立资产。
- v1 不交付已播动画（只出 spine 静态源 + 特效源）。
- 不照搬 <1KB 占位 stub。

## 11. Sources
- `crashgame-cg03r-ui/cg03/public/assets/**`（资产+尺寸视觉审查）
- `cg03/src/game/project/scenes/MainScene/**`、`network/{CluckDashSocket,RealSocket}.ts`、`SoundDefs.ts`
- `cg03/public/assets/theme/theme.json`、`src/assets/localizations/*`

---

**ADD 结束（逆向版）。玩法见 GDD-CG03R.md；界面布局见 UI-GREYBOX-CG03R.html。**
