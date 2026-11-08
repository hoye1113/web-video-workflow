/* p48 · 也能给你自己一个温暖安稳的港湾
 * 图：../scene-library/f1108-p48-43.png（处境图库，图不复制）
 */
ENGINE.visual('p48', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1108-p48-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

});
