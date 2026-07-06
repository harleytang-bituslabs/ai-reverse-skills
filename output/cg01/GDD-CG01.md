# GAME DESIGN — cg01「Crash Game / 足球 Soccer Crash」

> **本文回答**：什么游戏、什么规则、什么状态流转、经济模型。给写前后端代码的 agent。
> **不回答**：资产长相/规格/音频（见 [ART-AUDIO-CG01.md](ART-AUDIO-CG01.md)）、每屏控件布局与动画时序（见 [UI-GREYBOX-CG01.html](UI-GREYBOX-CG01.html)，动画时长以 HTML 为权威）。
> **来源**：`~/harley/cg01/crashgame-cg01-ui/cg01` 全量代码抽取。**经济/曲线为服务端权威**；`CrashGameplayManager` 按 `_devBypass` 选 `DummySocket`(mock 占位) vs 真 `ProtoSocket`。标 mock 处为离线占位、**勿作线上真值**。

---

## 1. 概要

| 项 | 值 |
|---|---|
| 品类 | **多人连续曲线 crash（Aviator 类）**，足球题材 |
| 主体 | 足球被踢飞升空，倍率连续上涨；被拦截（crash）即结束 |
| 玩家面 | 同房间多人实时：排行榜(AllPlayers) + 共享奖池(PrizePool)；**单注栏**（每玩家一局一注，非 A/B 双注） |
| 平台 | PixiJS v8，竖屏 1080×1920，Web（中台鉴权 + WebSocket protobuf） |
| 货币 | ISO 4217 → 符号（USD `$`、CNY `¥`、PHP `₱`… 全表见 ADD/§8）；源 `gameConfig.defaultSettings.currency` |
| 胜负 | crash 前 CASH OUT → 赢 `下注 × 套现倍率`；未套现 → 输全部下注 |

**核心循环**：下注（8s）→ 足球起飞、倍率持续涨（bg 随倍率拉近、火球/速度线升级）→ 在 crash 前 CASH OUT 锁定 → 否则撞毁清零 → 结算（奖杯庆祝）→ 下一局。

---

## 2. 回合状态机（服务端驱动）

`RoomState` 聚合 `NET_*` → `STATE_*`，UI 只消费 `STATE_*`。三相位（GRACE 为内部不可见）：

```
BETTING ──(倒计时结束/踢球)──▶ RUNNING ──(crash)──▶ [GRACE 1s 静默] ──▶ RESULT ──▶ BETTING(下一局)
```

| 相位 | 时长（mock，服务端定） | 客户端行为 |
|---|---|---|
| **BETTING** | `BETTING_DURATION=8000ms`（`phaseEndAtMs` 权威；fallback 8000） | 待机足球 spine(idle1/2/3) + 倒计时进度条；可下注/取消/设 AC；倒计时最后 1s 触发 kickoff 序列 |
| **RUNNING** | 不定（曲线长度服务端定） | 足球飞行，倍率连续上涨（`NET_GAME_STATUS` 每 `GAME_STATUS_TICK=100ms` 推 multiplier + isCrash）；可 CASH OUT；3 段视觉升级 |
| **GRACE** | `GRACE_DURATION=1000ms`（客户端不可见） | crash→RESULT 间静默窗口 |
| **RESULT** | `RESULT_DURATION=5000ms` | 结算：套现成功播 SettlementPanel(奖杯+金额+金币雨)；未套现仅静态展示 crash |

- **倍率曲线 100% 服务端**：客户端收 tick 值，**无生成公式**；用 `LinearValuePredictor.longWindowLinear(scaling)` 在 100ms 帧间线性外推（forward-snap，永远落后服务端、不回退）。`MAX_MULTIPLIER=1000`（mock 上限）。
- **crash 检测服务端**：`STATE_CRASH(multiplier, phase)` 边沿触发；RUNNING 时播踢球 gameover 动画，RESULT 时只静态展示。
- `HISTORY_CAP=20`：近 20 局 crash 点（最新在头），驱动顶部历史条（normal<2x 绿 / profit 2-10x 白 / super≥10x 金）。
- 重连：`NET_RECONNECTING` 冻结预测器（倍率/bg 缩放停在最后样本）→ `NET_RECONNECTED` 恢复 + 自动请求 snapshot（snapshot 原子覆盖一切）。`NetworkStaleDetector` 3s 无消息判"连而不通"；首连看门狗 30s。

