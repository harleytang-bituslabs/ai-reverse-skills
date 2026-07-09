# ART-AUDIO-CG05 · MineBeach(海滩扫雷)美术与音频设计文档

> **来源锚点**:`crashgame-cg05-ui @ 65b8ced`;资产根 `cg05/public/assets/`(128 物理文件,逐文件全量见 `elements-CG05.json.assets`,本文只列**逻辑主体资产**并折叠组合件)。
> 徽标:全文 **code-derived**(部署形态零截图,原生尺寸=盘上实测,上屏尺寸=源码常量换算)。
> 玩法/状态机见 `GDD-CG05.md`;逐屏几何与动画时长唯一权威在 `UI-GREYBOX-CG05.html`。

---

## §0 Style Bible(一句话美学 + 不变量)

**阳光手绘卡通海滩**:高饱和沙金 + 海洋青蓝,圆润厚涂质感(非 cg03 像素/体素风)。

- **60-30-10 配色**:60% 沙金(沙块/滩地 `#E8C27A~#F2D9A0` 族)+ 30% 海洋青蓝(天空/水面/HUD 玻璃蓝 `#2B71BE`、深海设置底)+ 10% 强调(GO 绿=第三钮、警示橙金描边、金币金 `#FED027~#FFEF73`)。UI 框架色板(theme.json):textPrimary #FFF / settingOverlayBg #112E60 α0.85 / tab 渐变字 #D7E6ED→#4AD1EA / 历史三态盒 绿(cashout)/橙红(minehit)/金(perfectclear)。
- **材质族**:①手绘厚涂(背景/沙块/logo);②玻璃果冻钮(蓝底橙金描边 btn_bet_mines / 绿底 btn_start_cashout);③木框羊皮纸(loading 错误面板/维护面板/进度条);④深夜蓝面板(弹层 bet/mines 纯色深蓝 speech-bubble、语言弹窗矢量渐变描边)。
- **不变量**:文字全 overlay 不烧字(唯 logo 烧字出 en/zh/tr 三张);按钮三态=独立贴图(`_idle/_hover/_pressed`);特效大半**程序化**(屏裂/爆炸粒子/星火=Graphics,非贴图);字体 Alibaba PuHuiTi 3.0(注单/Toast 用 Inter);金额两位小数。
- **像素风残留(有意保留的上屏事实)**:YOU WIN 底横幅 `label_youWinBanner`(cg03 像素绿横幅)直接复用于卡通海滩之上;雷数/投注弹层的展开箭头 `icon_collapsed/expand` 为像素阶梯形。复现时按现状保留,除非重制。

## §1 玩法 → 美术适配表

| 玩法机制(GDD) | 美术承接 |
|---|---|
| 5×5 翻格 | 7 种沙块盖面(贝壳/素面/脚印/海星/卵石等)按固定美学矩阵铺排,避免重复感;翻开=半透明棕底 rect + 金币/炸弹 |
| 倍率上爬 | TopBar 倍率条:沙金长条 + 蓝 pill 档位链,当前档换金 pill(icon_current_mul),箭头翻页 |
| 雷数选择 | 顶部两张计数卡(金币卡=安全格数 / 炸弹卡=雷数)实时联动;弹层 4×6 数字矩阵 |
| 收款/通关 | YOU WIN 横幅+金额;通关加 Grand Prize 金渐变大字 + 金币/彩带雨(coin 3×3、ribbon 5×5 图集) |
| 踩雷 | 格内火药爆(程序粒子)+ 全屏屏裂白闪震动(程序化,代码注释标注"占位美术,可换设计资产") |
| 断线/异常 | 木框羊皮纸弹窗(error_panel)+ Toast 深蓝横条 |

## §2 屏幕与场景系统

