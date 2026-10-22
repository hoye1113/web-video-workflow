/* p19 · 卡住你的不是她不够爱你，是你看不透
 * 图：../scene-library/p19-卡住你的不是她不够爱你-是你.png（处境图库，图不复制）
 * 屏上字：看透她（只做标签）
 */
ENGINE.visual('p19', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p19-卡住你的不是她不够爱你-是你.png', {
    at: 0,
    reveal: { from: 0.35, to: 1, at: 0.25, dur: 1.4 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("看透她", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.5 });
});
