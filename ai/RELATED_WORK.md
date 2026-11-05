# Related work outside this repository

Dante's job search in late 2026 produced several linked pieces of work. This site is one of them. The others live on Dante's OneDrive computer and are listed here so an assistant knows they exist and does not rebuild them. None of them is in this public repository, and anything personal in them stays out of this folder.

## ArtStation (dantecameron.artstation.com)

The studio and tech-art portfolio: Royal Shakespeare Company Virtual Rehearsal Room, Body of Mine (Meta Quest release, 2024), City of Apparition, and the SCAD projects. The site's nav links to it.

Drafts and image staging for those ArtStation pages are in `C:\Users\dante\OneDrive\Documents\portfolio-image-staging\`: `portfolio-artstation-structure.md` (which projects, what order, what each page says), `portfolio-page-drafts.md` (baked-text and caption drafts for RSC, Body of Mine and City of Apparition), `portfolio-artstation-stalled-showcases.md`, `capture-shotlist.md`, `portfolio-source-pack.md`, `MANIFEST.md`, and folders of images per project. The fabrication projects on this site were first seeded from Dante's existing ArtStation images.

Known ArtStation constraints: caption character limit; no text blocks between media; project description is the only long text field.

## Resume generator

`C:\Users\dante\OneDrive\Documents\resume\build_resumes.py` with `resume.css` builds five versions of Dante's resume from one source (balanced, tech art, 3D design, fabrication, design engineer) as HTML, DOCX and PDF, plus plain ATS PDFs. Rules that came out of its reviews are the same as this site's: no AI tells, no em dashes, light bolding, exact credits, no phone number, awards above education, no GPA. The portfolio URL on the resume is the ArtStation address; once `dantexcameron.com` is live it may make sense to switch it.

## Job search tooling

`C:\Users\dante\OneDrive\Documents\jobsearch\` holds a scanner script and an employer list that feed a job tracker Dante keeps as a Claude artifact. Not related to the site's code.

## Personal knowledge base (DKB)

`github.com/alighieri2000/DKB` is Dante's personal knowledge base for AI assistants: a `database/` of records and sources, a `tools/rebuild_context.py` that generates the `context/*.txt` files an assistant reads, and a `private/` folder whose contents never reach the generated context. Dante's current priorities, including personal and administrative matters, are tracked there, not here. If an assistant has access to that repo, `context/START_HERE.txt` and `context/PRIORITIES.txt` are the entry points.

## Old Webflow site

`dante-cameron.webflow.io` is the previous portfolio. Twelve pages and about seventy assets are archived in this repo under `webflow-archive/` (raw HTML and text plus `manifest.json`). The Wayback Machine was offline the day it was scraped, so the archive was taken live. The eleven project pages were converted into `content/techart/` and then hand-edited; treat the archive as read-only reference.
