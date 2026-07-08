---
project: CG05
doc: GDD
interaction: crash-step
board: grid
status: draft
owner: Nathan Kao (Game PM)
---

# CG05 MineBeach 沙灘掃雷 · GDD（游戏设计文档）

> 本文是 auto-art 的游戏上下文来源，美术只读参考，不设签字。视觉审签对象见 `ADD.md`。
> 未定数值一律进 §6 TBC 表并挂 owner，不在正文填占位数字。

---

## §1 项目定位

沙滩主题的 Mini Game 博弈小游戏：玩家在 5×5 盘面上逐格翻牌，安全格使累积倍率指数上升，可随时收款离场，踩雷即本局失败——`crash-step` 交互踩在 `grid` 盘面上。

- 代号：CG05
- interaction：crash-step
- board：grid（5×5 = 25 格）
- 参考游戏：Mines by Jili Games
- 屏幕与适配：1080×1920，portrait（手机竖版为主；Web 版维持竖版尺寸置中，左右留白以满版背景填充，不另做横向版面）
- 语言：简体中文, 英文, 葡萄牙语(巴西), 越南文, 印尼文, 泰文, 韩文, 马来文, 印度语, 缅甸文（共 10）
- 货币：CNY, PHP, USD, BRL（共 4）
- 目标 RTP：97.5%（House Edge 2.5%）
- 非目标：不支持多人对战；不自建钱包（依赖平台 Wallet API）；不支持 Free Round；不支持自定义盘面大小（固定 5×5）；不支持社交分享；本期无 Jackpot / 星星格等机制

---

## §2 游戏流程与状态机

| 状态 | 标识符 | 说明 |
|---|---|---|
| 等待下注 | `idle` | 显示游戏主画面，尚未下注 |
| 下注中 | `betting` | 玩家设定下注额与地雷数 |
| 游戏中 | `playing` | 玩家逐格翻开，可随时收款 |
| 主动收款 | `cash_out` | 玩家按收款，以当前倍率结算 |
| 爆炸 | `mine_hit` | 翻到地雷，本局失败 |
| 完美通关 | `perfect_clear` | 翻完所有安全格，自动以最高倍率结算 |
| 局结算 | `round_settled` | 显示完整盘面，回到 idle |
| 派彩待处理 | `payout_pending` | Wallet 派彩失败，进入 retry |

```
idle
  │
  ▼
betting ◄─[Server 建立 round 失败 → 回退 betting，未扣款，不写 DB]
  │
  ▼
playing ───────────────► payout_pending ──[retry]──┐
  │                          ▲                       │
  ├─on_cashout──────► cash_out ─────────┐            │
  │                                      │            │
  ├─on_mine_hit─────► mine_hit ─────────►┤            │
  │                                      │            │
  └─on_perfect_clear► perfect_clear ────►┤◄───────────┘
                                         ▼
                                    round_settled
                                         │
                                         ▼
                                        idle
```

标准局流程：玩家设定下注额 → 选地雷数（3~24）→ 按开始 → 后端生成地雷地图（不传前端）→ 逐格翻开，安全格累乘倍率 → 任意时机按收款落袋 / 或翻完全部安全格触发完美通关。MVP 单局单盘面单次下注，翻牌开始后不可改下注额或地雷数。

---

## §3 核心玩法

| 参数 | 标识符 | 规格 | 默认值 |
|---|---|---|---|
| 下注金额 | `bet_amount` | 从默认 Bet Option 列表中选取（不支持手动输入） | TBC |
| 地雷数 | `mine_count` | 整数，3~24 | 4 |
| 盘面大小 | `grid_size` | 固定 5×5 = 25 格 | 25 |
| 安全格 | `tile_safe` | 数量 = 25 − `mine_count`，翻开使倍率累乘 | — |
| 地雷格 | `tile_mine` | 数量 = `mine_count`，翻开即本局失败 | — |
| 当前倍率 | `current_multiplier` | 每翻一安全格 `× step_multiplier`，初始 `1.0` | 1.0 |

玩法要点：

- 累乘制：`current_multiplier = current_multiplier × step_multiplier(mine_count, revealed_count)`，初始 `1.0`。
- Cash Out：`playing` 任意时机触发 `on_cashout`，`payout = bet_amount × current_multiplier`，随后进入 `round_settled`。
- 完美通关：翻完所有安全格且未踩雷，自动以最高倍率 cashout，带专属动效与音效。
- 爆炸：翻到地雷，揭示全盘真实位置，玩家损失 `bet_amount`（本金不返还）。

