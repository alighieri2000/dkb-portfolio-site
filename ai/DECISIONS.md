# Decisions and rejected alternatives

Why the site is the way it is. Check here before proposing a change of platform, layout or scope.

## Platform

- **Webflow (the old site)**: rejected for cost. Dante: "I made a webflow site in the past but it was SO expensive", and the domain billed through Webflow was "absurdly expensive". The old site stays reachable at `dante-cameron.webflow.io` and is archived in `webflow-archive/`.
- **ArtStation**: kept for studio and tech-art work, rejected for the fabrication site. Reasons found while writing Body of Mine captions: captions have a character limit, and there is no way to put a normal text block between media on a project page, which is why Dante used to bake text into images. A portfolio reviewer also wanted the fabrication work on its own, cover-first site.
- **Behance**: Dante raised it; not pursued once a self-hosted site turned out to be free.
- **GitHub Pages with a custom domain**: chosen. Free, Dante keeps the files, the domain is already owned, and a build on push means Dante can edit on github.com in a pinch. Cost of the whole thing is the domain renewal at GoDaddy (about 20 dollars a year; Cloudflare Registrar would roughly halve that, no hurry).
- **Static Python build rather than a site generator**: one short script Dante can read, no Node toolchain, no theme to fight. Pillow makes the WebP variants so Dante can drop in full-size originals.
- **A local editor (the studio) rather than a CMS**: Dante asked for "a tool so I can make edits". A standard-library HTTP server that edits the same files keeps the hand-editing path intact.

## Domain

- `dantexcameron.com`: registered at GoDaddy (Wild West Domains) until 2027-07-29, DNS at domaincontrol.com, previously `www` pointed at `proxy-ssl.webflow.com`. The GoDaddy account is held by someone else, so DNS changes go through them.
- `dantecameron.com` (no x): owned by someone else, registered through Namecheap on 2026-09-25. Not available.
- `content/CNAME` is `dantexcameron.com`; `www` is a CNAME to `alighieri2000.github.io`.

## Design

- **Cover-first home page**: the reviewer's brief was "a page with JUST cover pages: huge and encompassing most of the screen as you scroll down", each opening the project. The first version used true full-screen covers; it became a two-column grid of 2:1 and 1:1 tiles when Dante asked for the full and half rhythm.
- **Titles overlaid on covers, not on a plate below**: Dante rejected the plate version on 2026-11-04.
- **Tight gutters**: Dante rejected wide white margins the same day. Earlier Dante had asked for "some nice white margins", then saw them and reversed; the current clamp values are the compromise.
- **Header above the gallery**: Dante asked for one; it carries the intro text that used to need a separate page.
- **Project page = gallery left, sticky text right**: modeled on ArtStation, which Dante called "pretty strong". Long description lives in `summary:`; body text is for short notes between images.
- **Hover clips**: required from the start. Clips load only on hover so the page stays light; MP4 recommended over GIF.
- **Light theme with a dichroic-style gradient accent**: replaced the first, dark version during the polish round.
- **Email as copyable text, not a mailto link**: survives bots and link blockers.

## Scope

- **Fabrication only on this site.** Tech-art pages were rebuilt from the Webflow archive ("Yes, rebuild them") and briefly live as a second section at `/tech-art/`; Dante then parked them: "lets just ignore tech art for now... It probably is better on its own separate site anyway." The content stays in `content/techart/` and the section mechanism stays in `build.py` so it can come back or move to another repo.
- **Voice**: the old pages were third person; rewritten in first person with Dante's approval.
- **Drafts stay in the repo**: projects without photos are committed as `draft: true` with their write-ups so the text is ready when the photos arrive.
- **Placeholders are visible to Dante, invisible to visitors**: HTML comments at the top of a `project.md`.

## Things not to re-propose

- Moving back to Webflow, Squarespace or another paid builder.
- Putting the tech-art section back on this site without Dante asking.
- A plate or caption block under the covers; wide margins.
- Third-person copy.
- A separate dark theme.
