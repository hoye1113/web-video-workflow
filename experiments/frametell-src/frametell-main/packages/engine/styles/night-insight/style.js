/* Night insight · 深色心理图解
 * 一套独立的套版：黑底 + 青色主色 + 橙色强调 + 信息图组件。
 * 不改 warm-emotion / tech-dark 的任何规则；项目用 META.style = 'night-insight' 拉进来。
 */
window.STYLE = {
  id: 'night-insight',
  theme: 'night',
  palette: {
    ink: '#F2F6F7',
    soft: '#C3D0D5',
    muted: '#8C9AA5',
    faint: '#26323A',
    blue: '#35E0D0',
    blueF: 'rgba(53,224,208,0.12)',
    orange: '#FFA23A',
    orangeF: 'rgba(255,162,58,0.12)',
    red: '#FF5A6A',
    redF: 'rgba(255,90,106,0.12)',
    green: '#7BE3A0',
    greenF: 'rgba(123,227,160,0.12)',
    purple: '#B08CFF',
    purpleF: 'rgba(176,140,255,0.12)',
    yellow: '#F5D06F',
    paper: '#0B0E12',
    inkF: '#11171D',
    softF: '#151D24',
    mutedF: '#1A232B',
    faintF: '#202A33',
  },
  setTheme() { this.theme = 'night'; return this; },
  background: (stage) => [
    // 64px grid: the two layers are sized in style.css
    'linear-gradient(rgba(255,255,255,0.026) 1px, transparent 1px)',
    'linear-gradient(90deg, rgba(255,255,255,0.026) 1px, transparent 1px)',
    `radial-gradient(${Math.round(stage.w * 0.40)}px ${Math.round(stage.h * 0.52)}px at 72% 26%, rgba(53,224,208,0.10), transparent 68%)`,
    `radial-gradient(${Math.round(stage.w * 0.36)}px ${Math.round(stage.h * 0.50)}px at 18% 82%, rgba(255,162,58,0.075), transparent 70%)`,
    `radial-gradient(${Math.round(stage.w * 0.47)}px ${Math.round(stage.h * 0.65)}px at 50% 50%, #0D1218 0%, #080B0F 55%, #05070A 100%)`,
  ].join(','),
};
