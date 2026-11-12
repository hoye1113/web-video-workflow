/* p24 · 正向 · generated */
ENGINE.visual("p24", (P) => {
  const H = P.hud;
  H.noirHeader(4, 7, "TWO PATHS", { at: 0.04, right: 'NOIR / 04' });
  H.noirLabel('04.03', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost("标", { x: 1270, y: 205, size: 300, opacity: 0.07 });
  P.noirReveal("正向", { x: 148, y: 220, size: 84, color: 'ink', at: 0.26, dur: 0.65, stagger: 0.045 });
  P.text("理性看待当下，多往正向的方向思考", { x: 152, y: 338, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 });
  P.noirHairline(150, 760, 394, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 });
  P.noirCurve('M960 720 C900 620 780 500 640 380', { color: 'blue', sw: 2.2, glow: 6, at: 1.05, dur: 1.0 });
  P.noirCurve('M960 720 C1020 620 1140 500 1280 380', { color: 'red', sw: 2.2, glow: 5, at: 1.2, dur: 1.0 });
  P.noirLabel("修复婚姻", 620, 340, { size: 20, color: 'blue', at: 1.7 });
  P.noirLabel("摧毁关系", 1240, 340, { size: 20, color: 'red', at: 1.8 });
  P.noirNode(960, 720, 6, { at: 1.0, dur: 0.4 });
  P.noirLabel('PATHS / 04.03', 150, 820, { size: 12, color: 'muted', at: 1.2 });
});
