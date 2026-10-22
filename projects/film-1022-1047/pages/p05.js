/* p05 · 冷得住气，沉得住气，不哭不闹
 * 图：../scene-library/p05-把精力留给自己-顺其自然.png（处境图库，图不复制）
 */
ENGINE.visual('p05', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p05-把精力留给自己-顺其自然.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
