#!/usr/bin/env python3
"""Static quality gate for PayGod bilingual Evidence Atlas.
No source, claims, verifier logic, or production settings are modified here.
"""
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "dist"


class PageAudit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.direction = None
        self.mains = 0
        self.navs = 0
        self.ids = []
        self.links = []
        self.noindex = False
        self.canonical = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
            self.direction = a.get("dir")
        if tag == "main":
            self.mains += 1
        if tag == "nav":
            self.navs += 1
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "meta" and a.get("name") == "robots":
            self.noindex = a.get("content") == "noindex,nofollow"
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical.append(a.get("href"))
        if tag == "a":
            self.links.append(a.get("href", ""))


def main():
    for name, expected_lang, direction, counterpart, relative in (
        ("explore/index.html", "en", "ltr", '<main class="ar"', "../ar/"),
        ("ar/index.html", "ar", "rtl", '<main class="en"', "../explore/"),
    ):
        path = PUBLIC / name
        assert path.is_file(), f"missing built page {path}"
        html = path.read_text(encoding="utf-8")
        audit = PageAudit()
        audit.feed(html)
        assert audit.lang == expected_lang and audit.direction == direction, (name, audit.lang, audit.direction)
        assert audit.mains == 1 and audit.navs == 1, (name, audit.mains, audit.navs)
        assert not (set(audit.ids) and len(set(audit.ids)) != len(audit.ids)), f"duplicate IDs: {name}"
        assert counterpart not in html, f"opposite-language body leaked into {name}"
        assert relative in audit.links, f"cross-language link missing: {name}"
        assert "../verifier/" in audit.links, f"verifier link missing: {name}"
        assert "0/10" in html and "v0.4" in html, f"canonical baseline missing: {name}"
        assert "WITHHELD" in html and "NOT RUN" in html, f"admission boundary missing: {name}"
        assert "paygod-c14n-v1" in html and "Ed25519" in html, f"verifier contract details missing: {name}"
        assert "https://github.com/hamadalmunyif/paygod-kernel-mvp" in html, f"Kernel source missing: {name}"
        for url in audit.links:
            if url.startswith("https://github.com/hamadalmunyif/"):
                assert url.startswith("https://github.com/hamadalmunyif/paygod-kernel-mvp"), f"noncanonical GitHub repository linked from {name}: {url}"
        assert "github.com/hamadalmunyif/paygod-workflow-observatory" not in html and "github.com/hamadalmunyif/agent-failure-taxonomy" not in html, f"experimental repository leaked to the site: {name}"
        assert "__TITLE__" not in html and "__LANG__" not in html and "__DESCRIPTION__" not in html, f"unrendered token: {name}"
        assert audit.noindex if "VERCEL_ENV" not in __import__("os").environ else True, f"unexpected preview indexing: {name}"
        print(f"PASS: {name} lang={audit.lang} dir={audit.direction}, 1 main, 1 nav, claims and links")

    for path in ("index.html", "verifier/index.html", "downloads/paygod-verifier.html"):
        assert (PUBLIC / path).is_file(), f"existing path disappeared: {path}"
    print("PASS: existing homepage, separate verifier and offline edition preserved")


if __name__ == "__main__":
    main()
