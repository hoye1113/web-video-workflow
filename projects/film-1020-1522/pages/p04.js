/* p04 · 第一种：他说别再联系，其实在等你来纠缠
 * 图：../scene-library/p04-phone-pushaway.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：别再联系（只做标签）
 */
ENGINE.visual('p04', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p04-phone-pushaway.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1.22], [T * 0.55, 1.22], [T * 0.55 + 0.7, 1.30], [T, 1.30]].map(([t, z]) => ({ t, z })),
  });

  P.light(900, 380, 420, { at: 0.5, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.5) / 1.6) });
  P.text("别再联系", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
