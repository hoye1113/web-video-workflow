/* p27 · 她先走过了那段
 * 图：../scene-library/p27-她已经走过那个阶段-你还没有.png（处境图库，图不复制）
 * 屏上字：她走过来了（只做标签）
 */
ENGINE.visual('p27', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p27-她已经走过那个阶段-你还没有.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("她走过来了", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
