/* p29 · 晚上回家装作没事，连亲密都不敢拒绝
 * 图：../scene-library/p29-晚上回家装作没事-连亲密都不.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：装没事（只做标签）
 */
ENGINE.visual('p29', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p29-晚上回家装作没事-连亲密都不.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(760, 520, 520, { at: 0.3, kind: 'lamp', k: (lt) => PV.clamp(lt / 1.8) });
  P.text("装没事", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.6 });
});
