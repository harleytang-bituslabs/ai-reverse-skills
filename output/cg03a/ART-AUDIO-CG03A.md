---
type: prd-split
audience: art_audio
product_code: cg03a
product_name: "Jeepney Glide"
genre: crash / step-progression (real-money)
output_profile: obsidian_md
status: reverse-engineered
source: 逆向自已交付的 cg03a 前端 (crashgame-cg03a-ui) + .art-meta + 真实资产视觉审查
language: zh-CN
canvas: 1080x1920 (portrait mobile)
created: 2026-06-19
purpose: agent 训练素材 —— 喂回 auto-art 应能再次复现 cg03a 全套美术资产
---

# cg03a「Jeepney Glide」— Art & Audio 美术与音频文档（逆向）

> **本文档定位 / 分工**：三件套之一，只管**美术/音频资产本身**（题材风格、资产清单与规格、场景图/spine/特效/音频）。**界面布局/坐标/编排/状态机**见 [UI-GREYBOX-CG03A.html](UI-GREYBOX-CG03A.html)；**玩法规则/经济/网络状态**见 [GDD-CG03A.md](GDD-CG03A.md)。三份交叉引用、互不重复。
>
> **复现目标**：把本文档喂给 auto-art agent（DESIGN→GENERATE），应能再次产出与 `crashgame-cg03a-ui/cg03a/public/assets/` 一致的资产集。因此每个资产都给出 **target_path / 类型 / 尺寸 / 视觉层级(tier) / 材质&配色 / 状态(derive vs generate) / 可直接转 prompt 的描述**。
>
> **真实资产事实基线**：92 件 Figma 源 PNG（见 `.art-meta/dev_book.md`）→ 精简接线为 `public/assets/` 下约 60 张图 + 13 套 spine + 9 条音频。本文档以**实际落地的 `public/assets/` 结构**为准（dev_book 的 Figma 目录仅作设计意图补充）。
>
> **命名注记**：上线 Logo 字标实为 **"JEEPNEY GLIDE"**（`logo_*.png` 视觉确认）；`.art-meta/dev_book.md` 内部代号写作 "Jeepney Dash"，主背景吉普尼车身印 "DASH"。复现以 **"JEEPNEY GLIDE"** 为准，车身装饰文字可沿用 "DASH/MABUHAY/PILIPINAS" 等本地化贴字。

> ⚠️ **设计稿 ↔ 上线 差异速查（铁律：以 `public/assets` + 代码 runtime 为准，`.art-meta`/Figma 仅为设计意图）**
> 本作自带 Figma 设计交付包 `.art-meta/`（dev_book/manifest/nodes.json，源自 Figma 文件「William 专用」）。设计稿对**资产尺寸/题材/层级**高度可信（多处与上线 1:1，如 win-banner 517×320≈上线 516×320），但下列处**设计与上线已分叉，复现时按上线**：
>
> | 项 | `.art-meta` 设计稿 | 上线实际（采信） |
> |---|---|---|
> | 游戏名 | "Jeepney **Dash**"（车身印 DASH） | Logo 字标 "JEEPNEY **GLIDE**" / 简中"乘风吉普尼" |
> | 吉普尼 spine | "**1 套骨架** + car1-4 方向动画，勿建多骨架" | **4 套骨架**（`car_easy/medium/hard/hardcore`，按难度换皮），每套各含 car1-4 + car_crash |
> | 乘客 spine | 文档仅列 **chara1-4**（small/med/VIP-A/B） | 实际 **chara1-9**（9 套，按难度×3 档映射，见 §6.2）；bonus 协议 3 档 `small/medium/big`（RealSocket） |
> | 套现/继续 按钮文案 | "**PARA!**"（他加禄语"停！"）/ CONTINUE | runtime i18n：**CASHOUT / GO**（简中 套现/继续） |
> | 难度名 | Cubao Express / EDSA Rush / Manila Bay Drive / Quiapo Hardcore | 通用 **Easy / Medium / Hard / Hardcore**（无独立贴字） |
> | 快捷投注 | 设计 4 键 `[1,2,5,10]`（见 nodes.json） | 上线 **5 键 `[0.1,0.5,1,5,10]`**（截图实测，UI-GREYBOX 已采信） |
> | 终点大奖文案 | 居中文字 "You have won the Grand Prize!" | runtime：金标题"恭喜获得大奖!" + 霓虹框"你赢了 $金额"（截图实测） |
> | Logo 源图 | `logo 1` 1254×3802（巨幅设计源） | 上线 `logo_*.png` 已缩切（每语一张） |

