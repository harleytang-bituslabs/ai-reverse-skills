# ART-AUDIO-SS02 · Beach Party(沙滩派对)美术与音频设计文档(ADD)

> **版本锚定**:Unity 构建 `1.0.0-71`(CDN `dev-assets-hybergaming/ss02`,2026-07-08 复核一致)。
> **信源**:UnityPy 全量导出(data.unity3d + 31 个 Addressables 功能/本地化 bundle)后**亲自查看**归纳;尺寸=真实像素,时长=AudioClip 元数据。零截图形态,徽标止于 extracted/derived。
> **定位**:设计文档 + **主体资产清单**(§8 分子表,族行折叠);逐物理文件(756 件)在 `elements-SS02.json.assets`。玩法/数学 → `GDD-SS02.md`;屏坐标 → `UI-GREYBOX-SS02.html`。

## 0. Style Bible

- **一句话美学**:霓虹灯牌下的夜派对海滩——糖果玻璃质感的度假小物在木板舞台上起舞,白日海滩(base)与紫夜派对(free)双场景。
- **60-30-10 配色**:60% 湖蓝-青(海面/天空/格网底);30% 糖果粉紫+奶油白(符号/气球/霓虹);10% 暖木+彩灯点缀(舞台框/灯串/旗串)。
- **材质族**:糖果玻璃(符号,高光+果冻透感)、霓虹灯管(Scatter/庆祝小物/BuyFeature 跑马灯)、原木+彩灯(Frame_Fence 舞台框)、气球乳胶(乘数)、水彩天幕(背景)。
- **不变量**:符号=Spine 动画资产(骨骼+图集,非静态帧);文字不烧图,例外=多语言文字图(win 标题/Title_Text/宿主 loading 标题);特效独立;运行时数值占位。

## 1. 符号集设计(Spine;上屏 cell 168×168,6×5 规整网格)

9 常规符号按赔付降序成两族:**交通工具**(游艇/水上飞机/皮划艇=高赔)与**冷饮水果**(圣代/甜筒/冰棍/芒果/西瓜/蓝莓=中低赔);每符号一套 Spine(`<字母>_<名>.skel/.atlas`)+ 整体渲染图(`Symbol_N_*`)+ 三色圆角底板(`Symbol_1/2/3_Bg` 棕/红/绿霓虹描边,按赔层)。
- **SCATTER=霓虹摩天轮**(`SCATTER` + `2025_0717_SCATTER_ANIMATION` 新版动画,方形霓虹框底)。
- **乘数气球**:红色双气球白字 X2-X100 八档,Spine `MULTIPLIER_X*` + 静态 `Symbol_Wild_X*`(**命名陷阱:机制是乘数,不是替代 Wild**)。

## 2. 场景分层与双模式皮

- 全屏背景横版全幅:`Background_Normal`(白日海滩/泳圈/椰影)/ `Background_FreeSpin`(紫夜海星沙滩)——竖屏裁切两翼。
- 牌网底 `Frame_Bg`(青色 6×5 格网)/ `Frame_Bg_FreeSpin` 变体;**`Frame_Fence` 木质舞台框**(顶梁彩灯串+木柱+底台)围住牌网。
- 场景装饰:Base=蓝三角旗串四角(**资产名 Left/Right 与实际位置镜像互换**,复现按位置);Free=彩旗+彩灯串+霓虹灯饰(皇冠/星星/"Let's party" 鸡尾酒灯牌)。
- 设置页背景独立双朝向(`Setting_Background(_Vertical)` 暮色椰影)。

## 3. 玩法 → 美术适配

