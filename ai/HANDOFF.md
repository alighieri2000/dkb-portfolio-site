# Handoff: dantexcameron.com, Dante Cameron's fabrication portfolio

Written 2026-11-04. Read this first.

## Who

Dante Cameron, New York (pronouns were not stated in the session; use they/them unless Dante says otherwise). Technical artist and fabricator: props, costumes, wearable effects and installations, designed in Maya and ZBrush and built in the shop (FDM and resin printing, vacuum forming, EVA foam, sewing, molding, paint, small electronics). Dante also has a realtime and VR tech-art background: SCAD's Immersive Reality program (2020 to 2022) and Agile Lens LLC in New York (February 2023 to October 2026: VR and digital-twin work for clients such as the Royal Shakespeare Company, Dell, SK-II and Four Seasons, plus the Meta Quest release of Body of Mine). Dante is now looking for work and this site is part of that search, aimed specifically at fabrication roles.

GitHub account: `alighieri2000`. Public email on the site: `dantexcameron@gmail.com`. ArtStation: `dantecameron.artstation.com` (holds the studio and tech-art work; this site deliberately does not).

Dante is technical enough to run Python scripts, edit Markdown and use GitHub Desktop, and prefers plain, direct explanations. Dante tests things in the browser and gives blunt feedback. Build what was asked, then ask.

## What this repository is

A static fabrication portfolio, free to host and owned outright, replacing an expensive Webflow site.

- **Home page**: a stack of large covers, one per project, with the title, subtitle and a year and materials line overlaid bottom-left. Full-width covers are 2:1 rectangles; `size: half` covers are 1:1 squares that sit two to a row. Hovering a cover plays a short clip if the project has one (`hover.mp4`, `.webm` or `.gif`); on phones the clip plays when the cover is mostly on screen.
- **Project pages**: images and short process notes scroll on the left, while the title, a spec sheet (year, client, role, materials, tools and so on), a summary paragraph and optional link buttons stay pinned on the right. Previous and next links at the bottom.
- **Content** lives in `content/projects/<slug>/project.md` (key: value front matter between `---` lines, then a Markdown write-up) next to the project's images. `content/site.json` holds the name, intro text, nav links and the list of sections.
- **Build**: `python build.py` turns `content/` into `site/` (resized WebP variants of every image, HTML from the templates). `--drafts` includes draft projects; `--serve` also opens a preview at `localhost:8000`.
- **Studio**: `python studio.py` (or `studio.bat`) is a local editor at `localhost:8001` for creating projects, uploading images and clips, choosing the cover, hover clip and size, editing the text, building, previewing and publishing (git add, commit, push) with one button.
- **Deploy**: pushing to `main` runs `.github/workflows/pages.yml`, which installs the two Python packages, runs `build.py` and deploys `site/` to GitHub Pages. `content/CNAME` holds the domain.

Full technical detail is in `SITE_INTERNALS.md`.

## Where it stands (2026-11-04)

- The site builds and deploys from `github.com/alighieri2000/dkb-portfolio-site` (public; Pages needs that on a free plan).
- **Live projects, in gallery order**: Remmick (order 2, full), Bloodhound Whistling Winter (order 3, full, has a hover GIF), Life-Size Cashout Station (order 3, full), Sex Pistols / Six Bullets (order 4, half), ARC Raiders Wasp (order 5, half). Bloodhound and Cashout both carry order 3 and sort by title; give them distinct numbers when Dante decides which comes first. The two half-size squares share the last row.
- **Drafts waiting on photos**: Life-Sized LEGO Knight, Galactic Couture PLINKO, Emma Frost. Each has front matter and a write-up but no cover, so the build skips them; `draft: true` keeps them off the published site either way.
- **Placeholders to replace**: the Cashout Station and Remmick write-ups were drafted from Dante's ArtStation slides and carry an HTML comment at the top saying what Dante needs to add. The Cashout and ARC Wasp covers are stills Dante wants to replace with cleaner shots.
- **Tech art is parked.** Eleven tech-art pages rebuilt from the old Webflow site sit in `content/techart/` with a section definition under `parked_sections` in `site.json`. They are not built. Dante said on 2026-11-04: "this is a fabrication work session... it probably is better on its own separate site anyway." Do not re-add them to this site unless Dante asks.
- **Domain**: `dantexcameron.com` is registered at GoDaddy until 2027-07-29 and was pointed at the old Webflow site. The GoDaddy account belongs to someone else, and Dante was waiting on them to change the DNS records (the exact records are in the repo `README.md`). One check during the session saw the records already resolving to GitHub, so verify with `nslookup dantexcameron.com` before assuming either state. After DNS: set the custom domain in the repo's Pages settings and tick Enforce HTTPS. Then cancel the Webflow site plan.
- **Two computers**: Dante's main working copy is in OneDrive at `C:\Users\dante\OneDrive\Documents\GitHub\portfolio-site`; a second computer has a clone at `D:\Github\dkb-portfolio-site`. They sync only through git, so commit and push before switching. On 2026-11-04 the second computer's Python lacked Pillow and Markdown; `build.py` now installs them itself on first run.
- Everything is committed and pushed as of the end of 2026-11-04.

## What to do next, in Dante's priority order as of 2026-11-04

1. **Photos for the three drafts**, then remove `draft: true`. The HTML comment at the top of each `project.md` lists the shots Dante planned.
2. **Real write-ups** for Cashout Station and Remmick: weight, how it packs, cost, time, what is printed versus sewn, how the fog rig works. Replace the placeholder paragraphs and delete the comment.
3. **Cleaner covers** for Cashout Station and ARC Wasp.
4. **Domain cutover** once DNS is confirmed (Pages settings, HTTPS, cancel Webflow).
5. Later, and only when Dante raises it: a separate tech-art site from `content/techart/`, or re-enabling the section here.

## Rules that matter most (details in STYLE_AND_FEEDBACK.md)

- Never invent facts about a build. If something is unknown, leave a visible `<!-- Dante: ... -->` comment asking for it.
- No em dashes. No AI-sounding roll-ups or buzzwords. Light use of bold. Plain, specific sentences.
- The site speaks in first person as Dante.
- Titles stay overlaid on the covers; gutters stay tight; no plates or wide margins around images.
- This site is fabrication only.