---

## 3. 飞行视觉分级（倍率 → 3 段，纯 UI 升级点；`EffectLevelManager` 只升不降）

| level | 倍率区间 | bg 缩放 `calcBgScale(m)` | 火球 | 速度线 | 模糊 | spine timeScale |
|---|---|---|---|---|---|---|
| **lv1** | < 2.0x | 1.0 → 1.125 | ×(0.425,0.75) @0.7fps | α0(隐) | off | 1.0 |
| **lv2** | 2.0 – 9.99x | 1.125 → 1.5 | ×(1.7,2.0) @1fps | α1 speed0.3 ×1.1 | 0.1 | 1.0 |
| **lv3** | ≥ 10.0x | 1.5 → 2.25(@1000x) | ×(2.2,2.6) @1.5fps | α1 speed0.5 | 0.1 | 1.25 |

- `calcBgScale(m)` 分段对数（控制点 m1→1.0 / 2→1.125 / 10→1.5 / 100→1.875 / 1000→2.25），150ms lerp 平滑追，pivot 右上 (234,−269)。**这是"升空/拉近"的全部来源——非相机/视差**（见 ADD §2）。
- 升档瞬间：火焰爆裂 + 镜头震动(200ms) + spine timeScale 提升。
- ⚠️ 阈值 2x/10x 仅视觉；倍率本身连续、服务端定。

---

## 4. 下注经济（PlayerWallet，ack-only 单注栏）

```
DEFAULT_BET_LIST = [0.50, 1.00]   ← 硬编码兜底；真值由 GET /bet/config 下发 {defaultBet, betList[], currencyType, maxPayout}
AutoCashout 输入范围 [1.01, 1000]x，默认 2.00x，最多 2 位小数（>1 才有意义）
货币默认 'USD'/'$'，由 gameConfig 注入
```

- **单注栏**：每玩家一局一注（无 A/B 双注、无 quick-bet 行）。BetSwitcher 用 ±(lower/raise) 在 betList 间切换注额；MoneyContainer ×2 显示余额 + 总注。
- **ack-only 模型**：用户点击 → `pending`（按钮 α0.5 禁点）→ 服务端 `NET_*` ack / snapshot / phase 边沿确认状态。`_betId`(bigint|null) 为权威，`hasBet = _betId!==null`。
- **下注流程**：BETTING 内点 BET（`UI_BET_PLACE`）→ pending → `NET_BET_PLACED` 确认 → 按钮转 cancel；可 cancel 撤回。
- **钱包校验**：`isWalletValid=false`（支付失败）→ 该注不作数、清零 hasBet。

### 套现（Cashout）
- 手动：RUNNING 内点 CASHOUT（`UI_CASHOUT`）→ pending → `NET_MY_CASHOUT` 确认（携带锁定倍率 + 派彩）。
- 自动（AC）：multiplier ≥ acValue 时客户端置 `_acAutoReached` 让按钮先进 wait（防重复点），**实际由服务端执行**并经 `NET_MY_CASHOUT` 回推（与触发值可能微差）。
- 派彩 = `bet × 套现倍率`（**服务端 `NET_MY_CASHOUT` 权威**；cashout 倍率锁定在套现瞬间，非实时 currentMultiplier）。客户端只显示。

### PlayButton 五态（`WALLET_PLAY_STATE`）
| 相位 \ hasBet | 无注 | 有注 |
|---|---|---|
| BETTING | **bet** | **cancel** |
| RUNNING | **wait** | 未套现→**cashout**；已套现→**wait** |
| RESULT | **next-round** | **next-round** |
（wait/next-round 共用 `btn_wait` 图、不可点。独立 pending 视觉态。）

---

## 5. 多人房间

