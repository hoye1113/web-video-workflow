// 03 一叠方格纸：上百个小格子里，三张被挑出的纸片依次立起
SCENES['03'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ss, ease, rng } = U;
  const C = { bg:'#F3EDE2', paper:'#FBF8F2', ink:'#1B1A17', soft:'#6B655B', red:'#C8402F' };
  const DUR = 13;
  const PX = 40, PY = 130, PW = 1840, PH = 860;
  const CELL = 108, COLS = 16, ROWS = 7;
  const GX = PX + (PW - COLS * CELL) / 2;
  const GY = PY + (PH - ROWS * CELL) / 2;
  const BY = GY + 5 * CELL;                         // 三张立牌的底座高度
  const CARDS = [[4, 0.2], [8, 4.4], [13, 8.8]];    // [所在列, 起立时刻]

  const R = rng(9137), NJ = 1500, J = new Float32Array(NJ);
  for (let i = 0; i < NJ; i++) J[i] = R() * 2 - 1;
  const wob = (x1, y1, x2, y2, seed, amp, seg) => {  // 同一支笔的抖动
    const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy) || 1;
    const ux = -dy / L, uy = dx / L, pts = [];
    for (let i = 0; i <= seg; i++) {
      const p = i / seg;
      const j = Math.sin(p * TAU * 1.5 + seed * 2.1) * amp * 0.6 + J[(seed * 37 + i * 11) % NJ] * amp;
      pts.push([lerp(x1, x2, p) + ux * j, lerp(y1, y2, p) + uy * j]);
    }
    return pts;
  };
  const line = (c, pts, col, lw, al) => {
    c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
    for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]);
    c.strokeStyle = col; c.lineWidth = lw; c.globalAlpha = al;
    c.lineJoin = 'round'; c.lineCap = 'round'; c.stroke(); c.globalAlpha = 1;
  };
  const card = (c, cx, q, t, i) => {                 // 一张从格子里立起来的纸片
    const g = ease.out(clamp(q));
    const bw = lerp(CELL * 0.82, 300, g);            // 底边 300，三张横跨约占画面 66%
    const h = lerp(26, 250 + Math.sin(t * 1.5 + i * 2.1) * 5, g);
    const lean = 24 * g, tw = bw * 0.9, O = 18 * g, OY = 10 * g;
    const bx0 = cx - bw / 2, bx1 = cx + bw / 2;
    const ty = BY - h, tx0 = cx - tw / 2 + lean, tx1 = cx + tw / 2 + lean;

    c.globalAlpha = 0.15 * g; c.fillStyle = C.soft;  // 落在纸上的影
    c.beginPath(); c.ellipse(cx + 24 * g, BY + 6, bw * 0.55, 16, 0, 0, TAU); c.fill();
    c.globalAlpha = 1;

    const back = new Path2D();                       // 纸片的厚度
    back.moveTo(bx0 + O, BY - OY); back.lineTo(bx1 + O, BY - OY);
    back.lineTo(tx1 + O, ty - OY); back.lineTo(tx0 + O, ty - OY); back.closePath();
    c.fillStyle = C.red; c.fill(back);
    c.globalAlpha = 0.85; c.strokeStyle = C.ink; c.lineWidth = 2.4;
    c.lineJoin = 'round'; c.stroke(back); c.globalAlpha = 1;

    const face = new Path2D();                       // 正面
    face.moveTo(bx0, BY); face.lineTo(bx1, BY);
    face.lineTo(tx1, ty); face.lineTo(tx0, ty); face.closePath();
    c.fillStyle = C.paper; c.fill(face);

    c.save(); c.clip(face);                          // 面上仍是方格纸
    for (let k = 1; k <= 3; k++) {
      const p = k / 4, y = lerp(BY, ty, p);
      line(c, wob(lerp(bx0, tx0, p) + 5, y, lerp(bx1, tx1, p) - 5, y, i * 11 + k, 1.1, 6), C.soft, 1.7, 0.3);
      line(c, wob(lerp(bx0, bx1, p), BY, lerp(tx0, tx1, p), ty, i * 17 + k, 1.1, 6), C.soft, 1.7, 0.24);
    }
    c.restore();

    line(c, wob(bx0, BY, bx1, BY, i * 5 + 1, 0.7, 8), C.ink, 3.3, 0.9);
    line(c, wob(bx1, BY, tx1, ty, i * 5 + 2, 0.7, 8), C.ink, 3.3, 0.9);
    line(c, wob(tx1, ty, tx0, ty, i * 5 + 3, 0.7, 8), C.ink, 3.3, 0.9);
    line(c, wob(tx0, ty, bx0, BY, i * 5 + 4, 0.7, 8), C.ink, 3.3, 0.9);
  };

  return {
    draw(c, lt, t) {
      c.fillStyle = C.bg; c.fillRect(0, 0, W, H);
      const cam = lerp(-140, 140, ease.inOut(clamp(lt / DUR)));   // 横移
      c.save(); c.translate(cam, 0);

      for (let k = 2; k >= 1; k--) {                 // 一叠纸的侧边
        c.globalAlpha = 0.3; c.strokeStyle = C.ink; c.lineWidth = 2;
        c.strokeRect(PX + k * 7, PY + k * 7, PW, PH);
      }
      c.globalAlpha = 1;
      c.fillStyle = C.paper; c.fillRect(PX, PY, PW, PH);

      const rx = lerp(GX - 320, GX + COLS * CELL + 320, ss(0, 2.8, lt)); // 铅笔从左边扫过来
      const dim = lerp(1, 0.4, ss(11.2, 12.6, lt));                     // 收束：只留下三张
      for (let i = 0; i < COLS; i++) {
        const x = GX + i * CELL;
        const a = clamp((rx - x) / 300) * dim;
        if (a < 0.02) continue;
        for (let j = 0; j < ROWS; j++) {
          if ((i + j) % 2) continue;
          c.globalAlpha = 0.07 * a; c.fillStyle = C.soft;
          c.fillRect(x, GY + j * CELL, CELL, CELL);
        }
        c.globalAlpha = 1;
        line(c, wob(x, GY, x, GY + ROWS * CELL, i * 3 + 1, 1.6, 9), C.ink, 2.3, 0.3 * a);
      }
      const ah = clamp((rx - GX - 216) / 300) * dim;
      if (ah > 0.02) {
        const w0 = Math.max(GX + 40, Math.min(rx - 12, GX + COLS * CELL));
        for (let j = 0; j <= ROWS; j++) {
          line(c, wob(GX, GY + j * CELL, w0, GY + j * CELL, j * 5 + 61, 1.6, 20), C.ink, 2.3, 0.3 * ah);
        }
      }

      for (const cd of CARDS) {                      // 出发点的小格
        const cx = GX + (cd[0] + 0.5) * CELL;
        c.globalAlpha = 0.45; c.strokeStyle = C.ink; c.lineWidth = 2.2;
        c.strokeRect(cx - CELL / 2 + 9, BY - CELL + 9, CELL - 18, CELL - 18);
        c.globalAlpha = 1;
      }
      for (let i = 0; i < CARDS.length; i++) {       // 三张依次立起
        card(c, GX + (CARDS[i][0] + 0.5) * CELL, ss(CARDS[i][1], CARDS[i][1] + 2.0, lt), t, i);
      }
      c.restore();

      const tp = ss(7.8, 8.7, lt);                   // 屏上字
      if (tp > 0.01) {
        c.save(); c.globalAlpha = tp; c.fillStyle = C.ink;
        c.font = "italic 62px 'KaiTi','STKaiti','Kaiti SC',serif";
        c.textAlign = 'left'; c.textBaseline = 'middle';
        c.fillText('挑出三个', 140, 210);
        const uw = 240 * tp;
        line(c, wob(140, 286, 140 + uw, 286, 7, 2.2, 10), C.red, 3, 0.85);
        c.restore();
      }
    },
  };
})();
