"""Checks the static site against design-specs/specs/lab-door-redteamtips.json and the CSP.

Run from the repository root:  python scripts/check_site.py
Exits non-zero on any failure. No third-party packages.

Limits, stated so a pass is not over-read:
- Tag balance only; full HTML validity is the CI tidy step.
- Contrast is checked on the palette tokens, not on every rendered element.
- CSP is checked for what pages load (stylesheets, images, icons, scripts) against
  the policy in staticwebapp.config.json, not by a browser.
"""
import json
import pathlib, re, sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE_FILES = [p for p in ROOT.rglob("*") if p.is_file()
              and not {".git", ".github", "scripts"} & set(p.relative_to(ROOT).parts)
              and p.name not in {"README.md"}]
PAGES = [p for p in SITE_FILES if p.suffix == ".html"]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BANNED = ["leverage", "synergy", "cutting-edge", "world-class", "best-in-class", "passionate"]
MAX_BYTES = 80_000        # spec technical.maxBytes, per page including its CSS and assets
WORD_BUDGET = 245         # spec constraints.wordBudget, index main content
failures = []

def fail(msg):
    failures.append(msg)

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.hrefs, self.srcs, self.ids, self.text = [], [], [], set(), []
        self.loads = []   # (directive, url) for resources the browser fetches
        self.in_main = 0
        self.has_inline_style = self.has_script = False
        self.lang = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = a.get("lang")
        if tag == "script": self.has_script = True
        if tag == "style" or "style" in a: self.has_inline_style = True
        if any(k.startswith("on") for k in a): self.has_script = True
        if "id" in a: self.ids.add(a["id"])
        if "href" in a: self.hrefs.append(a["href"])
        if "src" in a: self.srcs.append(a["src"])
        if tag == "link" and "href" in a:
            rel = a.get("rel", "").lower()
            if "stylesheet" in rel: self.loads.append(("style-src", a["href"]))
            elif "icon" in rel: self.loads.append(("img-src", a["href"]))
        if tag == "img" and "src" in a: self.loads.append(("img-src", a["src"]))
        if tag == "script" and "src" in a: self.loads.append(("script-src", a["src"]))
        if tag == "img" and "alt" not in a: fail(f"{self.name}: <img> without alt")
        if tag == "main": self.in_main += 1
        if tag not in VOID: self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack or self.stack[-1][0] != tag:
            fail(f"{self.name}: unbalanced </{tag}> at line {self.getpos()[0]}; open: {[t for t, _ in self.stack[-3:]]}")
            return
        self.stack.pop()
        if tag == "main": self.in_main -= 1
    def handle_data(self, data):
        if self.in_main: self.text.append(data)

