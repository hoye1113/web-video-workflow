// 这一页：静图慢推（17s 全程线性，末尾 10% 停稳）+ 文字后段淡入浮起；焦点用给定 (fx=1.00,fy=1.00)，不用明暗揭示（第10/26页不算开篇，第一帧即亮）
SCENES['10'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/10_1.png';
  const LINES = ["重新活了一次"];
  return {
    draw(c, lt, t, IMG) {
      const D = 17, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));        // 运动进度：最后 10% 停住
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);   // 兜底底色

      // ① 慢推：全程线性无 easing，从量出来的基准 z 再推 ~7%
      const z = lerp(1.24, 1.33, pm);

      // ② 单图铺满，fx/fy 用给定的焦点，不自己改
      MD.cover(c, IMG[P], { z, fx: 1.0, fy: 1.0 });

      // ③ 无第二张图 → 跳过特写；也不做明暗揭示，第 0 帧就是亮的

      // ④ 文字：放在左侧留白区，主体在右下不被压住；淡入 + 从下浮 14px
      LINES.forEach((s, i) => {
        const at = [0.30, 0.62, 0.85][i] || 0.85;
        const k = ss(at, at + 0.06, p);
        if (k <= 0) return;
        c.save();
        c.globalAlpha = k;
        c.fillStyle = '#1B1A17';
        c.font = '500 52px "LXGWWenKai-500"';
        c.textAlign = 'left';
        c.textBaseline = 'middle';
        c.fillText(s, 140, 210 + i * 76 + (1 - k) * 14);
        c.restore();
      });
    }
  };
})();
