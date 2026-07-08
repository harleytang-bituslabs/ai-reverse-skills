# GDD-SS02 · Beach Party(沙滩派对)玩法与数学设计文档

> **版本锚定**:Unity 构建 `1.0.0-71`(线上 `version.json` 2026-03-16,CDN `dev-assets-hybergaming/ss02`,2026-07-08 复核一致)。
> **信源纪律**:`~/harley/ss02` 无服务端 repo → 数学走判定阶梯②:**构建内 Guide 资产一手直读**(localization string-tables 规则文本 + `Setting_Guide_SymbolValue` 赔付贴图,均为 extracted,非截图);转轮权重/RTP/买价 server 权威不编。变体 repo(ss02a/b)文档为换皮遗留,数值一律不采信。零截图形态,无 validated。
> **分工**:美术/资产 → `ART-AUDIO-SS02.md`;屏/坐标 → `UI-GREYBOX-SS02.html`;机器清单 → `elements-SS02.json`。

## 1. 游戏概述

- Guide 自述(string-table id 1936333923672064):"**Beach Party is a 6×5 cascading slot machine**";两模式 Base / Free(base 4+ Scatter 触发);**中奖条件 = 任意位置 ≥8 枚同符号(pay-anywhere/scatter-pays)**;免费模式乘数符号(2×…100×)每转可落。
- 网格 **6 列 × 5 行规整 30 格**:Guide 文本 + 构建内 UI 复刻件 `BillDetailPage/ScenarioGrid`(6 Reel × 5 SymbolCell,cell 168×168)双源互证;世界转轮 6 根(世界 x=±2.54/±1.52/±0.51,列距 1.015)。
- 无 Wild 替代符(规则文本无替代规则;资产名 `Symbol_Wild_X*` 实为乘数气球,见 §4)。

## 2. 符号与赔付表(一手:构建 Guide 贴图 `Setting_Guide_SymbolValue`,odds×(总注/20))

| # | 符号 | 8~9 枚 | 10~11 枚 | 12+ 枚 |
|---|---|---|---|---|
| 1 | 游艇 A_YACHT | 200 | 500 | 1000 |
| 2 | 水上飞机 B_SEAPLANE | 50 | 200 | 500 |
| 3 | 皮划艇 C_RAFT | 40 | 100 | 300 |
| 4 | 圣代 D_SUNDAE | 30 | 40 | 240 |
| 5 | 甜筒 E_CONE | 20 | 30 | 200 |
| 6 | 冰棍 F_POPSICLE | 16 | 24 | 160 |
| 7 | 芒果 G_MANGO | 10 | 20 | 100 |
| 8 | 西瓜 H_WATERMELON | 8 | 18 | 80 |
| 9 | 蓝莓 J_BLUEBERRY | 5 | 15 | 40 |

- **派彩公式**(id 131898868228096):`Payout = (Total Bet / 20) × Winning symbol odds (× Multiplier, if any)`——记账单位=总注/20(BetCredit 制,同族引擎)。
- Scatter(摩天轮)不派彩只触发;"Special Symbol Payout Value" 分区(id 131922461188096)承载 Scatter/乘数说明。
- 显示规则:赔付随注额动态换算成货币两位小数(id 1936333923672064)。

## 3. Win 机制:8+ 任意位置计数 + 级联(cascade)

1. 每次落轮后统计各普通符号全盘数量;**≥8 枚即中奖**(不看列连续、不看线)。
2. 中奖符号爆裂消除(世界符号格 prefab `explose effect`),上方符号落下补位 → 再结算,循环至无新奖(Guide "cascading")。
3. 单次 spin 的累计中奖按符号分组进 `BillDetail_WinSymbolLine`(Symbol Count/Symbol Payout 行,ids 46402125096280064/46402293589860352);乘数行 `BillDetail_MultiplierLine`(Total Multiplier,id 47566939642388480)。

## 4. 乘数气球(仅免费模式;资产名 Symbol_Wild_X*)

- 档位 **2×/3×/5×/10×/20×/30×/50×/100×**(string-table id 1936333923672064 列全档;Spine 资产 `MULTIPLIER_X2..X100` 8 套对齐)。
- 规则(id 16071697227571200):仅 Free Game 出现;**作用于 base payout**;**多枚同落相加后再乘**:`total = base payout × (M1 + M2 + …)`。
- 落轮时机:每次免费 spin 均可落(id 1936333923672064)。权重/期望 server 权威。

