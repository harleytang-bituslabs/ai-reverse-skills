---
project: CG05
doc: ADD
interaction: crash-step
board: grid
status: draft
owner: Xina Zhong (Design Lead)
---

# CG05 MineBeach 沙灘掃雷 · ADD（美术与设计需求）

> 本文是美术审签对象 + auto-art 视觉输入。审签方在 §9 签字冻结；auto-art 从 §3 组件清单 + 品类模块段（§3a/§3b）+ §7 图清单机械提取输入。
> 文本永远为 normative：文图冲突时以文本 + changelog delta 为准，参考图仅作结构/气氛参照。

---

## §1 风格锚点

- 关键词：夏日沙滩, 晴天, 海洋, 贝壳, 椰子树
- 色板：暖黄, 天蓝, 珊瑚橘（具体 hex 值 TBC，见 §9）
- 气氛图：`assets/s5.1_main-visual_cb8421bd.png`（风格锚点参考，关联 §7）

---

## §2 屏幕与区块布局

| 屏幕 | 区块 | 位置 | 内容 |
|---|---|---|---|
| main | 美术风格区 | 顶部 | 沙滩元素 + 游戏名 Mines Beach + Setting 入口 |
| main | 赔率区 | 盘面上方 | 即时 current_multiplier + 倍率条（下一格预期赔率） |
| main | 盘面区 | 画面中央 | 5×5 格子阵列 + 翻格动画 |
| main | 控制区 | 盘面下方 | 下注额选择 + 地雷数选择 + 开始 / Cash Out 按钮 |
| bet_panel | 选项区 | 覆盖下半屏 | Bet + 币别标题 + 默认 Bet Option（单列，超过 6 项转双列） |
| mines_select | 数字网格 | 覆盖盘面 | 3~24 数字选择，默认 4 |
| settings | 设定区 | 全屏 | Sound / Language / Image Quality |
| history | 历史区 | 全屏 | Bet Count / Total Bet / Total Profit + 注单表 |
| guide | 说明区 | 全屏 | 玩法说明标题 + 规则正文 |

---

## §3 组件需求清单（审签对象主表）

| ID | 屏幕/区块 | 组件 | 需求描述 | 状态变体 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-C-001 | main/美术风格区 | 顶部栏 top_bar | 顶部沙滩元素背景带 + 游戏名 Mines Beach 区 | idle | P0 | s5.4_top-bar_402d1702.png | 沙滩主题 |
| ART-C-002 | main/美术风格区 | 设定按钮 setting_button | 右上角进入设定页的按钮 | idle | P1 | 无 | 与共用框架一致（§8） |
| ART-C-003 | main/赔率区 | 倍率显示器 multiplier_display | 即时 current_multiplier，翻格时微幅放大，精度两位小数（如 3.72×） | idle | P0 | s5.4_multiplier_c3abd482.png | baked/overlay 见 §6 |
| ART-C-004 | main/赔率区 | 倍率条 multiplier_bar | 横向倍率刻度条，高亮当前档 + 下一格预期，详见 §3b | idle | P1 | s5.4_multiplier_c3abd482.png | 刻度值 TBC（GDD §4 完整表） |
| ART-C-005 | main/盘面区 | 盘面格子 tile | 5×5 单格，四态视觉见 §3a | tile_hidden/tile_safe_revealed/tile_mine_revealed/tile_mine_exposed | P0 | 无 | 视觉见 §3a |
| ART-C-006 | main/控制区 | 下注栏 bet_bar | 显示 bet 文字 + 图标 + 当前下注金额 | idle | P0 | s5.4_bet-bar_d559dabc.png | — |
| ART-C-007 | bet_panel/选项区 | 下注面板 bet_panel | 点 Bet 弹出：Bet + 币别标题 + Bet Option 选项区；仅选默认 Bet Option | 单列/双列 | P0 | s5.4_bet-panel-1_5ffb7a66.png | 无金额输入框（§7 已知冲突） |
| ART-C-008 | mines_select/数字网格 | 地雷数选择菜单 mines_select | 点 Mines X 弹出 3~24 数字网格，默认 4 | idle | P0 | s5.4_mines-select_58710011.png | — |
| ART-C-009 | main/控制区 | 开始按钮 start_button | 非游戏中显示，绿色 = 开始 / 新局，色彩约定见 §3b | idle | P0 | s5.2_jili-copy-1_7c26621d.png | 绿色约定见 §3b |
| ART-C-010 | main/控制区 | 收款按钮 cashout_button | 游戏中显示，红色 = Cash Out，颜色区别于其他按钮；收款请求期间禁用 | idle/disabled | P0 | s5.4_cashout-btn_21ff431f.png | 红色约定见 §3b |
| ART-C-011 | main/控制区 | 开启新局按钮 newround_button | 局结束后出现，绿色圆形循环图标 | idle | P1 | s5.4_newround-btn_98690795.png | — |
| ART-C-012 | settings/设定区 | 设定面板 settings_panel | Sound / Language / Image Quality 三区 + 底部 nav | idle | P1 | s5.4_settings_8764dd9f.png | 沙滩主题背景，共用框架见 §8 |
| ART-C-013 | history/历史区 | 历史面板 history_panel | Bet Count / Total Bet / Total Profit + 注单表 | idle | P1 | s5.4_history_48713d64.png | 状态术语用 cashout/mine_hit/perfect_clear，共用框架见 §8 |
| ART-C-014 | guide/说明区 | 玩法说明面板 guide_panel | 标题 + 规则正文 | idle | P2 | 无 | 正文 TBC（§9） |
| ART-C-015 | main/异常 | 错误 Modal error_modal | 「操作失败，请重试」提示弹窗 | idle | P1 | 无 | 见 GDD §5 |
| ART-C-016 | main/异常 | 轻提示 toast | 「余额不足」等 Toast | idle | P1 | 无 | 见 GDD §5 |
| ART-C-017 | main/胜利演出 | 满版胜利层 win_overlay | Cash Out / 完美通关 满版胜利呈现 | idle | P1 | s5.5_cashout-win_26ff8de2.png | 换沙滩主题；动效见 ART-M-003/004 |

