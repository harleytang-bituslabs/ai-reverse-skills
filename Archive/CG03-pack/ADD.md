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

---

## §1 风格锚点

- 关键词：扁平卡通像素风, 2.5D 斜俯视, 小鸡过马路, 高饱和不刺眼, 国际化无文化符号
- 色板：暖黄 `#FFEB3B`, 草绿(安全 / GO) `#4CAF50`, 路面灰 `#424242`, 警示(STOP / 撞车) `#E53935`, 金奖(翻金井盖 / WIN) `#FFD54F`, 文本白 `#FFFFFF`(+浅蓝描边), 次级文本 `#8899AA` / `#667788`, 覆层底 黑 50% / 设置覆层深蓝 `#112E60` 85%
- 气氛图：`assets/tile_start.png`（横向卷轴开始帧 / 场景基调，风格锚点参考，关联 §7）；`assets/chicken_character_front.png`（主角小鸡造型锚点）

---

## §2 屏幕与区块布局

| 屏幕 | 区块 | 位置 | 内容 |
|---|---|---|---|
| loading | 加载区 | 全屏 | 加载背景 + 游戏 Logo + 进度条 + 错误 / 重连面板 |
| idle_play | 顶栏区 | 顶部 | 顶栏背景 + 货币符号 + 余额 + 设置入口 |
| idle_play | 场景区 | 画面中央 | 起跑线 / 鸡舍开始帧 + 小鸡待机 |
| idle_play | 控制区 | 底部 | 投注输入 + 快捷筹码 + 赛道选择器 + PLAY 按钮 |
| idle_difficulty_dropdown | 赛道弹层 | 覆盖控制区 | 4 赛道下拉选项 + 选中高亮 |
| run_main | 赔率区 | 场景上方 / 鸡身下 | 当前倍率 banner + 前方 2 格倍率气泡 |
| run_main | 场景区 | 画面中央 | 横向卷轴马路 + 小鸡 + 井盖 + 背景车流 |
| run_main | 控制区 | 底部 | STOP（左）+ GO（右主，预告下一格倍率）+ 可收金额 |
| win_banner / super_win | 胜利覆层 | 满屏 | YOU WIN / MAX WIN 横幅 + 金额 / 倍率 + Play Again / Share / History |
| bust_overlay | 撞车覆层 | 满屏 | BUST + 撞车前倍率（仅展示）+ Play Again / History |
| settings | 设定区 | 全屏 | Sound / Image Quality + 底部导航 |
| settings_language_picker | 语言弹层 | 覆盖设定区 | 语言选择器 + 选项弹层 |
| guide | 说明区 | 全屏 | how-to-play 标题 + 规则正文 |
| history | 历史区 | 全屏 | 日期范围筛选 + 注单表 + 复制 |
| network_error_popup | 异常弹窗 | 覆层 | 网络断开 / 货币错误 / 登录过期文案 + reload |

---

## §3 组件需求清单（审签对象主表）

