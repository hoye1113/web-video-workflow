/* p31 · 妻子一个电话让他回家送钥匙
 * 图：../scene-library/p31-妻子一个电话让他回家送钥匙.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：回家送钥匙（只做标签）
 */
ENGINE.visual('p31', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p31-妻子一个电话让他回家送钥匙.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.6 },
    cam: [[0, 1.22], [T * 0.55, 1.22], [T * 0.55 + 0.7, 1.30], [T, 1.30]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 180, 560, { at: 0.5, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp((lt - 0.3) / 1.6) });
  P.text("回家送钥匙", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
