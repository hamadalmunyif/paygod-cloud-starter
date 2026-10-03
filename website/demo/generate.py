"""Synthetic, explicitly non-production fixture for PayGod verifier v0.4."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'vendor'))
from verify_portable_evidence import canonical_json,verify

root=Path(__file__).resolve().parent
out=root/'bundle'
out.mkdir(exist_ok=True)
for stale in out.iterdir():
    if stale.is_file():
        stale.unlink()

def sha(b): return hashlib.sha256(b).hexdigest()
def write(n,v):
    b=(json.dumps(v,indent=2,ensure_ascii=True)+'\n').encode()
    (out/n).write_bytes(b)
    return b

clock='2026-09-28T12:00:00Z'
measurement={
 'fixture':'synthetic; not a real facility measurement',
 'metric':'electricity_consumption',
 'value':420,
 'unit':'kWh',
 'period':'2026-09-27',
 'source':'demo-meter-01'
}
write('measurement.json',measurement)
pack={
 'name':'demo-resource-review',
 'version':'0.1.0',
 'path':'demo/resource-review',
 'digest_sha256':sha(b'demo: flag if electricity consumption exceeds 400 kWh')
}
input_={'canonical_hash':sha(canonical_json(measurement).encode())}
data={
 'verdict':'flag',
 'rule_name':'review-consumption',
 'reason':'420 kWh exceeds the illustrative 400 kWh review threshold.',
 'pack':pack,
 'input_hash':input_['canonical_hash']
}
payload={'previous_hash':'0'*64,'timestamp':clock,'data':data}
entry={**payload,'entry_index':0,'record_hash':sha(canonical_json(payload).encode())}
(out/'ledger.jsonl').write_text(json.dumps(entry)+'\n',encoding='utf-8')
files=[
 {'name':n,'sha256':sha((out/n).read_bytes()),'bytes':(out/n).stat().st_size}
 for n in ['ledger.jsonl','measurement.json']
]
bundle={
 'algorithm':'sha256',
 'file_count':len(files),
 'bundle_digest':sha(''.join(sorted(f"{f['name']}={f['sha256']}\n" for f in files)).encode())
}
manifest={
 'api_version':'paygod/v1',
 'kind':'Manifest',
 'generated_at':clock,
 'pack':pack,
 'input':input_,
 'bundle':bundle,
 'files':files
}
mb=write('manifest.json',manifest)
receipt={
 'api_version':'paygod/v1',
 'kind':'Receipt',
 'spec_version':'0.2.0',
 'generated_at':clock,
 'clock':{'source':'env:PAYGOD_CLOCK','value':clock},
 'canonicalization':{'json':'paygod-c14n-v1'},
 'runner':{'image':'paygod/website-demo','image_digest':'unknown'},
 'pack':pack,
 'input':input_,
 'bundle':{**bundle,'manifest_sha256':sha(mb),'files':files},
 'verdict':{k:data[v] for k,v in [('value','verdict'),('rule_name','rule_name'),('reason','reason')]},
 'replay':{'command':'not performed by integrity verifier'}
}
receipt_bytes=write('receipt.json',receipt)
receipt_sha=sha(receipt_bytes)

DEMO_KEY_ID='paygod-demo-issuer-2026-10-03'
DEMO_RECEIPT_SHA='d019ae508d5d108bf959789d5e6ab212ae9d357ab08661cdbd0085efa8409cac'
DEMO_PUBLIC_KEY_B64='7VuSeH7L1r8sap/kKkixGpl1v1HlxBS/jxpCg6xSD4o='
DEMO_SIGNATURE_B64='6CJvUu3bnhFqwoyCHgoNb5mYhnZtgdfY3MKzskjT1fRDCJgWYEpJTuh7PPXZVtoFgx6u2Fa01qGeU+fHw/jrAA=='
assert receipt_sha==DEMO_RECEIPT_SHA,(receipt_sha,DEMO_RECEIPT_SHA)

signature={
 'profile':'paygod-ed25519-receipt-v1',
 'algorithm':'Ed25519',
 'key_id':DEMO_KEY_ID,
 'receipt_sha256':receipt_sha,
 'signature_b64':DEMO_SIGNATURE_B64
}
write('receipt.sig.json',signature)

trust={
 'profile':'paygod-ed25519-trust-v1',
 'keys':[{
  'key_id':DEMO_KEY_ID,
  'algorithm':'Ed25519',
  'public_key_b64':DEMO_PUBLIC_KEY_B64
 }]
}
(root/'trusted-issuer-demo.json').write_text(json.dumps(trust,indent=2)+'\n',encoding='utf-8')

transport={
 'format':'paygod-demo-transport/1',
 'description':'Synthetic signed fixture. UTF-8 file strings; not a new kernel bundle standard.',
 'files':{p.name:p.read_text(encoding='utf-8') for p in sorted(out.iterdir())}
}
(root/'sample.json').write_text(json.dumps(transport,indent=2)+'\n',encoding='utf-8')

result=verify(out)
assert result['status']=='valid',result
assert result['verifier_version']=='0.4.0',result
assert result['verification']['integrity']=='verified',result
assert result['verification']['issuer_authenticity']=='not_verified',result
assert result['issuer_signature']['reason']=='no_trust_anchor_supplied',result
assert result['verification']['replay']=='not_performed',result
assert result['verification']['time_authority']=='producer_supplied',result
(root/'upstream-result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
