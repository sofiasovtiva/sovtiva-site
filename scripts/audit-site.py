"""Static website release gate. Run from repository root: python scripts/audit-site.py."""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://sovtiva.com"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings = []
        self.meta = {}
        self.links = []
        self.resources = []
        self.ids = set()
        self.schema = []
        self._schema_active = False
        self._schema_buffer = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "h1":
            self.headings.append("h1")
        if tag == "meta":
            key = a.get("property") or a.get("name")
            if key:
                self.meta[key] = a.get("content", "")
        if tag == "link":
            if a.get("rel") == "canonical":
                self.meta["canonical"] = a.get("href", "")
            if a.get("href", "").startswith("/"):
                self.resources.append(a["href"])
        if tag == "a":
            self.links.append(a.get("href", ""))
        if tag in ("img", "script", "source") and a.get("src", "").startswith("/"):
            self.resources.append(a["src"])
        if tag == "img" and not a.get("alt", "").strip() and a.get("role") != "presentation":
            self.resources.append("MISSING_ALT")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._schema_active = True
            self._schema_buffer = []

    def handle_data(self, data):
        if self._schema_active:
            self._schema_buffer.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._schema_active:
            self.schema.append("".join(self._schema_buffer))
            self._schema_active = False


def route(file):
    relative = file.relative_to(ROOT).as_posix()
    return "/" if relative == "index.html" else "/" + relative.removesuffix("index.html")


def local_path(url):
    parsed = urlparse(url)
    candidate = ROOT / unquote(parsed.path.lstrip("/"))
    return candidate / "index.html" if parsed.path.endswith("/") else candidate


pages = {route(file): file for file in ROOT.rglob("index.html") if ".git" not in file.parts}
parsed = {}
problems = []
for path, file in pages.items():
    reader = Page()
    reader.feed(file.read_text(encoding="utf-8"))
    parsed[path] = reader
    for required in ("description", "og:title", "og:description", "og:url", "og:image", "canonical"):
        if not reader.meta.get(required):
            problems.append(f"{path}: missing {required}")
    if reader.meta.get("canonical") != ORIGIN + path:
        problems.append(f"{path}: canonical mismatch")
    if reader.meta.get("og:url") != ORIGIN + path:
        problems.append(f"{path}: Open Graph URL mismatch")
    if len(reader.headings) != 1:
        problems.append(f"{path}: expected one H1, found {len(reader.headings)}")
    for schema in reader.schema:
        try:
            json.loads(schema)
        except json.JSONDecodeError:
            problems.append(f"{path}: invalid structured data")
    for resource in reader.resources:
        if resource == "MISSING_ALT":
            problems.append(f"{path}: image without meaningful alt text")
        elif not local_path(resource.split("?", 1)[0]).is_file():
            problems.append(f"{path}: missing resource {resource}")
    image = reader.meta.get("og:image", "")
    if image.startswith(ORIGIN + "/") and not local_path(image[len(ORIGIN):]).is_file():
        problems.append(f"{path}: missing social image {image}")

for path, reader in parsed.items():
    for href in reader.links:
        if not href or href.startswith(("mailto:", "tel:", "javascript:")):
            continue
        parts = urlparse(href)
        if parts.scheme or parts.netloc:
            continue
        target_path = parts.path if parts.path.startswith("/") else path + parts.path
        if not parts.path:
            target_path = path
        target_file = local_path(target_path)
        if not target_file.is_file():
            problems.append(f"{path}: broken internal link {href}")
        elif parts.fragment and target_path in parsed and parts.fragment not in parsed[target_path].ids:
            problems.append(f"{path}: missing linked section {href}")

try:
    sitemap = ElementTree.parse(ROOT / "sitemap.xml")
    entries = {loc.text for loc in sitemap.findall(".//{*}loc") if loc.text}
    for path in pages:
        if ORIGIN + path not in entries:
            problems.append(f"{path}: missing sitemap entry")
except ElementTree.ParseError:
    problems.append("Invalid sitemap XML")

if problems:
    print(f"FAILED: {len(problems)} issue(s) across {len(pages)} pages")
    print("\n".join(problems))
    sys.exit(1)
print(f"PASS: {len(pages)} pages, metadata, assets, internal links, anchors, schema, sitemap")
