import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {verifyTransport,canonical,strictJsonParse,hash,issuerSigningMessage} from '../src/verifier.mjs';
import {createHash,generateKeyPairSync,sign as nodeSign} from 'node:crypto';
import {sha256Fallback} from '../src/sha256.mjs';

const enc=new TextEncoder();
const sample=JSON.parse(readFileSync(new URL('../demo/sample.json',import.meta.url),'utf8'));
const clone=x=>structuredClone(x);

function rawEd25519PublicKey(publicKey){
 const spki=publicKey.export({type:'spki',format:'der'});
 return new Uint8Array(spki.subarray(spki.length-32));
}
function b64(value){return Buffer.from(value).toString('base64');}
async function receiptSha(transport){return hash(transport.files['receipt.json']);}
async function attachSignature(transport,keyPair,keyId='website-test-key'){
 const digest=await receiptSha(transport);
 const signature=nodeSign(null,Buffer.from(issuerSigningMessage(keyId,digest)),keyPair.privateKey);
 transport.files['receipt.sig.json']=JSON.stringify({
  profile:'paygod-ed25519-receipt-v1',
  algorithm:'Ed25519',
  key_id:keyId,
  receipt_sha256:digest,
  signature_b64:signature.toString('base64')
 },null,2)+'\n';
 return {[keyId]:b64(rawEd25519PublicKey(keyPair.publicKey))};
}

const baseCases=[
 ['clean',x=>{},'valid'],
 ['one-byte payload change',x=>x.files['measurement.json']=x.files['measurement.json'].replace('420','421'),'invalid'],
 ['receipt decision substitution',x=>{let r=JSON.parse(x.files['receipt.json']);r.verdict.value='allow';x.files['receipt.json']=JSON.stringify(r,null,2)+'\n';},'invalid'],
 ['missing locked ledger',x=>delete x.files['ledger.jsonl'],'invalid'],
 ['clock downgrade',x=>{let r=JSON.parse(x.files['receipt.json']);r.clock.value='unset';r.generated_at='unset';x.files['receipt.json']=JSON.stringify(r,null,2)+'\n';},'invalid'],
 ['malformed control',x=>x.files['manifest.json']='[]','invalid'],
 ['malformed receipt',x=>x.files['receipt.json']='null','invalid'],
 ['duplicate manifest file',x=>{let m=JSON.parse(x.files['manifest.json']);m.files.push(m.files[0]);x.files['manifest.json']=JSON.stringify(m,null,2)+'\n';},'invalid'],
 ['unexpected member',x=>x.files['extra.txt']='noise','invalid'],
 ['legacy canonicalization claim',x=>{let r=JSON.parse(x.files['receipt.json']);r.canonicalization.json='rfc8785';x.files['receipt.json']=JSON.stringify(r,null,2)+'\\n';},'invalid']
];

for(const [name,mutate,expected] of baseCases){
 const t=clone(sample);mutate(t);
 const r=await verifyTransport(t);
 assert.equal(r.status,expected,name);
 console.log(name+': '+r.status);
}

const clean=await verifyTransport(sample);
assert.equal(clean.verifier_version,'0.4.0');
assert.equal(clean.profile,'paygod-c14n-v1');
assert.equal(clean.verification.integrity,'verified');
assert.equal(clean.verification.issuer_authenticity,'not_verified');
assert.equal(clean.verification.replay,'not_performed');
assert.equal(clean.verification.time_authority,'producer_supplied');
assert.match(clean.receipt_sha256,/^[a-f0-9]{64}$/);
assert.match(clean.ledger_head,/^[a-f0-9]{64}$/);
console.log('Scoped v0.4 verification dimensions: PASS');

const signed=clone(sample);
const signer=generateKeyPairSync('ed25519');
const trustedIssuerKeys=await attachSignature(signed,signer);

const signedNoTrust=await verifyTransport(signed);
assert.equal(signedNoTrust.status,'valid');
assert.equal(signedNoTrust.verification.integrity,'verified');
assert.equal(signedNoTrust.verification.issuer_authenticity,'not_verified');
assert.equal(signedNoTrust.issuer_signature.reason,'no_trust_anchor_supplied');

const signedTrusted=await verifyTransport(signed,{trustedIssuerKeys});
assert.equal(signedTrusted.status,'valid');
assert.equal(signedTrusted.verification.integrity,'verified');
assert.equal(signedTrusted.verification.issuer_authenticity,'verified');
assert.equal(signedTrusted.issuer_signature.signature_valid,true);

