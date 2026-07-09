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
> 本版（v1.1.0）玩法结构与数学示例值已按实测定稿；仅币种投注区间等运营侧数值保留 §6 TBC。

---

## §1 项目定位

步进式倍率 crash game：小鸡横向逐格冲过马路，每安全过一格倍率沿难度曲线上爬，玩家在每格之间自主决定 CASH OUT（锁定收益）或 GO（继续赌下一格）；被车撞即本局清零，走到赛道尽头按封顶倍率自动结算（Ultimate Win）——`crash-step` 交互踩在 `lane-scene`（横向卷轴场景）盘面上。单人离散对局，无对局倒计时、无多人广播、无跨局奖池。竖屏移动优先。

- 代号：CG03
- interaction：crash-step
- board：lane-scene（横向卷轴马路，向左滚动；小鸡视觉固定屏幕中央偏左，锚点 x474）
- 参考游戏：Chicken Road 2（InOut Games，玩法对标）
- 屏幕与适配：竖屏 portrait；**设计画布 1080×1920**，壳层 contain 等比缩放 + 黑边居中（实测定稿）
- 语言：英文(en), 简体中文(zh), 繁体中文(tr)（logo 出三语言变体；locale 键名 `tr` 落地内容为繁体中文）
- 货币：CNY, PHP, USD（顶栏货币符号图标三币种 + 通用符号回退）
- 非目标：不做 4 赛道差异化视觉换皮（v1 共用一套美术）；不做乘客 / 载具 cinematic；不做多人 / 跨局奖池 / 对局倒计时；不做 Bonus Game / Buy Bonus（实测确认无此屏与资产）；不做横版独立资产；不自建钱包（依赖平台 Wallet API）

---

## §2 游戏流程与状态机

| 状态 | 标识符 | 说明 |
|---|---|---|
| 启动加载 | `loading` | logo + 进度条（含错误 / 重连面板）；完成后出「开始」按钮 |
| 待机下注 | `betting` | 下注 + 选赛道，等点 PLAY；场景显示小鸡待机 + 前方 2 个待机井盖 |
| 飞行中 | `flying` | 已锁注逐格推进；每格之间等玩家 CASH OUT / GO（GO 请求由服务端逐格判定回执） |
| 撞车 | `crashed` | 服务端判定撞车，本局清零；场景内撞车演出（车压顶 + 红闪），无独立覆层 |
| 结算展示 | `settled` | 兑付 / 撞车 / 通关后的结果展示期；**普通 4s / 通关 10s 后自动回 `betting`（无 Play Again 按钮）** |

```
loading ──就绪+开始──► betting ──PLAY(锁注)──► flying(首格自动 GO)
  ▲                        ▲                    │
  │                        │            ┌─[safe]┴─(逐格: 倍率上爬, 等 GO/CASH OUT)
  │                        │            ├─[crash]────► crashed ─┐
  │                        │            ├─[CASH OUT]─► settled ◄┘
  │                        │            └─[走满全程]─► Ultimate Win → settled(10s)
  │                        └───────(4s/10s 自动)──────── settled
  └─(异常)─ maintenance / 错误弹窗
```

- HUD 双态（PlayState）：`bet`（难度选择 + PLAY 大钮）⇄ `cashout`（CASHOUT + GO 双钮）。
- 覆层（settings / language_picker / guide / history / warning / toast）叠加在主状态上、不进主状态机；settings 全屏覆层打开时吸收全部输入。

标准局流程：设定投注额 → 选赛道 → PLAY 锁注并自动走第 1 格 → 逐格：起跳 → 路障弹出挡车 → 落格 → 身后井盖翻金 → 加成预告 →（下一次 GO 时提交上一格加成)→ 等决策 → 任意格 CASH OUT 落袋 / GO 继续 / 走满全程自动 Ultimate Win。锁注后不可改投注额与赛道。

---

## §3 核心玩法

| 参数 | 标识符 | 规格 | 默认值 |
|---|---|---|---|
| 投注金额 | `bet_amount` | 快捷筹码 **5 档直接置值**（服务端 /bet/config 下发，UI 恰按 5 档布局）+ MIN / MAX 步进钮；无手动输入框 | 服务端 defaultBet（缺省回退 1.00） |
| 赛道 | `difficulty` | 4 档：`EASY / MEDIUM / HARD / HARDCORE`（向上弹出的下拉选择器） | EASY |
| 车道总数 | `total_lanes` | 按赛道 28 / 22 / 18 / 14 格 | 28（EASY） |
| 当前倍率 | `current_multiplier` | **乘法合成**：`eff = 逐格倍率 x_k × (1 + 累计加成 cumulative_bonus)` | 起步 x_1（EASY=1.01） |
| 翻盖加成 | `reveal_bonus` | 4 档 `none/+0.10/+0.30/+0.50`；**Model B 提交**：到达格仅预告，下一次 GO 时提交进累计；累计封顶 `b_max=2.0` | none |
| 视野 | `preview` | 待机显 2 个待机井盖；飞行中显示**下一格**倍率预告（井盖气泡 + GO 按钮同步显示 `{next}x`） | 下一格 |
| 步进节流 | `go_throttle` | GO 请求节流 600ms（=跳跃动画时长）；双钮另有 0.65s 软锁 | — |

玩法要点：

