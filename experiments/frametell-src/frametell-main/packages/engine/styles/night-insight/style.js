/* Night insight · 深色心理图解 / 米白变体
 * 一套独立的套版：项目用 META.style = 'night-insight' 拉进来。
 * META.cream = true 时切米白底：文字、卡片、聊天气泡都走浅色。
 */
const CREAM = !!(window.SCRIPT && window.SCRIPT.META && window.SCRIPT.META.cream);

window.STYLE = {
  id: 'night-insight',
  theme: CREAM ? 'cream' : 'night',
  cream: CREAM,
  palette: CREAM ? {
    ink: '#2B2520', soft: '#5E554C', muted: '#8A7D70', faint: '#D8CBB8',
    blue: '#1F8F89', blueF: 'rgba(31,143,137,0.10)',
    orange: '#C8782A', orangeF: 'rgba(200,120,42,0.10)',
    red: '#B84A4A', redF: 'rgba(184,74,74,0.10)',
    green: '#4C8759', greenF: 'rgba(76,135,89,0.10)',
    purple: '#8A6B9E', purpleF: 'rgba(138,107,158,0.10)',
    yellow: '#D8A83E', paper: '#FBF7EF',
    inkF: '#F3EBDD', softF: '#F5EEE3', mutedF: '#F8F2E8', faintF: '#FBF7EF',
  } : {
    ink: '#F2F6F7', soft: '#C3D0D5', muted: '#8C9AA5', faint: '#26323A',
    blue: '#35E0D0', blueF: 'rgba(53,224,208,0.12)',
    orange: '#FFA23A', orangeF: 'rgba(255,162,58,0.12)',
    red: '#FF5A6A', redF: 'rgba(255,90,106,0.12)',
    green: '#7BE3A0', greenF: 'rgba(123,227,160,0.12)',
    purple: '#B08CFF', purpleF: 'rgba(176,140,255,0.12)',
    yellow: '#F5D06F', paper: '#0B0E12',
    inkF: '#11171D', softF: '#151D24', mutedF: '#1A232B', faintF: '#202A33',
  },
  setTheme() { this.theme = CREAM ? 'cream' : 'night'; return this; },
  background: (stage) => CREAM ? [
    'linear-gradient(rgba(60,50,40,0.045) 1px, transparent 1px)',
    'linear-gradient(90deg, rgba(60,50,40,0.045) 1px, transparent 1px)',
    `radial-gradient(${Math.round(stage.w * 0.40)}px ${Math.round(stage.h * 0.52)}px at 72% 26%, rgba(31,143,137,0.08), transparent 68%)`,
    `radial-gradient(${Math.round(stage.w * 0.36)}px ${Math.round(stage.h * 0.50)}px at 18% 82%, rgba(200,120,42,0.07), transparent 70%)`,
    `radial-gradient(${Math.round(stage.w * 0.47)}px ${Math.round(stage.h * 0.65)}px at 50% 50%, #FFFDF8 0%, #F8F2E8 58%, #F3EBDD 100%)`,
  ].join(',') : [
    'linear-gradient(rgba(255,255,255,0.026) 1px, transparent 1px)',
    'linear-gradient(90deg, rgba(255,255,255,0.026) 1px, transparent 1px)',
    `radial-gradient(${Math.round(stage.w * 0.40)}px ${Math.round(stage.h * 0.52)}px at 72% 26%, rgba(53,224,208,0.10), transparent 68%)`,
    `radial-gradient(${Math.round(stage.w * 0.36)}px ${Math.round(stage.h * 0.50)}px at 18% 82%, rgba(255,162,58,0.075), transparent 70%)`,
    `radial-gradient(${Math.round(stage.w * 0.47)}px ${Math.round(stage.h * 0.65)}px at 50% 50%, #0D1218 0%, #080B0F 55%, #05070A 100%)`,
  ].join(','),
};

// 给 #frame 一个数据标记，让 style.css 能改 #vignette / #frame
if (CREAM && typeof document !== 'undefined' && document.getElementById('frame')) {
  document.getElementById('frame').dataset.theme = 'cream';
}
