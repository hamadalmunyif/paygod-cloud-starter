import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import {
  parseIssuerTrustStore,
  verifyTransport,
} from '../src/verifier.mjs';

const corpusPath=new URL('./fixtures/kernel-transport-parity-v1.json',import.meta.url);
const raw=readFileSync(corpusPath);
const blobSha=createHash('sha1')
  .update(`blob ${raw.byteLength}\0`)
  .update(raw)
  .digest('hex');

assert.equal(
  blobSha,
  'd3e682cb7f4f82cc88c4b8fd3ec7fb99d53357da',
  'frozen Kernel transport corpus bytes changed'
);

const corpus=JSON.parse(raw.toString('utf8'));
assert.equal(corpus.profile,'paygod-transport-parity-v1');
assert.equal(corpus.cases.length,10);

function materialize(name){
  const source=corpus.fixtures[name]?.files;
  assert.ok(source,'unknown fixture: '+name);
  return structuredClone(source);
}

for(const testCase of corpus.cases){
  const files=materialize(testCase.fixture);

  if(testCase.set_file){
    files[testCase.set_file.name]=testCase.set_file.content;
  }
  if(testCase.remove_file){
    delete files[testCase.remove_file];
  }

  const trustedIssuerKeys=testCase.trust_store
    ? parseIssuerTrustStore(corpus.trust_stores[testCase.trust_store])
    : {};

  const result=await verifyTransport(
    {format:corpus.transport_format,files},
    {
      expectedReceiptSha256:testCase.expected_receipt_sha256??null,
      trustedIssuerKeys,
    }
  );

  const expected=testCase.expected;
  assert.equal(result.status,expected.status,testCase.name+': status');
  assert.equal(
    result.verification.integrity,
    expected.integrity,
    testCase.name+': integrity'
  );

  for(const key of ['issuer_authenticity','replay','time_authority']){
    if(Object.hasOwn(expected,key)){
      assert.equal(
        result.verification[key],
        expected[key],
        testCase.name+': '+key
      );
    }
  }

  if(Object.hasOwn(expected,'issuer_reason')){
    assert.equal(
      result.issuer_signature?.reason,
      expected.issuer_reason,
      testCase.name+': issuer reason'
    );
  }

  for(const key of [
    'receipt_sha256',
    'manifest_sha256',
    'bundle_digest',
    'ledger_head',
  ]){
    if(Object.hasOwn(expected,key)){
      assert.equal(result[key],expected[key],testCase.name+': '+key);
    }
  }

  console.log('PASS:',testCase.name);
}

console.log(
  'PASS: website browser verifier consumed exact Kernel paygod-transport-parity-v1 corpus'
);