- **屏清单**(19 帧全集在灰盒):loading(进度/就绪)、维护、退出确认(vw 弹窗)、主场景×6 态(betting/playing/双弹层/兑付/踩雷/通关)、Toast、Warning、设置×3 页、语言弹窗;超屏 SCENES=倍率梯全条(22 档×143px=3146px)+ 历史虚拟长列表。
- **主场景合成**(单屏统一,无内容/HUD 视觉分带):bg_normal 全屏 → TopBar(场内 logo 640 宽+倍率条+计数卡+齿轮)→ 盘面 920×920 居中(y≈694,跨中/下分区)→ 余额条 997×109(y≈1624)→ 三钮行 322×108×3(y≈1761)。分区/层序/驱动信号契约见灰盒注释面板③。
- **场景(超屏)形态**:本作无长地图;"超一屏"的是**倍率梯内容条**(mask 内横向滚)与**注单虚拟列表**(1208 视口内纵向滚)。

## §3 资产子表 · 场景与盘面(content-view/game-view + images,34 文件)

| 资产(族) | 原生尺寸 | 上屏 | 说明 |
|---|---|---|---|
| images/bg_normal.png | 2160×3840 | 1080×1920 | 主背景 2x:上 1/3 天海棕榈,下 2/3 沙滩(贝壳/海星/脚印点缀);ContentView 宽匹配铺满 |
| images/bg_setting.png | 1080×1922 | 全屏 | 设置页海底光柱场景 |
| grid_1..7.png(族 7 张) | 180×182~188 | 盖面@格 184 | 沙块盖面 7 变体:1 贝壳卵石/2 素面/3 脚印/4 海星/5 素面/6 双贝/7 素面;固定矩阵铺排(MinesGrid LAYOUT) |
| coin.png | 125×128 | ≤150 | 翻开安全格的星星金币 |
| mines.png | 123×128 | ≤150 | 翻开雷格的黑色炸弹(点燃引信) |
| rect.png | 184×184 | 184² | 翻开格半透明棕底板 |
| win-banner/label_youWinBanner.png | 634×175 | 634×175 | YOU WIN 底横幅(**无字底**,像素绿,cg03 复用);文字运行时叠 |
| win-banner/current_multiplier_banner.png | 189×123 | — | 仅 Guide 死代码别名引用,主玩法未上屏 |
| decor/ 6 张(族) | 245~337 宽 | Guide 页 | cg03 遗留(体素鸡/金井盖/烤鸡盖/橙卡车/路障/灰桶),别名 guide_* 供 GuidePage 旧 mock(现死代码);tile_road_strip 316×1188 同族 |
| tile_start.png | 672×1188 | — | **孤儿**(cg03 起跑帧遗留,零引用) |

## §4 资产子表 · TopBar 与 HUD 控件(content-view/top-bar 12 + player-hud 26)

| 资产(族) | 原生尺寸 | 上屏 | 说明 |
|---|---|---|---|
| loading/game-title-logo/logo_mineBeach_{en,zh,tr}(族 3) | 1007×562 / 1545×1007 / 1524×994 | 场内 640 宽 / 入场箱 940×525 | 烧字 logo:Mine=熔岩橙+水雷,Beach=水蓝+棕榈浪花;pt 回退 en |
| top-bar/bar_multiplier.png | 2000×192 | 997×96 | 倍率条沙金长底(嵌卵石) |
| top-bar/icon_multiplier.png / icon_current_mul.png | 118×68 / 132×77 | chipH 78.7 | 档位 pill:蓝=普通,金=当前档(换贴图不换 scale) |
| top-bar/icon_left/right.png(族 2) | 63×78 / 55×70 | 66.7×82.6 | 翻页箭头(右箭头强制与左同尺寸);按下 α0.75 |
| top-bar/icon_coins.png / icon_mines.png | 146×176 ×2 | 146×176 | 计数卡:蓝玻璃圆角卡+金币/炸弹浮雕;计数 46px 白 stroke #2a3a6b |
| top-bar/icon_settings.png | 212×212 | 90×90 | 深蓝圆角齿轮钮(993.5,75.5) |
| top-bar/icon_currency_{CNY,PHP,USD,symbol}(族 4) | 72×72 | 56~64 | 币种圆徽;symbol=通用回退(BRL 等) |
| player-hud/buttons/btn_bet_mines_{idle,hover,pressed}(族 3) | 334×112 | 322×108 | 蓝果冻钮(Bet/Mines 共用底);橙金描边 |
| player-hud/buttons/btn_start_cashout_{idle,hover,pressed}(族 3) | 334×112 | 322×108 | 绿果冻钮(第三钮恒此底,overlay 换面) |
| player-hud/buttons/icon_bet/icon_mines/icon_cashout/icon_refresh(族 4) | 52²/52²/76×78/68×68 | 图上标 | 白筹码/白炸弹线稿/金星币/白循环箭头(refresh 面高 76px) |
| player-hud/bet-input/balance_win_container.png | 880×96 | 997×108.8 | 余额/盈利横条(蓝 pill 橙金边,中央结) |
| player-hud/bet-input/bet_background.png | 940×2082 | 470×1041 | 投注弹层深蓝气泡(50% 渲染,底部尾巴 33.4% 宽) |
| player-hud/bet-input/icon_line.png / icon_rect.png / icon_selector.png | 928×8 / 1×1 / 456×280 | 半尺寸 | 弹层分隔线/命中区/选中高亮框(456×280→228×140) |
| player-hud/difficulty_selector/mines_background.png | 1856×1794 | 928×898 | 雷数弹层深蓝气泡(尾巴 38.66% 宽) |
| player-hud/difficulty_selector/icon_{hline,vline,rect,selector,collapsed,expand}+popup_*+selector_base(族 8) | 见 elements | 半尺寸 | 弹层格线/选中框/像素箭头;popup_background 997×506 与 selector_base 761×134 为该目录旧组件(未上屏主链) |
| player-hud/buttons/btn_quickBetAmount_idle.png | 234×126 | (隐藏) | 快选钮底——quickBetLayer.visible=false,实装不上屏 |

