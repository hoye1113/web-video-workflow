/* p10 · 没有任何犹豫就认错，情绪完全失控
 * 图：../scene-library/p10-没有任何犹豫就认错-情绪完全.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：跪着求原谅（只做标签）
 */
ENGINE.visual('p10', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p10-没有任何犹豫就认错-情绪完全.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.6 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(1150, 320, 430, { at: 0.4, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(1 - (lt - 1.5) / 5) });
  P.text("跪着求原谅", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.6 });
});
