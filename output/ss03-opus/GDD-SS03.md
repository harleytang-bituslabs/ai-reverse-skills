---
type: prd-split
audience: game-logic (frontend + backend code agents)
product_code: ss03
product_name: "Mahjong Streak / 麻将连莊"
genre: slot / 2000-ways (real-money, cascade/tumble)
engine: Unity WebGL (IL2CPP, Addressables 2.x)
build: 1.0.0-56 (2026-03-26 09:11:18) — 当前 dev 线上实测版本
output_profile: obsidian_md
status: reverse-engineered (结构=构建 extracted;数学=服务端 repo 直读 cited;runtime 动效未截图=derived)
language: zh-CN
created: 2026-06-30
purpose: agent 训练素材 —— ss03 玩法逻辑 / 状态机 / 经济结构 / 协议
---

# ss03「Mahjong Streak / 麻将连莊」— Game Design Document（逆向·Unity）

> **分工**：只管玩法/规则/状态/数学。美术见 [ART-AUDIO-SS03.md](ART-AUDIO-SS03.md)；布局/动画时长见 [UI-GREYBOX-SS03.html](UI-GREYBOX-SS03.html)。
>
> ⚠️ **来源与置信度**：ss03 是 **Unity WebGL** 游戏。客户端 MonoBehaviour 配置被 **IL2CPP 剥离 typetree**（UnityPy 仅能读到 `m_Name`，玩法配置读不到）。**但本作的老虎机数学全部在服务端 repo 直读到了一手源**（`slotmachine-ss03-socket`，Java/Spring），故本 GDD 数值层 = **`server` 但有精确 cite**（file:line），不再是黑箱。Addressables catalog 全是本地化包（9 语），无玩法/数学配置。
> **徽标**：`extracted`=Unity 构建解出（资产/动画名/RectTransform）；`server`=服务端源码直读（带 file:line）；`derived`=由资产/命名推定，未经服务端或截图证实。**无 `validated`**（本轮未取真机截图；截图到位后升级动效/编排类条目）。

---

## 1. Summary 摘要

> **朝向**：ss03 主体为**竖屏 1080×1920**（Unity Canvas 全部 `*_Vertical`、参考分辨率 1080×1920）。宿主 `slotmachine-ss03-ui-static/ss03/src/components/Background.tsx` 用 `isLandscape = size.width > size.height` 同时支持横屏 1920×1080，但 **Addressables catalog 无横屏/场景包、无 `_Horizontal` Canvas** → 横屏 = **同一竖屏 Canvas 响应式重锚 + letterbox**，非独立资产（`derived`，需截图确认）。本 GDD 玩法/数学与朝向无关。

**Mahjong Streak（麻将连莊）** = **麻将题材 2000-ways 老虎机**（cascade / 消除连击）。**5 列错列网格**落麻将牌，**可见窗 4-5-5-5-4**（中 3 列各见 5 行、外 2 列各见 4 行，外列垂直居中）。**相邻列出现同牌即成 way**（`ways = 4×5×5×5×4 = 2000`，非固定 payline）。中奖牌**消除→上方下落补位→重新结算**形成连击（cascade streak，呼应游戏名 "Streak/连莊"），**每次连续 cascade 倍率进一档**。**元宝 Wild 百搭**、**金牌（Gold）在中 3 列出现并在中奖时转 Wild**、**胡（Hu）Scatter ≥3 触发免费游戏**。

**核心循环**：
```
选注 → SPIN(client:spin)
  → 服务端生成 4-5-5-5-4 落牌 + cascade 序列(scenarios[]) + scatter
  → 客户端逐 scenario 演出:结算 ways → ×cascade 倍率 → 消除中奖牌 → 下落补位 → 重算
  → cascade 链结束 → totalPayout
  → 胡 Scatter ≥3 → 免费游戏(client:free_spin, 更高倍率梯, 可 retrigger)
  → 结算回基础
```

## 2. 状态机 / 模式（Base + Free + Pity/Incentive-Free）

```
BaseGame ──(胡 Scatter ≥3)──▶ FreeGame ──(轮次耗尽)──▶ 结算 → BaseGame
   └──(Incentive 条件命中, 服务端 IncentiveService)──▶ Pity/Incentive Free Game
```

