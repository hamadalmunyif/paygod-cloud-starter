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

# A disabled-by-default *design* cannot smuggle collection scripts into either
# editable sources or generated browser output. This is a bounded static gate,
# not a substitute for reviewing CSP, remote scripts, consent or network traffic.
for location in (root / "src", root / "v2", root / "dist"):
    assert location.is_dir(), f"expected website source/build directory: {location}"
    checked = 0
    for path in location.rglob("*"):
        if not path.is_file() or path.suffix not in {".js", ".mjs", ".html"}:
            continue
        checked += 1
        content = path.read_text(encoding="utf-8").lower()
        for needle in ("posthog.init(", "posthog.capture(", "posthog-js",
                       "app.posthog.com", "eu.i.posthog.com", "us.i.posthog.com",
                       "phc_"):
            assert needle not in content, (path, needle)
    assert checked > 0, f"no browser files checked at {location}"

print("PASS: proposed taxonomy; no known PostHog SDK/capture in recursive source and built browser assets")
