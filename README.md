# ai-reverse-skills

逆向已上线游戏前端 → 产出 agent 训练素材三件套(ADD / GDD / UI-灰盒)的 skill 工程。cg 系列与 ss 系列的反向生成同属本任务。

## 布局

```
skills/reverse-unity-game-to-triad/   # ss 系列 skill:Unity WebGL 编译构建游戏(UnityPy 解包)
skills/reverse-game-to-triad/         # cg 系列 skill:web/JS 编译游戏(两 skill 互相独立,不交叉引用)
output/<code>/                        # 交付物:ART-AUDIO-<CODE>.md / GDD-<CODE>.md / UI-GREYBOX-<CODE>.html (+elements json)
lessons/                              # 教训台账(已整合进 skill 的条目留档追溯)
work/<code>*/                         # (gitignored) 构建/解包/抽取/合成等逆向工作材料
```

**skill 选型判据**:repo 依赖含 `react-unity-webgl`(游戏是 Unity 构建)→ `reverse-unity-game-to-triad`;否则 web/pixi 编译游戏 → `reverse-game-to-triad`。

## 已覆盖游戏

| code | 主题 | 系列/skill | 状态 |
|---|---|---|---|
| ss03 | Mahjong Streak / 麻将连莊 (build 1.0.0-56) | ss / unity | 三件套完成(旧版 skill 产出) |
| ss02 | Beach Party / 沙滩派对 (build 1.0.0-71) | ss / unity | 三件套待按新版 skill 重新生成(ADD 全量附录/灰盒 §5.0 硬清单) |
| cg01 | — | cg / web | 三件套完成;工作材料在 work/cg01-resource |
| cg02a | 榴莲派对(Aviator 类多人曲线) | cg / web | 三件套完成 |
| cg03a | Jeepney Glide(竖向逐站 crash,带 Figma) | cg / web | 三件套完成 |
| cg03r | Cluck Dash(横向车道 crash,多币种) | cg / web | 三件套完成 |

注:`ss07` 的逆向 ADD + fortune-gems 素材仍在主 repo `output/ss07`(auto-audio 分支活跃工作的验证素材,README 引用其路径),待该工作收尾后迁入。

## 核心原则(详见各 skill §0)

- **代码/构建是唯一真实信源**;截图只是可选反馈回路;**部署形态=零截图**。
- ADD 必须包含全部资产素材(机器生成全量清单+计数对账)。
- 灰盒按屏最小覆盖硬清单出齐;HUD 与 game content 代码分离则分卡。
- 依赖:`pip install UnityPy`(装进实际使用的 python)、项目内已 `npm i jsdom`、`ffprobe` 可选。
