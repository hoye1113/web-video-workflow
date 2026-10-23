/* p41 · 硬拽不想动的人，性价比最低
 * 图：../scene-library/p41-硬拽不想动的人最不划算.png（处境图库，图不复制）
 * 屏上字：性价比（只做标签）
 */
ENGINE.visual('p41', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p41-硬拽不想动的人最不划算.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("性价比", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
