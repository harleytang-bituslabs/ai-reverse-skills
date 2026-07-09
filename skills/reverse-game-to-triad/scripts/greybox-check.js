// 灰盒 jsdom 渲染 + 不变量自检: JS 错 / 漏件 / 越界一次抓。
// 肉眼读代码看不出"飞出屏外/被遮住/数量不符"——只在合成后的像素里现形。
// 前提: 每 box 把 x,y,w,h 写进 data-box、role 写进 data-role。
// 跑: node greybox-check.js UI-GREYBOX-<CODE>.html   (需 npm i jsdom)
const {JSDOM,VirtualConsole}=require('jsdom'),fs=require('fs');
const errs=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errs.push(e.message));
const d=new JSDOM(fs.readFileSync(process.argv[2],'utf8'),{runScripts:'dangerously',virtualConsole:vc}).window.document;
const DW=Number(process.argv[3])||1080,DH=Number(process.argv[4])||1920,T=2,allowOff=/hero|bleed|boarding|exception|offscreen:scroll/i;let n=0,boxes=0;
d.querySelectorAll('.stage').forEach(st=>{
  if(st.dataset.scene==='1')return;                       // SCENES 长卷整帧放行(超屏语义)
  const W=Number(st.dataset.w)||DW,H=Number(st.dataset.h)||DH;   // 逐帧参考分辨率
  st.querySelectorAll('.box:not(.zone):not(.ghost)').forEach(b=>{if(!b.dataset.box)return;boxes++;
    const[x,y,w,h]=b.dataset.box.split(',').map(Number);
    if((x<-T||y<-T||x+w>W+T||y+h>H+T)&&!allowOff.test(b.dataset.role||'')){n++;console.log('越界',b.dataset.role,b.dataset.box,`(帧${W}x${H})`);}});
});
if(boxes===0){console.log('FAIL: data-box 总数=0(渲染器未写检查属性,越界检查空转)');process.exitCode=1;}
console.log('frames',d.querySelectorAll('.stage').length,'| data-box',boxes,'| 越界',n,'| JS错',errs.length?errs:'无');
if(n>0||errs.length)process.exitCode=1;
// SCENES 长卷画廊画布更高,单独算或排除。可加: 弹层"行填满底图"/"成对件都在"/"各难度视口内站点数相等" 等专项断言。
