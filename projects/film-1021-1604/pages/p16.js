/* p16 · 第二件：提一个具体的小要求
 * 图：../scene-library/p16-第二件-提一个具体的小要求.png（处境图库，图不复制）
 * 屏上字：很小，很清楚（只做标签）
 */
ENGINE.visual('p16', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p16-第二件-提一个具体的小要求.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("很小，很清楚", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
