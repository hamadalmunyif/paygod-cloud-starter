const $ = id => document.getElementById(id);
const editor = $('bundle-editor');
const receiptPin = $('receipt-pin');
const trustInput = $('issuer-trust-store');
const trustStatus = $('issuer-trust-status');
let trustedIssuerKeys = {};
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

function setTrust(id, value) {
  const el = $(id);
  const label = String(value || 'not checked').replaceAll('_', ' ').toUpperCase();
  el.textContent = label;
  el.className =
    value === 'verified' ? 'passed' :
    value === 'failed' ? 'failed' :
    'unverified';
}

function issuerDetail(result) {
  const s = result?.issuer_signature;
  if (!s) return 'Not checked';
  const state = String(result.verification?.issuer_authenticity || 'not_verified').replaceAll('_', ' ').toUpperCase();
  const key = s.key_id ? ' · ' + s.key_id : '';
  const reason = s.reason ? ' · ' + s.reason : '';
  return state + key + reason;
}

function invalidate() {
  runId++; latest = null;
  $('status').textContent = 'NOT RUN'; $('status').className = 'status pending';
  $('result-title').textContent = editor.value.trim() ? 'Ready to verify the received bytes.' : 'Waiting for a bundle.';
  $('result-summary').textContent = 'Run verification to inspect integrity and the separate issuer-authentication boundary.';
  $('checks').replaceChildren(); $('error-detail').textContent = '';
  for (const id of ['digest', 'receipt-sha', 'ledger-head', 'manifest-sha']) $(id).textContent = 'Not calculated';
  $('issuer-signature').textContent = 'Not checked';
  setTrust('integrity-result', 'not_checked');
  setTrust('issuer-result', 'not_verified');
  setTrust('replay-result', 'not_performed');
  setTrust('time-result', 'not_checked');
  $('pin-result').textContent = receiptPin?.value.trim() ? 'NOT CHECKED' : 'NOT PROVIDED';
  $('pin-result').className = 'unverified';
  $('check-count').textContent = '0 checks'; $('download-result').disabled = true;
  $('transfer-state').textContent = ''; readSummary();
}

function setActive(kind) { for (const id of ['clean', 'tamper', 'receipt-tamper']) $(id)?.classList.toggle('active', id === kind); }

function load(kind = 'clean') {
  if (!SAMPLE) return;
  importId++;
  const t = structuredClone(SAMPLE);
  if (kind === 'tamper') t.files['measurement.json'] = t.files['measurement.json'].replace('420', '421');
  if (kind === 'receipt-tamper') {
    const receipt = JSON.parse(t.files['receipt.json']);
    receipt.verdict.value = 'allow';
    t.files['receipt.json'] = JSON.stringify(receipt, null, 2) + '\n';
  }
  editor.value = JSON.stringify(t, null, 2);
  if (receiptPin) receiptPin.value = '';
  invalidate();
  $('edit-state').textContent = kind === 'clean' ? 'SIGNED CLEAN SAMPLE' : kind === 'tamper' ? 'MEASUREMENT CHANGED' : 'DECISION CHANGED';
  $('file-label').textContent = 'Synthetic signed sample · ready to download'; setActive(kind);
}

function save(name, data, type = 'application/json') {
  const blob = new Blob([typeof data === 'string' ? data : JSON.stringify(data, null, 2) + '\n'], {type});
  const url = URL.createObjectURL(blob), a = document.createElement('a');
  a.href = url; a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(url), 5000);
}

for (const id of ['clean', 'tamper', 'receipt-tamper']) if ($(id)) $(id).onclick = () => load(id);
editor.oninput = () => {
  importId++; invalidate();
  $('edit-state').textContent = 'EDITED · REVERIFY';
  $('file-label').textContent = 'Edited in this workspace';
  setActive(null);
};
if (receiptPin) receiptPin.oninput = invalidate;

if (trustInput) {
  trustInput.onchange = async event => {
    trustedIssuerKeys = {};
    trustStatus.textContent = 'No trusted issuer keys loaded.';
    const file = event.target.files?.[0];
    if (!file) { invalidate(); return; }
    try {
      if (file.size > 200000) throw Error('Trust store too large.');
      const parsed = JSON.parse(await file.text());
      trustedIssuerKeys = parseIssuerTrustStore(parsed);
      const count = Object.keys(trustedIssuerKeys).length;
      trustStatus.textContent = count + ' trusted issuer key' + (count === 1 ? '' : 's') + ' loaded from ' + file.name + '.';
    } catch (error) {
      trustedIssuerKeys = {};
      trustStatus.textContent = 'Trust store rejected: ' + error.message;
    }
    invalidate();
  };
}

