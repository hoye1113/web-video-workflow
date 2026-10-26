/* p30 · 别敷衍，先接住她的痛
 * 图：../scene-library/p30-别敷衍-都过去了--要耐心接.png（处境图库，图不复制）
 * 屏上字：我陪着你（只做标签）
 */
ENGINE.visual('p30', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p30-别敷衍-都过去了--要耐心接.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("我陪着你", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
