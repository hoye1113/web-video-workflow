/* p01 · 先道歉的那个人，反而更委屈
 * 图：../scene-library/p01-先道歉的那个人-反而更委屈.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：先道歉的人（只做标签）
 */
ENGINE.visual('p01', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p01-先道歉的那个人-反而更委屈.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(900, 220, 520, { at: 0.4, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(lt / 2) });
  P.text("先道歉的人", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
