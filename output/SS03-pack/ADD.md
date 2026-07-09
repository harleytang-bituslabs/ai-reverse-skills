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
> 本版（v1.1.0）游戏层符号 / 背景 / 倍率 / 免费流程与赔付数值已实测定稿并配 normative 参考图；仅色板 hex、特效终稿等设计侧项保留 §9 TBC。

---

## §1 风格锚点

- 关键词：麻将, 招财, 金龙, 白玉牌, 金元宝, 翡翠绿桌面, 朱红漆木, 孔雀绿, 金色
- 色板：孔雀绿→翡翠绿（主背景 / 桌面）, 暖金（龙 / 金牌 / 币 / 元宝）, 象牙白（牌体）, 朱红（底板 / 中字）, 绿字（發）（具体 hex 值 TBC，见 §9）
- 气氛图：`loadingBg_large.jpg`（麻将金龙主视觉）/ `game_bg.png`（主玩法背景：翡翠桌面 + 金币元宝山，实测 1024²）（≥1，关联 §7）

---

## §2 屏幕与区块布局

| 屏幕 | 区块 | 位置 | 内容 |
|---|---|---|---|
| loading | 主视觉区 | 满屏 | 麻将金龙背景（2560²）+ 标题 Logo（按语言换图）+ 进度条 + Loading 文字 + 版本号 |
| entry | 入场区 | 满屏 | 全幅背景 + 标题 + 开始按钮（開始遊戲 / START GAME） |
| main | 转轴区 | 画面中央 | 4-5-5-5-4 异形麻将盘面（格 168 级视觉基准 184×224）+ 顶部半格预览 + 级联消除 |
| main | 转轴框顶栏 | 盘面框上梁 | 连莊倍率灯组 ×1/×2/×3/×5（免费 ×2/×4/×6/×10 同位换档） |
| main | 消息横幅 | 盘面下缘 | 每轮消除结算横幅（本轮赢分 / 提示滚动） |
| main | 信息栏 | 盘面上方 / 下方 | 余额 / 下注额 / 赢分显示；屏顶细提示条 |
| main | 控制区 | 盘面下方 | Spin / Auto / 下注选注入口 / 速度档 / 设置入口 |
| win_present | 中奖演出层 | 覆盖盘面 | 大奖 / 巨奖 / 超级巨奖 标题图（按语言换图）+ 中奖特效 |
| paytable | 赔付表屏 | 全屏 / 二级（长卷滚动） | 符号赔付表 + 2000 路说明 + 金符 / 免费 / 倍率玩法图文 |
| free_spin_announce | 公告区 | 覆盖盘面 | 免费旋转标题 / 引导 / 开始确认（按语言换图） |
| free_spin_play | 进行区 | 盘面 + 顶部 | 剩余次数 + 累计赢分标签；第 3 轴全金视觉 |
| free_spin_end | 结束区 | 覆盖盘面 | 结束确认 + 累積獎金（按语言换图） |
| bet_select | 选注面板 | 底部滑入 | 注额档位钮阵（服务端下发档位数自适应） |
| settings | 设定区 | 全屏 / 二级 | 音效（BGM/SFX 分档）/ 语言 / 画质（预留） |
| language_select | 语言选择 | 覆盖弹层 | 9 语言列表面板 |
| history | 历史区 | 全屏 / 二级 | 下注纪录注单表（今天 / 近 3 天 / 近一周） |
| bill_detail | 单注详情 | 全屏 / 三级 | 逐轮盘面复盘 + 倍率槽 + 派彩公式行 |
| exception | 异常层 | 满屏 | 纯 CSS 暗框（标题 + 描述）+ 可选退出按钮 + 版本号 |

---

## §3 组件需求清单（审签对象主表）

