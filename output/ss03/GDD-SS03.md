# GDD-SS03 · Mahjong Streak(麻将连莊)玩法与数学设计文档

> **版本锚定**:Unity 构建 `1.0.0-56`(线上 `version.json` 2026-03-26,CDN `dev-assets-hybergaming/ss03`,2026-07-07 复核一致)。
> **信源纪律**:数学/规则全部一手直读服务端 repo(`slotmachine-ss03-socket` / `slotmachine-ss03-api`,下称 socket/api),逐条 cite `file:line`;构建内 Guide 字符串表(localization bundle,非截图)作交叉印证。**RTP/转轮条/权重在 KMS 签名 zip 内,未解密,一律标 server-authoritative**。零截图形态:本文无 validated 徽标,凡 extracted/derived 均如实标注。
> **分工**:本文只写玩法与数学。美术/资产 → `ART-AUDIO-SS03.md`;屏/坐标/动画时长 → `UI-GREYBOX-SS03.html`(注释面板)。

## 1. 游戏概述

- 品类:**级联(cascade)+ ways 计数**麻将主题老虎机,Guide 自述:"Mahjong Streak is a **4-5-5-5-4 reel, cascading video slot** featuring **Gold Symbols that transform into Wilds** and an **increasing win multiplier**…**2,000 ways**"(en 字符串表 id 35997964525625344)。
- 模式:服务端 `SlotMode` 仅 `NORMAL`(socket `math/SlotMode.java:8-9`);玩法态 = base spin / free spins(scatter 触发);无 jackpot、无 buy(见 §11)。
- 双端结构:客户端(Unity WebGL)只演出服务端下发的 `SpinRet` 场景序列;客户端无任何派彩公式。

## 2. 网格与符号

### 2.1 网格(4/5/5/5/4,共 23 格 + 顶部半格预览)
- 5 列(`COLS=5`,socket `server/Const.java:10`),行容器上限 6(`MAX_ROW_SIZE=6`,`Const.java:8`)。
- 每列可见格数由 `SpinUtils.rowStart(col)` 决定:边列(1、5)= 4 格,中三列(2、3、4)= 5 格(socket `utils/SpinUtils.java:25-28`;`SpinService.toFirstBoard` `SpinService.java:280-300`)。
- **UI 复刻件互证**(构建内 `BillDetailPage/ScenarioGrid`):Reel_1/5 各 4 个 `SymbolCell`、Reel_2/3/4 各 5 个,单元格 184×224,边列顶部相对中列下沉 102px(错列)——见灰盒 §③ 世界板复刻卡。
- **顶部半格预览行**:每列在可见窗上方补一个"半个字符"展示位——结算后按转轮序列补(`SpinUtils.gridPaddingWReel` `SpinUtils.java:38-56`,调用处注释"补充半个字符" `SpinService.java:329-330`);无中奖的最终盘面用随机 key 补(`gridPadding` `SpinUtils.java:30-36`),随机 key 在中三列有约 50% 概率给金色变体(`randomKey` `SpinUtils.java:13-19`,仅演出)。
- 格坐标编码:`position=(row+1)*10+(col+1)`(`SpinUtils.gridPositionTransfer` `SpinUtils.java:21-23`)。

### 2.2 符号集(socket `resources/math_table/symbol.json` 全量)
| code | 符号 | 麻将牌(资产名) | 3 连 | 4 连 | 5 连 |
|---|---|---|---|---|---|
| 0 / A | 發 | fa / GreenDragon | 10 | 25 | 50 |
| 1 / B | 中 | hongzhong / RedDragon | 8 | 20 | 40 |
| 2 / C | 白 | bai / WhiteDragon | 6 | 15 | 30 |
| 3 / D | 八萬 | bawan / EightMan | 5 | 10 | 15 |
| 4 / E | 五筒 | wutong / FiveDots | 3 | 5 | 12 |
| 5 / F | 五條 | wutiao / FiveBamboo | 3 | 5 | 12 |
| 6 / G | 三筒 | santong / ThreeDots | 2 | 4 | 10 |
| 7 / H | 二筒 | ertong / TwoDots | 1 | 3 | 6 |
| 8 / I | 二條 | ertiao / TwoBamboo | 1 | 3 | 6 |
| 100–108 | 金色變體 GA–GI | `*_gold` | 同对应白牌 | 同 | 同 |
| 201 | 胡 Hu = **Scatter** | Symbol_Scatter_Hu | — 不派彩,触发免费 | | |
| 202 | 百搭 = **Wild** | Icon_Wild/yuanbao | — 替代符,无独立赔付 | | |

- `hits` 数组按"参与连列数−1"取值,1/2 列恒 0(`symbol.json:8` 等每行 `hits:[0,0,x,y,z]`);金符赔付与白牌完全一致(`symbol.json:58-111`)。
- 資產側白/金各 9 + 胡 + 百搭,原生 184×224 与单元格 1:1(ADD §符号集)。

