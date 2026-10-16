// 第6页·案例一·周先生：静图慢推(z 1.00→1.07，焦点 fx1.0/fy0.5) + 开头 6% 明暗揭示 + 文字「断联消息」后段浮现上移 + 最后 10% 停稳
SCENES['06'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/06_1.png';
  return {
    draw(c, lt, t, IMG) {
      const D = 12, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));       // 运动进度：最后 10% 停住
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);

      // ① 慢推：全程线性匀速，fx/fy 照抄量出来的焦点
      const z = lerp(1.000, 1.070, pm);
      MD.cover(c, IMG[P], { z, fx: 1.0, fy: 0.5 });

      // ② 明暗揭示：开头 6% 像灯慢慢打开（第 6 页靠前，可用）
      const rv = lerp(0.65, 0, clamp(p / 0.06));
      if (rv > 0) { c.fillStyle = 'rgba(20,16,12,' + rv + ')'; c.fillRect(0, 0, W, H); }

      // ③ 文字出现：0.30 淡入，同时从下方 14px 浮上来
      const word = function (s, at, y) {
        const k = ss(at, at + 0.06, p); if (k <= 0) return;
        c.save(); c.globalAlpha = k; c.fillStyle = '#1B1A17';
        c.font = '500 52px "LXGWWenKai-500"';
        c.textAlign = 'left'; c.textBaseline = 'middle';
        c.fillText(s, 140, y + (1 - k) * 14);
        c.restore();
      };
      word('断联消息', 0.30, 210);
    }
  };
})();
