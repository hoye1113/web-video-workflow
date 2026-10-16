// 08 案例一·周先生：静图近乎停住，只做极慢匀速推(1.31→1.41，最后10%停稳)；全程唯一自绘的局部是床头那排方格，0.40/0.50 最后两个空格先后暗掉后停住；文字「白天演，」「夜里熬」在 0.30/0.62 于左上留白淡入上浮
SCENES['08'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/08_1.png';
  const LINES = ['白天演，', '夜里熬'];
  // 那排方格里还没暗掉的两个空格（归一化中心 u/v，量自 08_1.png）
  const SQ = [[0.3946, 0.4336], [0.4041, 0.4251]];
  return {
    draw(c, lt, t, IMG) {
      const D = 14, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));        // 运动进度：最后 10% 停住
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);   // 兜底底色，第 0 帧图已铺好

      // ① 慢推：全程线性、几乎匀速（不套 easing），fx/fy 照抄量出来的焦点
      const z = lerp(1.31, 1.41, pm);
      const geo = MD.cover(c, IMG[P], { z, fx: 1.00, fy: 0.00 });

      // ② 唯一自绘局部：那排方格最后两个空格，0.40 / 0.50 先后暗下去（同一种形态接着长）
      const side = 13 * geo.s;
      SQ.forEach((q, i) => {
        const k = ss(0.40 + i * 0.10, 0.45 + i * 0.10, p); if (k <= 0) return;
        const [x, y] = MD.toScreen(geo, q);
        c.save(); c.globalAlpha = k; c.translate(x, y); c.rotate(-0.32);
        c.fillStyle = '#1B1A17'; c.fillRect(-side / 2, -side / 2, side, side);
        c.restore();
      });

      // ③ 文字依次出现：0.30 / 0.62，淡入 + 从下浮 14px，落在左上留白，不压主体
      const word = (s, at, y) => {
        const k = ss(at, at + 0.06, p); if (k <= 0) return;
        c.save(); c.globalAlpha = k; c.fillStyle = '#1B1A17';
        c.font = '500 46px "LXGWWenKai-500"';
        c.textAlign = 'left'; c.textBaseline = 'middle';
        c.fillText(s, 108, y + (1 - k) * 14);
        c.restore();
      };
      LINES.forEach((s, i) => word(s, [0.30, 0.62][i], 186 + i * 70));
    }
  };
})();