---

## 1. Summary 摘要

**Jeepney Glide** 是一款**菲律宾吉普尼(jeepney)题材的 crash / 逐站递进**真金游戏（非老虎机）。核心循环：

```
[1] 下注 + 选路线(4 难度) → 点 PLAY
[2] 行驶循环：吉普尼沿蜿蜒公路逐站前进；途中乘客(pasahero)上车 → bonus 倍率叠加
            玩家随时抉择：CASHOUT(落袋) 或 GO(继续到下一站，风险更高)
[3] 结算：cashout 成功 / 撞车(crash, 归零) / 终点大奖(grand prize)
```

玩法形态对标 crash 品类（递进式风险曲线），题材本地化为**马尼拉/外省菲律宾公路风情**：吉普尼、海岛、夜市霓虹、节庆色。视觉语言双调性——**白天暖色乡村**（加载/easy）与**夜晚紫金霓虹都市**（主玩法 ambient）。

**4 条难度路线**（runtime 文案，无独立贴字，UI 文本叠加）：Easy / Medium / Hard / Hardcore（简中：简单/中等/困难/极难）。设计意图代号曾为 Cubao Express / EDSA Rush / Manila Bay Drive / Quiapo Hardcore（见 dev_book §6，未做成独立 PNG）。

---

## 2. 题材方向 / Style Bible（art-direction 锚点）

> 复现时 **Step 0** 先确立本 Style Bible 并 `set_style_bible`，全程所有 prompt 从此出发。

### 2.1 美学方向（一句话定位）
**"马尼拉吉普尼霓虹夜行 + 热带岛屿公路之旅"**——把菲律宾国民吉普尼的**手绘花车涂装**与**夜市霓虹灯管**作为签名元素；既有白天热带海岛的鲜亮手绘场景，又有夜晚都市的紫金霓虹 HUD。签名记忆点：**彩虹霓虹灯管描边的吉普尼车头徽标**。

### 2.2 配色系统（60-30-10）
来源：`public/assets/theme/theme.json`（runtime tint）+ 资产视觉提取。

| 角色 | 占比 | 取值 | 用途 |
|---|---|---|---|
| **dominant 主色（退后）** | ~60% | 深夜蓝黑 `#0A0E1A`~`#1A1230`、遮罩黑 `#000000@50%`、设置遮罩深蓝 `#112E60@85%` | 背景、面板内底、玩法夜色 |
| **chrome 中性（HUD）** | ~30% | 暗玻璃/暗金属 `#2A2A2A`/`#333333`、按钮底 `#444444`(hover `#666`,pressed `#333`) | 普通控件底、文字底 |
| **accent 强调（仅 CTA/中奖）** | ~10% | **金 `#FFB300`/`#FFD24D`**、**彩虹霓虹**(粉`#FF3BD4` 青`#3BD4FF` 紫`#9B5BFF` 绿`#27E07A`) | CTA、中奖、徽标、bonus |

文字：主 `#FFFFFF`、次 `#8899AA`、弱 `#667788`。字号：按钮 14、tab 52。

### 2.3 两套 chrome 材质族（**关键签名，复现必守**）
所有面板/按钮/框体材质二选一：

1. **多彩霓虹灯管族（festive neon）**——圆角矩形，**外缘是发光 RGB 霓虹管**（粉/青/紫/绿/金多色渐变），深navy磨砂内底 + 细微斜纹/星点。用于：bonus_panel、win banner、进度条、难度选择器弹层、玩法内 HUD 条。质感参考：马尼拉吉普尼车身霓虹 + 夜市招牌。
2. **金色斜切框族（premium gold）**——**八角切角（cut-corner）**的描金 bevel 厚框，暗金渐变内底 + 金色火花/星点 + 偶有紫色高光擦光。用于：start 按钮、selector_base、各类 premium 面板/横幅、station_sign、result 横幅。质感参考：高端 casino 金框。

> 语义色覆盖材质：**GO=绿色霓虹边**、**CASHOUT=金色边**、**win/bonus=彩虹霓虹**、普通 chrome=暗金属+单金描边。

