---
type: prd-split
audience: game-logic (frontend + backend code agents)
product_code: ss02
product_name: "Beach Party / 沙滩派对"
genre: slot / 6×5 grid · multiplier-balloon wild (real-money)
engine: Unity WebGL (IL2CPP, Addressables 2.8.x)
build: 1.0.0-71 (2026-03-16 14:44:18) — 当前 dev 线上实测版本
output_profile: obsidian_md
status: reverse-engineered (结构+网格=构建 extracted;数学=服务端(本地无 ss02 server repo)→ server-authoritative 未 cite;机制结构=换肤框架文档 derived)
language: zh-CN
created: 2026-07-01
purpose: agent 训练素材 —— ss02 玩法逻辑 / 状态机 / 经济结构 / 协议
---

# ss02「Beach Party / 沙滩派对」— Game Design Document（逆向·Unity）

> **分工**：只管玩法/规则/状态/数学。美术见 [ART-AUDIO-SS02.md](ART-AUDIO-SS02.md)；布局/层级/坐标见 [UI-GREYBOX-SS02.html](UI-GREYBOX-SS02.html)。
>
> ⚠️ **来源与置信度（本作特有约束）**：
> - **构建 = ss02 自身**（`slotmachine-ss02-unity` 1.0.0-71，dev S3 实测）。网格/符号/资产/布局 = UnityPy 解 `data.unity3d` **extracted**。
> - **本地无 ss02 服务端 repo**（`~/harley/ss02` 只有 3 个 UI 宿主 repo）→ 老虎机数学(RTP/权重/转轮/赔付值)= **server-authoritative，本轮无一手 cite**（不同于 ss03 能直读 socket repo）。
> - **机制"结构"层**部分取自 **ss02a/ss02b 换肤框架文档**（`slotmachine-ss02a-ui/ai/*.md`，三者共用同一玩法框架代码）→ 标 `derived`。**⚠️ 那些文档是【进行中的换皮 repo】,含 SS03 遗留占位值**：其"5×3 网格 / 25 payline"与"赔付表(青龙/红龙…)"均为**遗留/待定,与 ss02 构建实测矛盾,本 GDD 不采用**(见 §3)。
> **徽标**：`extracted`=ss02 构建解出；`derived`=换肤框架文档/资产推定；`server`=服务端权威未证。**无 `validated`**(本轮未取真机截图)。

---

## 1. Summary 摘要

> **朝向：真·双朝向,各有独立 Canvas**（不同于 ss03 的响应式重锚）。构建含 `Canvas_PlayerHUD_Vertical`(竖 1080×1920) **与** `Canvas_PlayerHUD_Horizontal`(横 1920×1080) 两套 HUD;免费视频也分 `videoTexture`(1920×1080)/`videoTextureVertical`(1080×1920)。参考分辨率:横 1920×1080、竖 1080×1920(另支持 1920×1440 / 1440×1920)。两朝向布局见 HTML。

**Beach Party（沙滩派对）** = **沙滩夏日主题 6×5 老虎机**,核心是**乘数气球 Wild**(红气球带 ×2~×100 乘数)。**网格 6 列 × 5 行**(构建 `ScenarioGrid` 实测:`Reel_1..6`×`SymbolCell_1..5`,单元格 168×168)。Scatter=**霓虹摩天轮**,≥3 触发**免费旋转**(换皮框架文档 `derived`)。含 **购买免费游戏(Buy Free Spin)** 与 **双倍机会(Double Chance / ante bet)** 两个投注增强(构建资产+节点实证)。中奖分级 Big/Super/Mega/Epic。

**核心循环（结构 derived,数值 server）**：
```
[可选] 开 Double Chance(提升 scatter 概率, 加注) / 或 Buy Free Spin(直接买免费)
选注 → SPIN(client:spin)
  → 服务端下发 6×5 落定 + 中奖 + 乘数气球(Wild ×2~×100) + scatter 数
  → 客户端演出:符号中奖高亮 + 气球乘数结算 → 赢分(×乘数)
  → 摩天轮 Scatter ≥3 → 免费旋转(夜晚沙滩换皮,可 retrigger)
  → 结算回基础
```

