/* p28 · 失去了在一起的欲望
 * 图：../scene-library/p28-对方已经失去非要和你在一起的.png（处境图库，图不复制）
 * 屏上字：不想在一起（只做标签）
 */
ENGINE.visual('p28', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p28-对方已经失去非要和你在一起的.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("不想在一起", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