| ID | 屏幕/区块 | 组件 | 需求描述 | 状态变体 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-C-001 | loading/主视觉区 | 加载背景 loading_bg | 麻将金龙主视觉满屏背景，2560×2560 画布 `object-fit:none` 居中 | idle | P0 | loadingBg_large.jpg | 实测 2560×2560 JPG |
| ART-C-002 | loading/主视觉区 | 标题 Logo title_logo | "MAHJONG STREAK 麻將連莊" 主视觉大 Logo；按语言换图（§3e / §6 baked） | idle | P0 | LoadingEnglishTitle.png | en 768×700 / 简繁 797×700，baked |
| ART-C-003 | loading/主视觉区 | 进度条轨道 progress_track | 进度条底框 | idle | P1 | LoadingTrack.png | 实测 963×64 |
| ART-C-004 | loading/主视觉区 | 进度条填充 progress_bar | 进度填充（clip-path inset 推进） | idle | P1 | LoadingBar.png | 实测 931×30 |
| ART-C-005 | loading/主视觉区 | 进度头精灵 progress_tip | 进度条头部提示精灵 | idle | P2 | LoadingTip.png | 实测 134×80 |
| ART-C-006 | loading/主视觉区 | Loading 文字 loading_text | 底部白字 48px bold，呼吸 3.5s | idle | P2 | 无 | overlay（§6） |
| ART-C-007 | exception/异常层 | 异常容器 exception_box | 纯 CSS 暗框 960×(128~196)，圆角 36px，`rgba(35,35,45,.88)`；标题白字 52px + 描述 28px | idle | P1 | 无 | 非 PNG 面板 |
| ART-C-008 | exception/异常层 | 退出按钮 exit_button | 右上角退出图标，显示尺寸 66px（仅 URL 带 `backURL` 时显示） | idle | P1 | exit.png | 实测源图 148×148 |
| ART-C-009 | exception/异常层 | 版本号 version_label | 底部常驻版本号，白字 20px opacity .3 | idle | P2 | 无 | overlay |
| ART-C-010 | main/转轴区 | 游戏背景 game_bg | 翡翠绿桌面 + 金币元宝山主玩法背景（另有免费 / 保底免费两套换皮变体） | idle | P0 | game_bg.png | 实测 1024²，三模式皮成套换 |
| ART-C-011 | main/转轴区 | 转轴框 reel_frame | 盘面容器：朱红底板 + 上下描金围栏（顶梁 1080×340 内嵌倍率灯位、底栏 1040×120，两端龙首衔珠）；免费 / 保底免费换皮 | idle | P0 | frame_topfence_multiplier.png | 实测顶栏含灯位 |
| ART-C-012 | main/转轴区 | 白符号集 symbols_regular | 9 种白玉麻将牌：發/中/白/八萬/五筒/五條/三筒/二筒/二條，原生 184×224 与格位 1:1 | idle | P0 | symbol_fa_white.png / symbols_montage.png | 全集与命名见 §3a |
| ART-C-013 | main/转轴区 | 百搭 baida_wild | 「百搭」万能牌：金元宝 + 立体字（中英两版文字图），替代除胡外全部符号 | idle | P0 | symbol_wild_baida.png | 实测 192×215；无独立赔付 / 无倍率 |
| ART-C-014 | main/信息栏 | 余额 / 下注 / 赢分栏 info_bar | 余额 / 当前下注额 / 本局赢分数值显示；屏顶另有细提示条 | idle | P0 | 无 | 数值 overlay（§6） |
| ART-C-015 | main/控制区 | Spin 按钮 spin_button | 翡翠圆形主旋转钮（金框；Auto 态换方芯 + 剩余局数） | idle/pressed/disabled | P0 | 无 | 实测 208×208 |
| ART-C-016 | main/控制区 | Auto 按钮 auto_button | 自动旋转开关 + 局数选择面板入口 | idle/active | P1 | 无 | 92×92 小钮系 |
| ART-C-017 | main/控制区 | 选注入口 bet_button | 打开底部选注面板（档位钮阵见 ART-C-035） | idle | P0 | 无 | 92×92 小钮系 |
| ART-C-018 | main/控制区 | 设置入口 settings_button | 进入设定屏 | idle | P1 | 无 | 92×92 小钮系 |
| ART-C-019 | main/控制区 | 速度档 speed_toggle | 转速两档切换，钮下双指示灯 | idle/active | P1 | 无 | 92×92 小钮系 + 灯 ×2 |
| ART-C-020 | win_present/中奖演出层 | 中奖标题图 win_tier_title | 三档：大奖 / 巨奖 / 超级巨奖（升序），按语言换图，矩阵见 §3c / §3e | idle | P0 | win_big_title_hans.png / win_mega_title_hans.png / win_super_title_hans.png | baked（§6）；档序实测定稿 |
| ART-C-021 | win_present/中奖演出层 | 中奖演出层 win_overlay | 达档满版演出（黑幕 + 白描龙纹环旋转 + 标题 + 数字滚动 + 金币）；行内小奖另有 lv1–lv3 三级框 | idle | P0 | 无 | 特效终稿 TBC（§9） |
| ART-C-022 | paytable/赔付表屏 | 赔付表长卷 paytable_panel | 竖向长卷（972 宽）：符号赔付 + 2000 路说明 + 金符 / 免费 / 倍率图文；数值见 GDD §4 | idle | P1 | 无 | 结构见 §3b |
| ART-C-023 | free_spin_announce/公告区 | 免费旋转标题 freespin_announce_title | 免费旋转触发标题图，按语言换图 | idle | P1 | freespin_announce_title_en.png | baked（§6）；命名见 §3d |
| ART-C-024 | free_spin_announce/公告区 | 免费旋转引导 freespin_guide | 玩法引导图（金符转百搭 / 倍率翻倍说明），按语言换图 | idle | P1 | 无 | baked（§6） |
| ART-C-025 | free_spin_announce/公告区 | 开始确认 freespin_start_confirm | 开始按钮文字图，按语言换图 | idle | P1 | 无 | baked（§6） |
| ART-C-026 | free_spin_play/进行区 | 累计标签 freespin_total_label | 免费旋转累计赢分标签，按语言换图 | idle | P1 | 无 | baked（§6） |
| ART-C-027 | free_spin_end/结束区 | 结束确认 freespin_end_confirm | 结束确认（累積獎金 + 确认钮），按语言换图 | idle | P1 | 无 | baked（§6） |
| ART-C-028 | settings/设定区 | 设定面板 settings_panel | 音效（BGM / SFX 各档位拨钮）/ 语言行 / 画质三挡（预留位） | idle | P1 | 无 | 底部五键 TabList 导航 |
| ART-C-029 | history/历史区 | 下注纪录面板 history_panel | 注单表（今天 / 近 3 天 / 近一周 tab）+ 状态标（进行中 / 已完成） | idle | P1 | 无 | 长列表滚动 |
| ART-C-030 | main/异常 | 重连 / Toast reconnect_toast | 断线重连 / 闲置登出 / 余额不足等提示 | idle | P1 | 无 | 文案见 §6 / 共用壳 exceptions（§8） |
| ART-C-031 | main/转轴区 | 金符号集 symbols_gold | 9 种金色变体（與白符一一对应）：鎏金牌体 + 底缘金元宝徽；仅现于第 2/3/4 列，中奖后原位转百搭 | idle | P0 | symbol_fa_gold.png / symbols_montage.png | 赔率同白符（GDD §4） |
| ART-C-032 | main/转轴框顶栏 | 连莊倍率灯组 streak_multiplier_lamps | 四档灯位嵌于框顶梁：基础 ×1/×2/×3/×5；免费同位换 ×2/×4/×6/×10;当前档亮灯 + 光环 | idle/active | P0 | frame_topfence_multiplier.png | 三模式皮各一套 |
| ART-C-033 | bill_detail/单注详情 | 单注详情页 bill_detail_page | 逐轮盘面复盘（4-5-5-5-4 复刻格）+ 倍率四槽 + 派彩公式行 + 翻页钮 | idle | P2 | 无 | 数值 overlay |
| ART-C-034 | language_select/语言选择 | 语言选择面板 language_selector | 遮罩 + 800×960 面板 + 9 语言行 | idle | P1 | 无 | 语言清单见 §3e |
| ART-C-035 | bet_select/选注面板 | 选注面板 bet_selector_panel | 底部滑入面板，档位钮 4×3 阵列（档位数服务端下发自适应） | idle | P0 | 无 | 收起态驻屏下缘 |