## 2. 状态机 / 模式（Base + Free Spin）
```
BaseGame ──(摩天轮 Scatter ≥3, 或 Buy Free Spin)──▶ FreeSpin ──(轮次耗尽)──▶ 结算 → BaseGame
```
- **两模式换皮(资产实证 extracted)**:背景 `Background_Normal`(白天沙滩) / `Background_FreeSpin`(夜晚沙滩);转轮框 `Frame_Bg` / `Frame_Bg_FreeSpin`。**无 Pity/保底模式**(不同于 ss03)。
- 进入免费有**过场视频** `asset_v1/videos/freeSpin.mp4`(横竖各一版) + `Enter Free Spin_Wheel` 摩天轮音(换皮框架文档 derived)。
- BaseGirl / FreeGirl **角色位**(吉祥物,非玩法元素;横屏在机台前、竖屏在背景层;Spine,未在 288 张 PNG 中→在 Spine 骨架/Addressables)——`derived`。

## 3. 玩法核心：6×5 + 乘数气球 Wild

### 3.1 网格（构建实测 extracted）
- **6 列 × 5 行**:`ScenarioGrid` → `Reel_1..Reel_6`,每列 `SymbolCell_1..5`;单元格 **168×168**、列距 168、行距 168(相邻无缝);`GridBg` 1008×840(=6×168 × 5×168)。世界转轮 `Reel_1..6` world x=[-2.54,-1.52,-0.51,0.51,1.52,2.54](均匀,居中)。
- ⚠️ **与换皮文档矛盾**:`ss02a/ai/UNITY_PROJECT.md` 写 `HorizontalCount=5, VerticalCount=3`(5×3)+"25 payline"——**与 ss02 构建实测 6×5 不符**,该文档是进行中的换皮 repo(且其赔付表标注"SS03 遗留名"),**故其网格/payline/赔付值一律不采信**,以 ss02 构建为准。

### 3.2 中奖机制 = **pay-anywhere（任意位置计数赔付，scatter-pays）** `validated(Guide 帮助页)`
- **不是 payline/ways**：同一符号在整盘**出现 N 个即赔**(与位置无关);Guide「Regular Symbol Payout Value」按**计数档** `8~9 / 10~11 / 12+` 给赔率。构建佐证:有 `Reel_1..6`/`SymbolCell` 但**无 payline 节点**(`Line/LeftLine/RightLine/OffsetLine` 都是账单分隔线);账单详情 `WinSymbolContainer`(赢分符号明细)。
- **派彩公式**(Guide「Payout Calculation」):`Payout = (Total Bet ÷ 20) × 该符号 odds ×(乘数,若有)`。一次下注 = **20 credits**(账单详情实证 `Bet Credit 20 · Amount/Credit 0.025`,即 0.5 注 ÷20)。
- 结算三段(账单详情实测节点):`WinSymbolContainer`(符号赢分) + `ScattersContainer`(scatter 计数) + `MultipliersContainer`(乘数汇总)。
> ⚠️ 数学"值"来源:本地 **无 ss02 服务端 repo + localization bundle 403 未取到一手** → 上述规则/赔率以**运行时 Guide 帮助页(截图)**为 `validated` 依据,标注"localization/server 一手未 cite"。**几何(位置/尺寸)不受影响,全部来自代码 compose。**

### 3.3 符号集 + 赔付表（符号=构建 extracted;赔率=Guide 帮助页 `validated`）
资产 index 1-9(Spine `*.atlas`);赔率按计数档 **8~9 / 10~11 / 12+**(Guide「Regular Symbol Payout Value」):

