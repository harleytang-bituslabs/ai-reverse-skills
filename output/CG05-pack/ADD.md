---
project: CG05
doc: ADD
interaction: crash-step
board: grid
status: draft
owner: Xina Zhong (Design Lead)
---

# CG05 MineBeach 沙滩扫雷 · ADD(美术与设计需求)

> 本文是美术审签对象 + auto-art 视觉输入。审签方在 §9 签字冻结;auto-art 从 §3 组件清单 + 品类模块段(§3a/§3b)+ §7 图清单机械提取输入。
> 文本永远为 normative:文图冲突时以文本 + changelog delta 为准,参考图仅作结构/气氛参照。
> 本版(v1.1.0)几何/时长/状态已实测定稿(设计画布 1080×1920);§7 参考图全部换为实装资产(normative)。

---

## §1 风格锚点

- 关键词:阳光手绘卡通海滩, 高饱和厚涂, 沙滩水雷, 贝壳海星椰树, 玻璃果冻质感 UI, 国际化无文化符号
- 色板:60% 沙金(沙块/滩地 暖黄~米金)+ 30% 海洋青蓝(天空水面 + HUD 玻璃蓝面板/深海设置底 + tab 渐变字 `#D7E6ED→#4AD1EA`)+ 10% 强调(动作绿=第三钮、橙金描边、金币金渐变 `#FED027→#FFEF73`、警示橙红);框架色 textPrimary `#FFFFFF`、设置遮罩 `#112E60`(α0.85);精确主题色 hex 精调见 §9
- 气氛图:`logo_mineBeach_en.png`(题字风格锚:熔岩橙 Mine + 水雷,水蓝 Beach + 棕榈浪花);`loading_beach_illustration.jpg`(高细节滩景:宝箱+发光符文水雷);`bg_main_beach.png`(主场景滩地)(≥1,关联 §7)

---

## §2 屏幕与区块布局

| 屏幕 | 区块 | 位置 | 内容 |
|---|---|---|---|
| loading | 加载区 | 全屏 | 滩景插画 + Logo 箱 940×525@top40 + LOADING 54px@1652 + 进度条 734×76@1727(车灯游标) + 百分比 |
| loading_done | 开始区 | 全屏 | 同上;进度条淡出,**Game Start 钮 560×171@top1360** 淡入 |
| maintenance | 异常区 | 全屏 | 滩景 + 深色羊皮纸面板 878×238@bottom12% + 右上退出钮 66px(仅 backURL) |
| main | 顶栏区 | 顶部 | 齿轮 90²(993.5,75.5) + 场内 Logo 640 宽@y151 + 倍率梯条 997×96@y478 + 两侧计数卡 146×176(金币数/雷数) |
| main | 盘面区 | 中央偏下 | 5×5 沙块阵 920×920(x80,y694),翻格动画;**盘面无独立底板**(直接坐滩景上) |
| main | 控制区 | 底部 | 余额/盈利条 997×109@y1624 + 三钮行 322×108×3@y1761(Bet/Mines/动作钮) + 注单号 22px |
| bet_popup | 选档弹层 | 控制区上方 | 深蓝气泡 470×1041(尾指 Bet 钮):头行 Bet {币} + 6 选项行 |
| mines_popup | 数字矩阵 | 盘面上方 | 深蓝气泡 928×898:4 列×6 行 3~24(两空格),列降序 |
| win(cashout) | 演出 | 屏中 | YOU WIN 横幅组(底图 634×175+标题+金额+币icon)@(540,960);盘面保持揭示 |
| win(ultimate) | 演出 | 全屏 | Grand Prize 金渐变大字@(540,258) + 横幅下移@(540,858) + 金币彩带雨(顶部生成带) |
| busted | 场内演出 | 全屏 | 爆雷格火药爆 + 全屏白闪/裂纹/震屏(程序化);无覆层横幅 |
| settings | 设定区 | 全屏覆层 z999 | 海底背景 + 页头 144 + 内容滚动区 + 底部 5-tab 栏 180 |
| guide | 说明区 | 设定区内页 | Rules 富文本(带内联图标)+ Buttons 按钮示意(自动流式布局) |
| history | 历史区 | 设定区内页 | 3 列汇总 116 + 虚拟注单列表 1208(行 120)+ 3 日期 tab 314×100 |
| language_popup | 语言弹层 | 居中 800×960 | 矢量面板(蓝 α0.6+渐变描边)+ 4 语言行 548×114 |
| warning_popup | 异常弹窗 | 居中 976×576 | 羊皮纸面板 + 标题 80px + 正文 48px + reload 钮 294×104(队列式) |
| toast | 非模态提示 | 中心+760 | 882×179 浅羊皮纸横条,3s 自动隐/倒数常驻 |
| exit_modal | 退出确认 | 居中(vw) | 895/1920vw×600/1920vw 特例(随视口非画布) |

