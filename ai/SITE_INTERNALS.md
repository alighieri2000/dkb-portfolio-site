# Site internals

How the code works, as of 2026-11-04. Everything is plain Python 3 (standard library plus Pillow and Markdown), static HTML, one CSS file and one small script. No framework, no build tool beyond `build.py`.

```
build.py                 content/ -> site/
studio.py, studio.bat    local editor at http://localhost:8001/
preview.bat              python build.py --serve  (preview at http://localhost:8000/)
requirements.txt         pillow>=10, markdown>=3.5
templates/               index.html (gallery), project.html, 404.html
assets/                  site.css, site.js, favicon.svg  (copied into site/assets/)
content/site.json        name, description, email, copyright_year, sections, links, parked_sections
content/CNAME            dantexcameron.com  (copied to site/CNAME)
content/projects/        the fabrication gallery (home page)
content/techart/         the parked tech-art gallery (not built)
webflow-archive/         raw HTML, text and assets scraped from the old Webflow site, plus manifest.json
site/                    build output, git-ignored
.github/workflows/pages.yml
```

## content/site.json

- `sections`: a list of `{dir, path, title, headline, intro, where}`. `dir` is the folder under `content/`; `path` is the URL folder (`""` for the home page). The first section is the home page. Currently one section: `projects` at the root, titled Fabrication.
- `links`: nav links shown after the section links. `href` starting with `http` opens in a new tab. `#contact` scrolls to the footer email.
- `parked_sections`: ignored by the build. The tech-art section definition sits here; moving it into `sections` publishes `/tech-art/`.
- The nav shows section links only when there is more than one section (`nav_for` in `build.py`).

## project.md

Front matter is `key: value` lines between `---` markers; lines starting with `#` are ignored by the build. Then a Markdown body.

Keys the build uses:

| key | use |
|---|---|
| `title`, `subtitle` | title and the one-line subtitle; both appear on the cover label and the project page |
| `year`, `client`, `developer`, `role`, `platform`, `materials`, `tools`, `timeline`, `context`, `awards`, `status` | spec sheet rows, in that order, skipped when empty |
| `year`, `materials`, `platform` | also joined with ` · ` into the small line on the cover label |
| `summary` | Markdown, rendered in the side panel under the spec sheet |
| `links` | `Label | https://url ; Label | https://url`, rendered as buttons in the side panel |
| `cover` | file name of the cover image (default `cover.*`); extension is ignored, any of jpg/jpeg/png/webp is found |
| `hover` | file name of the hover clip (default `hover.*`); mp4 or webm become `<video>`, gif becomes `<img>` |
| `size` | `half`, `square` or `small` make a 1:1 half-width tile; anything else is full |
| `focus` | `50% 30%`: which part of the cover (and its hover clip) stays in view when a frame crops it; written by the studio's Cover framing panel, applied as `object-position` |
| `order` | sort key in the gallery, lowest first, ties broken by lowercase title; default 999 |
| `draft` | `true`, `yes` or `1` hides the project unless built with `--drafts` |

`hero` appears in the studio's key order for historical reasons but the build ignores it. A project without a cover image is skipped with a console message even when not a draft.

Body rules (`render_body`):

- Markdown with the `extra` and `sane_lists` extensions.
- A paragraph that is only images becomes `<figure>` elements; the alt text becomes the caption. Several images in one paragraph become `<div class="row" style="--n:N">` and sit side by side. Before Markdown runs, `IMG_MD` moves any `![]()` run onto its own paragraph, so an image with text on the very next line still renders.
- `![caption](clip.mp4)` (also webm or gif) is a clip in the write-up: the file is copied unchanged into `_img/`; mp4 and webm become `<video class="clip" muted loop playsinline controls preload="metadata">` (mp4 also gets `style="aspect-ratio:W / H"` from `mp4_size()`, a tiny MP4 box reader), gif becomes `<img class="clip">`. `site.js` plays and pauses these by visibility.
- A paragraph that is exactly `@youtube VIDEOID` becomes a `youtube-nocookie.com` iframe inside `<div class="video">`.
- Image paths are relative to the project folder; missing files print a warning and are dropped.
- HTML comments pass through Markdown and do not render, which is how placeholder notes to Dante are left in the files.

## build.py

