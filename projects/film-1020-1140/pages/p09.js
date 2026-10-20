/* p09 · 他退的不是这一句，是怕这段关系散掉
 * 图：../scene-library/p09-他退的不是这一句-是怕这段关.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：更怕失去（只做标签）
 */
ENGINE.visual('p09', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p09-他退的不是这一句-是怕这段关.png', {
    at: 0,
    reveal: { from: 0.32, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(1180, 380, 540, { at: 0.4, kind: 'lamp', k: (lt) => PV.clamp(lt / 2) });
  P.text("更怕失去", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
