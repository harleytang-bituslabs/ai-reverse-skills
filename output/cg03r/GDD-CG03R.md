# GDD-CG03R · Cluck Dash(小鸡狂奔)玩法与数学设计文档

> **版本锚定**:`crashgame-cg03r-ui` @ `570386d`(2026-06-30)/ `crashgame-cg03r-socket` @ `5baac77` / `crashgame-cg03r-api` @ `eb7a043`。未部署公开 CDN,以仓库 HEAD 为准。
> **信源纪律**:经济/数学一手 cite 服务端 `crashgame-cg03r-socket/src/main/resources/cg03/routes.json`(下称 routes.json)与客户端 `RealSocket.ts`;mock(`CluckDashSocket`)仅当占位对照。零截图形态,徽标止于 code-derived。
> **分工**:美术/资产 → `ART-AUDIO-CG03R.md`;屏/坐标/动画时长 → `UI-GREYBOX-CG03R.html`。

## 1. 游戏概述

单人**步进式 crash**(Cluck Dash):体素小鸡横穿车流车道,每前进一格(GO)倍率沿难度表上爬,可随时 CASH OUT;踩中危险格(服务端判定)则撞车归零;走完全程触发 **Ultimate Win**(通关,倍率封顶)。特色:**金井盖 bonus(Model B 累积加成)** 与四档难度换表。

- 品类:crash-step × 横向车道;引擎 Pixi.js v8(React 壳 + Pixi 场景);设计画布 **1080×1920 竖屏**(壳层 contain 等比缩放+黑边,`main.tsx layouts{1080,1920}`)。
- 双端:客户端只演出;**每一步安全/撞车由服务端 ack 判定**(`client:game:advance` → `safe`)。
- 模式:单一模式 × 4 难度(EASY/MEDIUM/HARD/HARDCORE,`GameManager.Difficulty`)。

## 2. 回合状态机与信号

相位:`idle → betting → flying → (crashed | settled) → betting`(`GameManager` 相位机;`RealSocket`/`CluckDashSocket` 驱动同一组 NET_* 信号)。

```
betting ──PLAYER_BET_PLACE(client:game:start ack)──► flying(首格自动 GO)
flying ──PLAYER_GO(client:game:advance ack)──► safe? ──否──► crashed ──NET_ROUND_RESULT──► settled
   │                                             │是(逐格: NET_LANE_ADVANCE+NET_MULTIPLIER)
   ├──PLAYER_CASHOUT(client:game:cashout ack)──► settled(NET_MY_CASHOUT+NET_CASHOUT_DONE)
   └──走满 totalLanes(capTriggered)──► Ultimate Win → 自动兑付 → settled
settled ──hold 4000ms(普通)/10000ms(Ultimate)──► betting(NET_ROUND_BETTING)
```

- PlayState(HUD 布局态,`PlayerWallet`):`bet`(难度选择+PLAY)⇄ `cashout`(CASHOUT+GO 双钮),由 `hasBetPlaced∧flying ∨ settlementInProgress` 派生。
- 关键信号:`NET_ROUND_BETTING/FLY/CRASH/RESULT`、`NET_LANE_ADVANCE{laneIdx,totalLanes,multiplier,nextMultiplier}`、`NET_MULTIPLIER`(有效倍率)、`NET_REVEAL_BONUS{tier,delta}`、`NET_MY_CASHOUT`、`NET_BALANCE`、`NET_DIFFICULTY(_PREVIEW)`、`NET_ROUTES`、`NET_LANE_RESUME`(断线快照恢复)、`FX_WIN_BANNER_UPDATE`/`ULTIMATE_WIN_SHOWN`(演出层)。
- Ultimate 时余额刷新**延迟到演出结束**(`PlayerWallet.deferNextBalance` 等 `ULTIMATE_WIN_SHOWN`)。

## 3. 难度与数学表(一手:routes.json;RTP 目标 0.96)

全局:`default_route=EASY`,**`b_max=2.0`**(bonus 累积上限),`max_mult_warn=100.0`,**`rtp_target=0.96`**(routes.json:2-5)。

