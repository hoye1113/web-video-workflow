/* p38 · 蜕变 · generated */
ENGINE.visual("p38", (P) => {
  const H = P.hud;
  H.noirHeader(7, 7, "TRANSFORMATION", { at: 0.04, right: 'NOIR / 07' });
  H.noirLabel('07.03', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost("生", { x: 1270, y: 205, size: 300, opacity: 0.07 });
  P.noirReveal("蜕变", { x: 148, y: 220, size: 84, color: 'ink', at: 0.26, dur: 0.65, stagger: 0.045 });
  P.text("像久旱逢甘霖的草木，完成蜕变，牢不可破", { x: 152, y: 338, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 });
  P.noirHairline(150, 760, 394, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 });
  P.noirSprout(1320, 320, 390, { color: 'green', at: 1.05 });
  P.noirLabel('AFTER / THE RAIN', 1210, 740, { size: 12, color: 'muted', at: 1.65 });
  P.noirLabel('NOTE / 07.03', 150, 820, { size: 12, color: 'muted', at: 1.1 });
});
