/* p37 · 每天十分钟，聊聊心情
 * 图：../scene-library/p37-建立新沟通-每天聊十分钟.png（处境图库，图不复制）
 * 屏上字：聊十分钟（只做标签）
 */
ENGINE.visual('p37', (P) => {
  STYLE.setTheme('day');
  const T = P.endT;

  P.scene('../scene-library/p37-建立新沟通-每天聊十分钟.png', {
    at: 0,
    reveal: { from: 0.34, to: 1, at: 0.22, dur: 1.5 },
    cam: [[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]].map(([t, z]) => ({ t, z })),
  });

  P.text("聊十分钟", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