---

## §3 组件需求清单(审签对象主表)

| ID | 屏幕/区块 | 组件 | 需求描述 | 状态变体 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-C-001 | loading/加载区 | 加载背景 loading_bg | 全屏高细节滩景插画(宝箱/发光符文水雷/贝壳浪花) | idle | P1 | loading_beach_illustration.jpg | 实测 1080×1920 cover |
| ART-C-002 | loading+main/顶栏 | 游戏 Logo game_logo | 烧字 logo 三语言变体(en/zh/tr;pt 回退 en);入场箱 940×525 contain,场内 640 宽居中 | idle | P0 | logo_mineBeach_en.png | baked;en 1007×562 / zh 1545×1007 / tr 1524×994 |
| ART-C-003 | loading/加载区 | 进度条 progress_bar | 容器 734×76(木框橙边)+填充 700×46(clip 左→右)+**车灯游标**(CSS 径向渐变 8px 脉动 1.4s)+百分比 48px | idle | P1 | loading_progress_container.png | 实测 top1727 居中;原图 1000×78 拉伸渲染 |
| ART-C-004 | loading/加载区 | 开始按钮 start_button | Game Start 560×171(绿果冻木框;文字 52px 叠加) | idle/hover/pressed | P0 | btn_gamestart_idle.png | hover scale1.15/active0.9(CSS);hover/pressed 贴图为孤儿 |
| ART-C-005 | main/全局 | 主背景 main_bg | 滩景全屏:上 1/3 天海棕榈,下 2/3 沙地(贝壳海星脚印) | idle | P0 | bg_main_beach.png | 源图 2160×3840(2x),宽匹配铺 1080×1920 |
| ART-C-006 | main/顶栏区 | 设置入口 settings_gear | 深蓝圆角齿轮 90×90(中心 993.5,75.5;右缘对齐倍率条右缘) | idle | P1 | btn_settings_gear.png | 原图 212² 渲染 90² |
| ART-C-007 | main/顶栏区 | 倍率梯条 multiplier_bar | 沙金长条 997×96 + 档位 pill 链(蓝=普通/金=当前,label 33px `#FFF8D6`)+ 两端翻页箭头 66.7×82.6;详见 §3b | idle/current | P0 | multiplier_bar_track.png / multiplier_chip_idle.png / multiplier_chip_current.png | 实测;chip 143px/枚,mask 视口 832px,可见≈5.8 枚 |
| ART-C-008 | main/顶栏区 | 计数卡对 counter_cards | 蓝玻璃卡×2:左金币卡=安全格数(25−雷),右炸弹卡=雷数;计数 46px 白 stroke `#2a3a6b` | idle | P0 | counter_card_coins.png / counter_card_mines.png | 146×176;底对齐 logo 底−55;实时联动雷数选择 |
| ART-C-009 | main/盘面区 | 盘面格 tile | 5×5 格距 184;盖面=**7 种沙块变体**(贝壳/素面/脚印/海星/卵石…)按固定美学矩阵铺排;四态见 §3a | tile_hidden×7/tile_safe/tile_mine_hit/tile_auto(α0.5) | P0 | tile_sand_var1.png | 盖面原图 180×182~188;点击=开格请求,一次一发 |
| ART-C-010 | main/盘面区 | 翻开件 reveal_set | 半透明棕底板 184² + 星星金币 125×128 / 黑水雷 123×128(长边≤150 上屏) | coin/bomb | P0 | tile_reveal_base.png / tile_reveal_coin.png / tile_reveal_bomb.png | 实测;金币/炸弹同框适配 |
| ART-C-011 | main/控制区 | 余额盈利条 balance_win_bar | 蓝 pill 橙金边 997×108.8(原生 880×96):左 BALANCE: 右 WIN:(44px 白+值金 `#FFD23E`,对称 7.5% 边距) | idle | P0 | balance_win_bar.png | 兑付后 WIN 值刷新 |
| ART-C-012 | main/控制区 | 投注选择钮 btn_bet | 蓝果冻钮 322×108(原 334×112):icon_bet 筹码+「Bet {值}」32px;开投注弹层 | idle/hover/pressed/locked | P1 | btn_selector_blue_idle.png | 三态贴图;局中禁开(只关不开) |
| ART-C-013 | main/控制区 | 雷数选择钮 btn_mines | 同上底:icon_mines 白炸弹+「Mines {n}」;开雷数弹层 | idle/hover/pressed/locked | P1 | btn_selector_blue_idle.png | 雷数只对下一局生效 |
| ART-C-014 | main/控制区 | 动作钮 btn_action | **绿果冻钮恒底** 322×108,overlay 换面:REFRESH 面(白循环箭头 76px,=下注+开局)⇄ CASH OUT 面(金星币 icon+文案 32px) | refresh/cashout(+三态贴图) | P0 | btn_action_green_idle.png / icon_refresh_face.png / icon_cashout_starcoin.png | 首翻后变 cashout,局末变回;**无红色收款钮**(v1.0 口径修正) |
| ART-C-015 | bet_popup | 投注弹层 bet_popup | 深蓝 speech-bubble 470×1041(50% 渲染;尾巴 33.4% 宽指向 Bet 钮):头行「Bet {币}」+6 选项行 464×140(4px 分隔线);选中=高亮框 228×140 | 单列 7 行 | P0 | popup_bet_selector.png | 档数 2~6 服务端下发,空行留白;无手输框 |
| ART-C-016 | mines_popup | 雷数弹层 mines_popup | 深蓝 speech-bubble 928×898(50% 渲染;尾巴 38.66% 宽):4 列×6 行数字格 228×140,列降序 [null,20,14,8]…[21,15,9,3];选中高亮框 | idle/selected | P0 | popup_mines_selector.png | 两个 null 空格无字不可点(3~24 共 22 值) |
| ART-C-017 | main/控制区 | 注单号 bet_id_label | 「Bet ID: {id}」22px bold 白 stroke4 α0.7,第三钮正下方+72px | idle | P2 | 无 | 开局显示、回投注清空 |
| ART-C-018 | win/演出 | 胜利横幅组 win_banner | 底横幅 634×175(**无烧字**)+「YOU WIN」56px `#FFFF00` stroke `#733406` +金额 60px 白 900+币icon 56²;手动兑付中心(540,960) | manual/ultimate(下移 858) | P0 | win_banner_base.png | 底图为像素绿横幅(沿用件,见 §7 冲突列);文字全 overlay |
| ART-C-019 | win/演出 | 通关大字 grand_prize | 「You have won the Grand Prize」80px 900 金渐变 `#FFECA1→#E0B736` stroke `#401919`,无底图,(540,258) | idle | P0 | 无 | 仅 ultimate;与横幅同屏(横幅让位下移) |
| ART-C-020 | win/演出 | 胜利雨图集 win_rain | 金币翻面序列图集 3×3(512×427)+彩带碎片图集 5×5(512×512) | idle | P1 | fx_coin_rain_sheet3x3.png / fx_ribbon_sheet5x5.png | 动效见 ART-M-006 |
| ART-C-021 | busted/演出 | 屏裂特效 screen_crack | 全屏白闪+9 条裂纹(深黑 w9+冰蓝芯 w3)+震屏;**程序化 Graphics,无贴图**(代码注明占位可换设计资产) | idle | P1 | 无 | 需求=补设计资产或维持程序化 |
| ART-C-022 | toast | Toast 面板 toast_panel | 浅羊皮纸横条 882×179(中心 y1720);文字 48px Inter bold wrap786 | idle/persistent | P1 | 无 | 3s 自动隐/倒数常驻;替换=crossfade 250ms |
| ART-C-023 | warning_popup | 警告弹窗 warning_popup | 羊皮纸面板 976×576(原 900×620 拉伸)+标题 80px `#344C6B`+正文 48px 700+reload 钮 294×104 三态 | idle/hover/clicked | P1 | panel_warning_parchment.png | 队列式;遮罩不可点关 |
| ART-C-024 | settings/设定区 | 设置系统 settings_panel | 海底背景+页头条 1080×144+底部 5-tab 栏 1080×180(back/setting/guide/history/exit,icon 72²+label 36px,active=渐变字+光晕 216×168)+音量双轨三档滑块 130×50+静音钮 64×52+语言入口 500×100+画质三档 150×90(toggle 48²) | tab active/idle;音量 0~3;画质 low/med/high | P1 | bg_setting_underwater.png | 画质三档实装(Low/Med/High,切渲染分辨率) |
| ART-C-025 | guide/说明区 | 玩法说明 guide_panel | Rules 分节(48px+装饰线 368×18)+四段富文本 34px(内联沙块/金币/炸弹/循环箭头图标 44px)+Buttons 分节:两按钮示意 412×132 | idle | P2 | 无 | 文案=locale 键 rules-p1~p4;{min}/{max} 运行时按币种注入;正文终稿 TBC(§9) |
| ART-C-026 | history/历史区 | 历史面板 history_panel | 3 列汇总(label 24px+值 56px,竖分隔 2×112)+虚拟列表视口 1016×1208(行 1016×120:左结果区 339+右详情 677,copy 32²)+3 日期 tab 314×100+滚动箭头/加载更多渐变底栏 | 行四态:cashout/mine_hit/perfect_clear/in_progress | P1 | history_result_cashout.png / history_result_minehit.png / history_result_perfectclear.png | 结果盒 160×40 绿/橙红/金;in_progress 无盒;盈利正值=金渐变字 |
| ART-C-027 | language_popup | 语言弹窗 language_popup | 面板 800×960 r28(蓝 α0.6+横向渐变描边 w4,**矢量绘制无底图**)+标题 64px(白描边+发光,两侧饰线)+4 语言行 548×114(gap64) | row idle/active/hover/pressed | P1 | 无 | en/简体中文/繁體中文/Português;旧 4 张切图为孤儿 |
| ART-C-028 | maintenance | 维护屏 maintenance | 深色羊皮纸面板 878×238@bottom12%+标题 56px+描述 28px+右上退出钮 66px | idle | P1 | 无 | DOM 壳;文案键 maintenance/banned/unsupported-* 等 7 组 |
| ART-C-029 | exit_modal | 退出确认 exit_modal | 弹窗 895/1920vw×600/1920vw(**vw 特例随视口**);标题 3.43vw `#0D4C8D`;弹入 0.4s 过冲 | idle | P2 | 无 | 遮罩 rgba(0,0,0,.6) 可点关 |

