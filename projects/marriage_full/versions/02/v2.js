// 页02｜钩子：一道纸裂缝从纸的底边慢慢往上爬，缝里露出后面的暗色，屏上字「窗户纸」
SCENES['02'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ss, ease, rng } = U;
  const C = { bg: '#F3EDE2', paper: '#FBF8F2', ink: '#1B1A17', gray: '#6B655B', red: '#C8402F', teal: '#2F5D62' };
  const LW = 4.5;                                    // 一支笔：全页只有一个线宽

  // ---------- 纸：一张略斜的纸，四周留白 ----------
  const SX = 400, SY = 120, SW = 1180, SH = 860, SR = 16;
  const CX = SX + SW / 2, CY = SY + SH / 2;
  const sheet = (() => {
    const p = new Path2D();
    p.moveTo(SX + SR, SY);
    p.arcTo(SX + SW, SY, SX + SW, SY + SH, SR);
    p.arcTo(SX + SW, SY + SH, SX, SY + SH, SR);
    p.arcTo(SX, SY + SH, SX, SY, SR);
    p.arcTo(SX, SY, SX + SW, SY, SR);
    p.closePath(); return p;
  })();
  const ink = (c, path, fill, lw = LW) => {
    if (fill) { c.fillStyle = fill; c.fill(path); }
    if (lw) { c.strokeStyle = C.ink; c.lineWidth = lw; c.lineJoin = 'round'; c.lineCap = 'round'; c.stroke(path); }
  };

  // ---------- 裂缝中心线：从纸的底边起，一路往上爬（占画高约七成）----------
  const N = 46, BY = SY + SH, TY = BY - H * 0.70;
  const CL = [];
  {
    const r = rng(2026);
    for (let i = 0; i < N; i++) {
      const u = i / (N - 1);
      const y = lerp(BY, TY, Math.pow(u, 1.02));
      const base = lerp(1182, 1140, Math.pow(u, 0.9));
      const wob = Math.sin(u * 9.3) * 15 + Math.sin(u * 4.1 + 0.7) * 11;
      const zig = (i % 2 ? 1 : -1) * (1.5 + r() * 3);          // 撕裂的细毛边：一笔的抖，不成锯齿块
      CL.push([base + wob + zig + (r() * 2 - 1) * 3, y]);
    }
  }
  const NM = [];
  for (let i = 0; i < N; i++) {
    const a = CL[Math.max(0, i - 1)], b = CL[Math.min(N - 1, i + 1)];
    const dx = b[0] - a[0], dy = b[1] - a[1], d = Math.sqrt(dx * dx + dy * dy) || 1;
    NM.push([-dy / d, dx / d]);                              // 法线（指向右）
  }

  // ---------- 裂缝什么时候爬到哪个位置（这一页的四拍）----------
  const KEY = [[0, 0, 0.7], [2.6, 0.40, 1], [3.1, 0.43, 1], [7.0, 0.90, 1], [9.0, 1.0, 1]];
  const crackAt = (x) => {
    if (x <= 0) return 0;
    for (let i = 0; i < KEY.length - 1; i++) {
      const ta = KEY[i][0], va = KEY[i][1], tb = KEY[i + 1][0], vb = KEY[i + 1][1];
      if (x <= tb) return lerp(va, vb, Math.pow(clamp((x - ta) / (tb - ta)), KEY[i][2]));
    }
    return 1;
  };
  const timeAt = (v) => {
    let lo = 0, hi = 10.5;
    for (let i = 0; i < 24; i++) { const m = (lo + hi) / 2; if (crackAt(m) < v) lo = m; else hi = m; }
    return (lo + hi) / 2;
  };

  // ---------- 纸纤维小齿 / 纸纹（种子随机，全部固定）----------
  const OMAX = 24;                                    // 底边处缝张开的半宽（裂缝整体加粗）
  const OA = [], FT = [], GR = [];
  {
    const r = rng(77);
    for (let i = 0; i < N; i++) OA.push([0.72 + r() * 0.56, 0.72 + r() * 0.56]);   // 两片纸的错口
    for (let k = 0; k < 12; k++) FT.push({ u: 0.08 + 0.8 * r(), len: 7 + r() * 6, ph: r(), t0: 0 });
    for (let k = 0; k < 44; k++) GR.push({ x: r(), y: r(), a: 0.05 + r() * 0.09, s: 1.6 + r() * 2.8 });
  }
  for (const ft of FT) ft.t0 = timeAt(ft.u) + ft.ph * 0.25;

  // ---------- 屏上字：窗户纸（竖排，一笔一笔写出来）----------
  const LAB = ['窗', '户', '纸'];
  const drawLabel = (c, lt) => {
    c.save();
    c.textAlign = 'center';
    c.textBaseline = 'middle';
    c.fillStyle = C.ink;
    c.font = '600 108px "LXGWWenKai-500"';
    for (let i = 0; i < LAB.length; i++) {
      const st = 6.55 + i * 0.42;
      const q = ss(st, st + 0.55, lt);
      if (q <= 0) continue;
      const x = 212, y = 372 + i * 152;
      c.save();
      c.beginPath(); c.rect(x - 78, y - 84, 156, 168 * q); c.clip();     // 从上往下写出来
      c.globalAlpha = ss(st, st + 0.32, lt);
      c.fillText(LAB[i], x, y + (1 - q) * 10);
      c.restore();
    }
    c.restore();
  };

  return {
    draw(c, lt, t) {
      const g = crackAt(lt);                                   // 裂缝爬到哪儿（0..1）
      const fr = Math.floor(lt * 12);                          // 12fps 的手绘抖笔
      const bl = (i) => (U.hash(i * 131 + 7, fr) * 2 - 1) * 1.2;   // 同一支笔、同一个抖动种子：整条缝一起抖

      // 1) 背景（每帧自己画）
      c.fillStyle = C.bg; c.fillRect(0, 0, W, H);

      // 2) 纸落下来、轻轻转正（镜头是停的，动的是纸自己）
      const set = ease.out(clamp((lt - 0.15) / 1.4));
      const ang = (1 - set) * -0.052 + Math.sin(lt * 7.6) * 0.011 * (1 - set);
      c.save();
      c.translate(CX, CY);
      c.rotate(ang);
      c.translate(-CX, -CY - (1 - set) * 34);

      // 3) 纸下的影
      c.save();
      c.globalAlpha = 0.14 * (0.35 + 0.65 * set);
      c.fillStyle = C.gray;
      c.translate(22, 26); c.fill(sheet);
      c.restore();

      // 4) 纸面
      c.save();
      c.clip(sheet);
      c.fillStyle = C.paper; c.fillRect(SX - 60, SY - 60, SW + 120, SH + 120);
      c.fillStyle = C.gray;
      for (const p of GR) { c.globalAlpha = p.a; c.beginPath(); c.arc(SX + p.x * SW, SY + p.y * SH, p.s * 0.5, 0, TAU); c.fill(); }
      c.globalAlpha = 1;

      // 5) 裂缝：尖端先过去，两片纸才慢慢让开；缝里露出后面的暗色
      const f = g * (N - 1);
      const k = Math.max(0, Math.min(Math.floor(f), N - 2));
      const ti = clamp(f - k, 0, 1);                            // 尖端落在 CL[k] → CL[k+1] 之间
      const OL = [], OR = [];
      for (let i = 0; i <= k; i++) {
        const u = i / (N - 1);
        const pass = clamp((f - i) / 3.6);                                   // 尖端过去后 3.6 个点才张开
        const wide = OMAX * Math.pow(1 - u, 1.05) * ss(0, 1, pass) * lerp(0.8, 1.15, ss(6, 10, lt));
        OL.push(Math.max(0, wide * OA[i][0]));
        OR.push(Math.max(0, wide * OA[i][1]));
      }
      // 中心线 + 左右两条缘：沿中心线对称张开，同一次手抖整体位移，不产生错位重影
      const LP = [], RP = [];
      for (let i = 0; i <= k; i++) {
        const tr = bl(i);
        const px = CL[i][0] + NM[i][0] * tr, py = CL[i][1] + NM[i][1] * tr;
        LP.push([px - NM[i][0] * OL[i], py - NM[i][1] * OL[i]]);
        RP.push([px + NM[i][0] * OR[i], py + NM[i][1] * OR[i]]);
      }
      const tip = [lerp(CL[k][0], CL[k + 1][0], ti), lerp(CL[k][1], CL[k + 1][1], ti)];

      // 6) 一条 path 画完整道缝：左缘上行 → 尖端锥形收细 → 右缘下行；
      //    与纸边线共用同一支笔（同线宽、同圆头圆接）
      if (g > 0.001) {
        const tear = new Path2D();
        tear.moveTo(LP[0][0], LP[0][1]);
        for (let i = 1; i <= k; i++) tear.lineTo(LP[i][0], LP[i][1]);
        tear.lineTo(tip[0], tip[1]);
        for (let i = k; i >= 0; i--) tear.lineTo(RP[i][0], RP[i][1]);
        tear.closePath();
        ink(c, tear, C.teal);
      }

      // 7) 撕口边的纸纤维小齿：沿裂缝中心线左右对称、紧贴撕口（同一支笔）
      c.save();
      c.strokeStyle = C.ink; c.lineWidth = LW; c.lineCap = 'round'; c.lineJoin = 'round';
      for (const ft of FT) {
        const up = ss(ft.t0, ft.t0 + 0.22, lt);
        if (up <= 0) continue;
        const i = Math.min(Math.round(ft.u * (N - 1)), k);
        if (OL[i] < 1 || OR[i] < 1) continue;                 // 还没张开的细口上不长齿
        const L = ft.len * up;
        c.globalAlpha = 0.85 * up;
        c.beginPath();
        c.moveTo(LP[i][0], LP[i][1]);
        c.lineTo(LP[i][0] - NM[i][0] * L, LP[i][1] - NM[i][1] * L);
        c.moveTo(RP[i][0], RP[i][1]);
        c.lineTo(RP[i][0] + NM[i][0] * L, RP[i][1] + NM[i][1] * L);
        c.stroke();
      }
      c.restore();

      // 8) 收束：红色顶端并入同一条裂缝 path，线宽一致，末端锥形收细，不独立成段
      const rq = ss(8.85, 9.5, lt);
      if (rq > 0.01 && g > 0.001) {
        const i1 = Math.min(Math.max(0, Math.floor((g - 0.055) * (N - 1))), k);
        const red = new Path2D();
        red.moveTo(LP[i1][0], LP[i1][1]);
        for (let i = i1 + 1; i <= k; i++) red.lineTo(LP[i][0], LP[i][1]);
        red.lineTo(tip[0], tip[1]);
        for (let i = k; i >= i1; i--) red.lineTo(RP[i][0], RP[i][1]);
        c.save();
        c.globalAlpha = 0.95 * rq; c.strokeStyle = C.red; c.lineWidth = LW; c.lineCap = 'round'; c.lineJoin = 'round';
        c.stroke(red);
        c.restore();
      }
      c.restore();                                   // 结束纸面裁剪

      // 9) 纸的轮廓（细铅笔线）
      ink(c, sheet, null);
      c.restore();                                   // 结束纸的位移/旋转

      // 10) 屏上字
      drawLabel(c, lt);
    },
  };
})();
