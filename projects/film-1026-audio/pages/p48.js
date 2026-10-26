/* p48 · 有些伤害让关系更坚韧
 * 图：../scene-library/p48-有些伤害不会留下疤-反让关系.png（处境图库，图不复制）
 */
ENGINE.visual('p48', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p48-有些伤害不会留下疤-反让关系.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

});
