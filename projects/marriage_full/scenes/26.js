// 第26页「行动与落点」：静图 15s 全程线性慢推，z 用给定基准 1.00→1.07、焦点 fx/fy 照抄 (1.00,0.50)，最后 10% 运动停稳；文字「重建边界」0.30 淡入并从下浮 14px，落在画面左下留白，不压主体；本页是全片最后一页，不做明暗揭示，第一帧就是亮的；只有一张图，不做特写插入。
SCENES['26'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/26_1.png';
  const LINES = ['重建边界'];
  const AT = [0.30, 0.62, 0.85];
  return {
    draw(c, lt, t, IMG) {
      const D = 15;
      const p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));
      c.fillStyle = '#F3EDE2';
      c.fillRect(0, 0, W, H);
      const z = lerp(1.000, 1.070, pm);
      MD.cover(c, IMG[P], { z, fx: 1.00, fy: 0.50 });
      LINES.forEach((s, i) => {
        const at = AT[i] || 0.85;
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