| ID | 屏幕/区块 | 组件 | 需求描述 | 状态变体 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-C-001 | loading/加载区 | 加载背景 loading_bg | 全屏加载底图 | idle | P1 | 无 | — |
| ART-C-002 | loading/加载区 | 游戏 Logo game_logo | 游戏名 logo，3 语言变体（en / zh / tr），烘焙进图片 | idle | P0 | logo_cluckDash_en.png | baked，语言变体见 §6 |
| ART-C-003 | loading/加载区 | 进度条 progress_bar | container + filled（左→右填充） | idle | P1 | 无 | — |
| ART-C-004 | loading/加载区 | 开始按钮 start_button | 加载完成后的进入按钮 | idle/hover/pressed | P0 | 无 | idle / hover / pressed 三态 |
| ART-C-005 | loading/加载区 | 错误 / 重连面板 error_panel | 错误底板 + reload 按钮 + 提示面板底（普通 / 加深 2 版） | idle/hover/clicked | P1 | 无 | reload 三态；见 GDD §5 |
| ART-C-006 | idle_play/顶栏区 | 顶栏背景 top_bar_bg | HUD chrome 顶栏底 | idle | P1 | 无 | — |
| ART-C-007 | idle_play/顶栏区 | 货币符号图标 currency_icon | 余额显示用，CNY / PHP / USD + 通用符号回退 | idle | P1 | 无 | 三币种见 §8 |
| ART-C-008 | idle_play/顶栏区 | 设置入口图标 settings_icon | 右上角齿轮，进入设定覆层 | idle | P1 | 无 | 共用框架见 §8 |
| ART-C-009 | run_main/控制区 | HUD 背景板 hud_bg | 底部控制区背景板 | idle | P1 | 无 | — |
| ART-C-010 | idle_play/控制区 | 投注输入容器 bet_input_container | 显示当前投注额，可双击编辑 | idle | P0 | 无 | 步进 / 精度见 GDD §6 |
| ART-C-011 | run_main/控制区 | GO 按钮 btn_go | 主操作，按钮上预告下一格倍率（如 GO! ×1.45），草绿；详见 §3b | idle/hover/pressed | P0 | btn_go_idle.png / btn_go_hover.png / btn_go_pressed.png | idle / hover / pressed 三态 |
| ART-C-012 | run_main/控制区 | 收款按钮 btn_cashout | STOP 收款，红 / 警告描边，区别于 GO；收款请求期间禁用；详见 §3b | idle/hover/pressed/disabled | P0 | btn_cashout_idle.png | idle / hover / pressed 三态；disabled 为设计新增态（视觉：置灰） |
| ART-C-013 | idle_play/控制区 | 开始按钮 btn_play | 待机时的 PLAY，草绿，按下锁定投注进入第 1 格 | idle/hover/pressed | P0 | 无 | idle / hover / pressed 三态 |
| ART-C-014 | idle_play/控制区 | 投注减 btn_min_adjust | 投注额减档 | idle/hover/pressed | P1 | 无 | idle / hover / pressed 三态 |
| ART-C-015 | idle_play/控制区 | 投注加 btn_max_adjust | 投注额加档 | idle/hover/pressed | P1 | 无 | idle / hover / pressed 三态 |
| ART-C-016 | idle_play/控制区 | 快捷筹码 btn_quick_bet | 快捷筹码累加（1 / 2 / 5 / 10） | idle/hover/pressed | P1 | 无 | idle / hover / pressed 三态 |
| ART-C-017 | idle_difficulty_dropdown/赛道弹层 | 难度选择器 difficulty_selector | 容器 base + 展开 / 收起图标 + 弹层底 + 选中高亮（共 5 件） | idle | P0 | difficulty_popup_background.png | 4 赛道变体见 §3a |
| ART-C-018 | run_main/赔率区 | 当前倍率 banner current_multiplier_banner | 鸡身下 / HUD 大数字底板，实时 current_multiplier，过格滚动刷新 | idle | P0 | 无 | baked/overlay 见 §6；刻度值 TBC（GDD §4） |
| ART-C-019 | run_main/赔率区 | 倍率气泡 multiplier_bubble | 前方 2 格井盖上的倍率气泡样式，高对比可读 | idle | P0 | 无 | 视野见 §3b；数值 TBC（GDD §4） |
| ART-C-020 | win_banner/胜利覆层 | WIN 横幅 win_banner | YOU WIN 文字图 + 金额 / 倍率 label 底 | idle | P0 | label_youWinBanner.png | 终点态叠 MAX WIN；动效见 ART-M-008 |
| ART-C-021 | run_main/场景区 | 开始帧 scene_start | 第 1 格：鸡舍 / 农场入口 / 起跑线（入场动画起点），详见 §3a | idle | P0 | tile_start.png | 视觉见 §3a |
| ART-C-022 | run_main/场景区 | 中间帧路面 scene_mid | 起始 tile + 路面循环 strip + 车道分隔虚线，横向无缝平铺，详见 §3a | idle | P0 | 无 | 可平铺；视觉见 §3a |
| ART-C-023 | run_main/场景区 | 终点帧 scene_end | 安全岛 / 超级胜利终点 tile + finishline（双向）+ 终点旗，详见 §3a | idle | P0 | 无 | 强制结算庆祝在此 |
| ART-C-024 | run_main/场景区 | 背景景观池 bg_landscape | 景观平铺 tile + 水面 + 建筑剪影（程序化背景元素） | idle | P1 | 无 | — |
| ART-C-025 | run_main/场景区 | 井盖 manhole | 路径记忆与倍率锁定载体，多态视觉见 §3a | manhole_hidden/manhole_gold/manhole_gold_bonus | P0 | manhole_gold.png | 视觉见 §3a |
| ART-C-026 | run_main/场景区 | 小鸡主角 chicken | 唯一可玩角色，承载全部玩法态 | idle/jump/win/die | P0 | chicken_character_front.png | idle 3 变体循环；动效见 ART-M |
| ART-C-027 | run_main/场景区 | 障碍车池 vehicle_pool | 巴士 + 卡车（绿 / 橙）+ 轿车（粉 / 黄）色变体池（约 5 种）；背景车流与撞击车共用视觉 | idle | P0 | 无 | 撞击车视觉一致 |
| ART-C-028 | run_main/场景区 | 路障 road_barrier | 草绿简化几何，安全过格时从地面弹出挡车 | idle | P1 | 无 | 动效见 ART-M-004 |
| ART-C-029 | run_main/场景区 | 货币粒子 currency_particle | 金币 + 美钞，WIN / 终点金币雨 / 余额视觉 | idle | P1 | 无 | 源分列金币 / 美钞两项，此处按同一粒子系统合并；动效见 ART-M-008 |
| ART-C-030 | settings/设定区 | 底部导航 bottom_nav | settings / guide / history / exit / back + container + 通用 hover overlay（共 6 件 + overlay） | idle/hover | P1 | 无 | 共用框架见 §8 |
| ART-C-031 | settings/设定区 | 装饰件 decorators | header 组合 + 左右装饰 + 长 / 短分隔线 + section divider（约 7 件，静态） | idle | P2 | 无 | 共用框架见 §8 |
| ART-C-032 | settings_language_picker/语言弹层 | 语言选择器 language_selector | 切换图标 + 容器 + 弹层面板 + 选项底（上 / 中 / 下 3 段）（共 6 件） | idle | P1 | 无 | 共用框架见 §8 |
| ART-C-033 | history/历史区 | 投注记录面板 history_panel | 日期范围按钮 + 容器 + 复制图标 + 下拉箭头 + 注单表 | date_range: idle/active; container: idle/highlighted | P1 | 无 | 两组 2 态逐项定稿；状态术语用 win / bust / max_win，共用框架见 §8 |
| ART-C-034 | settings/设定区 | 画质开关 image_quality_toggle | Low / Mid / High 画质切换开关 | on/off | P2 | 无 | 共用框架见 §8 |
| ART-C-035 | settings/设定区 | 声音控制 sound_control | 静音图标（mute / unmute）+ 滑块（on / off） | on/off | P2 | 无 | 共用框架见 §8 |
| ART-C-036 | guide/说明区 | 玩法说明面板 guide_panel | how-to-play 标题 + 规则正文 | idle | P2 | 无 | 正文 TBC（§9） |
| ART-C-037 | network_error_popup/异常弹窗 | 网络错误弹窗 network_error_popup | 网络断开 / 货币错误 / 登录过期提示 + reload | idle | P1 | 无 | 见 GDD §5，文案复用公版 exceptions（§8） |
| ART-C-038 | run_main/场景区 | 静态井盖装饰 manhole_decor | 井盖静态 decor 版：灰井盖（含小鸡 icon）+ 金井盖，装饰摆放用，区别于 ART-C-025 的 spine 动画版 | gray_chicken/gold | P2 | manhole_gold.png | 与 §3a 井盖状态矩阵同视觉语言 |
| ART-C-039 | win_banner/胜利覆层 | 结算按钮组 settlement_buttons | Play Again 主按钮 + Share / History 次按钮（WIN 覆层含 Share；BUST 覆层仅 Play Again + History），主题色通用按钮 | idle/hover/pressed | P1 | 无 | 文案 key 见 §6；覆层布局见 §2 |