## 3. Win 机制与派彩(ways / scatter-pays 判定:**左起连列 ways**)

判定阶梯走到了①服务端直读,机制为 **ways(左起连续列,同列多枚相乘)**,非 payline、非任意位置 pay-anywhere:

1. **逐列计数**:统计每列各普通符号出现次数;金符计入其对应白牌 code(`settleBet` 步骤1,`SpinService.java:227-245`,金→normalCode `:241`);Wild 单独计数并记录位置(`:237-239`)。
2. **左起连续列约束**:符号必须在第 1、2、3 列都出现(首三列计数乘积为 0 即整组剔除,`updateScenarioDetails` `SpinService.java:172-180`);第 4 列有才算 4 连,第 5 列必须建立在第 4 列之上(`:175-177`,`evalTotalPayoff:194-198`;`TOTAL_SYMBOL=3` 为最短连列,`Const.java:14`)。
3. **Wild 加成**:Wild 对该列**所有**参与符号计数 +N(`settleBet` 步骤4,`SpinService.java:264-274`);Wild 替代除 Scatter 外全部符号(Guide id 35997071147261952)。
4. **ways = 连列计数乘积**(`evalTotalPayoff:200-203`);全盘最大 ways = 4·5·5·5·4 = **2000**(Guide "2000 Ways" id 35997438094336000)。
5. **单符号组派彩**:
   `payout = bet × ways × hits[symbol][连列数−1] × FIXED_FACTOR(0.05) × multiplier`(`evalTotalPayoff:204-209`)
   - `FIXED_FACTOR=0.05`(`Const.java:16`)= 1/`BET_CREDIT`,`BET_CREDIT=20`(api `Const.java:14`)。
   - 与 Guide 公式一致:"**Bet Amount / Bet Credit * Symbol Odd * Ways * Multiplier**"(id 43171421185105920);Guide 示例 "10 × 6 = 60"(id 35997664213458944)。
   - 主界面符号赔付随注额动态显示,Guide 页只显示基础赔付(id 79025353358565376)。
6. 明细随 `SpinRet.win_symbol` 下发:code/连列数/ways/odds/multiplier/payout/totalPayout(`server.proto` `WinSymbol`;`SpinSnapshot.WinSymbol` 装配 `SpinService.java:210-218`)。

## 4. 级联(cascade)与连莊倍率(win multiplier)

- **级联循环**(一次 spin 内,`generateScenarios` `SpinService.java:302-352`):结算 → 有奖则:记录场景 → **消除**中奖符号与参与的 Wild(`crush` `:110-134`)→ **金符不消除而是原位变 Wild**(`crush:127-129`)→ 上方符号下落、按**转轮序列**顺序补新(非随机;`cascade` `:75-108`,补位 `:94-107`)→ 场景号 +1 再结算;直到无奖。每个场景(scenario)即客户端一次消除/掉落演出。
- **倍率梯**:`multiplier = BASE_MULTIPLIER[min(scenarioId,3)+1]`(`evalTotalPayoff:186-187`):
  - base:**x1 → x2 → x3 → x5**(第 4 次及以后级联封顶 x5;`Const.java:22`)
  - free:**x2 → x4 → x6 → x10**(`Const.java:24`)
  - Guide:"multiplier starts at x…"(id 35997300688936960)、"Win up to 5x multipliers!"(id 63898971947393024)、"Win up to 10x multipliers in Free Spins!"(id 63903383910604800)。
  - 表现:倍率指示灯挂在转轮框顶栏(世界节点 `SlotMachine/Decorations/Y/TopFence/MatchComboDisplay`,指示灯 x1/x2/x3/x5),**不是屏顶悬浮条**(灰盒 §③)。
- "连莊/Streak" 即同一 spin 内级联连击的倍率递增;**跨 spin 不保留**(倍率由 scenarioId 决定,每次 spin 从 0 开始)。

## 5. 金符(Gold Mahjong)与百搭(Wild)

- 金符仅出现在第 2、3、4 列(Guide id 35997071147261952 "Gold Mahjong symbols only appear on reels 2, 3, and 4";演出侧 `randomKey` 只在中三列产生金色,`SpinUtils.java:15-17`)。
- 金符参与中奖时**转化为 Wild 留在原位**(`crush:127-129`);新一轮(级联)中该 Wild 生效(Guide id 35997242279059456 "...any gold symbols from the previou[s round transform]")。
- Wild 中奖参与消除后移除(`crush:123-126` 按 `wildPosition`)。
- **免费模式**:第 3 列(reel 3)所有符号(除 Wild/Scatter)以金色出现(Guide id 35997429093359616;演出信号 `MidasMiddleReel_Signal` Timeline 资产,构建内)。

