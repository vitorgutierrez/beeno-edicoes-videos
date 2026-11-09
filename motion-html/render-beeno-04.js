const {spawn}=require('child_process'); const fs=require('fs'); const path=require('path');
const CHROME='C:/Program Files/Google/Chrome/Application/chrome.exe';
const W=1080,H=1920,FPS=60;
const MODE=process.argv[2]||'dark';           // dark | alpha
const OUTDIR=path.resolve(process.argv[3]||('frames_'+MODE));
const PORT=9460+(MODE==='alpha'?1:0);
const sleep=ms=>new Promise(r=>setTimeout(r,ms));

(async()=>{
  fs.rmSync(OUTDIR,{recursive:true,force:true}); fs.mkdirSync(OUTDIR,{recursive:true});
  const prof=path.join(OUTDIR,'..','prof_'+MODE);
  const chrome=spawn(CHROME,['--headless=new','--remote-debugging-port='+PORT,
    '--user-data-dir='+prof,'--no-first-run','--no-default-browser-check','--hide-scrollbars',
    '--disable-lcd-text','--force-device-scale-factor=1','--font-render-hinting=none',
    '--disable-extensions','--disable-background-timer-throttling','--mute-audio',
    '--window-size='+W+','+H,'about:blank'],{stdio:'ignore'});

  let ws=null;
  for(let i=0;i<80;i++){ await sleep(250);
    try{ const l=await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const pg=l.find(t=>t.type==='page'); if(pg&&pg.webSocketDebuggerUrl){ws=pg.webSocketDebuggerUrl;break} }catch(e){}
  }
  if(!ws) throw new Error('CDP não respondeu');

  const sock=new WebSocket(ws); let id=0; const pend=new Map(); const evs=new Map();
  sock.addEventListener('message',e=>{ const m=JSON.parse(e.data);
    if(m.id&&pend.has(m.id)){ const p=pend.get(m.id); pend.delete(m.id);
      m.error?p.rej(new Error(JSON.stringify(m.error))):p.res(m.result); }
    else if(m.method&&evs.has(m.method)){ evs.get(m.method)(); evs.delete(m.method); } });
  await new Promise((r,j)=>{sock.addEventListener('open',r);sock.addEventListener('error',j)});
  const cmd=(method,params={})=>new Promise((res,rej)=>{const i=++id;pend.set(i,{res,rej});sock.send(JSON.stringify({id:i,method,params}))});
  const once=m=>new Promise(r=>evs.set(m,r));

  await cmd('Page.enable'); await cmd('Runtime.enable');
  await cmd('Emulation.setDeviceMetricsOverride',{width:W,height:H,deviceScaleFactor:1,mobile:false});
  if(MODE==='alpha') await cmd('Emulation.setDefaultBackgroundColorOverride',{color:{r:0,g:0,b:0,a:0}});

  const url=require('url').pathToFileURL(path.resolve('anim-beeno-04.html')).href;
  const loaded=once('Page.loadEventFired'); await cmd('Page.navigate',{url}); await loaded;
  await cmd('Runtime.evaluate',{expression:`document.body.className=${JSON.stringify(MODE==='dark'?'dark':'')};document.fonts.ready.then(function(){return window.ASSETS_READY})`,awaitPromise:true});
  await sleep(500);
  const dur=(await cmd('Runtime.evaluate',{expression:'window.DUR',returnByValue:true})).result.value;
  const N=Math.round(dur*FPS);
  console.error(`[${MODE}] ${N} frames @${FPS}fps (${dur}s)`);

  const t00=Date.now();
  for(let f=0;f<N;f++){
    await cmd('Runtime.evaluate',{expression:`seek(${(f/FPS).toFixed(6)})`});
    const s=await cmd('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false});
    fs.writeFileSync(path.join(OUTDIR,'f'+String(f).padStart(5,'0')+'.png'),Buffer.from(s.data,'base64'));
    if(f%60===0) console.error(`  ${f}/${N}  ${((Date.now()-t00)/1000).toFixed(0)}s`);
  }
  console.error(`[${MODE}] pronto em ${((Date.now()-t00)/1000).toFixed(0)}s`);
  sock.close(); chrome.kill(); process.exit(0);
})().catch(e=>{console.error('ERRO',e);process.exit(1)});