1. Reads `site.json`, cleans `site/` but keeps every `_img` folder (the WebP cache), copies `assets/` and `CNAME`, writes `.nojekyll`.
2. For each section: loads projects (`load_section`), sorts them, renders a cover tile and a project page for each, then the section's index page. Root paths are computed from the section depth (`../` per level) so the site works from any base.
3. Writes `404.html`.

Images: `variants()` writes `name-WIDTH.webp` copies into the page's `_img/` folder at 2400 and 1200 px for covers and 1800 and 900 px for body images (never upscaled), WebP quality 84, EXIF orientation applied, skipped when the copy is newer than the source. `picture()` emits an `<img>` with `srcset`, `sizes`, `aspect-ratio` from the source, lazy loading except the first cover.

Cover tile markup: `<a class="cover full|half [has-motion]" href="slug/" style="--i:N"><div class="frame">` still image, optional motion element with `data-src` (not `src`, so nothing loads until hovered), then `<span class="label">` with `.num` (two-digit index), `.t` (title in `<strong>`, subtitle in `<em>`) and `.meta` (the year, materials, platform line).

Template filling (`fill`) is plain `{{name}}` replacement, run twice because nav links carry `{{root}}` inside them. Placeholders: index.html uses `root, nav, covers, headline, intro, where, page_title, site_name, site_description, email, year`; project.html uses `root, nav, title, subtitle, spec, summary, links, body, prevnext, section_title, section_href, draft_note` plus the common ones; 404.html uses `root, nav, site_name`.

`ensure_packages()` runs before the third-party imports: if Pillow or Markdown is missing for the running Python it pip-installs them and prints a first-run line; if pip fails it exits with the exact command to run. `studio.py` imports `build` at startup so this happens in the console before the first build.

`--serve` builds with drafts and serves `site/` on `127.0.0.1:8000`, opening the browser.

## assets/site.css

