#!/usr/bin/env python3
"""Render the specification to static HTML for xprs.dev/spec.

Input is the Markdown in this repository; output is site/, which the Pages
workflow publishes. Nothing is committed: the HTML is built on push.

Anchors follow GitHub's slug rules, so a link written for the file on GitHub
(XPRS.md#3-callsigns) resolves on the published page (xprs.dev/spec/#3-callsigns).
"""

import html
import pathlib
import re
import shutil
import sys

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site"

EXTENSIONS = ["tables", "fenced_code", "sane_lists"]

# GitHub slug: lowercase, drop everything that is not a word character, a
# space or a hyphen, then spaces to hyphens. "## 3.1.2 Suffixes" -> 3.1.2 is
# kept without its dots, which is what the document's own links assume.
_STRIP = re.compile(r"[^\w\- ]", re.UNICODE)


def slug(text):
    s = re.sub(r"<[^>]+>", "", text)
    s = html.unescape(s).strip().lower()
    s = _STRIP.sub("", s)
    return s.replace(" ", "-")


HEADING = re.compile(r"<h([1234])>(.*?)</h\1>", re.S)


def anchor(body):
    """Give every h2-h4 an id and a self-link, and collect the contents list."""
    toc = []
    seen = {}

    def one(m):
        level, text = int(m.group(1)), m.group(2)
        s = slug(text)
        n = seen.get(s, 0)
        seen[s] = n + 1
        if n:
            s = f"{s}-{n}"
        toc.append((level, s, re.sub(r"<[^>]+>", "", text)))
        return (f'<h{level} id="{s}">'
                f'<a href="#{s}">{text}</a></h{level}>')

    return HEADING.sub(one, body), toc


def nav(toc, current):
    """Sidebar: every section, and the subsections of the document itself."""
    out = ['<nav class="toc" aria-label="Contents"><details>',
           "<summary>Contents</summary><ul>"]
    top = min((l for l, _, _ in toc), default=2)
    for level, s, text in toc:
        # Two levels: parts and sections. Anything deeper belongs to the
        # text, not to a navigation column.
        if level > top + 1 or text.strip().lower() == "contents":
            continue
        cls = "part" if level == top else "sect"
        out.append(f'<li class="{cls}"><a href="#{s}">{html.escape(text)}</a></li>')
    out.append("</ul></details></nav>")
    return "\n".join(out)


