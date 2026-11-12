import { createRequire } from 'module';
import { fileURLToPath, pathToFileURL } from 'url';
import path from 'path';
import fs from 'fs';

const here = path.dirname(fileURLToPath(import.meta.url));
const engineEntry = path.join(here, '..', '..', 'experiments', 'frametell-src', 'frametell-main', 'packages', 'engine', 'tools', 'render.mjs');
const { chromium } = createRequire(engineEntry)('playwright-core');
const chrome = process.env.CHROME_PATH || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const out = path.join(here, 'out', '封面-3x4.png');
fs.mkdirSync(path.dirname(out), { recursive: true });

const browser = await chromium.launch({ executablePath: chrome, args: ['--force-color-profile=srgb', '--disable-lcd-text'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(here, 'cover.html')).href);
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(250);
await page.screenshot({ path: out, type: 'png' });
await browser.close();
console.log(out);
