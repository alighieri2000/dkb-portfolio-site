"""
studio.py: a local editor for the site. Double-click studio.bat (or run `python studio.py`) and a
page opens at http://localhost:8001/ where you can add projects to either section, upload covers,
hover clips and images, edit the text, rebuild the site, preview it, and publish with one button.

Everything it does is ordinary file edits inside content/, a run of build.py, and git. It listens
on this computer only.
"""
import html, json, mimetypes, re, subprocess, sys, urllib.parse, webbrowser
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT, SITE = ROOT / "content", ROOT / "site"
PORT = 8001
IMG = {".jpg", ".jpeg", ".png", ".webp"}
MOTION = {".mp4", ".webm", ".gif"}
FIELDS = [("title", "Title"), ("subtitle", "Subtitle (one line under the title)"), ("year", "Year"),
          ("client", "Client"), ("developer", "Developer / team"), ("role", "Role"), ("platform", "Platform"),
          ("materials", "Materials"), ("tools", "Tools"), ("timeline", "Timeline"), ("context", "Context"),
          ("awards", "Awards"), ("links", "Links  (Label | https://url ; Label | https://url)")]
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,60}$")


def sections():
    site = json.loads((CONTENT / "site.json").read_text(encoding="utf-8"))
    secs = site.get("sections") or [{"dir": "projects", "path": "", "title": "Work"}]
    return {s["dir"]: s for s in secs}


CSS = """
body{margin:0;background:#f3f4f6;color:#16181b;font:15px/1.5 "Instrument Sans","Segoe UI",Arial,sans-serif}
a{color:inherit} .wrap{max-width:1100px;margin:0 auto;padding:24px 20px 60px}
h1,h2{font-family:"Bricolage Grotesque",Arial,sans-serif;letter-spacing:-.01em;margin:0 0 12px} h1{font-size:28px} h2{font-size:18px;margin-top:28px}
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:22px}
.btn{display:inline-block;padding:8px 14px;border:1px solid #c9ced5;border-radius:6px;background:#fff;font:inherit;cursor:pointer;text-decoration:none;color:inherit}
.btn.primary{background:#16181b;color:#fff;border-color:#16181b}
.btn.danger{color:#b23a3a}
table{border-collapse:collapse;width:100%;background:#fff;border:1px solid #dcdfe4;border-radius:8px;overflow:hidden;margin-bottom:8px}
td,th{padding:10px 12px;border-bottom:1px solid #eceef1;text-align:left;vertical-align:middle} th{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#6b727b}
.thumb{width:72px;height:48px;object-fit:cover;border-radius:4px;background:#e8eaee}
label{display:block;font-size:13px;color:#6b727b;margin:14px 0 4px}
input[type=text],input[type=number],select,textarea{width:100%;padding:8px 10px;border:1px solid #c9ced5;border-radius:6px;font:inherit;background:#fff}
textarea{min-height:360px;font-family:"JetBrains Mono",Consolas,monospace;font-size:13.5px;line-height:1.5}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:0 24px} .grid .full{grid-column:1/-1}
.files{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin-top:8px}
.file{background:#fff;border:1px solid #dcdfe4;border-radius:8px;padding:8px;font-size:12px}
.file img,.file video{width:100%;height:96px;object-fit:cover;border-radius:4px;background:#e8eaee;display:block;margin-bottom:6px}
.file .name{font-family:"JetBrains Mono",Consolas,monospace;word-break:break-all}
.file .acts{display:flex;gap:6px;margin-top:6px} .file .acts button{font-size:12px;padding:4px 8px}
.note{background:#fff7d6;border:1px solid #f0dc8a;padding:10px 12px;border-radius:6px;margin:12px 0}
pre{background:#16181b;color:#e7ecef;padding:12px;border-radius:6px;overflow:auto;font-size:12.5px}
.ok{color:#2e8b57} .muted{color:#6b727b}
@media (max-width:760px){.grid{grid-template-columns:1fr}}
"""


