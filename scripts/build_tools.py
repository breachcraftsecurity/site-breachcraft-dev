"""Builds the tool catalogue pages from the captured markdown.

Run from the repository root:  python scripts/build_tools.py
Reads content/tools/<slug>.md (the tool README) and content/tools/<slug>.cheats.md
(the command cheatsheet), writes tools/<slug>/index.html, tools/index.html and
sitemap.xml. Deterministic: same input, same bytes.

The markdown support here is deliberately small - headings, paragraphs, lists,
tables, fenced code, inline code, links, bold and italic - because the input is
known and CI checks the output. No third-party packages.
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "tools"
OUT = ROOT / "tools"
CAPTURED = "22 Nov 2026"
SOURCE_REPO = "AzureFactory/Azure_Offensive_Tooling"

HEAD = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' data:; style-src 'self'; script-src 'self'; base-uri 'self'; form-action 'self'; connect-src 'self'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://breachcraft.dev{path}">
<link rel="icon" href="/assets/mark.svg" type="image/svg+xml">
<link rel="stylesheet" href="/styles.css">
<meta name="theme-color" content="#0b1014">
</head>
<body>
<main>
  <p class="brand">Breachcraft<span>Dev</span></p>
"""

TAIL = """  <p class="licence">Captured from <a href="https://github.com/{repo}">{repo}</a> on {captured}. Upstream content, reproduced as captured; each tool keeps its own licence. Private, all rights reserved.</p>
  <p class="action"><a href="/tools/">All tools</a> &rarr;</p>
  <p class="small">Elsewhere &middot; <a href="https://breachcraftsecurity.com/">Services</a> &middot; <a href="https://breachcraft.academy/">Academy</a> &middot; <a href="https://breachcraft.app/">Labs</a> &middot; <a href="https://breachcraft.org/">Standards</a></p>
  <p class="small">Breachcraft Security &middot; Evilsaint Ltd &middot; <a href="mailto:hello@breachcraftsecurity.com">hello@breachcraftsecurity.com</a></p>
</main>
</body>
</html>
"""

