"""Public routes shared by validation and the local preview server."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://rinatabidullin.github.io/kilogram-site/"
PREFIX = "/kilogram-site/"
LOCALES = {"en": "", "ru": "ru/"}
ROUTES = ("", "privacy/", "terms/", "support/", "data-sources/", "licenses/")
PAGES = tuple(prefix + route + "index.html"
              for prefix in LOCALES.values() for route in ROUTES) + ("404.html",)
