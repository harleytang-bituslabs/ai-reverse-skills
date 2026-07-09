# ART-AUDIO-CG03R · Cluck Dash(小鸡狂奔)美术与音频设计文档(ADD)

> **版本锚定**:`crashgame-cg03r-ui` @ `570386d`(2026-06-30)。
> **信源**:`public/assets` 全树机扫(111 图 + 24 音频/数据)+ 亲自查看导出图;尺寸=真实像素。零截图形态,徽标止于 code-derived。
> **定位**:设计文档 + 主体资产清单(§8 分子表);逐文件机器清单同步在 `elements-CG03R.json.assets`。玩法/数学 → `GDD-CG03R.md`;屏坐标 → `UI-GREYBOX-CG03R.html`。

## 0. Style Bible

- **一句话美学**:Crossy-Road 式体素玩具街区的深夜霓虹马路——白色方块小鸡在像素车流里闯关,金币金蛋点缀,UI 为深蓝夜空上的青蓝像素锯齿框。
- **60-30-10 配色**:60% 深蓝夜空(`bg_normal`/HUD 底/`0x3B3C50` 游戏区底色);30% 青蓝像素 UI(`#DAEAFF` 文字/`0x2B71BE` 面板/`#A2C0E6` 分割线);10% 橙金强调(cashout 钮/金井盖/金蛋/金币)+ 绿色 GO/草地。
- **材质族**:体素/像素方块(角色/车辆/井盖/tile,硬边无抗锯齿)、像素锯齿边框按钮(三态换色)、半透深蓝玻璃面板(圆角 18-28,`0x14223F α0.55`/`0x2B71BE α0.60`+描边渐变)、暖黄点光(车头灯/金光)。
- **不变量**:按钮三态=**独立贴图**(idle/hover/pressed 三图,非 tint 派生);井盖=Spine(normal/turning gold 皮肤);文字不烧图,例外=logo 三语(`logo_cluckDash_en/zh/tr`)与 YOU WIN 横幅底(`win_banner`,文字 runtime 叠);运行时数值(余额/倍率/注额)一律文本层。

## 1. 场景系统(横向车道,SCENES 主体)

- **车道单元**:`LANE_WIDTH_PX=316`;每格 = `road_strip`(路面条)+ 井盖 Spine(205×195 显示)+ 可选路障(`road_barrier` 298×154,底锚 y-140)。
- **路面三段契约**:头段 `tile_start`(原生 672 宽,拉高到 1188)→ 循环车道格(逐 hop 左滚 316px)→ 尾段 `tile_end_superwin`(通关终点,提前 3 格入列)。终点线 Spine(`finishline_up/down`)@(-366,-40)+旗 Spine `flag`@(228,-200)。
- **背景层**:`bg_normal`(1080×1920 拉伸)全屏 + 游戏区 `0x3B3C50` 底色;`bg_pixelLandscapeTile`(654×1188)为像素地景 tile(资产池备用);水面 tile `decor_water_tile`。
- **车辆池**(5 种,过路车/急刹车共用):`veh_car_yellow/veh_car_pink/veh_bus/veh_truck_green/veh_truck_orange`(像素竖版车,235×423 级)。
- **井盖三态**:灰盖(normal)→ 金盖(turning gold,bonus 预告翻面)→ 烤鸡金盖(`decor_manhole_chicken`,撞车格彩蛋)+ `barrel_chicken` 装饰(104×76)。

## 2. 玩法 → 美术适配

