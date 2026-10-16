// 复制一份工程，只改配色（META.look.palette）—— 用来 A/B 看"配色到底有没有用"
import fs from 'fs';
import path from 'path';

const FT = 'D:/WorkSpace/video-factory/experiments/frametell-src/frametell-main';
const { linkProject } = await import('file://' + FT + '/packages/engine/tools/project.mjs');

const src = 'D:/WorkSpace/video-factory/experiments/ft-run/实验-情感';
const dst = 'D:/WorkSpace/video-factory/experiments/ft-run/实验-情感-夜';

fs.rmSync(dst, { recursive: true, force: true });
fs.mkdirSync(dst, { recursive: true });
for (const e of fs.readdirSync(src, { withFileTypes: true })) {
  if (['out', 'engine', 'engine_modules'].includes(e.name)) continue;
  const from = path.join(src, e.name), to = path.join(dst, e.name);
  if (e.isDirectory()) fs.cpSync(from, to, { recursive: true });
  else fs.copyFileSync(from, to);
}
linkProject(dst);

// 只改这一处：把配色换成「夜灯」（深底 + 暖光）
const LOOK = `    look: { palette: {
      paper: '#17151A', ink: '#EFE9DE', soft: '#8E8578', muted: '#6A6259', faint: '#332E2A',
      red: '#E0895A', redF: '#5A3A2E', blue: '#7FA6B8', blueF: '#2C3F48',
      green: '#9FB08A', greenF: '#2F3A2C', yellow: '#E8C777', orange: '#E0A23B', orangeF: '#4A3A22',
    } },
`;
const f = path.join(dst, 'script.js');
let s = fs.readFileSync(f, 'utf8');
s = s.replace('    extras:', LOOK + '    extras:');
fs.writeFileSync(f, s);

console.log('夜灯版工程：', dst);
console.log('script.js 里的 look：', /look: \{ palette/.test(s) ? '已写入' : '没写进去！');
console.log('文件：', fs.readdirSync(dst).join('  '));
