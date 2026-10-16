/* 实验-情感 · 用我们那条片子的两页，检验"它这套能不能承载情感类"
 * 旁白原文来自 projects/marriage_full（第 13 页、第 26 页）。 */
(function (root) {
  const META = {
    style: 'warm-story',
    title: '婚姻修复：不是回到过去',
    name: '实验-情感',
    gap: 0.8,
    pace: { maxHold: 1.0, gap: 0.8 },
    voice: { speaker: 'zh-CN-XiaoxiaoNeural', provider: 'edge' },
    extras: ['extras/warm.js'],
  };
  const PAGES = [
    { id: 'p13', section: '愧疚与背叛', title: '愧疚与背叛并存', cues: [
      '反而他更加倾向于用一种补偿心态去维持表面的和平，',
      '比如对妻子更顺从一些啦，',
      '好像这样就能抵消掉自己的那种内心的不安。',
      '也就是说，他不是完全没有愧疚，',
      { t: '而是愧疚和背叛这件事情可以同时存在。', hold: 0.6 },
    ] },
    { id: 'p26', section: '重建边界', title: '重建边界', cues: [
      '而是双方都在错误的方式里面继续消耗彼此。',
      '真正的修复不是简单的回到过去，',
      { t: '而是重新建立规则和边界，', hold: 0.4 },
      '让这段关系重新变得可承受可持续。',
    ] },
    { id: 'p09', section: '无波无澜', title: '无波无澜', cues: [
      '很多人以为婚姻的危机是从出轨那天开始的，',
      '但真正出问题的时间要早得多，',
      '早到两个人自己都没察觉 ——',
      '日子照过，只是没什么话可说了。',
    ] },
  ];
  root.SCRIPT = { META, PAGES };
})(typeof window !== 'undefined' ? window : globalThis);
