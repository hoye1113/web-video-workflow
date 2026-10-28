/* p18 · 想改，却改不动
 * 图：../scene-library/p18-你想改-却改不动-也不敢改.png（处境图库，图不复制）
 * 屏上字：改不动（只做标签）
 */
ENGINE.visual('p18', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p18-你想改-却改不动-也不敢改.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.48 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("改不动", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.45 });
});
