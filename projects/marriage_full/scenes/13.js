// 第13页：一个铅笔圆（载体＝表面的和平）和一个红圆（主角＝背叛/愧疚）从右边胀大着滑进来、慢慢叠在一起。红从圆的左缘往右淌满＝涂红；交叠的那一块再压一道红＝愧疚与背叛同时存在；末尾铅笔线重新压在红上＝补偿维持的表面和平。节奏：0.0s 两个圆都已起笔、红已从左缘起头 → 0.20*dur 铅笔圆闭合 → 0.17~0.52*dur 涂红淌满 → 0.52~0.69*dur 交叠区加深 → 0.60*dur 手写「愧疚与背叛并存」 → 0.74~1.0*dur 微抖、表面线慢慢压回（补偿）。镜头缓推。
SCENES['13'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ss, ease, rng } = U;
  const C = { bg: '#F3EDE2', ink: '#1B1A17', red: '#C8402F' };
  const DUR = 13, R = 440, CY = 500;            // 圆的直径 880px ＝ 画面宽 46% / 高 81%：主角够大
  const CXA = 870, CXB = 1210, CX0 = 1380;      // 铅笔圆心 / 红圆终位 / 红圆起位（整体略偏右，给左上留出屏上字的位置）
  const TXT = '愧疚与背叛并存';

  // 同一支笔：分段描边，线宽在 1.5~2.5 倍之间自然顿挫，圆头圆角；taper 收细刚起头的笔尖
  const pen = (c, pts, col, w, seed, taper) => {
    const r = rng(seed);
    c.save(); c.strokeStyle = col; c.lineCap = 'round'; c.lineJoin = 'round';
    for (let i = 1; i < pts.length; i++) {
      const s = i / (pts.length - 1), tp = taper ? clamp((1 - s) / taper) : 1;
      c.lineWidth = w * (0.75 + r() * 0.75) * (0.35 + 0.65 * tp);
      c.beginPath(); c.moveTo(pts[i - 1][0], pts[i - 1][1]); c.lineTo(pts[i][0], pts[i][1]); c.stroke();
    }
    c.restore();
  };
  // 圆的点列：从 a0 起笔、顺时针；抖动固定不随帧变（否则线会逐帧发颤）
  const JIT = (() => { const r = rng(31), o = []; for (let i = 0; i <= 96; i++) o.push((r() - 0.5) * 3); return o; })();
  const ring = (cx, cy, rad, k, a0 = -Math.PI / 2) => {
    const o = [], m = Math.max(2, Math.round(k * 96));
    for (let i = 0; i <= m; i++) {
      const a = a0 + (i / 96) * TAU, rr = rad + JIT[i];
      o.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]);
    }
    return o;
  };
  const disc = (cx, cy, rad) => U.poly(ring(cx, cy, rad, 1), true);
  // 涂红的前沿：一条手画的湿边，不是一支机械的竖线
  const flood = (xL, xF, yT, yB) => {
    const p = new Path2D(); p.moveTo(xL, yT); p.lineTo(xF, yT);
    for (let i = 1; i <= 8; i++) p.lineTo(xF + Math.sin(i * 2.3) * 4.5, yT + (yB - yT) * i / 8);
    p.lineTo(xL, yB); p.closePath(); return p;
  };

  return {
    draw(c, lt) {
      c.fillStyle = C.bg; c.fillRect(0, 0, W, H);                 // 每帧自己画背景

      // 镜头缓推：朝两个圆的重心轻推，最后 8% 停稳
      const z = lerp(1.0, 1.07, clamp(lt / (DUR * 0.92)));
      c.save(); c.translate(960, 540); c.scale(z, z); c.translate(-960, -540);

      // 主角＝红圆：一边胀大一边从右边压上来；最后一路缓缓往里挤，还带轻微抖（表面和平维持得很不稳）
      const sl = ease.out(clamp(lt / 7.6)) * 0.90 + ss(7.6, 12.5, lt) * 0.10;
      const cx = lerp(CX0, CXB, sl) + ss(9.6, 11.0, lt) * 3.2 * Math.sin((lt - 9.6) * 8.5);
      const rd = lerp(0.62 * R, R, ease.out(clamp(lt / 4.6)));

      // ① 载体：铅笔圆（表面的和平）——从圆的底下起笔往左转，第一帧就有起头的线头
      const kc = 0.10 + 0.90 * ease.out(clamp(lt / 2.6));
      pen(c, ring(CXA, CY, R, kc, Math.PI / 2), C.ink, 4.0, 13, kc < 1 ? 0.22 : 0);

      // ② 主体：红圆的轮廓同步起笔（先有线，红后面才淌进去）
      const kd = 0.16 + 0.84 * ease.out(clamp(lt / 2.4));
      const rim = () => pen(c, ring(cx, CY, rd, kd), C.ink, 4.0, 29, kd < 1 ? 0.22 : 0);
      rim();

      // ③ 涂红：从圆的左缘往右淌满；两档平涂——淡红一层，交叠那一块再压一层（同时存在）
      const fw = clamp((0.10 + 0.90 * ease.inOut(clamp((lt - 0.9) / 5.4))) * 1.18);
      const pd = flood(cx - rd - 6, cx - rd + 2 * rd * fw, CY - rd - 6, CY + rd + 6);
      c.save();
      c.clip(disc(cx, CY, rd));
      c.globalAlpha = 0.55; c.fillStyle = C.red; c.fill(pd);
      const lens = ss(6.8, 9.0, lt);
      if (lens > 0.01) { c.globalAlpha = lens; c.clip(disc(CXA, CY, R)); c.fill(pd); }
      c.restore();

      // ④ 轮廓压回最上层，线不被红糊掉
      rim();

      // ⑤ 补偿：末尾铅笔线重新压在红上——把表面的和平裱回去
      const seal = ss(10.2, 12.6, lt);
      if (seal > 0.01) {
        c.save(); c.globalAlpha = seal;
        pen(c, ring(CXA, CY, R, 1, Math.PI / 2), C.ink, 4.0, 13, 0);
        c.restore();
      }
      c.restore();

      // ⑥ 0.6*dur 出字：手写体逐字浮现，落在左上方留白，不抢画面重心
      const pt = ss(7.8, 8.9, lt);
      if (pt > 0.01) {
        c.save(); c.fillStyle = C.ink; c.font = '500 40px "LXGWWenKai-500"';
        c.textAlign = 'left'; c.textBaseline = 'middle';
        let tx = 140;
        for (let i = 0; i < TXT.length; i++) {
          const cw = c.measureText(TXT[i]).width, k = clamp(pt * 1.6 - i * 0.085);
          if (k > 0.01) { c.globalAlpha = 0.92 * k; c.fillText(TXT[i], tx, 210 + (1 - k) * 14); }
          tx += cw + 7;
        }
        c.restore();
      }
    }
  };
})();
