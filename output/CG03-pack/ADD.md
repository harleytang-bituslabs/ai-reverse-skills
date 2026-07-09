---
project: CG03
doc: ADD
interaction: crash-step
board: lane-scene
status: draft
owner: Design Lead (TBC)
---

# CG03 Cluck Dash 小鸡狂奔 · ADD（美术与设计需求）

> 本文是美术审签对象 + auto-art 视觉输入。审签方在 §9 签字冻结；auto-art 从 §3 组件清单 + 品类模块段（§3a/§3b）+ §7 图清单机械提取输入。
> 文本永远为 normative：文图冲突时以文本 + changelog delta 为准，参考图仅作结构 / 气氛参照。
> 本版（v1.1.0）几何 / 时长 / 色板已实测定稿（设计画布 1080×1920）；备注列「实测」值为规格基准。

---

## §1 风格锚点

- 关键词：体素/像素方块(Crossy-Road 式), 2.5D 斜俯视, 小鸡过马路, 深夜霓虹马路, 高饱和不刺眼, 国际化无文化符号
- 色板：深蓝夜空底 `#14171C`~`#3B3C50`(游戏区), 像素 UI 青蓝 文字`#DAEAFF` / 面板`#2B71BE`(α0.6) / 卡底`#14223F`(α0.55) / 分割`#A2C0E6`, 草绿(GO/安全) , 橙金(CASH OUT/金井盖/金币) , 警示红(撞车红闪) , 覆层黑 50% / 设置遮罩深蓝 85%（hex 精调见 §9）
- 气氛图：`tile_start.png`（横向卷轴开始帧 / 场景基调）；`chicken_character_front.png`（主角小鸡造型锚点）（≥1，关联 §7）

---

## §2 屏幕与区块布局

| 屏幕 | 区块 | 位置 | 内容 |
|---|---|---|---|
| loading | 加载区 | 全屏 | 农场插画背景 + Logo(940 宽@top40) + 进度条(734×76@top1727,车头灯游标) + LOADING 文字 + 百分比 |
| loading_done | 开始区 | 全屏 | 同上背景;进度条淡出,**开始按钮 720×306@top952** 淡入(Game Start) |
| maintenance | 异常区 | 全屏 | 背景 + 提示面板(878 宽@bottom12%) + 右上退出钮 66px(仅 backURL) |
| error_modal | 错误弹窗 | 覆层 | 错误面板 + reload 按钮(vw 单位特例,随视口缩放) |
| betting | 顶栏区 | 顶部 1080×131 | 顶栏底 + 余额 48px + 币种图标 64² + 设置齿轮 90² |
| betting | 场景区 | 中央(y131..1188) | 起跑帧 + 小鸡待机 + 前方 2 个待机井盖 |
| betting | 控制区 | 底部 1080×869(y1051) | 注额行(MIN/输入显示/MAX) + 快选 5 钮 + 难度选择器 + PLAY 大钮 |
| difficulty_dropdown | 赛道弹层 | 控制区上方 | 4 赛道下拉(997×506 向上弹出,顶入场景区) + 选中高亮 |
| flying | 赔率区 | 小鸡下方/右上 | 当前倍率横幅 188×116(小鸡脚下) + 下一格倍率气泡 + 右上累计加成横幅 292×110 |
| flying | 场景区 | 中央 | 横向卷轴马路 + 小鸡 + 井盖 + 路障 + 背景车流 |
| flying | 控制区 | 底部 | CASHOUT(左,含可收金额)+ GO(右,预告 {next}x)双钮 494×372 |
| crashed | 场景内演出 | 中央 | 车压顶 + 全屏红闪 + 小鸡倒地(**无独立覆层**,4s 自动回) |
| cashout_win | 场景内演出 | 场景上部 | YOU WIN 横幅 634×175 + 金额滚动 + 金币彩带雨(**无按钮**,4s 自动回) |
| ultimate_win | 场景内过场 | 全场景 | 半速大跳 + 终点线/旗 + 横幅下移 + 金渐变大字 + 雨(10s 自动回) |
| settings | 设定区 | 全屏覆层 z999 | 标题区 144 + 内容滚动区 + 底部 5-tab 导航 180 |
| language_picker | 语言弹层 | 居中 800×960 | 3 语言行 548×114 + 遮罩 |
| guide | 说明区 | 设定区内页 | how-to-play 4 分页图文(滚动) |
| history | 历史区 | 设定区内页 | 统计 3 列头 + 注单虚拟列表(行 1016×120) + 3 日期筛选 tab |
| warning_popup | 异常弹窗 | 居中 976×576 | 断线/会话文案 + reload 按钮(队列式) |
| toast | 非模态提示 | 下方 y≈1720 | 882×179 面板,3s 自动隐(余额不足/重连倒数等) |