规则：状态变体列逐项显式声明（多态组件如 chicken、manhole、btn_go / btn_cashout 列出全部态，静态件为 idle 单态）；ART-C 编号连续无重复；参考图列文件均登记于 §7。

<!-- module: board=lane-scene -->
### §3a 场景分段与难度变体

场景分段表（横向卷轴三段，向左滚动，路面横向无缝平铺）：

| 段 | 标识符 | 位置 | 视觉 |
|---|---|---|---|
| 开始帧 | `scene_start` | 第 1 格 | 鸡舍 / 农场入口 / 起跑线，小鸡入场动画从此出 |
| 中间帧 | `scene_mid` | 第 2 ~ 倒数第 2 格 | 标准马路 + 车道分隔虚线 + 井盖，循环图块可平铺 |
| 终点帧 | `scene_end` | 最后 1 格 | 安全岛 / 彩带 / 终点旗，强制结算庆祝在此 |

井盖状态矩阵（场景内路径记忆与倍率锁定）：

| 井盖状态 | 标识符 | 视觉 |
|---|---|---|
| 未翻 | `manhole_hidden` | 灰色井盖（未走过） |
| 翻金 | `manhole_gold` | 金色井盖 + 锁定倍率数字（安全跳过该格后） |
| 翻金 + 加成 | `manhole_gold_bonus` | 金井盖 + 倍率 + ✦/✦✦/✦✦✦ 粒子（翻盖判定为 bonus 档时） |

