/* P2-d 总验收：用 warm-emotion 重做原片的 05 / 15 / 18 三页。
 * 旁白沿用原片分镜（略精简），配图是 Flow 新生成的处境图。 */
(function (root) {
  const META = {
    style: 'warm-emotion',
    title: 'P2-d 三页对比',
    name: 'warm-emotion-3pages',
    gap: 0.8,
    extras: ['engine/styles/warm-emotion/kit.js'],
  };
  const PAGES = [
    { id: 'p05', section: '案例一', title: '妻子提离婚当晚，他跪下来认错', cues: [
      '妻子当晚就拿出了离婚协议。',
      '他整个人直接崩掉了，',
      { t: '没有任何犹豫就认错，跪着求她原谅。', hold: 0.8 },
    ] },
    { id: 'p15', section: '案例三', title: '白天正常，晚上装没事', cues: [
      '白天要维持正常的生活，',
      '晚上回到家还要装作什么都没发生过。',
      { t: '这种状态一直在消耗他。', hold: 0.8 },
    ] },
    { id: 'p18', section: '真相拆解', title: '一边要家庭，一边要刺激', cues: [
      '一边想要维持家庭，',
      '一边又想满足外面的刺激。',
      { t: '看起来是在做选择，其实是内在的冲突。', hold: 0.8 },
    ] },
  ];
  root.SCRIPT = { META, PAGES };
})(typeof window !== 'undefined' ? window : globalThis);
