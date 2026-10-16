#!/usr/bin/env python3
"""Fail-closed static privacy contract for an analytics PLAN, not live telemetry."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
contract = json.loads((root / "analytics" / "EVENTS.v0.json").read_text(encoding="utf-8"))

assert contract["status"] == "not_instrumented"
for setting in ("default_capture_enabled", "session_replay_enabled",
                "autocapture_enabled", "person_identification_enabled"):
    assert contract[setting] is False, setting

allowed = set(contract["allowed_properties"])
assert allowed == {
    "route_id", "page_locale", "site_release", "surface", "challenge_kind",
    "integrity_result", "issuer_authenticity", "target_kind", "deployment_env",
}
events = contract["events"]
names = [e["name"] for e in events]
assert len(names) == len(set(names)), "duplicate telemetry event name"
assert all(n.startswith("pg_") for n in names)
assert all(e["status"] in ("proposed", "reserved_until_form_and_consent_exist")
           for e in events)
assert len(contract["forbidden_data"]) > 0

# This docs-only proposal must not quietly inject an analytics client into
# the deployed static JS. A later separately reviewed PR must change this gate.
for location in ((root / "src"), (root / "v2")):
    for path in location.glob("*.js"):
        text = path.read_text(encoding="utf-8").lower()
        assert "posthog.init(" not in text, path
        assert "posthog.capture(" not in text, path

print("PASS: proposed taxonomy, privacy defaults, no live PostHog capture in website JS")
