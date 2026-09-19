"""Regression checks for localization mistakes that still produce valid HTML."""
import unittest
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from unittest.mock import patch

from check_site import Document, check, localization_errors
from site_config import PAGES, ROOT


class LocalizationChecks(unittest.TestCase):
    def setUp(self):
        self.sources = {name: (ROOT / name).read_text(encoding="utf-8") for name in PAGES}

    def errors_after(self, page, before, after):
        self.assertIn(before, self.sources[page])
        self.sources[page] = self.sources[page].replace(before, after, 1)
        return localization_errors({name: Document(text) for name, text in self.sources.items()})

    def test_current_localizations(self):
        self.assertEqual(localization_errors({name: Document(text) for name, text in self.sources.items()}), [])

    def test_missing_translation_is_reported_without_crashing(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for name, source in self.sources.items():
                if name == "ru/support/index.html":
                    continue
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(source, encoding="utf-8")
            shutil.copytree(ROOT / "assets", root / "assets")
            with patch("check_site.ROOT", root):
                with self.assertRaisesRegex(SystemExit, "ru/support/index.html: missing public page or translation"):
                    check()

    def test_switcher_cannot_return_to_home_from_support(self):
        errors = self.errors_after("ru/support/index.html", 'href="../../support/"', 'href="../../"')
        self.assertTrue(any("language switcher" in error for error in errors))

    def test_russian_navigation_cannot_open_english_document(self):
        errors = self.errors_after("ru/support/index.html", 'href="../privacy/"', 'href="../../privacy/"')
        self.assertTrue(any("navigation leaves ru" in error for error in errors))

    def test_russian_canonical_cannot_point_to_english(self):
        errors = self.errors_after("ru/support/index.html",
                                  'rel="canonical" href="https://rinatabidullin.github.io/kilogram-site/ru/support/"',
                                  'rel="canonical" href="https://rinatabidullin.github.io/kilogram-site/support/"')
        self.assertTrue(any("canonical" in error for error in errors))

    def test_missing_hreflang_is_detected(self):
        errors = self.errors_after("support/index.html", 'hreflang="ru"', 'hreflang="de"')
        self.assertTrue(any("reciprocal hreflang" in error for error in errors))

    def test_missing_translated_section_is_detected(self):
        errors = self.errors_after("ru/support/index.html", "<h2>Отмена подписки</h2>", "")
        self.assertTrue(any("section structure" in error for error in errors))

    def test_outdated_document_version_is_detected(self):
        errors = self.errors_after("ru/support/index.html", 'datetime="2026-09-16"', 'datetime="2026-09-15"')
        self.assertTrue(any("document dates" in error for error in errors))

    def test_changed_download_is_detected(self):
        errors = self.errors_after("ru/data-sources/index.html",
                                  "https://drive.google.com/file/d/1NzUM6jaEcSZrMdNPCFFt3goFEkJGOzcD",
                                  "https://drive.google.com/file/d/different-catalogue")
        self.assertTrue(any("content links" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