| idx | 资产 | 符号 | 8~9 | 10~11 | 12+ |
|--:|---|---|--:|--:|--:|
| 1 | `Symbol_1_A_YACHT` | 游艇(霓虹快艇) 最高 | 200 | 500 | 1000 |
| 2 | `Symbol_2_B_SEAPLANE` | 水上飞机 | 50 | 200 | 500 |
| 3 | `Symbol_3_C_RAFT` | 充气救生艇 | 40 | 100 | 300 |
| 4 | `Symbol_4_D_SUNDAE` | 圣代 | 30 | 40 | 240 |
| 5 | `Symbol_5_E_CONE` | 彩虹甜筒 | 20 | 30 | 200 |
| 6 | `Symbol_6_F_POPSICLE` | 粉冰棍 | 16 | 24 | 160 |
| 7 | `Symbol_7_G_MANGO` | 芒果 | 10 | 20 | 100 |
| 8 | `Symbol_8_H_WATERMELON` | 西瓜 | 8 | 18 | 80 |
| 9 | `Symbol_9_J_BLUEBERRY` | 蓝莓 最低 | 5 | 15 | 40 |
| Scatter | `Symbol_SCATTER`(`SCATTER.atlas`) | 霓虹摩天轮 | — 触发免费(§5) | | |
| Wild | `Symbol_Wild_X{2,3,5,10,20,30,50,100}` | **乘数气球** | — 仅免费·带乘数(§3.4) | | |

> 赔率值 = 运行时 Guide 帮助页(`validated`);localization/server 一手未 cite(bundle 403/无 repo)。odds 为**赔率倍数**,乘 `(Total Bet÷20)` 得赢分(§3.2)。⚠️ 换皮文档的 SS03 遗留赔付表(青龙…)不采用。

### 3.4 乘数气球 Wild（资产 extracted;规则 Guide `validated`）
- Wild = **红气球,携带乘数 ×2/×3/×5/×10/×20/×30/×50/×100**(`Symbol_Wild_X*` + `MULTIPLIER_X*` Spine + `BallonContainer`/`BallonDigit`)。
- **规则(Guide「Multiplier」)**:**仅免费游戏出现**;乘数**作用于 base payout**;**若多个乘数同时落地(如 M1、M2),总赢 = base payout ×(M1 + M2)**(相加,非相乘)。
- 引爆音 `Big/Small Ballon Bomb`/`Fruit Bomb`。

## 4. 投注增强（构建实证 extracted,数值 derived/server）
- **Buy Featured Games(购买免费,主界面「BUY FEATURED GAMES」)**:`GameBoardUI_Placeholder/…/PurchaseFreeSpin` + `EnsureFreePanel`(确认弹窗) + `BuyFeature_Popup_*`。直接买进免费旋转;**价格 = 100×底注**(截图 `validated`:底注 0.5 → 50.00)。(ss02a 换皮 repo 移除了它,但 **ss02 原作在**。)
- **Double Chance(「MORE FREE GAME CHANCES」/ ante bet)**:`DoubleChance` + `Toggle(on/off)` + `Bet`。开启后**加注 ~1.5×底注**(截图 `validated`:0.5 → 0.75)以提升免费触发概率。
- `BetItem_Boost` 资产 = 增强投注标识。

## 5. 免费旋转（Free Spin）`validated(Guide/主界面)`
- **触发(Guide「Scatter Symbol」)**:base 内落 **≥4 个摩天轮 Scatter → 触发 10 次免费**(主界面横幅亦证"4 [wheel] Trigger 10 Free Spins");免费内 **≥3 个 Scatter → retrigger +10 次**。(⚠️ 换皮文档写的 base=3 是 SS03 遗留,不采用;以 Guide 为准。)
- 换皮:夜晚沙滩 `Background_FreeSpin` + `Frame_Bg_FreeSpin`;进入有摩天轮过场视频 + `FreeSpinCount_Label`(剩余转数) + `FreeSpinTotalProfit_Text`(累计赢分)。
- 免费内乘数气球梯是否更高/累计 = **server**(资产未区分 free 专用乘数,疑与 base 共用 ×2~×100)。