规则:状态变体列逐项显式声明;ART-C 编号连续无重复(v1.1.0 全表按实装重写,编号与 v1.0 不对应,映射见 §9 changelog);参考图列文件均登记于 §7。

<!-- module: board=grid -->
### §3a 格子状态矩阵

| tile 状态 | 标识符 | 视觉 |
|---|---|---|
| 未翻开 | `tile_hidden` | 沙块盖面,**7 变体**(贝壳/素面×3/脚印/海星/双贝卵石)按固定矩阵铺排防重复感 |
| 安全翻开(玩家) | `tile_safe_revealed` | 棕底板+星星金币,全不透明;金币翻面+闪光+星火演出 |
| 爆雷(踩中) | `tile_mine_hit` | 棕底板+黑水雷,全不透明;火药爆(火球/火星/烟)+全屏屏裂 |
| 局末自动揭示 | `tile_auto_revealed` | 棕底板+金币或水雷,**α0.5 半透明**(区分玩家足迹),安静弹出 |
| 揭示保持 | `board_settled` | 全盘揭示态保持到玩家按 REFRESH(无自动重盖) |

> 入场 demo 盘(四角雷预览)仅存在于 dev mock,生产入场直接盖盘投注态,不出资产需求。

<!-- module: interaction=crash-step -->
### §3b 步进 / 倍率条展示与按钮约定

