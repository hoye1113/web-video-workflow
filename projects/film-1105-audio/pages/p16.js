/* p16 · 沟通成审问，沉默成惩罚
 * 图：../scene-library/p16-沟通变成审问-沉默变成惩罚--43.png（处境图库，图不复制）
 * 屏上字：越走越远（只做标签）
 */
ENGINE.visual('p16', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p16-沟通变成审问-沉默变成惩罚--43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("越走越远", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
