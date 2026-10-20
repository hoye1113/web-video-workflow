/* p06 · 先道歉的人，先把责任全揽了过去
 * 图：../scene-library/p06-先道歉的人-先把责任全揽了过.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：错他都揽了（只做标签）
 */
ENGINE.visual('p06', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p06-先道歉的人-先把责任全揽了过.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(900, 560, 520, { at: 0.4, kind: 'lamp', k: (lt) => PV.clamp(lt / 2) });
  P.text("错他都揽了", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
