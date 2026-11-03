/* p28 · 信任要一次次重新垒起来
 * 图：../scene-library/p28-每一次信任崩塌后都要重建-可.png（处境图库，图不复制）
 * 屏上字：一年还是三年（只做标签）
 */
ENGINE.visual('p28', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p28-每一次信任崩塌后都要重建-可.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("一年还是三年", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