### 2.4 场景美术风格
- **视角**：高角度俯视 / 轻等距（top-down-ish isometric），手绘插画质感（非写实照片，非扁平矢量）。
- **路径**：一条蜿蜒 **S 形公路**纵向贯穿，沿途密集填充菲律宾环境物（椰树、nipa 竹屋、sari-sari 杂货店、市集摊、townsfolk、bus stop 候车亭、海岸/都市）。
- **难度换皮**：**同一 S 弯路结构，按难度重绘主题皮**（结构/路宽/锚点一致，像素全换）：
  - easy = 热带海滩 + 乡村集市（暖色白天，蓝绿海）
  - medium / hard = 过渡（城镇→密集都市，渐入夜）
  - hardcore = 未来科技都市（青/白/金高科技，玻璃楼、全息招牌、运河）
- **隔离背景**：所有需抠图的 sprite 用 **纯品红 #FF00FF chroma-key**；全屏 bg/scene **不**用 chroma-key（full-bleed 直出）。

### 2.5 文字与特效不变量
- **不烧文字**：除 `logo`（每语言一张字标）外，所有 UI 一律 text-free，文案 runtime 叠加（PLAY/GO/CASHOUT/PARA!/难度名/金额/倍率全是 i18n 文本层）。
- **动态光效（发光/火花/烟花/烟雾）是独立 `effect` 资产**，不烧进按钮/面板；但**作为框体身份的静态霓虹管/金边可烧进该资产本身**（它是材质，非运行时特效）。

---

## 3. 资产按屏归组（哪些资产属于哪个屏）

竖版 1080×1920。**各屏的布局/坐标/状态机/切换见 [UI-GREYBOX-CG03A.html](UI-GREYBOX-CG03A.html)，本节只列资产归属。**

| 屏幕 | 主要资产组 |
|---|---|
| **Loading 加载** | bg、logo(×3语)、进度条(container+filled)、START 按钮、错误面板(currency-error/login-expired/error-panel + reload) |
| **Main Game 主玩法** | 滚动场景(scene-bg)、吉普尼 spine、乘客 spine、top-bar、difficulty_selector、bet-input、按钮组(GO/CASHOUT/PLAY/min/max/quickBet)、separator、bonus_panel、station_sign |
| **Result 结算** | win-banner(label + youWinText)、烟花、撞车烟雾 |
| **Difficulty Selector** | selector_base、icon_collapsed/expand、popup_background、popup_selected |
| **Settings 设置** | bottom-buttons、decorators、language-selector、image-quality toggle、sound-controll、back |
| **Error / Disconnect 弹窗** | error-panel/background + btn_reload、currency-error/panel、login-expired/panel |

> Guide 教程页文案 `public/assets/texts/how-to-play.md` 当前为**占位模板（未填）**；复现时按 §1 玩法循环补写。

---

## 4. 逐资产清单（**复现核心** —— target_path / 类型 / 尺寸 / tier / mode / origin / 描述）

> 字段含义：`type`=资产类型；`tier`=视觉层级(hero/featured/support/chrome/bg/fx)；`mode`=`regen`(抠图 sprite)/`full_bleed`(满屏)/`sheet`；`origin`=`generate`(原创)/`derive`(代码派生)。**路径即 target_path**，复现时原样写回 `public/assets/<path>`。

