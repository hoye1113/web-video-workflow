/* p38 · 别让这段婚姻潦草收场
 * 图：../scene-library/p38-别就这样潦草收场-可以随时和.png（处境图库，图不复制）
 * 屏上字：跟我说说（只做标签）
 */
ENGINE.visual('p38', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p38-别就这样潦草收场-可以随时和.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("跟我说说", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.6 });
});
