/* p02 · 亲密的时候，脑子里到底有没有别人
 * 图：../scene-library/p02-亲密的时候-脑子里到底有没有.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：脑子里有谁（只做标签）
 */
ENGINE.visual('p02', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p02-亲密的时候-脑子里到底有没有.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(1150, 320, 430, { at: 0.4, kind: 'window', color: 'blue', k: (lt) => PV.clamp(1 - (lt - 1.5) / 5) });
  P.text("脑子里有谁", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
