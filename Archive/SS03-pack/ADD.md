---
project: SS03
doc: ADD
interaction: slot
board: reel
status: draft
owner: Design Lead (TBC)
---

# SS03 Mahjong Streak 麻將連莊 · ADD（美术与设计需求）

> 本文是美术审签对象 + auto-art 视觉输入。审签方在 §9 签字冻结；auto-art 从 §3 组件清单 + 品类模块段（§3a–§3e）+ §7 图清单机械提取输入。
> 文本永远为 normative：文图冲突时以文本 + changelog delta 为准，参考图仅作结构 / 气氛参照。
> 本作 Unity 游戏层的逐项符号 / 背景 / 特效与多数玩法数值尚未定稿，相应组件的具体规格挂 §9 TBC——TBC 行数偏多是本作当前形态的预期特征。

---

## §1 风格锚点

- 关键词：麻将, 招财, 金龙, 麻将牌山, 铜钱, 孔雀绿, 金色
- 色板：孔雀绿（主背景渐变）, 金色（龙 / 牌 / 币）, 绿字（發 = 发财）, 红字（中 = 红中）（具体 hex 值 TBC，见 §9）
- 气氛图：`loadingBg_large.jpg`（麻将金龙主视觉，风格锚点参考，关联 §7）

---

## §2 屏幕与区块布局

| 屏幕 | 区块 | 位置 | 内容 |
|---|---|---|---|
| loading | 主视觉区 | 满屏 | 麻将金龙背景（2560²）+ 标题 Logo（按语言换图）+ 进度条 + Loading 文字 + 版本号 |
| main | 转轴区 | 画面中央 | 麻将转轴盘面（几何 TBC）+ 百搭 Wild + 级联消除区 |
| main | 信息栏 | 盘面上方 / 下方 | 余额 / 下注额 / 赢分显示 |
| main | 控制区 | 盘面下方 | Spin / Auto / 下注加减 / 设置入口 / 历史入口 |
| win_present | 中奖演出层 | 覆盖盘面 | Big / Super / Mega 标题图（按语言换图）+ 中奖特效 |
| paytable | 赔付表屏 | 全屏 / 覆盖 | 符号赔付倍数表 + 玩法说明 |
| free_spin_announce | 公告区 | 覆盖盘面 | 免费旋转标题 / 引导 / 开始确认（按语言换图）|
| free_spin_play | 进行区 | 盘面 + 顶部 | 累计赢分标签 + 剩余次数 |
| free_spin_end | 结束区 | 覆盖盘面 | 结束确认（按语言换图）|
| settings | 设定区 | 全屏 / 二级 | 音效 / 语言（SetLanguage）/ 速度 |
| history | 历史区 | 全屏 / 二级 | 下注纪录注单表 |
| exception | 异常层 | 满屏 | 纯 CSS 暗框（标题 + 描述）+ 可选退出按钮 + 版本号 |

---

## §3 组件需求清单（审签对象主表）

