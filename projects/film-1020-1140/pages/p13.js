/* p13 · 该道歉的道歉，不该的不必
 * 图：../scene-library/p13-该道歉的道歉-不该的不必.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：握住对方的手（只做标签）
 */
ENGINE.visual('p13', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p13-该道歉的道歉-不该的不必.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.6 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
    grade: { brightness: 0.92, saturate: 0.9 },
  });

  P.light(960, 200, 700, { at: 0.4, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(lt / 2) });
  P.text("握住对方的手", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.6 });
});
