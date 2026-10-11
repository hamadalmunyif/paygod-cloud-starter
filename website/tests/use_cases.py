#!/usr/bin/env python3
"""Source-bound editorial checks for bilingual Kernel use-case pages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
KERNEL = "https://github.com/hamadalmunyif/paygod-kernel-mvp"

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.dir = None
        self.mains = 0
        self.navs = 0
        self.details = 0
        self.links = []
        self.ids = set()
        self.duplicate_ids = set()
        self.robots = None
        self.canonicals = []
        self.alt_languages = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang, self.dir = attrs.get("lang"), attrs.get("dir")
        if tag == "main":
            self.mains += 1
        if tag == "nav":
            self.navs += 1
        if tag == "details":
            self.details += 1
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.duplicate_ids.add(attrs["id"])
            self.ids.add(attrs["id"])
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "meta" and attrs.get("name") == "robots":
            self.robots = attrs.get("content")
        if tag == "link":
            if attrs.get("rel") == "canonical":
                self.canonicals.append(attrs.get("href"))
            if attrs.get("rel") == "alternate":
                self.alt_languages.add(attrs.get("hreflang"))

def audit(path, lang, direction, peer, canonical, verifier):
    file = DIST / path
    assert file.is_file(), f"missing built page: {path}"
    html = file.read_text(encoding="utf-8")
    p = Page()
    p.feed(html)
    assert (p.lang, p.dir) == (lang, direction), (p.lang, p.dir)
    assert (p.mains, p.navs) == (1,1), (p.mains, p.navs)
    assert p.details == 9, f"expected 3 cases each for 3 actual Packs: {p.details}"
    assert not p.duplicate_ids, f"duplicate IDs: {p.duplicate_ids}"
    assert peer in p.links and verifier in p.links, f"missing peer language or verifier: {path}"
    assert {"en", "ar", "x-default"}.issubset(p.alt_languages)
    assert p.robots in ("noindex,nofollow", "index,follow")
    if p.robots == "index,follow":
        assert p.canonicals == [canonical], p.canonicals
    else:
        assert not p.canonicals, p.canonicals
    assert all(x not in html for x in ("__ATLAS_CSS__", "__TITLE__", "__HOME_HREF__", "__LANG__", "__DIR__", "__DESCRIPTION__"))
    assert ("<main class=\"" + ("ar" if lang == "en" else "en") + "\"") not in html
    assert "paygod-workflow-observatory" not in html and "agent-failure-taxonomy" not in html
    assert "SYNTHETIC TESTS" in html
    assert "WITHHELD" in html and "NOT RUN" in html
    for folder in ("ghg-scope-1-2-guard", "critical-cve-blocker", "iso27001-policy-review"):
        for fixture in ("pack.yaml", "tests/cases.yaml"):
            url = KERNEL + "/blob/main/packs/core/" + folder + "/" + fixture
            assert url in p.links, f"missing actual source link {url}"
    for href in p.links:
        if href.startswith("https://github.com/hamadalmunyif/"):
            assert href.startswith(KERNEL + "/") or href == KERNEL, f"noncanonical technical repo linked: {href}"
        if not href or href.startswith(("#", "https://", "mailto:")):
            continue
        destination = (file.parent / href.split("#")[0]).resolve()
        assert DIST.resolve() in destination.parents or destination == DIST.resolve(), f"path escape: {href}"
        assert destination.is_file() or (destination.is_dir() and (destination / "index.html").is_file()), f"broken local path: {path}: {href}"
    for fragment in ["/#architecture","/#cases","/#limits"]:
        assert fragment[2:] in p.ids, fragment
    print(f"PASS {path}: {lang} {direction}, 3 real Packs, 9 synthetic cases, source-only links, route integrity")

def main():
    audit("use-cases/index.html", "en", "ltr", "../ar/use-cases/", "https://paygod.net/use-cases/", "../verifier/")
    audit("ar/use-cases/index.html", "ar", "rtl", "../../use-cases/", "https://paygod.net/ar/use-cases/", "../../verifier/")
    landing = (DIST / "index.html").read_text(encoding="utf-8")
    atlas_en = (DIST / "explore/index.html").read_text(encoding="utf-8")
    atlas_ar = (DIST / "ar/index.html").read_text(encoding="utf-8")
    # The canonical homepage now uses the approved V2 visual route family.
    assert 'href="/v2/use-cases/"' in landing
    assert 'href="../use-cases/"' in atlas_en
    assert 'href="../ar/use-cases/"' in atlas_ar
    for path in ["verifier/index.html", "downloads/paygod-verifier.html"]:
        assert (DIST / path).is_file(), f"existing verifier removed: {path}"
    print("PASS: canonical landing and atlas discovery; independent verifier preserved")

if __name__ == "__main__":
    main()
