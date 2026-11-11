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
- **Live projects, in gallery order (2026-11-10)**: Self-Illuminating Diamonds (folder `emma-frost`, order 1, half, hover video), Smoking Wearable Wound Prop (`remmick`, order 2, half, hover video), Cyberpunk Deer Mask and Costume (`bloodhound`, order 3, full, hover GIF), ARC Raiders Wasp (`arc-wasp`, order 5, full). Between 2026-11-05 and 11-10 Dante renamed the titles away from franchise names and set Life-Size Cashout Station and Sex Pistols / Six Bullets back to drafts; the folder names did not change.
- **Drafts**: Life-Sized LEGO Knight and Galactic Couture PLINKO still have no photos. Life-Size Cashout Station and Sex Pistols / Six Bullets have photos and covers but carry `draft: true` as of 2026-11-10 (Dante did not say why; ask before publishing them).
- **Placeholders to replace**: the Cashout Station and Smoking Wearable Wound Prop write-ups were drafted from Dante's ArtStation slides and may still carry an HTML comment at the top saying what Dante needs to add (check `CONTENT_STATUS.md`). The ARC Wasp cover is a still Dante wanted to replace with a cleaner shot.
- **Tech art is parked.** Eleven tech-art pages rebuilt from the old Webflow site sit in `content/techart/` with a section definition under `parked_sections` in `site.json`. They are not built. Dante said on 2026-11-04: "this is a fabrication work session... it probably is better on its own separate site anyway." Do not re-add them to this site unless Dante asks.
- **Domain**: `dantexcameron.com` serves the site over HTTPS as of 2026-11-10; the GoDaddy DNS (account held by someone else, registration until 2027-07-29) was switched from Webflow to GitHub Pages. The old Webflow site plan can be cancelled once Dante confirms nothing else depends on it.
- **Two computers**: Dante's main working copy is in OneDrive at `C:\Users\dante\OneDrive\Documents\GitHub\portfolio-site`; a second computer has a clone at `D:\Github\dkb-portfolio-site`. They sync only through git, so commit and push before switching. On 2026-11-04 the second computer's Python lacked Pillow and Markdown; `build.py` now installs them itself on first run.
- Dante edits through the studio on either computer and sometimes leaves edits unpublished; run `git status` before building on anything, and treat uncommitted content changes as Dante's work in progress.
- **Hover clips on phones** (fixed 2026-11-10): the two cover videos were re-encoded small and silent, and `site.js` now buffers a clip before it scrolls into view, shows it only once frames arrive, and retries on the first tap if the phone blocks autoplay. Clips can also go inside write-ups (`![caption](clip.mp4)`).

## What to do next, in Dante's priority order as of 2026-11-10

1. **Photos for LEGO Knight and Galactic PLINKO**, then remove `draft: true`. The HTML comment at the top of each `project.md` lists the shots Dante planned.
2. **Real write-ups** for Cashout Station and the wound prop: weight, how it packs, cost, time, what is printed versus sewn, how the fog rig works. Replace the placeholder paragraphs and delete the comment.
3. **Decide whether Cashout Station and Six Bullets go back live** (both drafts as of 2026-11-10).
4. **Cleaner cover** for ARC Wasp, if Dante still wants one.
5. **Cancel the Webflow plan** now that the domain points here.
6. Later, and only when Dante raises it: a separate tech-art site from `content/techart/`, or re-enabling the section here.

## Rules that matter most (details in STYLE_AND_FEEDBACK.md)

- Never invent facts about a build. If something is unknown, leave a visible `<!-- Dante: ... -->` comment asking for it.
- No em dashes. No AI-sounding roll-ups or buzzwords. Light use of bold. Plain, specific sentences.
- The site speaks in first person as Dante.
- Titles stay overlaid on the covers; gutters stay tight; no plates or wide margins around images.
- This site is fabrication only.
