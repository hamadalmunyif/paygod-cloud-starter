import {readFileSync} from "node:fs";
import assert from "node:assert/strict";
import {verifyTransport} from "../src/verifier.mjs";

const sample = JSON.parse(readFileSync(new URL("../dist/lab/assets/sample.json", import.meta.url), "utf8"));
const original = JSON.parse(readFileSync(new URL("../demo/sample.json", import.meta.url), "utf8"));
assert.deepEqual(sample, original, "Evidence Lab must share the existing fixture, not mint another bundle");

const clean = await verifyTransport(structuredClone(sample), {trustedIssuerKeys:{}});
assert.equal(clean.status, "valid", "Intact synthetic transport");
assert.equal(clean.verification.integrity, "verified");
assert.equal(clean.verification.issuer_authenticity, "not_verified");

const mutated = structuredClone(sample);
const before = mutated.files["measurement.json"];
mutated.files["measurement.json"] = before.replace('"value": 420', '"value": 421');
assert.notEqual(mutated.files["measurement.json"], before, "Mutation must change the sample bytes");
const altered = await verifyTransport(mutated, {trustedIssuerKeys:{}});
assert.equal(altered.status, "invalid", "Modified evidence must fail closed");
assert.equal(altered.verification.integrity, "failed");
assert.ok((altered.checks || []).some(c => !c.ok), "Mutation should expose a named failed check");

// The CVE screen is expectation-only. Admission is separate and explicit.
// Against this single-fixture representation:
// score_x10=95, unfixed -> deny; 80 -> flag; 50 -> allow;
// marked fixed with independently confirmed installed version -> allow;
// incomplete source -> withheld before the Kernel is invoked.
function expectation(scoreX10, fixed, complete) {
  if (!complete) return "withheld";
  if (fixed || scoreX10 < 70) return "allow";
  return scoreX10 >= 90 ? "deny" : "flag";
}
assert.equal(expectation(95, false, true), "deny");
assert.equal(expectation(80, false, true), "flag");
assert.equal(expectation(50, false, true), "allow");
assert.equal(expectation(95, true, true), "allow");
assert.equal(expectation(95, false, false), "withheld");
console.log("PASS: intact synthetic sample VERIFIED; one changed measurement FAILED; CVE expectation boundary checked");
