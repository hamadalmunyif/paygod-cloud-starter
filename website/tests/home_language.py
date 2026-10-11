#!/usr/bin/env python3
"""Gate canonical V2 bilingual home and preserved classic producer/demo workspaces.

Previously the classic pages occupied / and /ar/home/; post-promotion the
new landing occupies those URLs, while the originals remain /legacy/ and
/ar/legacy/. The verifier is neither changed nor loaded by this test.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import os
import re

DIST = Path(__file__).resolve().parents[1] / "dist"
KERNEL = "https://github.com/hamadalmunyif/paygod-kernel-mvp"

class Audit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.direction = None
        self.mains = 0
        self.navs = 0
        self.links = []
        self.ids = set()
        self.duplicates = set()
        self.alternates = {}
        self.canonicals = []
        self.robots = None
        self.text = []
        self.stylesheets = []
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang, self.direction = a.get("lang"), a.get("dir")
        if tag == "main": self.mains += 1
        if tag == "nav": self.navs += 1
        if "id" in a:
            if a["id"] in self.ids: self.duplicates.add(a["id"])
            self.ids.add(a["id"])
        if tag == "a": self.links.append(a.get("href", ""))
        if tag == "link":
            if a.get("rel") == "alternate": self.alternates[a.get("hreflang")] = a.get("href")
            if a.get("rel") == "canonical": self.canonicals.append(a.get("href"))
            if a.get("rel") == "stylesheet": self.stylesheets.append(a.get("href", ""))
        if tag == "script" and a.get("src"): self.scripts.append(a.get("src"))
        if tag == "meta" and a.get("name") == "robots": self.robots = a.get("content")
    def handle_data(self, data): self.text.append(data)

def inspect(path):
    file = DIST / path
    assert file.is_file(), path
    html = file.read_text(encoding="utf-8")
    p = Audit()
    p.feed(html)
    assert (p.mains, p.navs) == (1, 1), (path, p.mains, p.navs)
    assert not p.duplicates, (path, p.duplicates)
    assert "paygod-workflow-observatory" not in html, path
    return p, html

def validate_local_links(path, audit):
    base = (DIST / path).parent
    for href in [*audit.links, *audit.stylesheets, *audit.scripts]:
        assert href, (path, href)
        if href.startswith(("https://", "http://", "mailto:", "tel:", "data:")): continue
        parts = urlsplit(href)
        if parts.path.startswith("/"):
            dest = DIST / unquote(parts.path.lstrip("/"))
        else:
            dest = base / unquote(parts.path)
        dest = dest.resolve()
        assert dest == DIST.resolve() or DIST.resolve() in dest.parents, (path, href)
        assert dest.is_file() or (dest.is_dir() and (dest/"index.html").is_file()), (path, href)
        if parts.fragment and (dest/"index.html").is_file() if dest.is_dir() else False:
            target = dest/"index.html"
            assert 'id="' + parts.fragment + '"' in target.read_text(encoding="utf-8"), (path, href)

def main():
    for lang, home, classic, link_to_other, expected_classic in (
        ("en", "index.html", "legacy/index.html", "/ar/home/", "/legacy/"),
        ("ar", "ar/home/index.html", "ar/legacy/index.html", "/", "/ar/legacy/"),
    ):
        p, html = inspect(home)
        assert (p.lang, p.direction) == (lang, "rtl" if lang == "ar" else None), (home, p.lang, p.direction)
        assert "data-evidence-lens" in html and "data-evidence-journey" in html, home
        assert len(re.findall('class="stage-card"', html)) == 6, home
        assert len(re.findall("data-claim-panel=", html)) == 6, home
        assert len(re.findall("data-journey-step=", html)) == 6, home
        assert "CONCEPT V2 / NOT PRODUCTION" not in html and "نسخة تصورية V2" not in html
        assert "preview-strip" not in html, home
        assert "PayGod V2 visual exploration" not in html, home
        assert link_to_other in p.links and expected_classic in p.links, (home, p.links)
        assert "/verifier/" in p.links, home
        assert "/v2/use-cases/" in p.links if lang == "en" else "/v2/ar/use-cases/" in p.links
        assert p.alternates.get("en") == "https://paygod.net/", home
        assert p.alternates.get("ar") == "https://paygod.net/ar/home/", home
        if os.environ.get("VERCEL_ENV") == "production":
            assert p.robots == "index,follow", home
            assert p.canonicals == [("https://paygod.net/" if lang == "en" else "https://paygod.net/ar/home/")], home
        else:
            assert p.robots == "noindex,nofollow" and not p.canonicals, home
        assert "data-workspace=\"producer\"" not in html, "legacy technical demo must not be duplicated in new homepage"
        validate_local_links(home, p)

        archived, archived_html = inspect(classic)
        assert archived.lang == lang and archived.robots == "noindex,nofollow", classic
        assert not archived.canonicals, classic
        assert 'data-workspace="producer"' in archived_html, classic
        assert 'class="button secondary"' in archived_html, classic
        assert "verifier v0.4" in archived_html and "paygod-c14n-v1" in archived_html, classic
        if lang == "ar":
            assert archived.direction == "rtl"
            assert 'aria-label="English-language synthetic technical demo"' in archived_html
            assert "واجهة التجربة التقنية التفاعلية" in archived_html
        validate_local_links(classic, archived)
    assert (DIST/"verifier/index.html").is_file()
    assert (DIST/"downloads/paygod-verifier.html").is_file()
    assert (DIST/"v2/ar/index.html").is_file()

    # Original mobile nav is preserved on the archived original experience.
    style = (Path(__file__).resolve().parents[1] / "src/style.css").read_text(encoding="utf-8")
    hidden_rule = style.find("header nav{display:none}")
    visible_rule = style.rfind('body[data-workspace="producer"] header nav{')
    assert hidden_rule >= 0 and visible_rule > hidden_rule
    visible_block = style[visible_rule:style.find("}", visible_rule)]
    assert "display:flex" in visible_block and "order:3" in visible_block and "width:100%" in visible_block
    assert 'header nav a[href^="#"]' in style
    print("PASS: EN/AR V2 canonical home, real navigation, canonical SEO, six slides and lens")
    print("PASS: two archived classic synthetic workspaces, local links, unchanged verifier and mobile nav")

if __name__ == "__main__":
    main()
