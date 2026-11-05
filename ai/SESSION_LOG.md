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