### 4.1 loading/（加载页）
| target_path | type | dims | tier | mode | origin | 描述（prompt 锚点） |
|---|---|---|---|---|---|---|
| `loading/game-view/background.jpg` | bg | 1080×1920 | bg | full_bleed | generate | 黄金时刻菲律宾乡村：彩绘吉普尼(车身"PILIPINAS/MABUHAY")停靠 BUS STOP，两名乘客，椰树、热带花、湿地反光、菲律宾太阳徽、夕阳橙紫天。暖色饱和手绘。 |
| `loading/game-title-logo/logo_en.png` | logo | 584×330 | hero | regen | generate | 字标 "JEEPNEY GLIDE"：金色立体斜面字 + 蓝色 "GLIDE" 副条；深色八角盾徽底，双椰树 + 3 颗金星(菲国旗意象) + 中央小皇冠/吉普尼徽，彩虹霓虹描边。 |
| `loading/game-title-logo/logo_zh_cn.png` | logo | 584×269 | hero | regen | generate | 简中字标 **"乘风吉普尼"**（金"乘风"+蓝"吉普尼"，同八角盾徽）。 |
| `loading/game-title-logo/logo_zh_tw.png` | logo | 584×262 | hero | regen | generate | 同上，繁中字标变体。 |
| `loading/progress-bar/progress_bar_container.png` | bar(container) | 1424×236 | featured | regen | generate | 八角切角金框空轨道，暗金内底 + 多彩星点。固定宽不拉伸。 |
| `loading/progress-bar/progress_bar_filled.png` | bar(filled) | 1311×114 | featured | regen | generate | 单条左锚点可横向拉伸的渐变填充条（金→亮金 能量感）。 |
| `loading/start-button/btn_gamestart_idle.png` | button | 1200×336 | featured | regen | generate | 八角切角金 bevel 宽按钮，暗金渐变面 + 火花 + 紫光擦光；text-free（START 叠字）。hover/pressed=derive。 |
| `loading/error-panel/background.png` | panel | 974×536 | support | regen | generate | 通用错误面板底：暗紫 + 金框，空内。 |
| `loading/error-panel/btn_reload_idle.png` | button | 390×120 | chrome | regen | generate | reload 按钮 idle，text-free。 |
| `loading/currency-error/panel.png` | panel | 878×260 | support | regen | generate | 货币错误窄面板。 |
| `loading/login-expired/panel.png` | panel | 878×206 | support | regen | generate | 登录过期窄面板。 |

### 4.2 content-view/（顶栏 + 结算横幅）
| target_path | type | dims | tier | mode | origin | 描述 |
|---|---|---|---|---|---|---|
| `content-view/top-bar/background.png` | panel | 1080×130 | chrome | regen | generate | 顶栏底：**浮动金框深色余额胶囊**（非不透明横条，路面透到最顶被它盖住）。 |
| `content-view/top-bar/icon_currency_symbol.png` | icon | 64×64 | chrome | regen | generate | **金色五角星金币**（货币图标；亦用于快捷投注/赢分金额内联）。 |
| `content-view/top-bar/icon_settings.png` | icon | 72×72 | chrome | regen | generate | 设置齿轮图标。 |
| `content-view/game-view/win-banner/label_youWinBanner.png` | fx/hero word | 516×320 | hero | regen | generate | YOU WIN 横幅：顶部彩虹霓虹吉普尼车头徽 + 下方彩虹霓虹管圆角框(承载金额)。signature 霓虹件。 |
| `content-view/game-view/win-banner/youWinText.png` | logo/word-art | 260×48 | featured | regen | generate | YOU WIN 艺术字，**按 locale 烧字**（简中="你赢了"）；坐于 win 横幅内、金额上方。 |

### 4.3 main-game/（玩法区 —— 详见 §5 场景系统）
| target_path | type | dims | tier | mode | origin | 描述 |
|---|---|---|---|---|---|---|
| `main-game/scene-bg/<diff>/start.jpg` | scene | **easy 1080×450 / 其余 1080×900** | bg | full_bleed | generate | 起步段：路面绘 START + 棋格旗；难度主题皮(easy=海滩)。**仅 easy 为短段(450)**，medium/hard/hardcore 同 middle 高(900)。 |
| `main-game/scene-bg/<diff>/middle.jpg` | scene | 1080×900 | bg | full_bleed | generate | 中段(bulk)：沿移动轴**无缝循环**主体路段，密集环境物。 |
| `main-game/scene-bg/<diff>/end.jpg` | scene | 1080×900 | bg | full_bleed | generate | 终点段：升旗/终点(grand prize 触发点)。 |
| `main-game/scene-bg/station_sign.png` | icon/panel | 290×100（运行渲染 235×81） | support | regen | generate | 站点倍率牌：深蓝底 + 金框 + 金火花，text-free（叠 x_k）。**沿路两块一左一右、对侧镜像**；下注态预览赔率梯（随难度递增 easy 1.01–1.04→hardcore 1.07–1.18）。定位见 UI-GREYBOX 画廊 B。 |
| `main-game/scene-bg/centerline.json` | data | — | — | — | data | 路径锚点数据（非图片，见 §5.2）。 |
| `main-game/game-view/bonus_panel.png` | panel | 570×192（运行渲染 340×114） | featured | regen | generate | 累计 bonus 面板：多彩霓虹管圆角框 + 深navy内底，text-free。右下角，cumBonus>0 显。位置/行为见 UI-GREYBOX 飞行态帧。 |

