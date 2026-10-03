import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {verifyTransport,canonical,strictJsonParse,hash,parseIssuerTrustStore} from '../src/verifier.mjs';
import {createHash} from 'node:crypto';
import {sha256Fallback} from '../src/sha256.mjs';

const enc=new TextEncoder();
const sample=JSON.parse(readFileSync(new URL('../demo/sample.json',import.meta.url),'utf8'));
const demoTrust=JSON.parse(readFileSync(new URL('../demo/trusted-issuer-demo.json',import.meta.url),'utf8'));
const trustedIssuerKeys=parseIssuerTrustStore(demoTrust);
const clone=x=>structuredClone(x);

async function receiptSha(transport){return hash(transport.files['receipt.json']);}

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
 ['legacy canonicalization claim',x=>{let r=JSON.parse(x.files['receipt.json']);r.canonicalization.json='rfc8785';x.files['receipt.json']=JSON.stringify(r,null,2)+'\n';},'invalid']
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
assert.equal(clean.issuer_signature.reason,'no_trust_anchor_supplied');
assert.equal(clean.verification.replay,'not_performed');
assert.equal(clean.verification.time_authority,'producer_supplied');
assert.match(clean.receipt_sha256,/^[a-f0-9]{64}$/);
assert.match(clean.ledger_head,/^[a-f0-9]{64}$/);
console.log('Scoped v0.4 verification dimensions: PASS');

const trusted=await verifyTransport(sample,{trustedIssuerKeys});
assert.equal(trusted.status,'valid');
assert.equal(trusted.verification.integrity,'verified');
assert.equal(trusted.verification.issuer_authenticity,'verified');
assert.equal(trusted.issuer_signature.key_id,'paygod-demo-issuer-2026-10-03');
assert.equal(trusted.issuer_signature.key_trusted,true);
assert.equal(trusted.issuer_signature.signature_valid,true);
console.log('Detached Ed25519 + recipient trust store: VERIFIED');

const noSignature=clone(sample);
delete noSignature.files['receipt.sig.json'];
const unsigned=await verifyTransport(noSignature,{trustedIssuerKeys});
assert.equal(unsigned.status,'valid');
assert.equal(unsigned.verification.integrity,'verified');
assert.equal(unsigned.verification.issuer_authenticity,'not_verified');
assert.equal(unsigned.issuer_signature.reason,'signature_not_present');

const wrongTrust=parseIssuerTrustStore({
 profile:'paygod-ed25519-trust-v1',
 keys:[{
  key_id:'paygod-demo-issuer-2026-10-03',
  algorithm:'Ed25519',
  public_key_b64:Buffer.alloc(32,1).toString('base64')
 }]
});
const wrongKey=await verifyTransport(sample,{trustedIssuerKeys:wrongTrust});
assert.equal(wrongKey.status,'valid');
assert.equal(wrongKey.verification.integrity,'verified');
assert.equal(wrongKey.verification.issuer_authenticity,'failed');
assert.equal(wrongKey.issuer_signature.reason,'signature_invalid');

const receiptChanged=clone(sample);
receiptChanged.files['receipt.json']+=' ';
const receiptChangedResult=await verifyTransport(receiptChanged,{trustedIssuerKeys});
assert.equal(receiptChangedResult.status,'valid');
assert.equal(receiptChangedResult.verification.integrity,'verified');
assert.equal(receiptChangedResult.verification.issuer_authenticity,'failed');
assert.equal(receiptChangedResult.issuer_signature.reason,'receipt_commitment_mismatch');

const malformedSig=clone(sample);
const sig=JSON.parse(malformedSig.files['receipt.sig.json']);
sig.signature_b64='***';
malformedSig.files['receipt.sig.json']=JSON.stringify(sig,null,2)+'\n';
const malformedSigResult=await verifyTransport(malformedSig,{trustedIssuerKeys});
assert.equal(malformedSigResult.status,'valid');
assert.equal(malformedSigResult.verification.integrity,'verified');
assert.equal(malformedSigResult.verification.issuer_authenticity,'failed');
assert.match(malformedSigResult.issuer_signature.reason,/signature_envelope_invalid/);

const wrongKeyIdTrust=parseIssuerTrustStore({
 profile:'paygod-ed25519-trust-v1',
 keys:[{
  key_id:'different-demo-key',
  algorithm:'Ed25519',
  public_key_b64:demoTrust.keys[0].public_key_b64
 }]
});
const wrongKeyId=await verifyTransport(sample,{trustedIssuerKeys:wrongKeyIdTrust});
assert.equal(wrongKeyId.status,'valid');
assert.equal(wrongKeyId.verification.integrity,'verified');
assert.equal(wrongKeyId.verification.issuer_authenticity,'failed');
assert.equal(wrongKeyId.issuer_signature.reason,'key_id_not_in_trust_store');
console.log('Issuer-auth negative cases: PASS');

const rfcPublic=Uint8Array.from(Buffer.from('d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a','hex'));
const rfcSignature=Uint8Array.from(Buffer.from(
 'e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155'+
 '5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b','hex'
));
const rfcKey=await globalThis.crypto.subtle.importKey('raw',rfcPublic,{name:'Ed25519'},false,['verify']);
assert.equal(await globalThis.crypto.subtle.verify({name:'Ed25519'},rfcKey,rfcSignature,new Uint8Array()),true);
console.log('RFC 8032 vector 1: PASS');

const originalPin=await receiptSha(sample);
assert.equal((await verifyTransport(sample,{expectedReceiptSha256:originalPin})).status,'valid');
assert.equal((await verifyTransport(sample,{expectedReceiptSha256:'f'.repeat(64)})).status,'invalid');
console.log('External receipt commitment match/mismatch: PASS');

const rewritten=clone(sample);
const ledger=JSON.parse(rewritten.files['ledger.jsonl'].trim());
ledger.data.verdict='deny';
ledger.data.reason='coordinated rewrite test';
ledger.record_hash=await hash(canonical({previous_hash:ledger.previous_hash,timestamp:ledger.timestamp,data:ledger.data}));
rewritten.files['ledger.jsonl']=JSON.stringify(ledger)+'\n';

const manifest=JSON.parse(rewritten.files['manifest.json']);
for(const entry of manifest.files){
 const raw=rewritten.files[entry.name];
 entry.sha256=await hash(raw);
 entry.bytes=enc.encode(raw).length;
}
manifest.bundle.bundle_digest=await hash(manifest.files.map(x=>x.name+'='+x.sha256+'\n').sort().join(''));
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
assert.equal(rewrittenUnpinned.verification.issuer_authenticity,'failed');
const rewrittenPinned=await verifyTransport(rewritten,{expectedReceiptSha256:originalPin});
assert.equal(rewrittenPinned.status,'invalid','original external pin must reject coherent rewrite');
console.log('Coordinated rewrite + original receipt pin: PASS');

assert.equal(canonical({text:'e\u0301',arabic:'سلام'}),'{"arabic":"\\u0633\\u0644\\u0627\\u0645","text":"e\\u0301"}');
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
const offline=await verifyTransport(sample);
assert.equal(offline.status,'valid');
assert.equal(offline.verification.integrity,'verified');
assert.equal(offline.verification.issuer_authenticity,'not_verified');
Object.defineProperty(globalThis,'crypto',{value:saved,configurable:true});
console.log('Offline fallback integrity path: PASS');
