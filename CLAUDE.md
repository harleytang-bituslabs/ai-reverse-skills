# CLAUDE.md

本 repo 是「逆向已上线游戏 → 训练素材三件套」的 skill 工程,含两个互相独立的 skill:
**ss 系列**(Unity WebGL 编译构建)→ `skills/reverse-unity-game-to-triad/SKILL.md`;
**cg 系列**(web/JS 编译)→ `skills/reverse-game-to-triad/SKILL.md`。
**做任何逆向/生成工作前,先按游戏类型选对 skill 并严格照做**(判据:repo 依赖含 `react-unity-webgl` → ss/unity skill);README.md 有项目布局。两个 skill 互不引用(ss skill 必须自包含,不得提及 cg 系列内容)。

## 硬规则(用户定,优先级最高)

1. **代码/构建是唯一真实信源**:生成结果里的每个坐标/尺寸/资产/结构必须回代码或构建 cite;
   截图只是可选的外部反馈回路(核对结果/升 validated 徽标/暴露盲区),**绝不从截图推导**;
   **部署形态=零截图**——无截图必须照常出齐全部产物,只降徽标不缺结构。
2. **ADD=设计文档+主体资产清单;逐物理文件全量进 elements json**(2026-07-07 修订):ADD 含全部
   **逻辑主体资产**(尺寸/类型/分类/位置/说明,序列帧/图集页/多语言等组合件折叠为族行,主次分明);
   asset-manifest.py 逐文件全量写入 `elements-<CODE>.json.assets`;两层计数对账,抽取工件不入清单。
3. **灰盒屏最小覆盖**:loading / 入场 / 玩法主页面(UI 以整屏为单位、每态一帧;仅 game content/场景
   按代码分离分卡;朝向按构建证据——有孪生 Canvas 才双朝向,竖屏设计游戏只出竖屏+notes 如实描述
   该游戏横屏行为) / 玩法衍生态 / settings+衍生 / 弹窗辅助 / 超屏 SCENES / 未归类兜底。
4. **勿借旧草稿骨架**:数据每游戏回源重导;`output/` 旧版三件套只当历史,不当骨架。
5. **到可提交节点就停下告知用户,不自行 commit**。
6. **删除文件前先列清单征得确认**;搬迁/重构默认只移不删,废弃物入 `_legacy/` 由用户处置。

## 产物与验证

- 三件套命名固定:`output/<code>/ART-AUDIO-<CODE>.md`(ADD)/ `GDD-<CODE>.md` / `UI-GREYBOX-<CODE>.html`
  (ss 系列另**必出** `elements-<CODE>.json`:`ui_elements`+`assets` 双段机器清单)。
- 灰盒机械验收门(两个 skill 各带同名脚本):`node skills/<skill>/scripts/greybox-check.js <html> [W H]`,
  通过标准 = 0 JS 错 + data-box>0 + 越界全部分诊完;渲染器须给每个 box 写 `data-box`/`data-role` 才可被检测。
- 各 SKILL.md 末尾有完整脚本用法表与提交前 checklist,照表执行,不要凭记忆拼命令。

## 教训台账

新教训先整合进对应 SKILL.md(改流程/加坑条目),再在 `lessons/LESSONS-<code>.md` 留档并标注去向;
lessons/ 只作追溯,不是执行时要读的规程。

## 环境备注

- UnityPy 装在 `python3.10` user-site(`pip install UnityPy`;别的 python 版本没有)。
- jsdom 已装在本 repo 根 `node_modules/`(scripts 在 repo 内运行时 node 可直接 resolve)。
- 中间产物/工作材料一律放 `work/<code>*/`(gitignored):build 下载、unpacked、extract、bundles、
  all_layout.json、cg 源构建(cg01-resource)等。
- `ss07` 的逆向 ADD + fortune-gems 仍在主 repo `output/ss07`(auto-audio 活跃工作的验证素材,
  其 README 引用该路径),待收尾后迁入本 repo。`ss03-raw`(过时草稿,禁止引用)留在主 repo。