`<diff>` ∈ {easy, medium, hard, hardcore}，共 4×3=12 张 scene jpg。

### 4.4 player-hud/（玩法 HUD 控件）
| target_path | type | dims | tier | mode | origin | 描述 |
|---|---|---|---|---|---|---|
| `player-hud/buttons/btn_go_idle.png` | button | 460×381 | featured | regen | generate | **GO 按钮：绿色霓虹边**圆角厚板，暗绿发光内底 + 磨砂金属 + 星点。text-free。 |
| `player-hud/buttons/btn_cashout_idle.png` | button | 460×381 | featured | regen | generate | **CASHOUT 按钮：金色霓虹边**圆角厚板，暗琥珀内底。与 GO **语义切换共存**（两件 generate，前端原地切）。 |
| `player-hud/buttons/btn_play_idle.png` | button | 800×168 | featured | regen | generate | 下注页 PLAY 主按钮，**紫色金框宽板**（截图确认；代码注释"green"是 cg03r 旧皮残留），text-free。 |
| `player-hud/buttons/btn_minAdjust_idle.png` | button | 174×141 | chrome | regen | generate | 减注按钮 idle。 |
| `player-hud/buttons/btn_maxAdjust_idle.png` | button | 174×141 | chrome | regen | generate | 加注按钮 idle（与 min 可水平镜像派生关系，但此处各一件）。 |
| `player-hud/buttons/btn_quickBetAmount_idle.png` | button | 220×126 | chrome | regen | generate | 快捷投注额按钮 idle：**紫色渐变 + 金框**，内含金值 + 星币（一行 5 个 0.1/0.5/1/5/10）。 |
| `player-hud/bet-input/bet_amount_input_container.png` | panel | 826×122 | chrome | regen | generate | 投注额输入容器，空内。 |
| `player-hud/difficulty_selector/selector_base.png` | panel | 993×122 | support | regen | generate | 难度选择器底：八角切角金框横条，空内（难度名叠字）。 |
| `player-hud/difficulty_selector/icon_collapsed.png` | icon | 78×43 | chrome | regen | generate | 收起箭头图标。 |
| `player-hud/difficulty_selector/icon_expand.png` | icon | 78×43 | chrome | regen | generate | 展开箭头图标。 |
| `player-hud/difficulty_selector/popup_background.png` | panel | 1000×484 | support | regen | generate | 难度弹层底（多彩霓虹族）。 |
| `player-hud/difficulty_selector/popup_selected.png` | panel | 940×106 | support | regen | generate | 弹层内选中行高亮底。 |
| `player-hud/separator/separator_line.png` | bar | 1080×16 | chrome | regen | generate | 通用分隔线。 |

> **按钮状态规则**：仅交付 `_idle` 原件；hover(+10~15%亮)/pressed(-10~20%)/disabled(去饱和+降透明)=**code-derive，不生成**。GO↔CASHOUT、min↔max 是**语义/镜像**关系，按需各自 generate 或 flip-derive（见 asset-types 控件态表）。

### 4.5 settings-panel/（设置二级菜单）
复用原型（跨游戏结构近似，换皮）。主要件：

| target_path | type | dims | origin | 备注 |
|---|---|---|---|---|
| `settings-panel/bottom-buttons/btn_{settings,guide,history,exit}.png` | icon | 72×72 | generate | 底部导航图标（tab）。 |
| `settings-panel/bottom-buttons/btn_back.png` | button | 140×140 | generate | 返回按钮。 |
| `settings-panel/bottom-buttons/btn-hover.png` | fx | 216×168 | derive/overlay | 通用 hover overlay。 |
| `settings-panel/bottom-buttons/buttons-container.png` | panel | 1080×180 | generate | 底栏容器（**<1KB，疑似占位/极简，复现需确认**）。 |
| `settings-panel/decorators/{header,decor-section-header,decor-section-divider,header-decor-left,header-decor-right}.png` | decor | 见尺寸表 | generate | 装饰件(header/分隔/左右角饰)；部分 <1KB 疑似占位。 |
| `settings-panel/language-selector/icon_selector.png` | icon | 80×80 | generate | 语言选择图标。 |
| `settings-panel/language-selector/language-selector-popup-panel.png` | panel | 800×960 | generate | 语言弹层面板。 |
| `settings-panel/language-selector/{language_switcher_container,option_eng,option_tr,option_zh}.png` | panel/button | — | generate | 语言行容器 + 3 选项（**均 <1KB，疑似占位，复现需重出**；选项数=locale 数）。 |
| `settings-panel/image-quality/toggle_{on,off}.png` | toggle | 63×63 | generate | 画质开关 on/off（**各态独立资产**，前端交叉淡入；toggle_on <1KB 疑似占位）。 |
| `settings-panel/game-history/date-range-btn-{idle,hover}.png` | button | 314×100 | idle=generate, hover=derive | 日期范围按钮 2 态。 |
| `settings-panel/game-history/icon_copy.png` | icon | 28×28 | generate | 复制图标（共享）。 |
| `settings-panel/sound-controll/{icon_mute,hover_overlay_active,hover_overlay_idle}.png` | icon/fx | — | generate | 声音控制 base + on/off 派生。 |

