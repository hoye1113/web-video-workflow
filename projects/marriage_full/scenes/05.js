// 05 案例一·周先生：静图慢推（线性、收尾停稳）+ 开篇明暗揭示 + 文字依次浮现
SCENES['05'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/05_1.png';
  const LINES = ['当场', '崩塌'];
  return {
    draw(c, lt, t, IMG) {
      const D = 15, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));   // 运动进度：最后 10% 停住
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);   // 兜底底色

      // ① 慢推：全程线性，从量出的基准 z 再推 7%；fx/fy 用给定的焦点
      const z = lerp(1.000, 1.070, pm);
      MD.cover(c, IMG[P], { z, fx: 1.0, fy: 0.5 });

      // ② 明暗揭示：0 → 0.06 线性开灯（第 5 页，靠前可用）
      const rv = 1 - clamp(p / 0.06);
      if (rv > 0) {
        c.fillStyle = 'rgba(20,16,12,' + (0.65 * rv).toFixed(3) + ')';
        c.fillRect(0, 0, W, H);
      }

      // ③ 只有一张图，跳过细节插入（不拿变焦假装特写）

      // ④ 文字依次出现：0.30 / 0.62，淡入 + 从下浮 14px，放左下留白区
      const word = (s, at, y) => {
        const k = ss(at, at + 0.06, p); if (k <= 0) return;
        c.save(); c.globalAlpha = k; c.fillStyle = '#2A211A';
        c.font = '500 54px "LXGWWenKai-500"';
        c.textAlign = 'left'; c.textBaseline = 'middle';
        c.fillText(s, 150, y + (1 - k) * 14);
        c.restore();
      };
      LINES.forEach((s, i) => word(s, [0.30, 0.62][i] || 0.62, 832 + i * 78));

      // ⑤ 细线：文字上方短下划线，随第一条文字展开（收尾保持静止）
      const lk = ss(0.30, 0.42, p);
      if (lk > 0) {
        c.fillStyle = 'rgba(42,33,26,0.5)';
        c.fillRect(150, 792, 176 * lk, 2);
      }
    }
  };
})();