| 玩法机制(GDD) | 美术落地 |
|---|---|
| 步进 GO(§2) | 小鸡 Spine `chicken`(312×312 显示,脚线 pivot 156)jump→idle1;路面整体左滚 316px(0.2s delay+0.4s);车道格 `manhole` 前方格显示 `{x}x` 倍率预览(54px 白 stroke) |
| 撞车(§2) | 随机车辆从上砸下(y-800→800,0.6s)+全屏红闪(α0.45×2)+小鸡 die 位移(-46,40);0.65s 冲击节奏 |
| 金井盖 bonus(§4) | 金盖翻面(0.55s 延迟)+`+50%` 式标签;**提交时**金币从井盖飞向右上 bonus 横幅(`decor_bonus_banner` 292×110 @(931,973))——`fx_pixel_dot` 领头+`fx_trail` 拖尾(0.7s),到达 `fx_pixel_explode` 三层爆点+横幅弹性脉冲 |
| 有效倍率(§4) | 小鸡头顶倍率横幅 `mult_banner`(188×116,@小鸡 x-8,y+128)显示 eff;hop 间隐 0.2s→0.55s 重显 |
| CASH OUT(§5) | `win_banner`(634×175)+YOU WIN 文案(56px 金黄描棕)+金额滚动(0.4s);金币雨+彩带雨(`coin` 3×3 图集+`ribbonelements` 5×5,3s)+烟花(程序粒子) |
| Ultimate Win(§5) | 过场:半速大跳(timeScale 0.5)+路面滚 632px(1.6s)+终点线 finish 动画+旗 raise;横幅下移至小鸡下方(y727.5)+金色大字样式 |
| 听牌感/near-miss | 安全过格时 60% 概率邻道急刹车演出(y-900→-550,0.5s,brake 音);过路车 80% 概率穿行(路障格拦停 y-540) |
| 难度换表(§3) | 难度选择器(997×134 pill,向上弹 997×506 面板四行);预览态整条车道表重铺 |

## 3. UI chrome 设计要点

- **壳层(React,1080×1920 设计画布)**:loading=农场全景插画 `background.jpg` + logo(940 宽@top40)+ 进度条(`progress_bar_container` 734×76@top1727,填充 700×46 clip-path + **车头灯游标**(8px 暖黄光柱,随进度移动,1.4s 脉动))+ LOADING...(54px@top1652)+ **开始按钮**(`btn_gamestart_idle` 720×306@top952,Game Start 74px,完成后淡入);维护面板 `message_panel_background_deepened`(878 宽@bottom12%)+ 右上退出钮(66px);错误弹窗 `error-panel/background`+`btn_reload_*`(vw 单位特例)。
- **顶栏**(1080×131):`topbar_bg` + 余额(48px `#daeaff`@19,66)+ 币种图标(64×64,USD/CNY/PHP 专图)+ 设置齿轮(90×90@951,65.5)。
- **HUD**(1080×869@y1051):`hud_bg`;注额行=MIN/MAX(174×161 像素钮)夹 `bet_input_bg`(761×134,金额 72px);快选 5 钮(185×126,`btn_quickbet`+币标 51px);**PLAY 大钮**(`btn_playGreen_*` 1011×195,150px 文字)⇄ **CASHOUT+GO 双钮**(`btn_cashout_*` 橙金/`btn_go_*` 绿,各 494×372,76px 双行文案);难度选择器(见 §2 表)。
- **设置叠层**(全屏 z999):底部 5-tab 栏(1080×180,`tab_bar_bg`+`tab_selected_aura` 216×168;back 图标 140,其余 72+32px 标签);三页=设置(SFX/BGM 三段滑块 160×50×3+静音钮/语言按钮 500×100)/指南(4 页图文,深蓝面板+金渐变分页标题 88px)/历史(统计 3 列头+虚拟列表 1016×120 行+3 日期 tab 314×100)。
- **弹窗族**(统一 0.25s back.out 弹入,α0.5 遮罩):语言选择(800×960 矢量圆角面板,3 行 548×114:en/简体中文/繁體中文)、Warning(`error_panel_bg` 976×576+`btn_reload_*` 294×104)、Toast(`toast_panel_bg` 882×179 @y 中心 1720)。

## 4. Spine 与序列帧

