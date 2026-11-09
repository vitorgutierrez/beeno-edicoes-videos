// Monta o reel "Torre de controle": extrai os quadros dos clipes (clips/cenaN.mp4) em 1080x1920/30fps,
// desenha cada quadro do video.html e codifica em H.264.
// Uso: node videos/torre-de-controle/render.js [--preview 1.0,5.0,12.0] [--music caminho.mp3]
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const DIR = __dirname;
const ROOT = path.resolve(DIR, '../..');
const args = process.argv.slice(2);
const opt = k => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const HTML = opt('--html') || 'video.html';
const CLIPS = opt('--clips') || 'clips';
const OUT = opt('--out') || 'BEENO-TORRE-DE-CONTROLE.mp4';
const GRAIN = opt('--grain') || '0';

function extractFrames() {
  for (const f of fs.readdirSync(path.join(DIR, CLIPS)).filter(f => /\.mp4$/.test(f))) {
    const name = f.replace('.mp4', ''), out = path.join(DIR, 'frames', CLIPS, name);
    const src = path.join(DIR, CLIPS, f);
    if (fs.existsSync(out) && fs.statSync(out).mtimeMs > fs.statSync(src).mtimeMs) continue;
    fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
    execFileSync('ffmpeg', ['-v', 'error', '-i', src, '-vf',
      `fps=30,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5${+GRAIN ? `,noise=alls=${GRAIN}:allf=t` : ''}`, '-q:v', '2', path.join(out, '%04d.jpg')]);
    console.log('quadros:', name);
  }
}

(async () => {
  extractFrames();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(DIR, HTML));
  await page.evaluate(() => document.fonts.ready);
  const total = await page.evaluate(() => window.TOTAL);

  const preview = opt('--preview');
  if (preview) {
    const outDir = path.join(DIR, 'render', 'preview'); fs.mkdirSync(outDir, { recursive: true });
    for (const t of preview.split(',').map(Number)) {
      await page.evaluate(t => window.seek(t), t);
      await page.screenshot({ path: path.join(outDir, `t${t.toFixed(2)}.png`) });
    }
    await browser.close(); console.log('prévias em', outDir); return;
  }

  const fr = path.join(DIR, 'render', 'frames'); fs.rmSync(fr, { recursive: true, force: true }); fs.mkdirSync(fr, { recursive: true });
  const n = Math.round(total * 30);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.seek(t), i / 30);
    await page.screenshot({ path: path.join(fr, `${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92 });
    if (i % 90 === 0) console.log(`${i}/${n}`);
  }
  await browser.close();

  const out = path.join(ROOT, 'output', OUT);
  const music = opt('--music');
  const ff = ['-v', 'error', '-y', '-framerate', '30', '-i', path.join(fr, '%05d.jpg')];
  if (music) ff.push('-i', music, '-filter_complex', `[1:a]afade=t=in:d=0.5,afade=t=out:st=${(total - 1.5).toFixed(2)}:d=1.5,loudnorm=I=-14[a]`, '-map', '0:v', '-map', '[a]', '-c:a', 'aac', '-b:a', '192k', '-shortest');
  ff.push('-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out);
  execFileSync('ffmpeg', ff);
  console.log('ok:', out);
})();
