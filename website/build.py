from pathlib import Path
r=Path(__file__).parent
html=(r/'src/page.html').read_text().replace('/*STYLE*/',(r/'src/style.css').read_text())
js=(r/'src/sha256.mjs').read_text().replace('export ','')+'\n'+(r/'src/verifier.mjs').read_text().replace("import {sha256Fallback} from './sha256.mjs';",'').replace('export ','')+'\nconst SAMPLE='+ (r/'demo/sample.json').read_text()+';\n'+(r/'src/ui.js').read_text()
html=html.replace('/*SCRIPT*/',js)
(r/'dist').mkdir(exist_ok=True)
(r/'dist/index.html').write_text(html)
print('Built self-contained dist/index.html:',len(html.encode()),'bytes')
