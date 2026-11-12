import { createRequire } from 'module';
import { fileURLToPath, pathToFileURL } from 'url';
import { execFileSync } from 'child_process';
import path from 'path';
import fs from 'fs';

const here = path.dirname(fileURLToPath(import.meta.url));
const engineEntry = path.join(here, '..', '..', 'experiments', 'frametell-src', 'frametell-main', 'packages', 'engine', 'tools', 'render.mjs');
const { chromium } = createRequire(engineEntry)('playwright-core');
const html = path.join(here, 'preview.html');
const outDir = path.join(here, 'out');
const frameDir = path.join(outDir, 'frames');
const keyDir = path.join(outDir, 'keyframes');
fs.mkdirSync(frameDir, { recursive: true });
fs.mkdirSync(keyDir, { recursive: true });

const args = process.argv.slice(2);
const doVideo = !args.includes('--no-video');
const doKeys = !args.includes('--no-keys');
const fps = 30;
const duration = 30;
const chrome = process.env.CHROME_PATH || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const browser = await chromium.launch({
  executablePath: chrome,
  args: ['--force-color-profile=srgb', '--disable-lcd-text'],
});
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(html).href + '?capture=1');
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(250);

// keyframes at the middle of each page
if (doKeys) {
  const marks = [
    ['p01', 2.0], ['p02', 6.0], ['p03', 10.25], ['p04', 15.0],
    ['p05', 20.0], ['p06', 25.0], ['p07', 28.75],
  ];
  for (const [name, t] of marks) {
    await page.evaluate((x) => window.__seek(x), t);
    await page.screenshot({ path: path.join(keyDir, `${name}.png`), type: 'png' });
    console.log(`keyframe ${name} @ ${t}s`);
  }
}

if (doVideo) {
  const total = Math.round(fps * duration);
  const t0 = Date.now();
  for (let i = 0; i < total; i++) {
    const t = i / fps;
    await page.evaluate((x) => window.__seek(x), t);
    await page.screenshot({
      path: path.join(frameDir, `${String(i).padStart(4, '0')}.jpg`),
      type: 'jpeg',
      quality: 92,
    });
    if (i % 90 === 0) {
      const elapsed = ((Date.now() - t0) / 1000).toFixed(1);
      console.log(`frames ${i}/${total}  ${elapsed}s`);
    }
  }
  const mp4 = path.join(outDir, 'preview-30s.mp4');
  execFileSync('ffmpeg', [
    '-y', '-hide_banner', '-loglevel', 'error',
    '-framerate', String(fps), '-i', path.join(frameDir, '%04d.jpg'),
    '-vf', 'scale=in_range=full:out_range=tv,format=yuv420p',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
    '-preset', 'medium', '-movflags', '+faststart', mp4,
  ], { stdio: 'inherit' });
  console.log(`video -> ${mp4}`);
}

await browser.close();
