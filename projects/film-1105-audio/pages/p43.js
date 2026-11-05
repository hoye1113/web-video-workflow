/* p43 · 别把价值交给一个表情
 * 图：../scene-library/p43-别把全部价值和情绪交给对方一-43.png（处境图库，图不复制）
 */
ENGINE.visual('p43', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p43-别把全部价值和情绪交给对方一-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