难度变体表（目录级变体声明）：

| 赛道 | 标识符 | 车道数 | 视觉变体 |
|---|---|---|---|
| Country / Easy | `track_country` | 28 | v1 共用同一套场景美术 |
| Town / Medium | `track_town` | 22 | v1 共用同一套场景美术 |
| City / Hard | `track_city` | 18 | v1 共用同一套场景美术 |
| Highway / Extreme | `track_highway` | 14 | v1 共用同一套场景美术 |

> v1：4 赛道**共用全部美术**（场景 / 井盖 / 车辆 / 小鸡 / 动画 / 音效），赛道间**只有数学差异**（车道数、逐格倍率、单步撞车概率、翻盖分布，均见 GDD §4 / §6 TBC）。视觉换皮留待后续。

<!-- module: interaction=crash-step -->
### §3b 步进 / 倍率条展示与按钮约定

倍率随过格前进：当前倍率 banner 从旧值**滚动**到新值（过格后逐格倍率 + 翻盖加成）；前方 2 格井盖上以倍率气泡预告下一格预期，第 3 格起不预告；刻度 / 数值以数学组倍率曲线为准（TBC，见 GDD §4 / §6）。

按钮色彩与交互态约定：

| 交互态 | 主操作按钮 | 颜色约定 | 状态变体 | 参考图 |
|---|---|---|---|---|
| 待机（idle / betting） | PLAY 开始 / Play Again | 草绿 | idle/hover/pressed | 无 |
| 决策（at_tile） | GO 继续（按钮预告下一格倍率 GO! ×n） | 草绿 | idle/hover/pressed | btn_go_idle.png / btn_go_hover.png / btn_go_pressed.png |
| 决策（at_tile） | STOP 收款 | 红 / 警告（区别于草绿 GO） | idle/hover/pressed | btn_cashout_idle.png |
| 收款中 | STOP disabled | 置灰 | disabled | 无 |

「STOP / GO」按钮位于底部（STOP 左、GO 右主），尺寸倾向对称同宽。

