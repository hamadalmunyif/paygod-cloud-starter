import {sha256Fallback} from './sha256.mjs';
// Browser demonstration profile of pinned PayGod verifier 0.2.0.
// Deliberately supports safe integers only; never claims full numeric parity.
const encoder=new TextEncoder();
export async function hash(s){if(!globalThis.crypto?.subtle)return sha256Fallback(encoder.encode(s));return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',encoder.encode(s))),b=>b.toString(16).padStart(2,'0')).join('');}
export function canonical(v){
 if(v===null||typeof v==='boolean')return JSON.stringify(v);
 if(typeof v==='number'){if(!Number.isSafeInteger(v))throw Error('Browser demo supports safe integers only. Use the Python verifier for other numeric values.');return String(v);}
 if(typeof v==='string')return JSON.stringify(v.normalize('NFC')).replace(/[\u007f-\uffff]/g,c=>'\\u'+c.charCodeAt(0).toString(16).padStart(4,'0'));
 if(Array.isArray(v))return '['+v.map(canonical).join(',')+']';
 if(v&&typeof v==='object')return '{'+Object.keys(v).sort().map(k=>canonical(k)+':'+canonical(v[k])).join(',')+'}';
 throw Error('Unsupported JSON value');
}
export async function verifyTransport(input){
 const checks=[],errors=[]; const check=(name,ok,detail)=>{checks.push({name,ok,detail});if(!ok)errors.push(name+': check failed.');};
 const obj=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
 const hex=x=>typeof x==='string'&&/^[a-f0-9]{64}$/.test(x);
 const same=(a,b)=>canonical(a)===canonical(b);
 try{
 if(!obj(input)||input.format!=='paygod-demo-transport/1'||!obj(input.files))throw Error('Expected paygod-demo-transport/1 with UTF-8 file strings.');
 const f=input.files;if(Object.keys(f).length>32||Object.values(f).some(x=>typeof x!=='string'||encoder.encode(x).length>1000000))throw Error('File count or size exceeds demo limits.');
 if(!Object.hasOwn(f,'manifest.json')||!Object.hasOwn(f,'receipt.json'))throw Error('Missing manifest.json or receipt.json.');
 const m=JSON.parse(f['manifest.json']),r=JSON.parse(f['receipt.json']);
 if(!obj(m)||!obj(r)||!Array.isArray(m.files)||!m.files.length||!obj(m.bundle)||!obj(r.bundle))throw Error('Malformed manifest or receipt controls.');
 check('Contract','paygod/v1'===m.api_version&&m.kind==='Manifest'&&r.api_version==='paygod/v1'&&r.kind==='Receipt','Manifest and receipt use paygod/v1.');
 const seen=new Set(),lines=[];
 for(const entry of m.files){
  if(!obj(entry)||typeof entry.name!=='string'||!entry.name||/[\\/]/.test(entry.name)||['.','..','manifest.json','receipt.json'].includes(entry.name)||seen.has(entry.name)||!hex(entry.sha256)||!Number.isSafeInteger(entry.bytes)||entry.bytes<0)throw Error('Invalid or duplicate manifest file entry.');
  seen.add(entry.name);const raw=f[entry.name];
  check('Artifact · '+entry.name,typeof raw==='string'&&await hash(raw)===entry.sha256&&encoder.encode(raw).length===entry.bytes,'SHA-256 and byte count: '+entry.name);
  lines.push(entry.name+'='+entry.sha256+'\n');
 }
 const digest=await hash(lines.sort().join(''));
 check('Bundle digest',m.bundle.algorithm==='sha256'&&m.bundle.file_count===m.files.length&&hex(m.bundle.bundle_digest)&&digest===m.bundle.bundle_digest,'Manifest bundle digest matches the ordered file commitments.');
 check('Manifest binding',r.bundle.manifest_sha256===await hash(f['manifest.json'])&&r.bundle.bundle_digest===digest&&same(r.bundle.files,m.files),'Receipt binds the exact manifest bytes and bundle digest.');
 check('Locked ledger',seen.has('ledger.jsonl')&&typeof f['ledger.jsonl']==='string','Exactly one ledger.jsonl is locked in the manifest.');
 if(!seen.has('ledger.jsonl')||typeof f['ledger.jsonl']!=='string')throw Error('Missing manifest-locked ledger.');
 let previous='0'.repeat(64),index=0,last;let chain=true;
 for(const line of f['ledger.jsonl'].split(/\r?\n/).filter(x=>x.trim())){
  const e=JSON.parse(line);if(!obj(e))throw Error('Malformed ledger entry.');
  const calculated=await hash(canonical({previous_hash:e.previous_hash,timestamp:e.timestamp,data:e.data}));
  chain=chain&&e.entry_index===index&&e.previous_hash===previous&&e.record_hash===calculated;
  previous=e.record_hash;last=e;index++;
 }
 check('Ledger chain',index>0&&chain,'Ledger sequence, previous hashes and record hashes are consistent.');
 if(!last||!obj(last.data)||!obj(r.verdict)||!obj(r.pack)||!obj(r.input)||!obj(r.clock))throw Error('Missing decision-critical control fields.');
 const d=last.data,v=r.verdict;
 const verdicts=['allow','deny','flag','error'];
 check('Decision binding',verdicts.includes(v.value)&&verdicts.includes(d.verdict)&&typeof v.rule_name==='string'&&typeof v.reason==='string'&&v.value===d.verdict&&v.rule_name===d.rule_name&&v.reason===d.reason,'Receipt verdict, rule and reason match the locked ledger.');
 check('Pack and input binding',['name','version','path','digest_sha256'].every(k=>typeof r.pack[k]==='string')&&hex(r.pack.digest_sha256)&&hex(r.input.canonical_hash)&&same(r.pack,m.pack)&&same(r.pack,d.pack)&&same(r.input,m.input)&&r.input.canonical_hash===d.input_hash,'Pack identity and input hash agree across receipt, manifest and ledger.');
 const instant=x=>typeof x==='string'&&/(Z|[+-]\d{2}:\d{2})$/.test(x)&&Number.isFinite(Date.parse(x));
 check('Clock binding',r.clock.source==='env:PAYGOD_CLOCK'&&r.generated_at===r.clock.value&&[r.clock.value,m.generated_at,last.timestamp].every(instant)&&Date.parse(r.clock.value)===Date.parse(m.generated_at)&&Date.parse(m.generated_at)===Date.parse(last.timestamp),'Injected receipt clock matches manifest and ledger time. Unset is rejected.');
 check('Canonicalization declaration',obj(r.canonicalization)&&r.canonicalization.json==='rfc8785','Receipt declares the producer canonicalization profile.');
 return {status:errors.length?'INVALID':'VALID',profile:'browser-demo/0.1; safe-integer subset',checks,errors,bundle_digest:digest,issuer_authenticated:false,external_fact_verified:false};
 }catch(e){errors.push(e.message);return {status:'INVALID',profile:'browser-demo/0.1; safe-integer subset',checks,errors,issuer_authenticated:false,external_fact_verified:false};}
}
