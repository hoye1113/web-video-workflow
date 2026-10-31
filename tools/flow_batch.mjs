// Playwright Flow batch generator (fallback when bsk/extension port is occupied).
// Reads a JSON queue: [{id, cast, prompt, out}].
// Usage: node tools/flow_batch.mjs --queue <file> [--skip-existing] [--limit N]
import fs from 'fs';
import path from 'path';
import { createRequire } from 'node:module';

const require = createRequire('file:///C:/Users/QWQ/web-video-workflow/experiments/frametell-src/frametell-main/packages/engine/');
const { chromium } = require('playwright-core');

const arg = (k, d = '') => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const has = (k) => process.argv.includes('--' + k);
const queueFile = arg('queue');
if (!queueFile) { console.error('need --queue <json>'); process.exit(2); }
const queue = JSON.parse(fs.readFileSync(queueFile, 'utf8'));
const skipExisting = has('skip-existing');
const limit = +arg('limit', '0') || queue.length;
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

const GET_IMGS = `(()=>{const H=["flow-content.google","flow.google.com/asb","/asb/"];const s=new Set();for(const i of document.querySelectorAll('img')){const u=i.src||'';if(!H.some(h=>u.includes(h)))continue;s.add(u.replace(/=s\\d+(-rw)?$/,''));}return [...s];})()`;
const GET_CHIPS = `(()=>{const els=[...document.querySelectorAll('[contenteditable=true]')];const el=els[els.length-1];if(!el)return [];let q=el;for(let i=0;i<3&&q;i++)q=q.parentElement;return q?[...q.querySelectorAll('img')].map(i=>({src:i.src||'',w:i.naturalWidth,h:i.naturalHeight})):[];})()`;