## 6. 胡(Scatter)与免费旋转

- **计数时点**:一次 spin 全部级联结束后的**最终盘面**计 Scatter(`spin()` 中对最后一个 scenario 的 grid 计数,`SpinService.java:373-375`;`countScatter:140-154`)。
- **触发表**(`SCATTER_COUNT=3` `Const.java:12`;`FREE_COUNT_W_SCATTER` `Const.java:26`):

  | 胡数量 | 3 | 4 | 5 | 6 | 7 |
  |---|---|---|---|---|---|
  | 免费转数 | 10 | 12 | 14 | 16 | 18 |

  Guide:"3 trigger 10 Free Spins, each additional symbol adds +2 spins"(id 60638390826033152)。
- **发放机制**:服务端按次生成一次性 **token**(UUID,`triggerFreeSpin` `SpinService.java:409-436`),事件 `server:free_spin:triggered{tokens[],bet,triggered_spin_id,triggeredType:0}`(`server.proto` FreeSpinTriggered;发送 `:439-444`);客户端逐 token 调 `client:free_spin{token}` 消耗(`client.proto` FreeSpin;token 单次使用校验 `freeSpin` `:456-461`)。
- 免费局:`bet=0`、派彩按锁定的 `equivalentBet` 计(`freeSpin:467`);用免费专用转轮脚本 `normalStore.free()`(`:465`);倍率梯用 FREE 档(§4)。
- **retrigger 允许**:免费局中再触发按同表追加(`triggerFreeSpin` 的 `retrigger` 分支 `:419-422`;`SpinRet.scatter.triggerCount` 回传)。
- 激励免费:服务端存在 `IncentiveService`/`incentivized` 通道(`spin()` 参数 `:359`,埋点 `is_incentive` `:451,474`)——运营侧发放,机制 server-authoritative。

## 7. 数学表 / 转轮条 / RTP(server-authoritative)

- 转轮条按列封装:`Script.reels[] = Reel(index, reel[])`(`generateScenarios:309` 起使用);内容在 `math_table/*.zip`,**KMS 签名/加密**(`math/SignatureValidator|KMSSignatureValidator|ZipFileResolver.java`),**未解密——本文不给任何权重/RTP 数值**。
- 表变体(文件名即全部可知信息,socket `resources/math_table/`):`normal_zero`、`normal_zero98kai`、`normal_zero98kaini`、`normal_zero_95_kai`、`normal_Zero_BG97_Saitekika_BGadj`、`normal_risky`、`normal_ichi/ni/san/shi/go/roku`、`normal_kakuteiA/B`(命名暗示多档 RTP/波动配置,**具体值 server 权威**)。
- **分表策略**:按用户实验/MAB 决策选表——`MathTableStrategyManager.evaluate(ctx)`(`baseSpin` `SpinService.java:481-488`)、`AbExperimentStrategy`/`DefaultTableStrategyManager`(`PlayerTableRegistry.tableId(uid,…)` `DefaultTableStrategyManager.java:36-38`);命中日志 `[ABTest][AI:MATH][BASE|FREE]`(`:464,486`)。同桌 free 用同 tableId(`freeSpin:463-465`)。
- **MaxPayout 封顶**:每用户 auth 携带 `MaxPayout`,期望派彩超限则截断(`spin():361-371`);值来自 Redis 平台配置(`BetConfigService.getMaxPayout:46-51`)。

## 8. 投注与钱包

- **bet 档位:服务端下发,无客户端兜底清单**——`BetConfigService.getBetOptions(platform,op,currency)` 从 Redis 读,空即异常(`BetConfigService.java:28-44`);**档位数量与数值按平台/运营/币种可变,勿断言固定档数**。选注面板为 4×3 按钮容器,运行时按 count 自适应(灰盒 §⑥ BetAmountSelectorPanel)。
- 记账单位:`BET_CREDIT=20`(api `Const.java:14`)——赔率表以"注额/20"为 1 个 credit(§3.5)。
- 下注流:`client:spin{bet_amount}` → 扣款(`transactionService.bet` `SpinService.java:404`)→ `SpinRet`;余额变动另有 `server:balance:changed{balance}` 推送(`server.proto`)。
- 币种/显示:`Money{value,currency_code,display_scale,compact_notation(0:none,1:K)}`(`common.proto`);历史页提示"Current bet history shows only bets in <currency>"(字符串表 id 7294577764458496)。

## 9. 回合状态机与时序

