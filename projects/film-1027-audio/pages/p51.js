/* p51 · 先递个台阶，一起翻过这一页
 * 图：../scene-library/p51-先递一个台阶-一起翻过这黑暗.png（处境图库，图不复制）
 * 屏上字：递个台阶（只做标签）
 */
ENGINE.visual('p51', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p51-先递一个台阶-一起翻过这黑暗.png', {
    at: 0,
    reveal: { from: 0.36, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]].map(([t, z]) => ({ t, z })),
  });

  P.text("递个台阶", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
