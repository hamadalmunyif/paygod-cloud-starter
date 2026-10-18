from pathlib import Path
import json
import shutil
import os
import subprocess
import sys
import re

r = Path(__file__).parent
subprocess.run([sys.executable, str(r / 'demo' / 'generate.py')], check=True)
style = (r / 'src/style.css').read_text(encoding='utf-8')
core = (r / 'src/sha256.mjs').read_text(encoding='utf-8').replace('export ', '')
core += '\n' + (r / 'src/verifier.mjs').read_text(encoding='utf-8').replace("import {sha256Fallback} from './sha256.mjs';", '').replace('export ', '')
core += '\n' + (r / 'src/summary.mjs').read_text(encoding='utf-8').replace('export ', '')
ui = (r / 'src/ui.js').read_text(encoding='utf-8')
inspector = (r / 'src/inspector.html').read_text(encoding='utf-8')
sample = (r / 'demo/sample.json').read_text(encoding='utf-8')

def render_inspector(recipient=False):
    intro = '<div class="scenario"><span class="mono">RECEIVED EVIDENCE</span><h3>Open the package you received.</h3><p>The card shows what the files declare. Run verification to check their integrity and bindings.</p></div>' if recipient else '<div class="scenario"><span class="mono">SYNTHETIC INDUSTRIAL EXAMPLE</span><h3>One measurement. A review decision.</h3><p>The sample records 420 kWh against a fictional 400 kWh review threshold. The recorded decision is FLAG. This is a prepared fixture, not a live meter or policy execution.</p></div><div class="demo-buttons sample-controls"><button id="clean" class="small-button active">Load clean bundle</button><button id="tamper" class="small-button">Change the measurement</button><button id="receipt-tamper" class="small-button">Change the decision</button></div>'
    return inspector.replace('/*WORKSPACE_LABEL*/', 'RECIPIENT WORKSPACE' if recipient else 'PRODUCER WORKSPACE').replace('<!--INPUT_INTRO-->', intro)

def render(source, recipient=False, offline=False):
    html = (r / 'src' / source).read_text(encoding='utf-8')
    inspector_html = render_inspector(recipient)
    if source == 'home_ar.html':
        # The technical demo's controls and dynamic JS remain English; distinguish
        # this explicitly from the translated Arabic editorial landing page.
        inspector_html = '<div lang="en" dir="ltr" aria-label="English-language synthetic technical demo">' + inspector_html + '</div>'
    html = html.replace('/*STYLE*/', style).replace('<!--INSPECTOR-->', inspector_html)
    offline_link = '<p class="offline-ready">You have the self-contained HTML edition. Keep this file and open it again whenever you need it.</p>' if offline else '<a class="button secondary" href="../downloads/paygod-verifier.html" download>Download offline verifier</a>'
    html = html.replace('<!--OFFLINE_DOWNLOAD-->', offline_link)
    js = core + '\nconst SAMPLE = ' + ('null' if recipient else sample) + ';\n' + ui
    return html.replace('/*SCRIPT*/', js)

dist = r / 'dist'
for sub in ('verifier', 'downloads'):
    (dist / sub).mkdir(parents=True, exist_ok=True)
# Standalone, dependency-free Trust Factory prototype; no verifier/runtime mutation.
# The route is a simulation until wired to an independently verified result.
outputs = {
    'index.html': render('page.html'),
    'lab/index.html': (r / 'src/trust-factory.html').read_text(encoding='utf-8'),
    'ar/home/index.html': render('home_ar.html'),
    'verifier/index.html': render('standalone.html', True),
    'downloads/paygod-verifier.html': render('standalone.html', True, True),
}
# The evidence atlas is a separate editorial surface; the original verifier core and
# recipient workspace remain untouched. Language variants are static and SEO-addressable.
atlas_source = (r / 'src/atlas.html').read_text(encoding='utf-8')
for language, direction, title, description, output_path in (
    ('en', 'ltr', 'PayGod — Examine the Evidence',
     'Inspectable infrastructure: deterministic decision evidence, bounded tests, independent verification and documented limits.',
     'explore/index.html'),
    ('ar', 'rtl', 'PayGod — الأدلة والمنهج والمساهمة',
     'بنية مفتوحة للأدلة والقرارات الحتمية والتحقق المستقل، مع شواهد قابلة للفحص وحدود معلنة.',
     'ar/index.html'),
):
    page = (atlas_source
        .replace('__LANG__', language)
        .replace('__DIR__', direction)
        .replace('__TITLE__', title)
        .replace('__DESCRIPTION__', description))
    opposite = 'ar' if language == 'en' else 'en'
    # One main landmark and one locale navigation per generated page.
    page = re.sub(r'<nav class="' + opposite + r'"[^>]*>.*?</nav>', '', page, flags=re.S)
    page = re.sub(r'<main class="' + opposite + r'"[^>]*>.*?</main>', '', page, flags=re.S)
    if language == 'ar':
        page = page.replace('href="../" aria-label="PayGod home"', 'href="home/" aria-label="PayGod الصفحة الرئيسية"')
    outputs[output_path] = page

