# Session log

Newest at the bottom. One entry per working session: date, who (Dante plus which assistant), what changed, what was left open.

## Before this repo (late October to early November 2026)

Dante and a Claude session worked through resume versions, the ArtStation structure and captions (RSC, Body of Mine, City of Apparition), a personal knowledge base, and job-search tooling. A portfolio reviewer then asked for a fabrication-only, cover-first site, which led to this repo. See `RELATED_WORK.md`.

## 2026-11-04, Dante with Claude (Claude Code desktop app)

Built the whole site in one long session.

- Created the repo: `build.py`, templates, `site.css`, `site.js`, `preview.bat`, `requirements.txt`, Pages workflow, `CNAME`, README. Seeded five fabrication projects from Dante's ArtStation images (Remmick, Bloodhound with a hover GIF, Cashout Station, Six Bullets, ARC Wasp) and three drafts without photos (LEGO Knight, Galactic PLINKO, Emma Frost).
- Dante created `github.com/alighieri2000/dkb-portfolio-site`, pushed, made it public, and deployed. Domain DNS left with the GoDaddy account holder.
- Added the studio (`studio.py`, `studio.bat`): project list, editor, uploads, cover and hover selection, build, preview, publish.
- Polish round: header and intro above the gallery, project pages with gallery left and sticky spec sheet right (`summary:` and `links:` front matter).
- Scraped the old Webflow site into `webflow-archive/` and converted its eleven project pages into `content/techart/` as a second section with `@youtube` embeds and trailer-frame covers; rewrote them in first person by hand.
- Dante's feedback: titles back onto the covers, smaller margins, full and half tile sizes. Implemented the 2:1 and 1:1 grid, `size: half`, overlaid labels, tight gutters, and a size select in the studio.
- Dante parked tech art: section moved to `parked_sections`, nav hides section links when only one section exists. Live site is fabrication only.
- Dante hit a build failure on a second computer (`D:\Github\dkb-portfolio-site`, Python without Markdown and Pillow). Added `ensure_packages()` to `build.py`, a startup import in `studio.py`, a hint on the studio's failure page, and a README note. Tested from a bare venv. Pushed as `aa8cb02`.
- Wrote this `ai/` folder so the work can continue in another assistant.

Open at the end of the session: photos for the three drafts; real write-ups for Cashout Station and Remmick; cleaner covers for Cashout and ARC Wasp; order tie between Bloodhound and Cashout (both 3); domain cutover after DNS; tech art parked for a possible separate site.

## 2026-11-05 to 11-09, Dante with other Claude sessions (forks of the 11-04 session) and the studio

Known from the git history and the files, not from a log: the domain went live; Dante added hover videos for Emma Frost and Remmick, new covers, and renamed the titles (Self-Illuminating Diamonds, Smoking Wearable Wound Prop, Cyberpunk Deer Mask and Costume); Cashout Station and Six Bullets were set back to drafts. A session added the studio's Cover framing panel (`focus:` key), dark-mode colours in the CSS, the git-ignored `source-media/` folder, a first re-encode of the Emma Frost clip, a link field that accepts plain addresses, and a fix for images that sit directly above a line of text (`IMG_MD` in `build.py`). Commits dc42f42, e8f4ab0, c2a5573.

## 2026-11-10, Dante with Claude (Claude Code desktop app)

- Dante: the Emma Frost and Remmick hover videos do not play on mobile; the Bloodhound GIF does. Both files were H.264 and the host answers range requests, so the likely causes were size (Remmick was 14.5 MB with an audio track) and phones that block autoplay. Re-encoded both with the ffmpeg bundled in the `imageio-ffmpeg` Python package (silent, High profile level 4.0, yuv420p, 960 or 1280 wide, CRF 26, 2 Mbps cap, faststart): Remmick 2.6 MB, Emma Frost 1.3 MB. Originals kept in `source-media/`.
- `site.js` rewritten for covers: on touch screens a clip starts loading one screen before it is visible; the clip is shown only on the video's `playing` event so a stalled video never covers the still; a refused `play()` is retried on the first tap, click or key press. Desktop hover path unchanged.
- Dante: "can you make it so i can insert the videos into the pages too?" `![caption](clip.mp4)` (mp4, webm, gif) in a write-up now renders a `<figure>` with a muted, looping, inline video that keeps its controls and plays while on screen (pauses when scrolled past, stays paused after a manual pause); gifs render as plain images. `mp4_size()` reads the tkhd box so the page reserves the right aspect ratio. The studio's Insert button now works for clips too. README documents both and gives the ffmpeg shrink command.
- Verified in the desktop app's browser pane: phone emulation plays both cover clips once scrolled, the write-up clip plays, pauses and resumes correctly, and the desktop hover path still works. Not verified on a real phone.
- Published together with Dante's pending Bloodhound title change.

Open: a real-phone check of the covers; whether the Bloodhound GIF should become an MP4; everything listed under HANDOFF's next steps.
