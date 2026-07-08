---
project: CG03
doc: GDD
interaction: crash-step
board: lane-scene
status: draft
owner: Game PM (TBC)
---

# CG03 Cluck Dash 小鸡狂奔 · GDD（游戏设计文档）

> 本文是 auto-art 的游戏上下文来源，美术只读参考，不设签字。视觉审签对象见 `ADD.md`。
> 未定数值一律进 §6 TBC 表并挂 owner，不在正文填占位数字。

---

## §1 项目定位

步进式倍率 crash game：小鸡横向逐格冲过马路，每安全过一格倍率递增，玩家在每格之间自主决定 CASH OUT（锁定收益）或 GO（继续赌下一格更高倍率）；被车撞即本局清零，走到赛道尽头自动按最大倍率强制结算——`crash-step` 交互踩在 `lane-scene`（横向卷轴场景）盘面上。单人离散对局，无对局倒计时、无多人广播、无跨局奖池。竖屏移动优先。

- 代号：CG03
- interaction：crash-step
- board：lane-scene（横向卷轴马路，向左滚动；小鸡视觉固定屏幕中央偏左）
- 参考游戏：Chicken Road 2（InOut Games，玩法对标）
- 屏幕与适配：竖屏 portrait，移动优先 H5（Web 版维持竖版尺寸置中）；基准分辨率 TBC（见 §6）
- 语言：英文(en), 繁体中文(zh), 土耳其文(tr)（logo 出此三语言变体；locale 文件 `tr` 当前落地为繁中，见 §6）
- 货币：CNY, PHP, USD（顶栏货币符号图标已备三币种 + 通用符号回退）
- 非目标：不做 4 赛道差异化视觉换皮（v1 共用一套美术）；不做乘客 / 载具 cinematic（CG03A 内容）；不做多人 / 跨局奖池 / 对局倒计时；不做 Bonus Game / Buy Bonus；不做横版独立资产（竖屏优先）；不自建钱包（依赖平台 Wallet API）

---

## §2 游戏流程与状态机

| 状态 | 标识符 | 说明 |
|---|---|---|
| 启动加载 | `loading` | logo + 进度条载入，含错误 / 重连面板 |
| 待机下注 | `idle` | 下注 + 选赛道，等点 PLAY |
| 跳格中 | `hop` | 小鸡跳一格中（入场 / 起跳动画 + server 判定回执），按钮 disabled |
| 落地待决策 | `at_tile` | 落到下一格，等玩家 STOP / GO |
| 撞车结算 | `bust` | 被车撞，本局清零，看覆层 → Play Again |
| 胜利结算 | `win` | STOP 主动收款 或 走到终点强制结算，看覆层 → Play Again |

```
loading
  │[就绪]
  ▼
idle ──[PLAY + 投注OK]──► hop(第1格)
  ▲                        │
  │                        ├─[safe]────► at_tile
  │                        ├─[crash]───► bust
  │                        └─[reach_end]► win(终点强制)
  │                                       ▲
  │            at_tile ─[GO]─► hop        │
  │            at_tile ─[STOP]────────────┘
  │
  └──[Play Again]── bust | win
```

标准局流程：玩家设定投注额 → 选赛道 → 按 PLAY 锁定投注 → 小鸡起跑（入场动画）→ 逐格 HOP：安全则路障弹出挡车、落到下一格、身后井盖翻金锁定倍率、翻盖判定加成、等决策 → 任意时机 STOP 落袋 / GO 继续 / 走到尽头自动 MAX WIN。翻牌开始后本局不可改投注额与赛道。

覆层（settings / language_picker / guide / history / network_error_popup / super_win_celebration）叠加在主状态上、不进主状态机；打开时主状态冻结。

---

## §3 核心玩法

| 参数 | 标识符 | 规格 | 默认值 |
|---|---|---|---|
| 投注金额 | `bet_amount` | 快捷筹码累加（1 / 2 / 5 / 10），可双击编辑；MIN / MAX / 步进 / 精度按币种 TBC | 上次投注额 |
| 赛道 | `track` | 4 档难度：Country/Easy、Town/Medium、City/Hard、Highway/Extreme | Country/Easy |
| 车道总数 | `total_lanes` | 按赛道：28 / 22 / 18 / 14 格 | 28（Easy） |
| 当前倍率 | `current_multiplier` | 每安全过一格 = 逐格倍率 + 翻盖加成，逐步累加，初始 `1.00` | 1.00 |
| 翻盖加成 | `reveal_bonus` | 每过一格触发一次，4 档 `empty / small / medium / large`，加法叠加 | empty |
| 视野 | `preview` | 只显示当前格 + 前方 2 格倍率，第 3 格起不预告 | 前 2 格 |

玩法要点：