---

## §4 动效需求清单

| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-M-001 | loading→idle_play | 入场 loading_intro | 鸡舍门开，小鸡探头 | 0.8s / loading 就绪 | P1 | chicken_character_front.png | — |
| ART-M-002 | idle_play/场景区 | 待机 chicken_idle | 头部浮动 + 偶尔眨眼 | 循环 / idle | P1 | chicken_character_front.png | idle 3 变体 |
| ART-M-003 | idle_play→run_main | 起跑 chicken_dash_start | 鸡冲出鸡舍，世界开始左卷 | 0.4s / PLAY | P0 | 无 | — |
| ART-M-004 | run_main/场景区 | 安全单跳 hop_safe | 起跳 squash → 世界左卷 → 路障弹出 → 落地 → 井盖翻金 → 倍率滚动 | 0.8~1.0s / GO safe | P0 | 无 | — |
| ART-M-005 | run_main/场景区 | 撞车 hop_crash | 车侧面冲入碰撞 → 红闪 + 震动 → 小鸡升天 + 羽毛漫天 | 0.5s 撞击 + 1.0s 升天 / crash | P0 | 无 | 用爆裂 sprite（pixelexplode）+ 羽毛 |
| ART-M-006 | run_main/场景区 | 翻盖加成 reveal_bonus | 三档强度递增：小闪 / 闪光环 / 满屏粒子 | 0.5 / 0.8 / 1.2s / reveal 判定 | P1 | 无 | 用 pixelDot 小点粒子 |
| ART-M-007 | run_main/场景区 | 井盖翻金 manhole_flip | 灰 → 金渐变 + 倍率数字浮起 | ~0.3s / 安全落地后 | P1 | manhole_gold.png | manhole spine |
| ART-M-008 | win_banner/胜利覆层 | 终点庆祝 finish_celebrate | 冲断彩带 → 金币雨 + 满堂彩 → MAX WIN 票据 | 0.6s + 1.5~2.5s / reach_end | P0 | label_youWinBanner.png | 用 coin / dollar + ribbon 粒子 |
| ART-M-009 | super_win/胜利覆层 | 超级胜利 super_win | 大字 + 皇冠小鸡 + 满屏粒子 | 2.5s / super_win 阈值 | P1 | 无 | 阈值 TBC（GDD §6） |
| ART-M-010 | 覆层/通用 | 覆层滑入 overlay_slide | 顶部下滑覆层（settings / 弹窗） | 0.3s / overlay 打开 | P2 | 无 | — |
| ART-M-011 | run_main/场景区 | 运动拖尾 chicken_trail | 小鸡跳跃 trail 贴图 | 跟随 hop | P2 | 无 | 弱机可降级（见 GDD §5 / TDD 降级策略） |

规格停在需求清单级，不作逐帧规格。

---

## §5 音效需求清单

| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-S-001 | 全局 | 按钮点击 sfx_click | 所有按钮通用点击音 | 点击触发 | P1 | 无 | — |
| ART-S-002 | run_main | 跳跃 sfx_jump | 小鸡起跳（boing） | 起跳触发 | P0 | 无 | 挂 chicken jump |
| ART-S-003 | run_main | 落地 sfx_land | 落地 squash | 落地触发 | P0 | 无 | 挂 chicken land |
| ART-S-004 | run_main | 撞死 sfx_die | 小鸡被撞哀鸣 | crash 触发 | P0 | 无 | 挂 chicken die |
| ART-S-005 | run_main | 刹车 sfx_brake | 障碍车刹车（3 变体随机） | 障碍车逼近 | P1 | 无 | 3 变体 |
| ART-S-006 | run_main | 车流路过 sfx_pass_by | 背景车流穿过（2 变体随机） | 背景车流 | P2 | 无 | 2 变体 |
| ART-S-007 | run_main | 收款 sfx_cashout | STOP 成功结算 | cashout 触发 | P0 | 无 | — |
| ART-S-008 | win_banner | 胜利 sfx_win | 胜利 / 终点 jingle | win / reach_end | P0 | 无 | — |
| ART-S-009 | 全局 | 主循环 bgm | 轻松田野 / 车流氛围调性，循环 | 全程循环 | P1 | 无 | 1 条 BGM |