- **Spine 4 套**(`spine/`):`chicken`(jump/idle1/die,事件驱动音效 jump/land/die)、`manhole`(normal/turning gold)、`finishline`(up/down,hold/finish)、`flag`(hold/raise)。上屏尺寸:小鸡 312²(脚线 156,注释自证"起步猜测需目测调"→code-derived)、井盖 205×195;终点线/旗未设尺寸=Spine 原生(code-derived)。
- **序列帧/图集**:`goldcoin`(4×2,24fps,挂小鸡眼部骨骼)、`coin`(3×3 金币雨)、`ribbonelements`(5×5 彩带)、`cg03_chara` 图集页、`fx_pixel_dot/fx_trail/fx_pixel_explode`(bonus 轨迹三件)、`pixelDot/pixelexplode`(通用光斑/爆点)。
- 程序化粒子(无贴图):烟花(100 方块)、撞车红闪;另有 6 个未接线粒子类(CircleBurst/CoinRain/RibbonFall/CashOutAnim/CoinEffect/Confetti)——存量未用,如实记录。

## 5. 音频设计(11 SFX + 1 BGM;`SoundDefs.ts` ↔ 磁盘逐一核对)

| 触发 | 文件(assets/audio/) |
|---|---|
| BGM 循环 | bgm/bgm.mp3 |
| 点击 | sfx/click.mp3 |
| 小鸡跳/落/死(Spine 事件) | sfx/effect chick jump/land/die.mp3 |
| 兑付 | sfx/effect cashout.mp3 |
| 通关/胜利 | sfx/effect win.mp3 |
| 急刹(安全 near-miss,随机 1/3) | sfx/effect car brake1/2/3.mp3 |
| 过路车(撞车/穿行,随机 1/2) | sfx/effect car pass by1/2.mp3 |

## 6. 文案/i18n 与主题

- 语言 3 档:en / zh(简体中文)/ tr(繁體中文)(`LANG_DEFS` 硬编码;平台码归一 zh-hans→zh、zh-hant→tr);键表在 `src/assets/localizations`(CSV→JSON 管线);logo 按语言换图三张。
- `theme.json` 全量色板(文字 `#FFFFFF/#8899AA/#667788`、按钮四态灰、tab tint、设置遮罩 `#112E60 α0.85`);字体:UI 主字 'Alibaba PuHuiTi 3.0'(回退 PingFang/YaHei)、历史条目 'Inter'、壳层引入 Google 'Alfa Slab One'(index.css @import,外链存在性如实记录)。
- 占位/孤儿(完整性门结论):`images/placeholder.png`(静音图标缺失时兜底,脚手架注释自证)、`SpriteDigits` 空图集(未接线)、`src/assets/react.svg`(模板孤儿,零引用)、`bg:main` 与 `bg_normal` 双别名同文件。

## 7. 资产命名与派生规则

- 目录即域:`loading/`(壳)/`content-view/`(顶栏+游戏区)/`tile-asset-pool/`(车道池)/`player-hud/`/`settings-panel/`/`spine/`/`sprite/`/`effect/`/`texts/`(logo 文字图)/`theme/`。
- 按钮三态独立出图(`*_idle/_hover/_pressed`);井盖金化走 Spine 皮肤非换图;币种图标 `icon_currency_<CODE>.png` 常规化,新增币种按同规格补图即可。

## 8. 主体资产清单(111 图 + 24 音频/数据 = 135 件,分 9 子表)

> 全部为 `public/assets/` 实体文件机扫(尺寸=真实像素);cg03r 资产量小,逐件列出、不折叠。

### 8.1 loading(壳层)(15 件)