- **PrizePoolBar**（HUD 顶）：左「玩家数」(icon_player + count) + 右「$奖池」。源 `STATE_*`（NET_ROOM_OTHERS/SNAPSHOT 派生）。
- **AllPlayersPanel 排行榜**：他人下注/套现，**top 50，profit>0 按 bet×mult 降序**（profit=0 段 BETTING 时按 joinOrder 反序、否则正序）；100ms 增量刷新；BETTING 清空重建；VirtualScrollContainer 虚拟滚动；用户名 maskPlayerName 脱敏。盈利行金渐变发光。
- **他人套现飘字**：游戏区抛物线飘字 + 径向彩带爆发（OtherCashout*，并发上限 20，100ms 散布防同帧）。
- HUD 底栏双 tab 切「我的(MyBetPanel)」↔「全部玩家(AllPlayersPanel)」。

---

## 6. 关键节奏（时长以 [UI-GREYBOX-CG01.html](UI-GREYBOX-CG01.html) 注释面板②为权威）

- BETTING 8s；倒计时 `progress=1−max(0,(remainingMs−1000)/(totalMs−1000))`，最后 1s `lastSecond` 触发 kickoff，fadeout 330ms。
- **kickoff 序列**（1000ms）：0ms `SFX.KICK_RUN` → 100ms `SFX.GAME_START` → 400ms spine `start` 起脚。
- bg 缩放 150ms lerp；火球/速度线/模糊按 lv 升级；升档镜头震动 200ms。
- crash 序列：spine `gameover` + 烟雾/灰尘(300ms 延迟)/速度线淡出(200ms) + `crashDoneTimer` 1000ms 后 fadeOut 250ms。
- 倍率/CRASHED 横幅：slam 350ms(easeOutBack scale2→1) + 抖 250ms(@12Hz,26px)。
- 我方 cashout 面板：fade 200/hold 1000/out 200，scale 0→1.33→1。结算：vignette 200ms→0.75、banner 弹入、金币雨/彩带 3s、奖杯 spine 播一次。

---

## 7. 异常 / 断线 / 教程

- `clientExceptionRegistry` 归一：`unsupported-platform`(unsupported-game/platform-op)、`maintenance`(unavailable-service)、`log-expired`(auth.expired/invalid-token/invalid-currency)、`banned-player`(blocked-ip/banned-player)、`unsupported-currency`。→ Maintenance overlay（标题+说明 i18n，退出回 backURL）。
- 断线：reconnecting→常驻 Toast；reconnected→Toast；failed(`cg01:socket:connect-failed`/看门狗)→异常屏。ConfirmModal 用于 reload。
- **首次进入教程**：localStorage `HG_FirstTime_CrashGame` 未置 → TutorialPanel（5 步累积，3s/步、末步 5s，可点击跳过；含 logo + 示意图 + PlayButton 复刻）。

## 8. 本地化 / 货币
- locale：`en / zh / tr`（教程 logo 每语一张；其余 runtime 文本叠加，LanguageManager.bindText）。
- 货币 ISO→符号全表：USD/CAD/AUD/SGD/HKD/MXN/NZD `$`、EUR `€`、GBP `£`、JPY/CNY `¥`、KRW `₩`、INR `₹`、BRL `R$`、VND `₫`、THB `฿`、IDR `Rp`、**PHP `₱`**、MYR `RM`、TRY `₺`、RUB `₽`、ILS `₪`、NGN `₦`、PLN `zł`、SEK/NOK/DKK `kr`、CHF。

## 9. Non-Goals（本文不覆盖）
- 倍率曲线公式 / crash 概率 / RTP / AC 服务端判定精度 / 房间人数上限 / bet 档位真值 —— **均服务端**，客户端不可见（DummySocket 仅 dev 占位）。
- 资产规格/配色/音频 → [ART-AUDIO-CG01.md](ART-AUDIO-CG01.md)；控件像素坐标/z序/动画曲线 → [UI-GREYBOX-CG01.html](UI-GREYBOX-CG01.html)。

## 10. Sources
`MainScene/{GameManager,CrashGameplayManager,RoomState,PlayerWallet,LayoutZones}.ts`、`network/DummySocket.ts` + `framework/network/ProtoSocket.ts`、`PlayerHUD/*`、`ContentView/GameView/*`、`effects/gameplay-flying/*`、`SettingPanel/*`、`configs/clientExceptionRegistry.ts`、`framework/core/{ThemeConfig,LanguageManager,AudioManager,util/CurrencySymbol}.ts`、`SoundDefs.ts`。