## §5 资产子表 · 弹窗与 loading 壳(loading 15 + effect 2)

| 资产(族) | 原生尺寸 | 上屏 | 说明 |
|---|---|---|---|
| loading/game-view/background.jpg | 1080×1920 | cover | 入场高细节沙滩插画(宝箱+发光符文水雷+贝壳);loading/维护屏共用 |
| loading/progress-bar/progress_bar_{container,filled}(族 2) | 1000×78 ×2 | 734×76 / 700×46 | 木框橙边进度条+绿色填充;车灯游标为 CSS 径向渐变(非贴图) |
| loading/start-button/btn_gamestart_{idle,hover,pressed}(族 3) | 700×214 | 560×171 | 绿果冻木框大钮;**hover/pressed 两张孤儿**(实装用 CSS scale) |
| loading/error-panel/background.png | 900×620 | 976×576 | 木框羊皮纸弹窗底(WarningPopup 拉伸至 976×576) |
| loading/error-panel/btn_reload_{idle,hover,clicked}(族 3) | 334×112 | 294×104 | 绿重载钮三态 |
| loading/message_panel_background.png | 960×192 | 882×179 | Toast 横条底(浅羊皮纸) |
| loading/message_panel_background_deepened.png | 878×238 | 878×238 | 维护屏深色面板 |
| effect/coin.png | 512×427 | 帧 68~102 | 金币雨图集 3×3=9 帧(翻面序列;族=1 图集) |
| effect/ribbonelements.png | 512×512 | 帧化 | 彩带/星星/糖果碎片图集 5×5=25 帧 |

## §6 资产子表 · 设置系统(settings-panel 43,孤儿 14)

