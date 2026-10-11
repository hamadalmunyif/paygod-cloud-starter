#!/usr/bin/env python3
"""V2 bilingual preview route, link, and independent-verifier boundary checks."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
import re
import json
import os

DIST = Path(__file__).resolve().parents[1] / "dist"
ROUTES = ("", "how-it-works/", "use-cases/", "atlas/", "verifier/")

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.language = None
        self.direction = None
        self.mains = 0
        self.navs = 0
        self.robots = None
        self.ids = set()
        self.duplicate = set()
        self.iframes = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.language = a.get("lang")
            self.direction = a.get("dir")
        if tag == "main": self.mains += 1
        if tag == "nav": self.navs += 1
        if tag == "a": self.links.append(a.get("href", ""))
        if tag == "iframe": self.iframes.append(a.get("src", ""))
        if tag == "meta" and a.get("name") == "robots": self.robots = a.get("content")
        if a.get("id"):
            if a["id"] in self.ids: self.duplicate.add(a["id"])
            self.ids.add(a["id"])

def main():
    assert (DIST/"v2/assets/style.css").is_file()
    js = (DIST/"v2/assets/interactions.js").read_text()
    assert "scrollIntoView" in js and "data-next" in js
    assert "dragstart" in js and "event.preventDefault()" in js
    assert "paygod:stage" in js
    lens_js = (DIST/"v2/assets/lens.js").read_text()
    assert "data-lens-toggle" in lens_js and "data-journey-pack" in lens_js
    assert "tools/verify_portable_evidence.py" in (Path(__file__).resolve().parents[1]/"v2/lens.py").read_text()
    assert "/verifier/" in (DIST/"verifier/index.html").as_posix()
    count=0
    for lang in ("en","ar"):
        prefix="v2/" + ("ar/" if lang=="ar" else "")
        for part in ROUTES:
            file=DIST/prefix/part/"index.html"
            assert file.is_file(), file
            html=file.read_text(encoding="utf-8")
            a=Inspect(); a.feed(html)
            assert (a.language,a.direction)==(lang,"rtl" if lang=="ar" else "ltr"), file
            assert a.mains==1 and a.navs==1, (file,a.mains,a.navs)
            assert not a.duplicate, (file,a.duplicate)
            assert a.robots=="noindex,nofollow", file
            assert "/v2/assets/style.css" in html and "/v2/assets/interactions.js" in html
            assert "/v2/assets/lens.css" in html and "/v2/assets/lens.js" in html
            raw = re.search(r'<script type="application/json" id="v2-lens-translations">(.+?)</script>', html)
            assert raw, file
            labels = json.loads(raw.group(1))
            assert len(labels["en"]["stageNotes"]) == len(labels["ar"]["stageNotes"]) == 6
            assert 'PayGod' in html
            assert "paygod-workflow-observatory" not in html
            for link in a.links:
                if link.startswith(("https://", "mailto:","#")): continue
                assert link.startswith("/"),(file,link)
                path=unquote(link.split("#",1)[0].split("?",1)[0])
                target=(DIST/path.lstrip("/")).resolve()
                assert target==DIST.resolve() or DIST.resolve() in target.parents,link
                assert target.is_file() or (target.is_dir() and (target/"index.html").is_file()),(file,link)
                fragment=link.partition("#")[2]
                if fragment and target.is_dir():
                    target_html=(target/"index.html").read_text(encoding="utf-8")
                    assert 'id="'+fragment+'"' in target_html,(file,link)
            if part in ("", "atlas/"):
                assert 'id="evidence-lens"' in html, file
                assert len(re.findall("data-claim-panel=",html)) == 6
                assert "docs/CLAIMS_REGISTER.md" in html
                assert "docs/STANDALONE_VERIFIER.md" in html
                assert "docs/REPOSITORY_BOUNDARY.md" in html
                assert "tests/cases.yaml" in html
                assert "NOT ESTABLISHED" in html if lang=="en" else "ما لا يثبته ذلك" in html
            if part in ("", "how-it-works/"):
                assert 'id="source-journey"' in html, file
                assert len(re.findall("data-journey-step=",html)) == 6
                assert len(re.findall("data-journey-pack=",html)) == 3
                assert "The final verifier" in html if lang=="en" else "المحقق النهائي" in html
            if part=="verifier/":
                assert a.iframes==["/verifier/"],a.iframes
                assert "original v0.4" in html if lang=="en" else "v0.4" in html
            if part=="":
                assert len(re.findall('class="stage-card"',html))==6
                assert len(re.findall("data-stage=",html))==6
                assert "/verifier/" in a.links
            count+=1
    # Production landing should use the same V2 source and keep V1 available for rollback.
    for lang, home, archived in (
        ("en", "index.html", "v1/index.html"),
        ("ar", "ar/home/index.html", "v1/ar/home/index.html"),
    ):
        file = DIST / home
        old = DIST / archived
        assert file.is_file() and old.is_file(), (file, old)
        html = file.read_text(encoding="utf-8")
        old_html = old.read_text(encoding="utf-8")
        audit = Inspect(); audit.feed(html)
        old_audit = Inspect(); old_audit.feed(old_html)
        assert audit.language == lang and audit.direction == ("rtl" if lang=="ar" else "ltr")
        assert audit.navs == audit.mains == 1
        assert not audit.duplicate
        assert old_audit.navs == old_audit.mains == 1
        assert old_audit.robots == "noindex,nofollow"
        assert "rel=\"canonical\"" not in old_html, archived
        assert 'id="evidence-lens"' in html
        assert 'id="source-journey"' in html
        assert len(re.findall('class="stage-card"', html)) == 6
        assert 'href="/v2/use-cases/"' in html
        assert 'href="/verifier/"' in html
        assert 'href="/v1/' in html
        assert "paygod-workflow-observatory" not in html
        assert 'href="https://paygod.net/"' in html
        assert 'href="https://paygod.net/ar/home/"' in html
        assert (("Evidence beyond" in old_html) if lang=="en" else ("أدلة قابلة للتحقق" in old_html))
        for route in ("/v2/assets/style.css", "/v2/assets/lens.css", "/v2/assets/interactions.js", "/v2/assets/lens.js"):
            assert route in html
            assert (DIST/route.lstrip("/")).is_file()
        for href in audit.links:
            if not href.startswith("/"):
                continue
            target = (DIST/href.lstrip("/").split("#",1)[0]).resolve()
            assert DIST.resolve() == target or DIST.resolve() in target.parents, href
            assert target.is_file() or (target.is_dir() and (target/"index.html").is_file()), (home,href)
        if os.environ.get("VERCEL_ENV") == "production":
            assert audit.robots == "index,follow", (home,audit.robots)
            canonical = "https://paygod.net/ar/home/" if lang=="ar" else "https://paygod.net/"
            assert '<link rel="canonical" href="'+canonical+'">' in html
        else:
            assert audit.robots == "noindex,nofollow", (home,audit.robots)
            assert 'rel="canonical"' not in html
    print("PASS: promoted bilingual V2 home, canonical/preview safety, archived V1 rollback, local links and verifier")
    print(f"PASS: {count} bilingual V2 pages, carousel, three Pack source tracks, claim-to-proof lens, unchanged verifier, preview noindex")

if __name__=="__main__":
    main()
