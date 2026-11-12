/* p08 · 情绪 · generated */
ENGINE.visual("p08", (P) => {
  const H = P.hud;
  H.noirHeader(1, 7, "THE WAVE", { at: 0.04, right: 'NOIR / 01' });
  H.noirLabel('01.08', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost("情", { x: 1270, y: 205, size: 300, opacity: 0.07 });
  P.noirReveal("情绪", { x: 148, y: 220, size: 84, color: 'ink', at: 0.26, dur: 0.65, stagger: 0.045 });
  P.text("一旦认定对方还会伤害你，情绪会瞬间席卷而来", { x: 152, y: 338, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 });
  P.noirHairline(150, 760, 394, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 });
  P.noirWave(1060, 400, 600, 150, { bars: 42, gap: 5, color: 'blue', at: 1.05 });
  P.noirLabel('EMOTION / SIGNAL', 1060, 370, { size: 12, color: 'muted', at: 1.1500000000000001 });
  P.noirLabel('NOTE / 01.08', 150, 820, { size: 12, color: 'muted', at: 1.1 });
});
