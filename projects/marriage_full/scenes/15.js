// 第15页：单张静图慢推（全程线性、最后10%停稳）+「装没事」后段淡入浮出；无明暗揭示、无特写
SCENES['15'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/15_1.png';
  const LINES = ["装没事"];
  return {
    draw(c, lt, t, IMG) {
      const D = 11, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));          // 运动进度：最后 10% 停住
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);

      // ① 慢推：从量出的基准 z 线性推到终点，fx/fy 照抄给定焦点
      const z = lerp(1.350, 1.440, pm);

      // ② 单图铺满，焦点 0.97/1.0，主体落在右侧门边
      MD.cover(c, IMG[P], { z, fx: 0.97, fy: 1.00 });

      // ③ 本页不用明暗揭示：第一帧就是亮的（揭示层只在开篇页用）

      // ④ 文字后段出现：淡入 0.06s + 从下 14px 浮上来，放在左侧留白
      const word = (s, at, y) => {
        const k = ss(at, at + 0.06, p); if (k <= 0) return;
        c.save(); c.globalAlpha = k; c.fillStyle = '#1B1A17';
        c.font = '500 52px "LXGWWenKai-500"';
        c.textAlign = 'left'; c.textBaseline = 'middle';
        c.fillText(s, 140, y + (1 - k) * 14);
        c.restore();
      };
      LINES.forEach((s, i) => word(s, [0.30, 0.62, 0.85][i] || 0.85, 210 + i * 76));
    }
  };
})();
