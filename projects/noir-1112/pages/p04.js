/* p04 · 失去确定性 · generated */
ENGINE.visual("p04", (P) => {
  const H = P.hud;
  H.noirHeader(1, 7, "CERTAINTY", { at: 0.04, right: 'NOIR / 01' });
  H.noirLabel('01.04', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost("定", { x: 1270, y: 205, size: 300, opacity: 0.07 });
  P.noirReveal("失去确定性", { x: 148, y: 220, size: 84, color: 'ink', at: 0.26, dur: 0.65, stagger: 0.045 });
  P.text("失去信任，本质是失去了对这段感情的确定性", { x: 152, y: 338, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 });
  P.noirHairline(150, 760, 394, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 });
  P.noirCurve('M980 360 C1180 360 1380 560 1720 720', { color: 'blue', sw: 2.4, glow: 7, at: 1.05 });
  P.noirHairline(980, 1720, 600, { color: 'faint', sw: 1, at: 1.25, dur: 0.7, opacity: 0.4 });
  P.noirLabel('CERTAINTY / LOST', 1530, 760, { size: 12, color: 'muted', at: 1.75 });
  P.noirLabel('NOTE / 01.04', 150, 820, { size: 12, color: 'muted', at: 1.1 });
});
