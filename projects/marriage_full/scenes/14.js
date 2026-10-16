// 这一页：静图全程匀速慢推（z 1.02→1.09，焦点 fx/fy=1.00），最后 10% 推到头停稳；不用明暗揭示，第一帧就是亮的；文字「主动断掉」在 0.30 淡入并从下浮起。
SCENES['14'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss } = U;
  const P = 'demos/marriage_full/assets/14_1.png';
  const TEXT = '主动断掉';
  return {
    draw(c, lt, t, IMG) {
      const D = 11, p = clamp(lt / D);
      const pm = clamp(lt / (D * 0.9));   // 运动进度：最后 10% 停住

      // ① 每帧第一件事：铺底色
      c.fillStyle = '#F3EDE2'; c.fillRect(0, 0, W, H);

      // ② 慢推：全程线性、几乎匀速，从基准 z 再推 7%；fx/fy 照抄量出来的焦点
      const z = lerp(1.02, 1.09, pm);
      MD.cover(c, IMG[P], { z, fx: 1.0, fy: 1.0 });

      // ③ 文字：0.30 淡入 + 从下 14px 浮上来，落在左下留白，不压主体
      const k = ss(0.30, 0.36, p);
      if (k > 0) {
        c.save();
        c.globalAlpha = k;
        c.fillStyle = '#1B1A17';
        c.font = '500 52px "LXGWWenKai-500"';
        c.textAlign = 'left';
        c.textBaseline = 'middle';
        c.fillText(TEXT, 140, 210 + (1 - k) * 14);
        c.restore();
      }
    }
  };
})();
