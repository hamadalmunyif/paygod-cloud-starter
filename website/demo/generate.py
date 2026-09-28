"""Synthetic, explicitly non-production fixture for the pinned upstream verifier."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'vendor'))
from verify_portable_evidence import canonical_json,verify
root=Path(__file__).resolve().parent
out=root/'bundle'; out.mkdir(exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def write(n,v):
 b=(json.dumps(v,indent=2,ensure_ascii=True)+'\n').encode(); (out/n).write_bytes(b); return b
clock='2026-09-28T12:00:00Z'
measurement={'fixture':'synthetic; not a real facility measurement','metric':'electricity_consumption','value':420,'unit':'kWh','period':'2026-09-27','source':'demo-meter-01'}
raw=write('measurement.json',measurement)
pack={'name':'demo-resource-review','version':'0.1.0','path':'demo/resource-review','digest_sha256':sha(b'demo: flag if electricity consumption exceeds 400 kWh')}
input_={'canonical_hash':sha(canonical_json(measurement).encode())}
data={'verdict':'flag','rule_name':'review-consumption','reason':'420 kWh exceeds the illustrative 400 kWh review threshold.','pack':pack,'input_hash':input_['canonical_hash']}
payload={'previous_hash':'0'*64,'timestamp':clock,'data':data}
entry={**payload,'entry_index':0,'record_hash':sha(canonical_json(payload).encode())}
(out/'ledger.jsonl').write_text(json.dumps(entry)+'\n')
files=[{'name':n,'sha256':sha((out/n).read_bytes()),'bytes':(out/n).stat().st_size} for n in ['ledger.jsonl','measurement.json']]
bundle={'algorithm':'sha256','file_count':len(files),'bundle_digest':sha(''.join(sorted(f"{f['name']}={f['sha256']}\n" for f in files)).encode())}
m={'api_version':'paygod/v1','kind':'Manifest','generated_at':clock,'pack':pack,'input':input_,'bundle':bundle,'files':files}
mb=write('manifest.json',m)
r={'api_version':'paygod/v1','kind':'Receipt','generated_at':clock,'clock':{'source':'env:PAYGOD_CLOCK','value':clock},'canonicalization':{'json':'rfc8785'},'pack':pack,'input':input_,'bundle':{**bundle,'manifest_sha256':sha(mb),'files':files},'verdict':{k:data[v] for k,v in [('value','verdict'),('rule_name','rule_name'),('reason','reason')]}}
write('receipt.json',r)
transport={'format':'paygod-demo-transport/1','description':'Synthetic fixture. UTF-8 file strings; not a new kernel bundle standard.','files':{p.name:p.read_text() for p in sorted(out.iterdir())}}
(root/'sample.json').write_text(json.dumps(transport,indent=2)+'\n')
result=verify(out); assert result['status']=='valid',result
(root/'upstream-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