- **三套换皮（资产实证 `extracted`）**：背景 `Back_BaseGame` / `Back_FreeGame` / `Back_PityFreeGame`；转轮框 `Frame_TopFence` / `_Free` / `_Pity`；连击件 `Combo_Base_*` / `Combo_Free_*` / `Combo_PityFree_*`。→ **本 1.0.0-56 仍含 Pity/保底免费模式**（与某些后续构建不同）。
- **Combo 倍率梯（cascade 倍率，`server` 实证）**：
  - Base：`x1 → x2 → x3 → x5`（`Const.java` L22 `BASE_MULTIPLIER = {1:1, 2:2, 3:3, 4:5}`，cascade≥4 封顶 x5）
  - Free：`x2 → x4 → x6 → x10`（`Const.java` L24 `FREE_MULTIPLIER = {1:2, 2:4, 3:6, 4:10}`）
  - Pity/Incentive Free：资产 `Combo_PityFree_x2/x4/x6/x10`（梯同 Free，`extracted`）。
  - **倍率索引 = cascade 次数**：`multiplierId = min(scenarioId, 3)`，第 N 次 cascade 取梯第 N 档（`SpinService.java` L186-187）。
- 倍率梯与连击件均有 `_Light` 高亮态资产（当前档点亮）。

## 3. 玩法核心：2000-ways + cascade 消除连击

### 3.1 网格 / ways（`server` 实证）
- **维度**：`Const.java` L8-10 `MAX_ROW_SIZE = 6`、`COLS = 5`。
- **可见窗 4-5-5-5-4**：`SpinUtils.rowStart(col)` L25-28 —— `col==0 || col==COLS-1` 时起始行 = `(6-1)-1`（见 4 行），否则见 5 行。即外 2 列各 4 行、中 3 列各 5 行。**与构建 `ScenarioGrid` 实测一致**（`extracted`：Reel_1/Reel_5 各 4 个 `SymbolCell`、Reel_2/3/4 各 5 个；单元格 184×224、列距 184、行距 204；外列垂直居中）。
- **ways**：`SpinService.java` L200-203 `ways = ∏(各列该符号出现数)`；满窗 = `4×5×5×5×4 = 2000`（命中 banner「2000 路」/ `Guide_2000_Ways` 资产）。
- **成奖 = ways-pay**：从最左列起、**相邻列出现同符号**即累计（任意行位，非固定 payline）。`Guide_2000_Ways` 图示：相邻列同牌 ✓、跳列 ✗。

### 3.2 赔付表（`server` 直读 `symbol.json`，**非推定**）
来源：`slotmachine-ss03-socket/src/main/resources/math_table/symbol.json`（`hits` 数组按 `totalColWSymbol-1` 索引；index 2/3/4 = 3/4/5 连）。符号 code 0-8 = 普通牌、100-108 = 金牌（赔付相同）、201 = Scatter、202 = Wild。

| code | 符号（对应美术） | 3 连 | 4 连 | 5 连 | 档 |
|--:|---|--:|--:|--:|---|
| 0 | **發** GreenDragon（绿，honor） | 10 | 25 | 50 | 最高 |
| 1 | **中** RedDragon（红，honor） | 8 | 20 | 40 | |
| 2 | **白板** WhiteDragon（白，honor） | 6 | 15 | 30 | |
| 3 | **八萬** bawan（万） | 5 | 10 | 15 | |
| 4 | **五筒** wutong（筒） | 3 | 5 | 12 | |
| 5 | **五条** wutiao（条） | 3 | 5 | 12 | |
| 6 | **三筒** santong（筒） | 2 | 4 | 10 | |
| 7 | **二筒** ertong（筒） | 1 | 3 | 6 | 最低 |
| 8 | **二条** ertiao（条） | 1 | 3 | 6 | 最低 |
| 100-108 | **金牌 Gold**（GA-GI） | 同 0-8 | | | 中奖转 Wild |
| 201 | **胡 Hu** = Scatter | — 触发免费游戏 | | | |
| 202 | **元宝** = Wild | — 替代除 Scatter 外全部 | | | |

