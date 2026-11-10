// Renderiza o reel "Por que trocar de CRM" quadro a quadro (seek(t)) e codifica em H.264.
// Uso: node videos/reel-trocar/render.js [--preview 1,5,12] [--audio mix.wav]
const path = require('path'); const fs = require('fs');
const { execFileSync } = require('child_process'); const { chromium } = require('playwright');
const DIR = __dirname, ROOT = path.resolve(DIR, '../..');
const args = process.argv.slice(2); const opt = k => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(DIR, 'reel.html')); await p.evaluate(() => document.fonts.ready);
  const total = await p.evaluate(() => window.TOTAL);
  if (opt('--preview')) {
    const out = path.join(DIR, 'render', 'preview'); fs.mkdirSync(out, { recursive: true });
    for (const t of opt('--preview').split(',').map(Number)) { await p.evaluate(t => window.seek(t), t); await p.screenshot({ path: path.join(out, `t${t.toFixed(2)}.png`) }); }
    await b.close(); return console.log('prévias em', out);
  }
  const fr = path.join(DIR, 'render', 'frames'); fs.rmSync(fr, { recursive: true, force: true }); fs.mkdirSync(fr, { recursive: true });
  const n = Math.round(total * 30);
  for (let i = 0; i < n; i++) { await p.evaluate(t => window.seek(t), i / 30); await p.screenshot({ path: path.join(fr, `${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 93 }); }
  await b.close();
  const out = path.join(ROOT, 'output', 'BEENO-REEL-POR-QUE-TROCAR.mp4'); const a = opt('--audio');
  const ff = ['-v', 'error', '-y', '-framerate', '30', '-i', path.join(fr, '%05d.jpg')];
  if (a) ff.push('-i', a, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '256k', '-shortest');
  ff.push('-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out);
  execFileSync('ffmpeg', ff); console.log('ok:', out);
})();