---

## §3 组件需求清单（审签对象主表）

| ID | 屏幕/区块 | 组件 | 需求描述 | 状态变体 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-C-001 | loading/加载区 | 加载背景 loading_bg | 全屏农场插画底图 | idle | P1 | 无 | 实测 1080×1936(cover) |
| ART-C-002 | loading/加载区 | 游戏 Logo game_logo | 游戏名 logo,3 语言变体(en/zh/tr),烘焙进图片;上屏 940 宽 | idle | P0 | logo_cluckDash_en.png | baked;实测 en 1356×490 / zh 1318×526 / tr 1324×536 |
| ART-C-003 | loading/加载区 | 进度条 progress_bar | container 734×76 + filled 700×46(clip-path 左→右) + **车头灯游标**(8px 暖黄光柱随进度,1.4s 脉动) + 百分比 48px | idle | P1 | 无 | 实测 top1727 居中 |
| ART-C-004 | loading/加载区 | 开始按钮 start_button | 加载完成后的进入按钮 720×306(Game Start 74px 叠字) | idle/hover/pressed | P0 | 无 | 实测 top952;hover 1.15/active 0.9 |
| ART-C-005 | loading/加载区 | 错误 / 重连面板 error_panel | 错误底板 975×574 + reload 按钮 294×103 + 提示面板底(普通/加深 2 版 878 宽) | idle/hover/clicked | P1 | 无 | reload 三态;弹窗用 vw 单位(随视口) |
| ART-C-006 | betting/顶栏区 | 顶栏背景 top_bar_bg | HUD chrome 顶栏底 1080×131 | idle | P1 | 无 | 实测 |
| ART-C-007 | betting/顶栏区 | 货币符号图标 currency_icon | 余额显示用,CNY/PHP/USD + 通用符号回退;上屏 64×64 | idle | P1 | 无 | 三币种见 §8 |
| ART-C-008 | betting/顶栏区 | 设置入口图标 settings_icon | 右上角齿轮 90×90(中心 951,65.5) | idle | P1 | 无 | 共用框架见 §8 |
| ART-C-009 | flying/控制区 | HUD 背景板 hud_bg | 底部控制区背景板 1080×869(y1051) | idle | P1 | 无 | 实测 |
| ART-C-010 | betting/控制区 | 投注显示容器 bet_input_container | 显示当前投注额 761×134(金额 72px+币符 52px);**无手动输入**,由 MIN/MAX/快选置值 | idle/locked | P0 | 无 | 实测;锁定 tint 0xDDDDDD α0.85 |
| ART-C-011 | flying/控制区 | GO 按钮 btn_go | 主操作 494×372,按钮上预告下一格倍率('GO'+'{next}x'),草绿;详见 §3b | idle/hover/pressed | P0 | btn_go_idle.png / btn_go_hover.png / btn_go_pressed.png | 三态;GO 节流 600ms+软锁 0.65s(α0.6) |
| ART-C-012 | flying/控制区 | 收款按钮 btn_cashout | CASH OUT 494×372,橙金,双行(文案+可收金额);收款请求期间置灰;详见 §3b | idle/hover/pressed/disabled | P0 | btn_cashout_idle.png | 三态+pending α0.5(设计置灰态) |
| ART-C-013 | betting/控制区 | 开始按钮 btn_play | 待机 PLAY 大钮 1011×195(文字 150px #D0FFF7),按下锁注进第 1 格 | idle/hover/pressed | P0 | btn_playGreen_idle.png | 实测;hover tint 0xFFFFBB/press 0xBBDDFF |
| ART-C-014 | betting/控制区 | 投注减 btn_min_adjust | 投注额减档 174×161 像素钮 | idle/hover/pressed | P1 | 无 | 实测 |
| ART-C-015 | betting/控制区 | 投注加 btn_max_adjust | 投注额加档 174×161 | idle/hover/pressed | P1 | 无 | 实测 |
| ART-C-016 | betting/控制区 | 快捷筹码 btn_quick_bet | **5 档直接置值**(服务端下发档位;值 64px+币icon 51²),每钮 185×126 | idle/hover/pressed/locked | P1 | 无 | 实测 行 y329;锁定 tint |
| ART-C-017 | difficulty_dropdown/赛道弹层 | 难度选择器 difficulty_selector | 容器 base 997×134 + 展开/收起 chevron 56×40 + 弹层底 997×506(向上弹) + 选中高亮行 885×124(共 5 件) | idle/open/disabled | P0 | difficulty_popup_background.png | 4 赛道见 §3a;disabled α0.5 |
| ART-C-018 | flying/赔率区 | 当前倍率横幅 current_multiplier_banner | 小鸡脚下倍率横幅 188×116,实时 eff 值 40px 白 stroke;过格滚动刷新 | idle | P0 | current_multiplier_banner.png | 实测@小鸡(x-8,y+128);hop 间隐 0.2s→0.55s 重显 |
| ART-C-019 | flying/赔率区 | 倍率气泡 multiplier_bubble | **下一格**井盖上的倍率预告 '{x}x' 54px 白 stroke 高对比;待机态显 2 个空待机井盖 | idle | P0 | 无 | 视野见 §3b;数值=难度曲线(GDD §4) |
| ART-C-020 | cashout_win/演出 | WIN 横幅 win_banner | 横幅底图 634×175(**无烧字**);YOU WIN 56px 金黄+金额 60px 运行时叠 | idle | P0 | label_youWinBanner.png | 文字 overlay(§6);通关态下移+金渐变大字 80px |
| ART-C-021 | flying/场景区 | 开始帧 scene_start | 第 1 格:鸡舍/农场入口/起跑线 672×1188 | idle | P0 | tile_start.png | 实测;详见 §3a |
| ART-C-022 | flying/场景区 | 中间帧路面 scene_mid | 车道循环 strip 316×1188(=1 格宽),横向无缝平铺 | idle | P0 | tile_road_strip.png | 实测;LANE_WIDTH=316px |
| ART-C-023 | flying/场景区 | 终点帧 scene_end | 终点 tile 1440×1188 + finishline Spine(双向) + 终点旗 Spine | idle | P0 | 无 | 提前 3 格入列;通关庆祝在此 |
| ART-C-024 | flying/场景区 | 背景景观池 bg_landscape | 像素地景 tile 654×1188 + 水面 tile + 建筑剪影(程序化摆放) | idle | P1 | 无 | — |
| ART-C-025 | flying/场景区 | 井盖 manhole | 路径记忆与倍率载体,Spine(205×195 显示),多态见 §3a | manhole_hidden/manhole_current/manhole_gold/manhole_gold_bonus | P0 | manhole_gold.png | 当前格隐预览(小鸡+横幅遮) |
| ART-C-026 | flying/场景区 | 小鸡主角 chicken | 唯一可玩角色 Spine,上屏 312×312(脚线 pivot 156) | idle/jump/win/die | P0 | chicken_character_front.png | 实测;jump→idle1 每 hop |
| ART-C-027 | flying/场景区 | 障碍车池 vehicle_pool | 巴士+卡车(绿/橙)+轿车(粉/黄)5 种(235×423 级);背景车流与撞击车共用 | idle | P0 | decor_pixelCarYellow.png | 实测;穿行 80%/急刹 60% 概率演出 |
| ART-C-028 | flying/场景区 | 路障 road_barrier | 337×175(上屏 298×154 底锚),安全过格时弹出挡车(spring 0.2s) | idle | P1 | decor_roadBarrier.png | 实测 |
| ART-C-029 | 演出/通用 | 货币粒子 currency_particle | 金币序列(goldcoin 4×2 图集,挂小鸡)+金币雨(coin 3×3)+彩带(ribbon 5×5)+烟花(程序粒子) | idle | P1 | goldcoin.png | 动效见 ART-M-008 |
| ART-C-030 | settings/设定区 | 底部导航 bottom_nav | 5-tab 栏 1080×180:back(icon140)/setting/guide/history/exit(icon72+label32)+选中光晕 216×168 | idle/hover/active | P1 | 无 | 实测;共用框架见 §8 |
| ART-C-031 | settings/设定区 | 装饰件 decorators | 标题区底 1080×144 + 分区线 903×2 渐变 + 各分割线(约 7 件,静态) | idle | P2 | 无 | 共用框架见 §8 |
| ART-C-032 | language_picker/语言弹层 | 语言选择器 language_selector | 切换按钮 500×100(icon 80²) + 弹层 800×960(矢量圆角 28+渐变描边) + 语言行 548×114 ×3 | idle/selected/hover | P1 | 无 | 实测;行态见备注:选中 α0.6+白描边 |
| ART-C-033 | history/历史区 | 投注记录面板 history_panel | 统计 3 列头 1016×116 + 注单行 1016×120(左态区 339+右详情 677,copy 32²) + 3 日期 tab 314×100 | date_range: idle/active; row: cashout/crashed/in_progress | P1 | 无 | 实测;行三态改色(金渐变/红/灰) |
| ART-C-034 | settings/设定区 | 声音控制 sound_control | SFX/BGM 两行:静音钮 64×52 + 3 段滑块(160×50×3,亮度=音量);**无画质设置** | on/off/partial | P2 | 无 | 实测;v1.0 的画质开关项不存在,已移除 |
| ART-C-035 | guide/说明区 | 玩法说明面板 guide_panel | 4 分页图文:步骤卡(圆角 18 深蓝板+序号圆徽 56)+难度表+按钮示意+bonus 表 | idle | P2 | 无 | 页内示例值为静态占位;正文终稿 TBC(§9) |
| ART-C-036 | warning_popup/异常弹窗 | 网络错误弹窗 warning_popup | 面板 976×576 + 标题 80px + 正文 48px + reload 钮 294×104(三态) | idle/hover/clicked | P1 | 无 | 实测;队列式;文案复用公版 exceptions(§8) |
| ART-C-037 | flying/场景区 | 静态井盖装饰 manhole_decor | 灰井盖(含小鸡 icon 版)+金井盖+烤鸡金盖 decor(309×222)+油桶鸡 104×76 | gray_chicken/gold/chicken_roast | P2 | manhole_gold.png / decor_manhole_chicken.png | 与 §3a 同视觉语言 |
| ART-C-038 | flying/赔率区 | 累计加成横幅 bonus_banner | 右上累计加成横幅 292×110(中心 931,973)+'+0.00' 54px;金币轨迹飞入时弹性脉冲 | idle/pulse | P0 | decor_bonus_banner.png | 实测;v1.1.0 新增(Model B 累计的视觉锚点) |
| ART-C-039 | toast/非模态提示 | Toast 面板 toast_panel | 882×179 面板@y≈1720,文字 48px 自适应;3s 自动隐/倒数常驻 | idle | P1 | 无 | 实测;v1.1.0 新增 |
| ART-C-040 | flying/控制区 | 注单号标签 bet_id_label | 'Bet ID: <id>' 22px α0.7(快选行上方),锁注后显示 | idle | P2 | 无 | 实测;v1.1.0 新增 |

规则：状态变体列逐项显式声明；ART-C 编号连续无重复（v1.1.0 重排：原 034 画质开关与 039 结算按钮组经实测不存在已删除，原 035-038 前移一位，038-040 为新增，映射见 §9 changelog）；参考图列文件均登记于 §7。

<!-- module: board=lane-scene -->
### §3a 场景分段与难度变体

场景分段表（横向卷轴三段，向左滚动，路面横向无缝平铺；每格 316px）：

| 段 | 标识符 | 位置 | 视觉 |
|---|---|---|---|
| 开始帧 | `scene_start` | 第 1 格前 | 鸡舍/农场入口/起跑线 672×1188,小鸡入场从此出 |
| 中间帧 | `scene_mid` | 逐格循环 | 路面 strip 316×1188 + 车道虚线 + 井盖,无缝平铺 |
| 终点帧 | `scene_end` | 最后 1 格后 | 终点 tile 1440×1188 + finishline Spine + 旗 Spine,通关庆祝在此 |

井盖状态矩阵：

| 井盖状态 | 标识符 | 视觉 |
|---|---|---|
| 未翻 | `manhole_hidden` | 灰井盖 + 下一格显倍率预告 '{x}x' |
| 当前格 | `manhole_current` | 隐藏预告(小鸡与倍率横幅遮盖) |
| 翻金 | `manhole_gold` | 金井盖(Spine turning-gold 皮肤,走过后) |
| 翻金+加成 | `manhole_gold_bonus` | 金井盖 + `+N%` 加成标签(三档字号 56/72/96,色 #F0F8FF/#FFE680/#FFD24A) |

难度变体表（目录级变体声明）：

| 赛道 | 标识符 | 车道数 | 视觉变体 |
|---|---|---|---|
| Easy | `EASY` | 28 | v1 共用同一套场景美术 |
| Medium | `MEDIUM` | 22 | 同上 |
| Hard | `HARD` | 18 | 同上 |
| Hardcore | `HARDCORE` | 14 | 同上 |

> v1：4 赛道共用全部美术,赛道间只有数学差异(格数/倍率曲线/撞车概率/加成分布,数值见 GDD §4)。

<!-- module: interaction=crash-step -->
### §3b 步进 / 倍率条展示与按钮约定

- 当前倍率横幅(188×116,小鸡脚下)显示**有效倍率 eff**,过格从旧值滚动到新值(0.4s);右上累计加成横幅(292×110)显示 `+N%` 累计,金币轨迹(0.7s)飞入时脉冲。
- 视野:待机 2 个待机井盖;飞行中**下一格**井盖气泡 '{x}x' + GO 按钮同步预告 '{next}x';第 2 格起不预告。
- 按钮色彩与交互态约定：

| 交互态 | 主操作按钮 | 颜色约定 | 状态变体 | 参考图 |
|---|---|---|---|---|
| 待机(betting) | PLAY(1011×195) | 草绿 | idle/hover/pressed | btn_playGreen_idle.png |
| 决策(flying) | GO(494×372,含 {next}x) | 草绿 | idle/hover/pressed | btn_go_idle.png / btn_go_hover.png / btn_go_pressed.png |
| 决策(flying) | CASH OUT(494×372,含可收金额) | 橙金(区别于草绿 GO) | idle/hover/pressed | btn_cashout_idle.png |
| 收款中 | CASH OUT pending | α0.5 置灰 | disabled | 无 |

「CASH OUT / GO」并排(CASHOUT 左,GO 右),同宽 494,间距 30;GO 节流 600ms、软锁 0.65s(α0.6 不换图)。

---

## §4 动效需求清单

| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-M-001 | loading→betting | 入场过渡 loading_intro | 幕布淡出进场,小鸡与待机井盖已就位 | 0.5s / 加载完点开始 | P1 | 无 | 实测 curtain fadeOut 500ms |
| ART-M-002 | betting/场景区 | 待机 chicken_idle | 小鸡 idle 循环(Spine idle1) | 循环 / betting | P1 | chicken_character_front.png | — |
| ART-M-003 | flying/场景区 | 安全单跳 hop_safe | 起跳(jump)→世界左卷 316px→落地→身后井盖翻金→倍率滚动 | 0.2s 延迟+0.4s 滚动;翻金@0.55s / GO safe | P0 | 无 | 实测;倍率横幅隐0.2s→0.55s 重显 |
| ART-M-004 | flying/场景区 | 路障弹出 barrier_spring | 安全格路障从地面弹出挡车(scaleY spring) | 0.2s back.out @延迟0.5s | P1 | decor_roadBarrier.png | 实测;伴随急刹车演出(60% 概率) |
| ART-M-005 | flying/场景区 | 撞车 hop_crash | 车从上冲入(0.6s)+全屏红闪 α0.45×2+小鸡 die 位移 | 冲击节奏 0.65s / crash | P0 | 无 | 实测;die 0.1s;结算 4s 自动回 |
| ART-M-006 | flying/场景区 | 翻盖加成预告 reveal_bonus | 加成弹字三档强度(字号 56/72/96 上飘渐隐)+金盖翻面 | 1.0~1.4s / 落格判定 | P1 | 无 | 实测;预览翻牌 0.6s(延迟 0.32s) |
| ART-M-007 | flying/赔率区 | 加成提交轨迹 bonus_commit_trail | 金光点+火花拖尾从井盖飞向右上累计横幅,到达三层爆点+横幅脉冲 | 0.7s(提交)/0.6s(兑付) power2.inOut | P0 | decor_bonus_banner.png | 实测;v1.1.0 新增(Model B 视觉) |
| ART-M-008 | cashout_win/演出 | 兑付庆祝 cashout_celebrate | WIN 横幅弹入(0.25s back.out)+呼吸脉冲+金额滚动(0.4s)+金币彩带雨(3s)+烟花 | 兑付 ack 后 | P0 | label_youWinBanner.png | 实测;4s 自动回投注 |
| ART-M-009 | ultimate_win/过场 | 通关过场 ultimate_cinematic | 半速大跳(1.1s)+路面滚 632px(1.6s)+终点线 finish+旗 raise+横幅下移金字+雨 | LAND0.55+0.3 起链 / capTriggered | P1 | 无 | 实测;结算 10s 自动回 |
| ART-M-010 | 覆层/通用 | 弹窗弹入 popup_pop | 弹窗 α0→1+scale0.6→1(back.out);关闭反向 | 0.25s / 打开/关闭 | P2 | 无 | 实测;语言/警告/Toast 三窗同参 |
| ART-M-011 | flying/场景区 | 过路车流 traffic_pass | 背景车随机穿行(80% 概率,0.6s 直落);路障格拦停 | 空闲 0.6s 后检测/1.5s 周期 | P2 | 无 | 实测;撞击车与车流共用视觉 |

规格停在需求清单级，不作逐帧规格。

---

## §5 音效需求清单

| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-S-001 | 全局 | 按钮点击 sfx_click | 所有按钮通用点击音 | 点击触发 | P1 | 无 | click.mp3 |
| ART-S-002 | flying | 跳跃 sfx_jump | 小鸡起跳 | Spine jump 事件 | P0 | 无 | effect chick jump.mp3 |
| ART-S-003 | flying | 落地 sfx_land | 落地 squash | Spine land 事件 | P0 | 无 | effect chick land.mp3 |
| ART-S-004 | flying | 撞死 sfx_die | 小鸡被撞哀鸣 | Spine die 事件 | P0 | 无 | effect chick die.mp3 |
| ART-S-005 | flying | 刹车 sfx_brake | 障碍车急刹(3 变体随机) | 安全格急刹演出(60%) | P1 | 无 | effect car brake1/2/3.mp3 |
| ART-S-006 | flying | 车流路过 sfx_pass_by | 车穿行/撞击(2 变体随机) | 过路车/撞车 | P2 | 无 | effect car pass by1/2.mp3 |
| ART-S-007 | 演出 | 收款 sfx_cashout | CASH OUT 成功结算 | cashout ack | P0 | 无 | effect cashout.mp3 |
| ART-S-008 | 演出 | 胜利 sfx_win | 胜利/通关 jingle | win / capTriggered | P0 | 无 | effect win.mp3 |
| ART-S-009 | 全局 | 主循环 bgm | 轻松田野/车流氛围,循环 | 全程循环 | P1 | 无 | bgm.mp3(1 条) |

规格停在需求清单级，不作逐轨规格。清单与实装音频 1:1(11 SFX + 1 BGM)。

---

## §6 文案 / 本地化

baked-text 政策：游戏 Logo **烘焙**进图片（`baked`，en/zh/tr 三语言变体图）；**其余 UI 文字全部 `overlay`**（运行时文本层，i18n 三语切换）——含 YOU WIN 横幅文字（横幅底图无字，文字运行时叠加）。字体：主 UI 'Alibaba PuHuiTi 3.0'（回退 PingFang/YaHei），历史条目 'Inter'。

| key | en | zh | baked/overlay |
|---|---|---|---|
| game_logo | Cluck Dash | 小鸡狂奔 | baked |
| loading_label | LOADING... | LOADING...(硬编码不随语言) | overlay |
| start_game | Game Start | 開始遊戲(tr)/开始游戏(zh) | overlay |
| play_label | PLAY | 开始 | overlay |
| go_label | GO | 继续 | overlay |
| cashout_label | CASH OUT | 收款 | overlay |
| bet_label | Bet | 下注 | overlay |
| balance_label | Balance | 余额 | overlay |
| win_title | YOU WIN | 你赢了 | overlay |
| bet_id_label | Bet ID: {id} | 注单号: {id} | overlay |
| difficulty_names | Easy/Medium/Hard/Hardcore | 简单/中等/困难/极限 | overlay |
| language_names | English / 简体中文 / 繁體中文 | —(自名不翻译) | overlay |
| insufficient_balance | Insufficient balance | 余额不足 | overlay |
| reconnect_countdown | Auto cash out in {n}s | {n} 秒后自动收款 | overlay |
| guide_body | TBC | TBC | TBC |
| disclaimer | In the event of any dispute, the operator's final interpretation shall prevail. | TBC | overlay |

> 语言:en / zh(简体) / tr(繁体);语言选择弹层三行自名显示(English/简体中文/繁體中文)。zh 列展示值为简体基准,tr 值随本地化表(§9 TBC)。

---

## §7 参考图清单

| 文件 | 关联章节/组件ID | provenance | caption | 已知冲突 |
|---|---|---|---|---|
| logo_cluckDash_en.png | ART-C-002 / §1 | normative | 游戏 Logo 英文变体 1356×490,烘焙进图片 | 无 |
| chicken_character_front.png | §1 / ART-C-026 | normative | 主角小鸡正面造型 274×312:白色体素身形+红鸡冠 | 无 |
| tile_start.png | §1 / §3a / ART-C-021 | normative | 开始帧 672×1188:草地起跑区,场景基调锚点 | 无 |
| tile_road_strip.png | §3a / ART-C-022 | normative | 路面循环 strip 316×1188(1 格宽,无缝平铺) | 无 |
| manhole_gold.png | §3a / ART-C-025 / ART-C-037 | normative | 金井盖 257×245(decor 版,Spine 同视觉) | 无 |
| decor_manhole_chicken.png | ART-C-037 | normative | 烤鸡金井盖彩蛋 decor 309×222 | 无 |
| btn_go_idle.png | §3b / ART-C-011 | normative | GO 按钮 idle 态:草绿像素锯齿框 | 无 |
| btn_go_hover.png | §3b / ART-C-011 | normative | GO 按钮 hover 态 | 无 |
| btn_go_pressed.png | §3b / ART-C-011 | normative | GO 按钮 pressed 态 | 无 |
| btn_cashout_idle.png | §3b / ART-C-012 | normative | CASH OUT 按钮 idle 态:橙金,区别于草绿 GO | 无 |
| btn_playGreen_idle.png | §3b / ART-C-013 | normative | PLAY 大钮 idle 态 1011×195 | 无 |
| difficulty_popup_background.png | §3a / ART-C-017 | normative | 难度弹层底板 997×506(向上展开) | 无 |
| label_youWinBanner.png | ART-C-020 / ART-M-008 | normative | 胜利横幅**底图** 634×175(无烧字,文字运行时叠) | 文件名含 label 易误解为文字图,实为无字底 |
| current_multiplier_banner.png | ART-C-018 / §3b | normative | 当前倍率横幅 189×123(小鸡脚下) | 无 |
| decor_bonus_banner.png | ART-C-038 / ART-M-007 | normative | 累计加成横幅 291×119(右上) | 无 |
| decor_pixelCarYellow.png | ART-C-027 | normative | 车辆池样例:黄色像素轿车 235×423 | 无 |
| decor_roadBarrier.png | ART-C-028 / ART-M-004 | normative | 路障 337×175(黄黑纹) | 无 |
| goldcoin.png | ART-C-029 | normative | 金币序列图集 4×2(挂角色骨骼) | 无 |

provenance 四值：`normative` / `illustrative` / `foreign-theme` / `placeholder`。本包参考图全部取自本作实装资产,视觉即需求,故全部 `normative`。文图冲突时以文本 + changelog delta 为准。

---

## §8 共用壳引用

| 模块 | 路径 | 本作差异 |
|---|---|---|
| history | ../_common/history.md | 注单字段:difficulty / totalLanes / lanesAdvanced / cashOutAt / crashPoint / cumulativeBonus / finalMultiplier(=cashOutAt×(1+cumulativeBonus)) / result(cashout\|crashed\|in_progress) / betAmount / payout / billId;窗口筛选 1/3/7 天 |
| locale | ../_common/locale.md | en / zh(简体) / tr(繁体) 三语;locale 键名 tr 落地内容为繁中 |
| currency | ../_common/currency.md | CNY / PHP / USD 三币种图标 + 通用回退;千分位 + 小数精度按币种 TBC(§9) |
| session | ../_common/session.md | 会话续局(快照恢复到原格);**3 分钟闲置 → 15s 倒数自动兑付**;断线 15s 自动兑付 |
| exceptions | ../_common/exceptions.md | 断线重连 / 余额不足 / 会话过期 / 维护 / 重复登入(SSO) 子集;告警文案服务端已本地化直显 |
| params | ../_common/params.md | 局中续局过期时长 pending(§9);ack 超时 8s;重连退避 1-5s×10 次 |
| telemetry | ../_common/telemetry.md | 通用信封全用;业务事件 game_start / hop / cashout / crash / ultimate_win / difficulty_switch / session_end |
| backoffice | ../_common/backoffice.md | 注单表 + 限红;投注区间按币种 pending(§9) |

Settings / Language / Guide / History 屏承接 CG 系共用框架(见上表对应模块)。

---

## §9 TBC + 签字区

### TBC 表

| item | owner | 影响范围 |
|---|---|---|
| 投注步进 / 精度 / 区间(各币种) | 产品 + BackOffice | ART-C-010/016 投注面板配置 |
| 各币种金额显示小数位规则 | 设计 + 数据 | 投注 / 派彩数字显示 |
| how-to-play 规则正文与配图终稿(三语言) | PM + 本地化 | ART-C-035 guide 面板 |
| 完整三语言键表(en/zh/tr) | 本地化 | §6 文案落地 |
| 局中续局过期时长 | 产品 | §8 session / params |
| 色板 hex 精调(§1 语义色落地) | 设计 | §1 风格锚点 |

### 签字表

| 角色 | 姓名 | 日期 | 冻结范围 |
|---|---|---|---|
| Design Lead |  |  |  |
| Game PM |  |  |  |
| Art Reviewer |  |  |  |

### Changelog

| 版本 | 日期 | delta |
|---|---|---|
| v1.0.0 | 2026-07-02 | 初版：crash-step × lane-scene 双轴定型；§3 组件清单 37 项；§3a 场景分段 / 井盖状态 / 4 赛道变体；§3b GO/STOP/PLAY 按钮态；§4 动效 11 项；§5 音效 9 项；数学项归并 §9 TBC |
| v1.0.1 | 2026-07-02 | 补静态井盖装饰(ART-C-038)与结算按钮组(ART-C-039,含 Share)；ART-C-029 备注合并口径；ART-C-033 变体值校准；btn_cashout disabled 标注为设计新增态 |
| v1.1.0 | 2026-07-09 | 实测定稿与勘误：**删除两项不存在组件**——原 034 画质开关(设置页仅音量+语言)与原 039 结算按钮组(结算 4s/10s 自动回投注,无 Play Again/Share;§6 同步删 play_again/share/bust 键);编号重排:原 035→034、036→035、037→036、038→037,新增 038 累计加成横幅 / 039 Toast / 040 注单号;全表补实测几何(画布 1080×1920/格宽 316/按钮与面板尺寸);§3a 赛道名定为 EASY/MEDIUM/HARD/HARDCORE、井盖矩阵补 current 态与加成三档字号色;§3b 倍率合成改乘法口径(随 GDD v1.1.0);win 横幅证实为无字底图,YOU WIN 改 overlay;§4 动效全表实测时长化+新增 bonus 提交轨迹;§5 音效与实装 11+1 逐一对应;§7 参考图 10→18 张(全 normative)并给 label_youWinBanner 标注命名歧义;§8 session 修正为存在闲置自动兑付;§9 TBC 由 14 项缩至 6 项 |
