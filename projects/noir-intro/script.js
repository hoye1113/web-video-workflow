/* Noir editorial proof · 4 chapters, one narration line each.
 * Duration is driven by voice.js (edge-tts), not by a fixed target. */
(function (root) {
  const META = {
    style: 'noir-editorial',
    title: '你真正想知道的',
    name: 'noir-intro',
    gap: 0.32,
    pageMotion: false,
    voice: { speaker: 'zh-CN-YunjianNeural', provider: 'edge' },
    extras: ['engine/styles/noir-editorial/kit.js'],
  };
  const PAGES = [
    { id: 'p01', section: '钩子', title: '你真正想知道的', cues: [
      '你真正想知道的，不是他爱不爱你。',
    ] },
    { id: 'p02', section: '拆解', title: '三个问题', cues: [
      '而是这段关系，还值不值得你继续。',
    ] },
    { id: 'p03', section: '判断', title: '判断力', cues: [
      '别急着找答案，先找回你的判断力。',
    ] },
    { id: 'p04', section: '身份', title: '听过我的声音', cues: [
      '你不一定认识我，但你一定听过我的声音。',
    ] },
  ];
  root.SCRIPT = { META, PAGES };
})(typeof window !== 'undefined' ? window : globalThis);