| ID | 屏幕/区块 | 组件 | 需求描述 | 状态变体 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-C-001 | loading/主视觉区 | 加载背景 loading_bg | 麻将金龙主视觉满屏背景，2560×2560 画布 `object-fit:none` 居中 | idle | P0 | loadingBg_large.jpg | 实测 2560×2560 JPG |
| ART-C-002 | loading/主视觉区 | 标题 Logo title_logo | "MAHJONG STREAK 麻將連莊" 主视觉式大 Logo，高约 700px；按语言换图（见 §3e / §6 baked） | idle | P0 | LoadingEnglishTitle.png | en 768×700 / 简繁 797×700，baked |
| ART-C-003 | loading/主视觉区 | 进度条轨道 progress_track | 进度条底框 | idle | P1 | LoadingTrack.png | 实测 963×64 |
| ART-C-004 | loading/主视觉区 | 进度条填充 progress_bar | 进度填充（clip-path inset 推进） | idle | P1 | LoadingBar.png | 实测 931×30 |
| ART-C-005 | loading/主视觉区 | 进度头精灵 progress_tip | 进度条头部提示精灵 | idle | P2 | LoadingTip.png | 实测 134×80 |
| ART-C-006 | loading/主视觉区 | Loading 文字 loading_text | 底部白字 48px bold，呼吸 3.5s；无气泡粒子 | idle | P2 | 无 | overlay（见 §6）|
| ART-C-007 | exception/异常层 | 异常容器 exception_box | 纯 CSS 暗框 960×(128~196)，圆角 36px，`rgba(35,35,45,.88)`；标题白字 52px + 描述 28px | idle | P1 | 无 | 非 PNG 面板 |
| ART-C-008 | exception/异常层 | 退出按钮 exit_button | 右上角退出图标，显示尺寸 66px（仅 URL 带 `backURL` 时显示） | idle | P1 | exit.png | 实测源图 148×148 |
| ART-C-009 | exception/异常层 | 版本号 version_label | 底部常驻版本号，白字 20px opacity .3，格式 `{env}-v{server}-{unity}` | idle | P2 | 无 | overlay |
| ART-C-010 | main/转轴区 | 游戏背景 game_bg | 麻将招财主题游戏背景（金龙 / 牌山 / 铜钱 / 孔雀绿） | idle | P0 | 无 | 主题视觉 TBC（§9）|
| ART-C-011 | main/转轴区 | 转轴框 reel_frame | 转轴盘面容器，几何尺寸依数学组（GDD §6）| idle | P0 | 无 | 盘面几何 TBC |
| ART-C-012 | main/转轴区 | 符号集 symbols | 麻将牌面符号集，视觉与语义见 §3a | idle | P0 | 无 | 符号全集 TBC（§3a）|
| ART-C-013 | main/转轴区 | 百搭 Wild wild_symbol | 麻将「百搭」万能牌符号，醒目金牌样式 | idle | P0 | 无 | 是否带倍率 TBC（GDD §6）|
| ART-C-014 | main/信息栏 | 余额 / 下注 / 赢分栏 info_bar | 余额 / 当前下注额 / 本局赢分数值显示 | idle | P0 | 无 | 数值 overlay（§6）|
| ART-C-015 | main/控制区 | Spin 按钮 spin_button | 主旋转按钮 | idle/pressed/disabled | P0 | 无 | 多态逐态声明 |
| ART-C-016 | main/控制区 | Auto 按钮 auto_button | 自动旋转开关 | idle/active | P1 | 无 | 多态逐态声明 |
| ART-C-017 | main/控制区 | 下注加减 bet_stepper | 下注额加 / 减控件 | idle/disabled | P0 | 无 | — |
| ART-C-018 | main/控制区 | 设置入口 settings_button | 进入设定屏 | idle | P1 | 无 | 共用框架（§8）|
| ART-C-019 | main/控制区 | 历史入口 history_button | 进入下注纪录屏 | idle | P1 | 无 | 共用框架（§8）|
| ART-C-020 | win_present/中奖演出层 | 中奖标题图 win_tier_title | Big / Super / Mega 中奖标题图，按语言换图，命名与矩阵见 §3c / §3e | idle | P0 | 无 | baked（§6），档数是否 >3 TBC |
| ART-C-021 | win_present/中奖演出层 | 中奖演出层 win_overlay | 达档满版中奖演出（粒子 / 金币 / 龙），`Win_Texts` / `WinEffectQA` 资产组 | idle | P0 | 无 | 特效素材 TBC（§9）|
| ART-C-022 | paytable/赔付表屏 | 赔付表面板 paytable_panel | 符号赔付倍数表 + 玩法说明，结构见 §3b | idle | P1 | 无 | 倍数与符号集 TBC（§3b）|
| ART-C-023 | free_spin_announce/公告区 | 免费旋转标题 freespin_announce_title | 免费旋转触发标题图，按语言换图 | idle | P1 | 无 | baked（§6）；命名见 §3d |
| ART-C-024 | free_spin_announce/公告区 | 免费旋转引导 freespin_guide | 玩法引导图，按语言换图 | idle | P1 | 无 | baked（§6）|
| ART-C-025 | free_spin_announce/公告区 | 开始确认 freespin_start_confirm | 开始确认屏，按语言换图 | idle | P1 | 无 | baked（§6）|
| ART-C-026 | free_spin_play/进行区 | 累计标签 freespin_total_label | 累计赢分标签，按语言换图 | idle | P1 | 无 | baked（§6）|
| ART-C-027 | free_spin_end/结束区 | 结束确认 freespin_end_confirm | 结束确认屏，按语言换图 | idle | P1 | 无 | baked（§6）|
| ART-C-028 | settings/设定区 | 设定面板 settings_panel | 音效 / 语言（SetLanguage）/ 速度三区 | idle | P1 | 无 | 共用框架（§8）|
| ART-C-029 | history/历史区 | 下注纪录面板 history_panel | 历史注单表 + 详情 | idle | P1 | 无 | 共用框架（§8）|
| ART-C-030 | main/异常 | 重连 / Toast reconnect_toast | 断线重连 / 重复登录 / 处理中等提示 | idle | P1 | 无 | 文案见共用壳 exceptions（§8）|

