# GAME DESIGN — cg02a「榴莲派对 / Durian Party」

> **本文回答**：什么游戏、什么规则、什么状态流转、经济模型。给写前后端代码的 agent 当参考。
> **不回答**：资产长相/规格/音频（见 [ART-AUDIO-CG02A.md](ART-AUDIO-CG02A.md)）、每屏控件布局与动画时序（见 [UI-GREYBOX-CG02A.html](UI-GREYBOX-CG02A.html)，动画时长以 HTML 为权威）。
> **来源**：`~/harley/cg02/crashgame-cg02a-ui/cg02a` 全量代码抽取。客户端只显示服务端推送，**经济/曲线为服务端**（标注处客户端无公式）。

---

## 1. 概要

| 项 | 值 |
|---|---|
| 品类 | **多人连续曲线 crash（Aviator 类）** |
| 主体 | 一颗榴莲在天空升空，倍率连续上涨；UFO 拦截 → 榴莲被切开爆炸 |
| 玩家面 | 同房间多人实时：排行榜 + 共享奖池 + 双注栏（A/B） |
| 平台 | PixiJS v8，竖屏 1080×1920，Web（中台鉴权 + WebSocket proto） |
| 货币 | 默认 USD `$`（服务端可下发其它币种/精度） |
| 胜负 | 在 crash 前 CASH OUT → 赢 `下注 × 套现倍率`；未套现 → 输全部下注 |

**核心循环**：下注（5s）→ 榴莲起飞、倍率持续涨 → 在 UFO 拦截前点 CASH OUT 锁定 → 否则撞毁清零 → 结算 → 下一局。

---

## 2. 回合状态机（服务端驱动）

服务端 `ServerPhase` 四态，经 `NET_PHASE` 推送，客户端 `RoomState` 聚合为 `STATE_*` 信号：

```
BETTING ──(5s 倒计时结束)──▶ RUNNING ──(crash)──▶ CASHOUT_GRACE ──▶ RESULT ──▶ BETTING(下一局)
```

| 相位 | 时长 | 客户端行为 |
|---|---|---|
| **BETTING** | ~5s（`phaseEndAtMs` 绝对时戳；fallback 5000ms） | 显示待机榴莲 + 倒计时进度条；可下注/取消/设自动套现；倒计时 <1000ms 锁定（`lastSecond`）触发起跳 kickoff |
| **RUNNING** | 不定（曲线长度由服务端定） | 榴莲飞行，倍率连续上涨（`NET_GAME_STATUS` tick 推 `multiplier` + `isCrash`）；可 CASH OUT；按倍率切 lv1/2/3 |
| **CASHOUT_GRACE** | 短宽限 | crash 已发生，结算前的缓冲；按钮转 `next-round` |
| **RESULT** | ~结算 | 显示本局盈利（若套现成功）；亏损不显示（A1 关闭 lose_container） |

- **倍率曲线 100% 服务端**：客户端收到的是十进制 tick 串，**无任何客户端生成公式**；用 `LinearValuePredictor.longWindowLinear(0.5)`（保守 0.5×）做平滑插值跟随，永不超过服务端值。
- **crash 检测服务端**：`STATE_CRASH(multiplier, phase)` 到达即播撞毁动画。客户端**无 RTP / house edge / crash 概率**常量。
- `HISTORY_CAP = 20`：最近 20 局 crash 点（最新在前），驱动顶部历史条。
- 重连：`StaleRecoveryMonitor` + `NET_RECONNECTING/RECONNECTED/RECONNECT_FAILED`，mid-round 重入按当前 multiplier 同步 level；reconnect 期间出 toast/warning。

---

## 3. 飞行视觉分级（倍率 → level，纯 UI 升级点）

