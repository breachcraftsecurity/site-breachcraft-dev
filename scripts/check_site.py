"""Checks a lab front-door static site against its design spec and the CSP.

Run from the repository root:  python scripts/check_site.py
Exits non-zero on any failure. No third-party packages.

Per-site values live in site.json: cname, wordBudget, maxBytes, mustInclude,
allowButton, specId.

Limits, stated so a pass is not over-read:
- Tag balance only; full HTML validity is the CI tidy step.
- Contrast is checked on the palette tokens, not on every rendered element.
- CSP is checked for what pages load against the policy in
  staticwebapp.config.json, not by a browser.
"""
import json
import pathlib, re, sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
EXCLUDE = set(SITE.get("exclude", []))
SITE_FILES = [p for p in ROOT.rglob("*") if p.is_file()
              and not {".git", ".github", "scripts"} & set(p.relative_to(ROOT).parts)
              and not EXCLUDE & set(p.relative_to(ROOT).parts)
              and p.name not in {"README.md", "site.json"}]
PAGES = [p for p in SITE_FILES if p.suffix == ".html"]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BANNED = ["leverage", "synergy", "cutting-edge", "world-class", "best-in-class", "passionate"]
MAX_BYTES = SITE["maxBytes"]
WORD_BUDGET = SITE["wordBudget"]
failures = []

CSP = {}
_policy = re.search(r'"Content-Security-Policy":\s*"([^"]+)"',
                    (ROOT / "staticwebapp.config.json").read_text(encoding="utf-8"))
for _part in (_policy.group(1) if _policy else "").split(";"):
    _bits = _part.split()
    if _bits:
        CSP[_bits[0]] = _bits[1:]


def fail(msg):
    failures.append(msg)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.hrefs, self.srcs, self.ids, self.text = [], [], [], set(), []
        self.loads = []
        self.in_main = 0
        self.has_inline_style = self.has_script = False
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if a.get("style"):
            self.has_inline_style = True
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "main":
            self.in_main += 1
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        if tag == "link" and a.get("href"):
            self.srcs.append(a["href"])
            rel = (a.get("rel") or "").lower()
            if rel in ("stylesheet", "icon", "shortcut icon", "apple-touch-icon"):
                self.loads.append(("style-src" if rel == "stylesheet" else "img-src", a["href"]))
        if tag == "img" and a.get("src"):
            self.srcs.append(a["src"])
            self.loads.append(("img-src", a["src"]))
        if tag == "script":
            self.has_script = True
        if tag in VOID:
            return
        self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass

    def handle_data(self, data):
        if self.in_main:
            self.text.append(data)


def resolve(page, href):
    path = href.split("#")[0].split("?")[0]
    if not path:
        return page
    target = (ROOT / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    if target.is_dir():
        target = target / "index.html"
    return target if target.is_file() else None


def target_of(page, href):
    return resolve(page, href) or page


def csp_allows(directive, url):
    sources = CSP.get(directive, CSP.get("default-src", []))
    if url.startswith(("http://", "https://", "//")):
        host = re.sub(r"^(https?:)?//", "", url).split("/")[0]
        return any(host == src or src.endswith("//" + host) for src in sources)
    if url.startswith("data:"):
        return "data:" in sources
    return "'self'" in sources


def dependencies(page, loads):
    seen, queue = set(), [target_of(page, u) for _, u in loads if not u.startswith(("http", "//", "data:"))]
    while queue:
        f = queue.pop()
        if f in seen or not f.is_file():
            continue
        seen.add(f)
        if f.suffix == ".css":
            for ref in re.findall(r"url\(['\"]?([^'\")]+)", f.read_text(encoding="utf-8")):
                if not ref.startswith(("http", "//", "data:")):
                    queue.append(target_of(f, ref))
    return seen


def luminance(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


css = (ROOT / "styles.css").read_text(encoding="utf-8")
tokens = dict(re.findall(r"--(bg|ink|muted|accent|line):\s*(#[0-9a-fA-F]{6})", css))
for key in ("ink", "muted", "accent", "line"):
    if key not in tokens:
        fail(f"styles.css: missing --{key} token")
for fg in ("ink", "muted", "accent"):
    if fg in tokens and "bg" in tokens:
        ratio = contrast(tokens[fg], tokens["bg"])
        if ratio < 4.5:
            fail(f"contrast {fg} on bg {ratio:.2f} < 4.5 (AA body text)")

PAGE_IDS, PARSED = {}, []
for page, rel, p in [(pg, pg.relative_to(ROOT).as_posix(), Page()) for pg in PAGES]:
    src = page.read_text(encoding="utf-8")
    p.feed(src); p.close()
    if p.stack:
        fail(f"{rel}: unclosed {p.stack}")
    if p.lang != "en-GB":
        fail(f"{rel}: lang is {p.lang!r}, spec requires en-GB")
    if p.has_script:
        fail(f"{rel}: script present (noJs, CSP script-src 'none')")
    if p.has_inline_style:
        fail(f"{rel}: inline style present (CSP style-src 'self')")
    PAGE_IDS[page] = p.ids
    PARSED.append((page, rel, p))
    for directive, url in p.loads:
        if not csp_allows(directive, url):
            fail(f"{rel}: {url} blocked by CSP {directive}")
    for href in p.hrefs + p.srcs:
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        if href.startswith("#"):
            if href[1:] and href[1:] not in p.ids:
                fail(f"{rel}: fragment {href} has no target")
            continue
        if not resolve(page, href):
            fail(f"{rel}: broken internal link {href}")
    text = " ".join(" ".join(p.text).split())
    for w in BANNED:
        if re.search(rf"\b{re.escape(w)}\b", text, re.I):
            fail(f"{rel}: banned word {w!r}")
    weight = len(src.encode("utf-8")) + sum(f.stat().st_size for f in dependencies(page, p.loads))
    if weight > MAX_BYTES:
        fail(f"{rel}: {weight} bytes > {MAX_BYTES}")
    if rel == "index.html":
        words = len(re.findall(r"[A-Za-z0-9][\w'’.-]*", text))
        if words > WORD_BUDGET:
            fail(f"index.html: {words} words > budget {WORD_BUDGET}")
        for phrase in SITE.get("mustInclude", []):
            if not re.search(re.escape(phrase), text, re.I):
                fail(f"index.html: mustInclude {phrase!r} missing")
        if not SITE.get("allowButton", True) and "<button" in src.lower():
            fail("index.html: design says no button")
        print(f"index.html: {words} words, {weight} bytes with CSS and assets")

for page, rel, p in PARSED:
    for href in p.hrefs:
        if "#" in href and not href.startswith(("#", "http://", "https://", "mailto:")):
            frag = href.split("#", 1)[1]
            t = target_of(page, href)
            if frag and t in PAGE_IDS and frag not in PAGE_IDS[t]:
                fail(f"{rel}: {href} has no target on that page")

cname = (ROOT / "CNAME").read_text(encoding="utf-8").strip() if (ROOT / "CNAME").is_file() else ""
if cname != SITE["cname"]:
    fail(f"CNAME is {cname!r}, not {SITE['cname']!r}")

print(f"checked {len(PAGES)} pages, {len(SITE_FILES)} site files; "
      f"contrast ink {contrast(tokens['ink'], tokens['bg']):.1f}, "
      f"muted {contrast(tokens['muted'], tokens['bg']):.1f}, "
      f"accent {contrast(tokens['accent'], tokens['bg']):.1f}")
print("\n".join(failures) if failures else "all checks passed")
sys.exit(1 if failures else 0)
