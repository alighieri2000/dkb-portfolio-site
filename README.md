# dantexcameron.com

A fabrication portfolio: a page of full-screen covers, one per project, each opening a project page with large images and text between them. Built from plain files in `content/`, published free on GitHub Pages under your own domain.

## How it is organized

The live site is the fabrication gallery at the root (`content/projects/`). A tech-art gallery (`content/techart/`, rebuilt from the old Webflow pages) is parked: its section definition sits under `parked_sections` in `content/site.json`, and moving it into `sections` publishes it at `/tech-art/` with its own headline and intro. The same mechanism adds any further gallery.

```
content/
  site.json                 your name, email, the sections, nav links
  CNAME                     the domain the site is served at
  techart/                  the tech-art gallery (same layout as below)
  projects/
    remmick/
      project.md            the write-up (see below)
      cover.jpg             the full-screen cover on the home page (jpg, png, or webp)
      hover.mp4             optional: plays when someone hovers the cover (mp4, webm, or gif)
      01.jpg, 02.jpg ...    the images the write-up refers to
build.py                    turns content/ into site/
preview.bat                 double-click to build and open a local preview
```

## The easy way: the studio

Double-click `studio.bat`. A page opens at `http://localhost:8001/` listing every project. From there you can create a project, upload a cover, a hover clip and images, pick which file is the cover and which is the hover clip, fill in the spec sheet and the write-up, build and preview the site, and publish to GitHub with one button. It only edits the files described below, so you can always fall back to editing them by hand.

## Add or edit a project by hand

1. Make a folder under `content/projects/`. The folder name becomes the page address (`remmick` becomes `dantexcameron.com/remmick/`), so use lowercase and hyphens.
2. Drop in `cover.jpg` (at least 2400 px wide; it fills the whole screen) and your images.
3. Write `project.md`. The top is a few labeled lines between `---` markers; everything after is the write-up:

```
---
title: Remmick
subtitle: Costume FX for the villain of Sinners
year: 2025
client: Personal build
role: Costume FX design and fabrication
materials: 3D-printed parts, fog effect
tools: Maya, ZBrush, FDM printing
order: 2
---

A paragraph of text.

![A caption under the image](01.jpg)

More text. Two images side by side:

![](02.jpg) ![](03.jpg)

## A heading

- A list
```

   `size: half` makes the project a square that shares a row with the next half-size project; leave it out for a full-width rectangle. `order` sets the position on the home page (1 is the top). Any label you leave out is simply not shown. `draft: true` keeps a project off the published site while you work on it; previews still show it. Other optional lines: `summary:` (the paragraph in the side panel), `links:` (`Label | https://url ; Label | https://url`, shown as buttons), `cover: 03.jpg` and `hover: clip.mp4` to use files not named cover/hover, and `timeline:`.

   A video file works like an image: `![caption](clip.mp4)` (mp4, webm or gif) puts the clip in the write-up, where it plays silently while on screen and keeps its controls for sound or scrubbing. Keep such clips small the same way as hover clips. A line containing only `@youtube VIDEOID` embeds that YouTube video. Tech-art pages also use `developer:`, `platform:`, `context:` and `awards:` in the spec sheet.

   On the project page the images and write-up scroll on the left while the title, spec sheet and summary stay pinned on the right. Text in the write-up appears between the images, so use it for short process notes; the longer description belongs in `summary`.

4. Preview: double-click `preview.bat`. It builds the site and opens it in your browser. Close the window when you are done.
5. Publish: commit and push the change (GitHub Desktop: write a summary, click Commit, click Push). GitHub rebuilds the site in about a minute. You can also edit `project.md` or upload images straight on github.com in the browser; every saved change publishes the same way.

## Choosing what shows in a cover

Covers are cropped to fit the gallery frames (a wide rectangle, a square, and a tall phone shape), so sometimes the crop cuts off the part you care about. In the studio, open a project: under the cover and hover-clip menus there is a **Cover framing** panel showing all three frames. Drag the picture inside any frame and the others follow. "Show hover clip" previews the clip in the same frames, and "Center" resets. Saving writes a `focus:` line to `project.md` (for example `focus: 30% 50%`); the cover and its hover clip both use it. It moves the crop; it does not zoom, so for a tighter crop, trim the image first.

## Header and site text

In the studio, press **Edit header and site text** on the project list. That page edits your name, email, the links at the top right, the search-result description, and the home page headline, paragraph, and small line. It writes `content/site.json`, and Publish sends it live like any other change.

## Hover clips

Put `hover.mp4` (or `.webm`, or `.gif`) next to the cover. Keep it short (5 to 10 seconds, it loops), silent, 1080p or smaller, and under about 4 MB; an MP4 is a tenth the size of the same GIF. On phones, which have no hover, the clip plays while that cover fills the screen. If a phone refuses to start videos on its own (iPhone Low Power Mode, or Auto-Play Video Previews turned off in Accessibility settings), the still stays in place and the clip starts at the first tap on the page.

Phones need small, plain H.264 files: no audio track, 1280 px wide or less, and a few megabytes at most. A 15 MB clip may never get far enough to play on a cellular connection. If you have ffmpeg, this shrinks a clip to that shape:

```
ffmpeg -i big.mp4 -an -vf "scale=1280:-2" -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -crf 26 -maxrate 2000k -bufsize 4000k -movflags +faststart hover.mp4
```

## Domain

The domain `dantexcameron.com` is registered at GoDaddy (through July 2027) and currently points at the old Webflow site. To point it here instead:

1. In GoDaddy DNS, delete the old `A` and `CNAME` records that point to Webflow, then add:
   - `A` records for `@` to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - a `CNAME` record for `www` to `alighieri2000.github.io`
2. On GitHub, in the repository's Settings, Pages: set the source to "GitHub Actions", enter `dantexcameron.com` as the custom domain, wait for the DNS check, then tick "Enforce HTTPS".
3. Cancel the Webflow site plan. The domain itself renews at GoDaddy (about $20 a year); moving it to Cloudflare Registrar later roughly halves that, but there is no hurry.

## Continuing with an AI assistant

The `ai/` folder is a handoff for any AI assistant: who the site is for, how it works, what each project still needs, what was decided and why, and a dated log. Start a new session by having the assistant read `ai/HANDOFF.md`, `ai/STYLE_AND_FEEDBACK.md` and `ai/SITE_INTERNALS.md`, and end each session by updating `ai/SESSION_LOG.md`. The repository is public, so nothing private goes in there.

## Local requirements

Python 3. The first time `studio.bat` or `preview.bat` runs on a computer it installs the two packages the build needs (Pillow for images, Markdown for text) for that Python. If that fails, for example without internet or with a locked-down Python, run this in a terminal in this folder:

```
python -m pip install -r requirements.txt
```

GitHub builds the site on its own servers, so none of this is needed for publishing, only for local previews.
