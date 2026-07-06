// 灰盒 jsdom 渲染 + 不变量自检: JS 错 / 漏件 / 越界一次抓。
// 肉眼读代码看不出"飞出屏外/被遮住/数量不符"——只在合成后的像素里现形。
// 前提: 每 box 把 x,y,w,h 写进 data-box、role 写进 data-role。
// 跑: node greybox-check.js UI-GREYBOX-<CODE>.html   (需 npm i jsdom)
const {JSDOM,VirtualConsole}=require('jsdom'),fs=require('fs');
const errs=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errs.push(e.message));
const d=new JSDOM(fs.readFileSync(process.argv[2],'utf8'),{runScripts:'dangerously',virtualConsole:vc}).window.document;
const W=1080,H=1920,T=2,allowOff=/hero|bleed|boarding|exception/i;let n=0;   // ← 按游戏画布改 W/H
d.querySelectorAll('.stage .box:not(.zone):not(.ghost)').forEach(b=>{if(!b.dataset.box)return;
  const[x,y,w,h]=b.dataset.box.split(',').map(Number);
  if((x<-T||y<-T||x+w>W+T||y+h>H+T)&&!allowOff.test(b.dataset.role||'')){n++;console.log('越界',b.dataset.role,b.dataset.box);}});
console.log('frames',d.querySelectorAll('.frame').length,'| 越界',n,'| JS错',errs.length?errs:'无');
// SCENES 长卷画廊画布更高,单独算或排除。可加: 弹层"行填满底图"/"成对件都在"/"各难度视口内站点数相等" 等专项断言。
