/* p25 · 憋久了的怨气会变成冷暴力
 * 图：../scene-library/p25-憋久了的怨气-最后会变成冷暴.png（处境图库，图不复制）
 * 屏上字：冷暴力（只做标签）
 */
ENGINE.visual('p25', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p25-憋久了的怨气-最后会变成冷暴.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("冷暴力", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