- 倍率条=**横向可滚档位链**:每档一枚 pill(值 `{x.xx}X` 两位小数),当前档换金 pill 并自动滚入视野;换雷数整链重建(3 雷 22 档 … 24 雷 1 档);两端箭头手动翻页,mask 边缘允许半枚裁切。数值以服务端梯为准(GDD §4)。
- 无独立大倍率读数:当前倍率的视觉载体=金 pill 高亮(+收款后余额条 WIN 值)。
- 按钮色彩与交互态约定(v1.1.0 实测更正:**收款不是红色**):

| 交互态 | 主操作按钮 | 颜色约定 | 状态变体 | 参考图 |
|---|---|---|---|---|
| 待机(betting) | 第三钮 REFRESH 面(=下注+开局) | 绿(白循环箭头面) | idle/hover/pressed | btn_action_green_idle.png + icon_refresh_face.png |
| 游戏中(playing,已首翻) | 第三钮 CASH OUT 面 | 绿底不变,overlay 换金星币+文案 | idle/hover/pressed/pending 置灰 | btn_action_green_idle.png + icon_cashout_starcoin.png |
| 任意时 | Bet / Mines 选择钮 | 蓝(区别于绿动作钮) | idle/hover/pressed/locked | btn_selector_blue_idle.png |

