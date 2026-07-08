---
project: SS03
doc: GDD
interaction: slot
board: reel
status: draft
owner: Game PM (TBC)
---

# SS03 Mahjong Streak 麻將連莊 · GDD（游戏设计文档）

> 本文是 auto-art 的游戏上下文来源，美术只读参考，不设签字。视觉审签对象见 `ADD.md`。
> 玩法数值（转轴尺寸 / 赔线 / 赔付 / RTP / 免费次数）尚未定稿，一律进 §6 TBC 表并挂 owner，不在正文填占位数字。

---

## §1 项目定位

麻将招财主题的视频 slot：符号为麻将牌面，中奖走 Tumble（级联连消）玩法——盘面消除后剩余符号塌落、空位再填充，单次投注可连续触发多轮消除，直至无新的中奖组合。交互为 `slot`，盘面为 `reel`（tumble 形态）。

- 代号：SS03
- interaction：slot
- board：reel（tumble 级联，盘面几何尺寸见 §3 / §6 TBC）
- 参考游戏：无（原创麻将 slot；客户端沿用平台共用 Unity-middleware 外壳）
- 屏幕与适配：1920×1080 / 1080×1920，landscape + portrait 双向自适应
- 语言：英文(en), 印度语(hi), 印尼文(id), 韩文(kr), 马来文(my=ms-MY Malay), 泰文(th), 越南文(vi), 简体中文(zh-hans), 繁体中文(zh-hant)（共 9，另有 Shared 非语言共用表；locale 总数待核，TBC 见 §6）
- 货币：TBC（见 §6，由运营 / PM 定）
- 目标 RTP：TBC（见 §6，数学组定）
- 非目标：不自建钱包（依赖平台 Wallet API）；本包不定义具体转轴尺寸 / 赔线 / 赔付表 / RTP（属数学组交付，见 §6）；不含社交分享

---

## §2 游戏流程与状态机

外壳层（React）负责 Loading / 异常 / 桥接，Unity 层负责基础转、Tumble 结算与 Free Spin。状态标识符 snake_case。

| 状态 | 标识符 | 说明 |
|---|---|---|
| 加载 | `loading` | bootstrap：背景 + Loading 进度，等待登录 + 资产 + Unity GameReady |
| 主游戏 | `main_game` | 转轴就绪，等待投注 / Spin |
| 转轴判定 | `spin_resolve` | 一次 Spin 落定后判定中奖组合 |
| 级联消除 | `tumble_cascade` | 中奖符号消除 → 剩余塌落 → 空位填充，循环直至无新中奖 |
| 中奖演出 | `win_present` | 达档触发 Big / Super / Mega 演出层 |
| 免费旋转公告 | `free_spin_announce` | 触发 Free Spin 时的公告 / 引导 / 开始确认屏 |
| 免费旋转进行 | `free_spin_play` | Free Spin 循环，显示累计与剩余次数 |
| 免费旋转结束 | `free_spin_end` | 结束确认屏，回主游戏 |
| 维护 / 异常 | `maintenance` | 外壳 exception 归一态（全屏暗框） |

```
loading
  │  登录OK + 资产/版本就绪 + Unity GameReady
  ▼
main_game ──on_spin──► spin_resolve ──有中奖──► tumble_cascade ──┐
  ▲                        │                         │  (循环消除)  │
  │                        │无中奖                    └─────────────┘
  │                        ▼                         达档 │
  │                     main_game ◄── win_present ◄───────┘
  │                        │
  │                        └──触发 Free Spin──► free_spin_announce
  │                                                   │
  │                                                   ▼
  │                                            free_spin_play ──(次数用尽)──► free_spin_end
  └───────────────────────────────────────────────────────────────────────────┘

loading/main_game ──exception──► maintenance ──(exception 清除)──► loading
main_game ──ExitGame(backURL / history.back)──► [退出]
```

标准局流程：玩家设定投注额 → Spin → 转轴落定判定 → 若有中奖组合则进入 Tumble 级联（消除 / 塌落 / 填充循环），逐轮累计本局赢分 → 达到档位阈值触发中奖演出 → 满足条件触发 Free Spin 层。Tumble 级联深度、触发规则与免费次数为数学组交付（见 §6）。

---

## §3 核心玩法

| 参数 | 标识符 | 规格 | 默认值 |
|---|---|---|---|
| 盘面几何 | `board_geometry` | 转轴列数 × 行数 / cluster 形态（Tumble 常见 5×N 或 cluster） | TBC |
| 中奖判定 | `win_evaluation` | scatter-pay / ways / cluster（Tumble 无固定线概率高） | TBC |
| 级联消除 | `tumble_cascade` | 中奖符号消除 → 剩余塌落 → 空位填充，循环至无新中奖 | 机制确证，参数 TBC |
| 百搭 | `wild_baihua` | 麻将「百搭」= 万能牌，可替代常规符号参与组合 | 确证存在 |
| 中奖档位 | `win_tier` | 至少 Big / Super / Mega 三档达档演出 | ≥3 档确证 |
| 免费旋转 | `free_spin` | Scatter / 特定组合触发免费旋转层（整套公告→进行→结束） | 存在确证，触发数 / 次数 TBC |