规则：状态变体列逐项显式声明（多态组件如 tile、cashout_button 列出全部态，其余按钮当前为 idle 单态）；ART-C 编号连续无重复；参考图列文件均登记于 §7。

<!-- module: board=grid -->
### §3a 格子状态矩阵

| tile 状态 | 标识符 | 视觉 |
|---|---|---|
| 未翻开 | tile_hidden | 沙滩底图（沙子纹路） |
| 安全格翻开 | tile_safe_revealed | 显示金币（沙滩主题化） |
| 地雷翻开 | tile_mine_revealed | 地雷 + 爆炸特效（沙滩主题化） |
| 局后揭示 | tile_mine_exposed | 揭示全盘地雷位置，半透明黄色覆盖（最终由设计定夺，见 §9） |

<!-- module: interaction=crash-step -->
### §3b 步进 / 倍率条展示与按钮约定

倍率条随翻格前进，高亮当前 `current_multiplier` 档并示意下一格预期赔率；刻度数值以数学组完整倍率表为准（TBC，见 GDD §4 / §6），视觉分档可参照 GDD §4 倍率上限建议表。

按钮色彩与交互态约定：

| 交互态 | 主操作按钮 | 颜色约定 | 参考图 |
|---|---|---|---|
| 非游戏中（idle / betting） | 开始游戏 / 开启新局 | 绿色 | s5.2_jili-copy-1_7c26621d.png / s5.4_newround-btn_98690795.png |
| 游戏中（playing） | Cash Out 收款 | 红色（区别于蓝色 Bet / Mines） | s5.2_jili-copy-2_414f0cdd.png / s5.4_cashout-btn_21ff431f.png |
| 收款中 | Cash Out disabled | 置灰（具体表现 TBC） | 无 |

「Cash Out / 开始游戏」按钮尺寸倾向与 Bet、Mines 同宽。

---

## §4 动效需求清单

| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-M-001 | main/盘面区 | 新局翻面 newround_flip | 全部格子翻面（沙滩主题可考虑其他表现形式） | 300~500 ms / 新局开始 | P0 | s5.5_anim-newround_b0286fed.gif | — |
| ART-M-002 | main/盘面区 | 爆炸 explode | 单格爆炸后全部格子翻面呈现 | 触发 on_mine_hit | P0 | s5.5_anim-explode_77b0eb69.gif | — |
| ART-M-003 | main/胜利演出 | Cash Out 满版 cashout_win | 收款胜利满版呈现 | 触发 on_cashout | P0 | s5.5_cashout-win_26ff8de2.png | — |
| ART-M-004 | main/胜利演出 | 完美通关 perfect_win | Perfect Win 满版，显示赢得金额 | 触发 on_perfect_clear | P1 | 无 | 文案与独立图 TBC（§9） |