> `Guide_Sample_Payout` 帮助页只画了 **發 5/4/3=50/25/10**，与 `symbol.json` 一致（交叉印证）。
> **派彩公式**（`SpinService.java` L204-207）：`单符号派彩 = Bet × ways × hits[连数] × 0.05(FIXED_FACTOR)`；`本 cascade 总派彩 = Σ符号 × multiplier(cascade 档)`。最终 `totalPayout = Σ各 cascade`，再受 `maxPayout` 封顶（见 §6）。

### 3.3 Wild / Gold / Scatter（`server` 实证）
- **Wild = 元宝（code 202）**：替代除 Scatter 外所有符号参与 ways 计算（`SpinService.java` L264-274：把 wildCount 加到各列各符号计数）。
- **金牌 Gold（code 100-108）只在中 3 列**：`SpinUtils.randomKey(column)` L13-18 —— `column != 0 && column != 4` 时才可能 `+100` 变金牌；外 2 列恒普通牌。中奖时金牌**转 Wild** 参与后续 cascade（`SpinService.java` L127-129）。
- **Scatter = 胡（code 201）**：`SpinService.java` L140-154 统计全盘胡数；`< SCATTER_COUNT(=3)` 不触发，`≥3` 触发免费游戏。

## 4. 连击倍率（cascade streak）
- **机制**：cascade（tumble）—— `SpinService.java` L75-108/318-349 主循环：`settleBet → evalTotalPayoff → 有中奖则 crush(消除中奖牌, 金牌转 wild) → cascade(上方下落 + 顶部补新) → scenarioId++ → 重算`，直到某次无中奖退出。
- **倍率随 cascade 进档**：见 §2（Base x1/2/3/5、Free x2/4/6/10，第 4 次起封顶）。**倍率显示 = 一排 4 个方槽**（`ScenarioMutiplierDisplay/Slot_1..4`，各 **175×140**、x=[116,340,564,788]、pitch 224，`extracted`），当前档 `LightSlot+Aura+LightImage` 点亮；**挂在转轮框顶栏**（world-space `MatchComboDisplay` under `SlotMachine/Decorations/FrameFence/TopFence`），**直接位于牌网正上方**，背景=顶栏横幅 `Frame_TopFence`（非屏幕顶部悬浮条、非一条 bar）。见 ADD §4 / HTML ①。
- **派彩**：见 §3.2 公式；最终值服务端下发，客户端用 `DigitNumber` 切图显示（余额💰 + WIN 两枚 pill + 本轮 `MessageBanner` 横幅）。

## 5. 免费游戏（Free Game）
- **触发**：胡 Scatter `≥3`。**给转数按 Scatter 数**（`Const.java` L26 `FREE_COUNT_W_SCATTER`）：

  | Scatter 数 | 3 | 4 | 5 | 6 | 7 |
  |--|--|--|--|--|--|
  | 免费转数 | 10 | 12 | 14 | 16 | 18 |

- **Retrigger**：免费中再出 Scatter 触发追加（`FreeSpinListener.java` L62 `triggerFreeSpin(..., true)`）。
- **倍率梯更高**：Free x2/4/6/10（§2）。换皮 `Back_FreeGame` + 金色满列（`Guide_Free_Game` 图示一整列转金 + 盘龙边框）。
- **流程音**（ADD §音频）：`Free Spin Transition → Charge Jump Text → Confirm Button → Calculate → ComboDisplaySwap → End` + BGM `FreeGame`。
- **Pity / Incentive Free Game**：`IncentiveService.java` L64-97 —— 服务端按玩家旋转统计（如长期未中/余额条件）下发的激励性免费，配置存 Redis（`incentive:config`）。对应 `Back_PityFreeGame` / `Combo_PityFree_*` 资产（`extracted`）。具体触发阈值 = Redis 配置（`server`）。

