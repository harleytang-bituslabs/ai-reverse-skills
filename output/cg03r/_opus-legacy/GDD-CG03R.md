---
type: prd-split
audience: game-logic (frontend + backend code agents)
product_code: cg03r
product_name: "Cluck Dash / 小鸡狂奔"
genre: crash / step-progression (real-money)
output_profile: obsidian_md
status: reverse-engineered
triad: ART-AUDIO-CG03R.md (资产) · GDD-CG03R.md (本文档·玩法/状态) · UI-GREYBOX-CG03R.html (布局)
language: zh-CN
created: 2026-06-22
purpose: agent 训练素材 —— 喂回写前后端代码的 agent 即可复现 cg03r 玩法逻辑与状态机
---

# cg03r「Cluck Dash / 小鸡狂奔」— Game Design Document（逆向）

> **分工**：本文档只管**游戏规则/玩法循环/状态机/经济/数学/网络时序**。美术见 [ART-AUDIO-CG03R.md](ART-AUDIO-CG03R.md)；界面布局/动画时长见 [UI-GREYBOX-CG03R.html](UI-GREYBOX-CG03R.html)（动画"长相"以 HTML 为权威）。
>
> **数据来源**：`src/.../GameManager / CrashGameplayManager / PlayerWallet / CluckDashSocket / RealSocket`。难度梯/碰撞率/bonus 取自 `CluckDashSocket`(dev mock，注释"镜像服务端 routes.json")。
>
> **关系**：cg03r 是原版，cg03a「Jeepney Glide」reskin 自它 —— **数学框架与状态机一致**（难度梯/碰撞率完全相同），仅题材/场景/美术不同。

---

## 1. Summary
**逐车道递进 crash**：体素小鸡**横向**逐车道前进，每跳一条车道（落到一个井盖）赔率台阶上升、本道有被车撞的概率；玩家随时 **CASHOUT 套现** 或 **GO 继续**。到终点车道触发 Super Win 自动结算。
```
下注(额+难度) → PLACE BET → 飞行: GO 跳一道(赔率↑/碰撞 roll) → [bonus 翻牌] → CASHOUT or GO
  ├ CASHOUT → bet × 当前赔率 × (1+累计bonus)
  ├ 撞车 → 归零
  └ 终点车道(laneIdx≥totalLanes) → Super Win 自动结算(isUltimate)
```

## 2. 回合状态机（`GameManager`）
```
idle → betting(NET_ROUND_BETTING) → flying(NET_ROUND_FLY) → crashed(NET_ROUND_CRASH) | settled(NET_ROUND_RESULT)
```
- 纯数据层。**下注态 PlayState**（`PlayerWallet`）：`bet`(无在飞回合) ↔ `cashout`(已下注+飞行/结算中) —— 驱动 HUD 控件互换（见 HTML）。
- 关键信号：
  - 进站：`NET_LANE_ADVANCE{laneIdx,totalLanes,multiplier,nextMultiplier}`、`NET_LANE_RESUME{laneIdx,totalLanes,multiplier,cumulativeBonus,bonuses[]}`（重连续飞）
  - bonus：`NET_REVEAL_BONUS{tier:'small'|'medium'|'big',delta,multiplier}`
  - 结算：`NET_MY_CASHOUT{bet,multiplier,baseMultiplier,cashout,isUltimate}`、`NET_ROUND_CRASH(m)`、`NET_ROUND_RESULT(HistoryEntry)`
  - 难度：`NET_DIFFICULTY{mode,totalLanes,laneMultipliers[]}`、`NET_DIFFICULTY_PREVIEW(number[])`、`NET_ROUTES{EASY,MEDIUM,HARD,HARDCORE}`
  - 玩家→网络：`PLAYER_BET_PLACE{amount,difficulty}` / `PLAYER_GO` / `PLAYER_CASHOUT`；UI：`ui:bet:place/lower/raise/quick`、`ui:go`、`ui:cashout`、`ui:difficulty`
  - 落地回执：`HOP_GO_PENDING → HOP_RESOLVED`（hop 落定再启用按钮，多倍率延迟到落定应用）
  - 结算回执：`NET_CASHOUT_PENDING/FAIL`、`NET_CASHOUT_DONE`、`ULTIMATE_WIN_SHOWN`（大奖动画显毕才到账）

