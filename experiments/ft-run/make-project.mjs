// 搭一个能跑的工程目录：复制示例片的文件 + 建 engine / engine_modules 两个 junction
// 用法：node experiments/ft-run/make-project.mjs <工程名> [示例片目录]
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const FT = 'D:/WorkSpace/video-factory/experiments/frametell-src/frametell-main';
const { linkProject, ENGINE_DIR } = await import('file://' + FT + '/packages/engine/tools/project.mjs');

const name = process.argv[2] || '复利';
const src = process.argv[3] || path.join(FT, 'packages/engine/styles/warm-story/example');
const dst = path.join('D:/WorkSpace/video-factory/experiments/ft-run', name);

fs.mkdirSync(dst, { recursive: true });
// 复制示例片（跳过 junction 和 out）
for (const e of fs.readdirSync(src, { withFileTypes: true })) {
  if (e.name === 'engine' || e.name === 'engine_modules' || e.name === 'out' || e.name === '.gitignore') continue;
  const from = path.join(src, e.name), to = path.join(dst, e.name);
  if (e.isDirectory()) fs.cpSync(from, to, { recursive: true });
  else fs.copyFileSync(from, to);
}
linkProject(dst);
console.log('工程目录：', dst);
console.log('里面：', fs.readdirSync(dst).join('  '));
console.log('engine 指向：', fs.readlinkSync(path.join(dst, 'engine')));
console.log('engine_modules 指向：', fs.readlinkSync(path.join(dst, 'engine_modules')));
