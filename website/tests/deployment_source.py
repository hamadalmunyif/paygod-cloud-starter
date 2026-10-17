import json
import os
import re
from pathlib import Path

payload_path = Path("dist/meta/deployment-source.json")
assert payload_path.is_file(), "deployment source identity was not built"

payload = json.loads(payload_path.read_text(encoding="utf-8"))
assert payload["profile"] == "paygod-deployment-source-v1"

sha = payload["git_sha"]
assert re.fullmatch(r"[0-9a-f]{40}", sha), sha

expected = os.environ.get("GITHUB_SHA")
if expected:
    assert sha == expected, (sha, expected)
    assert payload["source"] == "github:GITHUB_SHA", payload

print("PASS: deployment-source identity matches exact CI source SHA", sha)
