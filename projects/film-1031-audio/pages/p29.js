/* p29 · 强撑着的两个人
 * 图：../scene-library/p29-靠强撑维持两个人在一起-又何.png（处境图库，图不复制）
 * 屏上字：何必强撑（只做标签）
 */
ENGINE.visual('p29', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p29-靠强撑维持两个人在一起-又何.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("何必强撑", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
