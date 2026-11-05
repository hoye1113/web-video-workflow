/* p46 · 别让情绪成为婚姻主角
 * 图：../scene-library/p46-别让情绪成为婚姻里的主角-43.png（处境图库，图不复制）
 * 屏上字：情绪主角（只做标签）
 */
ENGINE.visual('p46', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p46-别让情绪成为婚姻里的主角-43.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("情绪主角", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