三钮同宽 322×108 并排(gap 20);三态=独立贴图(`_idle/_hover/_pressed`)。

---

## §4 动效需求清单

| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-M-001 | loading→main | 入场过渡 loading_intro | 黑幕布线性淡出 | 0.5s / 就绪+Game Start | P1 | 无 | 实测 GameCurtain 500ms |
| ART-M-002 | main/盘面 | 金币翻出 tile_flip_safe | pop 0.18s back.out(2)→硬币翻面(scaleX 镜像 0.12s×5 yoyo)+加法闪光 0.45s+6 星火 0.5s | 玩家翻安全格 | P0 | tile_reveal_coin.png | 实测 |
| ART-M-003 | main/盘面 | 爆雷 tile_flip_mine | pop 0.16s+回正 elastic 0.4s+爆闪 0.35s+冲击环 0.5s+9 碎屑 0.55~0.75s+火药(火球 0.28s+10 火星+5 烟) | 翻中雷 | P0 | tile_reveal_bomb.png | 实测;格内程序粒子 |
| ART-M-004 | busted/全屏 | 屏裂震动 screen_crack | 白闪 α0.7→0 0.4s;裂纹入 0.06s 出 0.6s(delay 0.5s);震屏 amp18 六步 0.45s | 爆雷同刻 | P0 | 无 | 程序化;裂心(540,~1056) |
| ART-M-005 | main/盘面 | 局末揭示 auto_reveal | 未翻格逐格安静弹出 0.2s back.out(1.6),α0.5 | 兑付/爆雷回执 | P1 | 无 | 玩家足迹保持全亮 |
| ART-M-006 | win/演出 | 胜利横幅 win_pop | 弹入 0.25s back.out(2)+呼吸脉冲 1↔1.20(0.35s yoyo 循环);4s 后淡出 | 兑付回执 | P0 | win_banner_base.png | 盘面不清场 |
| ART-M-007 | win/演出 | 通关序列 ultimate_sequence | 延迟 **1.95s**(读倍率节拍)→横幅(下移位)+Grand Prize+雨齐出;余额此刻才入账 | 翻满安全格 | P0 | 无 | 实测 |
| ART-M-008 | win/演出 | 金币彩带雨 win_rain | coin 雨 15/s(68~102px,3×3 帧翻面 8 圈,命 1.5~3s)+ribbon 雨 18/s(命 5~10s);顶部 20px 生成带,重力下落,尾 30% 线性淡出;发射 3s 自止 | ultimate | P1 | fx_coin_rain_sheet3x3.png | 实测 |
| ART-M-009 | 弹窗/通用 | 弹窗弹入 popup_pop | α0→1+scale0.6→1(back.out(2))0.25s;关闭反向;Toast 替换=crossfade 250ms | 各弹层开合 | P2 | 无 | 语言/警告/Toast/双选档层同参 |
| ART-M-010 | 顶栏/设置 | 微交互 micro_set | 倍率 chip 高亮换金+滚入;tab 缩放 lerp0.22/帧;音量档 crossfade 250ms+squish 360ms;语言钮 hover α0.9/scale1.1(0.25s) | 各交互 | P2 | multiplier_chip_current.png | 实测 |