# ----------------------------------------------------------------- project files
def read_project(folder):
    p = folder / "project.md"
    if not p.exists():
        return {}, ""
    text = p.read_text(encoding="utf-8")
    meta, body = {}, text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta, body.strip()


def write_project(folder, meta, body):
    order = ["title", "subtitle", "year", "client", "developer", "role", "platform", "materials", "tools", "timeline",
             "context", "awards", "summary", "links", "cover", "hero", "hover", "size", "order", "draft"]
    keys = [k for k in order if meta.get(k)] + [k for k in meta if k not in order and meta.get(k)]
    fm = "\n".join(f"{k}: {meta[k]}" for k in keys)
    (folder / "project.md").write_text(f"---\n{fm}\n---\n\n{body.strip()}\n", encoding="utf-8")


def files_of(folder):
    return sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMG | MOTION)


def projects(sec_dir):
    out = []
    src = CONTENT / sec_dir
    if not src.exists():
        return out
    for f in sorted(p for p in src.iterdir() if p.is_dir()):
        meta, _ = read_project(f)
        if meta:
            out.append((f, meta))
    out.sort(key=lambda x: (int(x[1].get("order", 999) or 999), x[1].get("title", "").lower()))
    return out


def cover_of(folder, meta):
    want = meta.get("cover", "cover").rsplit(".", 1)[0]
    for p in files_of(folder):
        if p.stem == want and p.suffix.lower() in IMG:
            return p.name
    return None


def is_draft(meta):
    return meta.get("draft", "").lower() in ("true", "yes", "1")


# ----------------------------------------------------------------- pages
def page(title, body):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · Studio</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700&family=Instrument+Sans:wght@400;500&family=JetBrains+Mono&display=swap">
<style>{CSS}</style></head><body><div class="wrap">{body}</div></body></html>"""


def index_page(msg=""):
    secs = sections()
    tables = []
    for d, sec in secs.items():
        rows = []
        for folder, meta in projects(d):
            cov = cover_of(folder, meta)
            thumb = f'<img class="thumb" src="/files/{d}/{folder.name}/{cov}" alt="">' if cov else '<div class="thumb"></div>'
            state = '<span class="muted">draft</span>' if is_draft(meta) else '<span class="ok">live</span>'
            rows.append(f'<tr><td>{thumb}</td><td><a href="/edit/{d}/{folder.name}"><strong>{html.escape(meta.get("title", folder.name))}</strong></a>'
                        f'<br><span class="muted">{html.escape(meta.get("subtitle", ""))}</span></td><td>{html.escape(meta.get("order", ""))}</td>'
                        f'<td>{state}</td><td>{"cover" if cov else "<strong>no cover</strong>"}</td></tr>')
        pv = "/preview/" + (sec["path"] + "/" if sec["path"] else "")
        tables.append(f'<h2>{html.escape(sec["title"])} <a class="btn" href="{pv}" target="_blank" style="font-size:13px;margin-left:8px">Preview this gallery</a></h2>'
                      f'<table><tr><th></th><th>Project</th><th>Order</th><th>Status</th><th>Cover</th></tr>{"".join(rows) or "<tr><td colspan=5 class=muted>No projects yet.</td></tr>"}</table>')
    sec_opts = "".join(f'<option value="{d}">{html.escape(s["title"])}</option>' for d, s in secs.items())
    body = f"""<h1>Site studio</h1>
