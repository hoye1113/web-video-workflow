/* Noir editorial: a near-black teal ground, bone and muted gold type, hairlines and a very
 * quiet HUD. Built for type-led manifestos and chapter cards, not for photo stories. */
window.STYLE = {
  id: 'noir-editorial',
  // the line is almost a printed rule: barely any wobble, one crisp stroke
  roughScale: 0.04, bowScale: 0.02, sw: 1.6, single: true,
  palette: {
    ink: '#E9E4D8', soft: '#AEB6B1', muted: '#73807D', faint: '#2A3436',
    blue: '#7FB3A8', blueF: '#102322',      // muted teal: the one cool accent
    orange: '#D8B173', orangeF: '#2A2317',  // old gold: titles and the one warm accent
    red: '#C97062', redF: '#2A1A18',
    green: '#8FBF9A', greenF: '#17251B',
    purple: '#B49AA8', purpleF: '#241C22',
    yellow: '#E6C566', paper: '#060A0B',
    inkF: '#1A2224', softF: '#151C1E', mutedF: '#111719', faintF: '#0C1214',
  },
  // a faint 64px drafting grid, a horizon haze, and a warm-cold falloff into the corners
  background: (stage) => [
    'radial-gradient(ellipse 78% 28% at 50% 31%, rgba(95, 160, 148, 0.045), transparent 72%)',
    'linear-gradient(180deg, transparent 30.6%, rgba(170, 210, 200, 0.022) 31%, transparent 31.5%)',
    'linear-gradient(rgba(255,255,255,0.026) 1px, transparent 1px) 0 0 / 64px 64px',
    'linear-gradient(90deg, rgba(255,255,255,0.026) 1px, transparent 1px) 0 0 / 64px 64px',
    `radial-gradient(${stage.w * 1.02}px ${stage.h * 0.92}px at 50% 38%, #091113, #060A0B 58%, #030506)`,
  ].join(','),
  setTheme() {},
};
