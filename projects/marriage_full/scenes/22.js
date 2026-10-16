// 22｜行动与落点·第一步不是向外补偿，而是先看清两个点：一支笔在纸上点出两个圈——第一帧压痕已在、笔已入场；0.45~4.30 画第一圈（起笔先落一个实心点）、4.30~4.75 抬笔平移、4.75~8.30 画第二圈、0.60*dur 出字「先看清两点」、0.85*dur 两点压红收束；镜头全程快推。
SCENES['22'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ss, ease, rng } = U;
  const C = { bg: '#F3EDE2', paper: '#FBF8F2', ink: '#1B1A17', gray: '#6B655B', red: '#C8402F', teal: '#2F5D62' };
  const DUR = 14;
  // 主角＝两个圈本身：两圈合起来横跨 1040px（画面 54%），单个直径 480px（画面 44%）；纸只是载体
  const AX = 680, BX = 1240, CY = 540, R = 240;
  const T1 = 0.45, D1 = 3.85, T2 = 4.75, D2 = 3.55, TT = DUR * 0.6, TS = DUR * 0.85;   // 0.60*dur 出字、0.85*dur 收束

  // 全片同一支笔：分段描边，线宽在 1.5~2.5 倍之间自然扰动，圆头圆角，不做第二套笔触
  const pen = (c, pts, w, seed, taper, a, col) => {
    if (!pts || pts.length < 2) return;
    const r = rng(seed);
    c.save(); c.globalAlpha = a === undefined ? 1 : a; c.strokeStyle = col || C.ink;
    c.lineCap = 'round'; c.lineJoin = 'round';
    for (let i = 1; i < pts.length; i++) {
      const s = i / (pts.length - 1), tp = taper ? clamp((1 - s) / taper) : 1;
      c.lineWidth = w * (0.8 + r() * 0.5) * (0.4 + 0.6 * tp);
      c.beginPath(); c.moveTo(pts[i - 1][0], pts[i - 1][1]); c.lineTo(pts[i][0], pts[i][1]); c.stroke();
    }
    c.restore();
  };
  // 圈：一条首尾重合的闭合曲线，整页只沿它长大，不换身份
  const ring = (cx, a0, seed) => {
    const r0 = rng(seed), o = [], N = 112;
    for (let i = 0; i <= N; i++) {
      const a = a0 + (i / N) * TAU;
      const rr = R * (1 + 0.012 * Math.sin(a * 3.1 + 1.2) + 0.007 * Math.sin(a * 6.3 + 0.4) + 0.006 * (r0() * 2 - 1));
      o.push([cx + Math.cos(a) * rr, CY + Math.sin(a) * rr]);
    }
    o[N] = o[0].slice();
    return o;
  };
  const AR = ring(AX, -2.30, 2201), BR = ring(BX, -0.80, 2202);
  const at = (o, p) => {
    const i = clamp(p) * (o.length - 1), k = Math.min(Math.floor(i), o.length - 2), f = i - k;
    return [lerp(o[k][0], o[k + 1][0], f), lerp(o[k][1], o[k + 1][1], f)];
  };
  const tan = (o, p) => {
    const a = at(o, Math.max(0, p - 0.03)), b = at(o, Math.min(1, p + 0.03));
    return Math.atan2(b[1] - a[1], b[0] - a[0]);
  };
  const cut = (o, p) => {
    const n = Math.max(2, Math.min(o.length, Math.ceil(clamp(p) * (o.length - 1)) + 1));
    return o.slice(0, n);
  };
  const arcPts = (cx, cy, rr, a0, sweep, n) => {
    const o = [];
    for (let i = 0; i <= n; i++) { const a = a0 + sweep * i / n; o.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]); }
    return o;
  };
  // 笔尖一路贴着走；抬笔平移那一段离纸面
  const penAt = (lt) => {
    const p1 = clamp((lt - T1) / D1), p2 = clamp((lt - T2) / D2);
    let x, y, ang, a = 0.3 + 0.7 * clamp(lt / 0.35);
    if (lt < T1) {
      const q = ease.out(clamp(lt / T1)), s = at(AR, 0);
      x = s[0] - 300 * (1 - q); y = s[1] - 190 * (1 - q); ang = tan(AR, 0.04) + 0.9 * (1 - q);
    } else if (p1 < 1) {
      const s = at(AR, p1); x = s[0]; y = s[1]; ang = tan(AR, p1);
    } else if (lt < T2) {
      const q = ease.inOut(clamp((lt - T1 - D1) / (T2 - T1 - D1)));
      const e = at(AR, 1), s = at(BR, 0);
      x = lerp(e[0], s[0], q); y = lerp(e[1], s[1], q) - 110 * Math.sin(q * Math.PI);
      ang = Math.atan2(s[1] - e[1], s[0] - e[0]);
    } else if (p2 < 1) {
      const s = at(BR, p2); x = s[0]; y = s[1]; ang = tan(BR, p2);
    } else {
      const q = ease.out(clamp((lt - T2 - D2) / 1.5)), e = at(BR, 1);
      x = e[0] + 300 * q; y = e[1] - 320 * q; ang = -0.6;
      a *= 1 - clamp((lt - T2 - D2 - 0.8) / 0.7);
    }
    return { x, y, ang, a };
  };
  const drawPen = (c, s) => {
    if (s.a <= 0.01) return;
    c.save(); c.translate(s.x, s.y); c.rotate(s.ang + Math.PI); c.globalAlpha = s.a;
    const nib = U.poly([[0, 0], [34, -9], [40, -9], [40, 9], [34, 9]], true);
    c.fillStyle = C.ink; c.fill(nib);
    const body = U.poly([[38, -12], [196, -13], [210, -6], [214, 0], [210, 6], [196, 13], [38, 12]], true);
    c.fillStyle = C.teal; c.fill(body);
    pen(c, body, 2.4, 2244, 0, 0.8);              // 同一支笔勾笔杆轮廓
    c.fillStyle = C.red; c.fillRect(112, -11, 16, 22);
    c.restore();
  };
  // 屏上字：同一支笔的手写感，逐字浮出，落在下方留白
  const handText = (c, s, cx, y, size, a) => {
    const r = rng(2211), ws = [];
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
      const p1 = clamp((lt - T1) / D1), p2 = clamp((lt - T2) / D2);
      const deep = clamp((lt - TS) / 1.5);                       // 0.85*dur 起收束
      c.fillStyle = C.bg; c.fillRect(0, 0, W, H);                 // 每帧自己画背景

      const z = 1 + 0.13 * ease.out(clamp(lt / 5.2));             // 镜头：快推到 1.13 后停稳
      c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2);

      // ① 载体：一张纸
      c.fillStyle = C.paper; c.fillRect(150, 80, 1620, 920);
      c.save(); c.globalAlpha = 0.16; c.strokeStyle = C.gray; c.lineWidth = 2.6;
      c.strokeRect(150, 80, 1620, 920); c.restore();

      // ② 起笔前的极淡压痕：第一帧就交代两个圈的位置和走向
      const gAl = 0.15 * (1 - deep) + 0.03;
      c.save(); c.setLineDash([30, 22]);
      pen(c, AR, 3.0, 3301, 0, gAl); pen(c, BR, 3.0, 3302, 0, gAl);
      c.restore();

      // ③ 主角：同一支笔沿同一个圈长出来（收束时加深、加粗一档）
      const lw = 6.0 + 1.6 * deep, al = 0.9 + 0.1 * deep;
      if (p1 > 0.004) pen(c, cut(AR, p1), lw, 2211, 0.08, al);
      if (p2 > 0.004) pen(c, cut(BR, p2), lw, 2212, 0.08, al);

      // ④ 起笔先落一个实心点；收束时两点压深、各加一圈红
      const dot = (o, d) => {
        if (d <= 0) return;
        const rr = (11 + 6 * deep) * ease.out(d);
        c.save(); c.globalAlpha = 0.92; c.fillStyle = C.ink;
        c.beginPath(); c.arc(o[0], o[1], rr, 0, TAU); c.fill(); c.restore();
        if (deep > 0.02) pen(c, arcPts(o[0], o[1], rr + 9, -2.4, 4.6 * deep, 22), 3.2, 2213, 0, 0.8 * deep, C.red);
      };
      dot(AR[0], clamp((lt - T1) / 0.5));
      dot(BR[0], clamp((lt - T2) / 0.5));

      // ⑤ 笔：贴着笔尖走，画完抬走
      drawPen(c, penAt(lt));
      c.restore();

      // ⑥ 0.60*dur 出字，落在下方留白、居中，不抢重心
      const pt = ss(TT, TT + 1.3, lt);
      if (pt > 0.01) handText(c, '先看清两点', 960, 940, 54, pt);
    }
  };
})();
