/* p37 · 一边怕失去一边停不下来：这是内在的冲突
 * 图：../scene-library/p37-一边怕失去一边停不下来-这是.png（处境图库，图不复制）
 * 光：lamp、screen（光就是情绪）
 * 屏上字：停不下来（只做标签）
 */
ENGINE.visual('p37', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p37-一边怕失去一边停不下来-这是.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.25, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.light(300, 640, 520, { at: 0.4, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(lt / 2) });
  P.light(1620, 640, 520, { at: 0.9, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 0.9) / 1.5) });
  P.text("停不下来", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