规则：状态变体列逐项显式声明（多态组件如 spin_button / auto_button / bet_stepper 列出全部态，其余为 idle 单态）；ART-C 编号连续无重复；参考图列文件均登记于 §7。

<!-- module: board=reel -->
### §3a 符号表

麻将牌面符号集。以下为背景主视觉可确证的符号行；**符号全集（含常规牌面全序列、Scatter、以及各符号赔付分级）为 TBC（见 §9）**。

| 符号 | 标识符 | 语义 | Wild/Scatter | 视觉 |
|---|---|---|---|---|
| 發 | `sym_fa` | 发财（绿） | 常规 | 绿字牌面 |
| 中 | `sym_zhong` | 红中（红） | 常规 | 红字牌面 |
| 萬 | `sym_wan` | 万 | 常规 | 金字牌面 |
| 八萬 | `sym_ba_wan` | 八万 | 常规 | 金字牌面 |
| 百搭 | `sym_wild` | 万能牌 | **Wild** | 醒目金牌「百搭」|
| （常规符号全序列）| `sym_*` | TBC | 常规 | TBC |
| （Scatter，若有）| `sym_scatter` | TBC | Scatter? | TBC（是否存在独立 Scatter 待数学组确认）|

<!-- module: board=reel -->
### §3b 赔付表屏视觉

赔付表屏（`paytable_panel`）向玩家展示各符号的赔付。**结构**：符号图标列 + 命中数量档（如 3 / 4 / 5 连或 cluster 数量）× 对应赔付倍数网格 + 百搭 / Scatter 说明 + 玩法（Tumble 级联）文字说明。

| 版面块 | 内容 | 状态 |
|---|---|---|
| 符号赔付网格 | 各符号 × 命中数量 → 倍数 | 倍数值 TBC（数学组，GDD §6）|
| 百搭说明 | 百搭替代规则 / 是否带倍率 | TBC |
| Scatter / Free Spin 说明 | 触发条件与奖励 | TBC（GDD §6）|
| 玩法说明 | Tumble 级联（消除 → 塌落 → 填充）图文 | 机制确证，配图 TBC |

> 赔付网格的行数（符号数）与列数（命中档）依 §3a 符号全集与 §3 盘面几何定稿后确定。

<!-- module: interaction=slot -->
### §3c win-tier 演出矩阵

中奖分档演出确证至少 **Big / Super / Mega 三档**，每档标题图按语言换图。命名规律：`win_{tier}_title_{lang}.png`，其中 `tier ∈ {big, super, mega}`，`lang` 为下列 8 个图变体键（印尼 / 马来合用一张 `id_and_my`）。

| 档 (tier) | 组件 | 命名前缀 | 语言图变体 (lang) |
|---|---|---|---|
| Big | win_tier_title | `win_big_title_*` | en / hans / hant / hindi / id_and_my / kr / th / vi |
| Super | win_tier_title | `win_super_title_*` | en / hans / hant / hindi / id_and_my / kr / th / vi |
| Mega | win_tier_title | `win_mega_title_*` | en / hans / hant / hindi / id_and_my / kr / th / vi |

> 每档 8 个语言图变体 → 每档 8 张，共 3 档。是否另有 Normal / Epic 等档为 TBC（见 §9）。标题图内文字 baked（§6）。

<!-- module: interaction=slot -->
### §3d Free Spin 层

确证存在完整 Free Spin 流程（公告 → 进行 → 结束）。各屏组件按语言换图；命名规律见下表。触发条件、免费次数、是否 retrigger 为数学组交付（GDD §6）。