## 6. 投注 / 自动 / RTP / 中奖分级
- **bet 档位(换皮框架 `derived`)**:`{0.5, 1, 2.5, 5, 8, 15, 25, 50, 70, 100, 250, 500}`(`ss02a/ai/UNITY_PROJECT.md`;实际档位/币种运行时下发,server)。
- **auto 档位**:`{10, 20, 50, 100, 200, -1(无限)}`。
- **中奖分级(音频 + 换皮文档 `WIN_EFFECT.md` `derived`)**:Basic `<bet×5` / **Big ≥bet×5** / **Super ≥bet×20** / **Mega ≥bet×50** / **Epic ≥bet×100**(音频 `2_Big Win`/`3_Super Win`/`4_Mega Win`/`5_Epic Win` 对应)。
- **RTP / 转轮权重 / 赔付值 / 乘数分布 / Buy 价格 / DoubleChance 概率 = server-authoritative,本地无 repo 未证**。

## 7. 网络 / 协议（换皮框架文档 `derived`）
- 路径:`/game/ss02-socket/socket.io`、`/game/ss02-api/v1/api`(宿主 find-cdn + `ss02-ui-static` 实证)。ss02a/b 走运行时 `indexConfig`(socketPath/apiPath)。
- socket 事件(`ss02a/ai/Features/REACT_UNITY_BRIDGE.md`):`server:free_spin:triggered` / `server:balance:changed` / `server:alert`;连接 queryParams `{access_token, platform, game_id}`。
- **React↔Unity 桥**:`BridgeReady` 握手 → `HandleAppConfig(AppConfig{envInfo, urls{socketUrl,socketPath,apiUrl,cloudfrontUrl,...}, userInfo, defaultSettings, verifyResponse})`。result 由服务端 socket 下发,客户端只演出。
- 异常:`server:alert` / RoastPopup(维护/重连)。

## 8. Non-Goals / 待补
- **无一手数学**:RTP/转轮条/符号权重/赔付值/乘数施加规则/Buy 价格/DoubleChance 概率/免费给转数 —— 需 **ss02 服务端 repo**(本地缺)或真机录屏。
- **未截图(derived,待升级 validated)**:win 规则(pay-anywhere vs ways vs line)、乘数气球引爆编排、免费流程、Buy/DoubleChance 交互、大奖分级演出。
- **Addressables UI/玩法 bundle 已抽**(纠正上一版"未抽"):`ui_settingpage_pack`(设置 V/H + 帮助赔付 `GuidePaperDisplay` + `LanguageSelector` + 账单)、`ui_popuppage_pack`(Reconnecting/Toast/Warning)、`gameplay_freegame_noticerpack`(FreeSpinNoticer 免费过场)、`gameplay_winreward_effectpack`(Big/Super/Mega/Epic 特效)、`gameplay_decoration(_character_pack)`(装饰 + 角色 girl)、`gameplay_introanim` —— 布局见 HTML。bundle 路径:本地包 `addressables_assets/aa/WebGL/`、远程包 `addressables_assets/ServerData/WebGL/`。剩余未抽:部分 audio pack、locale 表。
- 美术/动画时长 → ADD/HTML。

## 9. Sources
- **ss02 构建 1.0.0-71** `data.unity3d`(UnityPy):网格 6×5、符号、气球 Wild、Buy/DoubleChance 节点、双朝向 HUD、音频/动画名 —— 一手 extracted。
- **换皮框架文档** `slotmachine-ss02a-ui/ai/{PROJECT,UNITY_PROJECT,TODO}.md` + `ai/Features/{FREESPIN,WIN_EFFECT,REACT_UNITY_BRIDGE}.md`(三 repo 共用玩法框架)→ 机制结构 `derived`;**其 SS03 遗留赔付/5×3-25line 不采用**。
- CDN:`https://dev-assets-hybergaming.s3.us-west-2.amazonaws.com/ss02`(公开 S3,find-cdn 实证)。
- ⚠️ **无 ss02 服务端 repo** → 数学层未取一手源,标 server。

---
**GDD 结束(逆向·Unity 1.0.0-71)。网格/符号/功能=构建实测;数学=服务端未证;机制结构=换肤框架文档(剔除 SS03 遗留)。美术见 ART-AUDIO-SS02.md;布局见 UI-GREYBOX-SS02.html。**
