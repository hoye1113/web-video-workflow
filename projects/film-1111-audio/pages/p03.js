/* p03 · 伴侣越变越体贴
 * 图：../scene-library/f1111-p03-43.png（处境图库，图不复制）
 * 屏上字：越谈越累？（只做标签）
 */
ENGINE.visual('p03', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1111-p03-43.png', {
    at: 0,
    reveal: { from: 0.65, to: 1, at: 0.15, dur: 1.2 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("越谈越累？", { x: 250, y: 230, size: 50, align: 'l', color: 'ink', at: 1.2 });
});
