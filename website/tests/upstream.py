import sys,json,tempfile,shutil,hashlib
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'vendor'))
from verify_portable_evidence import verify

root=Path(__file__).resolve().parents[1]
clean_receipt_sha=hashlib.sha256((root/'demo/bundle/receipt.json').read_bytes()).hexdigest()

for case in ['clean','payload','receipt','clock','missing-ledger','malformed','unexpected','canonicalization','wrong-pin']:
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)
        shutil.copytree(root/'demo/bundle',p,dirs_exist_ok=True)

        if case=='payload':
            q=p/'measurement.json'
            q.write_bytes(q.read_bytes().replace(b'420',b'421'))

        if case in ['receipt','clock','canonicalization']:
            q=p/'receipt.json'
            r=json.loads(q.read_text(encoding='utf-8'))
            if case=='receipt':
                r['verdict']['value']='allow'
            elif case=='clock':
                r['clock']['value']='unset'
                r['generated_at']='unset'
            else:
                r['canonicalization']['json']='rfc8785'
            q.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')

        if case=='missing-ledger':
            (p/'ledger.jsonl').unlink()

        if case=='malformed':
            (p/'manifest.json').write_text('[]',encoding='utf-8')

        if case=='unexpected':
            (p/'extra.txt').write_text('noise',encoding='utf-8')

        expected_pin='f'*64 if case=='wrong-pin' else (clean_receipt_sha if case=='clean' else None)
        result=verify(p,expected_receipt_sha256=expected_pin)

        expected='valid' if case=='clean' else 'invalid'
        assert result['status']==expected,(case,result)

        if case=='clean':
            assert result['verifier_version']=='0.3.0',result
            assert result['verification']['integrity']=='verified',result
            assert result['verification']['issuer_authenticity']=='not_verified',result
            assert result['verification']['replay']=='not_performed',result
            assert result['verification']['time_authority']=='producer_supplied',result
            assert result['receipt_sha256']==clean_receipt_sha,result
            assert len(result['ledger_head'])==64,result

        print(case+': '+result['status'])