INLINE_CODE = re.compile(r"`([^`]+)`")
BADGE_BLOCK = re.compile(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)", re.S)
IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK = re.compile(r"\[(.+?)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
AUTOLINK = re.compile(r"(?<![\"'=>])\b(https?://[^\s<)\]]+)")
BOLD = re.compile(r"\*\*([^*]+)\*\*|__([^_]+)__")
ITALIC = re.compile(r"(?<![\w*])\*([^*\s][^*]*)\*(?![\w*])")
BANNED = [("leveraging", "using"), ("leverage", "use")]


def escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(text):
    stashed = []

    def keep(fragment):
        stashed.append(fragment)
        return f"\x00{len(stashed) - 1}\x00"

    text = text.replace("\\[", "\x03").replace("\\]", "\x04")
    text = BADGE_BLOCK.sub("", text)
    text = IMAGE.sub("", text)
    text = INLINE_CODE.sub(lambda m: keep(f"<code>{escape(m.group(1))}</code>"), text)
    text = escape(text)
    text = LINK.sub(lambda m: keep(link(m.group(1), m.group(2))), text)
    text = AUTOLINK.sub(lambda m: keep(link(m.group(1), m.group(1))), text)
    text = BOLD.sub(lambda m: f"<strong>{m.group(1) or m.group(2)}</strong>", text)
    text = ITALIC.sub(lambda m: f"<em>{m.group(1)}</em>", text)
    for word, replacement in BANNED:
        text = re.sub(rf"\b{word}\b", replacement, text, flags=re.I)
    text = re.sub(r"\x00(\d+)\x00", lambda m: stashed[int(m.group(1))], text)
    return text.replace("`", "").replace("\x03", "[").replace("\x04", "]")


def link(label, href):
    href = href.replace("&amp;", "&").replace("&lt;", "").replace("&gt;", "")
    href = href.strip("<>")
    if href.startswith(("#", "./", "../")):
        return inline_label(label) or escape(href.lstrip("#"))
    if not href.startswith(("http://", "https://", "mailto:")):
        return inline_label(label) or escape(href)
    shown = inline_label(label) or escape(href)
    return f'<a href="{html.escape(href, quote=True)}">{shown}</a>'


def inline_label(label):
    label = escape(label)
    return BOLD.sub(lambda m: f"<strong>{m.group(1) or m.group(2)}</strong>", label)


def block_table(lines):
    rows = [line.strip().strip("|").split("|") for line in lines]
    head, body = rows[0], rows[2:]
    out = ["<table>", "<thead>", "<tr>"]
    out += [f"<th>{inline(cell.strip())}</th>" for cell in head]
    out += ["</tr>", "</thead>", "<tbody>"]
    for row in body:
        out.append("<tr>" + "".join(f"<td>{inline(c.strip())}</td>" for c in row) + "</tr>")
    out += ["</tbody>", "</table>"]
    return "\n".join(out)


def blocks(text):
    lines = text.replace("\r\n", "\n").split("\n")
    out, i = [], 0
    list_tag = None

    def close_list():
        nonlocal list_tag
        if list_tag:
            out.append(f"</{list_tag}>")
            list_tag = None

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()

        if re.match(r"^(```|~~~)", line):
            fence = line[:3]
            close_list()
            i += 1
            body = []
            while i < len(lines) and not lines[i].strip().startswith(fence):
                body.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>" + escape("\n".join(body)) + "</code></pre>")
            continue

        if not line:
            close_list()
            i += 1
            continue

        if re.fullmatch(r"^(---+|\*\*\*+|___+)$", line):
            close_list()
            i += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.*?)\s*#*$", line)
        if heading:
            close_list()
            level = min(len(heading.group(1)) + 1, 4)
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        if line.startswith("|"):
            close_list()
            table = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table.append(lines[i])
                i += 1
            if len(table) > 1 and re.match(r"^\s*\|[-\s:|]+\|\s*$", table[1]):
                out.append(block_table(table))
            else:
                out.append("<pre><code>" + escape("\n".join(row.strip() for row in table)) + "</code></pre>")
            continue

        item = re.match(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$", raw)
        if item:
            tag = "ol" if re.match(r"^\s*\d", raw) else "ul"
            if list_tag != tag:
                close_list()
                out.append(f"<{tag}>")
                list_tag = tag
            out.append(f"<li>{inline(item.group(1))}</li>")
            i += 1
            continue

        if line.startswith(">"):
            close_list()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote><p>" + inline(" ".join(quote)) + "</p></blockquote>")
            continue

        if re.match(r"^<[a-zA-Z/!]", line):
            close_list()
            if re.match(r"^<img\b", line, re.I):
                i += 1
                continue
            text_line = [re.sub(r"<[^>]+>", "", line).strip()]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(
                    r"^\s*(#{1,6}\s|[-*+]\s|\d+[.)]\s|>|```|~~~)", lines[i]):
                text_line.append(re.sub(r"<[^>]+>", "", lines[i]).strip())
                i += 1
            joined = inline(" ".join(part for part in text_line if part))
            if joined.strip():
                out.append(f"<p>{joined}</p>")
            continue

        close_list()
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^\s*(#{1,6}\s|[-*+]\s|\d+[.)]\s|>|\||```|~~~|<[a-zA-Z/!])", lines[i]):
            para.append(lines[i].strip())
            i += 1
        text = inline(" ".join(para).strip())
        if text.strip():
            out.append("<p>" + text + "</p>")

    close_list()
    return "\n".join(out)


def plain(text):
    """Flattens inline markdown to the words, for titles and descriptions."""
    text = text.replace("\\[", "\x03").replace("\\]", "\x04")
    text = BADGE_BLOCK.sub("", text)
    text = IMAGE.sub("", text)
    text = LINK.sub(lambda m: m.group(1), text)
    text = AUTOLINK.sub(lambda m: m.group(1), text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("**", "").replace("`", "").replace("&amp;", "&")
    text = re.sub(r"\s+", " ", text.replace("\x03", "[").replace("\x04", "]"))
    return text.strip()


def summary(text):
    for line in text.split("\n"):
        clean = plain(re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line.strip()))
        clean = re.sub(r"^#+\s*", "", clean)
        if len(clean) > 40:
            clean = clean.split(". ")[0].rstrip(".")
            return (clean[:157] + "...") if len(clean) > 160 else clean
    return "An Azure or Entra assessment tool."


def first_heading(text, fallback):
    match = re.search(r"^#\s+(.+)$", text, re.M)
    name = plain(match.group(1)) if match else ""
    return name or fallback


def split_facts(text):
    """Takes the leading **Key:** value block off the cheatsheet as an at-a-glance list."""
    lines = text.split("\n")
    start = 0
    while start < len(lines) and not lines[start].strip():
        start += 1
    facts, end = [], start
    while end < len(lines):
        match = re.match(r"^\*\*([A-Za-z ]+):\*\*\s*(.+)$", lines[end].strip())
        if match:
            facts.append(match.groups())
            end += 1
            continue
        if not lines[end].strip() and end + 1 < len(lines) and re.match(
                r"^\*\*[A-Za-z ]+:\*\*", lines[end + 1].strip()):
            end += 1
            continue
        break
    if len(facts) > 8:
        facts, end = facts[:8], start + 8
    return facts, "\n".join(lines[end:])


def facts_html(found):
    if not found:
        return ""
    items = "".join(f"<li><strong>{k}</strong> {escape(v.strip())}</li>" for k, v in found)
    return f'<ul class="facts">{items}</ul>\n'


CLIP_BYTES = 60000


def clip(text):
    if len(text.encode("utf-8")) <= CLIP_BYTES:
        return text, ""
    cut = text.encode("utf-8")[:CLIP_BYTES].decode("utf-8", "ignore")
    at = cut.rfind("\n## ")
    if at > 4000:
        cut = cut[:at]
    note = ('<p class="small">Trimmed to the first part of the upstream README so the page '
            'stays inside the byte ceiling. The command reference below is complete.</p>')
    return cut, note


def page(slug, name, readme, cheats):
    readme, note = clip(readme)
    body_readme = re.sub(r"^#\s+.*$", "", readme, count=1, flags=re.M)
    description = summary(body_readme)
    head, _, rest = body_readme.partition("\n\n")
    body_readme = rest if len(summary(rest)) > 60 else body_readme
    out = HEAD.format(title=f"{name} - Breachcraft Dev", description=html.escape(description, quote=True),
                      path=f"/tools/{slug}/")
    out += f"  <p class=\"badge\"><span>Azure tool</span> upstream README &middot; captured {CAPTURED}</p>\n"
    out += f"  <p class=\"kicker\">{escape(name)}</p>\n  <h1>{escape(name)}</h1>\n"
    out += f"  <p class=\"lede\">{escape(description)}</p>\n"
    out += "  <h2>What it is</h2>\n" + blocks(body_readme) + ("\n  " + note if note else "")
    out += "\n  <h2>Commands</h2>\n"
    found, rest = split_facts(re.sub(r"^#\s+.*$", "", cheats, count=1, flags=re.M))
    out += facts_html(found) + blocks(rest)
    out += "\n" + TAIL.format(repo=SOURCE_REPO, captured=CAPTURED)
    (OUT / slug).mkdir(parents=True, exist_ok=True)
    (OUT / slug / "index.html").write_text(out, encoding="utf-8", newline="\n")
    return description


def main():
    if not CONTENT.is_dir():
        sys.exit(f"no content at {CONTENT}")
    tools = []
    for path in sorted(CONTENT.glob("*.cheats.md")):
        slug = path.name.removesuffix(".cheats.md")
        readme_path = CONTENT / f"{slug}.md"
        if not readme_path.is_file():
            continue
        readme = readme_path.read_text(encoding="utf-8")
        cheats = path.read_text(encoding="utf-8")
        name = first_heading(readme, slug.replace("-", " "))
        tools.append((slug, name, readme, cheats))

    index = HEAD.format(title="Offensive Azure tools - Breachcraft Dev",
                        description="Captured catalogue of open offensive Azure and Entra tooling: what each one is and the commands it runs.",
                        path="/tools/")
    index += '  <p class="kicker">Catalogue</p>\n  <h1>Offensive Azure tooling</h1>\n'
    index += '  <p class="lede">Every tool here is captured, with its commands, so a job starts from a reference rather than a search. Licences and provenance sit on each page.</p>\n'
    index += '  <ul class="items">\n'
    for slug, name, readme, cheats in tools:
        description = page(slug, name, readme, cheats)
        index += f'    <li><h2><a href="/tools/{slug}/">{escape(name)}</a></h2><p>{escape(description)}</p></li>\n'
    index += "  </ul>\n"
    index += '  <p class="small"><a href="/">&larr; Breachcraft Dev</a></p>\n</main>\n</body>\n</html>\n'
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(index, encoding="utf-8", newline="\n")

    urls = ["https://breachcraft.dev/", "https://breachcraft.dev/brief-lint/",
            "https://breachcraft.dev/site-audit/", "https://breachcraft.dev/tools/"]
    urls += [f"https://breachcraft.dev/tools/{slug}/" for slug, *_ in tools]
    sitemap = ['<?xml version="1.0" encoding="utf-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{url}</loc></url>" for url in urls]
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8", newline="\n")
    print(f"built {len(tools)} tool pages")


if __name__ == "__main__":
    main()