| 玩法机制(GDD) | 美术落地 |
|---|---|
| 8+ 任意位置中奖+级联(§3) | 符号格 prefab 内 `explose effect` 爆裂消除;confetti/stars and trails/smoke 粒子;补位下落即 Spine 待机 |
| 乘数气球(§4) | 免费限定:红双气球 Spine 落轮,X2-X100 白字;结算入 `BillDetail_MultiplierLine`(Total Multiplier) |
| Scatter 触发(§5) | 摩天轮霓虹 Spine;2025_0717 新版动画;触发后 `FreeSpinNoticer`:彩色气球群(balloon_0-11)+“You Have Won N Free Spins”+START 钮 |
| 免费模式切换(§5) | 场景整套换皮:紫夜背景+彩灯旗串+霓虹灯饰+`Character_FemaleFull_FreeSpin`(沙滩女郎立绘换装 FreeGirl);Director_CurtainIn/Out 幕布过场 |
| 购买功能(§6) | `BuyFeature_Background`(紫底灯泡跑马灯框)+ `BuyFeature_Popup_*` 弹层与按钮;面板挂 ScreenBoard |
| Win 四级庆祝(§7 结算) | **BIG WIN(蓝)→ MEGA WIN(绿,六芒星霓虹 32 帧序列)→ SUPER WIN(橙,太阳+木板)→ EPIC WIN(粉,火烈鸟/樱桃/吉他霓虹)**+钞票飞散序列+YOU WON |
| 入场(§7 回合流) | `gameplay_introanim`:海滩全景 `Background_Loading`+海鸥 16 帧+云/棕榈/遮阳伞/冲浪板/沙滩椅+CONGRATULATIONS+**START GAME 胶囊钮三态**,Timeline 编排 |
| 角色氛围 | `Character_FemaleFull_Normal/FreeSpin`(BaseGirl/FreeGirl Spine 白裙女郎),站位世界层 |

## 4. UI chrome 设计要点

- **HUD**:水泡玻璃拟物——Play 主钮=大水泡(Hover/Normal/Pressed 三态)+Common 小水泡;灰蓝毛玻璃 ButtonPanel 底板(Top/Bottom/ExtraLine);胶囊 Panel(BetAmount/SpeedLevel 双点/Wallet);Title_Panel 橙金椭圆;icon 白线族(齿轮/循环/钱袋/筹码/闪电/手势)。双朝向孪生布局(横屏按钮横排右置 PlayButton,竖屏居中)。
- **菜单/历史**:TabList 五键;`Setting_Tab` 三态双朝向;History 日期 tab 三态;BetItem 行 Normal/Win(橙)双朝向+**Boost 金标**(激励局);BillDetail 双朝向+翻页钮。
- **弹窗**:Toast/Warning 深蓝面板+描边;`WarningPopup_ConfirmButton` 双态;LanguageSelector 面板。
- **Guide 长纸**(972 宽):`Guide_PaperBackground`+分区线;**`Setting_Guide_SymbolValue`(1022×498)=9 符号×三档赔付一图**(GDD §2 之源)。

## 5. 音频设计(31 clips;全清单在 elements)

- 双 bundle 分包:`gameplay_basegame_audiopack` / `gameplay_freegame_audiopack`(base/free BGM 与场景音分离加载)。
- 触发族(资产名+包归属推定 derived,时长 extracted):点击/落轮/消除爆裂/级联下落/scatter 现身/免费开场结算/乘数气球/win 分级/金币计数——逐条见 elements assets(audio 31 行)。

## 6. i18n 策略

string-tables 6 语言(en/zh-hans/zh-hant/id/km/vi;en 表 95 条含全部规则);文字图仅 hans/hant/shared(`Title_Text_En/Zh` ×2 尺寸);宿主 loading 标题 3 资产(En/SimpChinese/TradChinese);其余文字走 TMP(AlibabaPuHuiTi+Sans 系字体图集 4 套)。

## 7. 宿主壳美术(S3 `ui-assets`,middleware 宿主)

