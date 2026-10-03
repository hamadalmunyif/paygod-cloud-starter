import base64
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

vendor = Path(__file__).resolve().parents[1] / 'vendor'
sys.path.insert(0, str(vendor))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from issuer_auth import ALGORITHM, PROFILE, TRUST_PROFILE, signing_message
from verify_portable_evidence import verify

root = Path(__file__).resolve().parents[1]
clean_receipt_sha = hashlib.sha256((root / 'demo/bundle/receipt.json').read_bytes()).hexdigest()


def write_signature(bundle: Path, private_key: Ed25519PrivateKey, key_id: str) -> bytes:
    receipt_sha = hashlib.sha256((bundle / 'receipt.json').read_bytes()).hexdigest()
    signature = private_key.sign(signing_message(key_id, receipt_sha))
    envelope = {
        'profile': PROFILE,
        'algorithm': ALGORITHM,
        'key_id': key_id,
        'receipt_sha256': receipt_sha,
        'signature_b64': base64.b64encode(signature).decode('ascii'),
    }
    (bundle / 'receipt.sig.json').write_text(
        json.dumps(envelope, indent=2, sort_keys=True) + '\n',
        encoding='utf-8',
    )
    return private_key.public_key().public_bytes_raw()


def write_trust_store(path: Path, key_id: str, public_key_raw: bytes):
    path.write_text(
        json.dumps({
            'profile': TRUST_PROFILE,
            'keys': [{
                'key_id': key_id,
                'algorithm': ALGORITHM,
                'public_key_b64': base64.b64encode(public_key_raw).decode('ascii'),
            }],
        }, indent=2) + '\n',
        encoding='utf-8',
    )


for case in [
    'clean',
    'payload',
    'receipt',
    'clock',
    'missing-ledger',
    'malformed',
    'unexpected',
    'canonicalization',
    'wrong-pin',
]:
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        bundle = p / 'bundle'
        shutil.copytree(root / 'demo/bundle', bundle)

        if case == 'payload':
            q = bundle / 'measurement.json'
            q.write_bytes(q.read_bytes().replace(b'420', b'421'))

        if case in ['receipt', 'clock', 'canonicalization']:
            q = bundle / 'receipt.json'
            r = json.loads(q.read_text(encoding='utf-8'))
            if case == 'receipt':
                r['verdict']['value'] = 'allow'
            elif case == 'clock':
                r['clock']['value'] = 'unset'
                r['generated_at'] = 'unset'
            else:
                r['canonicalization']['json'] = 'rfc8785'
            q.write_text(json.dumps(r, indent=2) + '\n', encoding='utf-8')

        if case == 'missing-ledger':
            (bundle / 'ledger.jsonl').unlink()

        if case == 'malformed':
            (bundle / 'manifest.json').write_text('[]', encoding='utf-8')

        if case == 'unexpected':
            (bundle / 'extra.txt').write_text('noise', encoding='utf-8')

        expected_pin = 'f' * 64 if case == 'wrong-pin' else (clean_receipt_sha if case == 'clean' else None)
        result = verify(bundle, expected_receipt_sha256=expected_pin)

        expected = 'valid' if case == 'clean' else 'invalid'
        assert result['status'] == expected, (case, result)

        if case == 'clean':
            assert result['verifier_version'] == '0.4.0', result
            assert result['verification']['integrity'] == 'verified', result
            assert result['verification']['issuer_authenticity'] == 'not_verified', result
            assert result['verification']['replay'] == 'not_performed', result
            assert result['verification']['time_authority'] == 'producer_supplied', result
            assert result['receipt_sha256'] == clean_receipt_sha, result
            assert len(result['ledger_head']) == 64, result

        print(case + ': ' + result['status'])

with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp)
    bundle = p / 'bundle'
    shutil.copytree(root / 'demo/bundle', bundle)

    key_id = 'website-ci-issuer'
    private_key = Ed25519PrivateKey.generate()
    public_raw = write_signature(bundle, private_key, key_id)
    trust_store = p / 'trusted-issuers.json'
    write_trust_store(trust_store, key_id, public_raw)

    no_trust = verify(bundle)
    assert no_trust['status'] == 'valid'
    assert no_trust['verification']['integrity'] == 'verified'
    assert no_trust['verification']['issuer_authenticity'] == 'not_verified'
    assert no_trust['issuer_signature']['reason'] == 'no_trust_anchor_supplied'

    trusted = verify(bundle, trusted_issuer_keys_path=trust_store)
    assert trusted['status'] == 'valid'
    assert trusted['verification']['integrity'] == 'verified'
    assert trusted['verification']['issuer_authenticity'] == 'verified'
    assert trusted['issuer_signature']['key_trusted'] is True
    assert trusted['issuer_signature']['signature_valid'] is True

    receipt = bundle / 'receipt.json'
    receipt.write_bytes(receipt.read_bytes() + b' ')
    changed = verify(bundle, trusted_issuer_keys_path=trust_store)
    assert changed['status'] == 'valid'
    assert changed['verification']['integrity'] == 'verified'
    assert changed['verification']['issuer_authenticity'] == 'failed'
    assert changed['issuer_signature']['reason'] == 'receipt_commitment_mismatch'

    print('issuer-auth: verified / receipt-mutation failed as expected')