| 流程屏 | 组件 | 命名前缀 | 说明 |
|---|---|---|---|
| 公告标题 | freespin_announce_title | `FreespinAnnounce_title_*` | 免费旋转触发标题 |
| 玩法引导 | freespin_guide | `FreespinAnnounce_guide_*` | 免费旋转玩法引导 |
| 开始确认 | freespin_start_confirm | `FreespinAnnounce_start_confirm_*` | 进入免费旋转前确认 |
| 累计标签 | freespin_total_label | `FreespinAnnounce_totalLabel_*` | 免费旋转累计赢分标签 |
| 结束确认 | freespin_end_confirm | `Freespin_end_confirm_*` | 免费旋转结束确认 |

> 另有 `FreespinZi` / `FreespinAnounceTextImgs` 字样图组。各组按语言出图（baked，§6）。

<!-- module: interaction=slot -->
### §3e locale × 换图矩阵

Unity 内建 **9 locale + Shared 非语言共用表**：英文(en) / 印度语(hi) / 印尼文(id) / 韩文(kr) / 马来文(my=ms-MY Malay) / 泰文(th) / 越南文(vi) / 简体中文(zh-hans) / 繁体中文(zh-hant)；locale 总数与最终语言名单待核（TBC，见 §9）。以下图组按语言换图（baked）；win-tier 与 Free Spin 图组的语言键集为 8 变体（印尼 / 马来合用 `id_and_my`），加载标题图为 3 变体（en / 简 / 繁）。

| 图组 | 组件 ID | 命名规律 | 语言键集 | baked/overlay |
|---|---|---|---|---|
| 加载标题 Logo | ART-C-002 | `Loading{English,ChineseSimp,ChineseTrad}Title.png` | en / 简 / 繁（3）| baked |
| 中奖标题（Big/Super/Mega）| ART-C-020 | `win_{tier}_title_{lang}.png` | en/hans/hant/hindi/id_and_my/kr/th/vi（8）| baked |
| 免费旋转公告组 | ART-C-023~027 | `FreespinAnnounce_{title,guide,start_confirm,totalLabel}_{lang}` / `Freespin_end_confirm_{lang}` | 按 8 语言键集出图 | baked |
| 功能文字（余额 / 下注 / 赢分等）| ART-C-014 等 | 运行时字符串（Unity StringTable / 外壳 i18n）| 9 locale | overlay |

> 语言键集差异（图变体 8 vs locale 9）是确证事实（印尼 / 马来共用一张标题图 `id_and_my`，加载标题仅出 3 语言版本）；其余语言在运行时以文本层呈现（overlay）。

---

## §4 动效需求清单

| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-M-001 | main/转轴区 | 级联消除 tumble_cascade | 中奖符号消除 → 剩余符号塌落 → 顶部空位再填充，循环直至无新中奖 | 触发 on_win（每轮消除）| P0 | 无 | Tumble 核心动效，逐帧规格 TBC |
| ART-M-002 | win_present | 中奖档演出 win_tier_present | Big / Super / Mega 满版演出（标题图入场 + 金币 / 龙特效）| 触发 达档 | P0 | 无 | 分档表现 TBC（§9）|
| ART-M-003 | main/转轴区 | 转轴滚动 reel_spin | Spin 触发的转轴滚动 → 落定 | 触发 on_spin | P0 | 无 | — |
| ART-M-004 | free_spin | 免费旋转转场 freespin_transition | 进入 / 退出 Free Spin 的公告与结束转场 | 触发 Free Spin 进 / 出 | P1 | 无 | — |

规格停在需求清单级，不作逐帧规格。

---

## §5 音效需求清单

| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-S-001 | 全局 | 音效需求集 sfx_set | BGM（常规 / Free Game）+ SFX（旋转 / 落定 / 级联消除 / 麻将牌碰撞 / 中奖分档 / 龙吟等） | 各状态触发点 | TBC | 无 | 完整音效清单不可得，整表 TBC（§9）——文件名 / 分轨 / 数量待 Unity 工程或音效交付 |

规格停在需求清单级，不作逐轨规格。

---

## §6 文案 / 本地化