> ⚠️ **占位提醒**：`images/placeholder.png`(1×1) 及上表 **<1KB** 的若干 settings 件是占位/极简 stub，**复现时应按真实结构重新生成**，不要照抄空文件。
>
> 🗑 **孤儿 / 未部署（源码穷尽抽取所得，复现可忽略）**：`scene_packs/_layouts.json`（grep 全 src 无引用，Figma 期产物）；`SpriteDigits.ts` 基础设施存在但 **digit 切图未部署 → 所有数字走 runtime 样式化 Text**（余额/金额/倍率/派彩皆然，不必出 digit-strip 资产）。设置 tab 图标别名↔路径：`tab_icon_setting/guide/history/exit` ↔ `settings-panel/bottom-buttons/btn_*.png`、back ↔ `btn_back.png`。
>
> ✅ **更正（实测 atlas）**：`spine/chara9/chara9_2.webp` **不是孤儿**——它是 `chara9.atlas` 的**第 2 张图集页**（page1 `chara9.webp` 1555² 含 region chara9-1/2/5/6；page2 `chara9_2.webp` 1415² 含 chara9-0/3/4）。chara9 是**双页图集**，两张都要出。

### 4.6 effects/（特效 —— 独立 fx 资产）
| target_path | type | dims | mode | 描述 |
|---|---|---|---|---|
| `effects/crash-smoke/smoke.webp` | effect | 864×864 | single | 撞车烟雾（单一烟团）。 |
| `effects/fireworks/firework{1,2,3}.png`(+`.json`) | effect | 1141×759 / 658×817 / 256×256 | single+atlas | 大奖烟花（各带 json，可能为粒子/帧数据）。 |
| `effects/pixelDot.png` / `pixelexplode.png` / `trail.png` | effect | 512×512 / 256×256 / 256×256 | single | 粒子贴图（点/爆裂/拖尾）。 |

> 全部 fx 为**单一隔离元素**（非 contact-sheet），运行时由前端合成/粒子系统驱动。

---

## 5. 场景系统 —— 要产出的图 & 数据契约

> **运行机制**（scrollY 滚动、车姿 car1–4 选择、站牌定位/镜像、boarding 过场、难度黑幕淡切、终点演出）见 [UI-GREYBOX-CG03A.html](UI-GREYBOX-CG03A.html) 画廊 B + 机制注释；**玩法含义**（每 hop=进站=赔率台阶）见 [GDD-CG03A.md](GDD-CG03A.md)。本节只交付**美术要产出什么**。

### 5.1 每难度三段（资产契约）
玩法区是纵向滚动公路，每难度一套 3 段，沿移动轴(向上滚)拼接，**同结构换主题皮**（style-regen 重绘，非 tint；路宽/走向跨难度一致）：

| 段 | easy | medium/hard/hardcore | 说明 |
|---|---|---|---|
| start 起步段 | 1080×450 | 1080×900 | 路面绘 START + 棋格旗 |
| middle 中段(bulk) | 1080×900 | 1080×900 | **沿移动轴无缝循环**，按里程重复 N 次 |
| end 终点段 | 1080×900 | 1080×900 | 升旗 / grand-prize 触发点 |

主题皮：easy=热带海滩/乡村集市(白天) → medium/hard=城镇渐入夜 → hardcore=未来科技城(青金)。

