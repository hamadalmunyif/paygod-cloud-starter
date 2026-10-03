from pathlib import Path
import shutil
import os
import subprocess
import sys

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
    html = html.replace('/*STYLE*/', style).replace('<!--INSPECTOR-->', render_inspector(recipient))
    offline_link = '<p class="offline-ready">You have the self-contained HTML edition. Keep this file and open it again whenever you need it.</p>' if offline else '<a class="button secondary" href="../downloads/paygod-verifier.html" download>Download offline verifier</a>'
    html = html.replace('<!--OFFLINE_DOWNLOAD-->', offline_link)
    js = core + '\nconst SAMPLE = ' + ('null' if recipient else sample) + ';\n' + ui
    return html.replace('/*SCRIPT*/', js)

dist = r / 'dist'
for sub in ('verifier', 'downloads'):
    (dist / sub).mkdir(parents=True, exist_ok=True)
outputs = {'index.html': render('page.html'), 'verifier/index.html': render('standalone.html', True), 'downloads/paygod-verifier.html': render('standalone.html', True, True)}
production = os.environ.get('VERCEL_ENV') == 'production'
if production:
    outputs['index.html'] = outputs['index.html'].replace('<meta name="robots" content="noindex,nofollow">', '<meta name="robots" content="index,follow"><link rel="canonical" href="https://paygod.net/">')
(dist / 'robots.txt').write_text('User-agent: *\nDisallow: /verifier/\nDisallow: /downloads/\nSitemap: https://paygod.net/sitemap.xml\n' if production else 'User-agent: *\nDisallow: /\n', encoding='utf-8')
sitemap = dist / 'sitemap.xml'
if production:
    sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://paygod.net/</loc></url></urlset>', encoding='utf-8')
else:
    sitemap.unlink(missing_ok=True)
for path, html in outputs.items():
    (dist / path).write_text(html, encoding='utf-8')
    print(f'Built {path}: {len(html.encode())} bytes')
shutil.copyfile(r / 'PILOT_BRIEF.md', dist / 'downloads/paygod-pilot-brief.md')
shutil.copyfile(r / 'demo' / 'trusted-issuer-demo.json', dist / 'downloads' / 'paygod-demo-trust-store.json')