## 3. 玩法核心：逐车道 hop（横向）
- `laneIdx=0`=出发前；GO 推进 `1..totalLanes`，每 hop=跳一条车道、落到一个井盖。
- **赔率台阶**：车道 k 赔率 = `laneMults[k-1]`（§4）。飞行态双按钮各带值：**套现(CASHOUT)** 显当前派彩 `$=bet×mult×(1+bonus)`、**继续(GO)** 显**下一道**倍率 `<next>x`(子行)；小鸡下方"当前倍率横幅"显当前 x_k；前方井盖显预览梯。
- **碰撞**：每 GO 在目标车道 roll `Math.random()<pHazard[laneIdx]` → 被车撞归零；否则前进。（mock 硬编 collisions=false 永不撞，供 dev/美术；线上 RealSocket 服务端 `AdvanceRet.safe` 权威。）
- **hop 节流**：`GO_THROTTLE_MS=600`（=HOP_DELAY 0.2 + HOP_DURATION 0.4 + buffer）；`hopInFlight` 防重复 GO。

## 4. 难度系统（4 路线；与 cg03a 同梯）
UI 文案 EASY/MEDIUM/HARD/HARDCORE。难度越高站数越少、赔率梯越陡、碰撞率越高、bonus 越少。

| 难度 | totalLanes | laneMults（道 1→终点） | 终点 |
|---|--:|---|--:|
| **EASY** | 28 | 1.01,1.04,1.10,1.17,1.25,1.35,1.46,1.59,1.75,1.93,2.13,2.37,2.65,2.97,3.34,3.77,4.26,4.84,5.51,6.29,7.21,8.28,9.53,11.00,12.72,14.76,17.16,**20.00** | 20x |
| **MEDIUM** | 22 | 1.02,1.07,1.15,1.25,1.37,1.52,1.70,1.92,2.19,2.51,2.90,3.37,3.94,4.63,5.47,6.49,7.75,9.28,11.17,13.51,16.40,**20.00** | 20x |
| **HARD** | 18 | 1.04,1.11,1.22,1.37,1.57,1.82,2.15,2.56,3.08,3.76,4.62,5.74,7.20,9.09,11.58,14.85,19.20,**25.00** | 25x |
| **HARDCORE** | 14 | 1.07,1.18,1.35,1.60,1.95,2.45,3.15,4.12,5.51,7.48,10.35,14.53,20.73,**30.00** | 30x |

**碰撞率 pHazard（每道，递增）**：
- EASY: 0.0515,0.0727,0.0836,0.0915,0.0979,0.1033,0.1079,0.1121,0.1159,0.1193,0.1225,0.1254,0.1282,0.1308,0.1333,0.1356,0.1378,0.1399,0.1420,0.1439,0.1458,0.1476,0.1493,0.1510,0.1527,0.1542,0.1558,0.1573
- MEDIUM: 0.0657,0.0945,0.1096,0.1206,0.1294,0.1369,0.1434,0.1492,0.1544,0.1592,0.1637,0.1678,0.1717,0.1753,0.1787,0.1820,0.1851,0.1881,0.1909,0.1936,0.1962,0.1988
- HARD: 0.0821,0.1217,0.1427,0.1582,0.1707,0.1813,0.1905,0.1987,0.2062,0.2130,0.2193,0.2252,0.2307,0.2359,0.2408,0.2454,0.2498,0.2540
- HARDCORE: 0.1109,0.1683,0.1991,0.2219,0.2402,0.2557,0.2692,0.2813,0.2921,0.3020,0.3112,0.3197,0.3276,0.3351

## 5. 乘客 bonus 经济（路口翻牌）
- **触发**：每安全前进一道，提交上道预览的 bonus，并为当前道抽新预览（`NET_REVEAL_BONUS`）。
- **档位 delta**（实测 `CluckDashSocket` bonusTiers，加到累计 bonus）：**small +0.1 / medium +0.3 / big +0.5**；累计 **cap B_MAX=2.0**（最高 +200%）。
- **应用**：有效赔率 = `raw_xk × (1 + 累计bonus)`；派彩 = `bet × 有效赔率`。
- **概率（CDF，按难度，源 routes.json）**：

| 难度 | none | small(+0.1) | medium(+0.3) | big(+0.5) |
|---|--:|--:|--:|--:|
| EASY | 80% | 12% | 6% | 2% |
| MEDIUM | 75% | 14% | 8% | 3% |
| HARD | 70% | 16% | 10% | 4% |
| HARDCORE | 60% | 20% | 10% | 10% |

