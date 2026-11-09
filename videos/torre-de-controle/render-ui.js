// Gera ui/<tela>.png (3200x2000) a partir do ui-kit.html. Uso: node videos/torre-de-controle/render-ui.js
const path = require('path'); const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1700, height: 1100 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'ui-kit.html')); await p.evaluate(() => document.fonts.ready);
  for (const id of ['kanban', 'dash', 'auto']) { await (await p.$('#' + id)).screenshot({ path: path.join(__dirname, 'ui', id + '.png') }); console.log(id); }
  await b.close();
})();