规则：状态变体列逐项显式声明；ART-C 编号连续无重复；参考图列文件均登记于 §7。

<!-- module: board=reel -->
### §3a 符号表

实测定稿：9 常规符号 × 白 / 金双版本 + 胡（Scatter）+ 百搭（Wild）。金符仅现于第 2/3/4 列，参与中奖后原位转百搭。

| 符号 | 标识符 | 语义 | Wild/Scatter | 视觉 |
|---|---|---|---|---|
| 發 | `sym_fa` | 发财（高赔 1 位） | 常规（有金变体） | 白玉牌绿字 / 金牌绿字（symbol_fa_white.png / symbol_fa_gold.png） |
| 中 | `sym_zhong` | 红中 | 常规（有金变体） | 白玉牌红字 |
| 白 | `sym_bai` | 白板 | 常规（有金变体） | 白玉牌群青描框 |
| 八萬 | `sym_ba_wan` | 八万 | 常规（有金变体） | 蓝「八」+ 红「萬」 |
| 五筒 | `sym_wu_tong` | 五筒 | 常规（有金变体） | 同心圆点阵 ×5 |
| 五條 | `sym_wu_tiao` | 五条 | 常规（有金变体） | 竹节 ×5 |
| 三筒 | `sym_san_tong` | 三筒 | 常规（有金变体） | 同心圆点阵 ×3 |
| 二筒 | `sym_er_tong` | 二筒 | 常规（有金变体） | 同心圆点阵 ×2 |
| 二條 | `sym_er_tiao` | 二条（低赔末位） | 常规（有金变体） | 竹节 ×2 |
| 胡 | `sym_hu_scatter` | 触发免费 | **Scatter** | 立体红金「胡」字 + 圆形鎏金纹章底（symbol_scatter_hu.png）；不派彩 |
| 百搭 | `sym_baida_wild` | 万能牌 | **Wild** | 金元宝 + 立体「百搭/WILD」字（symbol_wild_baida.png）；由金符转化产生 |

