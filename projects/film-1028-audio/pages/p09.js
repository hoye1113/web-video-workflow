/* p09 · 怕离婚的慌乱藏不住
 * 图：../scene-library/p09-你怕离婚的慌乱-她看得一清二.png（处境图库，图不复制）
 * 屏上字：她看得见（只做标签）
 */
ENGINE.visual('p09', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p09-你怕离婚的慌乱-她看得一清二.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.24, dur: 1.52 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("她看得见", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