```
IDLE ─ client:spin(bet) ──> SPINNING(服务端已判定,客户端演出 GridStop 落轮)
  └─> 逐 scenario 演出:结算高亮 → 消除爆炸(金符→Wild)→ 级联下落补位 → 倍率灯 +1 档
  └─> 最终盘面:胡≥3 ? ──> server:free_spin:triggered(tokens) → 免费过场(幕布/Noticer)
IDLE(free)─ client:free_spin(token) ──> 同上,FREE 倍率梯,计数 HUD(FreeGamePanel)
  └─> tokens 用尽 → EndFreeGame 结算(TOTAL WIN)→ 回 base
```
- 服务端**一次性返回整段级联剧本**(`SpinRet.scenarios[]`),客户端只按序演出;`GridStop` 为各列停轮索引(`spin():377-381`)。
- 中奖分级演出(大奖/巨奖/超级巨奖)与各段动画时长:引擎 AnimationClip 可读(49 支)——**时长唯一权威在灰盒 HTML 注释面板**,本文不重复。
- 快速/停止:turbo 三档 Slow/Medium/Fast,默认 Medium(Guide id 35998142003404800);Auto Spin 面板选局数,进行中 Spin 键变 Stop 显示剩余局数(Guide id 35998137670688768)。

## 10. Socket 协议(protobuf,socket.io 传输)

事件全集(grep socket 源码,`SpinHandler` 等注册处):
| 方向 | 事件 | 消息体(`resources/protocol/*.proto`) |
|---|---|---|
| C→S | `client:spin` | `Spin{bet_amount:Money}` |
| C→S | `client:free_spin` | `FreeSpin{token}` |
| C→S | `client:balance` | `Void` |
| S→C(ACK) | (spin 应答) | `SpinRet{spin_id, spin_type(0base/1free), GridStop[], scenarios[]{id,grid[30]{position,code},win_symbol[]}, scatter{code,count,triggered,triggerCount}, total_payout, bet}` |
| S→C | `server:free_spin:triggered` | `FreeSpinTriggered{triggered_spin_id, triggered_type(0:scatter), tokens[], bet}` |
| S→C | `server:balance:changed` | `BalanceChanged{balance}` |
| S→C | `server:alert` | `Alert{code, type(0:popup,1:toast), message_en_US/zh_CN/zh_TW}` |

- 认证/入口(平台版宿主 B):`POST {KONG}/game/ss03-api/v1/api/auth/verify|validate`(B `service/auth.ts:43,71`);Unity 环境注入 `SetEnvironmentConfig{apiUrl,socketUrl,socketPath:"/game/ss03-socket/socket.io",…,defaultConfig{LocaleKey,ShowExitButton,MuteAudio,UseCompanyPlayButton}}`(B `UnityBridge.tsx:46-77`)。
- 账单:api 服务分页(`DEFAULT_PAGE_SIZE=10`,api `Const.java:5-9`);单注详情=BillDetailPage(逐 scenario 复盘,含公式行 Formula/Calculation)。

## 11. 异常、断线与门控功能

- **弹窗/提示文案**(构建字符串表,en):3 分钟无 spin 登出(id 514792862244864)、断线请重载(id 515962980786176)、连接中(id 516287741550592)、余额不足(id 516539575951360);承载 UI = ReconnectingPopup/ToastPopup/WarningPopup(灰盒 §⑥)+ `server:alert` 的 popup/toast 分型。
- **宿主终态页**:auth 失败/维护/封禁/币种不支持/刷新 → `ss03/exit?page=…`(B `UnityBridge.tsx:110-171`;Unity→UI `PlayerBanned` `receiveActionRequestFromUnity.ts:32`);维护另有宿主 A Maintenance 组件。
- **config-gated / 存量未上线**(代码是运行时超集,存在性如实记录):
  - `Buy 10 FG` 文案存在(id 17498488051851264)但**服务端无 buy 事件** → 购买免费功能未上线;
  - 菜单 TabList 含 `Exit` 键(构建节点,0 尺寸 runtime 排布;宿主 `ShowExitButton` 配置项对应);
  - 设置页 `ImageQuality`(Low/Mid/High)分区 `act=false` 默认隐藏;
  - `DebugUI*` 调试样板 24 件在构建中(默认不显)。
- 断线重连:`ReconnectingPopup`(Mask+Toast 条,灰盒 §⑥);无独立重连协议——重新走 auth+socket 连接(宿主 `ReloadGame` 桥事件,A `unityHandlerRegistry.ts:34-174` / B `receiveActionRequestFromUnity.ts:18-159`)。

## 12. 交叉引用

- 资产/音频/风格与玩法→美术适配 → `ART-AUDIO-SS03.md`(精炼设计文档 + 计数对账指针)。
- 屏结构/坐标/徽标/越界分诊 → `UI-GREYBOX-SS03.html`(23 帧竖屏,零截图形态)。
- 机器可读全量 → `elements-SS03.json`(ui_elements 320 可见承重件 + assets 875 逐文件资产清单)。