## 5. Scatter 与免费旋转

- Scatter=霓虹摩天轮,**全部 6 轮可现**(id 1936333923672064 "Scatter symbols appear on all reels")。
- **触发表**(id 131934100381696 + 15258989653647360):Base 落 **4+** → **10 次免费**;免费中落 **3+** → **再 +10 次**(retrigger)。
- 免费开场 `FreeSpinNoticer`("You Have Won {0} Free Spins!!!" id 2561089454727168,START 钮),结算 "TOTAL WIN: {0}"(id 19990302730215424);免费模式换紫夜场景+乘数气球启用。

## 6. 购买功能(构建+文案齐备;价格 server 权威)

- **Buy Free Game**(`GameBoardUI_Placeholder/PurchaseFreeSpin`,272×180 面板):"BUY FEATURED GAMES"(id 14343720601714688)、确认文案 "Confirm To Buy {0} Featured Games:"(id 14344181056602112)→ 直接买 **10 次免费**(Guide id 1936333923672064 "Instantly buy 10 Featured Games")。
- **Double Chance**(`…/DoubleChance`,toggle on/off):"MORE FREE GAME CHANCES"(id 14344430022098944)→ 加价提升免费触发率(Guide "buy more chances to hit Free Games")。
- 确认弹层 `EnsureFreePanel`(Buy/Close,默认隐藏);两面板挂 1920×1080 ScreenBoard(灰盒 §④)。价格倍数/触发率提升值未在客户端资产层出现 → server-authoritative。

## 7. 投注、时序与操作

- bet 档位:服务端下发(选注面板 `BetAmountSelectorPanel` 4×3 钮阵运行时填充,数量自适应);"Bet Credit"/"Amount/Credit {0}" 记账口径(ids 47840134949756928/47840228595982336)。
- 操作(Guide id 1936864054337536):Spin / Auto Spin(AutoSelector 局数钮 10/20/50/100…资产族)/ **Quick Spin(turbo,双灯两档)** / Stop——加速"不影响实际结果"。
- 回合流:IDLE → spin(服务端判定,客户端演出级联剧本)→ 逐段消除+补位 → Scatter≥4?→ FreeSpinNoticer → 免费循环(乘数气球)→ TOTAL WIN 结算 → 回 base。动画时长唯一权威在灰盒注释面板。

## 8. 协议与宿主桥(无服务端 repo,客户端侧可证部分)

- 宿主→Unity:`HandleAppConfig`(gameConfig:language/**showExitButton**/**muteAudio**/**useCompanyPlayButton**/openingVideoFolder,`defaultSettingProcessorRegistry.ts:34-40`)。
- Unity→宿主(`unityHandlerRegistry.ts`):`BridgeReady`/`GameReady`/`ReloadGame`/`ExitGame`(回 `<gameType>_backURL` 或 history.go(-1))/`CopyToClipboard`。
- socket 协议(spin/结果结构)无服务端 repo 一手 → server-authoritative;账单结构可由 BillDetail 字段反推(Round/Bet Credit/Payout/Multiplier/Balance After Bet,ids 47840036597522432 等)。

## 9. 异常与门控

- 弹窗文案(string-table):3 分钟闲置登出(514792862244864)、断线重载(515962980786176)、连接中(516287741550592)、余额不足(516539575951360)、网络不稳(30117819004739584);载体 Reconnecting/Toast/Warning(popuppage bundle)。
- 账单状态:In Progress / Completed / **Refunded**(ids 17263283513393152 等);`BetItem_Boost` 金标=激励局标记(incentive,机制 server 权威)。
- config-gated/存量:宿主 ConfirmModal/BaseModal 未接线(死码);`TestPanel`(ScreenEffect 内测试板);`ScreenEmptyClicker`;Exit 按钮由 `showExitButton` 平台配置门控。

## 10. 交叉引用

- 美术/音频/玩法适配 → `ART-AUDIO-SS02.md`;屏/坐标/徽标/分诊 → `UI-GREYBOX-SS02.html`(23 帧,双朝向);机器全量 → `elements-SS02.json`(ui_elements 510 + assets 756)。
