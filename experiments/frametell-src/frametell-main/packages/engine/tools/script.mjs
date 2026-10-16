// Writes the timed voiceover script (out/口播脚本.md) and subtitles (out/字幕.srt) from the episode's script.js.
import fs from 'fs';
import path from 'path';
import { loadEpisode, OUT } from './lib.mjs';
const { TIMING, META, L } = loadEpisode();
const { pages, duration } = L;

const mmss = (t) => {
  t = Math.round(t * 10) / 10;
  const m = Math.floor(t / 60), s = t - m * 60;
  return `${String(m).padStart(2, '0')}:${s.toFixed(1).padStart(4, '0')}`;
};
const srtTime = (t) => {
  const ms = Math.round(t * 1000), h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, s = Math.floor(ms / 1000) % 60;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')},${String(ms % 1000).padStart(3, '0')}`;
};

const md = [];
md.push(`# 口播脚本 · ${META.title || ''}`, '');
md.push(`> 总时长 **${mmss(duration)}**（${pages.length} 页）。语速按约 ${TIMING.CPS} 字/秒估算，每页讲完后留 **${L.gap} 秒空档**（画面停住、无字幕），方便你停顿或临场发挥。`);
md.push('> 时间码与视频画面、字幕完全对齐；每页画面的动画按下表每句话的起点触发。', '');
md.push('## 分页总览', '', '| 页 | 时间段 | 章节 | 画面主题 |', '|---|---|---|---|');
for (const p of pages) md.push(`| ${p.index + 1} | ${mmss(p.start)} – ${mmss(p.speechEnd)} | ${p.section} | ${p.title} |`);
md.push('');
let sec = '';
for (const p of pages) {
  if (p.section !== sec) { sec = p.section; md.push(`## ${sec}`, ''); }
  md.push(`### 第 ${p.index + 1} 页 · ${p.title}　\`${mmss(p.start)} – ${mmss(p.end)}\``, '');
  md.push('| 时间 | 口播 |', '|---|---|');
  for (const c of p.cues) md.push(`| ${mmss(c.start)} – ${mmss(c.end)} | ${c.text} |`);
  if (p.index < pages.length - 1) md.push(`| ${mmss(p.speechEnd)} – ${mmss(p.end)} | *（空档 ${(p.end - p.speechEnd).toFixed(1)}s · 翻页）* |`);
  md.push('');
}
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, '口播脚本.md'), md.join('\n'));

const srt = [];
let n = 1;
// ── 短句切分 ────────────────────────────────────────────────────────────────────────────────
// 一条 cue 常常 15-25 字，短视频的字幕惯例是一行 8-12 字。切在标点处，时间从 `c.k`
// （逐字起点）里取 —— **精确到字**，不是按字数拍脑袋分。没有 k（没配音的片子）就按字数比例分。
// 一行上限可用 FRAMETELL_SUB_MAX 调（默认 12）。
const SUB_MAX = Math.max(6, Math.min(20, +(process.env.FRAMETELL_SUB_MAX || 12)));
const PUNCT = /[，。！？；：、,.!?;:—…]/;

function splitCue(c) {
  const chars = [...c.text];
  const k = c.k && c.k.length === chars.length ? c.k : null;
  const lines = [];
  let from = 0;
  for (let i = 1; i <= chars.length; i++) {
    const hit = i === chars.length || PUNCT.test(chars[i - 1]) || i - from >= SUB_MAX;
    if (!hit) continue;
    const text = chars.slice(from, i).join('').replace(/^[\s，。！？；：、,.!?;:—…]+/, '').trim();
    if (text) lines.push({ from, to: i, text });
    from = i;
  }
  const at = (i) => (k ? c.start + (k[Math.min(i, k.length - 1)] - k[0]) : c.start + (c.end - c.start) * (i / chars.length));
  return lines.map((l, idx) => ({
    text: l.text,
    start: Math.max(c.start, at(l.from)),
    end: idx === lines.length - 1 ? c.end : Math.max(at(l.to), at(l.from) + 0.4),
  }));
}

for (const p of pages) for (const c of p.cues) {
  for (const line of splitCue(c)) srt.push(`${n++}\n${srtTime(line.start)} --> ${srtTime(line.end)}\n${line.text}\n`);
}
fs.writeFileSync(path.join(OUT, '字幕.srt'), srt.join('\n'));
console.log(`pages=${pages.length} cues=${pages.reduce((a, p) => a + p.cues.length, 0)} srtLines=${n - 1} duration=${mmss(duration)}`);
