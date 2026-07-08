# ai-reverse-skills

逆向已上线游戏前端 → 产出 agent 训练素材三件套(ADD / GDD / UI-灰盒)的 skill 工程。cg 系列与 ss 系列的反向生成同属本任务。

## 布局

```
skills/reverse-unity-game-to-triad/   # ss 系列 skill:Unity WebGL 编译构建游戏(UnityPy 解包)
skills/reverse-game-to-triad/         # cg 系列 skill:web/JS 编译游戏(两 skill 互相独立,不交叉引用)
skills/reverse-game-to-upstream-pack/ # 上游文档包 skill:<SLUG>-pack(GDD+ADD+assets+html),
                                      #   规范=Archive/upstream-doc-pack-spec.md;采集复用上两者
Archive/                              # 上游规范 + 同事 Opus 版样例包(SS03/CG03/CG05,只作参照)
output/<code>/                        # 交付物:ART-AUDIO-<CODE>.md / GDD-<CODE>.md / UI-GREYBOX-<CODE>.html
                                      #   (ss 系列另必出 elements-<CODE>.json:ui_elements+assets 双段机器清单)
lessons/                              # 教训台账(已整合进 skill 的条目留档追溯)
work/<code>*/                         # (gitignored) 构建/解包/抽取/合成等逆向工作材料
```

**skill 选型判据**:repo 依赖含 `react-unity-webgl`(游戏是 Unity 构建)→ `reverse-unity-game-to-triad`;否则 web/pixi 编译游戏 → `reverse-game-to-triad`。

## 已覆盖游戏

| code | 主题 | 系列/skill | 状态 |
|---|---|---|---|
| ss03 | Mahjong Streak / 麻将连莊 (build 1.0.0-56) | ss / unity | **三件套完成(2026-07-07,新版 skill)**:服务端数学一手 cite、23 帧竖屏灰盒、elements 双段 |
| ss02 | Beach Party / 沙滩派对 (build 1.0.0-71) | ss / unity | **三件套完成(2026-07-08,新版 skill)**:string-tables 全取到(规则/赔付一手)、双朝向四主屏帧、Buy/DoubleChance 入档;旧版存档于 `output/ss02-opus/`(只作历史) |
| cg01 | — | cg / web | 三件套完成;工作材料在 work/cg01-resource |
| cg02a | 榴莲派对(Aviator 类多人曲线) | cg / web | 三件套完成 |
| cg03a | Jeepney Glide(竖向逐站 crash,带 Figma) | cg / web | 三件套完成 |
| cg03r | Cluck Dash(横向车道 crash,多币种) | cg / web | 三件套完成 |

注:`ss07` 的逆向 ADD + fortune-gems 素材仍在主 repo `output/ss07`(auto-audio 分支活跃工作的验证素材,README 引用其路径),待该工作收尾后迁入。

## 核心原则(详见各 skill §0;2026-07-07 修订版)

- **代码/构建是唯一真实信源**;截图只是可选反馈回路;**部署形态=零截图**(照常出齐全部产物,只降徽标)。
- **ADD=设计文档+主体资产清单**:正文精讲设计意图与「玩法→美术适配」;主体清单=逻辑资产分子表(组合件折叠为族行);**逐物理文件机器全量在 elements json `assets` 段**,两层计数对账。
- **灰盒 UI 以屏为单位**(每态一帧,勿切碎;仅 game content/场景按代码分离分卡);**朝向按构建证据**(孪生 Canvas 才双朝向,竖屏游戏只出竖屏+notes 说明);inject 注入节点必须带换算式并逐个复算。
- 依赖:`pip install UnityPy`(装进实际使用的 python,本机为 `python3.10`)、repo 根已 `npm i jsdom`、`ffprobe` 可选。
