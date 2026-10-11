#!/usr/bin/env python3
"""V2 bilingual preview route, link, and independent-verifier boundary checks."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
import re

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
            if part=="verifier/":
                assert a.iframes==["/verifier/"],a.iframes
                assert "original v0.4" in html if lang=="en" else "v0.4" in html
            if part=="":
                assert len(re.findall('class="stage-card"',html))==6
                assert len(re.findall("data-stage=",html))==6
                assert "/verifier/" in a.links
            count+=1
    print(f"PASS: {count} bilingual V2 preview pages, local targets, carousel, unchanged verifier link; robots noindex")

if __name__=="__main__":
    main()