规格停在需求清单级,不作逐帧规格。

---

## §5 音效需求清单

| ID | 屏幕/区块 | 组件 | 需求描述 | 时长/触发 | 优先级 | 参考图 | 备注 |
|---|---|---|---|---|---|---|---|
| ART-S-001 | 全局 | 按钮点击 sfx_click | 所有按钮通用点击音 | 点击 | P1 | 无 | click.mp3(SoundBus 全局) |
| ART-S-002 | win | 收款 sfx_cashout | 兑付成功音 | 兑付回执 | P0 | 无 | effect cashout.mp3 |
| ART-S-003 | busted | 爆雷 sfx_mine_hit | 爆炸音,2 变体随机 | 爆雷 | P0 | 无 | 实装复用 effect car pass by1/2.mp3(**文件名为沿用件**,建议补正式爆炸音源) |
| ART-S-004 | 全局 | 主循环 bgm | 海滩轻松氛围循环 | 全程 | P1 | 无 | bgm.mp3(1 条) |
| ART-S-005 | win | 通关 jingle(缺口) | 通关/大奖专属音**实装缺失**(effect win.mp3 在包内但未接线) | ultimate | P2 | 无 | 需求=接线或替换;现状通关只有 cashout 音 |

音量:BGM/SFX 双轨三档+静音(设置页);音效清单与实装 1:1(接线 5 支+孤儿 1 支)。

---

## §6 文案 / 本地化

baked-text 政策:游戏 Logo **烘焙**(en/zh/tr 三张;pt 回退英文图);**其余 UI 文字全部 `overlay`**(运行时文本层,4 语言 json 切换)。字体:主 UI 'Alibaba PuHuiTi 3.0'(回退 PingFang SC/Microsoft YaHei),注单/Toast 'Inter'。

| key | en | zh | baked/overlay |
|---|---|---|---|
| game_logo | Mine Beach | (zh 变体图) | baked |
| loading_label | LOADING... | LOADING...(硬编码不随语言) | overlay |
| start_game | Game Start | (loading.start-button.text) | overlay |
| bet_label | Bet | 投注 | overlay |
| mines_label | Mines | 地雷 | overlay |
| cashout_label | CASH OUT | 收款 | overlay |
| balance_label | BALANCE | 余额 | overlay |
| win_label | WIN | 盈利 | overlay |
| you_win | YOU WIN | 你赢了! | overlay |
| grand_prize | You have won the Grand Prize | 恭喜获得大奖! | overlay |
| bet_id | Bet ID: {id}(前缀硬编码) | 同左 | overlay |
| insufficient_balance | Insufficient balance. Please deposit to continue. | 余额不足 | overlay |
| reconnect_countdown | Reconnecting... Auto-cashout in {n}s | 重连中…{n} 秒后自动收款 | overlay |
| history_result | Cashed Out / Mine Hit / In Progress / Perfect Clear | 四态 | overlay |
| settings 组 | Volume/Sound Effect/Background Music/Image Quality(Low/Med/High)/Language | 设置组 | overlay |
| guide_rules | rules-p1~p4(含 Max Win: x10,000 文案,与表封顶口径矛盾见 GDD §4) | TBC 终稿 | overlay |

> 语言:en / zh(简) / tr(繁) / pt(巴葡);服务端告警文案自带三语(EnUS/ZhCN/ZhTW,pt 落 EnUS)。

---

## §7 参考图清单

