"""Negative and positive checks for synthetic-only demo contract."""
import unittest
from copy import deepcopy
from verify_journey_demo import check, make_sample

class DemoContractTests(unittest.TestCase):
    def test_all_scenarios(self):
        for scenario in ("clean", "tamper", "auth", "demo"):
            with self.subTest(scenario=scenario):
                ok, errors = check(make_sample(scenario))
                self.assertTrue(ok, errors)

    def test_tamper_fields(self):
        for field, value in (
            ("payload", "altered"), ("outcome", "INTEGRITY FAILED"),
            ("bundle_id", "DEMO-EVB-002"), ("scenario", "clean"),
            ("synthetic", False), ("executable", True),
            ("decision_sha256", "0" * 64), ("receipt_sha256", "f" * 64),
            ("evidence_sha256", "a" * 64), ("format", "unknown"),
        ):
            with self.subTest(field=field):
                record = deepcopy(make_sample("demo"))
                record[field] = value
                self.assertFalse(check(record)[0])

    def test_unknown_or_missing(self):
        record = make_sample("demo")
        record["extra"] = "x"
        self.assertFalse(check(record)[0])
        del record["extra"]
        del record["payload"]
        self.assertFalse(check(record)[0])

    def test_wrong_types(self):
        record = make_sample("demo")
        record["executable"] = 0
        self.assertFalse(check(record)[0])

if __name__ == "__main__":
    unittest.main()
