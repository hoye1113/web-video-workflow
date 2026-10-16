// 这一页：静图慢推（13s 全程线性、几乎匀速，末尾 10% 停稳）+ 文字后段淡入上浮；焦点照抄给定 (fx=1.00,fy=0.73)，无第二张图 → 不做特写；第12/26页不算开篇 → 不做明暗揭示，第 0 帧即亮
SCENES['12'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/12_1.png';
  const LINES = ["更容易逃避"];
  return {
    draw(c, lt, t, IMG) {
      const D = 13, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));       // 运动进度：最后 10% 停住
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);   // 兜底底色，第 0 帧图已铺好

      // ① 慢推：全程线性无 easing，用给定的 z 基准 1.04 → 1.12，fx/fy 照抄焦点
      const z = lerp(1.04, 1.12, pm);

      // ② 单图铺满：fx/fy 是量出来的焦点，不自己改
      MD.cover(c, IMG[P], { z, fx: 1.00, fy: 0.73 });

      // ③ 无第二张图 → 跳过特写；不做明暗揭示

      // ④ 文字依次出现：淡入 + 从下浮 14px，落在左下留白，不压主体
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
