/* p08 · 清空账号不等于回归，白天演丈夫夜里睡不着
 * 图：../scene-library/male-06-bed-edge.png（处境图库，图不复制）
 * 光：lamp（光就是情绪）
 * 屏上字：白天演，夜里熬（只做标签）
 */
ENGINE.visual('p08', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/male-06-bed-edge.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.6 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
    grade: { brightness: 0.88, saturate: 0.9 },
  });

  P.light(1150, 320, 430, { at: 0.4, kind: 'lamp', color: 'orange', k: (lt) => PV.clamp(1 - (lt - 1.5) / 5) });
  P.text("白天演，夜里熬", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.6 });
});