<div class="bar"><form method="post" action="/build"><button class="btn">Build and preview</button></form>
<a class="btn" href="/preview/" target="_blank">Open preview</a>
<form method="post" action="/publish" onsubmit="return confirm('Commit everything and push to GitHub?')">
<input type="hidden" name="msg" value="Update site"><button class="btn primary">Publish to GitHub</button></form></div>
{f'<div class="note">{msg}</div>' if msg else ''}
{''.join(tables)}
<h2>New project</h2>
<form method="post" action="/new" class="grid">
<div><label>Section</label><select name="section">{sec_opts}</select></div>
<div><label>Title</label><input type="text" name="title" required></div>
<div><label>Folder name (lowercase, hyphens; becomes the web address)</label><input type="text" name="slug" pattern="[a-z0-9][a-z0-9-]*" required placeholder="emma-frost"></div>
<div class="full" style="margin-top:12px"><button class="btn primary">Create as draft</button></div></form>
<p class="muted" style="margin-top:28px">Lowest order number shows first in its gallery. A project stays a draft (hidden from the published site, visible in preview) until you untick Draft.</p>"""
    return page("Projects", body)


def edit_page(d, slug, msg=""):
    sec = sections()[d]
    folder = CONTENT / d / slug
    meta, body = read_project(folder)
    files = files_of(folder)
    imgs = [p for p in files if p.suffix.lower() in IMG]
    clips = [p for p in files if p.suffix.lower() in MOTION]
    cov = cover_of(folder, meta)
    hov = meta.get("hover", "hover").rsplit(".", 1)[0]
    cur_hover = next((p.name for p in clips if p.stem == hov), "")

    def opts(items, current, none_label):
        o = [f'<option value="">{none_label}</option>']
        o += [f'<option value="{p.name}"{" selected" if p.name == current else ""}>{p.name}</option>' for p in items]
        return "".join(o)

    fields = "".join(
        f'<div><label>{label}</label><input type="text" name="{k}" value="{html.escape(meta.get(k, ""))}"></div>' for k, label in FIELDS)
    tiles = []
    for p in files:
        if p.suffix.lower() in IMG:
            media = f'<img src="/files/{d}/{slug}/{p.name}" alt="">'
            insert = f'<button type="button" onclick="ins(\'{p.name}\')">Insert</button>'
        else:
            media = (f'<video src="/files/{d}/{slug}/{p.name}" muted loop playsinline onmouseover="this.play()" onmouseout="this.pause()"></video>'
                     if p.suffix.lower() != ".gif" else f'<img src="/files/{d}/{slug}/{p.name}" alt="">')
            insert = ""
        tiles.append(f'<div class="file">{media}<div class="name">{p.name}</div><div class="acts">{insert}'
                     f'<button type="button" class="btn danger" onclick="del(\'{p.name}\')">Delete</button></div></div>')
    pv = "/preview/" + (sec["path"] + "/" if sec["path"] else "") + slug + "/"
    body_html = f"""<div class="bar"><a class="btn" href="/">All projects</a><a class="btn" href="{pv}" target="_blank">Preview this page</a>
