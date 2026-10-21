/* p09 · 你把事都办好了，别人就没有需要你的地方
 * 图：../scene-library/p09-你把事都办好了-别人就没有需.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：你变得不重要（只做标签）
 */
ENGINE.visual('p09', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p09-你把事都办好了-别人就没有需.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.light(1180, 480, 520, { at: 0.5, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.5) / 1.5) });
  P.text("你变得不重要", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
