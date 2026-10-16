/* p13 愧疚与背叛并存
 * 两个大圆：背叛（陶土红）先到，愧疚（深青）压上去 —— 交叠就是这一页要讲的。
 * 一层「表面的和平」抹在交叠上；说到「不是完全没有愧疚」它往下滑、变淡，
 * 底下的红透出来 —— 补偿盖不住，两者同时在。
 * 标签一律放在下半个画面：相机推近时不会被顶出画外（第一版就栽在这）。
 */
ENGINE.visual('p13', (P) => {
  P.title('愧疚与背叛并存', { accent: 'red' });

  const CY = 545, D = 760, LX = 790, RX = 1130;
  const OV = (LX + RX) / 2;

  // ① 背叛先到
  P.circle(LX, CY, D, { fill: 'redF', color: 'red', at: 0.15, dur: 1.1 });
  P.tag(LX - 196, CY + 268, '背叛', { size: 48, color: 'red', at: P.c(0, 1.5) });

  // ② 愧疚压上去
  P.circle(RX, CY, D, { fill: 'blueF', color: 'blue', at: P.c(0, 0.8), dur: 1.1 });
  P.tag(RX + 196, CY + 268, '愧疚', { size: 48, color: 'blue', at: P.c(3, 0.25) });

  // ③「表面的和平」：一条米白的膜横抹在交叠上沿（薄薄一层，底下还看得见）
  const film = P.layer();
  film.box(OV - 300, CY - 330, 600, 210, { fill: 'paper', color: 'faint', r: 20, at: P.c(1, 0.15), dur: 0.7 });
  film.line(OV - 250, CY - 300, OV + 250, CY - 300, { color: 'faint', sw: 3, at: P.c(1, 0.8), dur: 0.4 });
  film.tag(OV, CY - 372, '表面的和平', { size: 38, color: 'soft', at: P.c(1, 1.0) });

  // ④「不是完全没有愧疚」：膜往下滑、变淡，红色从底下透出来
  P.move(film, (lt) => {
    const k = PV.ease.out(PV.clamp((lt - P.c(3, 0.05)) / 1.4));
    return { x: k * 34, y: k * 150, rot: k * 3, op: 1 - k * 0.6 };
  }, [OV, CY]);

  // ⑤ 收在「同时存在」：推近交叠的下半（标签都在那儿，推近也压不到）
  P.cam([P.push(P.c(4, 0.7), OV, CY + 120, 1.24), P.back(P.ce(4) + 0.35)]);
  P.tag(OV, CY + 130, '同时存在', { size: 44, color: 'ink', bg: 'yellow', at: P.c(4, 1.2) });
});
