/* p43 · 困住对方也困住自己
 * 图：../scene-library/p43-不惜赔上两个人余生的幸福-也.png（处境图库，图不复制）
 * 屏上字：困住彼此（只做标签）
 */
ENGINE.visual('p43', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p43-不惜赔上两个人余生的幸福-也.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("困住彼此", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