<!-- module: board=reel -->
### §3b 赔付表屏视觉

赔付表屏为竖向长卷（972 宽,分区滚动）：

| 版面块 | 内容 | 状态 |
|---|---|---|
| 首符特写 | 發 牌特写 + 3/4/5 连赔率示例（10 / 25 / 50） | 数值定稿（GDD §4） |
| 符号赔付网格 | 9 符号 × 3/4/5 连列赔率 | 数值定稿（GDD §4） |
| 2000 路说明 | 左起连列 ways 计算示意（2000路中獎組合） | 定稿 |
| 金符 / 百搭说明 | 金符仅 2/3/4 列、转百搭规则；百搭替代规则 | 定稿 |
| 免费 / 倍率说明 | 胡触发表、免费倍率翻倍、reel3 全金 | 定稿 |
| 玩法与 UI 图例 | Tumble 级联图文 + 按钮图例 + 免责声明 | 定稿（配图随美术终稿） |

<!-- module: interaction=slot -->
### §3c win-tier 演出矩阵

三档定稿，**升序：大奖（big）→ 巨奖（mega）→ 超级巨奖（super）**；每档标题图按语言换图，命名 `win_{tier}_title_{lang}.png`，lang 为 8 个图变体键（印尼 / 马来合用 `id_and_my`）。

| 档 (tier) | 中文题字 | 命名前缀 | 语言图变体 (lang) |
|---|---|---|---|
| 1 · big | 大奖 | `win_big_title_*` | en / hans / hant / hindi / id_and_my / kr / th / vi |
| 2 · mega | 巨奖 | `win_mega_title_*` | 同上 |
| 3 · super | 超级巨奖 | `win_super_title_*` | 同上 |

> 每档 8 语言 × 2 尺寸变体;行内小奖另有 lv1–lv3 三级小奖框（演出层组件,非独立标题档）。标题图内文字 baked（§6）。

<!-- module: interaction=slot -->
### §3d Free Spin 层

完整流程定稿（公告 → 进行 → 结束）;触发与次数见 GDD §3/§4（胡 3–7 → 10–18 次,retrigger 同表）。各屏组件按语言换图：

| 流程屏 | 组件 | 命名前缀 | 说明 |
|---|---|---|---|
| 公告标题 | freespin_announce_title | `FreespinAnnounce_title_*` | 「您已獲得 N 次免費旋轉」 |
| 玩法引导 | freespin_guide | `FreespinAnnounce_guide_*` | 金符转百搭 / 倍率翻倍说明 |
| 开始确认 | freespin_start_confirm | `FreespinAnnounce_start_confirm_*` | 开始按钮文字图 |
| 累计标签 | freespin_total_label | `FreespinAnnounce_totalLabel_*` | 免费累计赢分标签 |
| 结束确认 | freespin_end_confirm | `Freespin_end_confirm_*` | 累積獎金 + 确认钮 |

