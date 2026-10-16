// 页04｜孩子的课本旁边，一部手机亮起一条消息——三年婚外关系意外曝光
SCENES['04'] = (() => {
  const W = 1920, H = 1080;
  const { clamp, lerp, ss, ease, rng } = U;
  const C = { bg:'#F3EDE2', paper:'#FBF8F2', ink:'#1B1A17', gray:'#6B655B', red:'#C8402F', teal:'#2F5D62' };

  const fillP = (c,p,col,a) => { c.fillStyle = col; c.globalAlpha = (a == null ? 1 : a); c.fill(p); };
  const strokeP = (c,p,col,lw,a) => { c.strokeStyle = col; c.globalAlpha = (a == null ? 1 : a);
    c.lineWidth = lw; c.lineJoin = 'round'; c.lineCap = 'round'; c.stroke(p); };
  const piece = (c,p,fill,lw,col,a) => { if (fill) fillP(c,p,fill,a); if (lw) strokeP(c,p,col||C.ink,lw,a); };
  const jrr = (x,y,w,h,r,amp,seed) => { const R = rng(seed), j = () => (R()*2-1)*amp, p = new Path2D();
    p.moveTo(x+r+j(), y+j()); p.lineTo(x+w-r+j(), y+j());
    p.quadraticCurveTo(x+w+j(), y+j(), x+w+j(), y+r); p.lineTo(x+w+j(), y+h-r+j());
    p.quadraticCurveTo(x+w+j(), y+h+j(), x+w-r+j(), y+h+j()); p.lineTo(x+r+j(), y+h+j());
    p.quadraticCurveTo(x+j(), y+h+j(), x+j(), y+h-r); p.lineTo(x+j(), y+r+j());
    p.quadraticCurveTo(x+j(), y+j(), x+r+j(), y+j()); p.closePath(); return p; };
  const jline = (x1,y1,x2,y2,seg,amp,seed) => { const R = rng(seed), p = new Path2D(); p.moveTo(x1,y1);
    for (let i=1;i<=seg;i++){ const u=i/seg; p.lineTo(lerp(x1,x2,u)+(R()*2-1)*amp, lerp(y1,y2,u)+(R()*2-1)*amp); }
    return p; };
  const bell = (x,a,b) => { const u = (x-a)/(b-a); return (u>0 && u<1) ? Math.sin(u*Math.PI) : 0; };
  const circ = (r) => { const p = new Path2D(); p.arc(0,0,r,0,Math.PI*2); return p; };

  // 载体①：孩子摊开的课本（左下）
  const BOOK = (() => { const p = new Path2D();
    p.moveTo(98,800); p.quadraticCurveTo(240,768,383,782);
    p.quadraticCurveTo(526,768,672,800); p.lineTo(672,996);
    p.quadraticCurveTo(526,964,383,978); p.quadraticCurveTo(240,964,98,996);
    p.closePath(); return p; })();
  const CREASE = jline(383,782,383,978,6,1.6,11);
  const RULES = [ jline(140,850,334,838,5,1.6,12), jline(140,896,334,884,5,1.6,13), jline(140,942,334,930,5,1.6,14),
                  jline(432,838,626,850,5,1.6,15), jline(432,884,626,896,5,1.6,16), jline(432,930,626,942,5,1.6,17) ];
  const NOTES = [ jline(166,886,294,878,4,1.6,21), jline(166,932,264,926,4,1.6,22) ];

  // 载体②：手机。主角＝屏幕上那条消息，宽 1004px（画面 52%）
  const PX=700, PY=330, PW=1160, PH=690;
  const PHONE  = jrr(PX,PY,PW,PH,58,2,3);
  const SCREEN = jrr(PX+30,PY+30,PW-60,PH-60,36,2,4);
  const NOTCH  = jrr(PX+PW/2-70,PY+44,140,16,8,1.2,5);
  const BX=778, BY=412, BW=1004, BH=246;
  const BUBBLE = jrr(BX,BY,BW,BH,44,2.4,6);
  const ICON   = jrr(816,488,96,96,26,2,7);
  const L1 = jline(946,514,1300,514,8,2.2,41);
  const L2 = jline(946,574,1696,574,12,2.2,42);
  const DOT = circ(26), BADGE = { x:1772, y:430 };
  const LESSON = jrr(778,726,1004,228,30,2.2,61);
  const LL1 = jline(812,792,1500,792,7,2,62);
  const LL2 = jline(812,852,1320,852,7,2,63);
  const TRACK = jline(812,918,1748,918,11,2,64);
  const TXT = '意外曝光', FS = '76px KaiTi,"KaiTi GB2312","Segoe Script",cursive';

  return {
    draw(c, lt, t) {
      c.globalAlpha = 1; c.fillStyle = C.bg; c.fillRect(0,0,W,H);   // 背景自己画

      piece(c, BOOK, C.paper, 4.6);                                  // 课本
      strokeP(c, CREASE, C.gray, 3.6, 0.85);
      for (const l of RULES) strokeP(c, l, C.gray, 3, 0.45);
      for (const l of NOTES) strokeP(c, l, C.ink, 4.4, 0.5);

      // 手机入画：先歪着，1.5 秒里自己坐正；5.0s 被这条消息震一下
      const settle = -0.02*(1 - ss(0,1.5,lt));
      const buzz   = 0.011*Math.sin(lt*34)*bell(lt,5.0,6.1);
      const focus  = ss(8.8,10.8,lt);                                // 收束：视线从网课挪到消息

      c.save();
      c.translate(1280,675); c.rotate(settle+buzz); c.translate(-1280,-675);

      piece(c, PHONE, C.paper, 6);
      fillP(c, SCREEN, C.gray, 0.18); strokeP(c, SCREEN, C.gray, 3.2, 0.55);
      fillP(c, NOTCH, C.ink, 0.8);

      // 屏幕底下网课还在放：进度条一路走到底，收束时退到背景
      const lA = lerp(0.5,0.13,focus);
      fillP(c, LESSON, C.teal, lA*0.10);
      strokeP(c, LESSON, C.teal, 3.6, lA*0.9);
      strokeP(c, LL1, C.teal, 5, lA*0.6);
      strokeP(c, LL2, C.teal, 5, lA*0.6);
      strokeP(c, TRACK, C.teal, 12, lA*0.32);
      const prog = ease.inOut(clamp((lt-0.6)/9.8));
      strokeP(c, jline(812,918,812+936*prog,918,9,2,71), C.teal, 12, lA*0.95);

      // 第一帧就有主角的走向：屏幕上那道极淡的压痕
      strokeP(c, BUBBLE, C.gray, 4.2, 0.14 + 0.07*(0.5 + 0.5*Math.sin(lt*4.2)));

      // 主角长大：同一个圆角框，从左起笔，一笔扫满
      const sw = ease.inOut(clamp((lt-1.2)/2.0));
      if (sw > 0.002) {
        c.save(); c.beginPath(); c.rect(BX-34,BY-34,(BW+68)*sw,BH+68); c.clip();
        piece(c, BUBBLE, C.paper, lerp(4.6,6.2,focus));
        piece(c, ICON, C.red, 4.6, C.ink);
        strokeP(c, L1, C.ink, 13, 0.9);
        strokeP(c, L2, C.ink, 8, 0.5);
        c.restore();
      }

      // 未读小红点：扫满后弹出来，结尾轻轻一跳
      const bp = ease.outBack(clamp((lt-3.3)/0.85));
      if (bp > 0.01) {
        const pu = 1 + 0.18*bell(lt,9.3,10.7);
        c.save(); c.translate(BADGE.x,BADGE.y); c.scale(bp*pu,bp*pu);
        fillP(c, DOT, C.red, 1); strokeP(c, DOT, C.ink, 4.6, 1);
        c.restore();
      }

      c.restore();

      // 屏上字：6.6s（0.6 倍时长）逐字写出，落在左上留白
      const tp = clamp((lt-6.6)/0.9);
      if (tp > 0.01) {
        const R = rng(91);
        c.font = FS; c.textBaseline = 'middle'; c.fillStyle = C.ink;
        for (let i=0;i<4;i++){
          const jx=(R()*2-1)*5, jy=(R()*2-1)*7, ra=(R()*2-1)*0.05;
          const k = ease.out(clamp((tp - i*0.2)/0.34));
          if (k > 0.01) {
            c.save(); c.globalAlpha = k;
            c.translate(174 + i*96 + jx, 190 + jy); c.rotate(ra);
            c.fillText(TXT[i], 0, 0); c.restore();
          }
        }
        c.globalAlpha = 1;
      }
    },
  };
})();
