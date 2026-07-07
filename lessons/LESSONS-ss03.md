# ss03 逆向(2026-07-07 重生成)· 累积教训

**状态:L1~L7 已于 2026-07-07 全部整合进 skills/reverse-unity-game-to-triad/SKILL.md 与 CLAUDE.md。本文件只作台账。**

L1 ADD 资产清单分两层(user 两轮反馈收敛):ADD 内=**主体资产清单**(逻辑资产逐行:尺寸/类型/分类/位置/说明;序列帧/图集页/多语言变体等组合件折叠为族行——935 行逐文件全贴=过度抓取,纯设计文档零清单=缺主体信息);elements json `assets` 段=逐物理文件机器全量;两层计数对账。正文必配「玩法→美术适配」章;抽取工件/引擎内部纹理不当主体。 → skill 头部+§1 产物表+§3 修订+§6 资产对账项+坑26;CLAUDE.md 硬规则 2
L2 朝向按构建证据:ss03 为竖屏设计(全部 UI 固定 1080×1920 ResolutionBoard,无 _Horizontal 孪生 Canvas),横屏=board 居中+全幅背景(2560²/世界背景)自动拉伸填两侧——灰盒只出竖屏帧,横屏行为写 notes,勿造横屏投影帧(投影帧全是越界噪声)。(user 反馈) → skill §5.0③+§6 屏覆盖项+坑34;CLAUDE.md 硬规则 3
L3 "怪位置"先回原始 RectTransform 手算复核再怀疑 compose:TopHint(HUD 子件 aPos.y=+1290 锚到屏顶 y25)、PlayControlPanel(anchor 0.7145..1 + aPos.x=471 → x1055 屏外驻留滑入面板)均为真实设计,compose 无错。 → skill 坑35
L4 UI 以屏为单位,勿切碎(user 二轮反馈,取代首轮"合成卡补救"方案):HUD/横幅/提示等 UI Canvas 按 z 序合成整屏、每态一帧;只有 game content(世界空间/独立渲染域)按代码分离单独出卡(主屏内 ghost 占位);模板件归"复用模板件"区,Debug 样板全 exclude 只记 notes。 → skill §5.0③+坑22 改写+坑36
L5 三件套受众定位(写作准则):喂给下一个 agent 的训练材料,要回答"想要什么样的游戏/需要哪些美术素材/前端显示如何放置/玩法是什么/为匹配玩法在美术与前端做了哪些适配"——穷尽阅读代码是为了理解设计,输出最准确精炼的内容,不是罗列。(user 原话摘要) → skill §1 产物表 ADD 行+§3 修订
L6 skill 措辞保持泛化:横屏填充方式(背景拉伸/黑边/裁切)各游戏不同,ss03 的"背景自动拉伸"只写进 ss03 产物 notes,skill 只规定"按该游戏实际证据如实描述"。(user 反馈) → skill §5.0③+坑34
L7 inject 手算几何=高危区(user 发现 loading 条右偏):CSS 中心锚 `left:52%+translate(-50%,-50%)` 的 52% 是中心——y 轴减了半高、x 轴漏减半宽 → 整簇右偏 390px 且 greybox-check 不报(界内错位无检查)。整改:inject 节点在构建脚本里写明换算式,§6 新增"inject 节点逐个复算"门;同批复查揪出 GameEntry Exit 钮 x 同类错(926→958)。 → skill §5.1★ inject 条+§6 复算项+坑37
