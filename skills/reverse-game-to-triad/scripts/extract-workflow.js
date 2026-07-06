// 阶段1 穷尽抽取 workflow 模板 (参数化; 按实际仓库改 REPO + CLUSTERS)。
// 每 cluster 一个 Explore extractor(schema 化) → 完整性 critic → 可行性 judge。
// 中断恢复: Workflow({scriptPath, resumeFromRunId}) —— 已完成 agent 走缓存。
export const meta = { name:'<code>-ui-extract', description:'穷尽读某游戏布局代码抽布局规则 + 判定能否纯代码 1:1', phases:[{title:'Extract'},{title:'Verify'}] }
const REPO='<绝对路径>/<code>'
const CLUSTERS=[ /* 按实际结构: {key, focus, files:[绝对路径...]} —— 见 cg03a 11 类 */ ]
const EXTRACT={type:'object',additionalProperties:false,required:['cluster','components','asset_aliases','uncertainties'],properties:{
  cluster:{type:'string'},
  components:{type:'array',items:{type:'object',required:['name','file','layout'],additionalProperties:false,properties:{
    name:{type:'string'},file:{type:'string'},role:{type:'string'},assets:{type:'array',items:{type:'string'}},
    layout:{type:'string'},states:{type:'string'},animations:{type:'string'}}}},
  asset_aliases:{type:'array',items:{type:'string'}}, constants_dump:{type:'string'},
  uncertainties:{type:'array',items:{type:'object',required:['item','why','screenshot_helps'],additionalProperties:false,properties:{
    item:{type:'string'},why:{type:'string'},screenshot_helps:{type:'boolean'}}}}}}
const RULE='读 EVERY 列出文件全文(>1000行翻页到底,勿略读)；抽每个 x/y/w/h/anchor/pivot/scale/gap/z/alpha/时长/缓动 + 资产别名→路径 + 状态切换 + 动画。读到常量重算公式、不信注释。经济值注明出自 RealSocket(真) 还是 mock socket(占位)。uncertainties 标"上屏结果非代码常量直接可定"的(运行时算位/camera/mask/parallax/外部CDN资产/文字溢出/Spine上屏尺寸/服务端下发值)。'
phase('Extract')
const ex=(await parallel(CLUSTERS.map(c=>()=>agent(`抽取子系统 ${c.key}（${c.focus}）的精确布局规则供 1:1 复现。\n文件:\n${c.files.join('\n')}\n${RULE}`,
  {label:'extract:'+c.key,phase:'Extract',schema:EXTRACT,agentType:'Explore'})))).filter(Boolean)
phase('Verify')
const comp=await agent(`完整性审计 ${REPO}：grep 所有 assets/ 字面量 + getTexture/load 别名，列出未被以下覆盖的资产 + 未纳入 cluster 的可视源文件。已覆盖:\n${JSON.stringify([...new Set(ex.flatMap(e=>e.asset_aliases||[]))])}`,
  {schema:{type:'object',additionalProperties:false,required:['unmapped_assets','uncovered_files','notes'],properties:{unmapped_assets:{type:'array',items:{type:'string'}},uncovered_files:{type:'array',items:{type:'string'}},notes:{type:'string'}}},agentType:'Explore',phase:'Verify'})
const feas=await agent(`判定能否纯代码 1:1 复现 UI（固定画布游戏代码通常比截图精确）。逐条 uncertainty 给裁决,标哪需截图、是否阻塞。注意区分服务端下发值(代码无法定)与渲染常量(代码可定)。\n${JSON.stringify(ex.flatMap(e=>e.uncertainties||[]))}\n缺口:${JSON.stringify(comp)}`,
  {schema:{type:'object',additionalProperties:false,required:['verdict','code_authoritative_areas','screenshot_targets','rationale'],properties:{verdict:{type:'string',enum:['code-sufficient','code-mostly-needs-spot-checks','needs-screenshots']},code_authoritative_areas:{type:'array',items:{type:'string'}},screenshot_targets:{type:'array',items:{type:'object',additionalProperties:false,required:['screen','why','blocking'],properties:{screen:{type:'string'},why:{type:'string'},blocking:{type:'boolean'}}}},rationale:{type:'string'}}},phase:'Verify',effort:'high'})
return {extractions:ex,completeness:comp,feasibility:feas}
