// P1 配音验收：用 edge-tts 对我们的测试工程跑一次 narrate()
// narrate 的活：每页合成一整段（语气连贯）→ 在静音处切回句子 → 写 audio/ + voice.js（逐字时间戳）
import fs from 'fs';
import path from 'path';

const FT = 'D:/WorkSpace/video-factory/experiments/frametell-src/frametell-main';
const { narrate, directChild } = await import('file://' + FT + '/packages/voice/dist/narrate.js');
const { edgeTts } = await import('file://' + FT + '/packages/voice/dist/tts.js');

const dir = 'D:/WorkSpace/video-factory/experiments/ft-run/实验-情感';

// 直接的文件读写器（studio 用的是带沙箱的那版；这里是本地测试）
const files = {
  write: (d, rel, data) => {
    const p = path.join(d, rel);
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, data);
  },
  read: (d, rel) => fs.readFileSync(path.join(d, rel)),
};

const t0 = Date.now();
console.log('开始配音：', dir);
const r = await narrate(dir, {
  tts: edgeTts(),
  voice: { speaker: 'zh-CN-XiaoxiaoNeural', rate: -6, pitch: -1 },
  child: directChild,
  files,
  onProgress: (e) => console.log(`  ${e.page} ${e.index + 1}/${e.total}${e.cached ? '（缓存命中）' : ''}`),
});

console.log(`\n结果：合成 ${r.synthesized} 段，总时长 ${r.duration.toFixed(1)} 秒，用时 ${((Date.now() - t0) / 1000).toFixed(1)} 秒`);
if (r.warnings?.length) console.log('警告：', r.warnings.slice(0, 4));

const audioDir = path.join(dir, 'audio');
if (fs.existsSync(audioDir)) {
  const fsx = fs.readdirSync(audioDir);
  const total = fsx.reduce((a, f) => a + fs.statSync(path.join(audioDir, f)).size, 0);
  console.log(`audio/ ${fsx.length} 个文件，共 ${(total / 1024).toFixed(0)} KB`);
  fsx.slice(0, 5).forEach((f) => console.log('   ', f));
}
const voiceJs = path.join(dir, 'voice.js');
if (fs.existsSync(voiceJs)) {
  const s = fs.readFileSync(voiceJs, 'utf8');
  console.log(`\nvoice.js ${s.length} 字，带时间戳的字数：${(s.match(/"c":/g) || []).length}`);
  console.log('   开头：', s.slice(0, 240).replace(/\n/g, ' '));
}
