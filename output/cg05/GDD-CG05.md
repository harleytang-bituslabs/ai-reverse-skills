# GDD-CG05 · MineBeach(海滩扫雷)游戏设计文档

> **来源锚点**:`crashgame-cg05-ui @ 65b8ced`(feat: rework play buttons & guide, align UI with real socket)。
> 本文只答「什么游戏、什么规则、什么状态流转」;视觉/资产见 `ART-AUDIO-CG05.md`,逐屏几何与动画时长唯一权威在 `UI-GREYBOX-CG05.html`。
> 徽标:全文 **code-derived**(部署形态零截图);经济值一律标注 server-authoritative / mock-占位。

---

## 1. 定位与形态

- **品类**:单人步进式 Mines(crash-step × 5×5 grid)。玩家逐格翻沙块,安全=金币+倍率上爬,可随时收款;踩雷=本局清零;翻完全部安全格=自动按满盘倍率兑付(Grand Prize)。
- **引擎/画布**:Pixi.js v8,设计画布 **1080×1920 竖屏**(`main.tsx:15-16` baseWidth/baseHeight),壳层 contain 缩放;DOM 壳(React)负责 loading/维护/弹窗,Pixi 负责主场景。
- **语言**:en / zh(简体) / tr(繁体) / pt(巴葡)——`localizationLocalesRegistry.ts` 激活映射 + `src/assets/localizations/{en,zh,tr,pt}.json` 四份;jp/vi/th/id/kr 均被注释未启用。logo 只有 en/zh/tr 三张,**pt 回退英文 logo**(`TopBar.titleLogoAlias`)。
- **货币**:图标三币 CNY/PHP/USD + 通用符号回退(`MainSceneManifest CURRENCY_ICON_CODES`);小数位表 USD 2 / CNY 1 / PHP 0 / **BRL 2**(`currency.ts CURRENCY_DECIMALS`,BRL 无专属图标走回退)。币种来自登录快照 `userVerifyResponseData.currencyType`。
- **非目标**(实测确认):无 Buy/Free Round、无多人、无 Auto-Play/Auto-Cashout 面板(PlayerHUD 注释明删)、无手动输入注额、无难度换皮(雷数即难度)。

## 2. 回合状态机

相位(`GameManager.GamePhase`):`idle → betting → playing → busted | round_settled`;`cash_out / perfect_clear` 是**瞬态事件**(`NET_MY_CASHOUT{isUltimate}`),不驻留相位。

```
loading ──GAME_READY+Game Start──► betting(入场即此态;RealSocket SHOW_ENTRY_DEMO=false)
betting ──REFRESH 钮(=下注+开局)──► playing
playing ──格击 UI_GO(idx)──► safe: NET_TILE_REVEAL(金币,倍率上爬,首翻后第三钮变 CASH OUT)
                            └► mine: NET_ROUND_BUSTED → busted → round_settled(全盘揭示)
playing ──CASH OUT──► NET_MY_CASHOUT(isUltimate=false) → round_settled(YOU WIN 4s 自动隐)
playing ──翻满安全格(AdvanceRet.gameOver)──► 自动兑付 isUltimate=true → round_settled(10s 级演出)
round_settled ──REFRESH──► betting(盖盘)──(同一次点击链)──► 下注 → playing
```

**关键差异(vs 自动回合类)**:`enterSettled` **无自动回投注定时器**——盘面保持揭示直到玩家再点 REFRESH(`RealSocket.enterSettled` 注释明示;`SETTLE_DURATION_MS 4000/ULTIMATE 10000` 为**死常量**,只清不设)。YOU WIN 横幅自身 4s 自动隐(`GameView WIN_BANNER_HOLD_S`),但相位不回。

信号契约(数据层→表现层,均 `GameManager.ts`/`PlayerWallet.ts` 定义):
`NET_ROUND_BETTING/PLAYING/BUSTED/SETTLED`、`NET_TILE_REVEAL{index,safeCount,multiplier}`、`NET_MINES_REVEAL_ALL{layout[25],picked[],hitIndex|null,demo?}`、`NET_MY_CASHOUT{bet,multiplier,baseMultiplier,cashout,isUltimate}`、`NET_MULTIPLIER`、`NET_ROUND_ID`(bet id 显示/清空)、`NET_ROUTE_LADDERS{mineCount→x_k[]}`、`NET_ROUND_RESUME`、钱包侧 `WALLET_BALANCE/BET_AMT/BET_LOCKED/PLAY_STATE('bet'|'cashout')`。

## 3. 核心玩法参数

