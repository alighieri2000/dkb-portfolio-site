"""
build.py: turns content/ into a static website in site/.

    python build.py            # build the published projects
    python build.py --drafts   # also include projects marked draft: true
    python build.py --serve    # build, then open a local preview at http://localhost:8000

content/site.json lists the sections. Each section is a folder of projects (content/projects/,
content/techart/) and gets its own gallery page; the first section is the home page. Each project
is a folder with a project.md (a few "key: value" lines between --- markers, then the write-up in
Markdown) plus its images. See README.md.
"""
import html, json, re, shutil, sys, webbrowser
from pathlib import Path

import markdown
from PIL import Image, ImageOps

ROOT = Path(__file__).parent
CONTENT, SITE, TPL = ROOT / "content", ROOT / "site", ROOT / "templates"
COVER_WIDTHS, BODY_WIDTHS = (2400, 1200), (1800, 900)
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}
MOTION_EXT = {".mp4": "video", ".webm": "video", ".gif": "gif"}


# ----------------------------------------------------------------- content
def read_project(folder):
    text = (folder / "project.md").read_text(encoding="utf-8")
    meta, body = {}, text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line and not line.lstrip().startswith("#"):
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    meta["slug"] = folder.name
    meta["draft"] = meta.get("draft", "").lower() in ("true", "yes", "1")
    meta["order"] = int(meta.get("order", 999) or 999)
    meta.setdefault("title", folder.name.replace("-", " ").title())
    return meta, body.strip()


def find(folder, stem, exts):
    for ext in exts:
        p = folder / f"{stem}{ext}"
        if p.exists():
            return p
    return None


# ----------------------------------------------------------------- images
def variants(src, out_dir, widths):
    """Resized WebP copies of src in out_dir; returns [(width, filename)] largest first and the
    source aspect ratio. Skips work when the copy is newer than the source."""
    out_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        w, h = im.size
        made = []
        for target in sorted(widths, reverse=True):
            width = min(target, w)
            dest = out_dir / f"{src.stem}-{width}.webp"
            if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
                copy = im.convert("RGB") if im.mode not in ("RGB", "RGBA") else im
                if width < w:
                    copy = copy.resize((width, round(h * width / w)), Image.LANCZOS)
                copy.save(dest, "WEBP", quality=84, method=4)
            if not made or made[-1][0] != width:
                made.append((width, dest.name))
    return made, f"{w} / {h}"


def picture(made, ratio, rel, alt="", cls="", eager=False, sizes="100vw"):
    srcset = ", ".join(f"{rel}/{name} {w}w" for w, name in made)
    return (f'<img class="{cls}" src="{rel}/{made[-1][1]}" srcset="{srcset}" sizes="{sizes}" '
            f'alt="{html.escape(alt)}" style="aspect-ratio:{ratio}" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async">')


IMG_TAG = re.compile(r'<img\b[^>]*>')
IMG_PARA = re.compile(r'<p>((?:\s*<img\b[^>]*>\s*)+)</p>')
YT_LINE = re.compile(r"<p>\s*@youtube\s+([A-Za-z0-9_-]{6,})\s*</p>")


def attr(tag, name):
    m = re.search(rf'{name}="([^"]*)"', tag)
    return html.unescape(m.group(1)) if m else ""


def render_body(md_text, folder, out_dir):
    rendered = markdown.markdown(md_text, extensions=["extra", "sane_lists"])
    rendered = YT_LINE.sub(lambda m: f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{m.group(1)}" '
                                     'title="Video" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen></iframe></div>', rendered)

    def figure(match):
        tags = IMG_TAG.findall(match.group(1))
        items = []
        for tag in tags:
            src = attr(tag, "src")
            path = folder / src
            if path.suffix.lower() not in IMG_EXT or not path.exists():
                print(f"  warning: {folder.name}: image not found: {src}")
                continue
            made, ratio = variants(path, out_dir / "_img", BODY_WIDTHS)
            cap = attr(tag, "alt")
            sizes = "100vw" if len(tags) == 1 else f"{100 // len(tags)}vw"
            items.append("<figure>" + picture(made, ratio, "_img", cap, sizes=sizes) +
                         (f"<figcaption>{html.escape(cap)}</figcaption>" if cap else "") + "</figure>")
        if not items:
            return ""
        return items[0] if len(items) == 1 else f'<div class="row" style="--n:{len(items)}">{"".join(items)}</div>'

    return IMG_PARA.sub(figure, rendered)


