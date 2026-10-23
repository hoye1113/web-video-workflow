/* p16 · 靠得住的人，不用盯
 * 图：../scene-library/p16-靠得住的人不用盯.png（处境图库，图不复制）
 */
ENGINE.visual('p16', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p16-靠得住的人不用盯.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.45 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
