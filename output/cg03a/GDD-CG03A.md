---
type: prd-split
audience: game-logic (frontend + backend code agents)
product_code: cg03a
product_name: "Jeepney Glide"
genre: crash / step-progression (real-money)
output_profile: obsidian_md
status: reverse-engineered
triad: ART-AUDIO-CG03A.md (资产) · GDD-CG03A.md (本文档·玩法/状态/规则) · UI-GREYBOX-CG03A.html (布局)
language: zh-CN
created: 2026-06-22
purpose: agent 训练素材 —— 喂回写前后端代码的 agent 即可复现 cg03a 的玩法逻辑与状态机
---

# cg03a「Jeepney Glide」— Game Design Document（逆向）

> **本文档定位 / 分工**：三件套之一，只管**游戏规则、玩法循环、状态机、经济/数学、网络时序**——给写前后端代码的 agent。**美术资产**见 [ART-AUDIO-CG03A.md](ART-AUDIO-CG03A.md)；**界面布局/动画时长**见 [UI-GREYBOX-CG03A.html](UI-GREYBOX-CG03A.html)。本文档不含美术细节，动画"长相/时长"只在节奏层引用、以 HTML 为权威。
>
> **数据来源**：`crashgame-cg03a-ui/cg03a/src` 源码穷尽抽取（`GameManager / CrashGameplayManager / PlayerWallet / CluckDashSocket / RealSocket`）。其中难度梯/碰撞率/bonus 概率取自 `CluckDashSocket`（dev-bypass mock，注释标明"镜像服务端"）；**真机截图已验证各难度 laneMults[0]/[1] 与 mock 完全一致**（easy 1.01/1.04、medium 1.02/1.07、hard 1.04/1.11、hardcore 1.07/1.18），故 mock 梯可作复现参考；线上真值由服务端下发。

---

## 1. Summary 摘要

**Jeepney Glide** 是**逐站递进式 crash**真金游戏（非老虎机）：玩家驾吉普尼沿一条公路逐站前进，每前进一站赔率台阶上升、但本站有碰撞（撞车归零）概率；玩家随时可 **CASHOUT 落袋**或 **GO 继续**。途中乘客上车叠加 bonus 倍率。到达终点站触发 Grand Prize 自动结算。

**核心循环**：
```
下注(选额+选难度路线) → PLAY 下注开局
  └→ 飞行循环: GO 进一站(赔率↑/碰撞 roll) → [可能乘客上车叠 bonus] → 抉择 CASHOUT or GO
       ├ CASHOUT → 派彩 = bet × 当前赔率 × (1+累计bonus)
       ├ 撞车(碰撞 roll 命中) → 归零，本局结束
       └ 到达终点站 → Grand Prize 自动 cashout(ultimate)
```

## 2. 回合状态机（`GameManager`）

```
idle → betting(NET_ROUND_BETTING) → flying(NET_ROUND_FLY) → crashed(NET_ROUND_CRASH) | settled(NET_ROUND_RESULT)
```
- 纯数据层，无视图引用；`currentMultiplier` 由 `NET_MULTIPLIER` 推送跟踪；`phaseValue`/`multiplierValue` 可读。
- **下注态 PlayState（`PlayerWallet`）**：`bet`（无在飞回合）↔ `cashout`（已下注、飞行中）。驱动 HUD 控件互换（见 HTML）。
- 关键网络信号：
  - 回合：`NET_ROUND_BETTING / NET_ROUND_FLY / NET_ROUND_CRASH(m=crash 倍率) / NET_ROUND_RESULT`
  - 进站：`NET_LANE_ADVANCE{laneIdx,totalLanes,multiplier,accumulatedBonus}`、`NET_LANE_RESUME`（重连续飞）
  - bonus：`NET_REVEAL_BONUS{tier,delta,multiplier}`
  - 结算：`NET_MY_CASHOUT{bet,multiplier,baseMultiplier,cashout,isUltimate}`
  - 难度：`NET_DIFFICULTY{mode,totalLanes,laneMultipliers}`、`NET_DIFFICULTY_PREVIEW(laneMultipliers[])`（下注态预览赔率梯）
  - 玩家→网络：`PLAYER_BET_CONFIG_REQ`、`ui:bet:place`、`ui:go`、`ui:cashout`、`ui:bet:lower/raise/quick`
  - 落地回执：`HOP_GO_PENDING → HOP_RESOLVED`（hop 落定再启用按钮）、`NET_CASHOUT_PENDING/FAIL`

