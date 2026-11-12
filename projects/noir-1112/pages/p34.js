/* p34 · 空气 · generated */
ENGINE.visual("p34", (P) => {
  const H = P.hud;
  H.noirHeader(6, 7, "AIR", { at: 0.04, right: 'NOIR / 06' });
  H.noirLabel('06.03', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost("气", { x: 1270, y: 205, size: 300, opacity: 0.07 });
  P.noirReveal("空气", { x: 148, y: 220, size: 84, color: 'ink', at: 0.26, dur: 0.65, stagger: 0.045 });
  P.text("拥有时被忽略，消失时让人窒息", { x: 152, y: 338, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 });
  P.noirHairline(150, 760, 394, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 });
  P.noirWave(1060, 400, 600, 150, { bars: 42, gap: 5, color: 'blue', at: 1.05 });
  P.noirLabel('EMOTION / SIGNAL', 1060, 370, { size: 12, color: 'muted', at: 1.1500000000000001 });
  P.noirLabel('NOTE / 06.03', 150, 820, { size: 12, color: 'muted', at: 1.1 });
});
