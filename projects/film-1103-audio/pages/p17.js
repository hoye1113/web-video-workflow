/* p17 · 愧疚会一直跟着他
 * 图：../scene-library/p17-背叛的人也清楚自己做了什么-.png（处境图库，图不复制）
 * 屏上字：愧疚跟着（只做标签）
 */
ENGINE.visual('p17', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p17-背叛的人也清楚自己做了什么-.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("愧疚跟着", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.6 });
});