$('verify').onclick = async () => {
  const current = ++runId, source = editor.value;
  $('verify').disabled = true; $('verify').textContent = 'Checking…';
  let result;
  try {
    if (new TextEncoder().encode(source).length > 2000000) throw Error('Maximum bundle size is 2 MB.');
    result = await verifyTransport(JSON.parse(source), {
      expectedReceiptSha256: receiptPin?.value.trim() || null,
      trustedIssuerKeys
    });
  } catch (error) {
    result = {
      status: 'invalid',
      verification: {
        integrity: 'failed',
        issuer_authenticity: 'not_verified',
        replay: 'not_performed',
        time_authority: 'failed'
      },
      issuer_signature: null,
      checks: [],
      errors: [error.message],
      receipt_sha256: null,
      ledger_head: null,
      manifest_sha256: null,
      bundle_digest: null
    };
  }
  $('verify').disabled = !editor.value.trim(); $('verify').textContent = 'Run verification';
  if (current !== runId) return;
  latest = result;

  const integrityOk = result.verification?.integrity === 'verified';
  const issuerOk = result.verification?.issuer_authenticity === 'verified';
  $('status').textContent = integrityOk ? 'INTEGRITY VERIFIED' : 'INTEGRITY FAILED';
  $('status').className = 'status ' + (integrityOk ? 'valid' : 'invalid');
  $('result-title').textContent = integrityOk ? 'Bundle integrity verified.' : 'Bundle integrity failed.';
  $('result-summary').textContent = integrityOk
    ? issuerOk
      ? 'Integrity passed and the detached receipt signature verified under a recipient-supplied trusted Ed25519 key.'
      : 'The transferred bytes and declared decision bindings are internally consistent. Issuer authentication remains a separate result.'
    : 'One or more integrity checks failed. Inspect the errors before relying on the transferred package.';

  setTrust('integrity-result', result.verification?.integrity);
  setTrust('issuer-result', result.verification?.issuer_authenticity);
  setTrust('replay-result', result.verification?.replay);
  setTrust('time-result', result.verification?.time_authority);

  const pin = receiptPin?.value.trim() || '';
  const pinError = result.errors?.some(error => error.toLowerCase().includes('external receipt commitment'));
  $('pin-result').textContent = !pin ? 'NOT PROVIDED' : (!pinError && result.receipt_sha256 === pin ? 'MATCHED' : 'MISMATCH');
  $('pin-result').className = !pin ? 'unverified' : (!pinError && result.receipt_sha256 === pin ? 'passed' : 'failed');

  $('checks').replaceChildren();
  for (const check of result.checks || []) {
    const row = document.createElement('div'); row.className = 'check-row' + (check.ok ? '' : ' failed');
    const icon = document.createElement('span'), label = document.createElement('div');
    icon.textContent = check.ok ? '✓' : '×'; label.textContent = check.name;
    row.append(icon, label); $('checks').append(row);
  }

  $('check-count').textContent = (result.checks || []).filter(check => check.ok).length + '/' + (result.checks || []).length + ' passed';
  $('error-detail').textContent = (result.errors || []).join('\n');
  $('issuer-signature').textContent = issuerDetail(result);
  $('receipt-sha').textContent = result.receipt_sha256 || 'Not calculated';
  $('ledger-head').textContent = result.ledger_head || 'Not calculated';
  $('manifest-sha').textContent = result.manifest_sha256 || 'Not calculated';
  $('digest').textContent = result.bundle_digest || 'Not calculated';
  $('download-result').disabled = false;
};

$('download').onclick = () => {
  save('paygod-evidence-bundle.json', editor.value);
  $('transfer-state').textContent = 'Bundle download requested. Transfer this file separately from the recipient trust store.';
};
$('download-result').onclick = () => { if (latest) save('paygod-verification-result.json', latest); };

$('upload').onchange = async event => {
  const file = event.target.files[0]; if (!file) return;
  const current = ++importId;
  editor.value = ''; if (receiptPin) receiptPin.value = '';
  invalidate(); setActive(null); $('edit-state').textContent = 'READING FILE'; $('file-label').textContent = file.name;
  try {
    if (file.size > 2000000) throw Error('Import rejected: maximum size is 2 MB.');
    const text = await file.text(); if (current !== importId) return;
    editor.value = text; invalidate(); $('edit-state').textContent = 'IMPORTED · REVERIFY';
  } catch (error) {
    if (current === importId) {
      $('summary-error').textContent = error.message;
      $('edit-state').textContent = 'IMPORT REJECTED';
    }
  }
  event.target.value = '';
};

if (SAMPLE) load(); else invalidate();