---

## §4 数学框架

地雷数 `M`、总格 25、已翻 `k`：

| 项 | 公式/规格 | 示例值 |
|---|---|---|
| 全安全概率 | `P(k) = C(25 - M, k) / C(25, k)` | M=24, k=1 → 1/25 = 0.04 |
| 公平倍数 | `fair_multiplier(k) = 1 / P(k)` | M=24, k=1 → 25x |
| 实际倍数 | `actual_multiplier = fair_multiplier(k) × 0.975`（RTP_factor） | M=24, k=1 → ≈ 24.275x |
| 目标 RTP | 97.5%，对 3~24 全地雷数一致，上线前模拟验证 | 97.5% ± 容许误差 |
| 每步系数 `step_multiplier` | 基于组合机率 + RTP 系数（0.975）逐格产出 | 完整 3~24 表 TBC（§6） |
| 最大中奖 Max Win | 需数学组确认 | TBC（§6） |

示例倍率表（仅 3/5/10/24 地雷数 × 前六格，供 UI 展示比例参照；完整 3~24 表为 §6 TBC）：

| 地雷数 \ 已翻格 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 3 | 1.11x | 1.27x | 1.46x | 1.68x | 1.92x | 2.21x |
| 5 | 1.22x | 1.41x | 1.64x | 1.90x | 2.20x | 2.54x |
| 10 | 1.62x | 2.15x | 2.84x | 3.75x | 4.95x | 6.53x |
| 24 | 24.38x | — | — | — | — | — |

倍率上限随地雷数连动（初版建议值，待数学组验算定稿，见 §6）：

| 地雷数范围 | `max_multiplier` 区间 | 初版建议 | 备注 |
|---|---|---|---|
| 3~5 | 10x~25x | 20x | 低风险区，避免前期倍率过高 |
| 6~10 | 50x~100x | 80x | 中风险区 |
| 11~15 | 200x~500x | 300x | 中高风险区，主流高倍区 |
| 16~20 | 500x~1,000x | 800x | 高风险区，需搭配 Max Win |
| 21~23 | 25x~500x | 200x | 极短局区 |
| 24 | — | 25x（24.275x） | 需独立处理 |

> 注：16~20 颗的上限高于 21~24 颗——25 格盘面中前者可走步数更多、加成次数更多；21~23 颗仅剩 4~2 步。若设倍率上限，须确认不影响目标 RTP（高地雷数需特别验算，见 §6）。

---

## §5 系统边界（美术相关）

只收会产生 UI 素材需求的边界：

| 边界 | 触发 | 是否产生 UI 素材 | 说明 |
|---|---|---|---|
| 余额不足 | 下注额 > 余额 | yes | 开始按钮 disabled + Toast「余额不足」 |
| 网络请求失败 | 翻格/下注请求失败 | yes | 错误 Modal「操作失败，请重试」，不扣积分 |
| 收款进行中 | Cash Out 请求未回 | yes | 所有格子与按钮 disabled，直到结算回应 |
| 单一 session | 同账号第二端进入 | yes | 提示「此账号已在其他视窗开启游戏，请关闭后再试」并禁止进入 |
| 断线重连 | `playing` 中网络中断 | yes | 重连回到 `playing` 续局；逾时按 `reconnect_timeout` 自动 cashout 结算 |
| 派彩失败 | Wallet 派彩返回失败 | yes | 进入 `payout_pending` → retry，UI 呈现处理中状态 |

> `reconnect_timeout` 依照运营商上限处理，不预设时间。

---

## §6 TBC 表

| item | owner | 影响范围 |
|---|---|---|
| `step_multiplier` 每步系数 + 完整 3~24 倍率表 | 数学组 | §3 / §4 倍率展示、倍率条刻度 |
| 最大中奖 Max Win 数值 | 数学组 | §4 数值、可能的胜利上限展示 |
| 倍率上限区间是否影响 RTP（高地雷数验算） | 数学组 | §4 上限策略 |
| `bet_amount` 默认 Bet Option 档位表（各币种） | 产品 + BackOffice | §3 下注面板选项 |
| Dev / Staging / QA / UAT 排期 | PM | 交付节点 |
| 设计需求 Figma 启动 | 美术 | 视觉细化 |

---

## Changelog

| 版本 | 日期 | delta |
|---|---|---|
| v1.0.1 | 2026-06-29 | 下注仅选默认 Bet Option（移除金额输入框）；`reconnect_timeout` 依运营商上限处理；FE/BE Lead 记为 Jack Liao |
