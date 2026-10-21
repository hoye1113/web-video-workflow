/* p26 · 愧疚和背叛，可以同时存在
 * 图：../scene-library/p26-愧疚和背叛-可以同时存在.png（处境图库，图不复制）
 * 光：lamp、screen（光就是情绪）
 * 屏上字：愧疚、背叛（只做标签）
 */
ENGINE.visual('p26', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p26-愧疚和背叛-可以同时存在.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.light(420, 620, 560, { at: 0.5, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.5) / 1.5) });
  P.light(1520, 620, 560, { at: 1.0, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 1.0) / 1.5) });
  P.text("愧疚", { x: 300, y: 230, size: 40, align: 'l', color: 'orange', at: 1.4 });
  P.text("背叛", { x: 1500, y: 230, size: 40, align: 'l', color: 'blue', at: 2.2 });
});
