// 这一页：静图慢推（全程线性，收尾最后10%停稳）+ 开篇明暗揭示（8%内灯亮）+ "3年的关系"后段浮出；不画任何新东西
SCENES['04'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/04_1.png';
  const LINES = ['3年的关系'];
  return {
    draw(c, lt, t, IMG) {
      const D = 11, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));   // 运动进度：最后 10% 停住

      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);   // 兜底底色

      // ① 慢推：全程线性，从量出来的基准 z 再推 7%；fx/fy 用给定的焦点
      const z = lerp(1.000, 1.070, pm);

      // ② 单图直接铺满，不裁切、不加形
      MD.cover(c, IMG[P], { z, fx: 0.50, fy: 0.50 });

      // ③ 开篇明暗揭示：0→0.06 的时长里那层暖黑线性退到 0，像灯慢慢打开
      const rev = lerp(0.65, 0, clamp(p / 0.06));
      if (rev > 0) {
        c.fillStyle = 'rgba(20,16,12,' + rev.toFixed(4) + ')';
        c.fillRect(0, 0, W, H);
      }

      // ④ 文字依次出现：淡入 + 从下浮上来，放左下留白，不压主体
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