| 资产(public/assets/) | 尺寸 | 大小 |
|---|---|---|
| loading/error-panel/background.png | 975x574 | 4KB |
| loading/error-panel/btn_reload_clicked.png | 294x103 | 0KB |
| loading/error-panel/btn_reload_hover.png | 294x103 | 0KB |
| loading/error-panel/btn_reload_idle.png | 294x103 | 0KB |
| loading/game-title-logo/logo_cluckDash_en.png | 1356x490 | 148KB |
| loading/game-title-logo/logo_cluckDash_tr.png | 1324x536 | 187KB |
| loading/game-title-logo/logo_cluckDash_zh.png | 1318x526 | 167KB |
| loading/game-view/background.jpg | 1080x1936 | 186KB |
| loading/message_panel_background.png | 878x184 | 0KB |
| loading/message_panel_background_deepened.png | 878x238 | 0KB |
| loading/progress-bar/progress_bar_container.png | 734x74 | 0KB |
| loading/progress-bar/progress_bar_filled.png | 713x51 | 1KB |
| loading/start-button/btn_gamestart_hover.png | 719x305 | 49KB |
| loading/start-button/btn_gamestart_idle.png | 719x305 | 51KB |
| loading/start-button/btn_gamestart_pressed.png | 719x305 | 56KB |

### 8.2 content-view(顶栏/游戏区)(20 件)

| 资产(public/assets/) | 尺寸 | 大小 |
|---|---|---|
| content-view/game-view/decor/decor_barrelGray.png | 257x245 | 19KB |
| content-view/game-view/decor/decor_bonus_banner.png | 291x119 | 18KB |
| content-view/game-view/decor/decor_chicken_character_front.png | 274x312 | 20KB |
| content-view/game-view/decor/decor_manholeGold.png | 257x245 | 24KB |
| content-view/game-view/decor/decor_manhole_chicken.png | 309x222 | 24KB |
| content-view/game-view/decor/decor_pixelBus.png | 231x388 | 22KB |
| content-view/game-view/decor/decor_pixelTruckGreen.png | 245x443 | 27KB |
| content-view/game-view/decor/decor_pixelTruckOrange.png | 245x445 | 22KB |
| content-view/game-view/decor/decor_roadBarrier.png | 337x175 | 13KB |
| content-view/game-view/tile_end_superwin.png | 1440x1188 | 476KB |
| content-view/game-view/tile_road_strip.png | 316x1188 | 1KB |
| content-view/game-view/tile_start.png | 672x1188 | 221KB |
| content-view/game-view/win-banner/current_multiplier_banner.png | 189x123 | 1KB |
| content-view/game-view/win-banner/label_youWinBanner.png | 634x175 | 2KB |
| content-view/top-bar/background.png | 1080x131 | 2KB |
| content-view/top-bar/icon_currency_CNY.png | 72x72 | 2KB |
| content-view/top-bar/icon_currency_PHP.png | 72x72 | 2KB |
| content-view/top-bar/icon_currency_USD.png | 72x72 | 2KB |
| content-view/top-bar/icon_currency_symbol.png | 72x73 | 1KB |
| content-view/top-bar/icon_settings.png | 90x90 | 0KB |

### 8.3 tile-asset-pool(车道 tile/车辆/井盖)(5 件)

| 资产(public/assets/) | 尺寸 | 大小 |
|---|---|---|
| tile-asset-pool/building-silhouette/decor_building_silhouette.png | 263x251 | 20KB |
| tile-asset-pool/game-view/decor_pixelCarPink.png | 235x423 | 28KB |
| tile-asset-pool/game-view/decor_pixelCarYellow.png | 235x423 | 28KB |
| tile-asset-pool/landscape-tile/bg_pixelLandscapeTile.png | 654x1188 | 240KB |
| tile-asset-pool/water-tile/decor_water_tile.png | 234x126 | 0KB |

### 8.4 player-hud(下注面板)(25 件)

