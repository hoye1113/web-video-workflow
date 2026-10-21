/* p52 · 最怕的是双方都在错误的方式里消耗彼此
 * 图：../scene-library/p52-最怕的是双方都在错误的方式里.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：彼此消耗（只做标签）
 */
ENGINE.visual('p52', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p52-最怕的是双方都在错误的方式里.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.light(1150, 320, 430, { at: 0.4, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(1 - (lt - 1.5) / 5) });
  P.text("彼此消耗", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
