/* p27 · 你只是普通的一个
 * 图：../scene-library/p27-对方已经醒悟-你只是满大街都.png（处境图库，图不复制）
 * 屏上字：普通一个（只做标签）
 */
ENGINE.visual('p27', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p27-对方已经醒悟-你只是满大街都.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("普通一个", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