| 资产(public/assets/) | 尺寸 | 大小 |
|---|---|---|
| player-hud/background.png | 1080x869 | 61KB |
| player-hud/bet-input/bet_amount_input_container.png | 997x134 | 0KB |
| player-hud/buttons/btn_cashout_hover.png | 494x372 | 3KB |
| player-hud/buttons/btn_cashout_idle.png | 494x372 | 3KB |
| player-hud/buttons/btn_cashout_pressed.png | 494x372 | 3KB |
| player-hud/buttons/btn_go_hover.png | 494x372 | 3KB |
| player-hud/buttons/btn_go_idle.png | 494x372 | 3KB |
| player-hud/buttons/btn_go_pressed.png | 494x372 | 3KB |
| player-hud/buttons/btn_maxAdjust_hover.png | 174x161 | 0KB |
| player-hud/buttons/btn_maxAdjust_idle.png | 174x161 | 0KB |
| player-hud/buttons/btn_maxAdjust_pressed.png | 174x161 | 0KB |
| player-hud/buttons/btn_minAdjust_hover.png | 174x161 | 0KB |
| player-hud/buttons/btn_minAdjust_idle.png | 174x161 | 0KB |
| player-hud/buttons/btn_minAdjust_pressed.png | 174x161 | 0KB |
| player-hud/buttons/btn_playGreen_hover.png | 1011x195 | 2KB |
| player-hud/buttons/btn_playGreen_idle.png | 1011x195 | 3KB |
| player-hud/buttons/btn_playGreen_pressed.png | 1011x195 | 3KB |
| player-hud/buttons/btn_quickBetAmount_hover.png | 234x126 | 0KB |
| player-hud/buttons/btn_quickBetAmount_idle.png | 234x126 | 0KB |
| player-hud/buttons/btn_quickBetAmount_pressed.png | 234x126 | 0KB |
| player-hud/difficulty_selector/icon_collapsed.png | 56x40 | 0KB |
| player-hud/difficulty_selector/icon_expand.png | 56x40 | 0KB |
| player-hud/difficulty_selector/popup_background.png | 997x506 | 112KB |
| player-hud/difficulty_selector/popup_selected.png | 885x124 | 0KB |
| player-hud/difficulty_selector/selector_base.png | 761x134 | 0KB |

### 8.5 settings-panel(设置/历史/指南)(33 件)

| 资产(public/assets/) | 尺寸 | 大小 |
|---|---|---|
| settings-panel/bottom-buttons/btn_back.png | 140x140 | 3KB |
| settings-panel/bottom-buttons/btn_exit.png | 72x72 | 2KB |
| settings-panel/bottom-buttons/btn_guide.png | 72x72 | 3KB |
| settings-panel/bottom-buttons/btn_history.png | 72x72 | 3KB |
| settings-panel/bottom-buttons/btn_settings.png | 72x72 | 3KB |
| settings-panel/bottom-buttons/buttons-container.png | 1080x180 | 0KB |
| settings-panel/bottom-buttons/hover_overlay.png | 216x168 | 10KB |
| settings-panel/decorators/decorator_header_left.png | 123x38 | 0KB |
| settings-panel/decorators/decorator_header_right.png | 123x38 | 0KB |
| settings-panel/decorators/decorator_small_left.png | 76x4 | 0KB |
| settings-panel/decorators/decorator_small_right.png | 76x4 | 0KB |
| settings-panel/decorators/divider_long.png | 846x6 | 1KB |
| settings-panel/decorators/divider_short.png | 200x4 | 0KB |
| settings-panel/decorators/section-divider-long.png | 860x2 | 1KB |
| settings-panel/decorators/settings_header_combined.png | 1080x144 | 0KB |
| settings-panel/game-history/btn_date_range_active.png | 314x100 | 1KB |
| settings-panel/game-history/btn_date_range_idle.png | 314x100 | 1KB |
| settings-panel/game-history/container_highlighted.png | 990x120 | 0KB |
| settings-panel/game-history/container_idle.png | 990x120 | 0KB |
| settings-panel/game-history/icon_copy.png | 28x28 | 0KB |
| settings-panel/game-history/icon_down_arrow.png | 50x26 | 0KB |
| settings-panel/image-quality/toggle_off.png | 63x63 | 0KB |
| settings-panel/image-quality/toggle_on.png | 63x63 | 0KB |
| settings-panel/language-selector/icon_switch_language.png | 80x80 | 4KB |
| settings-panel/language-selector/language-selector-popup-panel.png | 801x960 | 2KB |
| settings-panel/language-selector/language_switcher_container.png | 560x100 | 0KB |
| settings-panel/language-selector/popup-language-option-background-bottom.png | 548x114 | 0KB |
| settings-panel/language-selector/popup-language-option-background-middle.png | 548x114 | 0KB |
| settings-panel/language-selector/popup-language-option-background-top.png | 548x114 | 0KB |
| settings-panel/sound-controll/icon_mute.png | 64x52 | 0KB |
| settings-panel/sound-controll/icon_unmute.png | 64x52 | 0KB |
| settings-panel/sound-controll/slider_off.png | 160x50 | 0KB |
| settings-panel/sound-controll/slider_on.png | 160x50 | 0KB |