| 参数 | 值 | 出处 |
|---|---|---|
| 盘面 | 5×5=25 格,行主序 index=row*5+col | `minesMultipliers.TILE_COUNT` / `MinesGrid N=5` |
| 雷数 | 3–24,默认 4 | `MIN/MAX/DEFAULT_MINES`;选择器 4 列×6 行矩阵(两空格) |
| 投注 | 仅弹层选档,**无手输**;服务端 `/bet/config` 下发 2–6 档(`betList`+`defaultBet`),兜底 `[0.2,0.5,1,3,5,10]`(USD)/defaultBet 1.00;币种默认注 USD→1 其余→0.1 | `PlayerWallet BET_QUICK_VALUES` / `MyBetPanel.onBetConfig`(<2 或 >6 档 console.error 并保持兜底) / `PlayButton.defaultBetValue` |
| 开局 | REFRESH 钮=重置盘面+下注(扣款点);翻格免费 | `PlayerWallet.onRefreshUI`→`PLAYER_REFRESH`+`tryPlaceBet` |
| 翻格 | 点盖格→`UI_GO(idx)`;一次一发(`pickInFlight`),已翻格/非 playing 忽略;600ms 节流 | `MinesGrid.onCellTap` / `RealSocket GO_THROTTLE_MS` |
| 收款 | 首翻后第三钮变 CASH OUT;`payout=bet×eff`,服务端 `payoutAmount` 权威;请求期 pending 门挡双击 | `MyBetPanel.onTileReveal` / `RealSocket.onCashout` |
| 完美通关 | safe advance 回执带 `gameOver=true`→自动兑付 `isUltimate`,余额从 `balanceAfterPayout` 原子入账,UI 余额更新**延迟到 Grand Prize 弹出**(`ULTIMATE_WIN_SHOWN`) | `RealSocket.finalizeAutoCashout` / `PlayerWallet.deferNextBalance` |
| 揭示规则 | 局末全盘揭示:玩家翻的全亮,其余 α0.5;踩的雷=爆点特效;盘面保持到下局 REFRESH | `MinesGrid.onRevealAll AUTO_ALPHA=0.5` |
| 弹层互斥 | bet/mines 选择器一次只开一个;`roundLive` 期间禁开(雷数只对下一局生效) | `MyBetPanel.toggleBetPopup/toggleMinesPopup` |

## 4. 数学框架(倍率表)

**前端副本表** `minesMultipliers.MINES_MULT`(注释:transcribed verbatim from the math table;**服务端为权威源**——真跑时 `client:routes` RPC 下发全部雷数的 x_k 梯,`NET_ROUTE_LADDERS` 覆盖本地表,mock 才用本地表):

`MULT[m][k-1]` = 翻开第 k 个安全格后的兑付倍率;行末=该雷数满盘封顶(自动兑付值)。

| 雷数 m | 首格 x₁ | 封顶(行末) | 档数(=25−m) |
|---|---|---|---|
| 3 | 1.11 | **20.00** | 22 |
| 4(默认) | 1.16 | 20.00 | 21 |
| 5 | 1.22 | 20.00 | 20 |
| 6 | 1.28 | **80.00** | 19 |
| 7 | 1.35 | 80.00 | 18 |
| 8 | 1.43 | 80.00 | 17 |
| 9 | 1.52 | 80.00 | 16 |
| 10 | 1.62 | 80.00 | 15 |
| 11 | 1.74 | **300.00** | 14 |
| 12 | 1.88 | 300.00 | 13 |
| 13 | 2.03 | 300.00 | 12 |
| 14 | 2.22 | 300.00 | 11 |
| 15 | 2.44 | 300.00 | 10 |
| 16 | 2.71 | **800.00** | 9 |
| 17 | 3.05 | 800.00 | 8 |
| 18 | 3.48 | 800.00 | 7 |
| 19 | 4.06 | 800.00 | 6 |
| 20 | 4.88 | 800.00 | 5 |
| 21 | 6.09 | **200.00** | 4 |
| 22 | 8.12 | 200.00 | 3 |
| 23 | 12.19 | 200.00 | 2 |
| 24 | **24.38** | 24.38 | 1 |

(全 22 行逐档数值以 `minesMultipliers.ts:16-39` 为准,elements/灰盒 SCENES 帧含 m=3 全梯。)

- **RTP 系数可复算 ≈0.975**:公平倍率 `fair(k)=C(25,k)/C(25−m,k)`,实测首档均 ≈ fair×0.975(例 m=24,k=1:25×0.975=24.375→24.38;m=3,k=1:25/22×0.975=1.108→1.11)。**深档被封顶截断**(m=3 公平尾档远超 20),故深档有效 RTP<0.975;封顶分档 20/80/300/800/200 与雷数区间绑定。
- **文案矛盾(实装事实,须记录)**:guide 文案 `setting-page.guide.rules-p3` 写 **“Max Win: x10,000”**,而客户端表最大封顶 800.00;`Max Payout = Max Win × Max Bet`。孰为运营真值由服务端定,客户端两处不一致原样记录。
- 显示格式:`multiplierLabel = value.toFixed(2)+"X"`(两位小数大写 X);金额 `toFixed(2)` 千分位 `toLocaleString`。
- wire 遗留:`AdvanceRet.accumulatedBonus/bonusType` 字段存在(chicken-road 协议),`eff=raw×(1+cumBonus)`,但 **mines 无 reveal-bonus,cumBonus 恒 0,base==eff**(`GameView.onMyCashout` 注释)。

