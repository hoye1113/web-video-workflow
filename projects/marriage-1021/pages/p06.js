/* p06 · 听完会改变你对背叛男人的理解；第一个是周先生
 * 图：../scene-library/p06-听完会改变你对背叛男人的理解.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：第一个·周先生（只做标签）
 */
ENGINE.visual('p06', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p06-听完会改变你对背叛男人的理解.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(1180, 470, 400, { at: 0.8, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.8) / 1.5) });
  P.text("第一个·周先生", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
