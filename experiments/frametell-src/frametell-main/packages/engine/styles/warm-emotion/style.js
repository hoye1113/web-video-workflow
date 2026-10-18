/* Warm emotion · 情感叙事风格：暖色纸本插画，角色来自生成图，光就是情绪。
 *
 * 两套色板（方案 §4 P2 已定）：
 *   day   日间暖纸本 —— 光从窗来，纸面是暖米色
 *   night 深底暖光   —— 只有一个光源，暗部大
 * 用法：页面开头（建场景之前）调 `STYLE.setTheme('night')`。
 *   注意：夜间**不是换色值就够**（方案 §6 的 A/B 已证）。组件里凡是有 `STYLE.theme === 'night'`
 *   判断的地方，都是在为夜间单独调（加辉光、减平涂、压低亮部）。初次校准在 P2-d 的 3 页对比。
 */
window.EXTRA_FONTS = (window.EXTRA_FONTS || []).concat(['600 40px Fredoka', '500 40px Fredoka']);

const DAY = {
  ink: '#3A322C', soft: '#6E6157', muted: '#A2937F', faint: '#DCD2C0',
  red: '#C8402F', redF: '#F2D6CF',        // 焦红：代价、警告、那道裂缝
  orange: '#D98F3C', orangeF: '#F7E3C4',  // 暖橘：光、答案、被需要的感觉
  green: '#8FA86A', greenF: '#E2EAD0',    // 嫩芽绿：生长、在一起时的松弛
  blue: '#4A7A85', blueF: '#D3E3E4',      // 灰青：冷静、时间、说不出口
  purple: '#8A6B72', purpleF: '#EADCDE',  // 暗藕：愧疚、忍耐、表面的和平
  yellow: '#E8C77A', paper: '#FBF7ED',
  inkF: '#E8E0D2', softF: '#EFE8DA', mutedF: '#F4EEE2', faintF: '#F8F4EA',
  // 角色锚点色（取自定妆图实测，供矢量层对齐镜头用；角色本体仍来自生成图）
  sprout: '#DEF0A8', hairF: '#F6E4D8', hairM: '#728A96', jacket: '#D2DEE4', shorts: '#7C6867',
  skinF: '#F6DED2',
  // plate：浅底素材 multiply 上来的底（scene 的 ground 用）。
  // 不能直接用 paper —— 太深会把主体一起吃掉；这一档是"底色够沉、主体还看得见"
  plate: '#EFE3CF',
};

const NIGHT = {
  ink: '#E8DCCB', soft: '#B9A98F', muted: '#857A68', faint: '#4A423A',
  red: '#D9614A', redF: '#4A2A24',
  orange: '#E8A94E', orangeF: '#4A3826',
  green: '#9CB57A', greenF: '#33402C',
  blue: '#6FA0A8', blueF: '#263436',
  purple: '#B0858E', purpleF: '#3A2C30',
  yellow: '#F0CE86', paper: '#1E1A18',
  inkF: '#2A2522', softF: '#332C28', mutedF: '#3B332E', faintF: '#443B35',
  sprout: '#C8D98E', hairF: '#C9A99C', hairM: '#5A6B76', jacket: '#8C99A2', shorts: '#4E4444',
  skinF: '#C9AFA2',
  // plate：夜间的底。比 paper 浅一档 —— 浅底素材 multiply 上来时主体还看得见（scene 的 ground 用）
  plate: '#6E5C49',
};

window.STYLE = {
  id: 'warm-emotion',
  roughScale: 0.30, bowScale: 0.38, sw: 3.2, single: true,
  theme: 'day',
  palettes: { day: DAY, night: NIGHT },
  // 运行时读的就是这个字段；切主题时整体替换（组件与页面只用颜色名，所以能跟着换）
  palette: { ...DAY },
  /** 切日夜。**必须写在页面的 visual 回调最前面**（颜色在构建时烘焙进 DOM）。
   *
   * 为什么不能只换 STYLE.palette：运行时在加载时做了 `Object.assign(C, STYLE.palette)`，
   * 而 `col()` 读的是它自己那份 `C` —— 所以必须**就地改 `PV.C`** 才生效。
   * 背景（STYLE.background）只在初始化时算一次，是**片级**的：
   *   · 整片夜间 → 在 script.js 的 META.look.palette 里覆盖（引擎自带这条路）
   *   · 只是某几页低谷 → 那几页自己用 `P.light(..., { full: true, ground: 'paper' })` 铺底
   */
  setTheme(name) {
    if (!this.palettes[name]) throw new Error(`warm-emotion: unknown theme "${name}"`);
    const p = this.palettes[name];
    this.theme = name;
    this.palette = { ...p };
    if (typeof window !== 'undefined' && window.PV && window.PV.C) Object.assign(window.PV.C, p);
    if (typeof document !== 'undefined' && document.documentElement) {
      document.documentElement.dataset.theme = name;
    }
    return this;
  },
  /** 情绪档位 → 主题。low = 情绪低谷（配色调暗），其余日间。 */
  themeFor(mood) { return mood === 'low' ? 'night' : 'day'; },
  /* 纸面：日间是暖米纸 + 细颗粒；夜间是深底 + 中心一点暖光晕（"只剩一盏灯"）。 */
  background: (stage) => {
    const grain = encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="420" height="420"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="5" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.32  0 0 0 0 0.2  0 0 0 0.09 0"/></filter><rect width="420" height="420" filter="url(#n)"/></svg>');
    if (window.STYLE.theme === 'night') {
      return [
        `url("data:image/svg+xml;utf8,${grain}")`,
        `radial-gradient(${stage.w * 0.55}px ${stage.h * 0.5}px at 50% 42%, #3A3129, #241F1C 58%, #16130F)`,
      ].join(',');
    }
    return [
      `url("data:image/svg+xml;utf8,${grain}")`,
      `radial-gradient(${stage.w * 0.9}px ${stage.h * 0.75}px at 50% 38%, #FDFAF2, #F6EFE0 62%, #EFE4D0)`,
    ].join(',');
  },
};
