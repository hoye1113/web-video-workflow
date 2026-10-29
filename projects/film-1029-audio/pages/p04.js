/* p04 · 你平时是怎么追女生的
 * 图：../scene-library/p04-先问你-平时是怎么追女生的.png（处境图库，图不复制）
 */
ENGINE.visual('p04', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p04-先问你-平时是怎么追女生的.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