| 文件 | 关联章节/组件ID | provenance | caption | 已知冲突 |
|---|---|---|---|---|
| logo_mineBeach_en.png | §1 / ART-C-002 | normative | 烧字 Logo 英文 1007×562:熔岩橙 Mine+水雷,水蓝 Beach+棕榈浪花 | 无 |
| loading_beach_illustration.jpg | §1 / ART-C-001 | normative | 加载滩景 1080×1920:宝箱+发光符文水雷+贝壳 | 无 |
| bg_main_beach.png | §1 / ART-C-005 | normative | 主背景(2160×3840 源图 50% 缩样存档) | 无 |
| bg_setting_underwater.png | ART-C-024 | normative | 设置页海底光柱背景 1080×1922 | 无 |
| tile_sand_var1.png | §3a / ART-C-009 | normative | 沙块盖面变体 1(贝壳卵石)180×183;**代表 7 变体族** | 无 |
| tile_reveal_base.png | ART-C-010 | normative | 翻开底板 184²(半透明棕) | 无 |
| tile_reveal_coin.png | ART-C-010 / ART-M-002 | normative | 星星金币 125×128 | 无 |
| tile_reveal_bomb.png | ART-C-010 / ART-M-003 | normative | 黑水雷 123×128(点燃引信) | 无 |
| multiplier_bar_track.png | ART-C-007 / §3b | normative | 倍率条沙金长底 2000×192(渲染 997×96) | 无 |
| multiplier_chip_idle.png | ART-C-007 | normative | 档位 pill 蓝 118×68 | 无 |
| multiplier_chip_current.png | ART-C-007 / ART-M-010 | normative | 当前档 pill 金 132×77(原生更大,同 scale 上屏) | 无 |
| counter_card_coins.png | ART-C-008 | normative | 金币计数卡 146×176 | 无 |
| counter_card_mines.png | ART-C-008 | normative | 炸弹计数卡 146×176 | 无 |
| btn_settings_gear.png | ART-C-006 | normative | 齿轮钮 212²(渲染 90²) | 无 |
| btn_selector_blue_idle.png | ART-C-012/013 / §3b | normative | 蓝果冻选择钮 334×112(Bet/Mines 共用底) | 无 |
| btn_action_green_idle.png | ART-C-014 / §3b | normative | 绿果冻动作钮 334×112(REFRESH/CASH OUT 恒底) | 无 |
| icon_refresh_face.png | ART-C-014 | normative | REFRESH 白循环箭头 68×68 | 无 |
| icon_cashout_starcoin.png | ART-C-014 | normative | CASH OUT 金星币 76×78 | 无 |
| balance_win_bar.png | ART-C-011 | normative | 余额盈利条 880×96(渲染 997 宽) | 无 |
| popup_bet_selector.png | ART-C-015 | normative | 投注弹层气泡 940×2082(50% 渲染;尾 33.4%) | 无 |
| popup_mines_selector.png | ART-C-016 | normative | 雷数弹层气泡 1856×1794(50% 渲染;尾 38.66%) | 无 |
| win_banner_base.png | ART-C-018 / ART-M-006 | normative | YOU WIN 底横幅 634×175(**无字底**) | 像素绿风格为沿用件,与海滩厚涂风格不一致——实装如此,重制与否由审签定 |
| fx_coin_rain_sheet3x3.png | ART-C-020 / ART-M-008 | normative | 金币翻面雨图集 512×427(3×3=9 帧) | 无 |
| fx_ribbon_sheet5x5.png | ART-C-020 / ART-M-008 | normative | 彩带碎片雨图集 512×512(5×5=25 帧) | 无 |
| loading_progress_container.png | ART-C-003 | normative | 进度条容器 1000×78(渲染 734×76) | 无 |
| btn_gamestart_idle.png | ART-C-004 | normative | Game Start 钮 700×214(渲染 560×171) | 无 |
| panel_warning_parchment.png | ART-C-023 | normative | 警告弹窗羊皮纸 900×620(渲染 976×576) | 无 |
| history_result_cashout.png | ART-C-026 | normative | 注单结果盒·绿(Cashed Out)160×40 | 无 |
| history_result_minehit.png | ART-C-026 | normative | 注单结果盒·橙红(Mine Hit)160×40 | 无 |
| history_result_perfectclear.png | ART-C-026 | normative | 注单结果盒·金(Perfect Clear)160×40 | 无 |

provenance 四值:`normative` / `illustrative` / `foreign-theme` / `placeholder`。本包参考图**全部取自实装资产(normative)**;v1.0 的 JILI/Spribe foreign-theme 截图与灰块示意图已随实装到位全部移除(见 §9 changelog)。文图冲突时以文本 + changelog delta 为准。

