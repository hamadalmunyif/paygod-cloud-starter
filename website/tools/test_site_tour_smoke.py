"""Static full-site tour smoke checks: links, preview isolation, bilingual content."""
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'src/site-tour.html').read_text(encoding='utf-8')
BUILD=(ROOT/'build.py').read_text(encoding='utf-8')
ROUTES={
    '/':'index.html',
    '/explore/':'explore/index.html',
    '/use-cases/':'use-cases/index.html',
    '/developers/':'developers/index.html',
    '/journey/':'journey/index.html',
    '/machinery/':'machinery/index.html',
    '/authority-gate/':'authority-gate/index.html',
    '/journey-check/':'journey-check/index.html',
    '/verifier/':'verifier/index.html',
    '/lab/':'lab/index.html',
    '/ar/home/':'ar/home/index.html',
    '/ar/':'ar/index.html',
    '/ar/use-cases/':'ar/use-cases/index.html',
    '/ar/developers/':'ar/developers/index.html',
}
class SiteTourSmoke(unittest.TestCase):
    def test_all_expected_links_present(self):
        hrefs=set(re.findall(r'href="([^"]+)"',HTML))
        self.assertFalse(set(ROUTES)-hrefs)
    def test_bilingual_content_and_accessibility(self):
        self.assertIn('lang="ar"',HTML)
        self.assertIn('dir="rtl"',HTML)
        self.assertIn('data-ar=',HTML)
        self.assertIn('data-en=',HTML)
        self.assertIn('prefers-reduced-motion',HTML)
        self.assertIn(':focus-visible',HTML)
    def test_preview_only_build(self):
        marker="tour_route = dist / 'site-tour' / 'index.html'"
        self.assertIn(marker,BUILD)
        self.assertIn('if not production:',BUILD[:BUILD.index(marker)])
        self.assertIn('noindex,nofollow',HTML)
    def test_links_are_local_and_expected(self):
        for href in re.findall(r'href="([^"]+)"',HTML):
            if href.startswith('/'):
                self.assertIn(href,ROUTES)
    def test_dist_routes_after_build_if_available(self):
        dist=ROOT/'dist'
        if not dist.exists():
            self.skipTest('Run python3 website/build.py first for generated-route checks')
        for route,path in ROUTES.items():
            with self.subTest(route=route):
                self.assertTrue((dist/path).is_file(),f'Missing generated route: {route}')

if __name__=='__main__':
    unittest.main()