| level | 倍率区间 | 背景 | 榴莲皮肤 | 氛围装饰 | 数字色 | 飞行循环音 |
|---|---|---|---|---|---|---|
| **lv1** | < 2.0x | bg1 | skin lv1 | 气球 ×3 | 蓝(normal) | spin_lv12 |
| **lv2** | 2.0 – 9.99x | bg2 | skin lv2 | 热气球 ×2 | 绿(profit) | spin_lv12 |
| **lv3** | ≥ 10.0x | bg3 | skin lv3 | UFO ×2 | 金(super) | spin_lv3 |

- 阈值常量：`LV2_THRESHOLD = 2`，`LV3_THRESHOLD = 10`。
- 升级瞬间：爆裂特效 + 火花 + 抛撒榴莲切片（lv1→2 抛 3 片、lv2→3 抛 2 片）+ `level_up_2/3` 音效。
- ⚠️ **这些只是视觉升级点**，倍率本身连续、由服务端定；榴莲 Y 固定不动（见 [ART-AUDIO-CG02A.md](ART-AUDIO-CG02A.md) §2 铁律）。

---

## 4. 下注经济（PlayerWallet，双注栏 A/B）

```
DEFAULT_BET_LIST = [0.5, 1, 2.5, 5, 8, 15, 100, 999.99]   DEFAULT_INDEX = 1 (=1.00)
  ↳ 真实 USD 档位仅 [0.5,1,2.5,5,8,15]（PM 规格）；尾部 [100,999.99] 是 dev 测试项，会被 MAX_PER_BET/MAX_TOTAL_BET 拒掉（源码注释「线上请删」），复现勿当真档位
MIN_PER_BET = 0.10   MAX_PER_BET = 100   MAX_TOTAL_BET = 150 (A+B 合计)
快捷投注 QuickBet = [$1, $5, $15]（硬编码 USD；源码 TODO：后端按币种下发不同档位，当前未接线）   货币默认 USD '$'
自动套现 AutoCashout 输入范围 [1.01, 1000]x，默认 2.00x，最多 2 位小数
```

- **双栏独立**：A、B 两条注各自有 `betAmount / acEnabled / acValue / hasBet / currentBetId`。**余额(balance)与总注(totalBet)全局/房间共享**（totalBet 是房间汇总）。
- **加减注 ±档位**：BetSwitcher 的具体增减幅由 wallet/服务端决定（UI 只发 `UI_BET_LOWER/RAISE`）。
- **下注流程**：BETTING 内点 BET → 锁定该栏（`UI_BET_PLACE`）→ 按钮转 cancel；可在 BETTING 内 cancel 撤回。

### 套现（Cashout）四型
| 类型 | 含义 |
|---|---|
| **MANUAL/FULL** | 手动点 CASHOUT，全额结算，按钮转 wait |
| **AUTO** | 倍率达到 acValue 时客户端本地先 fire（`WALLET_AC_FIRED_LOCAL` → halo 特效），服务端 `NET_MY_CASHOUT` 为准 |
| **HALF** | 先套 50%，该栏保留 `hasBet=true`，可对剩余 50% 再做一次 FULL（`cashout-half-done` 态） |

- 派彩：`cashout = bet × multiplier`，客户端**只显示服务端回的 `payoutAmount`（gross）**，不自算盈亏；HALF 后服务端回 `remainingBetAmount`。
- 结算显示：套现成功 → SpriteDigits `win` 样式显示派彩；亏损 → 不显示（A1 关闭）。

### PlayButton 状态映射
| 相位 \ 状态 | hasBet=false | hasBet=true |
|---|---|---|
| BETTING | 可选注 → **bet** | **cancel** |
| RUNNING | **wait**（未下注） | 有 AC→**cashout-no-half**；无 AC→**cashout**（可 50%+FULL 双键） |
| CASHOUT_GRACE / RESULT | **next-round** | **next-round** |

---

## 5. 多人房间