### 5.2 centerline.json（路径数据，随场景配套产出）
```json
{"source":".../road_simple.png","width":1080,"height":900,"stepY":2,"alphaThresh":32,
 "anchors":[{"iy":0,"ix":819.5},{"iy":2,"ix":819}, … 共~450 个]}
```
每隔 `stepY=2` px 记录该行路面中心线 X(`ix`)，描出 S 弯。**复现：scene 出图后扫描路面 alpha 导出此文件**，作为平铺契约一部分（车/站牌据它定位——用法见 UI-GREYBOX 画廊 B）。

---

## 6. Spine 骨骼动画（动效源）

> v1 静态源 = 代表性 webp 贴图（spine 图集）；骨骼绑定/播放是动效/前端的事。每套 = `*.json`(骨架) + `*.atlas`(图集索引) + `*.webp`(贴图)。

### 6.1 吉普尼车 `spine/car_<diff>/`（4 套，**一套骨架 5 动画**）
- 文件：`car.json` / `car.atlas` / `car.webp`(~900×900)。
- **动画**（实测 `car.json`）：`car1`(水平段) / `car2`(斜向段) / `car3`(垂直段, 旋转90°) / `car4`(反斜段) / **`car_crash`**(撞车)。`skins: [default]`，8 slot(4 车向 + 4 影)。
- **语义**：**ONE 吉普尼骨架，按路径切线方向切换 car1-4**，撞车播 car_crash——**不是 4 台不同的车，不实例化多骨架**。
- **per-difficulty 皮**：4 个 car_<diff> 是**共享骨架、按场景主题重绘的皮**（easy 彩绘花车 → hardcore 科技皮），style-regen。
- **视觉**：鲜艳菲律宾彩绘吉普尼，车身满布黄/青/紫/粉几何花纹与图腾，多面切割高光。

### 6.2 乘客 `spine/chara1..9/`（9 套，**idle/walk**）
- 文件：`charaN.json/.atlas/.webp`(926×926~1555×1555 不等)；动画：`idle` / `walk`。
- **分级映射**（`GameplayFlyingAssets.ts:89 CHARA_BY_DIFFICULTY`；注释 line 30）：

| 难度 | small bonus | medium bonus | big bonus |
|---|---|---|---|
| easy | chara1 | chara2 | chara3 |
| medium | chara1 | chara2 | chara3 |
| hard | chara4 | chara5 | chara6 |
| hardcore | chara7 | chara8 | chara9 |

- bonus 档（加到累计 bonus，cap +2.0）：真服务端 ≈ small **+0.1** / medium **+0.3** / big **+0.5**（截图累计 +30~80% + 原版 cg03r 印证；dev mock 占位 +0.20/+0.50/+1.50，勿作真值）。派彩 ×(1+累计bonus)。经济细节见 [GDD-CG03A.md](GDD-CG03A.md) §5。
- **视觉**：夸张插画人物，档位越高越"豪"——big 档=雪茄 + 紫金豹纹西装 + 金链珠宝的 VIP（chara3/6/9）；小档为普通市民乘客。
- 触发：bonus 上车演出(boarding cut-in)，spawn 播 idle → boarding 播 walk。

---

## 7. 音效与 BGM

> 接线见 `src/game/project/SoundDefs.ts` + `MainSceneManifest.ts`；共 1 BGM + 8 SFX（`public/assets/audio/`）。响度建议：SFX -16 LUFS / BGM -19 LUFS，TP -1.5。

### 7.1 BGM
| 文件 | 场景 | loop | 时长 | 描述 |
|---|---|---|---|---|
| `audio/bgm/bgm.mp3` | 主玩法(MainScene 进入即播) | ✓ 循环 | 60~120s | 菲律宾节庆调性主循环（建议本土乐器：班杜里亚/打击乐 + 轻快律动），与吉普尼公路之旅气氛一致。 |

