/* p04 · 她心里其实想留下
 * 图：../scene-library/p04-她心底最想要的是婚姻变好-自.png（处境图库，图不复制）
 * 屏上字：她想留下（只做标签）
 */
ENGINE.visual('p04', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p04-她心底最想要的是婚姻变好-自.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.48 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("她想留下", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