### 8.6 spine(骨骼动画)(5 件)

| 资产(public/assets/) | 尺寸 | 大小 |
|---|---|---|
| spine/chicken/cg03_chara.png | 1356x1356 | 418KB |
| spine/finishline/finishline_down.png | 448x448 | 15KB |
| spine/finishline/finishline_up.png | 448x448 | 15KB |
| spine/flag/flag.png | 748x748 | 57KB |
| spine/manhole/manhole_cover.png | 1088x1088 | 128KB |

### 8.7 sprite/effect(序列帧/特效)(7 件)

| 资产(public/assets/) | 尺寸 | 大小 |
|---|---|---|
| effect/coin.png | 512x427 | 71KB |
| effect/pixelDot.png | 512x512 | 6KB |
| effect/pixelexplode.png | 256x256 | 13KB |
| effect/ribbonelements.png | 512x512 | 160KB |
| effect/trail.png | 256x256 | 3KB |
| sprite/chicken/dollar.png | 162x264 | 19KB |
| sprite/chicken/goldcoin.png | 512x256 | 51KB |

### 8.8 images/texts/theme(背景/文案图/主题)(1 件)

| 资产(public/assets/) | 尺寸 | 大小 |
|---|---|---|
| images/bg_normal.png | 1080x1920 | 39KB |

### 8.9 音频与数据(24 件)

| 文件 | 类型 |
|---|---|
| audio/bgm/bgm.mp3 | mp3 |
| audio/sfx/click.mp3 | mp3 |
| audio/sfx/effect car brake1.mp3 | mp3 |
| audio/sfx/effect car brake2.mp3 | mp3 |
| audio/sfx/effect car brake3.mp3 | mp3 |
| audio/sfx/effect car pass by1.mp3 | mp3 |
| audio/sfx/effect car pass by2.mp3 | mp3 |
| audio/sfx/effect cashout.mp3 | mp3 |
| audio/sfx/effect chick die.mp3 | mp3 |
| audio/sfx/effect chick jump.mp3 | mp3 |
| audio/sfx/effect chick land.mp3 | mp3 |
| audio/sfx/effect win.mp3 | mp3 |
| spine/chicken/cg03_chara.atlas | atlas |
| spine/chicken/cg03_chara.json | json |
| spine/finishline/finishline_down.atlas | atlas |
| spine/finishline/finishline_down.json | json |
| spine/finishline/finishline_up.atlas | atlas |
| spine/finishline/finishline_up.json | json |
| spine/flag/flag.atlas | atlas |
| spine/flag/flag.json | json |
| spine/manhole/manhole_cover.atlas | atlas |
| spine/manhole/manhole_cover.json | json |
| texts/how-to-play.md | md |
| theme/theme.json | json |

> 图 111 + 其它 24 = 135;与阶段0 资产树逐文件一致(机扫)。
