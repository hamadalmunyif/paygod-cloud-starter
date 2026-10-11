#!/usr/bin/env python3
"""Regression audit: archived V1 homepages remain functional after V2 cutover."""
from html.parser import HTMLParser
from pathlib import Path
import os

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
        self.canonical = []
        self.robots = None
        self.text = []
    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag == "html":
            self.lang, self.direction = attr.get("lang"), attr.get("dir")
        if tag == "main":
            self.mains += 1
        if tag == "nav":
            self.navs += 1
        if "id" in attr:
            if attr["id"] in self.ids:
                self.duplicates.add(attr["id"])
            self.ids.add(attr["id"])
        if tag == "a":
            self.links.append((attr.get("href",""), attr.get("lang"), attr.get("aria-label")))
        if tag == "link" and attr.get("rel") == "alternate":
            self.alternates[attr.get("hreflang")] = attr.get("href")
        if tag == "link" and attr.get("rel") == "canonical":
            self.canonical.append(attr.get("href"))
        if tag == "meta" and attr.get("name") == "robots":
            self.robots = attr.get("content")
    def handle_data(self, data):
        self.text.append(data)

def parse(path):
    page = (DIST / path)
    assert page.is_file(), path
    a = Audit()
    a.feed(page.read_text(encoding="utf-8"))
    assert a.mains == 1 and a.navs == 1, (path, a.mains, a.navs)
    assert not a.duplicates, (path, a.duplicates)
    return a

def main():
    eng = parse("v1/index.html")
    ar = parse("v1/ar/home/index.html")
    assert eng.lang == "en" and (eng.direction is None or eng.direction == "ltr")
    assert (ar.lang, ar.direction) == ("ar", "rtl")
    assert ("/v1/ar/home/", "ar", "الانتقال إلى الصفحة الرئيسية بالعربية") in eng.links
    assert ("/v1/", "en", "View English home page") in ar.links
    assert eng.alternates.get("ar") == ar.alternates.get("ar") == "https://paygod.net/ar/home/"
    assert eng.alternates.get("en") == ar.alternates.get("en") == "https://paygod.net/"
    assert all(x in ar.ids for x in ("main","capabilities","architecture","verifier","applications","pilot"))
    assert "أدلة قابلة للتحقق" in "".join(ar.text)
    assert "العربية" in "".join(eng.text)
    assert "paygod-workflow-observatory" not in (DIST / "v1/ar/home/index.html").read_text(encoding="utf-8")
    for path, a in (("index.html",eng),("ar/home/index.html",ar)):
        base = (DIST / path).parent
        for url, _, _ in a.links:
            if url.startswith("https://github.com/hamadalmunyif/"):
                assert url == KERNEL or url.startswith(KERNEL + "/"), url
            if not url or url.startswith(("https://","mailto:")):
                continue
            if url.startswith("#"):
                if len(url)>1:
                    assert url[1:] in a.ids, (path,url)
                continue
            if url.startswith("/"):
                dest = DIST / url.lstrip("/")
            else:
                dest = base / url.split("#",1)[0]
            dest = dest.resolve()
            assert DIST.resolve() in dest.parents or dest == DIST.resolve(), (path,url)
            assert dest.is_file() or (dest.is_dir() and (dest / "index.html").is_file()), (path,url)
    assert ("/use-cases/", None, "Explore three real PayGod Kernel policy Pack use cases") in eng.links
    assert ("/ar/use-cases/", None, "استعرض ثلاث حالات استخدام فعلية لحزم PayGod Kernel") in ar.links
    assert ("/ar/use-cases/", None, None) in ar.links
    assert ("/ar/", None, None) in ar.links
    assert ("/verifier/", None, None) in ar.links
    # Actual technical demo remains the same v0.4 engine; its UI is clearly
    # labeled English inside the Arabic editorial homepage.
    ar_html = (DIST / "v1/ar/home/index.html").read_text(encoding="utf-8")
    assert 'aria-label="English-language synthetic technical demo"' in ar_html
    assert 'verifier v0.4' in ar_html and 'paygod-c14n-v1' in ar_html
    assert "واجهة التجربة التقنية التفاعلية" in ar_html
    assert (DIST / "verifier/index.html").is_file()
    assert (DIST / "downloads/paygod-verifier.html").is_file()
    atlas = (DIST / "ar/index.html").read_text(encoding="utf-8")
    cases = (DIST / "ar/use-cases/index.html").read_text(encoding="utf-8")
    assert 'href="home/"' in atlas, "Arabic atlas brand must link to Arabic home"
    assert 'href="../ar/home/"' in atlas, "Arabic atlas nav must link to Arabic home"
    assert 'href="../../ar/home/"' in cases, "Arabic cases nav must link to Arabic home"
    assert 'href="../home/"' in cases, "Arabic cases brand must link to Arabic home"
    # Previous pages are archived and must not compete with the new canonical homepages.
    assert eng.canonical == ar.canonical == []
    assert eng.robots == ar.robots == "noindex,nofollow"
    if os.environ.get("VERCEL_ENV") == "production":
        sitemap = (DIST / "sitemap.xml").read_text(encoding="utf-8")
        assert "https://paygod.net/ar/home/" in sitemap
        assert "https://paygod.net/v1/" not in sitemap
    # Regression for real phone widths: an old max-width:760px rule suppressed
    # header nav entirely, making Use Cases and the language switch inaccessible.
    style = (Path(__file__).resolve().parents[1] / "src/style.css").read_text(encoding="utf-8")
    hidden_rule = style.find("header nav{display:none}")
    visible_rule = style.rfind('body[data-workspace="producer"] header nav{')
    assert hidden_rule >= 0 and visible_rule > hidden_rule, "mobile nav must override the old display:none"
    visible_block = style[visible_rule:style.find("}", visible_rule)]
    assert "display:flex" in visible_block, "producer mobile navigation must be visible"
    assert "order:3" in visible_block and "width:100%" in visible_block
    assert 'header nav a[href^="#"]' in style, "mobile may collapse section anchors, not route/locale links"
    for raw, label in ((DIST / "v1/index.html", "en"), (DIST / "v1/ar/home/index.html", "ar")):
        content = raw.read_text(encoding="utf-8")
        assert 'data-workspace="producer"' in content, label
        assert 'class="button secondary"' in content, label
    print("PASS: archived V1 phone navigation CSS, Use Cases links and locale links retained")
    print("PASS: archived original Arabic/English landing is accessible at /v1/, with source/verifier routes retained")

if __name__ == "__main__":
    main()
