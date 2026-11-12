/* p26 · 两种极端 · generated */
ENGINE.visual("p26", (P) => {
  const H = P.hud;
  H.noirHeader(4, 7, "TWO EXTREMES", { at: 0.04, right: 'NOIR / 04' });
  H.noirLabel('04.05', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost("衡", { x: 1270, y: 205, size: 300, opacity: 0.07 });
  P.noirReveal("两种极端", { x: 148, y: 220, size: 84, color: 'ink', at: 0.26, dur: 0.65, stagger: 0.045 });
  P.text("都暗藏隐患", { x: 152, y: 338, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 });
  P.noirHairline(150, 760, 394, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 });
  P.noirScale(1300, 300, 430, { color: 'orange', at: 1.05 });
  P.noirLabel("绝对信任", 1020, 520, { size: 18, color: 'blue', at: 1.55 });
  P.noirLabel("绝对不信任", 1450, 520, { size: 18, color: 'red', at: 1.65 });
  P.noirLabel('PATHS / 04.05', 150, 820, { size: 12, color: 'muted', at: 1.2 });
});