---

## §8 共用壳引用

| 模块 | 路径 | 本作差异 |
|---|---|---|
| history | ../_common/history.md | 注单字段:billId(可复制)/时间/betAmount/win/result(**cashout \| mine_hit \| perfect_clear \| in_progress** 四态)/币种逐行;汇总 Bet Count / Total Bet / Total Payout;窗口 1/3/7 天;滚动近底自动翻页 |
| locale | ../_common/locale.md | en / zh(简) / tr(繁) / pt(巴葡) 四语;pt 无烧字 logo(回退 en) |
| currency | ../_common/currency.md | 图标 CNY/PHP/USD+通用回退;小数位 USD 2 / CNY 1 / PHP 0 / BRL 2(未知币 2) |
| session | ../_common/session.md | 单一 session(SSO 踢线弹窗,断线不进倒数);快照续局(重放已翻格);**playing 断线 15s 倒数自动兑付** |
| exceptions | ../_common/exceptions.md | 维护/封禁/平台不支持/币种不支持/登录过期/无服务/未知 7 组 + reload 钮;告警 type0=弹窗 type1=Toast |
| params | ../_common/params.md | ACK 超时 8s;重连退避 1~5s ≤10 次;手动重连 watchdog 10s→刷新;翻格节流 600ms |
| telemetry | ../_common/telemetry.md | sensors 双 hook(client+游戏桥);业务事件随平台埋点 |
| backoffice | ../_common/backoffice.md | betList/defaultBet 按币种 BO 配置(**2~6 档**,越界回退兜底档) |

Settings / Language / Guide / History 屏承接 CG 系共用框架(见上表对应模块)。

---

## §9 TBC + 签字区

### TBC 表

| item | owner | 影响范围 |
|---|---|---|
| 色板 hex 精调(§1 语义色落地) | 设计 | §1 风格锚点 |
| Bet Option 各币种档位表(2~6 档) | 产品 + BackOffice | ART-C-015 弹层行数 |
| 玩法说明正文终稿(4 语言) | PM + 本地化 | ART-C-025 guide |
| 通关专属音源(接线 effect win.mp3 或新制) | 音效 | ART-S-005 |
| YOU WIN 底横幅是否按海滩风重制(现为像素沿用件) | 设计 | ART-C-018 / §7 冲突 |
| 屏裂特效是否补设计资产(现程序化占位) | 设计 + 动效 | ART-C-021 / ART-M-004 |
| pt 专属 logo 是否补做 | 美术 | ART-C-002 |

### 签字表

| 角色 | 姓名 | 日期 | 冻结范围 |
|---|---|---|---|
| Design Lead |  |  |  |
| Game PM |  |  |  |
| Art Reviewer |  |  |  |

### Changelog

| 版本 | 日期 | delta |
|---|---|---|
| v1.0.1 | 2026-06-29 | 下注面板移除金额输入框,仅选默认 Bet Option;reconnect 依运营商上限处理;FE/BE Lead 记为 Jack Liao |
| v1.1.0 | 2026-07-09 | 实装定稿全面重写:§3 组件 17→**29 项**并按实装重排(编号不与 v1.0 对应);**关键口径更正**——收款钮为**绿底双面钮**(REFRESH⇄CASH OUT,非 v1.0 的红色独立钮)、开局=REFRESH 钮(v1.0 的 newround 循环图标即此面)、无独立倍率读数(载体=倍率条金 pill 高亮)、胜利呈现=横幅组+盘面保持揭示(非满版覆层);§2 屏表实测化(含 vw 退出弹窗/维护屏);§3a 格态 4→5 态(补 α0.5 自动揭示与揭示保持,7 变体盖面);§3b 补倍率条滚动/重建规则;§4 动效 4→10 项全实测时长;§5 音效由 TBC 改 5+1 实装清单(爆雷音为沿用文件名,通关音缺口挂 TBC);§6 键表实值化(4 语言);§7 参考图 16→**30 张全 normative**(移除全部 JILI/Spribe foreign-theme 截图与灰块 illustrative 示意,登记像素横幅风格冲突);§8 史行四态/币种小数/重连参数实值;§9 TBC 10→7 项 |
