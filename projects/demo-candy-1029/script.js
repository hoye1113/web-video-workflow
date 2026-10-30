/* emotion-full · 26 页口播稿（由 tools/make_script_js.py 从 script-source.json 生成）。
 * 改文案：改 script-source.json 再重跑，别手改这个文件。 */
(function (root) {
  const META = {
    style: 'warm-emotion',
    title: "最后一块糖",
    name: "demo-candy-1029",
    gap: 0.8,
    voice: { speaker: 'zh-CN-XiaoxiaoNeural', provider: 'edge' },
    extras: ['engine/styles/warm-emotion/kit.js'],
  };
  const PAGES = [
    { id: "p01", section: "钩子", title: "她总把最后一块糖，留到化了才吃", cues: [
      "她总把最后一块糖，",
      "留到化了才吃。",
    ] },
    { id: "p02", section: "习惯", title: "她说，好东西要留到最后，才不算浪费", cues: [
      "她笑着说，",
      "好东西要留到最后，",
      "才不算浪费。",
    ] },
    { id: "p03", section: "转折", title: "后来她才知道，有些甜，等不了那么久", cues: [
      "后来她才知道，",
      "有些甜，",
      "等不了那么久。",
    ] },
    { id: "p04", section: "落点", title: "那天，她把糖放进嘴里，笑了", cues: [
      "直到那天，",
      "她把糖放进嘴里，",
      "笑了。",
    ] },
  ];
  root.SCRIPT = { META, PAGES };
})(typeof window !== 'undefined' ? window : globalThis);
