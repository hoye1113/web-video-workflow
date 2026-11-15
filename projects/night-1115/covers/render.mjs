import { createRequire } from 'module';
import { fileURLToPath, pathToFileURL } from 'url';
import path from 'path';
import fs from 'fs';

const here = path.dirname(fileURLToPath(import.meta.url));
const engineEntry = path.join(here, '..', '..', '..', 'experiments', 'frametell-src', 'frametell-main', 'packages', 'engine', 'tools', 'render.mjs');
const { chromium } = createRequire(engineEntry)('playwright-core');
const chrome = process.env.CHROME_PATH || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const outDir = path.join(here, '..', 'out');
fs.mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch({ executablePath: chrome, args: ['--force-color-profile=srgb', '--disable-lcd-text'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 1 });

for (const [name, file] of [['封面A-3x4', 'a.html'], ['封面B-3x4', 'b.html']]) {
  await page.goto(pathToFileURL(path.join(here, file)).href);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(200);
  const out = path.join(outDir, name + '.png');
  await page.screenshot({ path: out, type: 'png' });
  console.log(out);
}

await browser.close();
