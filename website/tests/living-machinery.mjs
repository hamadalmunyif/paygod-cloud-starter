import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {join} from 'node:path';

// Static contract checks: intentionally do not claim browser E2E coverage.
const source=readFileSync(new URL('../src/trust-factory.html',import.meta.url),'utf8');
const config=JSON.parse(readFileSync(new URL('../vercel.json',import.meta.url),'utf8'));
const build=readFileSync(new URL('../build.py',import.meta.url),'utf8');
assert.match(build,/['"]lab\/index\.html['"]:\s*\(r\s*\/\s*['"]src\/trust-factory\.html['"]\)/);
for(const id of ['language','scenario','run','reset','machine','meter','output','status']){
  assert.match(source,new RegExp('id="'+id+'"'));
}
for(const caseName of ['clean','tamper','key','rewrite']){
  assert.match(source,new RegExp('value="'+caseName+'"'));
}
assert.match(source,/prefers-reduced-motion:reduce/);
assert.match(source,/document\.documentElement\.dir/);
assert.match(source,/textContent/);
assert.match(source,/NO SIGNED WARRANT|NOT A SIGNED WARRANT/);
assert.match(source,/No Kernel or Verifier call/);
assert.doesNotMatch(source,/<script[^>]+src=/);
assert.doesNotMatch(source,/fetch\s*\(|XMLHttpRequest|sendBeacon|localStorage|sessionStorage/);
const lab=config.headers.find(h=>h.source==='/lab/:path*');
assert.ok(lab,'Lab should have isolated preview headers');
assert.ok(lab.headers.some(h=>h.key==='X-Robots-Tag'&&h.value==='noindex, nofollow'));
console.log('Living Machinery static route, boundaries, privacy and accessibility contracts: PASS');