## 5. 网络协议(RealSocket,生产路径)

`_devBypass=false`(`GameEntry DEV_BYPASS=false`)→ `RealSocket`(socket.io-client + protobuf/base64,`cg05-socket` 后端);`MineBeachSocket` 仅 dev mock。

| RPC/推送 | 契约 | 说明 |
|---|---|---|
| `client:game:start` | `StartGame{betAmount:toFixed(2), currency, difficulty:String(mineCount)}` → `StartGameRet{sessionId, balanceAfterBet, laneMultipliers[]}` | **wire 的 difficulty 字段=雷数字符串 "3".."24"**(RouteKey 解析 int,送 EASY 会被拒);回执梯=本局权威 x_k;无隐式首步(修过 tile0 自动翻 bug) |
| `client:game:advance` | `Advance{sessionId, position:0..24}` → `AdvanceRet{stepNo, safe, currentMultiplier, gameOver, minePositions[], balanceAfterPayout?}` | 每次翻格;`safe=false`→全盘揭示+busted;`gameOver=true`(safe)→完美通关自动兑付 |
| `client:game:cashout` | `GameCashout{sessionId}` → `GameCashoutRet{payoutAmount, finalMultiplier, cumulativeBonus, balanceAfterPayout, capTriggered, minePositions[]}` | `payoutAmount` 权威;`capTriggered`→isUltimate |
| `client:snapshot` | → `GameSnapshot{session{sessionId,difficulty(=雷数),currentStepNo,currentMultiplier,laneMultipliers,betAmount,revealedPositions[],cumulativeBonus,gameOver}}` | (重)连后恢复:重放已翻格、re-emit `NET_BET_CONF` 锁 UI 为 CASH OUT;空快照且 phase=playing→回 betting |
| `client:routes` | → `RouteTable{routes[{difficulty(=雷数), laneMultipliers[]}]}` | 连接后拉一次全部 3..24 梯 → `NET_ROUTE_LADDERS`(倍率条显示后端值) |
| `client:balance` | 空包触发推送 | 连接后请求余额 |
| 推送 `server:balance:changed` / `server:alert{code,type,message×3语}` / `server:game:expired{sessionId,payoutAmount}` | alert type 0=弹窗 / 1=Toast;`sso-disconnected` 置一次性旗标;expired→会话过期 Toast+防御性收局 | 文案按 locale 取 EnUS/ZhCN/ZhTW(`pickAlertMessage`;pt 走 EnUS) |

**时序常量**:ACK 超时 8s(超时→`ACK_TIMEOUT` type1 Toast 1s+按钮回弹);GO 节流 600ms;重连 socket.io 自动 ≤10 次、退避 1–5s;**playing 中断线→15s 倒数自动兑付**(服务端侧保障,Toast 每秒 tick,归零后快照为空即回 betting);SSO 踢线跳过倒数;重连全败→Warning 弹窗,手动重连 10s watchdog 兜底整页 reload(`MainScene RECONNECT_RELOAD_TIMEOUT_MS`)。

## 6. 边界与输入锁

| 边界 | 行为 | 出处 |
|---|---|---|
| 余额不足 | `tryPlaceBet` 阻断+Toast `player-wallet.balance.insufficient` | `PlayerWallet.tryPlaceBet` |
| 断线(playing) | Toast「Reconnecting…」常驻+15s 倒数;归零→自动兑付文案;重连成功→3s Toast | `MainScene.onReconnectTick` |
| 闲置超时 | 服务端 `alert code='idle-timeout'` → 下一次 NET_RECONNECTING 换 Warning 弹窗(带 15s 倒数文案) | `MainScene.onNetAlert` |
| 会话过期/内部错误 | `internal-error`→常驻 session-expired Toast(需刷新);`server:game:expired`→3s Toast+防御性收局 | 同上 |
| SSO 重复登录 | `sso-disconnected` type0 弹窗;断线不进倒数 | `RealSocket.onPushAlert` |
| 收款进行中 | `cashoutPending` 拒双击;`NET_CASHOUT_PENDING/FAIL` 驱动按钮禁用/回弹 | `RealSocket.onCashout` |
| 双弹层/局中改注 | 弹层互斥;`WALLET_BET_LOCKED` 锁注(下注后至局末);雷数局中锁定 | `MyBetPanel` |
| 首次连接失败 | type0 弹窗(三语内置文案);重连期间 connect_error 静默 | `RealSocket.onConnectError` |
| 维护/封禁/不支持 | DOM 壳 Maintenance 屏(exceptionRegistry 键:maintenance/banned-player/unsupported-platform/unsupported-currency/log-expired/no-server/unknown) | `clientExceptionRegistry` |

