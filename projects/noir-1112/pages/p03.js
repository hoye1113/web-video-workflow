/* p03 · 防备 · generated */
ENGINE.visual("p03", (P) => {
  const H = P.hud;
  H.noirHeader(1, 7, "THE REFLEX", { at: 0.04, right: 'NOIR / 01' });
  H.noirLabel('01.03', 1700, 140, { size: 11, color: 'faint', at: 0.7 });
  P.noirGhost("防", { x: 1270, y: 205, size: 300, opacity: 0.07 });
  P.noirReveal("防备", { x: 148, y: 220, size: 84, color: 'ink', at: 0.26, dur: 0.65, stagger: 0.045 });
  P.text("不是小题大做，是信任崩塌后的本能反应", { x: 152, y: 338, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 });
  P.noirHairline(150, 760, 394, { color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 });
  P.noirCrack(1180, 270, 380, 470, { color: 'red', at: 1.05 });
  P.noirLabel('TRUST / BROKEN', 1160, 750, { size: 12, color: 'muted', at: 1.65 });
  P.noirLabel('NOTE / 01.03', 150, 820, { size: 12, color: 'muted', at: 1.1 });
});
