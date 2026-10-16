// 垂直切片 · 第 22 镜「一只沙漏 · 细沙一粒粒往下落」
// 画风锁：扁平矢量线稿 —— 米白底、墨线勾勒、砖红与暖黄点缀
// 这一镜是纯代码的强项测试：连续的粒子运动 + 面积增长，图片做不到。
// 预览：index.html?film=compare   渲染：render.py --film compare --solo zz_hourglass --from 0 --to 5
SCENES['22'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ease, rng } = U;
  const C = {
    bg: '#F3EEE6', glass: '#FDFBF7', ink: '#2A2A2A', grey: '#8A8A8A',
    red: '#C8553D', warm: '#E9B872', sand: '#E9B872', sandDk: '#D9A860',
  };
  const LW = 5;
  const ink = (c, path, fill, lw = LW) => {
    if (fill) { c.fillStyle = fill; c.fill(path); }
    if (lw) { c.strokeStyle = C.ink; c.lineWidth = lw; c.lineJoin = 'round'; c.lineCap = 'round'; c.stroke(path); }
  };
  const rrect = (x, y, w, h, r) => { const p = new Path2D(); p.moveTo(x + r, y); p.arcTo(x + w, y, x + w, y + h, r); p.arcTo(x + w, y + h, x, y + h, r); p.arcTo(x, y + h, x, y, r); p.arcTo(x, y, x + w, y, r); p.closePath(); return p; };

  // ---------- 几何 ----------
  const CX = 960, TOP = 258, BOT = 826, HW = 300, NY = 548, NW = 16;
  const TABLE = 884;                                   // 台面（底座正好站上去）
  const SCALE = 1.26;                                  // 整机放大：宽约占画幅 45%（含木盖）、高约 80%，水平居中
  const SANDIN = 9;                                    // 沙面左右顶点向内收，填色不越 V 形线
  const GAP = 8;                                       // 沙堆两脚与玻璃轮廓的间隙：填色不贴底，留 2–4px 视觉缝
  const NECK = NW * 2;                                 // 玻璃颈部全宽
  const STRW = NECK * 0.35;                            // 沙流固定全宽：三帧只改长度，不改宽度
  const glass = (() => {
    const p = new Path2D();
    p.moveTo(CX - HW, TOP);
    p.quadraticCurveTo(CX - HW + 58, NY - 132, CX - NW, NY);
    p.quadraticCurveTo(CX - HW + 58, NY + 132, CX - HW, BOT);
    p.lineTo(CX + HW, BOT);
    p.quadraticCurveTo(CX + HW - 58, NY + 132, CX + NW, NY);
    p.quadraticCurveTo(CX + HW - 58, NY - 132, CX + HW, TOP);
    p.closePath(); return p;
  })();
  // 玻璃左上内壁的二次段：给反光定位，端点严格落在轮廓上
  const WALL = { p0: [CX - HW, TOP], c1: [CX - HW + 58, NY - 132], p1: [CX - NW, NY] };
  const wallAt = t => {
    const a = WALL.p0, b = WALL.c1, d = WALL.p1, m = 1 - t;
    return [m * m * a[0] + 2 * m * t * b[0] + t * t * d[0], m * m * a[1] + 2 * m * t * b[1] + t * t * d[1]];
  };
  // 沙面：控制点 → Catmull-Rom 单调样条重采样，抹掉 1–2px 抖动控制点
  const spline = (pts, per) => {
    const out = [], n = pts.length, at = i => pts[Math.max(0, Math.min(n - 1, i))];
    for (let i = 0; i < n - 1; i++) {
      const p0 = at(i - 1), p1 = at(i), p2 = at(i + 1), p3 = at(i + 2);
      for (let j = 0; j < per; j++) {
        const u = j / per, u2 = u * u, u3 = u2 * u;
        out.push([
          0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * u + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * u2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * u3),
          0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * u + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * u2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * u3),
        ]);
      }
    }
    out.push(pts[n - 1]);
    return out;
  };
  // 沙堆：三帧共用同一归一化轮廓，只改缩放
  const CONE = [[-1, 0], [-0.16, -0.9], [0, -1], [0.16, -0.9], [1, 0]];
  const conePath = (cx, baseY, peakY, hw) => {
    const sy = baseY - peakY, p = new Path2D();
    p.moveTo(cx + CONE[0][0] * hw, baseY + CONE[0][1] * sy);
    p.lineTo(cx + CONE[1][0] * hw, baseY + CONE[1][1] * sy);
    p.quadraticCurveTo(cx, peakY - 0.01 * sy, cx + CONE[3][0] * hw, baseY + CONE[3][1] * sy);
    p.lineTo(cx + CONE[4][0] * hw, baseY + CONE[4][1] * sy);
    p.closePath(); return p;
  };

  // 沙流粒子：36 颗固定相位（种子随机），沿流循环
  const SAND = []; { const r = rng(22); for (let i = 0; i < 36; i++) SAND.push({ o: r() * 2 - 1, ph: r(), sz: 2.6 + r() * 3.4, sp: 0.85 + r() * 0.6 }); }
  // 落点溅起的小点
  const SPL = []; { const r = rng(31); for (let i = 0; i < 14; i++) SPL.push({ a: r() * TAU, ph: r(), d: 20 + r() * 62, sz: 2 + r() * 2.4 }); }
  // 上沙里的颗粒（固定）
  const GRAIN = []; { const r = rng(45); for (let i = 0; i < 90; i++) GRAIN.push({ x: r(), y: r(), a: 0.10 + r() * 0.16, s: 2 + r() * 3.4 }); }

  return {
    draw(c, lt, t) {
      const DUR = 5;
      const p = clamp(lt / DUR);
      const bob = Math.sin(t * 1.1) * 2.6;

      // ---- 背景 + 台面 ----
      c.fillStyle = C.bg; c.fillRect(0, 0, W, H);
      c.save(); c.fillStyle = C.warm; c.globalAlpha = 0.30; c.fillRect(0, TABLE, W, H - TABLE); c.restore();
      c.save(); c.strokeStyle = C.ink; c.lineWidth = LW; c.beginPath(); c.moveTo(0, TABLE); c.lineTo(W, TABLE); c.stroke(); c.restore();
      // 底座下的半透明阴影（玻璃外只留这一处，不再散沙点）；中心右移 60px，与左上光源方向一致
      const SHX = CX + 60;
      c.save(); c.globalAlpha = 0.16; c.fillStyle = C.grey;
      c.beginPath(); c.ellipse(SHX, TABLE - 4, (HW + 74) * SCALE, 20 * SCALE, 0, 0, TAU); c.fill(); c.restore();

      c.save();
      // 整机放大并水平居中：缩放锚在底座，底边仍站在台面上
      c.translate(CX, TABLE); c.scale(SCALE, SCALE); c.translate(-CX, -TABLE);
      c.translate(0, bob);

      // ---- 玻璃腔体 ----
      ink(c, glass, C.glass, LW);

      // 沙量守恒：上腔剩余沙量决定下堆高度（堆高 = 已流光体积 × 系数）
      const KF = [0.65, 0.45, 0.12];                       // 三帧上腔剩余占比
      const VOLK = 0.60 / (1 - KF[KF.length - 1]);         // 第3帧堆高落在玻璃底长的 60%，不顶满
      const seg = clamp(p) * (KF.length - 1);
      const i0 = Math.min(KF.length - 2, Math.floor(seg));
      const fTop = lerp(KF[i0], KF[i0 + 1], seg - i0);
      const fBot = Math.min(0.62, (1 - fTop) * VOLK);      // 由守恒推出，不再各帧手填
      const MX = HW - SANDIN;                                     // 沙面左右顶点（向内收，让填色落在 V 形线内）
      const surfY = lerp(TOP + 40, NY - 24, 1 - fTop);            // 上沙面整体高度
      const dip = lerp(12, 74, 1 - fTop);                         // 沙面中间凹陷（漏斗）随进度加深
      const peakY = BOT - fBot * (BOT - NY);                      // 沙堆顶点高度由沙量守恒算出
      const BASEY = BOT - GAP;                                    // 沙堆两脚离玻璃底线留缝
      const dxB = Math.min(HW - 8, (BASEY - peakY) * 1.15);       // 自然坡度，两脚不顶到玻璃壁

      c.save(); c.clip(glass);

      // ---- 上半：沙面是中间凹下去的漏斗（样条重采样，边缘干净）----
      const SP = spline([
        [CX - MX, surfY - dip * 0.34],
        [CX - MX * 0.62, surfY - dip * 0.02],
        [CX - MX * 0.24, surfY + dip * 0.60],
        [CX, surfY + dip],
        [CX + MX * 0.24, surfY + dip * 0.60],
        [CX + MX * 0.62, surfY - dip * 0.02],
        [CX + MX, surfY - dip * 0.34],
      ], 8);
      const up = new Path2D();
      up.moveTo(SP[0][0], SP[0][1]);
      for (let i = 1; i < SP.length; i++) up.lineTo(SP[i][0], SP[i][1]);
      up.lineTo(CX + MX, NY + 8); up.lineTo(CX - MX, NY + 8); up.closePath();
      ink(c, up, C.sand, 0);
      // 沙面孔隙颗粒：裁在沙体里，绝不越过沙面，坡面不再起毛刺
      c.save(); c.clip(up); c.fillStyle = C.sandDk;
      for (const g of GRAIN) {
        const gx = CX - HW + g.x * HW * 2, gy = surfY + g.y * Math.max(30, NY - surfY) * 0.95;
        c.globalAlpha = g.a; c.beginPath(); c.arc(gx, gy, g.s * 0.5, 0, TAU); c.fill();
      }
      c.restore();
      // 沙面硬边：墨线收口，填色完全落在 V 形线内，不再晕开
      c.save(); c.strokeStyle = C.ink; c.lineWidth = LW; c.lineCap = 'round'; c.lineJoin = 'round';
      c.beginPath(); c.moveTo(SP[0][0], SP[0][1]);
      for (let i = 1; i < SP.length; i++) c.lineTo(SP[i][0], SP[i][1]);
      c.stroke(); c.restore();

      // ---- 下半：沙堆是同一个沙锥，只按沙量改缩放；统一 #E9B872 填充、#2A2A2A 描轮廓 ----
      const hill = conePath(CX, BASEY, peakY, dxB);
      ink(c, hill, C.sand, LW);

      // ---- 沙流：固定宽度贯穿三帧，只改长度；纹理密度随长度等比缩放 ----
      const len = peakY - NY;
      const hwT = STRW * 0.5, hwB = STRW * 0.21;                  // 顶端/收口半宽，固定比例
      const stream = new Path2D();
      stream.moveTo(CX - hwT, NY + 2);
      stream.lineTo(CX + hwT, NY + 2);
      stream.lineTo(CX + hwB, peakY + 6);
      stream.lineTo(CX - hwB, peakY + 6);
      stream.closePath();
      c.fillStyle = '#F2C98A'; c.fill(stream);
      c.save(); c.strokeStyle = C.sandDk; c.lineWidth = 3; c.lineJoin = 'round'; c.stroke(stream); c.restore();
      // 粒子：拉成短竖线（运动模糊），条数随长度变化 → 单位长度密度恒定
      c.save(); c.strokeStyle = '#C9944C'; c.lineWidth = 2.8; c.lineCap = 'round';
      const nP = Math.max(3, Math.min(SAND.length, Math.round(len / 22)));
      for (let i = 0; i < nP; i++) {
        const s = SAND[i];
        const q = (t * s.sp * 1.05 + s.ph) % 1;
        const y = NY + q * (len + 12);
        const x = CX + s.o * STRW * 0.42;
        const L = s.sz * (1.4 + q * 1.6);
        c.globalAlpha = 0.55 + 0.45 * (1 - q);
        c.beginPath(); c.moveTo(x, y); c.lineTo(x, y + L); c.stroke();
      }
      c.restore();
      // 落点在锥顶砸出的小坑 + 溅起
      c.fillStyle = '#F2C98A';
      for (const s of SPL) {
        const q = (t * 1.5 + s.ph) % 1;
        const dx = Math.cos(s.a) * s.d * q, dy = -Math.sin(Math.abs(s.a)) * s.d * 0.55 * q + q * q * 42;
        c.beginPath(); c.arc(CX + dx, peakY + 6 + dy, s.sz * (1 - q * 0.6), 0, TAU); c.fill();
      }

      // ---- 玻璃反光：贴合左上内壁的暖黄短弧，整体收在玻璃轮廓内侧，不压轮廓线 ----
      c.save(); c.globalAlpha = 0.8; c.strokeStyle = C.warm; c.lineWidth = LW; c.lineCap = 'round';
      const INSET = 16;                                    // 沿 +x 向内收，端点离开轮廓线
      const hA = wallAt(0.12), hB = wallAt(0.38), hM = wallAt(0.25);
      c.beginPath();
      c.moveTo(hA[0] + INSET, hA[1]);
      c.quadraticCurveTo(hM[0] + INSET + 10, hM[1], hB[0] + INSET, hB[1]);
      c.stroke(); c.restore();
      c.restore();   // 结束裁切

      // ---- 玻璃轮廓 ----
      ink(c, glass, null, LW);

      // ---- 上下木盖 ----
      ink(c, rrect(CX - HW - 40, TOP - 58, (HW + 40) * 2, 58, 12), C.red, LW);
      ink(c, rrect(CX - HW - 40, BOT, (HW + 40) * 2, 58, 12), C.red, LW);

      c.restore();
    },
  };
})();