# ----------------------------------------------------------------- pages
def fill(template, **values):
    out = template
    for _ in range(2):  # nav links carry {{root}} themselves, so substitute twice
        for k, v in values.items():
            out = out.replace("{{" + k + "}}", v)
    return out


def spec_rows(meta):
    rows = []
    for key, label in (("year", "Year"), ("client", "Client"), ("developer", "Developer"), ("role", "Role"),
                       ("platform", "Platform"), ("materials", "Materials"), ("tools", "Tools"),
                       ("timeline", "Timeline"), ("context", "Context"), ("awards", "Awards"), ("status", "Status")):
        if meta.get(key):
            rows.append(f"<div><dt>{label}</dt><dd>{html.escape(meta[key])}</dd></div>")
    return "".join(rows)


def load_section(sec, include_drafts):
    projects = []
    src = CONTENT / sec["dir"]
    if not src.exists():
        return projects
    for folder in sorted(p for p in src.iterdir() if (p / "project.md").exists()):
        meta, body = read_project(folder)
        if meta["draft"] and not include_drafts:
            continue
        cover = find(folder, meta.get("cover", "cover").rsplit(".", 1)[0], IMG_EXT)
        if not cover:
            print(f"  skipping {sec['dir']}/{folder.name}: no cover image")
            continue
        projects.append((meta, body, folder, cover))
    projects.sort(key=lambda p: (p[0]["order"], p[0]["title"].lower()))
    return projects


