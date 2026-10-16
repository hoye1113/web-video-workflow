// 09 案例二·刘先生：全自绘。一支笔在纸上从左往右拉出一条笔直的水平线（主角：X0→X1 = 1520px，占画面宽 79%），
// 0.0s 极淡压痕先铺出走向 → 1.2s 笔尖落纸、墨线开始生长 → 7.2s（0.6*dur）「无波无澜」手写淡入 → 10.0s 收笔、笔抬起退场；全程镜头横移
SCENES['09'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ss, ease, rng } = U;
  const C = { bg:'#F3EDE2', paper:'#FBF8F2', ink:'#1B1A17', gray:'#6B655B', red:'#C8402F', teal:'#2F5D62' };
  const DUR = 12, LY = 566, X0 = 200, X1 = 1720;      // 线长 X1-X0 = 1520px（画面宽 1920 的 79%）
  const T0 = 1.2, T1 = 10.0, TX = 7.2;                // 落笔 / 收笔 / 出字
  const R = rng(9), PH = [R()*TAU, R()*TAU, R()*TAU, R()*TAU];
  // 同一条线：中心线几乎笔直（这是本页的论点），只有低频的粗细顿挫，干净连续，不做刺、不做锯齿
  const hw = x => 6.6 + 1.3*Math.sin(x*0.0135 + PH[0]) + 0.5*Math.sin(x*0.041 + PH[1]);
  const cy = x => LY + 0.7*Math.sin(x*0.0061 + PH[2]) + 0.25*Math.sin(x*0.023 + PH[3]);
  // 同一形态沿自身长大 / 变淡：front = 画到哪，thin = 粗细倍率；两端都是圆头
  const line = (front, thin) => {
    const up = [], dn = [], f = Math.max(front, X0 + 1e-3);
    for (let x = X0; x < f; x += 8) { up.push([x, cy(x) - hw(x)*thin]); dn.push([x, cy(x) + hw(x)*thin]); }
    up.push([f, cy(f) - hw(f)*thin]); dn.push([f, cy(f) + hw(f)*thin]);
    const p = new Path2D(); p.moveTo(up[0][0], up[0][1]);
    for (let i = 1; i < up.length; i++) p.lineTo(up[i][0], up[i][1]);
    const rf = hw(f)*thin;
    for (let a = -Math.PI/2; a <= Math.PI/2 + 0.01; a += 0.3) p.lineTo(f + Math.cos(a)*rf, cy(f) + Math.sin(a)*rf);
    for (let i = dn.length - 1; i >= 0; i--) p.lineTo(dn[i][0], dn[i][1]);
    const r0 = hw(X0)*thin;
    for (let a = Math.PI/2; a >= -Math.PI/2 - 0.01; a -= 0.3) p.lineTo(X0 + Math.cos(a)*r0, cy(X0) + Math.sin(a)*r0);
    p.closePath(); return p;
  };
  const paper = c => {                                // 载体：那张纸（离边框留空隙，不压线）
    c.save(); c.translate(960, 540); c.rotate(-0.018);
    c.beginPath(); c.rect(-850, -490, 1700, 980);
    c.fillStyle = C.paper; c.fill();
    c.globalAlpha = 0.45; c.strokeStyle = C.gray; c.lineWidth = 2.6; c.stroke();
    c.restore();
  };
  const pen = (c, x, y, a) => {                       // 那支笔：笔尖在 (x,y)，笔身朝右上
    if (a <= 0.01) return;
    c.save(); c.globalAlpha = a; c.translate(x, y); c.rotate(0.62);
    c.fillStyle = C.teal;
    c.beginPath(); c.moveTo(-12,-44); c.lineTo(-12,-244); c.quadraticCurveTo(-12,-258, 0,-258);
    c.quadraticCurveTo(12,-258, 12,-244); c.lineTo(12,-44); c.closePath(); c.fill();
    c.fillStyle = C.red; c.fillRect(-13.5, -100, 27, 32);
    c.fillStyle = C.ink;
    c.beginPath(); c.moveTo(-11,-44); c.lineTo(11,-44); c.lineTo(2.6,0); c.lineTo(-2.6,0); c.closePath(); c.fill();
    c.restore();
  };
  const TXT = '无波无澜';
  return {
    draw(c, lt) {
      c.fillStyle = C.bg; c.fillRect(0, 0, W, H);                 // 每帧自己画背景
      c.save(); c.translate(lerp(170, -170, clamp(lt / DUR)), 0);  // 镜头横移
      paper(c);
      // ① 0.0s 就有：极淡压痕铺满，交代主角的长相与走向（第一帧不空）
      c.globalAlpha = 0.24 * (1 - 0.85 * ss(T1 - 0.6, T1 + 0.9, lt));
      c.fillStyle = C.gray; c.fill(line(X1, 0.45));
      c.globalAlpha = 1;
      // ② 墨线沿压痕生长
      const lp = clamp((lt - T0) / (T1 - T0)), pe = ss(0, 1, lp);
      const front = lt < T0 ? X0 : lerp(X0, X1, pe);
      if (lt >= T0) { c.fillStyle = C.ink; c.fill(line(front, 1)); }
      // ③ 0.6*dur：屏上字，手写体，落在下方留白，不抢重心
      if (lt > TX) {
        c.font = '500 58px "LXGWWenKai-500"'; c.textAlign = 'center'; c.textBaseline = 'middle';
        c.fillStyle = C.ink;
        for (let i = 0; i < 4; i++) {
          const k = ss(0, 1, clamp((lt - TX - i * 0.16) / 0.7)); if (k <= 0) continue;
          c.globalAlpha = 0.88 * k;
          c.fillText(TXT[i], 494 + i * 78, 820 - 12 * (1 - k));
        }
        c.globalAlpha = 1;
      }
      // ④ 笔：入场 → 跟着线头走 → 收笔抬出画外
      let px, py, pa;
      if (lt < T0) { const q = ease.out(clamp(lt / T0)); px = lerp(70, X0, q); py = cy(X0) - lerp(105, 2, q); pa = clamp(lt / 0.35); }
      else if (lt <= T1) { px = front; py = cy(front); pa = 1; }
      else { const q = ease.in(clamp((lt - T1) / 1.5)); px = X1 + 320 * q; py = cy(X1) - 160 * q; pa = 1 - q; }
      pen(c, px, py, pa);
      c.restore();
    }
  };
})();
