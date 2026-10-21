/* p02 · 你说没关系，别人就真的当没关系
 * 图：../scene-library/p02-你说没关系-别人就真的当没关.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：他们不再问了（只做标签）
 */
ENGINE.visual('p02', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p02-你说没关系-别人就真的当没关.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(1180, 360, 560, { at: 0.5, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("他们不再问了", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.3 });
});
