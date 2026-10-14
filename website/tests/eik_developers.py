#!/usr/bin/env python3
"""Bilingual EIK developer routes: source, locale, bounded claims and production SEO."""
from html.parser import HTMLParser
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
KERNEL = "https://github.com/hamadalmunyif/paygod-kernel-mvp"
CLAIMS = KERNEL + "/blob/main/docs/CLAIMS_REGISTER.md"
REQUIRED = [
    KERNEL + "/blob/main/AGENTS.md",
    KERNEL + "/blob/main/docs/eik/README.md",
    KERNEL + "/blob/main/docs/eik/STATUS_2026-10-14.md",
    KERNEL + "/blob/main/docs/eik/capabilities.v0.json",
    KERNEL + "/blob/main/examples/eik-github-actions/README.md",
    KERNEL + "/blob/main/CONTRIBUTING.md",
    CLAIMS,
]


class Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = self.direction = self.robots = None
        self.mains = self.navs = 0
        self.links = []
        self.alternates = {}
        self.canonical = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "html":
            self.lang, self.direction = d.get("lang"), d.get("dir")
        if tag == "main":
            self.mains += 1
        if tag == "nav":
            self.navs += 1
        if tag == "a":
            self.links.append(d.get("href", ""))
        if tag == "meta" and d.get("name") == "robots":
            self.robots = d.get("content")
        if tag == "link" and d.get("rel") == "alternate":
            self.alternates[d.get("hreflang")] = d.get("href")
        if tag == "link" and d.get("rel") == "canonical":
            self.canonical.append(d.get("href"))


def main():
    for lang, path in (("en", "developers/index.html"), ("ar", "ar/developers/index.html")):
        f = DIST / path
        assert f.is_file(), path
        html = f.read_text(encoding="utf-8")
        check = Check()
        check.feed(html)
        assert (check.lang, check.direction) == (lang, "rtl" if lang == "ar" else "ltr")
        assert (check.mains, check.navs) == (1, 1)
        assert all(link in check.links for link in REQUIRED), (lang, "source/claims links missing")
        assert "paygod-workflow-observatory" not in html
        assert ("synthetic" in html.lower() if lang == "en" else "اصطناعي" in html)
        assert ("deploy" in html.lower() if lang == "en" else "تفويض" in html)
        assert check.alternates["en"] == "https://paygod.net/developers/"
        assert check.alternates["ar"] == "https://paygod.net/ar/developers/"
        assert "/v2/assets/style.css" in html
        assert (DIST / "v2/assets/style.css").is_file()
        if os.environ.get("VERCEL_ENV") == "production":
            assert check.robots == "index,follow"
            assert check.canonical == ["https://paygod.net/" + ("ar/" if lang == "ar" else "") + "developers/"]
        else:
            assert check.robots == "noindex,nofollow"
            assert not check.canonical

        home = (DIST / ("ar/home/index.html" if lang == "ar" else "index.html")).read_text(encoding="utf-8")
        link = "/ar/developers/" if lang == "ar" else "/developers/"
        assert 'href="' + link + '"' in home
        assert link in html
        assert (DIST / "v2" / ("ar" if lang == "ar" else "") / "index.html").is_file()
    if os.environ.get("VERCEL_ENV") == "production":
        sitemap = (DIST / "sitemap.xml").read_text(encoding="utf-8")
        assert "https://paygod.net/developers/" in sitemap
        assert "https://paygod.net/ar/developers/" in sitemap
    # Preserve the standalone verifier and independent technical demos untouched.
    assert (DIST / "verifier/index.html").is_file()
    assert (DIST / "downloads/paygod-verifier.html").is_file()
    print("PASS: bilingual developer entry, claim limits, current Kernel sources, production/preview isolation")


if __name__ == "__main__":
    main()