- **PrizePoolBar**（HUD 顶条）：左「N Players」(`STATE_PLAYERCOUNT_CHANGED`) + 右「$奖池」(`STATE_TOTALBET_CHANGED`)；飞行/宽限/结算期锁定，BETTING 重置。
- **AllPlayersPanel 排行榜**：他人套现结果，**top 50，按 total win 降序**（`totalWin = A.half + A.full + B.half + B.full`）；100ms 增量刷新（`STATE_LEADERBOARD_DELTA`），BETTING 清空、snapshot 全量重建。每卡显示 用户名(截断 8 ASCII/5 CJK) + A/B 槽 的 Half%/Bet/Win（盈利金色渐变、亏损红）。
- **他人套现飘字**（CashoutEventHandler）：他人套现时在游戏区抛物线飘字（最多并发 20，1000ms 生命）。
- HUD 底栏双 tab 切换「我的注(MyBetPanel)」↔「全部玩家(AllPlayersPanel)」。

---

## 6. 关键节奏（时长以 [UI-GREYBOX-CG02A.html](UI-GREYBOX-CG02A.html) 注释面板②为权威）

- 下注总时长 `BETTING_TOTAL_MS = 5000`；起跳 `JUMP_BAKED_MS = 667`，倒计时 ≥4000ms 才播完整 idle3→idle2→jump 序列，否则回退 1× loop。
- 榴莲入场滑入 0.6s（`ENTRY_OFFSET_Y=400`）；背景升级交叉淡化 600ms；飞行 woosh 每 2000ms。
- crash 序列总 `CRASH_DURATION_MS = 2000`（spine `end` + UFO + 光柱 + roundlight×4）。
- 盈利数字：落下 450ms(easeOutBack，从 -181px) + 抖动 250ms(@12Hz, 26px)，延迟 1000ms 出、2000ms 抖。
- 倍率撞毁横幅：slam 350ms(scale 2→1) + 抖 250ms。

---

## 7. 异常 / 断线状态机

`clientExceptionRegistry` 把服务端码归一为 UI 异常态：
- `unsupported-currency` / `unsupported-platform`（unsupported-game/platform-op）
- `maintenance`（unavailable-service）
- `log-expired`（auth.expired-token / invalid-token / invalid-currency / platform.rejected-auth）
- `banned-player`（blocked-ip / auth.banned-player）

异常 → Maintenance overlay（标题+描述 i18n，退出键回 backURL）。ConfirmModal 用于 reload 确认。Toast（3s 自动）/ Warning（需确认、排队）用于提示与断线警告。各屏长相见 HTML，本节只管触发/状态。

---

## 8. 本地化

- locale：`en / zh / tr / jp / vi / th / id`（`tr` 土耳其语在字号上与 `zh` 同组，用大字形）。
- 平台码→web：chinese/zh-cn/hans→zh，zh-hant/hant→tr，japanese/jp→jp…；web→game：zh→hans，tr→hant。
- logo 按语言：en→logo_en、zh→logo_zh_hans、tr→logo_zh_hant。
- 文案走 `LanguageManager.bindText`（推送式，locale 变化自动刷新；WeakRef 自动清理）。

---

## 9. Non-Goals（本文不覆盖）

- 倍率曲线公式、crash 概率、RTP、house edge、AC 服务端判定精度 —— **均服务端**，客户端不可见。
- 资产规格 / 配色 / 音频文件 → [ART-AUDIO-CG02A.md](ART-AUDIO-CG02A.md)。
- 控件像素坐标 / z 序 / 动画曲线细节 → [UI-GREYBOX-CG02A.html](UI-GREYBOX-CG02A.html)。

## 10. Sources

`MainScene/{GameManager,CrashGameplayManager,RoomState,PlayerWallet,LayoutZones}.ts`、`PlayerHUD/*`、`ContentView/GameView/*`、`effects/scene2/*`、`SettingPanel/*`、`configs/clientExceptionRegistry.ts`、`core/{ThemeConfig,LanguageManager,AudioManager}.ts`。换皮血统见 `GAME_GUIDE_RESKIN.md`（CG02→CG02A）。