规格停在需求清单级，不作逐轨规格。路障弹出 / 翻盖档 / 终点庆典等事件音若复用上述基础 SFX 则不另列，由下游按事件复用收敛。

---

## §6 文案 / 本地化

baked-text 政策：游戏 Logo **烘焙**进图片（`baked`，出 en / zh / tr 三语言变体图）；其余 UI 功能文字默认 `overlay`（运行时文本层叠加，走 i18n 以支持三语言切换）；how-to-play 正文与依据不足者标 `TBC`。缺此政策为不合格。字体 / 容器需对多语言长度有弹性。

| key | en | zh | baked/overlay |
|---|---|---|---|
| game_logo | Cluck Dash | 小鸡狂奔 | baked |
| play_label | PLAY | 開始 | overlay |
| go_label | GO | 繼續 | overlay |
| stop_label | Cash Out | 收款 | overlay |
| bet_label | Bet | 下注 | overlay |
| balance_label | Balance | 餘額 | overlay |
| win_title | YOU WIN | 你贏了 | overlay |
| max_win_title | MAX WIN | 最大獎 | overlay |
| bust_title | BUST | 撞車 | overlay |
| play_again | Play Again | 再玩一局 | overlay |
| share_label | Share | 分享 | overlay |
| history_label | History | 記錄 | overlay |
| guide_body | TBC | TBC | TBC |
| disclaimer | In the event of any dispute, HyberGaming's final interpretation shall prevail. | TBC | overlay |

> 语言：en / zh / tr 三语。zh 为繁体中文；`tr` locale 文件当前落地为繁中（locale 命名与内容差异一句带过，详见 `../_common/locale.md`）。tr 键值与完整三语言键表待本地化表定稿（见 §9 TBC）。

---

## §7 参考图清单

| 文件 | 关联章节/组件ID | provenance | caption | 已知冲突 |
|---|---|---|---|---|
| logo_cluckDash_en.png | ART-C-002 / §1 | normative | 游戏 Logo 英文变体：CLUCK DASH，烘焙进图片 | 无 |
| chicken_character_front.png | §1 / ART-C-026 / ART-M-001 | normative | 主角小鸡正面造型：圆润身形 + 红色鸡冠视觉焦点 | 无 |
| tile_start.png | §1 / §3a / ART-C-021 | normative | 横向卷轴开始帧：鸡舍 / 起跑线，场景基调锚点 | 无 |
| manhole_gold.png | §3a / ART-C-025 / ART-C-038 / ART-M-007 | normative | 井盖翻金态：金色井盖，倍率锁定载体（静态 decor 版同视觉） | 无 |
| btn_go_idle.png | §3b / ART-C-011 | normative | GO 按钮 idle 态：草绿主操作按钮 | 无 |
| btn_go_hover.png | §3b / ART-C-011 | normative | GO 按钮 hover 态 | 无 |
| btn_go_pressed.png | §3b / ART-C-011 | normative | GO 按钮 pressed 态 | 无 |
| btn_cashout_idle.png | §3b / ART-C-012 | normative | STOP 收款按钮 idle 态：红 / 警告，区别于草绿 GO | 无 |
| difficulty_popup_background.png | §3a / ART-C-017 | normative | 难度选择器弹层底板：4 赛道下拉容器 | 无 |
| label_youWinBanner.png | ART-C-020 / ART-M-008 | normative | YOU WIN 胜利横幅文字图 | 无 |

provenance 四值：`normative` / `illustrative` / `foreign-theme` / `placeholder`。本包参考图为本作视觉基准图，视觉即需求，故全部 `normative`。文图冲突时以文本 + changelog delta 为准。

