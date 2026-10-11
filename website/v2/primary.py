"""Promote approved V2 home to canonical roots without altering the original verifier.

A reversible HTML-only publication step:
  / and /ar/home/      approved V2 home
  /legacy/ /ar/legacy/ original pre-V2 landing, including its synthetic demo
  /verifier/            unchanged separate verifier
  /v2/                  preserved V2 route family
"""
from html import escape
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import re


def _legacy_html(html: str, original_path: str) -> str:
    """Rewrite links relative to the *original* home URL, not the archive path."""
    base = "https://paygod.net" + original_path

    def rewrite(match):
        href = match.group(1)
        if not href or href.startswith(("#", "/", "https://", "http://", "mailto:", "tel:", "data:", "javascript:")):
            return match.group(0)
        parsed = urlsplit(urljoin(base, href))
        new_href = parsed.path + (("?" + parsed.query) if parsed.query else "") + (("#" + parsed.fragment) if parsed.fragment else "")
        # The legacy producer demo historically had a ../downloads/ link which
        # resolves incorrectly from /ar/home/. Keep that genuine download usable.
        if new_href.startswith("/ar/downloads/"):
            new_href = new_href.replace("/ar/downloads/", "/downloads/", 1)
        return 'href="' + escape(new_href, quote=True) + '"'

    html = re.sub(r'\bhref="([^"]*)"', rewrite, html)
    html = re.sub(r'<link rel="canonical" href="[^"]*">', "", html)
    html = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex,nofollow">', html, count=1)
    return html


def promote_primary_home(dist: Path, production: bool) -> None:
    descriptions = {
        "en": "PayGod connects declared decisions and portable evidence with independently inspectable integrity and explicit limits of verification.",
        "ar": "PayGod يربط سياق القرار بالأدلة القابلة للنقل والفحص المستقل، مع حدود واضحة لسلامة الأدلة وصحة المصادر والسلطة.",
    }
    for lang, home, old_route, archive in (
        ("en", "index.html", "/", "legacy/index.html"),
        ("ar", "ar/home/index.html", "/ar/home/", "ar/legacy/index.html"),
    ):
        official = "https://paygod.net" + old_route
        current = dist / home
        assert current.is_file()
        old_html = current.read_text(encoding="utf-8")
        assert 'data-workspace="producer"' in old_html, "legacy producer workspace missing"
        archive_file = dist / archive
        archive_file.parent.mkdir(parents=True, exist_ok=True)
        archive_file.write_text(_legacy_html(old_html, old_route), encoding="utf-8")

        v2_path = dist / "v2" / ("ar/" if lang == "ar" else "") / "index.html"
        v2_html = v2_path.read_text(encoding="utf-8")
        assert 'data-evidence-lens' in v2_html and 'data-evidence-journey' in v2_html
        assert 'href="/verifier/"' in v2_html
        # The landing must not display the review/preview banner after adoption.
        v2_html, removed = re.subn(r'<div class="preview-strip">.*?</div>', '', v2_html, count=1, flags=re.S)
        assert removed == 1, "preview banner did not match"
        new_title = "PayGod — Portable Decision Evidence" if lang == "en" else "PayGod — أدلة قرارات قابلة للفحص المستقل"
        v2_html, title_count = re.subn(r'<title>.*?</title>', '<title>' + escape(new_title) + '</title>', v2_html, count=1)
        assert title_count == 1
        v2_html, description_count = re.subn(
            r'<meta name="description" content="[^"]*">',
            '<meta name="description" content="' + escape(descriptions[lang], quote=True) + '">',
            v2_html, count=1)
        assert description_count == 1
        # SEO alternate URLs must be absolute, while UI navigation stays local.
        for alternate_lang, target in (
            ("en", "https://paygod.net/"),
            ("ar", "https://paygod.net/ar/home/"),
        ):
            v2_html, count = re.subn(
                r'<link rel="alternate" hreflang="' + alternate_lang + r'" href="[^"]*">',
                '<link rel="alternate" hreflang="' + alternate_lang + '" href="' + target + '">',
                v2_html, count=1)
            assert count == 1, (lang, alternate_lang)
        if production:
            v2_html = v2_html.replace('<meta name="robots" content="noindex,nofollow">',
                '<meta name="robots" content="index,follow"><link rel="canonical" href="' + official + '">', 1)
        # Original archived template continues to be available from the footer.
        v2_html = v2_html.replace('PayGod <span>V2</span>', 'PayGod <span>Evidence</span>', 1)
        current.write_text(v2_html, encoding="utf-8")
        print(f'Promoted {home} as V2 homepage; archived original at {archive}')