CSS = """
:root {
  --bg: #f4f1ea; --ink: #2a2620; --dim: #6b645a; --line: #d8d2c4;
  --accent: #23557a; --code-bg: #ebe6da;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #232a2e; --ink: #e8e3d6; --dim: #9a938a; --line: #3a4248;
    --accent: #7db4d8; --code-bg: #1b2124;
  }
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: var(--bg); color: var(--ink);
  font: 17px/1.6 Georgia, 'Times New Roman', serif;
  padding: 0 1.2rem;
}
.page { max-width: 64rem; margin: 0 auto; padding: 2.5rem 0 5rem;
        display: grid; grid-template-columns: 1fr; gap: 2rem; }
/* The contents column appears only when there is room for it beside the
   text; below that width it is a collapsed block above the document. */
@media (min-width: 62rem) {
  .page { grid-template-columns: 15rem minmax(0, 1fr); }
  .toc { position: sticky; top: 1.5rem; align-self: start;
         max-height: calc(100vh - 3rem); overflow-y: auto; }
}
main { max-width: 44rem; min-width: 0; }
h1 { font-family: 'Courier New', monospace; font-size: 2.1rem;
     letter-spacing: 0.04em; margin-bottom: 0.4rem; }
.tagline { color: var(--dim); margin-bottom: 0.4rem; }
.meta { color: var(--dim); font-size: 0.9rem; margin-bottom: 2rem; }
.meta a { margin-right: 0.9rem; white-space: nowrap; }
main h1 { font-size: 1.5rem; margin: 3rem 0 0.8rem; padding-top: 1.4rem;
     border-top: 3px double var(--line); }
main > h1:first-child { font-size: 2.1rem; border-top: 0;
     margin-top: 0; padding-top: 0; }
h2 { font-family: 'Courier New', monospace; font-size: 1.15rem;
     margin: 2.4rem 0 0.8rem; padding-top: 1.2rem;
     border-top: 1px solid var(--line); scroll-margin-top: 1rem; }
h3 { font-family: 'Courier New', monospace; font-size: 1rem;
     margin: 1.8rem 0 0.6rem; scroll-margin-top: 1rem; }
h4 { font-family: 'Courier New', monospace; font-size: 0.95rem;
     margin: 1.4rem 0 0.5rem; scroll-margin-top: 1rem; }
main h1 a, h2 a, h3 a, h4 a { color: inherit; text-decoration: none; }
main h1 a::after, h2 a::after, h3 a::after, h4 a::after {
  content: ' #'; color: var(--dim); opacity: 0.3; font-weight: normal;
}
main h1 a:hover, h2 a:hover, h3 a:hover, h4 a:hover { color: var(--accent); }
p { margin-bottom: 0.9rem; }
a { color: var(--accent); }
ul, ol { margin: 0 0 0.9rem 1.4rem; }
li { margin-bottom: 0.45rem; }
code { font-family: 'Courier New', monospace; font-size: 0.92em; }
pre { background: var(--code-bg); border: 1px solid var(--line);
      padding: 0.8rem 1rem; overflow-x: auto;
      font: 13px/1.5 'Courier New', monospace;
      margin: 1rem 0; border-radius: 3px; }
pre code { font-size: inherit; }
blockquote { border-left: 3px solid var(--line); padding-left: 1rem;
             color: var(--dim); margin: 1rem 0; }
hr { border: 0; border-top: 1px solid var(--line); margin: 2rem 0; }
/* Tables are wide and the page must not scroll sideways, so each one
   scrolls inside its own box. */
.tw { overflow-x: auto; margin: 1rem 0; }
table { border-collapse: collapse; font-size: 0.92rem; }
th, td { text-align: left; padding: 0.45rem 0.9rem 0.45rem 0;
         border-bottom: 1px solid var(--line); vertical-align: top; }
th { font-family: 'Courier New', monospace; font-weight: normal;
     color: var(--dim); }
.toc { font-size: 0.88rem; line-height: 1.45; }
.toc summary { font-family: 'Courier New', monospace; color: var(--dim);
               cursor: pointer; margin-bottom: 0.6rem; }
.toc ul { list-style: none; margin: 0; }
.toc li { margin: 0 0 0.25rem; }
.toc a { text-decoration: none; }
.toc a:hover { text-decoration: underline; }
.toc .part { font-family: 'Courier New', monospace; margin-top: 0.7rem; }
.toc .sect { padding-left: 0.9rem; }
.toc .sect a { color: var(--dim); }
footer { margin-top: 3rem; padding-top: 1.2rem;
         border-top: 1px solid var(--line);
         color: var(--dim); font-size: 0.9rem; }
"""

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>{css}</style>
</head>
<body>
<div class="page">
{nav}
<main>
<h1>{h1}</h1>
<div class="tagline">{tagline}</div>
{meta_html}{body}
<footer>{footer}</footer>
</main>
</div>
<script>
if (matchMedia('(min-width: 62rem)').matches) {{
  var d = document.querySelector('.toc details');
  if (d) d.open = true;
}}
</script>
</body>
</html>
"""


def render(md_text):
    body = markdown.markdown(md_text, extensions=EXTENSIONS)
    # The document's own title is replaced by the page header, so it is
    # dropped before anchoring or it would head the contents column too.
    body = re.sub(r"^\s*<h1>.*?</h1>\s*", "", body, count=1, flags=re.S)
    body, toc = anchor(body)
    # Wrap tables so a wide one scrolls inside itself.
    body = body.replace("<table>", '<div class="tw"><table>')
    body = body.replace("</table>", "</table></div>")
    return body, toc


def strip_contents(body):
    """Drop the in-document contents section; the sidebar carries that list.

    The Markdown keeps it for anyone reading the file itself."""
    return re.sub(
        r'(<hr ?/?>\n?)?<h2 id="contents">.*?<hr ?/?>\n?', "", body, count=1, flags=re.S)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    spec = (ROOT / "XPRS.md").read_text(encoding="utf-8")
    body, toc = render(spec)
    body = strip_contents(body)
    (OUT / "index.html").write_text(PAGE.format(
        title="XPRS specification",
        desc=("The XPRS packet format: 250-byte key:value packets carrying "
              "messages, observations, files, commands and services over LoRa, "
              "BLE, WiFi, amateur bands and the internet."),
        css=CSS,
        nav=nav(toc, "spec"),
        h1="XPRS",
        tagline="eXtended Packet Radio System &mdash; protocol specification",
        meta_html="",
        body=body,
        footer=("Copyright (c) 2026 Max Brito. Licensed CC BY 4.0. "
                "This page is generated from XPRS.md in "
                '<a href="https://github.com/xprs-dev/spec">xprs-dev/spec</a>; '
                "the file is the authoritative copy."),
    ), encoding="utf-8")

    api = (ROOT / "API-HTTP.md").read_text(encoding="utf-8")
    abody, atoc = render(api)
    (OUT / "api-http.html").write_text(PAGE.format(
        title="XPRS station HTTP API",
        desc=("The HTTP interface an XPRS station offers on its local network: "
              "what it heard, its log, and handing it a packet to transmit."),
        css=CSS,
        nav=nav(atoc, "api"),
        h1="Station HTTP API",
        tagline="A convenience interface on the local network, not the protocol",
        meta_html=('<div class="meta"><a href="/">xprs.dev</a>'
                   '<a href="./">specification</a>'
                   '<a href="https://github.com/xprs-dev/spec">repository</a>'
                   '</div>'),
        body=abody,
        footer=("Copyright (c) 2026 Max Brito. Licensed CC BY 4.0. "
                "Generated from API-HTTP.md."),
    ), encoding="utf-8")

    shutil.copy(ROOT / "xprs_corpus.json", OUT / "xprs_corpus.json")
    for f in ("XPRS.md", "API-HTTP.md", "LICENSE", "NOTICE"):
        shutil.copy(ROOT / f, OUT / f)

    for f in sorted(OUT.iterdir()):
        print(f"{f.name}: {f.stat().st_size} bytes")


if __name__ == "__main__":
    sys.exit(main())
