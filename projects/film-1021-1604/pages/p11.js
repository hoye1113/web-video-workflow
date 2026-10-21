/* p11 · 不是他们忽略你，是你教他们忽略你
 * 图：../scene-library/p11-不是他们忽略你-是你教他们忽.png（处境图库，图不复制）
 * 屏上字：你教他们忽略你（只做标签）
 */
ENGINE.visual('p11', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p11-不是他们忽略你-是你教他们忽.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("你教他们忽略你", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
