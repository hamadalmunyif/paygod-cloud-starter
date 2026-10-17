import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {canonical,hash} from '../src/verifier.mjs';

const source=new URL('./fixtures/kernel-ledger-reference-20261017.json',import.meta.url);
const raw=readFileSync(source);

const gitBlob=createHash('sha1')
  .update(`blob ${raw.byteLength}\0`)
  .update(raw)
  .digest('hex');

assert.equal(
  gitBlob,
  'ac16a235641f22101dab93187af0eb992f010987',
  'the frozen Kernel ledger corpus was silently changed'
);

const vectors=JSON.parse(raw.toString('utf8'));
assert.equal(vectors.length,2,'expected exact Kernel ledger corpus length');

let previous='0'.repeat(64);
for(const [index,vector] of vectors.entries()){
  const actualCanonical=canonical(vector.input);
  assert.equal(
    actualCanonical,
    vector.expected_canonical,
    'ledger canonical bytes differ: '+vector.description
  );

  const actualHash=await hash(actualCanonical);
  assert.equal(
    actualHash,
    vector.expected_hash,
    'ledger record hash differs: '+vector.description
  );

  assert.equal(
    vector.input.previous_hash,
    previous,
    'ledger previous_hash does not chain to prior expected hash at vector '+index
  );

  previous=vector.expected_hash;
}

console.log(
  'PASS: website matched exact Kernel ledger corpus ('+
  vectors.length+' vectors), final head '+previous
);
