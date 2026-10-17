import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
sys.path.insert(0, str(VENDOR))

from verify_portable_evidence import verify

CORPUS_PATH = ROOT / "tests/fixtures/kernel-transport-parity-v1.json"
EXPECTED_BLOB = "d3e682cb7f4f82cc88c4b8fd3ec7fb99d53357da"

raw = CORPUS_PATH.read_bytes()
actual_blob = hashlib.sha1(
    f"blob {len(raw)}\0".encode("ascii") + raw
).hexdigest()
assert actual_blob == EXPECTED_BLOB, (actual_blob, EXPECTED_BLOB)

corpus = json.loads(raw)
assert corpus["profile"] == "paygod-transport-parity-v1"
assert len(corpus["cases"]) == 10


def materialize(root: Path, fixture_name: str) -> Path:
    bundle = root / "bundle"
    bundle.mkdir()
    for name, content in corpus["fixtures"][fixture_name]["files"].items():
        (bundle / name).write_bytes(content.encode("utf-8"))
    return bundle


for case in corpus["cases"]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        bundle = materialize(root, case["fixture"])

        if "set_file" in case:
            mutation = case["set_file"]
            (bundle / mutation["name"]).write_bytes(
                mutation["content"].encode("utf-8")
            )
        if "remove_file" in case:
            (bundle / case["remove_file"]).unlink()

        trust_path = None
        if "trust_store" in case:
            trust_path = root / "trust.json"
            trust_path.write_text(
                json.dumps(
                    corpus["trust_stores"][case["trust_store"]],
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

        result = verify(
            bundle,
            expected_receipt_sha256=case.get("expected_receipt_sha256"),
            trusted_issuer_keys_path=trust_path,
        )

        expected = case["expected"]
        assert result["status"] == expected["status"], (case["name"], result)
        assert result["verification"]["integrity"] == expected["integrity"], (
            case["name"],
            result,
        )

        for key in ("issuer_authenticity", "replay", "time_authority"):
            if key in expected:
                assert result["verification"][key] == expected[key], (
                    case["name"],
                    key,
                    result,
                )

        if "issuer_reason" in expected:
            assert result["issuer_signature"]["reason"] == expected["issuer_reason"], (
                case["name"],
                result,
            )

        for key in (
            "receipt_sha256",
            "manifest_sha256",
            "bundle_digest",
            "ledger_head",
        ):
            if key in expected:
                assert result[key] == expected[key], (case["name"], key, result)

        print("PASS:", case["name"])

print(
    "PASS: website vendored Python verifier consumed exact Kernel transport corpus"
)
