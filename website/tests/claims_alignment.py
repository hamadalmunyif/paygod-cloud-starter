#!/usr/bin/env python3
"""Check that every published editorial route points to ONE canonical claims register."""
from pathlib import Path
import re
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/"dist"
REGISTER="https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/CLAIMS_REGISTER.md"
ROUTES=[
    "index.html",
    "ar/home/index.html",
    "explore/index.html",
    "ar/index.html",
    "use-cases/index.html",
    "ar/use-cases/index.html",
]

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
    def handle_starttag(self, tag, attrs):
        if tag=="a":
            self.links.append(dict(attrs).get("href", ""))

def main():
    editorial = (ROOT/"CLAIMS_REGISTER_2026-10-10.md").read_text(encoding="utf-8")
    assert REGISTER in editorial
    assert "18" in editorial and "two skipped" in editorial, "must preserve exact pinned CI scope"
    assert "NOT" in editorial and "Observatory" in editorial

    for route in ROUTES:
        path=DIST/route
        assert path.is_file(), route
        content=path.read_text(encoding="utf-8")
        parsed=Links()
        parsed.feed(content)
        assert REGISTER in parsed.links, f"{route} missing auditable claims register"
        assert "paygod-workflow-observatory" not in content, f"second claimed software source leaked: {route}"
        assert "git_info_fail" not in content, f"deployment diagnostic leaked: {route}"
        assert "guarantee no" not in content.lower()
        assert "20-30%" not in content
        assert "meets SOC2/ISO" not in content
        assert len(re.findall(r'<main\b',content))==1, (route,"wrong main count")
        print("PASS claim-source link",route)

    cases=(DIST/"use-cases/index.html").read_text(encoding="utf-8")
    for item in ["ghg-scope-1-2-guard", "critical-cve-blocker", "iso27001-policy-review"]:
        assert item in cases
    assert "The current generic CLI run does not automatically" in cases or "does not enforce" in cases.lower()
    for route in ["verifier/index.html","downloads/paygod-verifier.html"]:
        assert (DIST/route).is_file(),route
    print("PASS: six editorial surfaces source-bound; verifier unaffected")

if __name__=="__main__":
    main()