baked-text 政策（本作示范点）：**标题类图片按语言换图 = baked**——加载标题 Logo、Big/Super/Mega 中奖标题、Free Spin 公告 / 引导 / 确认屏均将文字烘焙进图片，因此每语言各出一张（见 §3c/§3d/§3e 命名规律）。功能性文字（余额 / 下注 / 赢分 / 剩余次数等数值与短标签）默认 `overlay`，运行时以 Unity StringTable / 外壳 i18n 层按 9 locale 切换（另有 Shared 非语言共用表；locale 总数待核，见 §9）。完整 9 语言键表为 §9 TBC（源在 Unity Localization 表）。

| key | en | zh-hant | baked/overlay |
|---|---|---|---|
| game_logo | MAHJONG STREAK | 麻將連莊 | baked |
| win_big_title | BIG WIN | 大獎 | baked |
| win_super_title | SUPER WIN | 超級大獎 | baked |
| win_mega_title | MEGA WIN | 巨無霸大獎 | baked |
| freespin_announce_title | FREE SPIN | 免費旋轉 | baked |
| balance_label | Balance | 餘額 | overlay |
| bet_label | Bet | 下注 | overlay |
| win_label | Win | 贏分 | overlay |
| spin_label | Spin | 旋轉 | overlay |
| auto_label | Auto | 自動 | overlay |
| freespin_total_label | Total Win | 累計贏分 | overlay |
| freespin_remaining | Free Spins Left | 剩餘次數 | TBC |

其余语言键位与 en/zh-hant 一一对应，值待 9 语言本地化表定稿（见 §9 TBC）。

---

## §7 参考图清单

下列 8 张为外壳加载 / 异常层实测取得的权威图（`normative`）；Unity 游戏层的符号 / 背景 / 中奖标题 / Free Spin 屏等图槽尚未取得，以 `placeholder` 行保留，caption 标 `pending: copyCat`（这些行的「文件」列为待补图槽名，不是 `assets/` 内实文件——placeholder 意即待补真图）。

| 文件 | 关联章节/组件ID | provenance | caption | 已知冲突 |
|---|---|---|---|---|
| loadingBg_large.jpg | §1 / ART-C-001 | normative | 麻将金龙主视觉背景 2560×2560：双金龙、麻将牌山、铜钱、孔雀绿 | 无 |
| LoadingEnglishTitle.png | ART-C-002 / §3e | normative | 英文标题 Logo 768×700 "MAHJONG STREAK 麻將連莊" 金字 | 无 |
| LoadingChineseSimpTitle.png | ART-C-002 / §3e | normative | 简体标题 Logo 797×700 | 无 |
| LoadingChineseTradTitle.png | ART-C-002 / §3e | normative | 繁体标题 Logo 797×700 | 无 |
| LoadingTrack.png | ART-C-003 | normative | 进度条轨道底框 963×64 | 无 |
| LoadingBar.png | ART-C-004 | normative | 进度条填充 931×30 | 无 |
| LoadingTip.png | ART-C-005 | normative | 进度头精灵 134×80 | 无 |
| exit.png | ART-C-008 | normative | 退出图标（源图 148×148，显示 66px） | 无 |
| win_{tier}_title_{lang}.png（待补）| ART-C-020 / §3c | placeholder | pending: copyCat（Big/Super/Mega × 8 语言中奖标题图槽）| 无 |
| FreespinAnnounce_*_{lang}.png（待补）| ART-C-023~027 / §3d | placeholder | pending: copyCat（免费旋转公告 / 引导 / 确认屏图槽）| 无 |
| game_bg（待补）| ART-C-010 | placeholder | pending: copyCat（麻将招财主题游戏背景图槽）| 无 |
| symbols_sheet（待补）| ART-C-012 / §3a | placeholder | pending: copyCat（麻将符号集图槽，全序列待定）| 无 |
| paytable_screen（待补）| ART-C-022 / §3b | placeholder | pending: copyCat（赔付表屏图槽）| 无 |

provenance 四值：`normative` / `illustrative` / `foreign-theme` / `placeholder`。文图冲突时以文本 + changelog delta 为准。placeholder 行为待补图槽（尚无 `assets/` 内实文件），双向一致性检查仅适用于 normative / illustrative / foreign-theme 行。

---

## §8 共用壳引用

