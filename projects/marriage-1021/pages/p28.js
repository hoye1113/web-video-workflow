/* p28 · 结束了那段关系，却一直高度紧张
 * 图：../scene-library/p28-结束了那段关系-却一直高度紧.png（处境图库，图不复制）
 * 光：window（光就是情绪）
 * 屏上字：高度紧张（只做标签）
 */
ENGINE.visual('p28', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p28-结束了那段关系-却一直高度紧.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.light(960, 240, 760, { at: 0.5, kind: 'window', k: (lt) => PV.clamp(lt / 2) });
  P.text("高度紧张", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