| 难度 | 格数 | 封顶倍率 x_n | γ(曲线) | bonus 分布 none/small(+0.1)/medium(+0.3)/big(+0.5) |
|---|---|---|---|---|
| EASY | 28 | 20.0 | 1.28 | 0.80 / 0.12 / 0.06 / 0.02 |
| MEDIUM | 22 | 20.0 | 1.30 | 0.75 / 0.14 / 0.08 / 0.03 |
| HARD | 18 | 25.0 | 1.33 | 0.70 / 0.16 / 0.10 / 0.04 |
| HARDCORE | 14 | 30.0 | 1.36 | 0.60 / 0.20 / 0.10 / 0.10 |

- **逐步倍率 x_k 与危险概率 p_hazard**:四难度全表见 routes.json(EASY k1..28:x_k 1.01,1.04,1.10,1.17,1.25,1.35,1.46,1.59,1.75,1.93,2.13,2.37,2.65,2.97,3.34,3.77,4.26,4.84,5.51,6.29,7.21,8.28,9.53,11.00,12.72,14.76,17.16,20.00;p_hazard 0.0515→0.1573 单调升。MEDIUM 22 步 x_k 1.02→20.00;HARD 18 步 1.04→25.00;HARDCORE 14 步 1.07→30.00,p_hazard 0.1109→0.3351)。
- 客户端 mock `CluckDashSocket.DIFFICULTY_TABLE` 与 routes.json **逐值一致**(镜像,本次逐值对账 laneMults/pHazard/bonusTiers 全等)——仅供演出联调,真值永远走服务端。
- 难度切换:betting 期 `UI_DIFFICULTY` → `NET_DIFFICULTY_PREVIEW`(预览车道表);下注后 `NET_DIFFICULTY` 锁表。

## 4. Bonus(金井盖,Model B)与有效倍率

- 每格 bonus 由服务端下发(`advance ack: bonusType/bonusMultiplier/accumulatedBonus`;分布见 §3;mock 用 `Math.random()` CDF 占位)。
- **Model B 提交时序**:到达格仅**预告**(金井盖翻牌预览);**下一次 GO 时把上一格预告提交**进累计 `cumulativeBonus`(封顶 `b_max=2.0`),同时产生新格预告(`RealSocket committedDelta` 与 mock 注释一致)。
- **有效倍率** `eff = x_k × (1 + cumulativeBonus)`(RealSocket/CluckDash 同式);倍率横幅与 CASHOUT 金额显示 eff。
- 派彩 `payout = bet × eff`(cashout ack 的 `payoutAmount` 为权威;客户端 `bet×eff` 仅展示估算)。

## 5. 结算与自动兑付

- 手动 CASHOUT:`client:game:cashout` ack → `NET_MY_CASHOUT{bet,multiplier=eff,baseMultiplier=x_k,cashout=payout,isUltimate}` + `NET_BALANCE(balanceAfterPayout 权威)`。
- **Ultimate Win**:走满 totalLanes(ack `capTriggered`)→ 自动兑付;过场演出后 settle hold 10s。
- **断线自动兑付**:flying 中断线 → 15s 倒数(`AUTO_CASHOUT_COUNTDOWN_S=15`,每 1000ms tick);服务端 `enginee/DisconnectCashoutScheduler.java` 同步保障。
- **闲置**:3 分钟无操作(`IDLE_TIMEOUT_MS=180000`)→ 告警+15s 倒数自动兑付+`NET_SESSION_EXPIRED`。
- 结算 hold:普通 4000ms / Ultimate 10000ms(`SETTLE_DURATION_MS`,双端同值)后回 betting。

## 6. 输入锁与节流

- **GO 节流 600ms**(`GO_THROTTLE_MS=600` = HOP_DELAY 0.2s + HOP_DURATION 0.4s,与视图 `LaneTile` 常量互证);HUD 双钮另有 `HOP_LOCK_S=0.65` 软锁(alpha 0.6)。
- CASHOUT 单发门(`cashoutPending`):等待 ack 期间 `NET_CASHOUT_PENDING`,按钮 `PENDING_ALPHA=0.5`;失败 `NET_CASHOUT_FAIL` 恢复。
- PLAY 点击 = `ui:bet:place` + 首格 `ui:go` 连发(`MyBetPanel`);下注后注额输入与快选行锁定(tint 0xDDDDDD α0.85)。

## 7. 网络与断线状态机