玩法要点：

- Tumble 级联：一次 Spin 后，命中的符号组合被消除，其上方符号向下塌落填补空位，顶部再补入新符号；只要新盘面仍有中奖组合就继续消除，本局赢分逐轮累加，直至无新中奖。级联轮数无固定上限（由玩法参数与随机结果决定）。
- 百搭（Wild）：麻将「百搭」牌为万能符号，替代常规牌面凑成中奖组合；是否具倍率 / 是否仅现于特定位置为 TBC（§6）。
- 中奖分档：赢分达阈值触发 Big / Super / Mega 演出层（是否另有 Normal / Epic 档为 TBC）。
- 免费旋转：确证存在完整 Free Spin 流程（公告 / 引导 / 开始确认 / 进行累计 / 结束确认）；触发条件、免费次数、是否 retrigger 为数学组交付（§6）。

---

## §4 数学框架

Tumble slot 的数学模型（赔付表 / 各符号权重 / RTP / 波动 / Free Spin 期望）为数学组交付物；本包不编造数值，未知项一律进 §6。

| 项 | 公式/规格 | 示例值 |
|---|---|---|
| 目标 RTP | 由可换数学表决定 | TBC |
| 赔付表 | 各符号 × 命中数量的赔付倍数表 | TBC |
| 符号权重 / 转轴带 | 各符号在盘面出现的权重分布 | TBC |
| Tumble 期望 | 单次 Spin 的级联轮数期望 / 赢分分布 | TBC |
| Free Spin 触发与期望 | 触发条件 + 免费次数 + retrigger + 期望贡献 | TBC |
| 最大中奖 Max Win | 单局赢分上限倍数 | TBC |

> 上表所有数值属数学组 / 数学表交付（见 §6）。本包定型的是美术可见的玩法骨架（Tumble、Free Spin、中奖分档）与视觉需求，数值定稿后回填。

---

## §5 系统边界（美术相关）

只收会产生 UI 素材需求的边界：

| 边界 | 触发 | 是否产生 UI 素材 | 说明 |
|---|---|---|---|
| 断线重连 | 运行中网络中断 | yes | 重连提示 / Toast；恢复后回到中断前状态 |
| 单一 session | 同账号他处登录 | yes | 弹窗提示（`sso-disconnected`），禁止双端并行 |
| 外壳异常态 | 平台维护 / 版本 / 货币不支持等 | yes | 全屏纯 CSS 暗框（标题 + 描述 + 可选退出按钮 + 版本号） |
| 语言切换 | Unity 内切语言 | yes | `SetLanguage` 桥同步外壳 locale；标题 / 演出图按语言换图（见 ADD §3e / §6） |
| 派彩 / 结算失败 | Wallet / 结算返回失败 | yes | 处理中 / 重试提示（具体文案见共用壳 exceptions，ADD §8） |

> 外壳 exception 归一枚举与文案沿用平台共用壳（见 ADD §8 的 `exceptions` 模块），本作差异见该表。

---

## §6 TBC 表

| item | owner | 影响范围 |
|---|---|---|
| 盘面几何（列数 × 行数 / cluster 形态） | 数学组 | §3 盘面、ADD §3a 符号排布、盘面区版面 |
| 中奖判定方式（ways / cluster / scatter-pay） | 数学组 | §3 玩法、ADD §3b 赔付表屏 |
| 完整符号集（除已知 發 / 中 / 萬 / 八萬 / 百搭 外） | 数学组 + 美术 | ADD §3a 符号表 |
| 赔付表（各符号 × 命中数量倍数） | 数学组 | §4 数值、ADD §3b 赔付表屏内容 |
| 目标 RTP / 波动 | 数学组 | §4 数值 |
| 符号权重 / 转轴带 | 数学组 | §4 数值 |
| Free Spin 触发条件 / 免费次数 / retrigger | 数学组 | §3 / §4、ADD §3d Free Spin 层文案 |
| 最大中奖 Max Win | 数学组 | §4 数值、中奖上限展示 |
| 是否存在 Normal / Epic 等额外中奖档 | 数学组 + PM | ADD §3c win-tier 演出矩阵档数 |
| 货币列表 + 金额显示小数位（各币种） | 运营 + PM | §1 货币、下注 / 派彩数字显示 |
| Dev / Staging / QA / UAT 排期 | PM | 交付节点 |
| locale 总数与最终语言名单（当前登记 9 + Shared） | PM | §1 语言、ADD §3e / §6 本地化 |

---

## Changelog

| 版本 | 日期 | delta |
|---|---|---|
| v1.0.0 | 2026-07-02 | 初版：Tumble slot 玩法骨架 + Free Spin + 中奖分档确证入正文；全部玩法数值挂 §6 TBC |
| v1.0.1 | 2026-07-02 | 语言口径改为 9 locale + Shared 共用表（my=ms-MY Malay），删缅甸文；locale 总数挂 §6 TBC（owner: PM） |