## 6. 投注 / RTP / 数学表
- **bet**：`BetConfigService.java` L28-44 —— bet 档位**存 Redis**（`platform:op:currency:bet`），按平台/运营商/币种动态，非硬编码。校验 `SpinListener.java` L39-43（`chips.contains(bet)`）。
- **max payout 封顶**：`BetConfigService.getMaxPayout` L46-51（Redis）；`SpinService.java` L369-371 派彩超 `maxPayout` 则截顶。
- **RTP = 多数学表 + MAB 选臂**：
  - 数学表 `math_table/normal_*.zip`，每个含 `math_table.meta`（含 RTP/hit_rate/max_win）。例 `normal_zero`：overall RTP `0.9685`、base `0.7038`（max win 200×）、free `5.5007`（max win 2000×）。另例 `normal_Zero_BG97...`：overall `0.963`。
  - **MAB 控制器** `ss03-ai-mab-controller/src/main/resources/config_ss03_v3.json` L6-17 `arms` 列出十个 `normal_*` 臂；按玩家画像/状态为每位玩家选数学表（动态 RTP）。
- **reel strips / 符号权重**：`Reel.java`（`record Reel(int index, int[] reel)`）；实际转轮序列在 `math_table/normal_*.zip` 内的 **`base.script` / `free.script`（二进制/加密，`TextScriptResolver` 反序列化）** —— **未解密，符号权重 = 编码进 reel 序列**（`server`，需解密 SDK，超出本轮范围）。

## 7. 网络 / 协议（`server` 实证）
- 路径（宿主 + 部署 chunk 实证）：`/game/ss03-socket/socket.io`（socket.io 实时）、`/game/ss03-api/v1/api`（REST：`/auth/validate`、`/auth/verify`）。
- **事件**：`client:spin`（`SpinListener.java` L21）、`client:free_spin`（`FreeSpinListener.java` L19）、`server:free_spin:triggered`、`server:balance:changed`（`server.proto`）。
- **`SpinRet` 下发结构**（`server.proto` L43-52）：`spin_id, spin_type(0:base/1:free), GridStop[](终停位), scenarios[](全 cascade 序列), scatter, total_payout, bet`。
  - `Scenarios`（L37-41）：`id(cascade 序号), grid[], win_symbol[]`。
  - `WinSymbol`（L28-35）：`code, column(出现列数), ways, multiplier, payout, totalPayout`。
  - `Scatter`（L21-26）：`code(201), count, triggered(≥3), triggerCount(给转数)`。
- Unity 经 `react-unity-webgl` 桥与宿主通信；result 全由服务端 socket 下发，**客户端只演出**。
- 异常/重连：`ReconnectingPopup` / `ToastPopup` / `WarningPopup`（布局见 HTML）。

## 8. Non-Goals / 待补
- **未解密**：reel strip 实际序列与符号权重（`base.script`/`free.script` 二进制）→ 需服务端解密 SDK。
- **未截图（`derived`，待升级 `validated`）**：cascade 逐帧编排、连击进档时机的视觉、免费流程演出、大奖（大奖/巨奖/超级巨奖）阈值与演出、近失（NearMiss）触发。
- **Redis 动态值**：bet 档位/币种、max payout、Incentive 阈值（部署期配置）。
- 美术长相/动画时长 → ADD/HTML。

## 9. Sources
- **服务端（数学一手源，cited）**：`slotmachine-ss03-socket`（`Const.java`、`SpinService.java`、`SpinUtils.java`、`symbol.json`、`server.proto`、`BetConfigService.java`、`IncentiveService.java`、`FreeSpinListener.java`）；`ss03-ai-mab-controller/config_ss03_v3.json`。
- **Unity 构建 1.0.0-56**（结构/资产，`data.unity3d` via UnityPy）：符号集、Combo/Frame/Back 三模式资产、`Guide_*` 帮助页、`ScenarioGrid` 可见窗、动画/音频名。
- **宿主 repo** `slotmachine-ss03-ui-static`（socket/api 路径、朝向、i18n）。
- CDN：`https://dev-assets-hybergaming.s3.us-west-2.amazonaws.com/ss03`（公开 S3，find-cdn 实证）。

---
**GDD 结束（逆向·Unity 1.0.0-56）。数学层=服务端源码直读 cited；动效层待截图升级。美术见 ART-AUDIO-SS03.md；布局见 UI-GREYBOX-SS03.html。**
