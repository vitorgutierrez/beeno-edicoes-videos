const {spawn}=require('child_process'); const fs=require('fs'); const path=require('path');
const CHROME='C:/Program Files/Google/Chrome/Application/chrome.exe';
const W=1080,H=1920,PORT=9410;
const TIMES=process.argv.slice(2).map(Number);
const OUT=path.resolve('preview_beeno'); 
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  fs.mkdirSync(OUT,{recursive:true});
  const chrome=spawn(CHROME,['--headless=new','--remote-debugging-port='+PORT,
    '--user-data-dir='+require('os').tmpdir()+'/prof_prev_beeno','--no-first-run','--no-default-browser-check','--hide-scrollbars',
    '--disable-lcd-text','--force-device-scale-factor=1','--font-render-hinting=none',
    '--mute-audio','--window-size='+W+','+H,'about:blank'],{stdio:'ignore'});
  let ws=null;
  for(let i=0;i<80;i++){ await sleep(250);
    try{ const l=await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const pg=l.find(t=>t.type==='page'); if(pg&&pg.webSocketDebuggerUrl){ws=pg.webSocketDebuggerUrl;break} }catch(e){} }
  if(!ws) throw new Error('CDP nao respondeu');
  const sock=new WebSocket(ws); let id=0; const pend=new Map(); const evs=new Map();
  sock.addEventListener('message',e=>{const m=JSON.parse(e.data);
    if(m.id&&pend.has(m.id)){const p=pend.get(m.id);pend.delete(m.id);m.error?p.rej(new Error(JSON.stringify(m.error))):p.res(m.result);}
    else if(m.method&&evs.has(m.method)){evs.get(m.method)();evs.delete(m.method);}});
  await new Promise((r,j)=>{sock.addEventListener('open',r);sock.addEventListener('error',j)});
  const cmd=(m,p={})=>new Promise((res,rej)=>{const i=++id;pend.set(i,{res,rej});sock.send(JSON.stringify({id:i,method:m,params:p}))});
  const once=m=>new Promise(r=>evs.set(m,r));
  await cmd('Page.enable'); await cmd('Runtime.enable');
  await cmd('Emulation.setDeviceMetricsOverride',{width:W,height:H,deviceScaleFactor:1,mobile:false});
  const url=require('url').pathToFileURL(path.resolve('anim-beeno-01.html')).href;
  const loaded=once('Page.loadEventFired'); await cmd('Page.navigate',{url}); await loaded;
  await cmd('Runtime.evaluate',{expression:'document.body.className="dark";document.fonts.ready',awaitPromise:true});
  await sleep(600);
  const dur=(await cmd('Runtime.evaluate',{expression:'window.DUR',returnByValue:true})).result.value;
  console.error('DUR='+dur);
  for(const t of TIMES){
    await cmd('Runtime.evaluate',{expression:`seek(${t})`});
    const s=await cmd('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false});
    fs.writeFileSync(path.join(OUT,'t'+t.toFixed(2).replace('.','_')+'.png'),Buffer.from(s.data,'base64'));
  }
  console.error('ok '+TIMES.length+' frames -> '+OUT);
  sock.close(); chrome.kill(); process.exit(0);
})().catch(e=>{console.error('ERRO',e);process.exit(1)});