# One source, two static use-case routes. The page explains implemented Kernel
# Packs and synthetic fixtures; it does not execute packs in the browser.
case_source = (r / 'src/use-cases.html').read_text(encoding='utf-8')
atlas_css = atlas_source.split('<style>', 1)[1].split('</style>', 1)[0]
for language, direction, title, description, home_href, output_path in (
    ('en', 'ltr', 'PayGod — Architecture & Use Cases',
     'Three executable PayGod Kernel Packs: GHG Scope 1 and 2, critical CVE and ISO 27001 policy-review; exact proof boundaries.',
     '../', 'use-cases/index.html'),
    ('ar', 'rtl', 'PayGod — البنية وحالات الاستخدام',
     'ثلاث حزم فعلية في PayGod Kernel للانبعاثات والثغرات والحوكمة، مع شرح المدخلات والنتائج وحدود الإثبات.',
     '../home/', 'ar/use-cases/index.html'),
):
    case_page = (case_source
        .replace('__LANG__', language).replace('__DIR__', direction)
        .replace('__TITLE__', title).replace('__DESCRIPTION__', description)
        .replace('__HOME_HREF__', home_href)
        .replace('__ATLAS_CSS__', atlas_css))
    opposite = 'ar' if language == 'en' else 'en'
    case_page = re.sub(r'<nav class="' + opposite + r'"[^>]*>.*?</nav>', '', case_page, flags=re.S)
    case_page = re.sub(r'<main class="' + opposite + r'"[^>]*>.*?</main>', '', case_page, flags=re.S)
    outputs[output_path] = case_page

production = os.environ.get('VERCEL_ENV') == 'production'
if production:
    outputs['index.html'] = outputs['index.html'].replace('<meta name="robots" content="noindex,nofollow">', '<meta name="robots" content="index,follow"><link rel="canonical" href="https://paygod.net/">')
    outputs['ar/home/index.html'] = outputs['ar/home/index.html'].replace(
        '<meta name="robots" content="noindex,nofollow">',
        '<meta name="robots" content="index,follow"><link rel="canonical" href="https://paygod.net/ar/home/">')
    for atlas_path, canonical in (
        ('explore/index.html', 'https://paygod.net/explore/'),
        ('ar/index.html', 'https://paygod.net/ar/'),
    ):
        outputs[atlas_path] = outputs[atlas_path].replace(
            '<meta name="robots" content="noindex,nofollow">',
            f'<meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}">')
    for case_path, canonical in (
        ('use-cases/index.html', 'https://paygod.net/use-cases/'),
        ('ar/use-cases/index.html', 'https://paygod.net/ar/use-cases/'),
    ):
        outputs[case_path] = outputs[case_path].replace(
            '<meta name="robots" content="noindex,nofollow">',
            f'<meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}">')

(dist / 'robots.txt').write_text('User-agent: *\nDisallow: /verifier/\nDisallow: /downloads/\nSitemap: https://paygod.net/sitemap.xml\n' if production else 'User-agent: *\nDisallow: /\n', encoding='utf-8')
sitemap = dist / 'sitemap.xml'
if production:
    sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://paygod.net/</loc></url><url><loc>https://paygod.net/explore/</loc></url><url><loc>https://paygod.net/ar/</loc></url><url><loc>https://paygod.net/use-cases/</loc></url><url><loc>https://paygod.net/ar/use-cases/</loc></url><url><loc>https://paygod.net/ar/home/</loc></url><url><loc>https://paygod.net/developers/</loc></url><url><loc>https://paygod.net/ar/developers/</loc></url><url><loc>https://paygod.net/lab/</loc></url><url><loc>https://paygod.net/ar/lab/</loc></url></urlset>', encoding='utf-8')
else:
    sitemap.unlink(missing_ok=True)
for path, html in outputs.items():
    target = dist / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding='utf-8')
    print(f'Built {path}: {len(html.encode())} bytes')
shutil.copyfile(r / 'PILOT_BRIEF.md', dist / 'downloads/paygod-pilot-brief.md')
shutil.copyfile(r / 'demo' / 'trusted-issuer-demo.json', dist / 'downloads' / 'paygod-demo-trust-store.json')

# V2 builds source-linked preview routes under /v2/ and promotes its bilingual home onto the canonical home routes; the original homepage is archived under /v1/.
from v2.site import build_v2
build_v2(dist)

# Preserve the isolated Living Machinery preview: V2 generates /lab/ too,
# so publish this explicit experimental route only after the V2 build.
# Do not replace V2's canonical Evidence Lab in production.
if not production:
    machine_route = dist / 'machinery' / 'index.html'
    machine_route.parent.mkdir(parents=True, exist_ok=True)
    machine_route.write_text((r / 'src/trust-factory.html').read_text(encoding='utf-8'), encoding='utf-8')
    authority_route = dist / 'authority-gate' / 'index.html'
    authority_route.parent.mkdir(parents=True, exist_ok=True)
    authority_route.write_text((r / 'src/authority-gate.html').read_text(encoding='utf-8'), encoding='utf-8')
    journey_route = dist / 'journey' / 'index.html'
    journey_route.parent.mkdir(parents=True, exist_ok=True)
    journey_route.write_text((r / 'src/evidence-journey.html').read_text(encoding='utf-8'), encoding='utf-8')

# Publish a bounded, non-secret source identity so release smoke can prove that
# the live Vercel build corresponds to the exact Git SHA that triggered release CI.
source_sha = os.environ.get("VERCEL_GIT_COMMIT_SHA") or os.environ.get("GITHUB_SHA") or "unknown"
source_kind = (
    "vercel:VERCEL_GIT_COMMIT_SHA"
    if os.environ.get("VERCEL_GIT_COMMIT_SHA")
    else "github:GITHUB_SHA"
    if os.environ.get("GITHUB_SHA")
    else "unknown"
)
meta_dir = dist / "meta"
meta_dir.mkdir(parents=True, exist_ok=True)
(meta_dir / "deployment-source.json").write_text(
    json.dumps(
        {
            "profile": "paygod-deployment-source-v1",
            "git_sha": source_sha,
            "source": source_kind,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    + "\n",
    encoding="utf-8",
)

