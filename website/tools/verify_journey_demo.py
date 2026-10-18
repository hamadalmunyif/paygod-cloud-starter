#!/usr/bin/env python3
"""Independent verifier for the SYNTHETIC PayGod Journey demo only."""
import hashlib
import json
import sys
from pathlib import Path

FIXTURE = "PayGod demo payload | bundle DEMO-EVB-001 | amount_minor=1000 | policy=demo-v1"
OUTCOMES = {
    "clean": "AUTHORITY NOT ESTABLISHED",
    "tamper": "INTEGRITY FAILED",
    "auth": "ISSUER TRUST NOT ESTABLISHED",
    "demo": "SIMULATED ALLOW",
}
FIELDS = {
    "format", "bundle_id", "payload", "baseline_payload", "scenario", "outcome",
    "evidence_sha256", "decision_sha256", "receipt_sha256", "synthetic", "executable",
}

def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def encode(fields: list[str]) -> str:
    if not all(isinstance(x, str) and x.isascii() for x in fields):
        raise ValueError("v1 accepts ASCII-only preimage fields")
    return "|".join(f"{len(value)}:{value}" for value in fields)

def check(record: object) -> tuple[bool, list[str]]:
    errors = []
    if not isinstance(record, dict) or set(record) != FIELDS:
        return False, ["schema: required fields or unknown fields"]
    scenario = record["scenario"]
    if not isinstance(scenario, str) or scenario not in OUTCOMES:
        return False, ["scenario: invalid"]
    expected_payload = FIXTURE + (" | altered" if scenario == "tamper" else "")
    fixed = {
        "format": "paygod-journey-demo-v1",
        "bundle_id": "DEMO-EVB-001",
        "baseline_payload": FIXTURE,
        "payload": expected_payload,
        "outcome": OUTCOMES[scenario],
        "synthetic": True,
        "executable": False,
    }
    for field, expected in fixed.items():
        if type(record[field]) is not type(expected) or record[field] != expected:
            errors.append(f"{field}: unexpected value")
    for field in ("evidence_sha256", "decision_sha256", "receipt_sha256"):
        value = record[field]
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            errors.append(f"{field}: invalid lowercase sha256")
    if errors:
        return False, errors
    evidence = digest(record["payload"])
    decision = digest(encode([
        "paygod-demo-decision-v1", record["bundle_id"], evidence,
        scenario, record["outcome"], "synthetic-only",
    ]))
    receipt = digest(encode([
        "paygod-demo-receipt-v1", record["bundle_id"], evidence,
        decision, record["outcome"], "not-signed",
    ]))
    for field, expected in (
        ("evidence_sha256", evidence),
        ("decision_sha256", decision),
        ("receipt_sha256", receipt),
    ):
        if record[field] != expected:
            errors.append(f"{field}: mismatch")
    return not errors, errors

def make_sample(scenario: str) -> dict:
    if scenario not in OUTCOMES:
        raise ValueError("invalid scenario")
    payload = FIXTURE + (" | altered" if scenario == "tamper" else "")
    outcome = OUTCOMES[scenario]
    evidence = digest(payload)
    decision = digest(encode([
        "paygod-demo-decision-v1", "DEMO-EVB-001", evidence, scenario, outcome, "synthetic-only"
    ]))
    receipt = digest(encode([
        "paygod-demo-receipt-v1", "DEMO-EVB-001", evidence, decision, outcome, "not-signed"
    ]))
    return dict(format="paygod-journey-demo-v1", bundle_id="DEMO-EVB-001",
                payload=payload, baseline_payload=FIXTURE, scenario=scenario,
                outcome=outcome, evidence_sha256=evidence,
                decision_sha256=decision, receipt_sha256=receipt,
                synthetic=True, executable=False)

def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--sample":
        print(json.dumps(make_sample(sys.argv[2]), indent=2))
        return 0
    if len(sys.argv) != 2:
        print("Usage: python3 verify_journey_demo.py FILE.json | --sample SCENARIO", file=sys.stderr)
        return 2
    try:
        record = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        ok, errors = check(record)
    except (OSError, ValueError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print("DEMO CHAIN CONSISTENT — NOT AUTHORIZED" if ok else "INVALID DEMO CHAIN")
    for error in errors:
        print(f"- {error}")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
