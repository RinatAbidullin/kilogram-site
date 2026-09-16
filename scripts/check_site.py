#!/usr/bin/env python3
"""Check the static project site using only the Python standard library."""
import argparse
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
import struct
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://rinatabidullin.github.io/kilogram-site/"
PREFIX = "/kilogram-site/"
PAGES = ["index.html", "privacy/index.html", "terms/index.html", "support/index.html",
         "data-sources/index.html", "licenses/index.html", "404.html"]
FORBIDDEN = re.compile(
    r"DEVELOPER_NAME_OR_COMPANY|PRIVACY_EMAIL|SUPPORT_EMAIL|"
    r"OFF_DERIVATIVE_DATABASE_URL_OR_REMOVE|OPEN_SOURCE_NOTICES|YOUR_USERNAME|"
    r"PLACEHOLDER|Before publishing|Describe here|Add the exact|If Kilogram offers|"
    r"Редакторское|не публиковать|/Users/|file://", re.I)


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.tags = [], [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for name in ("href", "src"):
            if name in attrs:
                self.links.append((tag, name, attrs[name]))


def check(http=None, icon_source=None):
    errors, local, external = [], set(), set()
    documents = {name: Document((ROOT / name).read_text()) for name in PAGES}
    for path in [*(ROOT / name for name in PAGES), *sorted((ROOT / "assets").glob("*.css")),
                 *sorted((ROOT / "assets").glob("*.js"))]:
        if FORBIDDEN.search(path.read_text()):
            errors.append(f"{path.relative_to(ROOT)}: unfinished copy or private path")
    for name, doc in documents.items():
        page_url = urljoin(BASE, name.removesuffix("index.html"))
        if len(doc.ids) != len(set(doc.ids)):
            errors.append(f"{name}: duplicate IDs")
        if sum(tag == "h1" for tag, _ in doc.tags) != 1:
            errors.append(f"{name}: expected one h1")
        for tag, attrs in doc.tags:
            if tag in ("base", "form", "iframe"):
                errors.append(f"{name}: unexpected {tag}")
            if tag == "img" and not all(key in attrs for key in ("alt", "width", "height")):
                errors.append(f"{name}: image needs alt and intrinsic dimensions")
            if tag == "link" and attrs.get("rel") in ("preload", "prefetch", "preconnect", "dns-prefetch"):
                errors.append(f"{name}: unexpected preloading")
        for tag, attribute, value in doc.links:
            if value.startswith("/"):
                errors.append(f"{name}: root-relative URL {value}")
            if value.startswith("mailto:"):
                if urlsplit(value).path != "rinatabidullin@gmail.com":
                    errors.append(f"{name}: unexpected email {value}")
                continue
            resolved = urljoin(page_url, value)
            if not resolved.startswith(BASE):
                external.add(resolved)
                if tag != "a" or attribute != "href" or not resolved.startswith("https://"):
                    errors.append(f"{name}: unexpected external resource {resolved}")
                continue
            parts = urlsplit(resolved)
            relative = unquote(parts.path.removeprefix(PREFIX))
            target = ROOT / relative
            if target.is_dir():
                target /= "index.html"
            if not target.resolve().is_relative_to(ROOT) or not target.is_file():
                errors.append(f"{name}: missing local target {value}")
                continue
            local.add(parts.path)
            if parts.fragment:
                target_name = str(target.relative_to(ROOT))
                if target_name not in documents or unquote(parts.fragment) not in documents[target_name].ids:
                    errors.append(f"{name}: missing fragment {value}")
    image = (ROOT / "assets/kilogram-app-icon.png").read_bytes()
    if image[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", image[16:24]) != (1024, 1024) or image[25] != 6:
        errors.append("App icon must be a 1024×1024 RGBA PNG")
    if icon_source and image != Path(icon_source).read_bytes():
        errors.append("App icon differs from supplied original")
    if http:
        local.update(PREFIX + name.removesuffix("index.html") for name in PAGES)
        for path in sorted(local):
            try:
                with urlopen(http.rstrip("/") + path, timeout=10) as response:
                    if response.status != 200 or not response.read():
                        errors.append(f"HTTP failure: {path}")
            except Exception as exc:
                errors.append(f"HTTP failure: {path}: {exc}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(PAGES)} HTML pages; {len(local)} local targets; {len(external)} external URLs inventoried.")
    print("PASS: project prefix, fragments, mailto, public copy, local assets and RGBA icon.")
    print("Icon SHA-256:", hashlib.sha256(image).hexdigest())
    if http:
        print("PASS: HTTP responses for every local target under /kilogram-site/.")
    print("External URLs (inventory only; not a network check):")
    for url in sorted(external):
        print(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--http", help="Local server origin, e.g. http://127.0.0.1:8000")
    parser.add_argument("--icon-source", help="Optional original PNG for byte-for-byte comparison")
    args = parser.parse_args()
    check(args.http, args.icon_source)
