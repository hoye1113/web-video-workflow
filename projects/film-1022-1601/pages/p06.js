/* p06 · 换来焦虑和躲闪
 * 图：../scene-library/p06-换来的是焦虑和躲闪.png（处境图库，图不复制）
 */
ENGINE.visual('p06', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p06-换来的是焦虑和躲闪.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
