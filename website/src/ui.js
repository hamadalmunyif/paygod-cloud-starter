const $ = id => document.getElementById(id);
const editor = $('bundle-editor');
let latest = null, runId = 0, importId = 0;
function readSummary() {
  const hasInput = editor.value.trim().length > 0;
  $('verify').disabled = !hasInput;
  $('download').disabled = !hasInput;
  $('summary-error').textContent = '';
  $('summary-empty').hidden = hasInput;
  $('bundle-summary').hidden = true;
  if (!hasInput) return;
  try {
    if (new TextEncoder().encode(editor.value).length > 2000000) throw Error('Maximum bundle size is 2 MB.');
    const s = summarizeTransport(JSON.parse(editor.value));
    for (const key of ['measurement', 'metric', 'source', 'decision', 'rule', 'time']) $('summary-' + key).textContent = s[key];
    $('summary-files').textContent = s.files + ' files · ' + s.committed + ' committed artifacts';
    $('bundle-summary').hidden = false;
  } catch (error) { $('summary-error').textContent = 'Summary unavailable: ' + error.message; }
}
function invalidate() {
  runId++; latest = null;
  $('status').textContent = 'NOT RUN'; $('status').className = 'status pending';
  $('result-title').textContent = editor.value.trim() ? 'Ready to check the received bytes.' : 'Waiting for a bundle.';
  $('result-summary').textContent = 'Run verification to inspect file integrity and decision bindings.';
  $('checks').replaceChildren(); $('error-detail').textContent = ''; $('digest').textContent = 'Not calculated';
  for (const id of ['integrity-result', 'decision-result']) { $(id).textContent = 'Not checked'; $(id).className = ''; }
  $('check-count').textContent = '0 checks'; $('download-result').disabled = true;
  $('transfer-state').textContent = ''; readSummary();
}
function setActive(kind) { for (const id of ['clean', 'tamper', 'receipt-tamper']) $(id)?.classList.toggle('active', id === kind); }
function load(kind = 'clean') {
  if (!SAMPLE) return;
  importId++;
  const t = structuredClone(SAMPLE);
  if (kind === 'tamper') t.files['measurement.json'] = t.files['measurement.json'].replace('420', '421');
  if (kind === 'receipt-tamper') { const receipt = JSON.parse(t.files['receipt.json']); receipt.verdict.value = 'allow'; t.files['receipt.json'] = JSON.stringify(receipt, null, 2) + '\n'; }
  editor.value = JSON.stringify(t, null, 2); invalidate();
  $('edit-state').textContent = kind === 'clean' ? 'CLEAN SAMPLE' : kind === 'tamper' ? 'MEASUREMENT CHANGED' : 'DECISION CHANGED';
  $('file-label').textContent = 'Synthetic sample · ready to download'; setActive(kind);
}
function save(name, data, type = 'application/json') {
  const blob = new Blob([typeof data === 'string' ? data : JSON.stringify(data, null, 2) + '\n'], {type});
  const url = URL.createObjectURL(blob), a = document.createElement('a');
  a.href = url; a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(url), 5000);
}
for (const id of ['clean', 'tamper', 'receipt-tamper']) if ($(id)) $(id).onclick = () => load(id);
editor.oninput = () => { importId++; invalidate(); $('edit-state').textContent = 'EDITED · REVERIFY'; $('file-label').textContent = 'Edited in this workspace'; setActive(null); };
$('verify').onclick = async () => {
  const current = ++runId, bytes = editor.value;
  $('verify').disabled = true; $('verify').textContent = 'Checking…';
  let result;
  try { if (new TextEncoder().encode(bytes).length > 2000000) throw Error('Maximum bundle size is 2 MB.'); result = await verifyTransport(JSON.parse(bytes)); }
  catch (error) { result = {status: 'INVALID', checks: [], errors: [error.message], issuer_authenticated: false, external_fact_verified: false}; }
  $('verify').disabled = !editor.value.trim(); $('verify').textContent = 'Run verification';
  if (current !== runId) return;
  latest = result;
  const ok = result.status === 'VALID';
  $('status').textContent = result.status; $('status').className = 'status ' + (ok ? 'valid' : 'invalid');
  $('result-title').textContent = ok ? 'The supported checks passed.' : 'This bundle failed verification.';
  $('result-summary').textContent = ok ? 'The checked files and recorded decision are internally consistent. Source authenticity remains unverified.' : 'A file or binding could not be verified. Inspect the details before relying on this package.';
  const integrityChecks = result.checks.filter(check => check.name !== 'Decision binding');
  const integrityPassed = integrityChecks.length > 0 && integrityChecks.every(check => check.ok) && result.errors.every(error => error.startsWith('Decision binding:'));
  $('integrity-result').textContent = integrityPassed ? 'Passed' : 'Failed';
  $('integrity-result').className = integrityPassed ? 'passed' : 'failed';
  const decision = result.checks.find(check => check.name === 'Decision binding');
  const decisionDependencies = ['Contract', 'Artifact · ledger.jsonl', 'Manifest binding', 'Locked ledger', 'Ledger chain'];
  const decisionReady = decision && decisionDependencies.every(name => result.checks.some(check => check.name === name && check.ok));
  $('decision-result').textContent = !decisionReady ? 'Not established' : decision.ok ? 'Matched' : 'Mismatch';
  $('decision-result').className = decisionReady && decision.ok ? 'passed' : 'failed';
  $('checks').replaceChildren();
  for (const check of result.checks) {
    const row = document.createElement('div'); row.className = 'check-row' + (check.ok ? '' : ' failed');
    const icon = document.createElement('span'), label = document.createElement('div');
    icon.textContent = check.ok ? '✓' : '×'; label.textContent = check.name; row.append(icon, label); $('checks').append(row);
  }
  $('check-count').textContent = result.checks.filter(check => check.ok).length + '/' + result.checks.length + ' passed';
  $('error-detail').textContent = result.errors.join('\n'); $('digest').textContent = result.bundle_digest || 'Not calculated'; $('download-result').disabled = false;
};
$('download').onclick = () => { save('paygod-evidence-bundle.json', editor.value); $('transfer-state').textContent = 'Bundle download requested. Open the separate verifier and choose this file. The file—not a shared session—carries the evidence.'; };
$('download-result').onclick = () => { if (latest) save('paygod-verification-result.json', latest); };
$('upload').onchange = async event => {
  const file = event.target.files[0]; if (!file) return;
  const current = ++importId;
  editor.value = ''; invalidate(); setActive(null); $('edit-state').textContent = 'READING FILE'; $('file-label').textContent = file.name;
  try {
    if (file.size > 2000000) throw Error('Import rejected: maximum size is 2 MB.');
    const text = await file.text(); if (current !== importId) return;
    editor.value = text; invalidate(); $('edit-state').textContent = 'IMPORTED · REVERIFY';
  } catch (error) { if (current === importId) { $('summary-error').textContent = error.message; $('edit-state').textContent = 'IMPORT REJECTED'; } }
  event.target.value = '';
};
if (SAMPLE) load(); else invalidate();
