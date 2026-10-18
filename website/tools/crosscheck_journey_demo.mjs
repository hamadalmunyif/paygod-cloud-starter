import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';

const python='website/tools/verify_journey_demo.py';
const hash=s=>createHash('sha256').update(s,'utf8').digest('hex');
const encode=parts=>parts.map(x=>String(x.length)+':'+x).join('|');
const outcomes={
  clean:'AUTHORITY NOT ESTABLISHED',
  tamper:'INTEGRITY FAILED',
  auth:'ISSUER TRUST NOT ESTABLISHED',
  demo:'SIMULATED ALLOW'
};
function recompute(r){
 const evidence=hash(r.payload);
 const decision=hash(encode(['paygod-demo-decision-v1',r.bundle_id,evidence,r.scenario,r.outcome,'synthetic-only']));
 const receipt=hash(encode(['paygod-demo-receipt-v1',r.bundle_id,evidence,decision,r.outcome,'not-signed']));
 return [evidence,decision,receipt];
}
for(const scenario of Object.keys(outcomes)){
 const raw=execFileSync('python3',[python,'--sample',scenario],{encoding:'utf8'});
 const record=JSON.parse(raw);
 assert.equal(record.outcome,outcomes[scenario]);
 assert.deepEqual(recompute(record),[record.evidence_sha256,record.decision_sha256,record.receipt_sha256],scenario);
 const fields=['payload','outcome','bundle_id','scenario','evidence_sha256','decision_sha256','receipt_sha256'];
 for(const field of fields){
  const mutated={...record,[field]:record[field]+'X'};
  assert.notDeepEqual(recompute(mutated),[mutated.evidence_sha256,mutated.decision_sha256,mutated.receipt_sha256],scenario+':'+field);
 }
 console.log('PASS: '+scenario+' Python and Node digests agree; mutations change expected chain');
}
console.log('Cross-language demo check passed. No signature or authorization verified.');