规格停在需求清单级，不作逐帧规格。

---

## §5 音效需求清单

| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-S-001 | 全局 | 音效需求集 sfx_set | 翻格 / 安全格 / 爆炸 / 收款 / 完美通关 / 背景音乐等音效，分 Background Music 与 Sound Effect 两轨（见设定屏） | 各状态触发点 | TBC | 无 | 完整音效清单 TBC（§9），源需求在外部音效需求表 |

规格停在需求清单级，不作逐轨规格。

---

## §6 文案 / 本地化

baked-text 政策：每处 UI 文字逐条声明 `baked`（烘焙进图片）或 `overlay`（运行时文本层叠加）；无依据者标 `TBC`。游戏 logo 烘焙，功能文字默认 overlay 以支持 10 语言运行时切换。完整 10 语言键表为 §9 TBC（源在外部多语言表）。

| key | en | zh-CN | baked/overlay |
|---|---|---|---|
| game_logo | MINES BEACH | 沙灘掃雷 | baked |
| rules_title | Mines Rules | 扫雷基本规则 | overlay |
| bet_label | Bet | 下注 | overlay |
| mines_label | Mines | 地雷 | overlay |
| start_label | Start | 开始 | overlay |
| cashout_label | Cash Out | 收款 | overlay |
| balance_label | Balance | 余额 | overlay |
| win_label | Win | 赢得 | overlay |
| bet_panel_title | Bet {currency} | 下注 {currency} | overlay |
| rules_overview | TBC | TBC | TBC |
| rules_set_mines | TBC | TBC | TBC |
| disclaimer | In the event of any dispute, HyberGaming's final interpretation shall prevail. | TBC | overlay |

其余 8 语言键位与 en/zh-CN 一一对应，值待多语言表定稿（见 §9 TBC）。

---

## §7 参考图清单

| 文件 | 关联章节/组件ID | provenance | caption | 已知冲突 |
|---|---|---|---|---|
| s5.1_main-visual_cb8421bd.png | §1 / ART-C-001 | illustrative | 顶部区结构占位：菜单 / MINES logo / 关闭 + 「沙灘元素」灰块 + 倍率横条 + 棋子行 | 图内含灰色占位块，最终美术待创作，非最终主视觉 |
| s5.2_jili-copy-1_7c26621d.png | §3b / ART-C-009 | foreign-theme | 非游戏中整屏：揭示盘面 + 底部 Bet / Mines + 绿色开始按钮 | 金币 / 炸弹棋子为 Jili 参考题材，需换沙滩主题 |
| s5.2_jili-copy-2_414f0cdd.png | §3b / ART-C-010 | foreign-theme | 游戏中整屏：宝箱盘面 + 底部 Bet / Mines + 红色 Cash Out | 棋子 / 宝箱为 Jili 参考题材，需换沙滩主题 |
| s5.4_top-bar_402d1702.png | ART-C-001 | illustrative | 顶部区结构：「沙灘元素」灰块 + 齿轮 Setting + 倍率横条 | 图内含灰色占位块，最终美术待创作 |
| s5.4_bet-bar_d559dabc.png | ART-C-006 | foreign-theme | 下注栏局部：Bet 20 币堆图标 + Mines 3 + Balance | 取自 Jili 参考截图，题材需换沙滩主题 |
| s5.4_bet-panel-1_5ffb7a66.png | ART-C-007 | illustrative | 单列下注面板 Bet USD：6 档选项 | 图含已删除的 Input 输入框与 JACKPOT，以文本为准 |
| s5.4_bet-panel-2_7424d7c5.png | ART-C-007 | illustrative | 双列下注面板（选项 > 6）：14 档选项 | 图含已删除的 Input 输入框与 JACKPOT，以文本为准 |
| s5.4_multiplier_c3abd482.png | ART-C-003 / ART-C-004 | illustrative | 赔率区：倍率横条红框标注即时倍率 + 下一格预期 | 图内含灰色占位块，最终美术待创作；刻度值为示意 |
| s5.4_mines-select_58710011.png | ART-C-008 | foreign-theme | 地雷数选择：1~24 数字网格覆盖盘面 | 底层盘面 / 棋子为 Jili 参考题材，需换沙滩主题 |
| s5.4_cashout-btn_21ff431f.png | ART-C-010 | foreign-theme | 收款按钮态：红色 Cashout 区别于蓝色 Bet / Mines | 取自 Jili 参考截图，题材需换沙滩主题 |
| s5.4_newround-btn_98690795.png | ART-C-011 | foreign-theme | 新局按钮：绿色圆形循环按钮 | 取自 Jili 参考截图，题材需换沙滩主题 |
| s5.4_settings_8764dd9f.png | ART-C-012 / §8 | illustrative | 设定页：Sound / Language / Image Quality + 底部 nav | 背景为 One-Piece 风占位插画，非沙滩最终美术；共用框架借页 |
| s5.4_history_48713d64.png | ART-C-013 / §8 | illustrative | 历史页：Bet Count / Total Bet / Total Profit + 注单表 | 注单状态写 Crashed（crash 术语），CG05 应为 cashout / mine_hit / perfect_clear；共用框架借页 |
| s5.5_anim-newround_b0286fed.gif | ART-M-001 | foreign-theme | 新局全格翻面动效参照 | Jili Mines 浏览器截图（含 JACKPOT / Auto），棋子题材需换沙滩主题 |
| s5.5_anim-explode_77b0eb69.gif | ART-M-002 | foreign-theme | 爆炸后全格翻面动效参照 | Jili Mines 参考画面，棋子题材需换沙滩主题 |
| s5.5_cashout-win_26ff8de2.png | ART-M-003 / ART-C-017 | foreign-theme | 收款 / 胜利满版呈现参照：YOU WIN 大字 + CASHOUT | Spribe 风 Mines（货币 FUN、星星棋子），题材需换沙滩主题 |

