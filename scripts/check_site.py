#!/usr/bin/env python3
"""Check the static project site using only the Python standard library."""
import argparse
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
import struct
from urllib.parse import unquote, urljoin, urlsplit
from urllib.error import HTTPError
from urllib.request import urlopen

from site_config import BASE, LOCALES, PAGES, PREFIX, ROOT, ROUTES
FORBIDDEN = re.compile(
    r"DEVELOPER_NAME_OR_COMPANY|PRIVACY_EMAIL|SUPPORT_EMAIL|"
    r"OFF_DERIVATIVE_DATABASE_URL_OR_REMOVE|OPEN_SOURCE_NOTICES|YOUR_USERNAME|"
    r"PLACEHOLDER|Before publishing|Describe here|Add the exact|If Kilogram offers|"
    r"Редакторское|не публиковать|/Users/|file://", re.I)


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.tags = [], [], []
        self.language_links, self.navigation_links, self.main_links = [], [], []
        self.main_tags, self.title = [], []
        self.in_switcher = self.in_main = self.in_title = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "nav" and "language-switcher" in attrs.get("class", "").split():
            self.in_switcher = True
        if tag == "main":
            self.in_main = True
        if tag == "title":
            self.in_title = True
        if self.in_main:
            self.main_tags.append((tag, attrs))
        if tag == "a":
            (self.language_links if self.in_switcher else self.navigation_links).append(attrs)
            if self.in_main:
                self.main_links.append(attrs.get("href", ""))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for name in ("href", "src"):
            if name in attrs:
                self.links.append((tag, name, attrs[name]))

    def handle_endtag(self, tag):
        if tag == "nav":
            self.in_switcher = False
        if tag == "main":
            self.in_main = False
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


def localization_errors(documents):
    """Validate language pairs and routing; translation meaning needs human review."""
    errors = []
    for route in ROUTES:
        urls = {lang: BASE + prefix + route for lang, prefix in LOCALES.items()}
        pairs = {}
        for lang, prefix in LOCALES.items():
            name = prefix + route + "index.html"
            doc = documents.get(name)
            if doc is None:
                continue  # Missing files are reported by check().
            pairs[lang] = doc
            if [a.get("lang") for t, a in doc.tags if t == "html"] != [lang]:
                errors.append(f"{name}: expected html lang={lang}")
            if not "".join(doc.title).strip() or not any(
                    t == "meta" and a.get("name") == "description" and a.get("content", "").strip()
                    for t, a in doc.tags):
                errors.append(f"{name}: missing title or description")
            canonical = [a.get("href") for t, a in doc.tags if t == "link" and a.get("rel") == "canonical"]
            if canonical != [urls[lang]]:
                errors.append(f"{name}: canonical must point to this language version")
            alternates = [(a.get("hreflang"), a.get("href")) for t, a in doc.tags
                          if t == "link" and a.get("rel") == "alternate"]
            if sorted(alternates, key=str) != sorted(urls.items()):
                errors.append(f"{name}: expected reciprocal hreflang links for all locales")
            switches = [(a.get("hreflang"), urljoin(urls[lang], a.get("href", "")))
                        for a in doc.language_links]
            if sorted(switches, key=str) != sorted(urls.items()):
                errors.append(f"{name}: language switcher must link to the same page in all locales")
            active = [a.get("hreflang") for a in doc.language_links if a.get("aria-current") == "page"]
            if active != [lang] or any(a.get("lang") != a.get("hreflang") for a in doc.language_links):
                errors.append(f"{name}: incorrect switcher language or current state")
            for a in doc.navigation_links:
                resolved = urljoin(urls[lang], a.get("href", ""))
                if resolved.startswith(BASE):
                    relative = urlsplit(resolved).path.removeprefix(PREFIX)
                    target_lang = next((code for code, folder in LOCALES.items()
                                        if folder and relative.startswith(folder)), "en")
                    if target_lang != lang:
                        errors.append(f"{name}: navigation leaves {lang}: {a.get('href')}")
        original = pairs.get("en")
        if original is None:
            continue
        for lang, translated in pairs.items():
            if lang == "en":
                continue
            name = LOCALES[lang] + route + "index.html"
            for label, extract in (
                ("section structure", lambda d: [t for t, _ in d.main_tags if t in ("h2", "h3")]),
                ("fragment IDs", lambda d: sorted(d.ids)),
                ("document dates", lambda d: [a.get("datetime") for t, a in d.main_tags if t == "time"]),
            ):
                if extract(original) != extract(translated):
                    errors.append(f"{name}: {label} differs from English; update both versions")
            def normalized_links(doc, locale):
                result = []
                for href in doc.main_links:
                    resolved = urljoin(urls[locale], href)
                    prefix_url = BASE + LOCALES[locale]
                    result.append(BASE + resolved[len(prefix_url):] if resolved.startswith(prefix_url) else resolved)
                return sorted(result)
            if normalized_links(original, "en") != normalized_links(translated, lang):
                errors.append(f"{name}: content links differ from English; update both versions")
    return errors


def check(http=None, icon_source=None):
    errors, local, external = [], set(), set()
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*.html")
              if not any(part.startswith(".") or part == "node_modules" for part in p.relative_to(ROOT).parts)}
    for name in sorted(set(PAGES) - actual):
        errors.append(f"{name}: missing public page or translation")
    for name in sorted(actual - set(PAGES)):
        errors.append(f"{name}: unregistered HTML page; add all locales to site_config.py")
    documents = {name: Document((ROOT / name).read_text(encoding="utf-8")) for name in PAGES if name in actual}
    errors.extend(localization_errors(documents))
    for path in [*(ROOT / name for name in PAGES), *sorted((ROOT / "assets").glob("*.css")),
                 *sorted((ROOT / "assets").glob("*.js"))]:
        if path.is_file() and FORBIDDEN.search(path.read_text(encoding="utf-8")):
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
        for missing in ("not-a-page/", "ru/not-a-page/deeper/"):
            path = PREFIX + missing
            try:
                with urlopen(http.rstrip("/") + path, timeout=10):
                    errors.append(f"{path}: expected HTTP 404")
            except HTTPError as exc:
                body = exc.read().decode("utf-8")
                if exc.code != 404 or "Page not found" not in body or "Страница не найдена" not in body:
                    errors.append(f"{path}: expected bilingual HTTP 404")
            except Exception as exc:
                errors.append(f"HTTP failure: {path}: {exc}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(PAGES)} HTML pages; {len(local)} local targets; {len(external)} external URLs inventoried.")
    print("PASS: project prefix, fragments, mailto, public copy, local assets and RGBA icon.")
    print("PASS: EN/RU pairs, lang, canonical, hreflang, language switches, section structure, dates and content links.")
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
