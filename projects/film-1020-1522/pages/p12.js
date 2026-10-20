/* p12 · 距离越远，他越觉得安全
 * 图：../scene-library/p12-half-door.png（处境图库，图不复制）
 * 光：lamp、screen（光就是情绪）
 * 屏上字：距离说话（只做标签）
 */
ENGINE.visual('p12', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p12-half-door.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.light(700, 380, 420, { at: 0.6, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(lt / 2) });
  P.light(1010, 300, 300, { at: 1.1, kind: 'screen', color: 'blue', k: (lt) => PV.clamp((lt - 1.1) / 1.4) });
  P.text("距离说话", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