## 3. 玩法核心：逐站 hop

- **lane/station**：`laneIdx=0` = 出发前（depot，station 0）；GO 推进 `1..totalLanes`。每 hop = 前进一站。
- **赔率台阶**：站 k 的赔率 = `laneMults[k-1]`（见 §4 表）。飞行态双按钮各带值：**套现(CASHOUT)** 显当前派彩 `$=bet×mult×(1+bonus)`、**继续(GO)** 显**下一站**倍率 `<next>x`；沿途站牌显各站预览赔率梯（布局见 HTML）。
- **碰撞**：每次 GO 在目标站 roll `Math.random() < pHazard[laneIdx]` → 撞车归零；否则前进。（mock 有 `ALWAYS_PASS=true` 仅供美术/dev 永不撞。）
- **每 middle tile = 4 站**（站距 225px，见 HTML 画廊 B）；`startHops` = easy 0 / 其余 2；middle 数 = `(totalLanes - startHops)/4`。

## 4. 难度系统（4 路线）

UI 文案：简单/中等/困难/极难（`gameplay.difficulty.*`）。设计代号曾为 Cubao Express/EDSA Rush/Manila Bay Drive/Quiapo Hardcore（见 ADD）。难度越高站数越少、赔率梯越陡、碰撞率越高。

| 难度 | totalLanes | laneMults（站 1→终点） | 终点赔率 |
|---|--:|---|--:|
| **easy 简单** | 28 | 1.01, 1.04, 1.10, 1.17, 1.25, 1.35, 1.46, 1.59, 1.75, 1.93, 2.13, 2.37, 2.65, 2.97, 3.34, 3.77, 4.26, 4.84, 5.51, 6.29, 7.21, 8.28, 9.53, 11.00, 12.72, 14.76, 17.16, **20.00** | 20x |
| **medium 中等** | 22 | 1.02, 1.07, 1.15, 1.25, 1.37, 1.52, 1.70, 1.92, 2.19, 2.51, 2.90, 3.37, 3.94, 4.63, 5.47, 6.49, 7.75, 9.28, 11.17, 13.51, 16.40, **20.00** | 20x |
| **hard 困难** | 18 | 1.04, 1.11, 1.22, 1.37, 1.57, 1.82, 2.15, 2.56, 3.08, 3.76, 4.62, 5.74, 7.20, 9.09, 11.58, 14.85, 19.20, **25.00** | 25x |
| **hardcore 极难** | 14 | 1.07, 1.18, 1.35, 1.60, 1.95, 2.45, 3.15, 4.12, 5.51, 7.48, 10.35, 14.53, 20.73, **30.00** | 30x |

> 路面 = `start.jpg` + `middle.jpg`(单图 TilingSprite **无缝重复**铺满) + `end.jpg`（每难度 3 图，站高=900/4=225px）。**middle tile 重复数 = (totalLanes − startHops)/4**（startHops：easy 0 / 其余 2）→ **easy 7 / medium 5 / hard 4 / hardcore 3**（源码 `GameplayFlyingPanel.ensureRoadCoverage` L806-807 实证；与 §3、HTML 画廊 B 一致）。注意：middle **图**只有 1 张(TilingSprite)，但每难度的**重复次数是确定的**(非任意)。场景资产见 [ART-AUDIO-CG03A.md](ART-AUDIO-CG03A.md) §5 / 长卷见 [UI-GREYBOX-CG03A.html](UI-GREYBOX-CG03A.html) 画廊 B。

**碰撞率 pHazard（每站，递增）** —— 完整表（mock，镜像服务端）：
- easy: 0.0515, 0.0727, 0.0836, 0.0915, 0.0979, 0.1033, 0.1079, 0.1121, 0.1159, 0.1193, 0.1225, 0.1254, 0.1282, 0.1308, 0.1333, 0.1356, 0.1378, 0.1399, 0.1420, 0.1439, 0.1458, 0.1476, 0.1493, 0.1510, 0.1527, 0.1542, 0.1558, 0.1573
- medium: 0.0657, 0.0945, 0.1096, 0.1206, 0.1294, 0.1369, 0.1434, 0.1492, 0.1544, 0.1592, 0.1637, 0.1678, 0.1717, 0.1753, 0.1787, 0.1820, 0.1851, 0.1881, 0.1909, 0.1936, 0.1962, 0.1988
- hard: 0.0821, 0.1217, 0.1427, 0.1582, 0.1707, 0.1813, 0.1905, 0.1987, 0.2062, 0.2130, 0.2193, 0.2252, 0.2307, 0.2359, 0.2408, 0.2454, 0.2498, 0.2540
- hardcore: 0.1109, 0.1683, 0.1991, 0.2219, 0.2402, 0.2557, 0.2692, 0.2813, 0.2921, 0.3020, 0.3112, 0.3197, 0.3276, 0.3351

