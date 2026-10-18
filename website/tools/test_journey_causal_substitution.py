"""Causal substitution experiments for the synthetic demo chain.

A chain can be self-consistent but unauthenticated. These tests prove only
that partial substitutions are rejected, not that a real issuer is authorized.
"""
import unittest
from copy import deepcopy
from verify_journey_demo import check, make_sample, digest, encode

class CausalSubstitutionTests(unittest.TestCase):
    def test_swap_evidence_from_other_scenario(self):
        original = make_sample("demo")
        altered = make_sample("tamper")
        original["payload"] = altered["payload"]
        original["evidence_sha256"] = altered["evidence_sha256"]
        ok, errors = check(original)
        self.assertFalse(ok)
        self.assertTrue(any("payload" in e or "decision_sha256" in e for e in errors))

    def test_swap_decision_from_other_scenario(self):
        original = make_sample("demo")
        other = make_sample("clean")
        original["decision_sha256"] = other["decision_sha256"]
        ok, errors = check(original)
        self.assertFalse(ok)
        self.assertTrue(any("decision_sha256" in e for e in errors))

    def test_swap_receipt_from_other_scenario(self):
        original = make_sample("demo")
        original["receipt_sha256"] = make_sample("clean")["receipt_sha256"]
        ok, errors = check(original)
        self.assertFalse(ok)
        self.assertTrue(any("receipt_sha256" in e for e in errors))

    def test_swap_outcome_and_rehash_decision_and_receipt(self):
        original = make_sample("demo")
        original["outcome"] = "AUTHORITY NOT ESTABLISHED"
        e = original["evidence_sha256"]
        d = digest(encode(["paygod-demo-decision-v1", original["bundle_id"], e,
                           original["scenario"], original["outcome"], "synthetic-only"]))
        original["decision_sha256"] = d
        original["receipt_sha256"] = digest(encode([
            "paygod-demo-receipt-v1", original["bundle_id"], e, d,
            original["outcome"], "not-signed"]))
        ok, errors = check(original)
        self.assertFalse(ok)
        self.assertTrue(any("outcome" in e for e in errors))

    def test_rehash_full_chain_is_not_authenticity_proof(self):
        record = make_sample("demo")
        self.assertTrue(check(record)[0])
        # The fixture and hashing rules are public: any party can generate a
        # fully consistent chain. This success is NOT issuer authentication.
        forged = deepcopy(record)
        forged["evidence_sha256"] = digest(forged["payload"])
        forged["decision_sha256"] = digest(encode([
            "paygod-demo-decision-v1", forged["bundle_id"],
            forged["evidence_sha256"], forged["scenario"],
            forged["outcome"], "synthetic-only"]))
        forged["receipt_sha256"] = digest(encode([
            "paygod-demo-receipt-v1", forged["bundle_id"],
            forged["evidence_sha256"], forged["decision_sha256"],
            forged["outcome"], "not-signed"]))
        self.assertTrue(check(forged)[0])

if __name__ == "__main__":
    unittest.main()
