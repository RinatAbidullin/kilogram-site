"""Regression checks for localization and the optimized web icon contract."""
from contextlib import redirect_stdout
from io import StringIO
import struct
import unittest
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from unittest.mock import patch

from check_site import Document, check, localization_errors
from site_config import PAGES, ROOT


class IconChecks(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        for name in PAGES:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        shutil.copytree(ROOT / "assets", self.root / "assets")
        self.icon = self.root / "assets/kilogram-app-icon.png"
        self.original = self.icon.read_bytes()
        root_patch = patch("check_site.ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def test_current_web_icon_passes_site_check(self):
        with redirect_stdout(StringIO()):
            check()

    def test_wrong_icon_dimensions_are_rejected(self):
        for width, height in ((64, 64), (128, 64), (1024, 1024)):
            with self.subTest(width=width, height=height):
                image = bytearray(self.original)
                image[16:24] = struct.pack(">II", width, height)
                self.icon.write_bytes(image)
                with self.assertRaisesRegex(SystemExit, "128×128 8-bit RGBA PNG"):
                    check()

    def test_wrong_bit_depth_or_missing_alpha_is_rejected(self):
        for depth, color in ((16, 6), (8, 2), (8, 3)):
            with self.subTest(depth=depth, color=color):
                image = bytearray(self.original)
                image[24:26] = bytes((depth, color))
                self.icon.write_bytes(image)
                with self.assertRaisesRegex(SystemExit, "128×128 8-bit RGBA PNG"):
                    check()

    def test_invalid_or_truncated_header_is_reported_without_crashing(self):
        for image in (b"", b"not a PNG", self.original[:20], self.original[:32],
                      self.original[:12] + b"IDAT" + self.original[16:]):
            with self.subTest(header=image[:33]):
                self.icon.write_bytes(image)
                with self.assertRaisesRegex(SystemExit, "128×128 8-bit RGBA PNG"):
                    check()

    def test_optional_source_comparison_remains_byte_for_byte(self):
        source = self.root / "reference.png"
        source.write_bytes(self.original)
        with redirect_stdout(StringIO()):
            check(icon_source=source)
        source.write_bytes(self.original + b"different bytes")
        with self.assertRaisesRegex(SystemExit, "App icon differs from supplied original"):
            check(icon_source=source)


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
            root = Path(directory).resolve()
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
