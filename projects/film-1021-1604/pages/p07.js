/* p07 · 你说不用照顾，别人就真的不照顾你
 * 图：../scene-library/p07-你说不用照顾-别人就真的不照.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：没有人来看你（只做标签）
 */
ENGINE.visual('p07', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p07-你说不用照顾-别人就真的不照.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.2, dur: 1.4 },
    cam: [[0, 1.22], [T * 0.55, 1.22], [T * 0.55 + 0.7, 1.30], [T, 1.30]].map(([t, z]) => ({ t, z })),
    grade: { brightness: 0.86, saturate: 0.84 },
  });

  P.light(760, 560, 480, { at: 0.4, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(lt / 1.8) });
  P.text("没有人来看你", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
