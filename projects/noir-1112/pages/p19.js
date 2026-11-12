/* p19 · 耐心 · generated */
ENGINE.visual("p19", (P) => {
  const H = P.hud;
  H.noirHeader(3, 7, "PATIENCE", { at: 0.04, right: 'NOIR / 03' });
  H.noirLabel('03.06', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost("耐", { x: 1270, y: 205, size: 300, opacity: 0.07 });
  P.noirReveal("耐心", { x: 148, y: 220, size: 84, color: 'ink', at: 0.26, dur: 0.65, stagger: 0.045 });
  P.text("她需要接住你的情绪，陪你慢慢平复", { x: 152, y: 338, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 });
  P.noirHairline(150, 760, 394, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 });
  P.noirTwoNodes(1100, 520, 1600, 520, { color: 'blue', r: 10, at: 1.05 });
  P.noirLabel('YOU', 1080, 470, { size: 12, color: 'muted', at: 1.4 });
  P.noirLabel('HER', 1580, 470, { size: 12, color: 'muted', at: 1.5 });
  P.noirLabel('NOTE / 03.06', 150, 820, { size: 12, color: 'muted', at: 1.1 });
});