provenance 四值：`normative` / `illustrative` / `foreign-theme` / `placeholder`。文图冲突时以文本 + changelog delta 为准。

---

## §8 共用壳引用

| 模块 | 路径 | 本作差异 |
|---|---|---|
| history | ../_common/history.md | 注单状态枚举用 cashout / mine_hit / perfect_clear；展示 final_multiplier（如 @1.44x / @0x） |
| locale | ../_common/locale.md | 10 语言全用；设定页语言切换 |
| currency | ../_common/currency.md | CNY / PHP / USD / BRL 四币种；金额显示小数位规则待设计确认（§9） |
| session | ../_common/session.md | 单一 session 限制；断线重连续局 |
| exceptions | ../_common/exceptions.md | 余额不足 / 网络失败 / 重复登录 / 派彩失败等异常文案 |
| params | ../_common/params.md | reconnect_timeout 依运营商上限（不预设）；其余会话参数沿用公版 |
| telemetry | ../_common/telemetry.md | 通用信封全用；业务事件：session_end / bet_level_change / perfect_win_post_retention（后者与完美通关留存演出 ART-M-004 可能相关） |
| backoffice | ../_common/backoffice.md | Mines_rounds 注单表；Bet Option 档位由 BO 配置 |

Settings / History / Guide 屏承接与 CG01~CG03 共用的框架（见上表对应模块）。

---

## §9 TBC + 签字区

### TBC 表

| item | owner | 影响范围 |
|---|---|---|
| Bet Option 默认档位表（各币种） | 产品 + BackOffice | 下注面板选项数 → 单列 / 双列版面 |
| 色板具体 hex 值 | 设计 | §1 风格锚点落地 |
| 介绍页 Overview / 设定地雷数 等正文（10 语言） | PM + 本地化 | 玩法说明屏文案 |
| Perfect Win 胜利文案与独立图 | 设计 | 完美通关演出（ART-M-004） |
| tile_mine_exposed 覆盖视觉（半透明黄色待定夺） | 设计 | §3a 局后揭示态 |
| 完整音效清单 | 音效 | ART-S-001 |
| 动画需求完整清单 | 动效 | ART-M 逐项细化 |
| 金额显示小数位规则（各币种） | 设计 + 数据 | 下注 / 派彩数字显示 |
| 完整 10 语言键表 | 本地化 | §6 文案落地 |
| 沙滩主视觉气氛终稿 | 美术 | §1 风格锚点 |

### 签字表

| 角色 | 姓名 | 日期 | 冻结范围 |
|---|---|---|---|
| Design Lead |  |  |  |
| Game PM |  |  |  |
| Art Reviewer |  |  |  |

### Changelog

| 版本 | 日期 | delta |
|---|---|---|
| v1.0.1 | 2026-06-29 | 下注面板移除金额输入框，仅选默认 Bet Option；reconnect 依运营商上限处理；FE/BE Lead 记为 Jack Liao |
