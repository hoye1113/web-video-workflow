/* p34 · 责任把人磨得疲惫
 * 图：../scene-library/p34-那些责任只把人折磨得身心疲惫.png（处境图库，图不复制）
 * 屏上字：身心疲惫（只做标签）
 */
ENGINE.visual('p34', (P) => {
  STYLE.setTheme('night');
  const T = P.endT;

  P.scene('../scene-library/p34-那些责任只把人折磨得身心疲惫.png', {
    at: 0,
    reveal: { from: 0.3, to: 1, at: 0.2, dur: 1.5 },
    cam: [[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]].map(([t, z]) => ({ t, z })),
  });

  P.text("身心疲惫", { x: 250, y: 230, size: 44, align: 'l', color: 'ink', at: 1.4 });
});
