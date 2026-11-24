/* p05 · 都认定对方就是理想伴侣
 * 图：../scene-library/f1124-p05.png（处境图库，图不复制）
 * 屏上字：高开低走（只做标签）
 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1124-p05.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("高开低走", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