> 难度切换在下注态即时生效（`UI_DIFFICULTY`→road 预览换皮 + `NET_DIFFICULTY_PREVIEW` 刷站牌赔率）；视觉黑幕淡切见 HTML。

## 5. 乘客 bonus 经济

- **触发**：每进一站 roll bonus（`NET_REVEAL_BONUS`）。mock 概率：empty 70% / small 18% / medium 9% / big ~3%。
- **档位 delta**（加到累计 bonus，cap B_MAX=2.0）：⚠️ **dev mock 与真服务端不同，复现用真服务端值**。
  - **真服务端 ≈ small +0.1 / medium +0.3 / big +0.5**（复现以此为准）。依据：①真机截图累计 **+30/40/50/80%**、注单 `@4.62x(+40%)`/`@9.09x(+80%)`/`@3.34x(+50%)` 与 {10,30,50} 之和**完美吻合**（+40=10+30、+80=30+50、+30=30、+50=50），与 mock 的 {20,50,150} **对不上**；②与**原版 cg03r 源码确认值**（small+0.1/med+0.3/big+0.5）一致。
  - dev mock(`CluckDashSocket`) 占位为 small +0.20 / medium +0.50 / big +1.50（probs 70/18/9/3，源码实测，**仅离线 dev 用，勿作真值**）。
  - UI 显示：本站 `+N%`(头顶 count-up) + 累计 `BONUS +NN%`(右下面板)。
- **应用**：派彩 = `bet × multiplier × (1 + 累计bonus)`。
- **Model B（延迟上车）**：本站抽到的乘客**不立即结算**，停在站台；玩家**下次 GO 时**才播登车 cut-in 并提交到累计 bonus（`accumulatedBonus` 由服务端权威下发，前端同步）。
- **角色映射**（`CHARA_BY_DIFFICULTY`，bonus 档→spine 角色，资产细节见 ADD §6.2）：

| 难度 | small(+0.1) | medium(+0.3) | big(+0.5) |
|---|---|---|---|
| easy / medium | chara1 | chara2 | chara3 |
| hard | chara4 | chara5 | chara6 |
| hardcore | chara7 | chara8 | chara9 |

- 音效：small/medium/big → `bonus_1/2/3.mp3`（见 ADD §7）。

## 6. 派彩 / 胜负

- **CASHOUT**：`cashout = bet × currentMultiplier × (1 + cumBonus)`（服务端 `NET_MY_CASHOUT` 权威，带 `baseMultiplier`=未含 bonus 值，前端先显 base 再 count-up 到含 bonus 全额）。
- **撞车**：碰撞 roll 命中 → 本局归零，回 betting。
- **Ultimate（终点大奖）**：`laneIdx >= totalLanes` 自动 cashout，`isUltimate=true`；演出为终点 Grand Prize（无横幅纯文字 + 烟花，见 HTML）。**余额到账延后**到 `ULTIMATE_WIN_SHOWN`（Grand Prize 动画结束）。

## 7. 投注配置（`PlayerWallet`）

- 货币 `$`；`BET_MIN=0.10`、`BET_MAX=100.0`、`BET_STEP=0.10`。
- 快捷预设：硬编码兜底 `BET_QUICK_VALUES=[0.1, 0.5, 1, 5, 10]`（5 档），**服务端经 `NET_BET_CONFIG` 覆盖**；MyBetPanel 按 `count` 自适应按钮宽度（`QB_FOOTPRINT_W=965`，5 档→185px/个），**支持 4/5/6 档**（非固定 5；真机截图实测为 5 档 [0.1,0.5,1,5,10]）。〔更正：原"必须恰好 5 个"有误〕
- MIN/MAX 步进；不可负担时 PLAY 锁定（前端余额校验 `WALLET_BET_AFFORDABLE`）。

