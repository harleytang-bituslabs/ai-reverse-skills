// 灰盒 jsdom 渲染 + 不变量自检: JS 错 / 漏件 / 越界一次抓。
// 契约: 每 box 把 x,y,w,h 写进 data-box、role 写进 data-role(gen-greybox.py 已照做);
//        每 .stage 带 data-w/data-h(该帧参考分辨率,竖横屏混排时逐帧判);
//        超屏 scene 卡: stage 带 data-scene="1" 或 role 含 offscreen|bleed|hero → 放行越界。
// ★ data-box 总数为 0 = 越界检查空转(假阴性),直接报错退出。
// 用: node greybox-check.js UI-GREYBOX-<CODE>.html [默认W] [默认H]   (需 npm i jsdom)
const {JSDOM,VirtualConsole}=require('jsdom'),fs=require('fs');
const errs=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errs.push(e.message));
const d=new JSDOM(fs.readFileSync(process.argv[2],'utf8'),{runScripts:'dangerously',virtualConsole:vc}).window.document;
const DW=+(process.argv[3]||1080),DH=+(process.argv[4]||1920),T=2,allowOff=/bleed|hero|offscreen/i;
let n=0,boxes=0,zero=0,allowed=0;
d.querySelectorAll('.stage').forEach(st=>{
  const W=+(st.dataset.w||DW),H=+(st.dataset.h||DH),isScene=!!st.dataset.scene;
  st.querySelectorAll('.box:not(.zone):not(.ghost)').forEach(b=>{
    if(!b.dataset.box)return; boxes++;
    const[x,y,w,h]=b.dataset.box.split(',').map(Number);
    if(w<=0||h<=0){zero++;return;}                         // 布局组塌陷 0×0:位置无意义,不判越界(derived)
    if(x<-T||y<-T||x+w>W+T||y+h>H+T){
      if(isScene||allowOff.test(b.dataset.role||'')){allowed++;return;}   // scene 卡/滚动内容/盖板出血:放行
      n++;console.log('越界',b.dataset.role,b.dataset.box,`(帧${W}x${H})`);
    }
  });
});
console.log('frames',d.querySelectorAll('.frame').length,'| data-box',boxes,'| 越界',n,
  '| 放行(scene/offscreen/bleed)',allowed,'| 0尺寸(布局组)',zero,'| JS错',errs.length?errs:'无');
if(!boxes){console.error('★ FAIL: 没有任何 data-box —— 渲染器没写检查属性,越界检查空转(假阴性)。');process.exit(1);}
if(n||errs.length)process.exit(1);
// 老虎机专项断言可加: reel 网格行列数对、paytable 每页符号数对、符号集无重复/无漏。
