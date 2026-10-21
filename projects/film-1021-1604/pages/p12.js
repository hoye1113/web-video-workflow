/* p12 · 懂事是一场交易：不麻烦，换安全感
 * 图：../scene-library/p12-懂事是一场交易-不麻烦-换安.png（处境图库，图不复制）
 * 光：screen（光就是情绪）
 * 屏上字：不麻烦换安全感（只做标签）
 */
ENGINE.visual('p12', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p12-懂事是一场交易-不麻烦-换安.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 520, 520, { at: 0.5, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 0.5) / 1.5) });
  P.text("不麻烦换安全感", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
