/* 页面内容 + 版式。改这个文件就能换词/换图，不用动 pages/*.js。
 * layout: hook / split / translate / wall / heart / choice / end
 */
window.NIGHT_SPEC = {
  p01: {
    layout: 'hook',
    chapter: '01',
    name: '钩子',
    kicker: '她难过的时候',
    title: ['越<span class="accent-cyan">安慰</span>', '越<span class="accent-orange">崩溃</span>'],
    lead: '你越想把她拉出来，<br>她越觉得你没进去。',
    phone: {
      name: '她',
      status: '在线',
      messages: [
        { side: 'in', text: '我今天好累' },
        { side: 'out', text: '别想太多，早点睡' },
        { side: 'in', text: '……', dim: true },
        { side: 'in', text: '你根本不懂', dim: true },
      ],
      read: '已读',
      typing: '对方正在输入…',
    },
    note: '第 3 次已读不回',
  },

  p02: {
    layout: 'split',
    chapter: '02',
    name: '反常识',
    kicker: '反常识',
    title: ['大多数安慰，', '都在急着<span class="accent-cyan">解决问题</span>'],
    left: {
      color: 'orange',
      tag: '急着修好',
      tagColor: 'orange',
      icon: 'toolbox',
      title: '给方案',
      items: ['“别想了”', '“这有什么”', '“我教你怎么办”'],
    },
    right: {
      color: 'cyan',
      tag: '先接住',
      tagColor: 'cyan',
      icon: 'eye',
      title: '给回应',
      items: ['“我在”', '“很难受吧”', '“你慢慢说”'],
    },
    wall: '解决问题',
    caption: '她要的是<b>被看见</b>，不是被指导。',
  },

  p03: {
    layout: 'translate',
    chapter: '03',
    name: '错误示范',
    kicker: '一句话，两种翻译',
    title: ['你说“<span class="accent-orange">别想了</span>”'],
    saidLabel: '你的安慰',
    said: '别想了',
    heardLabel: '她听到的',
    heard: '你的感受不重要',
    caption: '否定情绪，比不回应更<b>伤人</b>。',
  },

  p04: {
    layout: 'wall',
    chapter: '04',
    name: '机制',
    kicker: '为什么进不去',
    title: ['情绪没被接住，', '<span class="accent-orange">道理</span>就进不去'],
    leftName: '你',
    rightName: '她',
    wall: '道理',
    caption: '越讲道理，她越觉得你在<b>对面</b>。',
  },

  p05: {
    layout: 'heart',
    chapter: '05',
    name: '正确动作',
    kicker: '先做什么',
    title: ['先接住情绪，', '再<span class="accent-cyan">给方案</span>'],
    quote: { label: '先说这一句', text: '“你现在一定很难受。”' },
    tool: { title: '方案', sub: '先放一边' },
    caption: '先接住，再说。',
  },

  p06: {
    layout: 'choice',
    chapter: '06',
    name: '把选择权交给她',
    kicker: '等她落地',
    title: ['再问一句'],
    left: { color: 'cyan', icon: 'ear', title: '听我说', sub: '先不评价，先听完' },
    right: { color: 'orange', icon: 'bulb', title: '一起想办法', sub: '她要的是队友，不是老师' },
    quote: '“你想让我听，<b>还是一起想办法</b>？”',
  },

  p07: {
    layout: 'end',
    chapter: '07',
    name: '收尾',
    kicker: '最后',
    title: ['安慰不是说服', '是<span class="accent-orange">靠近</span>'],
    note: '先接住，再讲<b>道理</b>。',
    sub: '关系里，靠近比正确更重要',
  },
};