<!-- module: interaction=slot -->
### §3e locale × 换图矩阵

Unity 内建 **9 locale + Shared 非语言共用表**（实测定稿）：en / hi / id / ko / ms-MY / th / vi / zh-hans / zh-hant。

| 图组 | 组件 ID | 命名规律 | 语言键集 | baked/overlay |
|---|---|---|---|---|
| 加载标题 Logo | ART-C-002 | `Loading{English,ChineseSimp,ChineseTrad}Title.png` | en / 简 / 繁（3） | baked |
| 中奖标题（三档） | ART-C-020 | `win_{tier}_title_{lang}.png` | 8 键（id_and_my 合用） | baked |
| 免费旋转公告组 | ART-C-023~027 | `FreespinAnnounce_{title,guide,start_confirm,totalLabel}_{lang}` / `Freespin_end_confirm_{lang}` | 8 键 | baked |
| 功能文字（余额 / 下注 / 赢分等） | ART-C-014 等 | 运行时字符串（Unity StringTable / 外壳 i18n） | 9 locale | overlay |

> 图变体 8 键 vs locale 9 为实测口径（印尼 / 马来共用文字图；加载标题仅 3 语言版）;其余语言运行时以文本层呈现。

---

## §4 动效需求清单

| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-M-001 | main/转轴区 | 级联消除 tumble_cascade | 中奖牌爆裂消除 → 塌落 → 顶部填充，循环至无新中奖 | 触发 on_win（每轮） | P0 | 无 | 两套爆裂序列（白 / 金） |
| ART-M-002 | main/转轴区 | 金符转百搭 gold_to_wild | 金牌原位翻转出金元宝百搭（不随消除移除） | 触发 金符参与中奖 | P0 | 无 | 元宝翻转序列 |
| ART-M-003 | main/转轴框顶栏 | 倍率灯递进 multiplier_step | 连莊倍率灯逐档点亮 + 光环脉冲；免费档位翻倍同构 | 触发 每轮级联 | P0 | frame_topfence_multiplier.png | 每档配升档语音（§5） |
| ART-M-004 | win_present | 中奖档演出 win_tier_present | 三档满版演出（黑幕 + 龙纹环旋转 + 标题入场 + 数字滚动） | 触发 达档 | P0 | 无 | 分档表现终稿 TBC（§9） |
| ART-M-005 | main/转轴区 | 转轴滚动 reel_spin | Spin 触发滚动 → 逐列落定;差一胡时听牌慢转 + 压暗聚焦 | 触发 on_spin / 听牌 | P0 | 无 | 听牌演出实测约 6.4s 音效配套 |
| ART-M-006 | free_spin | 免费旋转转场 freespin_transition | 进出 Free Spin 的幕布滑入 / 公告 / 结束转场 | 触发 Free Spin 进 / 出 | P1 | 无 | 三片幕布屏外平移入场 |

规格停在需求清单级，不作逐帧规格。

---

## §5 音效需求清单

实测音频共 **41 支**（BGM 2 + SFX/语音 39），按触发域分组如下；逐文件时长与命名随素材交付。

| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-S-001 | 全局 | 双轨 BGM bgm_set | 基础局循环（约 98s）+ 免费局变奏循环（约 23s） | 场景进入 | P0 | 无 | 2 支 |
| ART-S-002 | main/控制区 | 交互点击 sfx_click | 按钮 / Spin / 麻将点击 / 开始 / 免费确认 | 点击 | P1 | 无 | 5 支,0.16–0.81s |
| ART-S-003 | main/转轴区 | 转轮与落定 sfx_reel | 落牌 / 听牌慢转抖动 / 听牌全程 | 落定 / 听牌 | P0 | 无 | 3 支（听牌约 6.4s） |
| ART-S-004 | main/转轴区 | 结算与计数 sfx_settle | 消除配对 / 赢分滚动循环（约 60s 可中断）/ 结算收尾 / 总赢横幅 | 每轮结算 | P0 | 无 | 4 支 |
| ART-S-005 | main/转轴区 | 逐符号语音 vo_symbols | 高赔牌落定报牌名（绿龙 / 红中 / 八万 / 筒条系） | 对应符号成组 | P1 | 无 | 9 支,0.45–1.24s |
| ART-S-006 | main/转轴框顶栏 | 倍率语音 vo_multiplier | ×1/×2/×3/×5 与免费 ×4/×6/×10 升档播报 | 倍率升档 | P1 | 无 | 7 支 |
| ART-S-007 | free_spin | 免费流程音 sfx_freespin | 胡现身 /「胡啦」/ 转场 / 蓄力 / 结算 / 计数切换 / 结束 | 免费流程各节点 | P1 | 无 | 7 支 |
| ART-S-008 | win_present | 特效与彩蛋 sfx_misc | 百搭元宝现身 / 金龙现身 / 全中彩蛋男女声 | 对应演出 | P2 | 无 | 4 支;彩蛋触发口径 TBC（§9） |

