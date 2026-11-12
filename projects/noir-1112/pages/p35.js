/* p35 · 地基 · generated */
ENGINE.visual("p35", (P) => {
  const H = P.hud;
  H.noirHeader(6, 7, "FOUNDATION", { at: 0.04, right: 'NOIR / 06' });
  H.noirLabel('06.04', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost("基", { x: 1270, y: 205, size: 300, opacity: 0.07 });
  P.noirReveal("地基", { x: 148, y: 220, size: 84, color: 'ink', at: 0.26, dur: 0.65, stagger: 0.045 });
  P.text("没有信任的婚姻，如同没有地基的房子", { x: 152, y: 338, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 });
  P.noirHairline(150, 760, 394, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 });
  P.noirHouse(1160, 300, 420, { color: 'orange', at: 1.05 });
  P.noirLabel('FOUNDATION / TRUST', 1160, 720, { size: 12, color: 'muted', at: 1.85 });
  P.noirLabel('NOTE / 06.04', 150, 820, { size: 12, color: 'muted', at: 1.1 });
});