## 8. 输入锁（防连点 / 防越权）

- **animLock**（瞬态）：hop / 登车 cut-in 期间，由 `NET_INPUT_LOCK_UNTIL(untilMs)` 定时解锁（`performance.now()` 截止）。
- **phaseLock**（持续）：crash / settle 期间锁，至 `NET_ROUND_BETTING` 清。
- `hopInFlight` 标志防重复 GO；GO/CASHOUT 点击各自 0.65s 节流（`HOP_LOCK_S`）。
- 聚合信号 `WALLET_HUD_INPUT_LOCKED` 仅在状态翻转时发，禁用 PLAY/GO/CASHOUT + 难度器(alpha0.6)。

## 9. 断线 / idle / 错误状态机（`MainScene` + socket）

- **idle 超时**：`IDLE_TIMEOUT_MS=180000`（3 分，镜像服务端）→ `NET_RECONNECTING` + **15s 断线自动 cashout 倒计时**（`DISCONNECT_CASHOUT_S=15`，Warning 弹窗内 `NET_RECONNECT_TICK` 原地刷新；归 0 自动结算并转"已断线"文案）。
- **重连**：`NET_RECONNECTING`→常驻 Toast"重连中"；`NET_RECONNECTED`→3s Toast；`NET_RECONNECT_FAILED`→Warning + reload 按钮。手动重连看门狗 `RECONNECT_RELOAD_TIMEOUT_MS=10000`，超时整页 reload。
- **会话过期 / 服务端 alert**：type1→Toast，type0→Warning（标题用 `popup.warning.title.default`）。
- **客户端异常态**（`clientExceptionRegistry`，渲染异常屏）：`unsupported-platform / maintenance / log-expired(token 失效) / banned-player / unsupported-currency`。

## 10. 网络 / 协议层

- **`CrashGameplayManager`** 组合根：`gameConfig._devBypass=true` → `CluckDashSocket`（离线 mock，单机模拟，供美术/dev）；否则 `RealSocket`（protobuf + socket.io-client）。两者都发同一套 `NET_*` 信号 → 表现层与数据层解耦。
- `GAME_READY`：mock 同步发；real 握手后发。`PlayerWallet.sync()` 连接后刷初值。
- socket 路径（`public/config/index.config.js`）：`socketPath:/game/cg03a-socket/socket.io/`、`apiPath:/game/cg03a-api/v1/api`。
- REST：`/bet/summary` + `/bet/history`（History 页），`CrashApiClient`（真）/`CrashApiDummy`（假）。

## 11. 时序（节奏；动画"长相"以 HTML 为权威）

- 单站 hop **1.5s**（sine.inOut）。结算 settle 延时 **4s 普通 / 9.5s ultimate**（=登车~2.2 + 末 hop~1.5 + 停 0.3 + 终点 drive~1.5 + 保持~3）。
- 表现信号→音效（见 ADD §7）：`ANIM_DEPART`(发车)→insert_coin、`ANIM_HOP_START`→drive、`ANIM_CRASH_IMPACT`→car_crashed、`ANIM_CASHOUT_SHOW`→win、`ANIM_BONUS_CUTIN(tier)`→bonus_1/2/3。BGM 在 `ENTER_GAME` 后播（autoplay 闸门），channel `bgm`/`sfx` tag `scene:main`，loop SFX 音量 0.4。

## 12. Non-Goals（玩法不做）

- 不做多人/排行（单人逐站 crash）；无老虎机转轴/符号/paylines。
- 不做横版玩法；不做自动连开(Auto-spin) 独立面板（仅本逐站循环）。
- 美术/动画的具体长相不在此（归 ADD/HTML）。

## 13. Sources 信源
- `src/game/project/scenes/MainScene/{GameManager,CrashGameplayManager,PlayerWallet,MainScene}.ts`
- `src/game/project/network/{CluckDashSocket,RealSocket}.ts`（难度表/碰撞率/bonus 概率/idle/结算时序）
- `src/game/project/api/{CrashApiClient,CrashApiDummy}.ts`、`public/config/index.config.js`
- `src/configs/clientExceptionRegistry.ts`、`src/assets/localizations/*`
- 真机截图（4 难度下注态）验证 laneMults[0]/[1]

---

**GDD 结束（逆向版）。资产见 ART-AUDIO-CG03A.md；界面布局/动画见 UI-GREYBOX-CG03A.html。**
