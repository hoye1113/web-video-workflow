/* p13 · 他怕重蹈覆辙，也怕旁人眼光
 * 图：../scene-library/p13-他怕重蹈覆辙-也怕旁人指指点.png（处境图库，图不复制）
 */
ENGINE.visual('p13', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p13-他怕重蹈覆辙-也怕旁人指指点.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
