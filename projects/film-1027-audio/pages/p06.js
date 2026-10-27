/* p06 · 这是创伤后的应激反应
 * 图：../scene-library/p06-这是背叛带来的创伤后应激反应.png（处境图库，图不复制）
 * 屏上字：应激反应（只做标签）
 */
ENGINE.visual('p06', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p06-这是背叛带来的创伤后应激反应.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("应激反应", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