- RealSocket：服务端权威下发 `bonus_at_step + accumulatedBonus`；mock：客户端 CDF walk（Math.random，匹配 Cg03StepEngine）。
- UI：本道 `+N%`(小鸡头顶 count-up，small #F0F8FF 56px/medium #FFE680 72px/big #FFD24A 96px) → 飞入右上累计 bonus 横幅(292×110)。

## 6. 派彩 / 胜负
- **CASHOUT**：`cashout = bet × multiplier × (1+cumBonus)`（服务端 `NET_MY_CASHOUT` 权威，带 `baseMultiplier`=未含 bonus；前端先显 base 再 count-up 到全额 `FX_WIN_BANNER_UPDATE` 0.4s）。
- **撞车**：碰撞命中 → 归零，回 betting。`NET_ROUND_CRASH` → 红闪 + 车撞小鸡 + die 动画。
- **Ultimate / Super Win**：`laneIdx≥totalLanes` 自动 cashout，`isUltimate=true` → Grand Prize 文字(顶)+ YOU WIN 横幅(降至小鸡下方)+ 烟花/金币雨/彩带 + 升旗。**余额到账延后**到 `ULTIMATE_WIN_SHOWN`。

## 7. 投注配置（`PlayerWallet`）
- 货币 `$`（**计价 USDT**，Guide 文案"0.10–100 USDT"），**多币种**图标 USD/CNY/PHP 顶栏切换。
- 快捷投注：代码 fallback `BET_QUICK_VALUES=[0.1,0.5,1,5,10]`（5 键）；**真机部署经 `NET_BET_CONFIG` 覆盖为 [1,2,5,10]（4 键，截图实测）**——复现以部署 config 为准。MIN/MAX 步进吸附端点；默认 1.00；不可负担锁 PLAY。初始余额 mock=100。
- **设置-画质**：Graphics Quality 三档 Low/Med/High（`QualityManager` 预设：antialias/enableFilters/maxFPS 0/60/30；默认 High），UI 在设置页（见 HTML set-setting）。

## 8. 输入锁
- hop 期 `HOP_GO_PENDING`→禁 GO/CASHOUT，`HOP_RESOLVED` 落定再启用并应用延迟倍率；GO/CASHOUT 各 `HOP_LOCK_S=0.65s` 节流；`roundOver` 在 ultimate 期阻止重启用。难度器 disabled→alpha0.5+强制收起。

## 9. 断线 / idle / 错误状态机
- **idle**：`IDLE_TIMEOUT_MS=180000`(3min) → 飞行中触发 `NET_RECONNECTING` + **15s 自动 cashout 倒计时**(`DISCONNECT_CASHOUT_S=15`，`NET_RECONNECT_TICK` 每 1s)。
- **重连**：reconnecting→常驻 Toast；reconnected→3s Toast；failed→Warning+reload。socket.io `MAX_RECONNECT_ATTEMPTS=10`，delay 1~5s；手动重连看门狗 `RECONNECT_RELOAD_TIMEOUT_MS=10000` 超时整页 reload。`ACK_TIMEOUT_MS=8000`。
- 异常态（`clientExceptionRegistry`）：unsupported-platform / maintenance / log-expired / banned-player / unsupported-currency。

## 10. 网络 / 协议层
- `CrashGameplayManager`：`_devBypass=true`→`CluckDashSocket`(离线 mock)；否则 `RealSocket`(socket.io-client + protobuf；BigDecimal-as-string、int64 via Long 无损)。两者发同套 `NET_*`。`GAME_READY`：mock 同步 / real 握手后。
- RPC：`client:game:{start,advance,cashout,routes,snapshot}`（ACK + 8s timeout）；快照恢复 `requestSnapshot()`→`NET_LANE_RESUME`(laneIdx>0 保留 step bonuses)。

## 11. 时序（节奏；动画长相以 HTML 为权威）
- hop 0.2(delay)+0.4(duration)≈0.6s；结算 settle **4s 普通 / 10s ultimate**；cinematic hop 1.6s。
- 表现信号→音效（见 ADD §7）：起跳→`sfx_chick_jump`、落定→`sfx_chick_land`、撞车→`sfx_car_pass_by1/2`(50%随机)、结算→`sfx_cashout`/`sfx_chick_win`。BGM `bgm_normal` 4min loop（`ENTER_GAME` 后播），tag `scene:main`。

## 12. Non-Goals
- 不做每难度换皮（4 难度共用美术，仅数学不同）；无老虎机；无横版/Auto-spin 独立面板。
- 美术/动画长相不在此（归 ADD/HTML）。

## 13. Sources
- `src/game/project/scenes/MainScene/{GameManager,CrashGameplayManager,PlayerWallet,MainScene}.ts`
- `src/game/project/network/{CluckDashSocket,RealSocket,HistoryEntry}.ts`、`util/betConfig.ts`
- `src/configs/clientExceptionRegistry.ts`

---

**GDD 结束（逆向版）。资产见 ART-AUDIO-CG03R.md；布局见 UI-GREYBOX-CG03R.html。**