def build(include_drafts=False):
    site = json.loads((CONTENT / "site.json").read_text(encoding="utf-8"))
    sections = site.get("sections") or [{"dir": "projects", "path": "", "title": "Work"}]
    if SITE.exists():
        for child in SITE.iterdir():  # keep _img caches, replace everything else
            if child.is_dir() and (child / "_img").exists():
                for f in child.iterdir():
                    if f.name != "_img":
                        shutil.rmtree(f) if f.is_dir() else f.unlink()
            elif child.is_dir() and any((g / "_img").exists() for g in child.iterdir() if g.is_dir()):
                for f in child.iterdir():
                    if f.is_dir() and (f / "_img").exists():
                        for g in f.iterdir():
                            if g.name != "_img":
                                shutil.rmtree(g) if g.is_dir() else g.unlink()
                    else:
                        shutil.rmtree(f) if f.is_dir() else f.unlink()
            elif child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    SITE.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "assets", SITE / "assets")
    if (CONTENT / "CNAME").exists():
        shutil.copy(CONTENT / "CNAME", SITE / "CNAME")
    (SITE / ".nojekyll").write_text("")

    def nav_for(current):
        parts = []
        for s in (sections if len(sections) > 1 else []):  # a lone section needs no link to itself
            href = "{{root}}" + (s["path"] + "/" if s["path"] else "./")
            cur = ' aria-current="page"' if s is current else ""
            parts.append(f'<a href="{href}"{cur}>{html.escape(s["title"])}</a>')
        for l in site.get("links", []):
            ext = ' target="_blank" rel="noopener"' if l["href"].startswith("http") else ""
            parts.append(f'<a href="{html.escape(l["href"])}"{ext}>{html.escape(l["label"])}</a>')
        return "".join(parts)

    common = dict(site_name=html.escape(site["name"]), site_description=html.escape(site.get("description", "")),
                  email=html.escape(site.get("email", "")), year=str(site.get("copyright_year", "")))
    project_tpl = (TPL / "project.html").read_text(encoding="utf-8")
    index_tpl = (TPL / "index.html").read_text(encoding="utf-8")
    total = 0

    for sec in sections:
        base = SITE / sec["path"] if sec["path"] else SITE
        base.mkdir(parents=True, exist_ok=True)
        depth = 1 if sec["path"] else 0
        root_index, root_page = "../" * depth, "../" * (depth + 1)
        projects = load_section(sec, include_drafts)
        nav = nav_for(sec)
        covers = []
        for i, (meta, body, folder, cover) in enumerate(projects):
            out = base / meta["slug"]
            out.mkdir(exist_ok=True)
            made, ratio = variants(cover, out / "_img", COVER_WIDTHS)
            motion = find(folder, meta.get("hover", "hover").rsplit(".", 1)[0], MOTION_EXT.keys())
            motion_html = ""
            if motion:
                shutil.copy(motion, out / motion.name)
                if MOTION_EXT[motion.suffix.lower()] == "video":
                    motion_html = f'<video class="motion" muted loop playsinline preload="none" data-src="{meta["slug"]}/{motion.name}"></video>'
                else:
                    motion_html = f'<img class="motion" data-src="{meta["slug"]}/{motion.name}" alt="">'
            sub = html.escape(meta.get("subtitle", ""))
            line = " · ".join(html.escape(meta[k]) for k in ("year", "materials", "platform") if meta.get(k))
            size = "half" if meta.get("size", "").lower() in ("half", "square", "small") else "full"
            covers.append(
                f'<a class="cover {size}{" has-motion" if motion else ""}" href="{meta["slug"]}/" style="--i:{i}"><div class="frame">'
                + picture(made, ratio, meta["slug"] + "/_img", "", "still", eager=(i == 0), sizes="50vw" if size == "half" else "100vw") + motion_html
                + f'<span class="label"><span class="num">{i + 1:02d}</span><span class="t"><strong>{html.escape(meta["title"])}</strong>'
                + (f"<em>{sub}</em>" if sub else "") + f'</span><span class="meta">{line}</span></span></div></a>')

            prev = projects[i - 1][0] if i > 0 else None
            nxt = projects[i + 1][0] if i + 1 < len(projects) else None
            pn = ((f'<a class="prev" href="../{prev["slug"]}/"><span>Previous</span>{html.escape(prev["title"])}</a>' if prev else "<span></span>")
                  + (f'<a class="next" href="../{nxt["slug"]}/"><span>Next</span>{html.escape(nxt["title"])}</a>' if nxt else "<span></span>"))
            summary = markdown.markdown(meta.get("summary", "")) if meta.get("summary") else ""
            links = ""
            if meta.get("links"):
                items = []
                for pair in meta["links"].split(";"):
                    if "|" in pair:
                        label, url = (s.strip() for s in pair.split("|", 1))
                        items.append(f'<li><a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(label)}</a></li>')
                links = f'<ul class="links">{"".join(items)}</ul>' if items else ""
            page = fill(project_tpl, root=root_page, nav=nav, title=html.escape(meta["title"]), subtitle=sub,
                        spec=spec_rows(meta), summary=summary, links=links, body=render_body(body, folder, out),
                        prevnext=pn, section_title=html.escape(sec["title"]), section_href="{{root}}" + (sec["path"] + "/" if sec["path"] else ""),
                        draft_note='<p class="draft-note">Draft: not published yet.</p>' if meta["draft"] else "", **common)
            (out / "index.html").write_text(page, encoding="utf-8")
            print(f"  {sec['dir']}/{meta['slug']}: ok{' (draft)' if meta['draft'] else ''}{' + hover' if motion else ''}")
            total += 1

        (base / "index.html").write_text(
            fill(index_tpl, root=root_index, nav=nav, covers="\n".join(covers),
                 headline=html.escape(sec.get("headline", "")), intro=html.escape(sec.get("intro", "")),
                 where=html.escape(sec.get("where", "")), page_title=("" if not sec["path"] else html.escape(sec["title"]) + " · "), **common),
            encoding="utf-8")

    (SITE / "404.html").write_text(fill((TPL / "404.html").read_text(encoding="utf-8"), root="/", nav=nav_for(None), **common), encoding="utf-8")
    print(f"built {total} project(s) in {len(sections)} section(s) into {SITE}")


if __name__ == "__main__":
    build(include_drafts="--drafts" in sys.argv or "--serve" in sys.argv)
    if "--serve" in sys.argv:
        import functools, http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE))
        webbrowser.open("http://localhost:8000/")
        print("Preview at http://localhost:8000/  (Ctrl+C to stop)")
        http.server.ThreadingHTTPServer(("127.0.0.1", 8000), handler).serve_forever()