---

## §8 共用壳引用

| 模块 | 路径 | 本作差异 |
|---|---|---|
| history | ../_common/history.md | 注单玩法字段 track / totalLanes / lanesAdvanced / finalMultiplier / result(win\|bust\|max_win) / revealBonusTotal / betAmount / payout；删 slot 专属字段 |
| locale | ../_common/locale.md | en / zh / tr 三语；tr 文件当前落地为繁中（命名与内容差异，见模块说明） |
| currency | ../_common/currency.md | CNY / PHP / USD 三币种；千分位 + 小数精度按币种 TBC（§9） |
| session | ../_common/session.md | 会话续局；**不做挂机超时强制结算**（裁剪挂机阈值那条） |
| exceptions | ../_common/exceptions.md | 用断线重连 / 余额不足 / 会话过期 / 维护 / 重复登入子集；crash 玩法不涉及 slot 专属异常 |
| params | ../_common/params.md | 局中续局过期时长 pending（§9）；断线宽限沿用公版 |
| telemetry | ../_common/telemetry.md | 通用信封全用；业务事件 game_start / hop / cashout / bust / reach_end / super_win / track_switch / session_end |
| backoffice | ../_common/backoffice.md | 注单表 + 限红；投注区间按币种 pending（§9） |

Settings / Language / Guide / History 屏承接与 CG01~CG05 共用的框架（见上表对应模块）。

---

## §9 TBC + 签字区

### TBC 表

| item | owner | 影响范围 |
|---|---|---|
| 4 赛道逐格倍率曲线（M1） | 数学组 | §3b 倍率 banner / 气泡刻度 |
| 4 赛道单步撞车概率（M2） | 数学组 | 撞车节奏 / 演出 |
| 翻盖加成 4 档占比与加成数值（M3） | 数学组 | §3a 井盖 bonus 档 / ART-M-006 |
| 整体 RTP 目标（M4） | 数学组 | 数值校验 |
| 单局 Max Win 上限（M5） | 数学组 | 终点结算展示 |
| SUPER WIN 触发阈值（M6） | 数学组 | ART-M-009 super_win 触发 |
| 投注步进 / 精度 / 区间（各币种，M7） | 产品 + BackOffice | ART-C-010 投注输入 |
| 各币种金额显示小数位规则 | 设计 + 数据 | 投注 / 派彩数字显示 |
| how-to-play 规则正文（三语言） | PM + 本地化 | ART-C-036 guide 面板 |
| 完整三语言键表（en / zh / tr） | 本地化 | §6 文案落地 |
| 基准分辨率 / 适配尺寸 | 产品 + 前端 | §2 屏幕布局 |
| 局中续局过期时长 | 产品 | §8 session / params |
| `buy_bonus_popup` 残留屏去留 | 产品 + 设计 | 屏幕清单范围 |
| 色板具体 hex 落地校准 | 设计 | §1 风格锚点 |

### 签字表

| 角色 | 姓名 | 日期 | 冻结范围 |
|---|---|---|---|
| Design Lead |  |  |  |
| Game PM |  |  |  |
| Art Reviewer |  |  |  |

### Changelog

| 版本 | 日期 | delta |
|---|---|---|
| v1.0.0 | 2026-07-02 | 初版：crash-step × lane-scene 双轴定型；§3 组件清单 37 项（状态变体逐项定稿）；§3a 场景分段 / 井盖状态 / 4 赛道变体；§3b GO / STOP / PLAY 按钮态；§4 动效 11 项；§5 音效 9 项（真实清单 11 SFX + BGM 归并）；数学项归并 §9 TBC |
| v1.0.1 | 2026-07-02 | 补静态井盖装饰（ART-C-038）与结算按钮组（ART-C-039，含 Share，§6 补 share_label / history_label）；ART-C-029 备注合并口径；ART-C-033 变体值校准（container: idle/highlighted）；btn_cashout disabled 标注为设计新增态 |
