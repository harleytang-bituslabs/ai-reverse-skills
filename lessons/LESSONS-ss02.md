# ss02 逆向 · 累积教训

**状态: L1~L12 已于 2026-07-06、L13~L14 已于 2026-07-08 全部整合进 SKILL.md。本文件转为台账。**

L1 截图只作视觉理解,永不从截图推导生成结果;所有元素/px 只从代码 compose 而来。(user 硬规则) → skill §0 硬规则 + 坑33
L2 屏必须覆盖: loading / 主界面+衍生(free spins…) / settings+衍生 / 弹窗。缺一不可。 → skill §5.0 硬清单
L3 代码里 HUD 与 game content 若分离(不同 Canvas/根),生成结果也要分开展示,别合并。 → skill §5.0 ③ + 坑22
L4 运行时实例化的 UI 未必在 data.unity3d;必须拉全 Addressables + 抽 + 深扫后才能判"在不在构建"。 → skill 阶段1.5 + 坑11
L5 Addressables bundle 两条 base 路径(aa/WebGL 与 ServerData/WebGL)逐 bundle fallback。 → skill 阶段1.3 + 坑10
L6 UI 面板按功能 pack 分 bundle(settingpage/popuppage/freegame_noticer/winreward/decoration…)。 → skill 阶段1.5
L7 loading 屏=宿主 React 壳,从宿主 repo 取,标来源。 → skill 阶段0.5 + §5.0 ① + 坑7
L8 HUD 与 game content 分离 → 灰盒分屏展示。 → 同 L3
L9 代码是运行时的超集(Exit tab 被 ShowExitButton 关):几何/结构从代码,可见性差异标 config-gated。 → skill §0 徽标 + 坑31
L10 赔付文案在 localization/服务端,不可达时数学值以运行时 Guide 为 validated(注明无一手 cite);几何永远 compose。 → skill §4 回退 + §0 权威表
L11 入场 START GAME=平台中间件(@hg/middleware-facade+useEntry),不在游戏 repo/Unity。 → skill 阶段0.5 + §5.0 ②
L12 win 机制(payline/ways/pay-anywhere)判定阶梯:服务端>Guide 帮助页>构建暗示。ss02=pay-anywhere(8-9/10-11/12+)。 → skill §4 判定阶梯

## 本轮新增(2026-07-06,Fable 审视,已同步进 skill)
L13 检查器假阴性:greybox-check 依赖 data-box 属性,而数据驱动渲染器没写它 → "0 越界"实为"0 检查"。
    修复:渲染器契约强制写 data-box/data-role/data-w/h,检查器 data-box=0 直接 FAIL。 → skill §5.1/§5.5 + 坑32
L14 403 存根:S3 下载失败把 ~250B AccessDenied XML 存成 .bundle 静默混进目录(ss02 六个 localization 包)。
    修复:compose-bundles 内置检测(<2KB/AccessDenied/非 Unity 魔数),记缺口。 → skill 阶段1.4 + 坑10
L15 compose 需存完整路径:滚动祖先(Viewport/ScrollContents)判定沿全链;截断成后4段会漏判,越界误报。 → skill 坑18
L16 越界分诊五分类:滚动内容(自动 offscreen)/双朝向盖板 ScreenBoard·Veil·巨Mask(bleed 名单)/出血装饰(bleed)/
    布局组塌陷 0 尺寸(跳过)/真问题(回构建核查)。实测 ss02:233 越界 → 分诊后剩 3 个真问题
    (PlayerPocketPanel/PanelBG 底部出血36px、PlayControlPanel 驻屏右外420px、DynamicSelectionContainer 底缘超50px,重生成时核查)。 → skill §5.1 + 坑21
L17 ADD 必须全量(user 经验):ss02 实际 705 图+29 音频(data.unity3d 288 + bundles 417),旧 ADD 只 27 行=不合格。
    修复:asset-manifest.py 机械生成逐文件清单嵌 ADD 附录 + 计数对账。 → skill §3 + 坑26
L18 AnimationClip/AudioClip 是引擎原生类型,IL2CPP 剥不掉 typetree → 时长/事件可读可 cite(extracted),
    动效时长别全推给截图 derived。 → skill §0 权威表 + 坑25
L19 (user 定位)截图不是流程输入,是可选外部反馈回路;**部署形态=零截图**:无截图必须照常出齐全部产物,
    只降徽标不缺结构;无 server+无截图时数学"宁缺勿编"标 server-authoritative 未证。
    → skill §0 零截图部署 + 阶段3 反馈门(可选) + §4 回退 + §6 + 坑33
L20 (user 定位)skill 锚定不变量(§0 权威/§1 契约/§6 门禁=完成的定义),管线与脚本是可替换工具;
    单 skill 不拆分——方法论必须常驻眼前,拆分只增加"没加载对子技能"的失败面。 → skill §2 引言
L13 catalog strings 截断带括号长名 → 碎片名勿当"真缺",按 OK 组交叉甄别+grep catalog 复核实体组数(2026-07-08 重跑:14 条碎片全属已下载包,en/id/km/vi 本就无文字图包)。 → skill 坑12b
L14 同一 bundle 实名/带 hash 双名均可下载 → 抽取前按 md5 去重,防 manifest 双份计数(2026-07-08 重跑:47 下载=31 实体组+16 重复)。 → skill 坑12c