Tokens on `:root`: `--bg` (#f3f4f6), `--glint` (pink, orange, cyan gradient used as the hover line), `--display`, `--body`, `--mono` font stacks, `--gutter: clamp(12px,1.6vw,24px)`, `--gap: clamp(8px,1vw,14px)`.

- `.top`: header with `.brand` and `nav`. `.intro-home`: headline, intro, `.where`.
- `.covers`: a two-column grid with `--gap`. `.cover.full` spans both columns with a 2:1 frame; `.cover.half` is one column with a 1:1 frame. `.frame` clips the image; `.still` and `.motion` are stacked, `.motion` fades in while `.cover.playing`. `.frame::after` draws the glint line. `.label` is absolutely positioned bottom-left with a gradient scrim; half tiles use smaller label type.
- `.sheet-layout`: project page grid, `.gallery` left and `.side` right (sticky). `.spec` is a `<dl>` of rows; `.summary`; `.links` buttons; `.draft-note`. `.gallery .row` lays figures side by side using `--n`. `.gallery .video` is a 16:9 box for YouTube embeds; `.gallery figure video.clip` styles write-up clips like images.
- A `prefers-color-scheme: dark` block (added 2026-11-05 by another session) redefines the colour tokens, so the site is dark on phones and desktops set to dark mode; photos get a slight brightness reduction there.
- `.pn` previous and next; `.foot` footer with the copyable email.
- Breakpoints at 900 px (side panel moves under the gallery), 700 px and 640 px (single-column covers, smaller type). `prefers-reduced-motion` disables the clip fade and autoplay.

## assets/site.js

- Hover clips: for each `.cover.has-motion`, on devices that can hover, `pointerenter` and focus load the clip (moving `data-src` to `src`) and play it; leave and blur stop it. On touch devices one IntersectionObserver with `rootMargin: 100%` starts loading a clip (`preload="auto"`) while it is still a screen away, and a second plays whichever cover is at least 60 percent visible and pauses it when it leaves. The `.playing` class (which fades the clip in over the still) is added for videos only on the `playing` event and removed on `waiting` and `pause`, so a slow or refused video never hides the still. A `play()` that rejects (iPhone Low Power Mode, Auto-Play Video Previews off, data savers) is queued and retried on the first `touchend`, `pointerup` or `keydown`. Reduced-motion users get stills only.
- Write-up clips (`.gallery video.clip`): muted and inline, played at 50 percent visibility and paused when scrolled out. A pause the script did not cause marks the clip `data-manual`, and it is left alone from then on.
- Email: elements with `.email` and `data-email` copy the address on click and show "Copied" for a moment.

## Clip encoding for phones

What played on desktop but not on phones (2026-11-10) was a 14.5 MB H.264 file with an audio track and a 2.7 MB High-profile level 5.0 file. Phones need small, plain files: H.264 High profile at level 4.0 or lower, `yuv420p`, no audio, 1280 px wide or less, a 2 Mbps cap, `+faststart`. The README gives the ffmpeg command. On the OneDrive computer ffmpeg is not on the PATH, but the `imageio-ffmpeg` Python package ships one: `python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`. Put the original in `source-media/<slug>/` (git-ignored) before overwriting the clip in `content/`, so `project.md` keeps pointing at the same file name. GitHub Pages supports byte-range requests, so that was not the problem.

## studio.py

A `ThreadingHTTPServer` on `127.0.0.1:8001`, standard library only; `--no-open` skips opening the browser. Multipart uploads are parsed with `email.parser.BytesParser`.

Routes:

| route | what |
|---|---|
| `GET /` | all sections, their projects (thumb, title, order, live or draft, cover present), build, preview and publish buttons, new-project form |
| `GET /edit/<dir>/<slug>` | the editor: text fields from `FIELDS`, cover and hover selects built from the files in the folder, size select, Cover framing panel (writes `focus:`), order, draft checkbox, summary, write-up textarea with an Insert button per image and clip, upload form, delete buttons |
| `GET /files/<dir>/<slug>/<name>` | serves a content file for thumbnails |
| `GET /preview/...` | serves `site/` |
| `POST /new` | creates `content/<dir>/<slug>/project.md` as a draft with the next order number; slug must match `^[a-z0-9][a-z0-9-]{0,60}$` |
| `POST /save/<dir>/<slug>` | rewrites `project.md` from the form (`write_project` keeps a fixed key order, then any extra keys) |
| `POST /upload/<dir>/<slug>` | saves images and clips (jpg, jpeg, png, webp, gif, mp4, webm) |
| `POST /delete/<dir>/<slug>` | deletes one image or clip |
| `POST /build` | runs `sys.executable build.py --drafts`; on failure shows stdout and stderr, with a pip hint when the error is a missing module |
| `POST /publish` | `git add -A`, `git commit -m <msg>`, `git push`; "nothing to commit" is not treated as failure |

The studio has its own `read_project` (slightly simpler than the build's: it does not skip `#` lines). If you add a front-matter key, add it to `FIELDS` or the form and to `write_project`'s key order so the studio preserves it.

## Deploy

`.github/workflows/pages.yml` on push to `main` or manual dispatch: checkout, `configure-pages@v5` with `enablement: true` (turns Pages on the first time), Python 3.12, `pip install -r requirements.txt`, `python build.py` (no drafts), `upload-pages-artifact@v3` from `site/`, `deploy-pages@v4`. Concurrency group `pages`. The repo must be public for Pages on a free GitHub plan.

Domain records (also in the README): `A` records for `@` to 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; `CNAME` for `www` to `alighieri2000.github.io`. Then Pages settings: custom domain `dantexcameron.com`, Enforce HTTPS.

## Local checks that worked

- Build: `python build.py --drafts` from the repo root, then look at `http://localhost:8000/` (either `preview.bat` or `python -m http.server 8000 --directory site`).
- Phone layout: a browser's device emulation at 375 px wide. Headless Chrome screenshots ignore the viewport meta tag below its minimum window width, so use real device emulation for phone checks.
- Blank tiles in a screenshot taken right after load are lazy-loading, not a bug.
- A fresh Python with neither package: running `build.py` printed the install line, installed both and built (tested 2026-11-04 in a bare venv).

## Known quirks

- Two projects with the same `order` sort by title (Bloodhound and Cashout Station both have 3 as of 2026-11-04).
- `find()` matches the cover by stem, so `cover: 07.webp` and `cover: 07` are the same.
- The `_img` cache is keyed on file modification time; replacing an image with an older file keeps the stale variant. Delete the project's `_img` folder under `site/` if that happens.
- `webflow-archive/` is reference material only; the converter that turned it into `content/techart/` lived only in a chat session and no longer exists. Edit the tech-art `project.md` files directly.
