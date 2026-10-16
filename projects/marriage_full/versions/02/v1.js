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

  // ---------- 裂缝中心线：从纸的底边起，一路往上爬 ----------
  const N = 46, BY = SY + SH, TY = 300;
  const CL = [];
  {
    const r = rng(2026);
    for (let i = 0; i < N; i++) {
      const u = i / (N - 1);
      const y = lerp(BY, TY, Math.pow(u, 1.02));
      const base = lerp(1182, 1140, Math.pow(u, 0.9));
      const wob = Math.sin(u * 9.3) * 15 + Math.sin(u * 4.1 + 0.7) * 11;
      const zig = (i % 2 ? 1 : -1) * (4 + r() * 8);          // 撕裂的锯齿
      CL.push([base + wob + zig + (r() * 2 - 1) * 5, y]);
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

  // ---------- 纸屑 / 纤维 / 纸纹（种子随机，全部固定）----------
  const OMAX = 17;                                    // 底边处缝张开的半宽
  const OA = [], WK = [], FLK = [], GR = [];
  {
    const r = rng(77);
    for (let i = 0; i < N; i++) OA.push([0.72 + r() * 0.56, 0.72 + r() * 0.56]);   // 两片纸的错口
    for (let k = 0; k < 20; k++) WK.push({ u: 0.05 + 0.9 * r(), s: r() < 0.5 ? -1 : 1, len: 16 + r() * 30, ph: r(), t0: 0 });
    for (let k = 0; k < 8; k++) FLK.push({ u: 0.06 + 0.78 * r(), o: (r() * 2 - 1) * 12, sz: 6 + r() * 7, ph: r(), rot: (r() * 2 - 1) * 1.4, t0: 0 });
    for (let k = 0; k < 44; k++) GR.push({ x: r(), y: r(), a: 0.05 + r() * 0.09, s: 1.6 + r() * 2.8 });
  }
  for (const w of WK) w.t0 = timeAt(w.u);
  for (const f of FLK) f.t0 = timeAt(f.u) + f.ph * 0.35;

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
      const bl = (i, k) => (U.hash(i * 131 + k, fr) * 2 - 1) * 1.5;

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

      // 5) 裂缝：尖端先过去，两片纸才慢慢让开，缝里露出后面的暗色
      const f = g * (N - 1);
      const k = Math.min(Math.floor(f), N - 2);
      const ke = Math.min(k + 1, N - 1);
      const OL = [], OR = [];
      for (let i = 0; i <= ke; i++) {
        const u = i / (N - 1);
        const pass = clamp((f - i) / 3.6);                                   // 尖端过去后 3.6 个点才张开
        const wide = OMAX * Math.pow(1 - u, 1.05) * ss(0, 1, pass) * lerp(0.8, 1.15, ss(6, 10, lt));
        OL.push(Math.max(0, wide * OA[i][0] + bl(i, 1)));
        OR.push(Math.max(0, wide * OA[i][1] + bl(i, 2)));
      }
      const at = (arr, i) => [CL[i][0] + NM[i][0] * arr[i], CL[i][1] + NM[i][1] * arr[i]];
      const LP = [], RP = [];
      for (let i = 0; i <= ke; i++) { LP.push(at(OL, i)); RP.push(at(OR, i)); }

      // 抬起的纸唇：缝口两边各一道浅浅的暗（平涂，不发光）
      c.fillStyle = C.gray;
      if (ke >= 1) {
        const lip = (arr, sign, w, a) => {
          const pts = [];
          for (let i = 0; i <= ke; i++) pts.push(at(arr, i));
          for (let i = ke; i >= 0; i--) {
            const o = arr[i] + sign * w;
            pts.push([CL[i][0] + NM[i][0] * o, CL[i][1] + NM[i][1] * o]);
          }
          c.globalAlpha = a; c.fill(U.poly(pts, true));
        };
        lip(OR, 1, 12, 0.18);
        lip(OL, -1, 12, 0.10);
        c.globalAlpha = 1;
      }

      // 6) 还没张开的那一段：一根细的裂口线，先于缝往上走
      if (ke >= 1) {
        c.save();
        c.globalAlpha = 0.9; c.strokeStyle = C.ink; c.lineWidth = LW * 0.8; c.lineCap = 'round'; c.lineJoin = 'round';
        const seg = [];
        for (let i = 0; i <= ke; i++) seg.push(CL[i]);
        seg.push(at(OL, ke));
        c.stroke(U.poly(seg, false));
        c.restore();
      }

      // 7) 缝：两片纸让开，露出后面的暗色
      if (ke >= 1 && OR[ke] > 0.2) {
        const poly = [];
        for (let i = 0; i <= ke; i++) poly.push(LP[i]);
        for (let i = ke; i >= 0; i--) poly.push(RP[i]);
        c.save(); c.globalAlpha = 0.92; c.fillStyle = C.teal; c.fill(U.poly(poly, true)); c.restore();
      }
      // 撕口的两条边
      if (ke >= 1) {
        c.save();
        c.strokeStyle = C.ink; c.lineWidth = LW; c.lineCap = 'round'; c.lineJoin = 'round';
        c.stroke(U.poly(LP, false));
        c.stroke(U.poly(RP, false));
        c.restore();
      }

      // 8) 撕口上翘起来的纸纤维
      c.save();
      c.strokeStyle = C.gray; c.lineWidth = 2.4; c.lineCap = 'round';
      for (const w of WK) {
        const rev = ss(w.t0, w.t0 + 0.28, lt);
        if (rev <= 0) continue;
        const i = Math.min(Math.round(w.u * (N - 1)), ke);
        const o = w.s > 0 ? OR[i] : OL[i];
        const bx = CL[i][0] + NM[i][0] * o * w.s, by = CL[i][1] + NM[i][1] * o * w.s;
        const nx = NM[i][0] * w.s, ny = NM[i][1] * w.s;
        const L = w.len * rev * (1 + 0.08 * Math.sin(lt * 5 + w.ph * 8));
        c.globalAlpha = 0.5 * rev;
        c.beginPath();
        c.moveTo(bx, by);
        c.lineTo(bx + nx * L * 0.82 - ny * L * 0.45, by + ny * L * 0.82 + nx * L * 0.45);
        c.stroke();
      }
      c.restore();

      // 9) 掉下来的纸屑
      for (const fl of FLK) {
        const age = lt - fl.t0;
        if (age <= 0 || age > 2.6) continue;
        const a = ss(0, 0.2, age) * (1 - ss(1.5, 2.6, age));
        if (a <= 0.01) continue;
        const i = Math.min(Math.round(fl.u * (N - 1)), ke);
        const s = fl.sz * (1 - age * 0.18);
        c.save();
        c.translate(CL[i][0] + fl.o + Math.sin(age * 3.4 + fl.ph * 9) * 7, CL[i][1] + 90 * age + 30 * age * age);
        c.rotate(fl.rot + age * 1.1);
        c.globalAlpha = a * 0.9;
        const q = [[-s * 0.5, -s * 0.3], [s * 0.6, -s * 0.5], [s * 0.35, s * 0.5], [-s * 0.45, s * 0.35]];
        c.fillStyle = C.paper; c.fill(U.poly(q, true));
        c.strokeStyle = C.gray; c.lineWidth = 2; c.stroke(U.poly(q, true));
        c.restore();
      }

      // 10) 收束：裂缝尖上那一小段红——这一页唯一的重音
      const rq = ss(8.85, 9.5, lt);
      if (rq > 0.01) {
        const i1 = Math.max(0, Math.floor((g - 0.055) * (N - 1)));
        const seg = [];
        for (let i = i1; i <= ke; i++) seg.push(CL[i]);
        const tipIdx = clamp(f, 0, N - 1), i0 = Math.min(Math.floor(tipIdx), N - 2), uu = tipIdx - i0;
        const tip = [lerp(CL[i0][0], CL[i0 + 1][0], uu), lerp(CL[i0][1], CL[i0 + 1][1], uu)];
        seg.push(tip);
        if (seg.length > 1) {
          c.save();
          c.globalAlpha = 0.95 * rq; c.strokeStyle = C.red; c.lineWidth = LW; c.lineCap = 'round'; c.lineJoin = 'round';
          c.stroke(U.poly(seg, false));
          c.restore();
        }
        c.save();
        c.globalAlpha = rq; c.fillStyle = C.red;
        c.beginPath(); c.arc(tip[0], tip[1], 4.4 * rq, 0, TAU); c.fill();
        c.restore();
      }
      c.restore();                                   // 结束纸面裁剪

      // 11) 纸的轮廓（细铅笔线）
      ink(c, sheet, null);
      c.restore();                                   // 结束纸的位移/旋转

      // 12) 屏上字
      drawLabel(c, lt);
    },
  };
})();