<span class="muted">{html.escape(sec["title"])} · {html.escape(d)}/{html.escape(slug)}</span></div>
<h1>{html.escape(meta.get("title", slug))}</h1>
{f'<div class="note">{msg}</div>' if msg else ''}
{'' if cov else '<div class="note">No cover yet. Upload an image below and choose it as the cover.</div>'}
<form method="post" action="/save/{d}/{slug}" id="f">
<div class="grid">{fields}
<div><label>Cover image (fills the gallery frame)</label><select name="cover">{opts(imgs, cov or "", "choose an image")}</select></div>
<div><label>Hover clip (plays over the cover on hover)</label><select name="hover">{opts(clips, cur_hover, "none")}</select></div>
<div><label>Size in the gallery</label><select name="size"><option value="full"{"" if meta.get("size", "").lower() in ("half", "square", "small") else " selected"}>Full width rectangle</option><option value="half"{" selected" if meta.get("size", "").lower() in ("half", "square", "small") else ""}>Half width square (two sit side by side)</option></select></div>
<div><label>Order in the gallery (1 = first)</label><input type="number" name="order" value="{html.escape(meta.get("order", ""))}"></div>
<div><label>Draft</label><label style="font-size:15px;color:inherit"><input type="checkbox" name="draft" {"checked" if is_draft(meta) else ""}> Hide from the published site</label></div>
<div class="full"><label>Summary (the paragraph in the side panel)</label><input type="text" name="summary" value="{html.escape(meta.get("summary", ""))}"></div>
<div class="full"><label>Write-up. Images go where you put ![caption](file.jpg); two on one line sit side by side; ## makes a heading; a line with @youtube VIDEOID embeds a video.</label>
<textarea name="body" id="body">{html.escape(body)}</textarea></div>
<div class="full" style="margin-top:14px"><button class="btn primary">Save</button> <span class="muted">Saving writes project.md. Build to see it.</span></div>
</div></form>
<h2>Files in this project</h2>
<form method="post" action="/upload/{d}/{slug}" enctype="multipart/form-data" class="bar">
<input type="file" name="files" multiple accept=".jpg,.jpeg,.png,.webp,.gif,.mp4,.webm"><button class="btn">Upload</button>
<span class="muted">Covers: 2400 px wide or more. Clips: short, silent, under ~4 MB; MP4 beats GIF.</span></form>
<div class="files">{''.join(tiles) or '<p class="muted">Nothing uploaded yet.</p>'}</div>
<form method="post" action="/delete/{d}/{slug}" id="delf"><input type="hidden" name="name" id="delname"></form>
<script>
function ins(n){{var t=document.getElementById('body');var s=t.selectionStart;t.value=t.value.slice(0,s)+'\\n![]('+n+')\\n'+t.value.slice(s);t.focus();}}
function del(n){{if(confirm('Delete '+n+' from this project folder?')){{document.getElementById('delname').value=n;document.getElementById('delf').submit();}}}}
</script>"""
    return page(meta.get("title", slug), body_html)


# ----------------------------------------------------------------- server
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def send_html(self, text, code=200):
        data = text.encode("utf-8")
        self.send_response(code); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def redirect(self, to):
        self.send_response(303); self.send_header("Location", to); self.end_headers()

    def send_file(self, path):
        if not path.is_file():
            return self.send_html(page("Not found", "<h1>Not found</h1>"), 404)
        ctype = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        data = path.read_bytes()
        self.send_response(200); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def target(self, d, slug):
        """The project folder for a section dir + slug, or None if either is not valid."""
        if d in sections() and SLUG.match(slug) and (CONTENT / d / slug).is_dir():
            return CONTENT / d / slug
        return None

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        msg = html.escape(q.get("msg", [""])[0])
        parts = [p for p in u.path.split("/") if p]
        if not parts:
            return self.send_html(index_page(msg))
        if parts[0] == "edit" and len(parts) == 3 and self.target(parts[1], parts[2]):
            return self.send_html(edit_page(parts[1], parts[2], msg))
        if parts[0] == "files" and len(parts) == 4 and self.target(parts[1], parts[2]):
            return self.send_file(CONTENT / parts[1] / parts[2] / Path(parts[3]).name)
        if parts[0] == "preview":
            rel = Path(*parts[1:]) if len(parts) > 1 else Path(".")
            t = (SITE / rel).resolve()
            if SITE.resolve() not in t.parents and t != SITE.resolve():
                return self.send_html("forbidden", 403)
            if t.is_dir():
                t = t / "index.html"
            if not t.exists() and not SITE.exists():
                return self.send_html(page("No build yet", '<h1>No build yet</h1><p><a href="/">Back</a> and press Build.</p>'), 404)
            return self.send_file(t)
        self.send_html(page("Not found", '<h1>Not found</h1><p><a href="/">Back to projects</a></p>'), 404)

    def form(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        ctype = self.headers.get("Content-Type", "")
        if ctype.startswith("multipart/form-data"):
            msg = BytesParser(policy=policy.default).parsebytes(b"Content-Type: " + ctype.encode() + b"\r\nMIME-Version: 1.0\r\n\r\n" + raw)
            fields, files = {}, []
            for part in msg.iter_parts():
                name = part.get_param("name", header="content-disposition")
                fn = part.get_filename()
                if fn:
                    files.append((fn, part.get_payload(decode=True)))
                elif name:
                    fields[name] = part.get_content().strip() if part.get_content_type() == "text/plain" else part.get_payload(decode=True).decode("utf-8", "ignore")
            return fields, files
        return {k: v[0] for k, v in urllib.parse.parse_qs(raw.decode("utf-8")).items()}, []

    def do_POST(self):
        parts = [p for p in self.path.split("?")[0].split("/") if p]
        fields, files = self.form()
        if parts == ["new"]:
            d, slug, title = fields.get("section", ""), fields.get("slug", "").strip(), fields.get("title", "").strip()
            if d not in sections() or not SLUG.match(slug) or (CONTENT / d / slug).exists():
                return self.redirect("/?msg=" + urllib.parse.quote("That folder name is taken or invalid."))
            (CONTENT / d / slug).mkdir(parents=True)
            nxt = max([int(m.get("order", 0) or 0) for _, m in projects(d)] + [0]) + 1
            write_project(CONTENT / d / slug, {"title": title or slug, "order": str(nxt), "draft": "true"}, "")
            return self.redirect(f"/edit/{d}/{slug}?msg=" + urllib.parse.quote("Created. Upload a cover and write the page."))
        if parts == ["build"]:
            r = subprocess.run([sys.executable, str(ROOT / "build.py"), "--drafts"], capture_output=True, text=True, cwd=ROOT)
            if r.returncode != 0:
                return self.send_html(page("Build failed", f'<h1>Build failed</h1><pre>{html.escape(r.stdout + r.stderr)}</pre><a class="btn" href="/">Back</a>'))
            return self.redirect("/preview/")
        if parts == ["publish"]:
            out = []
            for cmd in (["git", "add", "-A"], ["git", "commit", "-m", fields.get("msg", "Update site") or "Update site"], ["git", "push"]):
                r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
                out.append(f"$ {' '.join(cmd)}\n{r.stdout}{r.stderr}")
                if r.returncode != 0 and not (cmd[1] == "commit" and "nothing to commit" in r.stdout):
                    break
            return self.send_html(page("Publish", f'<h1>Publish</h1><pre>{html.escape(chr(10).join(out))}</pre><p>GitHub rebuilds the site about a minute after a successful push.</p><a class="btn" href="/">Back</a>'))
        if len(parts) == 3 and self.target(parts[1], parts[2]):
            d, slug = parts[1], parts[2]
            folder = CONTENT / d / slug
            if parts[0] == "save":
                meta, _ = read_project(folder)
                for k, _label in FIELDS:
                    meta[k] = fields.get(k, "").strip()
                meta["summary"] = fields.get("summary", "").strip()
                meta["cover"] = Path(fields.get("cover", "")).name
                meta["hover"] = Path(fields.get("hover", "")).name
                meta["order"] = fields.get("order", "").strip()
                meta["size"] = "half" if fields.get("size") == "half" else ""
                meta["draft"] = "true" if fields.get("draft") else ""
                write_project(folder, meta, fields.get("body", "").replace("\r\n", "\n"))
                return self.redirect(f"/edit/{d}/{slug}?msg=Saved.")
            if parts[0] == "upload":
                saved = 0
                for fn, data in files:
                    name = re.sub(r"[^A-Za-z0-9._-]+", "-", Path(fn).name)
                    if Path(name).suffix.lower() in IMG | MOTION and data:
                        (folder / name).write_bytes(data); saved += 1
                return self.redirect(f"/edit/{d}/{slug}?msg=" + urllib.parse.quote(f"Uploaded {saved} file(s)."))
            if parts[0] == "delete":
                name = Path(fields.get("name", "")).name
                t = folder / name
                if t.is_file() and t.suffix.lower() in IMG | MOTION:
                    t.unlink()
                return self.redirect(f"/edit/{d}/{slug}?msg=" + urllib.parse.quote(f"Deleted {name}."))
        self.send_html(page("Not found", "<h1>Not found</h1>"), 404)


if __name__ == "__main__":
    for d in sections():
        (CONTENT / d).mkdir(parents=True, exist_ok=True)
    print(f"Studio at http://localhost:{PORT}/  (Ctrl+C or close this window to stop)")
    if "--no-open" not in sys.argv:
        webbrowser.open(f"http://localhost:{PORT}/")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
