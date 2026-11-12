/* p27 · 适度警觉 · generated */
ENGINE.visual("p27", (P) => {
  const H = P.hud;
  H.noirHeader(4, 7, "VIGILANCE", { at: 0.04, right: 'NOIR / 04' });
  H.noirLabel('04.06', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost("警", { x: 1270, y: 205, size: 300, opacity: 0.07 });
  P.noirReveal("适度警觉", { x: 148, y: 220, size: 84, color: 'ink', at: 0.26, dur: 0.65, stagger: 0.045 });
  P.text("清楚风险、摆正心态，才是对关系负责", { x: 152, y: 338, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 });
  P.noirHairline(150, 760, 394, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 });
  P.noirEye(1300, 430, 170, { color: 'blue', at: 1.05 });
  P.noirLabel('WATCH / NOT FEAR', 1160, 650, { size: 12, color: 'muted', at: 1.55 });
  P.noirLabel('NOTE / 04.06', 150, 820, { size: 12, color: 'muted', at: 1.1 });
});
