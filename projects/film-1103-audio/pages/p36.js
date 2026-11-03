/* p36 · 回不去，不代表过不好
 * 图：../scene-library/p36-回不去-不代表过不好-有些伤.png（处境图库，图不复制）
 * 屏上字：回不去（只做标签）
 */
ENGINE.visual('p36', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p36-回不去-不代表过不好-有些伤.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("回不去", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