- Cash Out：飞行中任意格触发，`payout = bet_amount × eff`（服务端回执 `payoutAmount` 为权威，按钮上金额为估算显示）。
- 撞车：GO 判定 `safe=false` 即撞车，损失本金；场景内演出（车冲入 + 红闪 + 小鸡倒地），结算 4s 后自动回投注。
- 终点强制：走满 `total_lanes` 由服务端标记 `capTriggered` 自动按封顶结算，触发 Ultimate Win 过场（终点线 + 旗 + 金币彩带雨）。
- 路径记忆：已走格保留翻金井盖与加成标签，随卷轴左移出屏。

---

## §4 数学框架

数学表为**服务端常驻配置**（`routes.json`），实测定稿如下；运行时经 `client:routes` 下发难度曲线供 UI 铺格。

全局：目标 **RTP = 0.96**；加成累计上限 **b_max = 2.0**；有效倍率 `eff = x_k × (1 + cumulative_bonus)`。

| 赛道 | 格数 | 封顶 x_n | 曲线 γ | 加成分布 none / +0.1 / +0.3 / +0.5 | 理论单局上限(eff) |
|---|---|---|---|---|---|
| EASY | 28 | 20.0 | 1.28 | 0.80 / 0.12 / 0.06 / 0.02 | 60x（=20×3） |
| MEDIUM | 22 | 20.0 | 1.30 | 0.75 / 0.14 / 0.08 / 0.03 | 60x |
| HARD | 18 | 25.0 | 1.33 | 0.70 / 0.16 / 0.10 / 0.04 | 75x |
| HARDCORE | 14 | 30.0 | 1.36 | 0.60 / 0.20 / 0.10 / 0.10 | 90x |

逐格判定顺序（每次 GO 服务端执行并回执）：

```
r1: if r1 < p_hazard[lane] → crash, 本局清零
safe: x = x_k[lane]                        # 逐格倍率曲线
提交上一格加成预告 → cumulative_bonus(≤2.0)  # Model B
r2: 按加成分布抽本格预告 tier(none/small/medium/big)
eff = x × (1 + cumulative_bonus)
if lane == total_lanes → capTriggered(Ultimate Win, 自动兑付)
```

- 逐格样例（EASY 28 格）：x_k = 1.01, 1.04, 1.10, 1.17, 1.25, …, 17.16, 20.00；p_hazard 单调升 0.051 → 0.157。HARDCORE 14 格：x_k = 1.07 → 30.00；p_hazard 0.111 → 0.335。四表全量随服务端配置交付。
- 公平性：服务端带种子揭示机制（SeedReveal，provably-fair）；抽样细节由服务端实现。

---

## §5 系统边界（美术相关）

| 边界 | 触发 | 是否产生 UI 素材 | 说明 |
|---|---|---|---|
| 网络请求失败 | GO / 下注 ack 超时（8s）或断网 | yes | Warning 弹窗 + 按钮 pending 置灰；重连后快照恢复续局 |
| 断线自动兑付 | flying 中断线 | yes | Toast 倒数 **15s**（每秒 tick），归零自动兑付；服务端侧同步保障 |
| 闲置超时 | **3 分钟无操作** | yes | 告警提示 + 15s 倒数自动兑付 + 会话过期弹窗（实测存在，产 UI） |
| 余额不足 | 投注额 > 余额 | yes | Toast 提示（i18n），PLAY 阻断 |
| 会话续局 | 崩溃 / 关页后重进 | yes | 服务端保留对局；重进后快照恢复到原格续局（无动画重建盘面） |
| 重复登录 | 同账号他处登录 | yes | SSO 弹窗踢出（不进倒数） |
| 收款进行中 | CASH OUT 请求未回 | yes | 按钮 α0.5 置灰，直到结算回执 |

---

## §6 TBC 表

| item | owner | 影响范围 |
|---|---|---|
| 投注步进 / 精度 / 区间（各币种） | 产品 + BackOffice | §3 投注面板、/bet/config 配置 |
| 各币种金额显示小数位规则 | 设计 + 数据 | 投注 / 派彩数字显示 |
| 局中续局过期时长 | 产品 | §5 会话续局 |
| how-to-play 指南终稿（三语言） | PM + 本地化 | 指南页正文与配图 |

---

## Changelog

| 版本 | 日期 | delta |
|---|---|---|
| v1.0.0 | 2026-07-02 | 初版：crash-step × lane-scene 双轴定型；玩法状态机、难度系统、翻盖加成、数学接入结构落定；数值项归并 §6 TBC |
| v1.1.0 | 2026-07-09 | 实测定稿：分辨率 1080×1920；状态机改实名 betting/flying/crashed/settled（结算 4s/10s 自动回投注，**移除 Play Again 交互**）；倍率合成修正为**乘法** eff=x_k×(1+累计加成) 且累计封顶 b_max=2.0（Model B 提交时序）；数学全表实值（RTP 0.96、四赛道曲线/撞车概率/加成分布、理论上限 60/60/75/90x）；赛道名定为 EASY/MEDIUM/HARD/HARDCORE；快捷筹码为 5 档置值非累加、无手输框；语言口径修正（zh=简体，tr=繁体）；§5 修正：**存在 3 分钟闲置自动兑付**（原版误记为无超时）、补断线 15s 倒数与 SSO；确认无 Buy Bonus 屏与资产；Provably Fair 确认保留（SeedReveal）；§6 TBC 由 11 项缩至 4 项 |
