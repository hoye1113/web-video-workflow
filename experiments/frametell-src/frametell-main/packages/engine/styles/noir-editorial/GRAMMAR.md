# Noir editorial · grammar card（暗色宣言体）

Reference: a 40-second channel manifesto cut into 11 chapter cards. The camera barely moves; the page is a printed spread with a HUD, not a slide.

## In one sentence

A dark editorial spread: one sentence, one diagram, and a lot of deliberate silence. The type is the image.

## Picture

- **Ground:** near-black teal (`#060A0B`), a faint 64px drafting grid, a horizon haze at 31%, grain, a heavy vignette. Never pure black and never a bright panel.
- **Palette:** bone (`ink`), old gold (`orange`), muted teal (`blue`), coral (`red`). At most two accents speak on one page. Gold is the title, teal is the live/answer line, red is only false/error.
- **One idea per page.** A chapter number, one serif headline, one supporting line, one line-art centre (mic, waveform, book, eye, curve, card). Everything else is microtype.
- **Hairlines, not boxes.** 1px rules, dashed connectors, tiny registration marks, IDs like `03.01`. They are the texture of the style; keep them at the edges and out of the reading path.
- **Type:** Chinese serif headline 72–96px, English mono 12–18px with 0.18–0.24em tracking, narration 32–36px. Use a high-contrast Songti. SimSun is the proof stand-in; license a display Songti for delivery.
- **Bottom band:** the last 12% belongs to narration. Nothing else enters it.

## Motion

- **0.3–0.7s, then hold.** Titles reveal per character (opacity + 0.2em rise + a short blur), rules draw left to right, diagrams draw on, counters roll once.
- **One accent motion per page.** The rest is still. No uniform slow push, no bounce, no flicker loops.
- **Chapters cross-fade.** A 0.3–0.5s dip is enough; hard cuts are for a deliberate interruption only.
- **HUD is fixed.** Chapter number, edge IDs and narration live on the HUD; the content layer may move, the HUD never does.

## Pacing

- 3–5 seconds per chapter, 8–12 chapters for a 40–60s manifesto.
- Each page has 2–4 visible events: chapter, title, diagram, narration. More than that and the reader stops reading.
- End on a sentence, not a CTA card.

## Never

- Neon, blue-purple, glitch, cyberpunk, matrix rain, heavy bloom.
- White cards, bright fills, stock-photo collages, 3D bevels.
- A page with only a title and nothing to look at; a page with five competing diagrams.
- Text under 20px for anything that must be read; decorative IDs may be 11–13px.
- Narration inside the bottom 12% if a separate subtitle track will be burned in.

## Components (`kit.js`)

`noirHeader` · `noirReveal` · `noirLabel` · `noirNarration` · `noirCounter` · `noirConnector` · `noirNode` · `noirCurve` · `noirEye` · `noirWave` · `noirBook` · `noirGhost` · `noirCard` · `noirHairline`

One page = one `ENGINE.visual`; call `P.hud.noirHeader(...)` and `P.hud.noirNarration(...)` for the fixed frame, `P.noirReveal(...)` / `P.noirCurve(...)` for the content.
