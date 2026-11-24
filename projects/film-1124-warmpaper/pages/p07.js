/* p07 · 开始不停追问纠缠
 * 图：../scene-library/f1124-p07.png（处境图库，图不复制）
 * 屏上字：越追越逃（只做标签）
 */
ENGINE.visual('p07', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/f1124-p07.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("越追越逃", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