| 资产(族) | 原生尺寸 | 上屏 | 说明 |
|---|---|---|---|
| bottom-buttons/btn_{back,settings,guide,history,exit}(+_idle 变体,族 9) | 108×52 / 72×72×8 | 原尺寸 | 青蓝 tab 图标:active/idle 双态(back 无 idle);label 36px(back 48) |
| bottom-buttons/buttons-container.png | 1080×180 | 1080×180 | tab 栏深蓝底(竖分隔已烘入) |
| bottom-buttons/hover_overlay.png | 216×168 | 216×168 | 选中光晕 |
| decorators/settings_header_combined.png | 1086×144 | 1080×144(±8 溢扫) | 页头深蓝条 |
| decorators/divider_short.png / divider_short_guide.png | 200×4 / 368×18 | 原尺寸 | 段头装饰线(设置页/指南页) |
| decorators/ 其余 4 张 | — | — | **孤儿**(divider_long/section-divider-long/decorator_small_l+r) |
| sound-controll/slider_{on,off}.png + icon_mute.png(族 3) | 160×50×2 / 64×52 | 130×50 / 64×52 | 三档音量块(on α=进度)+静音钮;**icon_unmute 孤儿**(unmute 态用 tint) |
| image-quality/toggle_{on,off}.png(族 2) | 63×63 | 48×48 | 画质单选钮(Low/Med/High 三档) |
| language-selector/language_switcher_container.png + icon_switch_language.png | 560×100 / 80×80 | 500×100 / 80×80 | 语言入口钮;**弹窗 4 张 png 全孤儿**(panel+option 3 张——实装 LanguagePicker 为矢量绘制) |
| game-history/btn_date_range_{idle,active}(族 2) | 314×100 | 314×100 | 日期 tab;**生效-1/2.png(中文名)为其孤儿重复件** |
| game-history/container_{cashout,minehit,perfectclear}(族 3) | 160×40 | 160×40 | 注单结果盒 绿/橙红/金;**container_/idle/highlighted 3 张孤儿** |
| game-history/icon_copy.png / icon_down_arrow.png / line.png | 28²/48×24/847×7 | 32²/原/原 | 复制/滚动箭头/分隔线 |

## §7 音频清单(audio 6,接线 5)

| 别名 | 文件 | 触发 | 说明 |
|---|---|---|---|
| bgm:normal | bgm/bgm.mp3 | 主场景循环 | 唯一 BGM(scene tag 管理) |
| sfx:click | sfx/click.mp3 | 全局按钮(SoundBus.setClickSFX) | 通用点击 |
| sfx:cashout | sfx/effect cashout.mp3 | `net:cashout:done` | 收款成功 |
| sfx:car_pass_by1/2(族 2) | sfx/effect car pass by1/2.mp3 | `net:round:busted` 随机一支 | **踩雷爆炸音**(cg03 文件名遗留,用途已改;文件名含空格) |
| — | sfx/effect win.mp3 | 未注册 | **孤儿**(SoundDefs 无此别名;通关无专属 jingle) |

音量:BGM/SFX 双轨三档(0/⅓/⅔/1 由三块 slider 表达)+静音;设置页 crossfade 250ms。

## §8 计数对账 + 孤儿清单

- **两层对账**:本文 §3–§7 逻辑主体行(族折叠)⇔ `elements-CG05.json.assets` 128 文件全量(audio 6 / content-view 32 / effect 2 / images 2 / loading 15 / player-hud 26 / settings-panel 43 / texts 1 / theme 1);`referenced=true` 109 / **孤儿 19**。
- **孤儿 19 全列**:effect win.mp3;tile_start.png;btn_gamestart_hover/pressed;settings decorators×4(divider_long、section-divider-long、decorator_small_left/right);game-history×5(container_、container_idle、container_highlighted、生效-1、生效-2);language-selector×4(panel+option top/middle/bottom);icon_unmute.png;texts/how-to-play.md(GuidePage 实装用 locale 键 rules-p1..p4,MarkdownLoader 未接)。
- **悬挂引用 2**(引用存在文件缺失):manifest `bet_input_bg→bet-input/bet_amount_input_container.png`(随 MIN/MAX 行删除);`SettingPage:304 placeholder.png`(mute 图缺失才触发的 fallback)。
- **非资产依赖**:theme/theme.json(框架色板)、localizations 4 json(文案)、程序化特效(屏裂/爆炸/星火/纸屑=Graphics 无贴图)。

## §9 i18n / 烧字政策

烧字仅 logo(en/zh/tr 三张;pt 回退 en)。其余全部 overlay:游戏内文案 4 语言 json(en/zh/tr/pt);服务端告警文案自带三语(EnUS/ZhCN/ZhTW,pt 落 EnUS);guide 正文=locale 键(rules-p1..p4,{min}/{max} 运行时按币种注入);历史/Toast 用 Inter 字体,其余 Alibaba PuHuiTi 3.0(回退 PingFang SC/Microsoft YaHei)。硬编码不随语言:LOADING... 文字、Bet ID 前缀。
