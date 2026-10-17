// Bounded parity probe using the canonical Kernel's pinned test vectors.
// DO NOT claim browser v0.5.1 full verifier parity from these 11 JSON cases.
// Source: hamadalmunyif/paygod-kernel-mvp
//        main@d347213848f03a6d25554631d0183a682879b11b
//        spec/test-vectors/canonical-json.json
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import assert from "node:assert/strict";
import { canonical, hash, strictJsonParse } from "../src/verifier.mjs";

const source = new URL("./fixtures/kernel-c14n-reference-20261014.json", import.meta.url);
const rawCorpus = readFileSync(source);
// Pin exact Git blob bytes from Kernel main@d347213: spec/test-vectors/canonical-json.json.
const gitBlob = createHash("sha1").update(`blob ${rawCorpus.byteLength}\0`).update(rawCorpus).digest("hex");
assert.equal(gitBlob, "3880d3a45b417ae95cae9a7b8cebb1c8c47722d8",
  "the frozen Kernel source corpus was silently changed");
const vectors = JSON.parse(rawCorpus.toString("utf8"));

assert.equal(vectors.length, 11, "expected the exact pinned canonical corpus length");
let accepted = 0;
let rejected = 0;

for (const vector of vectors) {
  if (Object.hasOwn(vector, "expected_error")) {
    assert.throws(() => canonical(vector.input), undefined,
      "expected rejection: " + vector.description);
    rejected += 1;
  } else {
    const actual = canonical(vector.input);
    assert.equal(actual, vector.expected_canonical,
      "canonical bytes differ: " + vector.description);
    assert.equal(await hash(actual), vector.expected_hash,
      "canonical SHA-256 differs: " + vector.description);
    accepted += 1;
  }
}

// JSON lexical semantics matter: JSON.parse followed by canonical() alone
// cannot recover whether the source number used a decimal or exponent.
// Inspect source text through the strict JSON parser first.
for (const raw of ['{"n":1.0}', '{"n":1e2}', '{"n":9007199254740992}']) {
  assert.throws(() => strictJsonParse(raw),
    undefined, "non-profile numeric input must fail closed: " + raw);
}

// This is deliberately a narrow shared-corpus witness; issuer trust,
// unexpected-file transport, receipt binding, replay and time authority
// require separate v0.5.1 contract-level cross-runtime comparison.
console.log("PASS: website verifier matched " + accepted + " canonical vectors, " +
            "rejected " + rejected + " canonical bad vectors and 3 lexical bad numbers");
