import sys,json,tempfile,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'vendor'))
from verify_portable_evidence import verify
root=Path(__file__).resolve().parents[1]
for case in ['clean','payload','receipt','clock','missing-ledger','malformed']:
 with tempfile.TemporaryDirectory() as tmp:
  p=Path(tmp);shutil.copytree(root/'demo/bundle',p,dirs_exist_ok=True)
  if case=='payload':
   q=p/'measurement.json';q.write_bytes(q.read_bytes().replace(b'420',b'421'))
  if case in ['receipt','clock']:
   q=p/'receipt.json';r=json.loads(q.read_text())
   if case=='receipt':r['verdict']['value']='allow'
   else:r['clock']['value']='unset';r['generated_at']='unset'
   q.write_text(json.dumps(r))
  if case=='missing-ledger':(p/'ledger.jsonl').unlink()
  if case=='malformed':(p/'manifest.json').write_text('[]')
  result=verify(p);assert result['status']==('valid' if case=='clean' else 'invalid'),result
  print(case+': '+result['status'])
