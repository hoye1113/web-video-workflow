ENGINE.visual('p09', (P) => {
  P.title('婚姻在出事之前，早就进入了无波无澜的状态', { accent: 'blue' });

  const SKY = 470;               // 水面线
  const tW = P.c(0, 0.05);       // 第一个 cue：水面铺开

  // 一潭静水：水面从中间向两侧铺平，下半幅满是水
  P.box(-140, SKY, 2200, 430, { fill: 'blueF', color: 'blue', sw: 0, at: tW, dur: 1.0 });
  P.line(960, SKY, -140, SKY, { color: 'blue', sw: 6, at: tW, dur: 0.9 });
  P.line(960, SKY, 2060, SKY, { color: 'blue', sw: 6, at: tW, dur: 0.9 });

  // 天上安安静静一枚太阳
  P.circle(1580, 296, 146, { fill: 'yellowF', color: 'yellow', sw: 4, at: P.c(0, 0.6), dur: 0.9 });

  // 两个人：从水中央慢慢分向两边，越拉越远
  const tShow = P.c(1, 0.02);
  const tSepA = P.c(1, 0.35);
  const tSepB = Math.max(tSepA + 1.8, P.c(2, 0.2));
  const G0 = 46, G1 = 480;

  P.liveRough((lt, R) => {
    const ap = PV.ease.out(PV.K(lt, tShow, 0.7));
    if (ap <= 0) return [];
    const u = PV.ease.inOut(PV.K(lt, tSepA, tSepB - tSepA));
    const g = G0 + (G1 - G0) * u;
    const d = 62 * (0.55 + 0.45 * ap);
    return [
      R.circle(960 - g, SKY, d, { fill: 'ink', color: 'ink', sw: 0 }),
      R.circle(960 + g, SKY, d, { fill: 'ink', color: 'ink', sw: 0 })
    ];
  });

  // 推近，看中间那道被拉开的空
  P.cam([P.push(P.c(2, 0.2), 960, 460, 1.15)]);

  // 空里落下一行字：不是吵架，是没话可说
  const tWord = P.cw(3, '没什么');
  const tLand = Math.max(P.c(2, 0.8), Math.min(tWord || P.c(3, 1.2), P.endT - 1.1));
  const tFall = tLand - 0.9;
  const TOP = 200, REST = SKY - 64;

  P.follow((lt) => ({
    text: '没话可说',
    x: 960,
    y: TOP + (REST - TOP) * PV.ease.out(PV.K(lt, tFall, 0.9)),
    opacity: PV.ease.out(PV.K(lt, tFall, 0.45))
  }), { size: 50, color: 'ink', align: 'c' });
});