### 7.2 SFX（触发取自代码）
| 文件 | 触发事件 | loop | 时长 | 描述 |
|---|---|---|---|---|
| `audio/sfx/click.mp3` | 所有 UI 按钮点击 | one-shot | 0.1~0.3s | 短促清脆 UI 反馈。 |
| `audio/sfx/inserting_coin.mp3` | 开局发车（fly 启动，ANIM_DEPART） | one-shot | 0.5~1.0s | 投币/发车音。 |
| `audio/sfx/drive_to_next_stop.mp3` | 每段 hop drive 启动（ANIM_HOP_START） | one-shot | 0.8~1.5s | 引擎加速/前进音。 |
| `audio/sfx/car_crashed.mp3` | 撞车归零（ANIM_CRASH_IMPACT） | one-shot | 0.8~1.5s | 撞击/急刹 + 失败感。 |
| `audio/sfx/win.mp3` | CASHOUT 结算 / win 横幅弹出（ANIM_CASHOUT_SHOW） | one-shot | 1.0~2.0s | 中奖/落袋庆祝音。 |
| `audio/sfx/bonus_1.mp3` | small bonus 乘客上车(chara1/4/7) | one-shot | 0.8~1.5s | 轻量正反馈 + 上车音。 |
| `audio/sfx/bonus_2.mp3` | medium bonus 乘客(chara2/5/8) | one-shot | 0.8~1.5s | 中等正反馈(更强)。 |
| `audio/sfx/bonus_3.mp3` | big bonus 乘客/VIP(chara3/6/9) | one-shot | 1.0~2.0s | 强正反馈 + 高级感(VIP 登场)。 |

> 缺口（复现可补，非现有）：终点 grand-prize 专属音、烟花音、站点经过音目前复用上述集合。

---

## 8. 多语言美术适配

- **支持 3 语**：en（英）、zh_cn（简中）、tr=zh_tw（繁中，键名 `tr`）。本地化文件 `src/assets/localizations/{en,zh,tr}.json`。
- **唯一按语言烧字的资产 = logo**：`logo_en/zh_cn/zh_tw.png` 三张真原件；`Background.tsx` 按 `useLocalization().t('background.title.file-name')` 取对应文件。
- **其余全部 runtime 文本叠加**：难度名(Easy/Medium/Hard/Hardcore↔简单/中等/困难/极难)、设置 tab(Back/Setting/Guide/History/Exit)、PLAY/GO/CASHOUT、金额、倍率、错误文案——容器需对长度差留弹性。
- 复现：logo 每 locale 一张(generate)，UI 框体一律 text-free。

---

## 9. 复现说明（喂回 agent 的用法）

1. **Step 0**：用 §2 Style Bible `set_style_bible`（双材质族 + 60-30-10 + 难度换皮规则 + 品红 chroma-key + 不烧字）。
2. **DESIGN**：用 §3 屏幕清单 + §4 逐资产表生成 design.json——每资产落 `target_path / asset_type / mode / origin / tier / dims`；scene 按 §5 三段 + centerline 平铺契约；spine 按 §6（一车一骨架多动画，难度皮共享骨架）。
3. **GENERATE**：按 art-direction prompt-loop 逐件出图；scene full_bleed 直出，sprite 走品红 chroma-key + clean_cutout；按钮仅出 idle，hover/pressed/disabled 派生；GO/CASHOUT、toggle on/off、tab active/inactive 各自 generate。
4. **校验**：对照本表 `dims` 与 `public/assets/` 实际尺寸；对照 §6 `CHARA_BY_DIFFICULTY` 与 car 动画名；占位件(§4.5 ⚠️)需真出。

---

## 10. Non-Goals 美术不做

- 不做横版独立资产（竖版优先）。
- 不做老虎机符号/转轴（本作是 crash，非 slot）。
- 不照搬占位/空 stub 文件（须重出）。
- v1 不交付已播动画（只出 spine 静态源 + 帧/特效源），骨骼绑定/粒子播放归动效/前端。

---

## 11. Sources 信源
- `crashgame-cg03a-ui/cg03a/public/assets/**`（真实资产 + 尺寸视觉审查）
- `cg03a/.art-meta/{dev_book,manifest,decisions,rename_map,qc_summary,delivery_report}.{md,json}`（设计意图 + Figma 源目录 + 派生关系）
- `cg03a/src/game/project/{SoundDefs.ts, scenes/MainScene/MainSceneManifest.ts, .../GameplayFlyingAssets.ts}`（接线/触发/分级映射）
- `cg03a/public/assets/main-game/scene-bg/centerline.json`、`scene_packs/_layouts.json`（场景平铺/路径）
- `cg03a/src/assets/localizations/{en,zh,tr}.json`、`public/assets/theme/theme.json`（i18n + 配色）

---

**ADD 结束（逆向版）。本文档为 agent 训练素材：喂回 auto-art 应能复现 cg03a「Jeepney Glide」全套美术与音频资产。**