规格停在需求清单级，不作逐轨规格。

---

## §6 文案 / 本地化

baked-text 政策：**标题类图片按语言换图 = baked**（加载 Logo、三档中奖标题、免费公告 / 引导 / 确认屏）;功能性文字（余额 / 下注 / 赢分 / 剩余次数等）默认 `overlay`，运行时按 9 locale 切换。完整 9 语言键表随 Localization 表交付（约 126 键;下表为核心键实测样例）。

| key | en | zh-hant | baked/overlay |
|---|---|---|---|
| game_logo | MAHJONG STREAK | 麻將連莊 | baked |
| win_big_title | BIG WIN | 大獎 | baked |
| win_mega_title | MEGA WIN | 巨獎 | baked |
| win_super_title | SUPER WIN | 超級巨獎 | baked |
| freespin_won | You Have Won {0} Free Spins!!! | 您已獲得 {0} 免費旋轉!!! | baked |
| start_game | START GAME | 開始遊戲 | baked |
| ways_slogan | 2000 Ways | 2000路中獎組合 | overlay |
| total_win | TOTAL WIN: {0} | 累積獎金：{0} | overlay |
| balance_label | Balance | 餘額 | overlay |
| bet_label | Bet | 下注 | overlay |
| win_label | Win | 盈利 | overlay |
| settings_label | Settings | 設置 | overlay |
| guide_label | Guide | 教程 | overlay |
| history_label | History | 下注紀錄 | overlay |
| loading_text | Loading... | 載入中... | overlay |
| idle_logout | No spin was made in the past 3 minutes. You were logged out! | （繁体值随表交付） | overlay |

---

## §7 参考图清单

19 张全部为实测取得的权威 / 示意图；游戏层图槽本版已配齐代表图,无 placeholder 行。

| 文件 | 关联章节/组件ID | provenance | caption | 已知冲突 |
|---|---|---|---|---|
| loadingBg_large.jpg | §1 / ART-C-001 | normative | 麻将金龙主视觉背景 2560×2560：双金龙、麻将牌山、铜钱、孔雀绿 | 无 |
| LoadingEnglishTitle.png | ART-C-002 / §3e | normative | 英文标题 Logo 768×700 | 无 |
| LoadingChineseSimpTitle.png | ART-C-002 / §3e | normative | 简体标题 Logo 797×700 | 无 |
| LoadingChineseTradTitle.png | ART-C-002 / §3e | normative | 繁体标题 Logo 797×700 | 无 |
| LoadingTrack.png | ART-C-003 | normative | 进度条轨道底框 963×64 | 无 |
| LoadingBar.png | ART-C-004 | normative | 进度条填充 931×30 | 无 |
| LoadingTip.png | ART-C-005 | normative | 进度头精灵 134×80 | 无 |
| exit.png | ART-C-008 | normative | 退出图标（源图 148×148，显示 66px） | 无 |
| game_bg.png | §1 / ART-C-010 | normative | 主玩法背景 1024²：翡翠桌面 + 金币元宝山 | 无 |
| frame_topfence_multiplier.png | ART-C-011 / ART-C-032 | normative | 转轴框顶梁 1080×340，内嵌 ×1/×2/×3/×5 倍率灯位 | 无 |
| symbol_fa_white.png | ART-C-012 / §3a | normative | 白符样例：發 184×224 | 无 |
| symbol_fa_gold.png | ART-C-031 / §3a | normative | 金符样例：發（鎏金 + 元宝徽）184×224 | 无 |
| symbol_scatter_hu.png | §3a | normative | 胡（Scatter）184×224 | 无 |
| symbol_wild_baida.png | ART-C-013 / §3a | normative | 百搭（Wild）192×215 | 无 |
| symbols_montage.png | ART-C-012 / ART-C-031 / §3a | illustrative | 全符号集汇总示意（白 / 金 / 胡 / 雕纹版拼图） | 无 |
| win_big_title_hans.png | ART-C-020 / §3c | normative | 大奖标题（hans 版,档 1） | 无 |
| win_mega_title_hans.png | ART-C-020 / §3c | normative | 巨奖标题（hans 版,档 2） | 无 |
| win_super_title_hans.png | ART-C-020 / §3c | normative | 超级巨奖标题（hans 版,档 3 最高） | 无 |
| freespin_announce_title_en.png | ART-C-023 / §3d | normative | 免费旋转公告标题（en 版） | 无 |