## 7. mock-vs-real 对照(勿把占位当真值)

| 项 | mock(`MineBeachSocket`/`CrashApiDummy`) | real(`RealSocket`/`CrashApiClient`) |
|---|---|---|
| 初始余额 | INITIAL_BALANCE=100(占位) | 登录快照+`server:balance:changed` |
| 倍率梯 | 本地 `MINES_MULT` 表 | `client:routes`/`StartGameRet.laneMultipliers`(权威) |
| 投注档 | DEMO `[0.2,0.5,1,3,5,10]`/default 1 | `/bet/config` betList+defaultBet(按币种) |
| 入场态 | 揭示 demo 盘(四角雷 `DEMO_MINE_TILES=[0,4,20,24]`) | 直接 betting(`SHOW_ENTRY_DEMO=false`;demo 代码在但关) |
| 历史/汇总 | CrashApiDummy 确定性假数据 | REST `/bet/summary` `/bet/history`(注单字段见 §8) |
| 派彩 | 本地表算 | `payoutAmount` 服务端 |

## 8. 历史注单(REST)

窗口筛选 Today/3 天/7 天(`FILTER_FROM_DAYS 1/3/7`);行状态 4 态:`cashout`(绿盒"Cashed Out")/`crashed`(橙红盒"Mine Hit"——**键名仍叫 crashed,显示已 mines 化**)/`perfect-clear`(金盒)/`in-progress`(灰,无盒);字段:billId(可复制)、时间、betAmount、盈利(正=金渐变)、币种逐行(`data.currencyType`,非当前钱包);汇总三列 Bet Count/Total Bet/Total Payout。分页:滚动近底自动拉下一页(0.5s poll+`hasMore`)。

## 9. 工程遗留与死代码(复现时须知)

- **cg03(Cluck Dash)遗留仍上屏**:`label_youWinBanner`(像素绿横幅=YOU WIN 底图)、踩雷音效=随机 `effect car pass by1/2.mp3`(文件名遗留、用途已改)、GO 节流注释仍写 hop 0.2+0.4。
- **死代码**(定义未接线,勿复现):`CrashedBanner`(load 后永不 show)、`BetPhaseView`(空桩)、`LoadingPanel`(Pixi 加载层,实际是 React Loading.tsx)、`CoinEffect/ConfettiEffect/CashOutAnim`(Texture.WHITE 占位,无调用者)、`LayoutTest`、`LayoutDetector`(被 DebugPanel 取代)、GuidePage 旧卡片/弹层 mock 一族、快选钮行(`quickBetLayer.visible=false`)、MIN/MAX 行(已删含资产)、`KNOWN_DIFFICULTIES`。
- **悬挂引用**:manifest `bet_input_bg → bet_amount_input_container.png`(文件已删,eager 加载会告警);`SettingPage:304` fallback `placeholder.png`(不存在,仅 mute 图缺失时才触发)。
- 孤儿资产 19 件清单见 `elements-CG05.json.assets[referenced=false]` 与 ADD §8。
- 调试:DebugPanel ESC×3 / 左上角 80×80 三连点唤出(50vh 顶置,console/network 两 tab);`LayoutZones` overlay 默认隐藏。
- 仓库杂项:`network/CluckDashSocket.ts.bak`(cg03 mock 备份,不参与编译);`index.html` 装有全局 `window.onerror` 红屏错误 UI(标题 "Mine Beach",加载 `config/index.config.js` 注入 `window.indexConfig` 网关地址);`public/favicon.ico` 与 `src/assets/react.svg` 零引用(浏览器约定/Vite 模板遗留)。
- 壳层缩放模型:middleware `AppRoot` 固定 1080×1920 设计画布 `scale(min(vw/1080, vh/1920))` contain 居中(mainPage 黑边);DOM 壳裸像素坐标(top:1727 等)在此画布内成立;Splash 黑幕 z1100(cg05 无开屏视频,0.5s 直接淡出)。

## 10. 交叉引用

- 逐屏盒几何/态帧/动画时长表 → `UI-GREYBOX-CG05.html`(19 帧 282 boxes;注释面板②为动画唯一权威)。
- 资产/风格/音频触发 → `ART-AUDIO-CG05.md`。
- 机器清单(282 ui + 128 assets 含孤儿标记)→ `elements-CG05.json`。