const wrongSigner=generateKeyPairSync('ed25519');
const wrongTrust={'website-test-key':b64(rawEd25519PublicKey(wrongSigner.publicKey))};
const signedWrongKey=await verifyTransport(signed,{trustedIssuerKeys:wrongTrust});
assert.equal(signedWrongKey.status,'valid');
assert.equal(signedWrongKey.verification.integrity,'verified');
assert.equal(signedWrongKey.verification.issuer_authenticity,'failed');
assert.equal(signedWrongKey.issuer_signature.reason,'signature_invalid');

const signedReceiptChanged=clone(signed);
signedReceiptChanged.files['receipt.json']+=' ';
const receiptChanged=await verifyTransport(signedReceiptChanged,{trustedIssuerKeys});
assert.equal(receiptChanged.status,'valid');
assert.equal(receiptChanged.verification.integrity,'verified');
assert.equal(receiptChanged.verification.issuer_authenticity,'failed');
assert.equal(receiptChanged.issuer_signature.reason,'receipt_commitment_mismatch');
console.log('Detached Ed25519 issuer-auth trust boundary: PASS');

const originalPin=await receiptSha(sample);
assert.equal((await verifyTransport(sample,{expectedReceiptSha256:originalPin})).status,'valid');
assert.equal((await verifyTransport(sample,{expectedReceiptSha256:'f'.repeat(64)})).status,'invalid');
console.log('External receipt commitment match/mismatch: PASS');

const rewritten=clone(sample);
const ledger=JSON.parse(rewritten.files['ledger.jsonl'].trim());
ledger.data.verdict='deny';
ledger.data.reason='coordinated rewrite test';
ledger.record_hash=await hash(canonical({
 previous_hash:ledger.previous_hash,
 timestamp:ledger.timestamp,
 data:ledger.data
}));
rewritten.files['ledger.jsonl']=JSON.stringify(ledger)+'\n';

const manifest=JSON.parse(rewritten.files['manifest.json']);
for(const entry of manifest.files){
 const raw=rewritten.files[entry.name];
 entry.sha256=await hash(raw);
 entry.bytes=enc.encode(raw).length;
}
manifest.bundle.bundle_digest=await hash(
 manifest.files.map(x=>x.name+'='+x.sha256+'\n').sort().join('')
);
rewritten.files['manifest.json']=JSON.stringify(manifest,null,2)+'\n';

const receipt=JSON.parse(rewritten.files['receipt.json']);
receipt.bundle.files=manifest.files;
receipt.bundle.bundle_digest=manifest.bundle.bundle_digest;
receipt.bundle.manifest_sha256=await hash(rewritten.files['manifest.json']);
receipt.verdict.value='deny';
receipt.verdict.reason='coordinated rewrite test';
rewritten.files['receipt.json']=JSON.stringify(receipt,null,2)+'\n';

const rewrittenUnpinned=await verifyTransport(rewritten);
assert.equal(rewrittenUnpinned.status,'valid','coherent rewrite is internally consistent');
const rewrittenPinned=await verifyTransport(rewritten,{expectedReceiptSha256:originalPin});
assert.equal(rewrittenPinned.status,'invalid','original external pin must reject coherent rewrite');
console.log('Coordinated rewrite + original receipt pin: PASS');

assert.equal(
 canonical({text:'e\u0301',arabic:'سلام'}),
 '{"arabic":"\\u0633\\u0644\\u0627\\u0645","text":"e\\u0301"}'
);
assert.throws(()=>canonical({'e\u0301':'value'}),/NFC/);
assert.throws(()=>strictJsonParse('{"n":1.0}'),/Floating-point/);
assert.throws(()=>strictJsonParse('{"n":1e2}'),/Floating-point/);
assert.throws(()=>strictJsonParse('{"n":9007199254740992}'),/safe range/);
assert.equal(strictJsonParse('{"n":9007199254740991}').n,9007199254740991);
console.log('Unicode and lexical numeric profile: PASS');

for(const s of ['', 'abc','سلام','e\u0301','😀','a'.repeat(55),'a'.repeat(56),'a'.repeat(63),'a'.repeat(64),'a'.repeat(65),'a'.repeat(1000000)]){
 assert.equal(sha256Fallback(enc.encode(s)),createHash('sha256').update(s).digest('hex'));
}
console.log('Fallback SHA-256 against Node crypto: 11 vectors PASS');

const saved=globalThis.crypto;
Object.defineProperty(globalThis,'crypto',{value:undefined,configurable:true});
assert.equal((await verifyTransport(sample)).status,'valid');
Object.defineProperty(globalThis,'crypto',{value:saved,configurable:true});
console.log('Offline fallback end-to-end: PASS');