provenance 四值：`normative` / `illustrative` / `foreign-theme` / `placeholder`。文图冲突时以文本 + changelog delta 为准。

---

## §8 共用壳引用

本作客户端为 Unity WebGL + 平台共用 React 外壳；共用壳覆盖面较窄——外壳仅负责加载 / 异常 / 桥接 / 语言，游戏内屏由 Unity 自绘。

| 模块 | 路径 | 本作差异 |
|---|---|---|
| locale | ../_common/locale.md | 9 locale + Shared 共用表（实测定稿）;Unity 内切语言经 `SetLanguage` 桥同步外壳 |
| exceptions | ../_common/exceptions.md | 异常归一枚举沿用；本作异常 UI 为纯 CSS 暗框（非 PNG 面板）；含他处登录弹窗 |
| session | ../_common/session.md | 单一 session 限制;断线重连恢复中断前状态;3 分钟闲置登出 |
| params | ../_common/params.md | 会话参数沿用公版;`reconnect_timeout` 依运营商上限（不预设） |

> 设定 / 历史 / 赔付等 Unity 游戏内屏不走 `_common` 框架借页;货币规则待 §9 定稿后按平台 Wallet 处理。

---

## §9 TBC + 签字区

### TBC 表

| item | owner | 影响范围 |
|---|---|---|
| 色板具体 hex 值 | 设计 | §1 风格锚点落地 |
| 中奖演出 / 级联特效素材终稿 | 美术 + 动效 | ART-C-021、ART-M-001~004 |
| 目标 RTP / 符号权重 / 数学表分配 | 数学组 | 数值层（GDD §4/§6） |
| 购买免费（Buy 10 FG）上线口径与入口素材 | PM + 数学组 | GDD §3;入口组件届时补入 §3 |
| 全中彩蛋语音触发口径 | 数学组 + 音效 | ART-S-008 |
| 货币列表 + 金额显示小数位 | 运营 + PM | §6 数值显示 |

### 签字表

| 角色 | 姓名 | 日期 | 冻结范围 |
|---|---|---|---|
| Design Lead |  |  |  |
| Game PM |  |  |  |
| Art Reviewer |  |  |  |

### Changelog

| 版本 | 日期 | delta |
|---|---|---|
| v1.0.0 | 2026-07-02 | 初版：外壳层加载 / 异常组件实测入表 + normative 图；slot 模块段首次实例化；Unity 游戏层素材与玩法数值挂 §9 TBC |
| v1.0.1 | 2026-07-02 | §3e/§6/§8 语言口径改为 9 locale + Shared 共用表（my=ms-MY Malay），删缅甸文；locale 总数挂 §9 TBC（owner: PM） |
| v1.1.0 | 2026-07-09 | 游戏层实测定稿：§3a 符号全集（9×白金 + 胡 + 百搭,金符转百搭）;§3c 档序定为 大奖<巨奖<超级巨奖（修正 v1.0 档序）并移除虚构「萬」符号行;§3b/GDD§4 赔付全量;新增 ART-C-031~035（金符 / 倍率灯组 / 单注详情 / 语言选择 / 选注面板）与 ART-M-002/003/005 补强;§5 音效由整表 TBC 改为 41 支分组清单;§6 键表实值化（en/zh-hant）;§7 placeholder 5 行全部换为 normative 实图（新增 11 张）;locale 定稿 9;§9 TBC 由 16 项缩至 6 项 |
