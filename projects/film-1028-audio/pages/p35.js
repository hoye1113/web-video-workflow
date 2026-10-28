/* p35 · 只剩一张嘴
 * 图：../scene-library/p35-只靠嘴-靠哭闹-她一眼就看穿.png（处境图库，图不复制）
 * 屏上字：只剩一张嘴（只做标签）
 */
ENGINE.visual('p35', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p35-只靠嘴-靠哭闹-她一眼就看穿.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.24, dur: 1.52 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("只剩一张嘴", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
