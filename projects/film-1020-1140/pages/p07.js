/* p07 · 委屈，来自那句没敢说出口的「我没错」
 * 图：../scene-library/p07-委屈-来自那句没敢说出口的-.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：我没错（只做标签）
 */
ENGINE.visual('p07', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p07-委屈-来自那句没敢说出口的-.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1.22], [T * 0.55, 1.22], [T * 0.55 + 0.7, 1.30], [T, 1.30]].map(([t, z]) => ({ t, z })),
  });

  P.light(520, 520, 560, { at: 0.5, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("我没错", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
