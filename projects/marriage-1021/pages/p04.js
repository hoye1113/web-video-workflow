/* p04 · 窗户纸不捅破，很多人一辈子蒙在鼓里
 * 图：../scene-library/p04-窗户纸不捅破-很多人一辈子蒙.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：捅破窗户纸（只做标签）
 */
ENGINE.visual('p04', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p04-窗户纸不捅破-很多人一辈子蒙.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(1180, 330, 430, { at: 0.9, kind: 'window', color: 'blue', k: (lt) => PV.clamp((lt - 0.9) / 1.6) });
  P.text("捅破窗户纸", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.2 });
});