- 传输:socket.io(仅 websocket)+ **protobuf over base64**;`baseUrl=indexConfig.serverUrls[0]`,`path=/game/cg03r-socket/socket.io/`;query `access_token/platform/game_id`。
- 重连:自动重连 ≤10 次,退避 1000→5000ms;成功 → `client:snapshot` **快照恢复**(飞行中 `NET_LANE_RESUME` 无动画重建盘面)或回 betting;失败 → `NET_RECONNECT_FAILED`(提示重载,`RECONNECT_RELOAD_TIMEOUT_MS=10000`)。
- ACK 超时 8000ms → 告警 toast;`server:alert` 服务端已本地化文本直显(en/zh-CN/zh-TW 字段);SSO `sso-disconnected` 抑制倒数直接踢出;`server:game:expired` → 会话过期。
- 首连序列:`client:routes` → `client:snapshot` → `client:balance` → `GAME_READY`。

## 8. 协议与后端接口

| 通道 | 事件/端点 | 说明 |
|---|---|---|
| WS C→S | `client:game:start{betAmount,currency,difficulty}` | 下注开局(ack:sessionId/balanceAfterBet/laneMultipliers) |
| WS C→S | `client:game:advance` | 步进(ack:safe/stepNo/currentMultiplier/nextMultiplier/bonus*/accumulatedBonus/capTriggered/balanceAfterPayout) |
| WS C→S | `client:game:cashout` | 兑付(ack:payoutAmount/finalMultiplier/cumulativeBonus/balanceAfterPayout) |
| WS C→S | `client:snapshot` / `client:routes` / `client:balance` | 快照恢复 / 难度表 / 余额 |
| WS S→C | `server:balance:changed` / `server:alert` / `server:game:expired` | 推送 |
| HTTP | `GET /bet/config` | bet 档位+默认注(**UI 快选行要求恰 5 档**,否则保留 fallback) |
| HTTP | `GET /bet/summary?from=` / `GET /bet/history?from=&nextId=` | 统计/历史(窗口 1/3/7 天;nextId 分页;`PROCESSING`=进行中) |

- 历史条目派生:`finalMultiplier = cashOutAt × (1+cumulativeBonus)`;crashed 行给 `crashPoint`。
- 公平性:服务端含 `SeedRevealService`(种子揭示,provably-fair 机制存在;算法 server 权威)。

## 9. 投注与钱包

- bet 档位/默认注:服务端 `/bet/config` 下发(数量与值按运营/币种配置);**客户端 fallback(占位勿作真值)**:快选 `[0.1,0.5,1,5,10]`、默认注 `1.00`、mock 初始余额 100。
- 币种:icon 按 `currencyIconAlias(code)` 解析(USD/CNY/PHP 专图,其余通用);符号 `'$'` 为占位,实际随 verify 会话。
- 余额权威=服务端(`balanceAfterBet/balanceAfterPayout/BalanceChanged`);客户端乐观显示后以 ack 校正。

## 10. mock-vs-real 陷阱(必读)

| 项 | mock(CluckDashSocket/CrashApiDummy) | real |
|---|---|---|
| 撞车 | **hazard 判定被禁用**(`if(false&&…)`,永不撞) | 服务端 `safe=false` 判定 |
| 余额/注 | INITIAL_BALANCE=100、快选 [0.1,0.5,1,5,10] | verify 会话+/bet/config |
| bonus 抽取 | `Math.random()` CDF 占位 | 服务端(SeedReveal 机制) |
| 历史 | xorshift 种子假数据 150 条 | /bet/history |
| 难度表 | 硬编码镜像(本次对账=routes.json) | `client:routes`/`NET_DIFFICULTY` |

## 11. 时序汇总(玩法侧;动画时长唯一权威在灰盒注释面板)

hop=0.2s delay+0.4s 滚动;金盖翻面 0.55s;撞车冲击 0.65s;GO 节流 600ms;settle 4s/10s;断线倒数 15s×1s;闲置 3min;ACK 8s;重连退避 1–5s×10;加载进度分段 0.10/0.80/0.90/1.00(bootstrap 管线)。

## 12. 交叉引用

- 资产/风格/玩法→美术适配 → `ART-AUDIO-CG03R.md`;屏结构/坐标/徽标/越界分诊 → `UI-GREYBOX-CG03R.html`;机器全量 → `elements-CG03R.json`(ui_elements+assets 双段)。旧版三件套已归档 `_opus-legacy/`(仅历史,不作数据源)。
