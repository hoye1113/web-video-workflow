// 25｜行动与落点·一把尺压在纸上、把刻度一道道推出来。镜头停，动的只有尺自己：第一帧只有中间一截尺头和一道极淡压痕（走向已交代）；2.2~7.6s 刻度从中间一截往两头长、一道道被推出来；0.60*dur 出字「看承担后果」；0.85*dur 红印落在长刻度上、穿过尺沿压到纸面，尺身下沉、压痕压深收束。
SCENES['25'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ss, ease, rng } = U;
  const C = { bg: '#F3EDE2', paper: '#FBF8F2', ink: '#1B1A17', gray: '#6B655B', red: '#C8402F', teal: '#2F5D62' };
  const DUR = 14;
  // 主角＝尺本身：全长 1260px = 画面宽的 66%；高 130px 里长刻度占 96px；纸只是载体
  const XC = 930, RY0 = 500, RH = 130, RY1 = RY0 + RH, RLEN = 1260, SLIDE = 72;
  const N = 34, STEP = 34, MAJ = 5, PICK = 20;
  const TXT = '看承担后果', TX = 1180, TY = 246, TFS = 52;

  const P = (p) => U.poly(p, true);
  // 全片同一支笔：一根线里线宽在 0.6~1.5 倍之间平滑起伏，圆头圆角，不做第二套笔触
  const pen = (c, pts, w, seed, a, col) => {
    if (!pts || pts.length < 2) return;
    const r = rng(seed), ph = r() * TAU, k = 0.85 + r() * 0.3;
    c.save();
    c.globalAlpha = a === undefined ? 1 : a;
    c.strokeStyle = col || C.ink;
    c.lineCap = 'round'; c.lineJoin = 'round';
    for (let i = 1; i < pts.length; i++) {
      const u = i / (pts.length - 1);
      c.lineWidth = w * k * (1 + 0.28 * Math.sin(u * 5.2 + ph));
      c.beginPath(); c.moveTo(pts[i - 1][0], pts[i - 1][1]); c.lineTo(pts[i][0], pts[i][1]); c.stroke();
    }
    c.restore();
  };
  // 一条抖动的直笔迹：起伏是连续的弧，不是锯齿；起笔收笔都落在端点上
  const seg = (ax, ay, bx, by, amp, seed, sub) => {
    const r = rng(seed), ph = r() * TAU, o = [[ax, ay]];
    const dx = bx - ax, dy = by - ay, L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
    sub = sub || 3;
    for (let k = 1; k <= sub; k++) {
      const u = k / sub;
      const oo = (k === sub) ? 0 : amp * (0.75 * Math.sin(u * 2.4 + ph) + 0.25 * (r() * 2 - 1));
      o.push([ax + dx * u + nx * oo, ay + dy * u + ny * oo]);
    }
    return o;
  };
  const rect = (x0, y0, x1, y1, amp, seed) => {
    const o = [], sub = (x1 - x0 > 600) ? 10 : 4;
    const ed = [[x0, y0, x1, y0, seed], [x1, y0, x1, y1, seed + 7],
                [x1, y1, x0, y1, seed + 13], [x0, y1, x0, y0, seed + 19]];
    for (const e of ed) {
      const s = seg(e[0], e[1], e[2], e[3], amp, e[4], sub);
      for (let i = 0; i < s.length - 1; i++) o.push(s[i]);
    }
    o.push(o[0]);
    return o;
  };
  // 屏上字：同一支笔的手写感，逐字浮出，落在上方留白区
  const handText = (c, s, cx, y, size, a) => {
    const r = rng(2511), ws = [];
    let tw = size * 0.06 * (s.length - 1);
    c.save(); c.fillStyle = C.ink; c.font = '500 ' + size + 'px "LXGWWenKai-500"'; c.textBaseline = 'middle';
    for (const ch of s) { const w = c.measureText(ch).width; ws.push(w); tw += w; }
    let x = cx - tw / 2;
    for (let i = 0; i < s.length; i++) {
      const ca = clamp(a * 1.8 - i * 0.16), w = ws[i];
      if (ca > 0.01) {
        c.save(); c.globalAlpha = ca; c.translate(x + w / 2, y + (r() - 0.5) * 5 + (1 - ca) * 10);
        c.rotate((r() - 0.5) * 0.04); c.fillText(s[i], -w / 2, 0); c.restore();
      }
      x += w + size * 0.06;
    }
    c.restore();
  };

  return {
    draw(c, lt, t) {
      c.fillStyle = C.bg; c.fillRect(0, 0, W, H);                        // 每帧自己画背景

      // ① 载体：一张纸
      c.fillStyle = C.paper; c.fill(P(rect(200, 96, 1720, 984, 2.6, 11)));
      pen(c, rect(200, 96, 1720, 984, 2.6, 11), 2.8, 12, 0.26, C.gray);

      // ② 尺的走向：第一帧就有的压痕，0.85*dur 起压深
      const deep = clamp((lt - 11.6) / 1.4);
      pen(c, seg(268, 674, 1652, 674, 5, 21, 14), 3.4, 21, 0.16 + 0.26 * deep, C.gray);

      // ③ 主角：尺从中间一截往两头长出来，全程缓慢往前推，收束时压沉一下
      const g = ease.out(clamp(lt / 2.8));
      const sl = SLIDE * ease.inOut(clamp((lt - 1.4) / 10.4));
      const pr = 6 * ss(11.9, 12.6, lt);
      const half = lerp(120, RLEN / 2, g);            // 从中间一截往两头长，重心始终在中间
      const x0 = XC - half + sl, x1 = XC + half + sl, y0 = RY0 + pr, y1 = RY1 + pr;
      const base = y1 - 22;
      c.fillStyle = C.bg; c.fill(P(rect(x0, y0, x1, y1, 2.4, 31)));       // 亮面
      c.fillStyle = C.gray; c.globalAlpha = 0.18;                          // 暗面一档
      c.fill(P(rect(x0 + 8, y1 - 26, x1 - 8, y1 - 6, 1.6, 41)));
      c.globalAlpha = 1;

      // ④ 刻度：被尺一路推出来，一道道生长；长刻度几乎顶到尺的上沿
      for (let i = 0; i < N; i++) {
        const tg = ease.outBack(clamp((lt - (2.2 + 5.2 * i / (N - 1))) / 0.5));
        if (tg < 0.02) continue;
        const x = x0 + 40 + i * STEP;
        if (x > x1 - 60) continue;
        const mm = i % MAJ === 0, hh = (mm ? 96 : 46) * clamp(tg, 0, 1.08);
        pen(c, seg(x, base, x, base - hh, 1.2, 200 + i, 3), mm ? 4.6 : 3.4, 200 + i);
      }
      pen(c, rect(x0, y0, x1, y1, 2.4, 31), 4.6, 31);                      // 轮廓压回最上层

      // ⑤ 0.85*dur 收束：红印正好落在第 20 道长刻度上，穿过尺沿压到纸面
      const rg = ease.out(clamp((lt - 11.9) / 0.7));
      if (rg > 0.02) {
        const rx = x0 + 40 + PICK * STEP;
        c.save(); c.globalAlpha = 0.9 * rg; c.strokeStyle = C.red; c.lineCap = 'round';
        c.lineWidth = 8 * (0.9 + 0.2 * rg);
        c.beginPath(); c.moveTo(rx, base - 34); c.lineTo(rx, base + 112 * rg); c.stroke();
        c.restore();
      }

      // ⑥ 0.60*dur 出字，落在上方留白；末尾再补一笔青线收住
      const pt = ss(8.4, 9.7, lt);
      if (pt > 0.01) handText(c, TXT, TX, TY, TFS, pt);
      const ug = ease.out(clamp((lt - 12.5) / 0.8));
      if (ug > 0.02) pen(c, seg(TX - 148, TY + 50, TX - 148 + 296 * ug, TY + 53, 2, 881, 6), 4, 881, 0.85, C.teal);
    }
  };
})();
