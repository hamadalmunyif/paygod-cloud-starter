#!/usr/bin/env python3
"""Static bilingual Evidence Lab routes; no second verifier or live policy authority."""
from html.parser import HTMLParser
from pathlib import Path
import os
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = self.direction = self.robots = None
        self.nav = self.main = 0
        self.links = []
        self.ids = set()
        self.dupes = set()
        self.canonical = []
        self.alternates = {}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang, self.direction = a.get("lang"), a.get("dir")
        if tag == "nav": self.nav += 1
        if tag == "main": self.main += 1
        if tag == "a": self.links.append(a.get("href"))
        if a.get("id"):
            if a["id"] in self.ids: self.dupes.add(a["id"])
            self.ids.add(a["id"])
        if tag == "meta" and a.get("name") == "robots": self.robots = a.get("content")
        if tag == "link" and a.get("rel") == "canonical": self.canonical.append(a.get("href"))
        if tag == "link" and a.get("rel") == "alternate": self.alternates[a.get("hreflang")] = a.get("href")

def main():
    for lang, name, home in (("en","lab/index.html","index.html"),("ar","ar/lab/index.html","ar/home/index.html")):
        page = (DIST / name).read_text(encoding="utf-8")
        p = Page()
        p.feed(page)
        assert p.lang == lang and p.direction == ("rtl" if lang == "ar" else "ltr")
        assert p.nav == p.main == 1 and not p.dupes, (name,p.nav,p.main,p.dupes)
        assert "/verifier/" in p.links
        assert "critical-cve-blocker/pack.yaml" in page
        assert "tests/cases.yaml" in page
        assert "/lab/assets/lab.css" in page and "/lab/assets/lab.js" in page
        assert "id=\"cve-score\"" in page and "id=\"remediation\"" in page
        assert "id=\"scan-complete\"" in page and "id=\"integrity-outcome\"" in page
        assert "id=\"lab-labels\"" in page and "application/json" in page
        assert "paygod-workflow-observatory" not in page
        assert p.alternates == {"en":"https://paygod.net/lab/","ar":"https://paygod.net/ar/lab/"}
        expected = "https://paygod.net/" + ("ar/" if lang == "ar" else "") + "lab/"
        if os.environ.get("VERCEL_ENV") == "production":
            assert p.robots == "index,follow" and p.canonical == [expected]
        else:
            assert p.robots == "noindex,nofollow" and not p.canonical
        main_home = (DIST / home).read_text(encoding="utf-8")
        assert 'href="' + ("/ar/lab/" if lang == "ar" else "/lab/") + '"' in main_home
        assert p.alternates["ar" if lang == "en" else "en"] in (page or "")
    for file in ("verifier.mjs", "sha256.mjs"):
        assert (DIST / "lab/assets" / file).read_bytes() == (ROOT / "src" / file).read_bytes(), file
    assert (DIST / "lab/assets/sample.json").read_bytes() == (ROOT / "demo/sample.json").read_bytes()
    css = (DIST / "lab/assets/lab.css").read_text(encoding="utf-8")
    js = (DIST / "lab/assets/lab.js").read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in css
    assert "verifyTransport" in js and 'from "./verifier.mjs"' in js
    assert "renderCve" in js and "WITHHELD" not in js  # Labels come from the bilingual page.
    assert (DIST / "verifier/index.html").is_file()
    assert (DIST / "v1/index.html").is_file()
    assert (DIST / "v1/ar/home/index.html").is_file()
    if os.environ.get("VERCEL_ENV") == "production":
        sitemap = (DIST / "sitemap.xml").read_text(encoding="utf-8")
        assert "<loc>https://paygod.net/lab/</loc>" in sitemap
        assert "<loc>https://paygod.net/ar/lab/</loc>" in sitemap
    print("PASS: bilingual lab, canonical/preview SEO, navigation, identical verifier modules and synthetic sample")

if __name__ == "__main__":
    main()
