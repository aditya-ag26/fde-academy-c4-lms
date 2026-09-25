const { chromium } = require('playwright-core');
const names={s1:'01-discussions-home',s2:'02-choose-category',s3:'03-new-discussion-form',s4:'04-replies-and-answers',s5:'05-labels-and-filters',s6:'06-formatting-code',s7:'00-which-category'};
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage({viewport:{width:1320,height:900},deviceScaleFactor:1.5});
  await p.goto('file://'+__dirname+'/mockups.html'); await p.waitForTimeout(500);
  for(const [id,n] of Object.entries(names)){
    await p.locator('#'+id).screenshot({path:(process.argv[2]||__dirname+"/..")+'/'+n+'.png'});
  }
  await b.close();
})();