async function connect() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];
  let page = ctx.pages().find(p => p.url().includes('flow.google.com/project/'));
  if (!page) {
    page = ctx.pages().find(p => p.url().includes('flow.google.com')) || await ctx.newPage();
    if (!page.url().includes('flow.google.com')) {
      await page.goto('https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb', { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(10000);
    }
  }
  await page.bringToFront();
  await page.setViewportSize({ width: 1600, height: 900 });
  return { browser, page };
}

async function ensureComposer(page, timeout = 60000) {
  const end = Date.now() + timeout;
  while (Date.now() < end) {
    const n = await page.locator('[contenteditable=true]').count();
    if (n > 0) return true;
    await page.waitForTimeout(2000);
  }
  return false;
}

async function resetOverlays(page) {
  for (let i = 0; i < 3; i++) {
    const n = await page.evaluate(() => document.querySelectorAll('[role=option],.cdk-overlay-backdrop').length);
    if (!n) break;
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(600);
  }
}

async function attachOne(page, name) {
  await resetOverlays(page);
  const plus = page.locator('button[aria-label="Add ingredients to the prompt box"]').first();
  await plus.click({ timeout: 30000 });
  await page.waitForTimeout(1800);
  // 搜索框最稳：先按名字过滤，避免在几千张图里滚动/点分类标签被遮罩挡住
  const search = page.locator('input[placeholder*="Search" i]').first();
  if (await search.count()) {
    await search.fill(name);
    await page.waitForTimeout(1800);
  }
  let opt = page.locator('[role=option]').filter({ hasText: name }).first();
  if (await opt.count() === 0) {
    // 兜底：用 JS 点 Characters 分类（真实点击有时被 cdk 遮罩拦截）
    const tab = page.locator('button,[role=tab],[role=button]').filter({ hasText: 'Characters' }).first();
    if (await tab.count()) {
      await tab.evaluate(el => el.click()).catch(() => {});
      await page.waitForTimeout(1500);
      if (await search.count()) { await search.fill(name); await page.waitForTimeout(1500); }
    }
    opt = page.locator('[role=option]').filter({ hasText: name }).first();
  }
  if (await opt.count() === 0) throw new Error(`角色不在选择器里：${name}`);
  const before = (await page.evaluate(GET_CHIPS)).length;
  await opt.click();
  await page.waitForTimeout(2500);
  let chips = await page.evaluate(GET_CHIPS);
  if (chips.length <= before) {
    const add = page.locator('button').filter({ hasText: /add to prompt/i }).first();
    if (await add.count() && await add.isEnabled().catch(() => false)) {
      await add.click();
      await page.waitForTimeout(2500);
      chips = await page.evaluate(GET_CHIPS);
    }
  }
  if (chips.length <= before) {
    // 关掉残留的选择器，避免下一次点 + 被遮罩挡住
    await page.keyboard.press('Escape').catch(() => {});
    throw new Error(`挂了「${name}」但 chip 没增加（${before} → ${chips.length}）`);
  }
  await resetOverlays(page);
  return chips.length;
}

async function typePrompt(page, text) {
  for (let i = 0; i < 10; i++) {
    const r = await page.evaluate((t) => {
      const els = [...document.querySelectorAll('[contenteditable=true]')];
      const el = els[els.length - 1];
      if (!el) return { ok: false, reason: 'no input' };
      el.focus();
      document.execCommand('selectAll', false, null);
      document.execCommand('delete', false, null);
      document.execCommand('insertText', false, t);
      return { ok: true, len: (el.textContent || '').length };
    }, text);
    if (r.ok && r.len) return r;
    await page.waitForTimeout(4000);
  }
  throw new Error('提示词没写进 Flow 输入框');
}

async function clickGenerate(page) {
  const b = page.locator('button[aria-label="Start generation"]').first();
  if (await b.count() === 0) throw new Error('找不到 Start generation 按钮');
  const end = Date.now() + 30000;
  while (Date.now() < end && await b.isDisabled().catch(() => true)) await page.waitForTimeout(1000);
  try {
    await b.click({ timeout: 30000 });
  } catch (e) {
    await resetOverlays(page);
    await page.waitForTimeout(1000);
    await b.click({ timeout: 30000 });
  }
}

async function getBases(page) { return await page.evaluate(GET_IMGS); }

const FETCH = `(async()=>{const bases=%s;const minW=900;const siz=1600;const res=[];for(const b of bases){let best=null;for(const u of [b+'=s'+siz+'-rw',b]){try{const r=await fetch(u);const blob=await r.blob();let w=0,h=0;try{const bm=await createImageBitmap(blob);w=bm.width;h=bm.height;bm.close();}catch(e){}if(!best||w>best.w)best={w:w,h:h,blob:blob};if(w>=minW)break;}catch(e){}}if(!best||best.w<minW)continue;const buf=await best.blob.arrayBuffer();const u8=new Uint8Array(buf);let s='';const CH=0x8000;for(let i=0;i<u8.length;i+=CH){s+=String.fromCharCode.apply(null,u8.subarray(i,i+CH));}res.push({b:b,w:best.w,h:best.h,size:u8.length,b64:btoa(s)});}return res;})()`;

async function generateOne(page, task) {
  await resetOverlays(page);
  if (!(await ensureComposer(page))) throw new Error('输入框没出现');
  const casts = String(task.cast ?? '小芽').split('+').filter(Boolean);
  let chips = 0;
  for (const c of casts) { chips = await attachOne(page, c); }
  await typePrompt(page, task.prompt);
  const before = new Set(await getBases(page));
  await clickGenerate(page);
  let fresh = [];
  for (let i = 0; i < 45; i++) {
    await page.waitForTimeout(7000);
    const cur = new Set(await getBases(page));
    fresh = [...cur].filter(b => !before.has(b));
    if (fresh.length) break;
  }
  if (!fresh.length) throw new Error('300 秒内没等到新图');
  await page.waitForTimeout(8000);
  const raws = await page.evaluate(FETCH.replace('%s', JSON.stringify(fresh.slice(0, 4))));
  const pick = raws.filter(r => r.w >= 900).sort((a, b) => b.w * b.h - a.w * a.h)[0];
  if (!pick) throw new Error('新图取不回来（尺寸不够）');
  const out = path.resolve(task.out);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, Buffer.from(pick.b64, 'base64'));
  // 第二张留作备选，方便以后比稿
  if (raws.length > 1) {
    const alt = out.replace(/\.png$/i, '-alt.png');
    fs.writeFileSync(alt, Buffer.from(raws[1].b64, 'base64'));
  }
  return { out, w: pick.w, h: pick.h, chips, fresh: fresh.length };
}

const { page } = await connect();
let n = 0;
for (const task of queue.slice(0, limit)) {
  n++;
  if (skipExisting && fs.existsSync(task.out)) { console.log(`[${n}/${limit}] skip ${task.id}`); continue; }
  const t0 = Date.now();
  try {
    let r;
    try { r = await generateOne(page, task); }
    catch (e) {
      console.log(`[${n}/${limit}] ${task.id} retry after: ${String(e).slice(0, 160)}`);
      await page.waitForTimeout(5000);
      r = await generateOne(page, task);
    }
    console.log(`[${n}/${limit}] ${task.id} ok ${r.w}x${r.h} chips=${r.chips} fresh=${r.fresh} ${((Date.now() - t0) / 1000).toFixed(0)}s -> ${r.out}`);
  } catch (e) {
    console.log(`[${n}/${limit}] ${task.id} FAIL ${String(e).slice(0, 300)}`);
  }
}
process.exit(0);