def resolve(page, href):
    path = href.split("#")[0].split("?")[0]
    if not path: return True
    target = (ROOT / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    return target.is_file() or (target / "index.html").is_file()

def target_of(page, url):
    path = url.split("#")[0].split("?")[0]
    t = (ROOT / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    return t / "index.html" if t.is_dir() else t

CONFIG = json.loads((ROOT / "staticwebapp.config.json").read_text(encoding="utf-8"))
CSP = {}
for part in CONFIG["globalHeaders"]["Content-Security-Policy"].split(";"):
    bits = part.split()
    if bits: CSP[bits[0]] = bits[1:]

def csp_allows(directive, url):
    sources = CSP.get(directive, CSP.get("default-src", []))
    if url.startswith(("http://", "https://", "//")):
        host = re.sub(r"^(https?:)?//", "", url).split("/")[0]
        return any(host == src or src.endswith("//" + host) for src in sources)
    if url.startswith("data:"): return "data:" in sources
    return "'self'" in sources

def dependencies(page, loads):
    """Same-origin files a page pulls in: stylesheets, images, icons and url() refs inside CSS."""
    seen, queue = set(), [target_of(page, u) for _, u in loads if not u.startswith(("http", "//", "data:"))]
    while queue:
        f = queue.pop()
        if f in seen or not f.is_file(): continue
        seen.add(f)
        if f.suffix == ".css":
            for ref in re.findall(r"url\(['\"]?([^'\")]+)", f.read_text(encoding="utf-8")):
                if not ref.startswith(("http", "//", "data:")): queue.append(target_of(f, ref))
    return seen

def luminance(hex_):
    r, g, b = (int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

css = (ROOT / "styles.css").read_text(encoding="utf-8")
tokens = dict(re.findall(r"--(bg|ink|muted|accent|line):\s*(#[0-9a-fA-F]{6})", css))
for fg in ("ink", "muted", "accent"):
    ratio = contrast(tokens[fg], tokens["bg"])
    if ratio < 4.5: fail(f"contrast {fg} on bg {ratio:.2f} < 4.5 (AA body text)")
# In-prose link underline must reach 3:1 against the background (non-colour link indicator).
if contrast(tokens["muted"], tokens["bg"]) < 3: fail("prose link underline below 3:1")

PAGE_IDS, PARSED = {}, []
for page in PAGES:
    rel = page.relative_to(ROOT).as_posix()
    p = Page(); p.name = rel
    src = page.read_text(encoding="utf-8")
    p.feed(src); p.close()
    if p.stack: fail(f"{rel}: unclosed {[t for t, _ in p.stack]}")
    if p.lang != "en-GB": fail(f"{rel}: lang is {p.lang!r}, spec requires en-GB")
    if p.has_script: fail(f"{rel}: script or inline handler present (spec noJs, CSP script-src 'none')")
    if p.has_inline_style: fail(f"{rel}: inline style present (CSP style-src 'self')")
    PAGE_IDS[page] = p.ids
    PARSED.append((page, rel, p))
    for directive, url in p.loads:
        if not csp_allows(directive, url): fail(f"{rel}: {url} is blocked by CSP {directive}")
    for href in p.hrefs + p.srcs:
        if href.startswith(("http://", "https://", "mailto:")): continue
        if href.startswith("#"):
            if href[1:] and href[1:] not in p.ids: fail(f"{rel}: fragment {href} has no target")
            continue
        if not resolve(page, href): fail(f"{rel}: broken internal link {href}")
    text = " ".join(" ".join(p.text).split())
    for w in BANNED:
        if re.search(rf"\b{re.escape(w)}\b", text, re.I): fail(f"{rel}: banned word {w!r}")
    weight = len(src.encode("utf-8")) + sum(f.stat().st_size for f in dependencies(page, p.loads))
    if weight > MAX_BYTES: fail(f"{rel}: {weight} bytes > {MAX_BYTES}")
    if rel == "index.html":
        words = len(re.findall(r"[A-Za-z0-9][\w'’.-]*", text))
        if words > WORD_BUDGET: fail(f"index.html: {words} words > budget {WORD_BUDGET}")
        if not re.search(r"ten years.*QinetiQ.*NCC Group", text, re.I): fail("index.html: mustInclude ten years QinetiQ to NCC Group missing")
        if "button" in src.lower(): fail("index.html: design says no button")
        print(f"index.html: {words} words, {weight} bytes with CSS and assets")

for page, rel, p in PARSED:
    for href in p.hrefs:
        if "#" in href and not href.startswith(("#", "http://", "https://", "mailto:")):
            frag = href.split("#", 1)[1]
            t = target_of(page, href)
            if frag and t in PAGE_IDS and frag not in PAGE_IDS[t]: fail(f"{rel}: {href} has no target on that page")

if not (ROOT / "CNAME").read_text().strip() == "redteamtips.com": fail("CNAME is not redteamtips.com")

print(f"checked {len(PAGES)} pages, {len(SITE_FILES)} site files; contrast ink {contrast(tokens['ink'], tokens['bg']):.1f}, muted {contrast(tokens['muted'], tokens['bg']):.1f}, accent {contrast(tokens['accent'], tokens['bg']):.1f}")
print("\n".join(failures) if failures else "all checks passed")
sys.exit(1 if failures else 0)
