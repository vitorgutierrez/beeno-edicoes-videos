// Renderiza cada <section class="slide"> de um post em PNG 1080x1350.
// Uso: node posts/render.js posts/carrossel-01-produto
// Saída: <pasta>/png/slide-01.png ... e <pasta>/png/preview.png (todos lado a lado)
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const dir = path.resolve(process.argv[2] || '.');
  const html = fs.readdirSync(dir).find(f => f.endsWith('.html'));
  const out = path.join(dir, 'png');
  fs.mkdirSync(out, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 1400 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(dir, html));
  await page.evaluate(() => document.fonts.ready);

  const slides = await page.$$('section.slide');
  for (let i = 0; i < slides.length; i++) {
    const f = path.join(out, `slide-${String(i + 1).padStart(2, '0')}.png`);
    await slides[i].screenshot({ path: f });
    console.log(f);
  }

  // prévia: todos os slides lado a lado, reduzidos
  const files = slides.map((_, i) => `slide-${String(i + 1).padStart(2, '0')}.png`);
  await page.setContent(`<body style="margin:0;background:#111;display:flex;gap:16px;padding:16px">${
    files.map(f => `<img src="file://${path.join(out, f)}" style="width:360px">`).join('')}</body>`);
  await page.setViewportSize({ width: 16 + files.length * 376, height: 482 });
  await page.waitForLoadState('load');
  await page.screenshot({ path: path.join(out, 'preview.png') });
  await browser.close();
})();