- 逐步累加：`current_multiplier = 过格后逐格倍率 + 翻盖加成`（先过格、再叠翻盖；翻空加成 = 0）。
- Cash Out：`at_tile` 任意时机触发 STOP，`payout = bet_amount × current_multiplier`，随后进入 `win`。
- 撞车：跳跃中段（落地前）来车冲入碰撞即 `bust`，玩家损失 `bet_amount`（本金不返还）；覆层展示撞车前最后一格倍率（仅展示）。
- 终点强制：走到最后一格自动按最大倍率结算，带终点彩带 + 金币雨演出；达 super-win 阈值时叠 SUPER WIN 庆祝。
- 不预告未来：视野内仅当前格 + 前方 2 格；已走格保留翻金井盖 + 当时倍率作为路径记忆，随卷轴左移出屏。

---

## §4 数学框架

每次 hop 的判定接入结构（判定顺序，供 UI 与埋点对齐；具体数值全部 TBC，见 §6）：

```
r1 ~ U(0,1); if r1 < crash_probability_curve[lane]: result = crash, 退出
result = safe; base = base_multiplier_curve[lane]
r2 ~ U(0,1) 按 reveal_distribution 落档 → tier; tier ≠ empty 时抽 delta
current_multiplier = base + delta          # 先过格、再叠翻盖（与 §3 一致）
if lane == total_lanes: result = reach_end
```

| 项 | 公式/规格 | 示例值 |
|---|---|---|
| 逐格倍率曲线 | `base_multiplier_curve[lane]`，每赛道一份，server 常驻不下发 | `[pending_math]` |
| 单步撞车概率 | `crash_probability_curve[lane]`，每赛道一份 | `[pending_math]` |
| 翻盖加成分布 | `reveal_distribution{empty, small, medium, large}` 各档 p + delta 范围 | `[pending_math]` |
| 累加倍率 | `current_multiplier = base_multiplier_curve[lane] + reveal_delta` | `[pending_math]` |
| 目标 RTP | 每赛道一致，上线前 ≥100 万局模拟验证 | `[pending_math]` |
| 单局 Max Win 上限 | `max_win_cap`，每赛道一份，封顶不被绕过 | `[pending_math]` |
| SUPER WIN 阈值 | `super_win_threshold`，触发满屏庆祝 | `[pending_math]` |

> 4 个赛道共用同一套场景美术，赛道间**只有数学差异**：车道总数、逐格倍率曲线、单步撞车概率、翻盖加成档分布。全部数值待数学组交付，见 §6。

---

## §5 系统边界（美术相关）

只收会产生 UI 素材需求的边界：

| 边界 | 触发 | 是否产生 UI 素材 | 说明 |
|---|---|---|---|
| 网络请求失败 | `hop` / 下注请求超时或断网 | yes | 弹 `network_error_popup` + 按钮置灰；重连后重试同 roundId，server 幂等返回同结果 |
| 余额不足 | 投注额 > 余额 | yes | `start` 返回 insufficient_balance，PLAY 阻断 + 充值引导 |
| 会话续局 | 崩溃 / 关页后重进 | yes | 无强制结算，server 保留对局，重进 loading 后恢复到原格续局 |
| 货币 / 登录异常 | 货币错误 / 登录过期 | yes | `network_error_popup` 呈现对应异常文案（复用公版 exceptions） |
| 收款进行中 | STOP 请求未回 | yes | 按钮置灰，直到结算回应 |
| 长时间不操作 | `at_tile` 久置 | no | 不超时、不强制结算（无额外素材需求） |

---

## §6 TBC 表

| item | owner | 影响范围 |
|---|---|---|
| 4 赛道逐格倍率曲线（M1） | 数学组 | §3 / §4 倍率展示、前方 2 格倍率气泡 |
| 4 赛道单步撞车概率（M2） | 数学组 | §4 判定、撞车节奏 |
| 翻盖加成 4 档占比与加成数值（M3） | 数学组 | §3 / §4 翻盖演出档位 |
| 整体 RTP 目标（M4，PRD 参考 96–97%） | 数学组 | §4 数值校验 |
| 单局 Max Win 上限（M5） | 数学组 | §4 封顶、终点结算展示 |
| SUPER WIN 触发金额 / 倍率阈值（M6） | 数学组 | §4 super-win 庆祝触发 |
| 投注步进 / 精度 / 区间（各币种，M7） | 产品 + BackOffice | §3 投注面板 |
| 基准分辨率 / 适配尺寸 | 产品 + 前端 | §1 屏幕适配 |
| 局中续局过期时长 | 产品 | §5 会话续局 |
| Provably Fair 是否保留 | 产品 | §4 RNG 设计 |
| `buy_bonus_popup` 残留屏去留 | 产品 + 设计 | 屏幕清单范围 |

---

## Changelog

| 版本 | 日期 | delta |
|---|---|---|
| v1.0.0 | 2026-07-02 | 初版：crash-step × lane-scene 双轴定型；玩法状态机、难度系统、翻盖加成、数学接入结构落定；数值项归并 §6 TBC |