本作客户端为 Unity WebGL + 平台共用 React 外壳；**共用壳覆盖面较窄**——外壳仅负责加载 / 异常 / 桥接 / 语言，游戏内屏（转轴 / 赔付 / Free Spin / 设定 / 历史）由 Unity 自绘，不由 `_common` 模块直接驱动。故仅引用以下外壳层模块：

| 模块 | 路径 | 本作差异 |
|---|---|---|
| locale | ../_common/locale.md | 9 locale（en/hi/id/kr/my=ms-MY Malay/th/vi/zh-hans/zh-hant）+ Shared 共用表，总数待核（§9）；Unity 内切语言经 `SetLanguage` 桥同步外壳 |
| exceptions | ../_common/exceptions.md | 异常归一枚举沿用；本作异常 UI 为纯 CSS 暗框（非 PNG 面板）；含 `sso-disconnected` 他处登录弹窗 |
| session | ../_common/session.md | 单一 session 限制；断线重连恢复中断前状态 |
| params | ../_common/params.md | 会话参数沿用公版；`reconnect_timeout` 依运营商上限（不预设）|

> 设定 / 历史 / 赔付等 Unity 游戏内屏不走 `_common` 框架借页（与 CG0x crash 系不同），故不引 history / backoffice / telemetry / currency 模块；货币规则待 §9 定稿后按平台 Wallet 处理。

---

## §9 TBC + 签字区

### TBC 表

| item | owner | 影响范围 |
|---|---|---|
| 盘面几何（列数 × 行数 / cluster） | 数学组 | §2 转轴区、§3a 符号排布 |
| 完整符号集（常规全序列 + 是否有 Scatter） | 数学组 + 美术 | §3a 符号表、ART-C-012 |
| 赔付表倍数（各符号 × 命中数量） | 数学组 | §3b 赔付表屏内容、ART-C-022 |
| 目标 RTP / 波动 / 符号权重 | 数学组 | 数值层（GDD §4）|
| Free Spin 触发条件 / 免费次数 / retrigger | 数学组 | §3d Free Spin 层文案 |
| 是否存在 Normal / Epic 等额外中奖档 | 数学组 + PM | §3c win-tier 矩阵档数、ART-C-020 |
| 百搭是否带倍率 / 出现位置限制 | 数学组 | ART-C-013 wild_symbol |
| 麻将招财主题游戏背景终稿 | 美术 | ART-C-010 game_bg |
| 麻将符号集视觉终稿 | 美术 | ART-C-012 symbols |
| 中奖演出 / 级联特效素材（`Win_Texts` / `WinEffectQA`） | 美术 + 动效 | ART-C-021、ART-M-001/002 |
| 色板具体 hex 值 | 设计 | §1 风格锚点落地 |
| 完整音效清单（BGM / SFX 文件名 / 分轨 / 数量） | 音效 | §5 ART-S-001 |
| 完整 9 语言键表 | 本地化 | §6 文案落地 |
| locale 总数与最终语言名单（当前登记 9 + Shared） | PM | §3e 换图矩阵、§6 键表、§8 locale 引用 |
| 货币列表 + 金额显示小数位（各币种） | 运营 + PM | §6 数值显示 |
| Unity 游戏层图槽真图（win-tier / Free Spin / 背景 / 符号 / 赔付屏） | 美术（copyCat 待补） | §7 placeholder 行 |

### 签字表

| 角色 | 姓名 | 日期 | 冻结范围 |
|---|---|---|---|
| Design Lead |  |  |  |
| Game PM |  |  |  |
| Art Reviewer |  |  |  |

### Changelog

| 版本 | 日期 | delta |
|---|---|---|
| v1.0.0 | 2026-07-02 | 初版：外壳层加载 / 异常组件实测入表 + normative 图；slot 模块段（§3a 符号表 / §3b 赔付表屏 / §3c win-tier 矩阵 / §3d Free Spin 层 / §3e locale×换图）首次实例化；Unity 游戏层素材与玩法数值挂 §9 TBC |
| v1.0.1 | 2026-07-02 | §3e/§6/§8 语言口径改为 9 locale + Shared 共用表（my=ms-MY Malay），删缅甸文；locale 总数挂 §9 TBC（owner: PM） |