loading 四件(Track/Bar/Tip/**Bubble 气泡粒子**)、`loadingBg_large.png` 2560² 虚拟画布、三语言标题图、Notice 面板套件(Maintenance 用 NoticeMessageContainer;NoticePanel/Button 为未接线 ConfirmModal 死码)。几何与换算式见灰盒 §①⑥。

## 8. 主体资产清单(逻辑资产 246 行 / 756 件,分 8 子表)

> 行=逻辑主体资产;序列帧/图集页/多语言/同名双导出折叠为族行(说明注 ×N 件);逐物理文件见 `elements-SS02.json.assets`。

### 8.1 符号集(27 行 / 85 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| SCATTER 新版动画图集页 | 图 | 1024x1024 | 符号·Scatter | 牌网 | 摩天轮 |
| A_YACHT | 图 | 512x512 | 符号 | 牌网 | Spine 图集/整体渲染 |
| B_SEAPLANE | 图 | 512x512 | 符号 | 牌网 | Spine 图集/整体渲染 |
| C_RAFT | 图 | 1024x1024 | 符号 | 牌网 | Spine 图集/整体渲染 |
| D_SUNDAE | 图 | 512x512 | 符号 | 牌网 | Spine 图集/整体渲染 |
| E_CONE | 图 | 256x256 | 符号 | 牌网 | Spine 图集/整体渲染 |
| F_POPSICLE | 图 | 256x256 | 符号 | 牌网 | Spine 图集/整体渲染 |
| G_MANGO | 图 | 512x512 | 符号 | 牌网 | Spine 图集/整体渲染 |
| H_WATERMELON | 图 | 256x256 | 符号 | 牌网 | Spine 图集/整体渲染 |
| J_BLUEBERRY | 图 | 256x256 | 符号 | 牌网 | Spine 图集/整体渲染 |
| 乘数气球 Spine 图集页(X2-X100) | 图 | 256x256 | 符号·乘数 | 牌网(免费) | ×8件 |
| SCATTER 摩天轮 Spine 图集页 | 图 | 512x512(等2种) | 符号·Scatter | 牌网 | 摩天轮×14件 |
| SCATTER | 图 | 1024x1024 | 符号·Scatter | 牌网 | 摩天轮 |
| Symbol_1_A_YACHT_02 | 图 | 336x336(等2种) | 符号 | 牌网 | Spine 图集/整体渲染×4件 |
| Symbol_1_Bg | 图 | 168x168 | 符号 | 牌网 | Spine 图集/整体渲染×2件 |
| Symbol_2_B_SEAPLANE | 图 | 336x336(等2种) | 符号 | 牌网 | Spine 图集/整体渲染×4件 |
| Symbol_2_Bg | 图 | 168x168 | 符号 | 牌网 | Spine 图集/整体渲染×2件 |
| Symbol_3_Bg | 图 | 168x168 | 符号 | 牌网 | Spine 图集/整体渲染×2件 |
| Symbol_3_C_RAFT_1 | 图 | 336x336(等2种) | 符号 | 牌网 | Spine 图集/整体渲染×2件 |
| Symbol_4_D_SUNDAE_1 | 图 | 336x336(等2种) | 符号 | 牌网 | Spine 图集/整体渲染×2件 |
| Symbol_5_E_CONE_1 | 图 | 336x336(等2种) | 符号 | 牌网 | Spine 图集/整体渲染×2件 |
| Symbol_6_F_POPSICLE_1 | 图 | 336x336(等2种) | 符号 | 牌网 | Spine 图集/整体渲染×2件 |
| Symbol_7_G_MANGO_1 | 图 | 336x336(等2种) | 符号 | 牌网 | Spine 图集/整体渲染×2件 |
| Symbol_8_H_WATERMELON_1 | 图 | 336x336(等2种) | 符号 | 牌网 | Spine 图集/整体渲染×2件 |
| Symbol_9_J_BLUEBERRY_1 | 图 | 336x336(等2种) | 符号 | 牌网 | Spine 图集/整体渲染×2件 |
| Symbol_SCATTER | 图 | 336x336 | 符号·Scatter | 牌网 | 摩天轮×4件 |
| 乘数气球静态渲染(Symbol_Wild_X2-X100) | 图 | 336x336(等4种) | 符号·乘数 | 牌网(免费) | ×20件 |

### 8.2 场景与框架(24 行 / 48 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| Background_FreeSpin | 图 | 2048x2048 | 场景/框架 | 世界板/面板 | ×2件 |
| Background_Normal | 图 | 2048x2048 | 场景/框架 | 世界板/面板 | ×4件 |
| BaseGame_Strip_LeftMIddle | 图 | 728x262 | 场景装饰 | 四角/围栏 | ×2件 |
| BaseGame_Strip_LeftUp | 图 | 768x308 | 场景装饰 | 四角/围栏 | ×4件 |
| BaseGame_Strip_RIghtMiddle | 图 | 740x304 | 场景装饰 | 四角/围栏 | ×2件 |
| BaseGame_Strip_RightUp | 图 | 768x308 | 场景装饰 | 四角/围栏 | ×4件 |
| BaseGame_Strip_Straight | 图 | 1242x84 | 场景装饰 | 四角/围栏 | ×2件 |
| BuyFeature_Background_0 | 图 | 272x180 | 场景/框架 | 世界板/面板 |  |
| BuyFeature_Background | 图 | 272x180 | 场景/框架 | 世界板/面板 |  |
| BuyFeature_Off_0 | 图 | 92x36 | 场景/框架 | 世界板/面板 |  |
| BuyFeature_Off | 图 | 92x36 | 场景/框架 | 世界板/面板 |  |
| BuyFeature_On_0 | 图 | 92x36 | 场景/框架 | 世界板/面板 |  |
| BuyFeature_On | 图 | 92x36 | 场景/框架 | 世界板/面板 |  |
| BuyFeature_Popup_Background_0 | 图 | 518x376 | 场景/框架 | 世界板/面板 |  |
| BuyFeature_Popup_Background | 图 | 518x376 | 场景/框架 | 世界板/面板 |  |
| BuyFeature_Popup_BuyButton_0 | 图 | 328x98 | 场景/框架 | 世界板/面板 |  |
| BuyFeature_Popup_BuyButton | 图 | 330x103 | 场景/框架 | 世界板/面板 |  |
| BuyFeature_Popup_CloseButton_0 | 图 | 82x82 | 场景/框架 | 世界板/面板 |  |
| BuyFeature_Popup_CloseButton | 图 | 82x82 | 场景/框架 | 世界板/面板 |  |
| Frame_Bg | 图 | 512x426 | 场景/框架 | 世界板/面板 | ×4件 |
| Frame_Bg_FreeSpin | 图 | 512x426 | 场景/框架 | 世界板/面板 | ×2件 |
| Frame_Fence | 图 | 1024x1024(等2种) | 场景/框架 | 世界板/面板 | ×2件 |
| Setting_Background | 图 | 1024x576 | 场景/框架 | 世界板/面板 | ×4件 |
| Setting_Background_Vertical | 图 | 576x1024 | 场景/框架 | 世界板/面板 | ×4件 |

### 8.3 HUD(35 行 / 74 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| ButtonPanel_Common_Hover | 图 | 136x136(等2种) | HUD | PlayerHUD | ×2件 |
| ButtonPanel_Common_Normal | 图 | 136x136(等2种) | HUD | PlayerHUD | ×2件 |
| ButtonPanel_Common_Pressed | 图 | 136x136(等2种) | HUD | PlayerHUD | ×2件 |
| ButtonPanel_Play_Hover | 图 | 260x260(等2种) | HUD | PlayerHUD | ×2件 |
| ButtonPanel_Play_Normal | 图 | 260x260(等2种) | HUD | PlayerHUD | ×2件 |
| ButtonPanel_Play_Pressed | 图 | 260x260(等2种) | HUD | PlayerHUD | ×2件 |
| Icon_AutoSelector | 图 | 60x60(等2种) | HUD | PlayerHUD | ×2件 |
| Icon_AutoSelector_Inner | 图 | 18x22 | HUD | PlayerHUD | ×2件 |
| Icon_Back | 图 | 119x56 | HUD | PlayerHUD | ×4件 |
| Icon_Back_Vertical | 图 | 140x140 | HUD | PlayerHUD | ×2件 |
| Icon_Balance | 图 | 56x66 | HUD | PlayerHUD | ×2件 |
| Icon_BetSelector | 图 | 60x60 | HUD | PlayerHUD | ×2件 |
| Icon_ChangeLanguage | 图 | 80x80 | HUD | PlayerHUD | ×2件 |
| Icon_Duplicate | 图 | 28x28 | HUD | PlayerHUD | ×4件 |
| Icon_Exit | 图 | 72x72 | HUD | PlayerHUD | ×2件 |
| Icon_Guide | 图 | 72x72 | HUD | PlayerHUD | ×2件 |
| Icon_History | 图 | 72x72 | HUD | PlayerHUD | ×2件 |
| Icon_Muted | 图 | 64x52 | HUD | PlayerHUD | ×2件 |
| Icon_OpenSetting | 图 | 60x60 | HUD | PlayerHUD | ×2件 |
| Icon_Play_Auto | 图 | 124x124(等2种) | HUD | PlayerHUD | ×2件 |
| Icon_Play_Holding | 图 | 124x124(等2种) | HUD | PlayerHUD | ×2件 |
| Icon_Play_Normal_HyberGame | 图 | 124x124(等2种) | HUD | PlayerHUD | ×2件 |
| Icon_Play_Normal_Universal | 图 | 146x120 | HUD | PlayerHUD | ×2件 |
| Icon_Profit | 图 | 66x66 | HUD | PlayerHUD | ×2件 |
| Icon_Setting | 图 | 72x72 | HUD | PlayerHUD | ×2件 |
| Icon_SpeedLevel | 图 | 60x60(等2种) | HUD | PlayerHUD | ×2件 |
| Icon_Unmuted | 图 | 64x52 | HUD | PlayerHUD | ×2件 |
| Panel_BetAmount | 图 | 152x64 | HUD | PlayerHUD | ×2件 |
| Panel_SpeedLevel | 图 | 140x80 | HUD | PlayerHUD | ×2件 |
| Panel_Wallet | 图 | 600x260(等2种) | HUD | PlayerHUD | ×2件 |
| PlayerHUD_ButtonPanel_BottomOffset | 图 | 256x57 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_ButtonPanel_ExtraLine | 图 | 256x88 | HUD | PlayerHUD | ×2件 |
| PlayerHUD_ButtonPanel_Top | 图 | 256x88 | HUD | PlayerHUD | ×2件 |
| Title_Panel | 图 | 476x250 | HUD | PlayerHUD | ×2件 |
| ToggleIcon_SpeedLevel | 图 | 91x29(等2种) | HUD | PlayerHUD | ×2件 |

### 8.4 菜单/历史/Guide(30 行 / 69 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| BetHistory_DayTab_Hover | 图 | 256x81 | 菜单/历史/Guide | GameSetting | ×2件 |
| BetHistory_DayTab_Press | 图 | 256x81 | 菜单/历史/Guide | GameSetting | ×2件 |
| BetHistory_DayTab_Selected | 图 | 256x81 | 菜单/历史/Guide | GameSetting | ×2件 |
| BetItem_Bg_Normal | 图 | 1024x114 | 菜单/历史/Guide | GameSetting | ×2件 |
| BetItem_Bg_Normal_Vertical | 图 | 1000x123 | 菜单/历史/Guide | GameSetting | ×2件 |
| BetItem_Bg_Win | 图 | 1024x114 | 菜单/历史/Guide | GameSetting | ×2件 |
| BetItem_Bg_Win_Vertical | 图 | 1000x123 | 菜单/历史/Guide | GameSetting | ×2件 |
| BetItem_Boost | 图 | 36x53 | 菜单/历史/Guide | GameSetting | ×4件 |
| BetItem_Copy | 图 | 28x28 | 菜单/历史/Guide | GameSetting |  |
| BetItem_Detail_ButtonIcon | 图 | 42x42 | 菜单/历史/Guide | GameSetting | ×2件 |
| BetItem_Status_Complete | 图 | 160x40 | 菜单/历史/Guide | GameSetting | ×2件 |
| BetItem_Status_InProgress | 图 | 160x40 | 菜单/历史/Guide | GameSetting | ×2件 |
| BetItem_Status_Refunded | 图 | 160x40 | 菜单/历史/Guide | GameSetting | ×2件 |
| BillDetailPage_BottomBlur | 图 | 512x47 | 菜单/历史/Guide | GameSetting | ×4件 |
| BillDetailPage_DivideLine_RightToLeft | 图 | 256x3 | 菜单/历史/Guide | GameSetting | ×4件 |
| BillDetailPage_Icon_FlipToRight | 图 | 120x120 | 菜单/历史/Guide | GameSetting | ×4件 |
| Guide_PaperBackground | 图 | 1024x894 | 菜单/历史/Guide | GameSetting | ×2件 |
| LanguageSelector_Panel | 图 | 800x960 | 菜单/历史/Guide | GameSetting | ×2件 |
| Line_GuideSectionHeader | 图 | 124x4 | 菜单/历史/Guide | GameSetting | ×2件 |
| Line_HeaderDecoration | 图 | 604x12 | 菜单/历史/Guide | GameSetting | ×2件 |
| Line_SectionHearderDecoration | 图 | 124x4 | 菜单/历史/Guide | GameSetting | ×2件 |
| Line_Section | 图 | 1024x4 | 菜单/历史/Guide | GameSetting | ×4件 |
| Line_Tab_Horizontal | 图 | 276x4 | 菜单/历史/Guide | GameSetting | ×2件 |
| Setting_Guide_SymbolValue | 图 | 1024x504(等2种) | 菜单/历史/Guide | GameSetting | ×2件 |
| Setting_Tab_Hover | 图 | 296x80 | 菜单/历史/Guide | GameSetting | ×2件 |
| Setting_Tab_Hover_Vertical | 图 | 216x168 | 菜单/历史/Guide | GameSetting | ×2件 |
| Setting_Tab_Press_Vertical | 图 | 216x168 | 菜单/历史/Guide | GameSetting | ×2件 |
| Setting_Tab_Pressed | 图 | 296x80 | 菜单/历史/Guide | GameSetting | ×2件 |
| Setting_Tab_Selected | 图 | 296x80 | 菜单/历史/Guide | GameSetting | ×2件 |
| Setting_Tab_Selected_Vertical | 图 | 216x168 | 菜单/历史/Guide | GameSetting | ×2件 |

### 8.5 入场与演出(12 行 / 241 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| IntroAnim START GAME 钮三态+开场全景 | 图 | 1024x1024(等3种) | 入场动画 | IntroAnim | ×9件 |
| 沙滩女郎 Spine 部件(Base/Free 两套) | 图 | 1024x1024(等3种) | 装饰演出 | 世界 | ×4件 |
| IntroAnim 海滩道具(云/树/伞/椅/沙/冲浪板/泳圈…) | 图 | 341x325(等20种) | 入场动画 | IntroAnim | ×34件 |
| 漂浮物(热气球/救生圈/海星) | 图 | 256x131(等4种) | 装饰演出 | 世界 | ×8件 |
| 免费模式霓虹灯饰(皇冠/星/Party 标语/灯串) | 图 | 1480x218(等7种) | 庆祝/免费演出 | Win/FreeSpin | ×14件 |
| 彩色气球群(免费公告/装饰) | 图 | 512x512(等5种) | 庆祝/免费演出 | Win/FreeSpin | ×14件 |
| BIG WIN/YOU WON 标题 | 图 | 1024x948(等3种) | 庆祝/免费演出 | Win/FreeSpin | ×6件 |
| EPIC WIN 霓虹小物+标题 | 图 | 1024x733(等9种) | 庆祝/免费演出 | Win/FreeSpin | ×18件 |
| MEGA WIN 标题+霓虹小物 | 图 | 1024x539(等6种) | 庆祝/免费演出 | Win/FreeSpin | ×12件 |
| MEGA 六芒星霓虹序列(32 帧) | 图 | 498x512(等2种) | 庆祝/免费演出 | Win/FreeSpin | ×70件 |
| 海鸥飞行序列(16 帧) | 图 | 256x175 | 装饰演出 | 世界 | ×32件 |
| SUPER WIN 标题+太阳/木板 | 图 | 1024x499(等9种) | 庆祝/免费演出 | Win/FreeSpin | ×20件 |

### 8.6 弹窗(6 行 / 6 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| ToastPopup_BG_0 | 图 | 512x106 | 弹窗 | Popups |  |
| ToastPopup_BG | 图 | 512x106 | 弹窗 | Popups |  |
| WarningPopup_BG_0 | 图 | 512x317 | 弹窗 | Popups |  |
| WarningPopup_BG | 图 | 512x317 | 弹窗 | Popups |  |
| WarningPopup_ConfirmButton_0 | 图 | 342x96 | 弹窗 | Popups |  |
| WarningPopup_ConfirmButton | 图 | 342x96 | 弹窗 | Popups |  |

### 8.7 通用光效与引擎(81 行 / 202 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| 引擎/字体图集内部纹理(非美术主体) | 图 | 1024x1024(等9种) | 引擎内部 | — | 非美术主体×25件 |
| AutoSelector_Infinity_Normal | 图 | 88x40 | 其它 | — | ×2件 |
| Background | 图 | 32x32 | 其它 | — | ×4件 |
| BallonContainer | 图 | 417x1024(等2种) | 其它 | — | ×2件 |
| BallonDigit_0 | 图 | 92x156 | 其它 | — |  |
| BallonDigit_1 | 图 | 70x156 | 其它 | — |  |
| BallonDigit_2 | 图 | 91x156 | 其它 | — |  |
| BallonDigit_3 | 图 | 92x156 | 其它 | — |  |
| BallonDigit_4 | 图 | 94x156 | 其它 | — |  |
| BallonDigit_5 | 图 | 93x156 | 其它 | — |  |
| BallonDigit_6 | 图 | 89x156 | 其它 | — |  |
| BallonDigit_7 | 图 | 92x156 | 其它 | — |  |
| BallonDigit_8 | 图 | 92x156 | 其它 | — |  |
| BallonDigit_9 | 图 | 92x156 | 其它 | — |  |
| BallonDigit_X | 图 | 75x101 | 其它 | — |  |
| BallonDigits | 图 | 1024x156 | 其它 | — |  |
| 通用光效/噪声/水面纹理(引擎特效用) | 图 | 658x642(等11种) | 通用光效 | 演出 | ×65件 |
| Default-Particle | 图 | 64x64 | 其它 | — |  |
| DigitNumber_0 | 图 | 144x185 | 其它 | — |  |
| DigitNumber_1 | 图 | 74x177 | 其它 | — |  |
| DigitNumber_2 | 图 | 137x180 | 其它 | — |  |
| DigitNumber_3 | 图 | 140x179 | 其它 | — |  |
| DigitNumber_4 | 图 | 144x179 | 其它 | — |  |
| DigitNumber_5 | 图 | 144x179 | 其它 | — |  |
| DigitNumber_6 | 图 | 144x184 | 其它 | — |  |
| DigitNumber | 图 | 1584x224 | 其它 | — |  |
| DigitNumber_7 | 图 | 144x179 | 其它 | — |  |
| DigitNumber_8 | 图 | 144x186 | 其它 | — |  |
| DigitNumber_9 | 图 | 144x183 | 其它 | — |  |
| DigitNumber_Comma | 图 | 66x144 | 其它 | — |  |
| DigitNumber_Dot | 图 | 62x56 | 其它 | — |  |
| FalloffLookupTexture | 图 | 2048x128 | 其它 | — |  |
| Frame_963_0 | 图 | 24x24 | 其它 | — |  |
| Free_Spin | 图 | 1024x252 | 其它 | — | ×2件 |
| InputFieldBackground | 图 | 32x32 | 其它 | — | ×2件 |
| LDR_LLL1_0 | 图 | 64x64 | 其它 | — |  |
| Light | 图 | 256x256 | 其它 | — | ×2件 |
| Noise03 | 图 | 128x64 | 其它 | — |  |
| RoastPopup_Loading_0 | 图 | 100x100 | 其它 | — | ×2件 |
| RoastPopup_Loading | 图 | 100x100 | 其它 | — | ×2件 |
| Sparkle | 图 | 256x256(等2种) | 其它 | — | ×2件 |
| T_flare02 | 图 | 256x256 | 其它 | — |  |
| Tapered_HorizontalGrad | 图 | 64x64 | 其它 | — |  |
| Title_Text_En | 图 | 470x242 | 其它 | — | ×4件 |
| Title_Text_Tr | 图 | 1024x512(等2种) | 其它 | — | ×2件 |
| Title_Text_Zh | 图 | 1024x512(等2种) | 其它 | — | ×2件 |
| Wave_Trail_Hor | 图 | 256x256 | 其它 | — |  |
| White1px | 图 | 1x1 | 其它 | — | ×2件 |
| ball | 图 | 80x80 | 其它 | — | ×2件 |
| balloon | 图 | 1867x364 | 其它 | — |  |
| beachstar | 图 | 128x128 | 其它 | — |  |
| blur_bg_0 | 图 | 256x256 | 其它 | — |  |
| blur_bg | 图 | 256x256 | 其它 | — |  |
| cash2stroke | 图 | 256x161 | 其它 | — |  |
| cashstroke | 图 | 256x256 | 其它 | — |  |
| circle | 图 | 128x128 | 其它 | — | ×2件 |
| coin | 图 | 256x256 | 其它 | — |  |
| explo | 图 | 128x128 | 其它 | — |  |
| explode_1 | 图 | 512x205 | 其它 | — |  |
| flare03 | 图 | 128x128 | 其它 | — |  |
| freespinbg | 图 | 1024x503 | 其它 | — | ×2件 |
| 彩灯串族 | 图 | 1024x158(等2种) | 其它 | — | ×10件 |
| mega_noon | 图 | 180x189 | 其它 | — | ×2件 |
| ribbon_elements | 图 | 512x512 | 其它 | — | ×2件 |
| scatterpng2 | 图 | 512x512 | 其它 | — | ×2件 |
| splash_1 | 图 | 512x341 | 其它 | — | ×2件 |
| star | 图 | 256x238 | 其它 | — |  |
| star_trail | 图 | 256x256 | 其它 | — |  |
| stars | 图 | 128x128 | 其它 | — |  |
| water | 图 | 512x512 | 其它 | — |  |
| water_explose_0 | 图 | 160x160 | 其它 | — |  |
| water_explose_1 | 图 | 160x160 | 其它 | — |  |
| water_explose_2 | 图 | 160x160 | 其它 | — |  |
| water_explose_3 | 图 | 160x160 | 其它 | — |  |
| water_explose_4 | 图 | 160x160 | 其它 | — |  |
| water_explose_5 | 图 | 160x160 | 其它 | — |  |
| water_explose_6 | 图 | 160x160 | 其它 | — |  |
| water_explose | 图 | 800x320 | 其它 | — |  |
| water_explose_7 | 图 | 160x160 | 其它 | — |  |
| water_explose_8 | 图 | 160x160 | 其它 | — |  |
| water_explose_9 | 图 | 160x160 | 其它 | — |  |

### 8.8 音频(31 行 / 31 件)

| 资产(族) | 类型 | 尺寸/时长 | 分类 | 位置 | 说明 |
|---|---|---|---|---|---|
| 2_Big Win | 音频 | 1.1s | 音频 | — |  |
| 3_Super Win | 音频 | 1.1s | 音频 | — |  |
| 4_Mega Win | 音频 | 1.1s | 音频 | — |  |
| 5_Epic Win | 音频 | 3.27s | 音频 | — |  |
| AirplaneMatch | 音频 | 1.17s | 音频 | — |  |
| BGM_BaseGame | 音频 | 111.53s | 音频 | — |  |
| BGM_FreeGame | 音频 | 81.61s | 音频 | — |  |
| BeforeSurprise | 音频 | 1.64s | 音频 | — |  |
| Big Balloon Bomb | 音频 | 1.07s | 音频 | — |  |
| BoatMatch | 音频 | 0.9s | 音频 | — |  |
| Click Button | 音频 | 0.13s | 音频 | — |  |
| Click Empty | 音频 | 0.03s | 音频 | — |  |
| Click Spin | 音频 | 0.32s | 音频 | — |  |
| CruiseMatch | 音频 | 1.23s | 音频 | — |  |
| Enter Free Spin_Beach | 音频 | 4.73s | 音频 | — |  |
| Enter Free Spin_Wheel | 音频 | 4.9s | 音频 | — |  |
| Fruit Bomb | 音频 | 0.7s | 音频 | — |  |
| FruitMatch | 音频 | 0.73s | 音频 | — |  |
| LickIceCream | 音频 | 1.09s | 音频 | — |  |
| Roulette Stop | 音频 | 0.1s | 音频 | — |  |
| SFX_NearMiss_Fast | 音频 | 1.67s | 音频 | — |  |
| SFX_NearMiss_Medium | 音频 | 3.67s | 音频 | — |  |
| SFX_NearMiss_Slow | 音频 | 6.07s | 音频 | — |  |
| SS02_SFX_FreeGameResult | 音频 | 7.89s | 音频 | — |  |
| SS02_SFX_SmallCoin | 音频 | 1.54s | 音频 | — |  |
| SS02_SFX_WinningCalculating | 音频 | 5.96s | 音频 | — |  |
| SS02_SFX_WinningEnd | 音频 | 1.02s | 音频 | — |  |
| ScatterAppear | 音频 | 0.92s | 音频 | — |  |
| ScatterMatch | 音频 | 0.57s | 音频 | — |  |
| Small Ballon Bomb | 音频 | 0.13s | 音频 | — |  |
| WelcomeDropdown_WaterSplash | 音频 | 0.87s | 音频 | — |  |

> 子表件数合计 725(图)+ 31(音频)= 756 == elements-SS02.json.assets 756。

## 9. 计数对账

- 全量资产 756(图 725+音频 31)= elements-SS02.json.assets = asset-manifest 机扫;主体清单 246 族行 member 合计 756 ✓。
- 普查(data.unity3d):Texture2D 172+Sprite 120(去重落盘 288)、AudioClip 26+bundle 5=31、TextAsset 42(Spine 9 符号+SCATTER×2+乘数×8 各 skel/atlas + 引擎 4)、AnimationClip 4(演出走 Spine/Timeline)、Font 4、VideoClip 0。
- Addressables:31 实体组全部下载成功(en/id/km/vi 无文字图包为 catalog 事实,非缺口)。
