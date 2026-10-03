import {sha256Fallback} from './sha256.mjs';

export const VERIFIER_VERSION='0.3.0';
export const CANONICALIZATION_PROFILE='paygod-c14n-v1';
export const SAFE_INTEGER_MAX=9007199254740991n;

const encoder=new TextEncoder();
const HEX64=/^[a-f0-9]{64}$/;
const VERDICTS=new Set(['allow','deny','flag','error']);

function toHex(bytes){return Array.from(bytes,b=>b.toString(16).padStart(2,'0')).join('');}
export async function hashBytes(bytes){
 if(globalThis.crypto?.subtle)return toHex(new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256',bytes)));
 return sha256Fallback(bytes);
}
export async function hash(value){return hashBytes(encoder.encode(value));}

function validateNumberLexemes(text){
 let inString=false,escaped=false;
 for(let i=0;i<text.length;i++){
  const ch=text[i];
  if(inString){
   if(escaped)escaped=false;
   else if(ch==='\\')escaped=true;
   else if(ch==='"')inString=false;
   continue;
  }
  if(ch==='"'){inString=true;continue;}
  if(ch==='-'||(ch>='0'&&ch<='9')){
   const match=text.slice(i).match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/);
   if(!match)continue;
   const token=match[0];
   if(/[.eE]/.test(token))throw Error('Floating-point and exponent numbers are not allowed by paygod-c14n-v1.');
   const value=BigInt(token);
   if(value < -SAFE_INTEGER_MAX || value > SAFE_INTEGER_MAX)throw Error('Integer outside paygod-c14n-v1 safe range.');
   i+=token.length-1;
  }
 }
}
export function strictJsonParse(text){
 validateNumberLexemes(text);
 return JSON.parse(text);
}
function ensurePairedSurrogates(value){
 for(let i=0;i<value.length;i++){
  const unit=value.charCodeAt(i);
  if(unit>=0xd800&&unit<=0xdbff){
   if(i+1>=value.length)throw Error('Unpaired Unicode surrogate.');
   const next=value.charCodeAt(i+1);
   if(next<0xdc00||next>0xdfff)throw Error('Unpaired Unicode surrogate.');
   i++;
  }else if(unit>=0xdc00&&unit<=0xdfff)throw Error('Unpaired Unicode surrogate.');
 }
}
function profileString(value){
 ensurePairedSurrogates(value);
 let out='"';
 for(let i=0;i<value.length;i++){
  const unit=value.charCodeAt(i);
  if(unit===0x22)out+='\\"';
  else if(unit===0x5c)out+='\\\\';
  else if(unit===0x08)out+='\\b';
  else if(unit===0x0c)out+='\\f';
  else if(unit===0x0a)out+='\\n';
  else if(unit===0x0d)out+='\\r';
  else if(unit===0x09)out+='\\t';
  else if(unit<0x20||unit>0x7e)out+='\\u'+unit.toString(16).padStart(4,'0');
  else out+=String.fromCharCode(unit);
 }
 return out+'"';
}
function ordinalCompare(a,b){
 const n=Math.min(a.length,b.length);
 for(let i=0;i<n;i++){const d=a.charCodeAt(i)-b.charCodeAt(i);if(d)return d;}
 return a.length-b.length;
}
export function canonical(value){
 if(value===null)return 'null';
 if(value===true)return 'true';
 if(value===false)return 'false';
 if(typeof value==='string')return profileString(value);
 if(Array.isArray(value))return '['+value.map(canonical).join(',')+']';
 if(typeof value==='number'){
  if(!Number.isInteger(value))throw Error('Floating-point numbers are not allowed by paygod-c14n-v1.');
  if(!Number.isSafeInteger(value))throw Error('Integer outside paygod-c14n-v1 safe range.');
  return Object.is(value,-0)?'0':String(value);
 }
 if(value&&typeof value==='object'){
  const keys=Object.keys(value);
  for(const key of keys){
   ensurePairedSurrogates(key);
   if(key.normalize('NFC')!==key)throw Error('JSON object key is not NFC-normalized.');
  }
  keys.sort(ordinalCompare);
  return '{'+keys.map(key=>profileString(key)+':'+canonical(value[key])).join(',')+'}';
 }
 throw Error('Unsupported JSON value.');
}
function deepEqual(a,b){
 if(a===b)return true;
 if(typeof a!==typeof b||a===null||b===null)return false;
 if(Array.isArray(a)||Array.isArray(b)){
  if(!Array.isArray(a)||!Array.isArray(b)||a.length!==b.length)return false;
  return a.every((v,i)=>deepEqual(v,b[i]));
 }
 if(typeof a==='object'){
  const ak=Object.keys(a).sort(ordinalCompare),bk=Object.keys(b).sort(ordinalCompare);
  return ak.length===bk.length&&ak.every((k,i)=>k===bk[i]&&deepEqual(a[k],b[k]));
 }
 return false;
}
function safeName(name){return typeof name==='string'&&name&&name!=='.'&&name!=='..'&&!/[\\/]/.test(name)&&!['manifest.json','receipt.json'].includes(name);}
function instant(value){return typeof value==='string'&&/(?:Z|[+-]\d{2}:\d{2})$/.test(value)&&Number.isFinite(Date.parse(value));}
function dimensions(integrity,timeAuthority='failed'){
 return {integrity,issuer_authenticity:'not_verified',replay:'not_performed',time_authority:timeAuthority};
}

async function verifyLedger(raw,errors,check){
 let previous='0'.repeat(64),expectedIndex=0,last=null,chainOk=true;
 const lines=raw.split(/\r?\n/).filter(x=>x.trim());
 for(let i=0;i<lines.length;i++){
  let entry;
  try{entry=strictJsonParse(lines[i]);}catch(error){errors.push('ledger line '+(i+1)+': '+error.message);return null;}
  if(!entry||Array.isArray(entry)||typeof entry!=='object'){errors.push('ledger line '+(i+1)+': entry must be an object.');return null;}
  if(entry.entry_index!==expectedIndex)chainOk=false;
  if(entry.previous_hash!==previous)chainOk=false;
  let calculated;
  try{calculated=await hash(canonical({previous_hash:entry.previous_hash??null,timestamp:entry.timestamp??null,data:entry.data??null}));}
  catch(error){errors.push('ledger line '+(i+1)+': canonicalization failed: '+error.message);return null;}
  if(typeof entry.record_hash!=='string'||!HEX64.test(entry.record_hash)||entry.record_hash!==calculated)chainOk=false;
  previous=typeof entry.record_hash==='string'?entry.record_hash:'';
  expectedIndex++;
  last=entry;
 }
 check('Ledger chain',expectedIndex>0&&chainOk,'Ledger sequence, previous hashes and record hashes are consistent.');
 return last;
}

export async function verifyTransport(input,{expectedReceiptSha256=null,allowUnboundClock=false}={}){
 const checks=[],errors=[];
 const check=(name,ok,detail)=>{checks.push({name,ok,detail});if(!ok)errors.push(name+': check failed.');};
 const obj=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
 try{
  if(!obj(input)||input.format!=='paygod-demo-transport/1'||!obj(input.files))throw Error('Expected paygod-demo-transport/1 with UTF-8 file strings.');
  const files=input.files,names=Object.keys(files);
  if(names.length>32||Object.values(files).some(x=>typeof x!=='string'||encoder.encode(x).length>1000000))throw Error('File count or size exceeds verifier limits.');
  if(!Object.hasOwn(files,'manifest.json')||!Object.hasOwn(files,'receipt.json'))throw Error('Missing manifest.json or receipt.json.');

  const receiptSha=await hash(files['receipt.json']);
  if(expectedReceiptSha256){
   check('External receipt commitment',HEX64.test(expectedReceiptSha256)&&receiptSha===expectedReceiptSha256,'Receipt SHA-256 matches the independently supplied commitment.');
  }

  let manifest,receipt;
  try{manifest=strictJsonParse(files['manifest.json']);receipt=strictJsonParse(files['receipt.json']);}
  catch(error){throw Error('Invalid control JSON: '+error.message);}
  if(!obj(manifest)||!obj(receipt)||!Array.isArray(manifest.files)||!manifest.files.length||!obj(manifest.bundle)||!obj(receipt.bundle))throw Error('Malformed manifest or receipt controls.');

  check('Contract',manifest.api_version==='paygod/v1'&&manifest.kind==='Manifest'&&receipt.api_version==='paygod/v1'&&receipt.kind==='Receipt','Manifest and receipt use paygod/v1.');
  check('Canonicalization declaration',obj(receipt.canonicalization)&&receipt.canonicalization.json===CANONICALIZATION_PROFILE,'Receipt declares paygod-c14n-v1.');

  const seen=new Set(),digestLines=[];
  for(let i=0;i<manifest.files.length;i++){
   const entry=manifest.files[i];
   if(!obj(entry)||!safeName(entry.name)||seen.has(entry.name)||typeof entry.sha256!=='string'||!HEX64.test(entry.sha256)||!Number.isSafeInteger(entry.bytes)||entry.bytes<0)throw Error('Invalid or duplicate manifest file entry.');
   seen.add(entry.name);
   const raw=files[entry.name];
   const ok=typeof raw==='string'&&await hash(raw)===entry.sha256&&encoder.encode(raw).length===entry.bytes;
   check('Artifact · '+entry.name,ok,'SHA-256 and byte count: '+entry.name);
   digestLines.push(entry.name+'='+entry.sha256+'\n');
  }

  const allowed=new Set(['manifest.json','receipt.json',...seen]);
  for(const name of names)if(!allowed.has(name))check('Unexpected member · '+name,false,'Every transferred file must be manifest-locked or a control file.');

  const digest=await hash(digestLines.sort().join(''));
  check('Bundle digest',manifest.bundle.algorithm==='sha256'&&manifest.bundle.file_count===manifest.files.length&&HEX64.test(manifest.bundle.bundle_digest)&&digest===manifest.bundle.bundle_digest,'Manifest bundle digest matches the ordered file commitments.');

  const manifestSha=await hash(files['manifest.json']);
  check('Manifest binding',receipt.bundle.manifest_sha256===manifestSha&&receipt.bundle.bundle_digest===digest&&deepEqual(receipt.bundle.files,manifest.files),'Receipt binds the exact manifest bytes and bundle digest.');

  const ledgerCount=manifest.files.filter(x=>obj(x)&&x.name==='ledger.jsonl').length;
  check('Locked ledger',ledgerCount===1&&typeof files['ledger.jsonl']==='string','Exactly one ledger.jsonl is locked in the manifest.');
  if(ledgerCount!==1||typeof files['ledger.jsonl']!=='string')throw Error('Missing manifest-locked ledger.');

  const last=await verifyLedger(files['ledger.jsonl'],errors,check);
  if(!last||!obj(last.data)||!obj(receipt.verdict)||!obj(receipt.pack)||!obj(receipt.input)||!obj(receipt.clock))throw Error('Missing decision-critical control fields.');

  const data=last.data,verdict=receipt.verdict;
  check('Decision binding',VERDICTS.has(verdict.value)&&VERDICTS.has(data.verdict)&&typeof verdict.rule_name==='string'&&typeof verdict.reason==='string'&&verdict.value===data.verdict&&verdict.rule_name===data.rule_name&&verdict.reason===data.reason,'Receipt verdict, rule and reason match the locked ledger.');
  check('Pack and input binding',['name','version','path','digest_sha256'].every(k=>typeof receipt.pack[k]==='string')&&HEX64.test(receipt.pack.digest_sha256)&&HEX64.test(receipt.input.canonical_hash)&&deepEqual(receipt.pack,manifest.pack)&&deepEqual(receipt.pack,data.pack)&&deepEqual(receipt.input,manifest.input)&&receipt.input.canonical_hash===data.input_hash,'Pack identity and input hash agree across receipt, manifest and ledger.');

  let timeAuthority='failed',clockBinding='invalid';
  if(receipt.clock.source!=='env:PAYGOD_CLOCK'||receipt.generated_at!==receipt.clock.value){
   check('Clock binding',false,'Receipt generated_at must match the declared producer clock.');
  }else if(receipt.clock.value==='unset'){
   timeAuthority='unbound';
   clockBinding=allowUnboundClock?'unbound-opt-in':'unbound-rejected';
   check('Clock binding',allowUnboundClock,'An unbound producer clock requires explicit opt-in.');
  }else{
   const ok=[receipt.clock.value,manifest.generated_at,last.timestamp].every(instant)&&Date.parse(receipt.clock.value)===Date.parse(manifest.generated_at)&&Date.parse(manifest.generated_at)===Date.parse(last.timestamp);
   if(ok){timeAuthority='producer_supplied';clockBinding='injected';}
   check('Clock binding',ok,'Producer-supplied clock matches manifest and ledger time. This is not a trusted third-party timestamp.');
  }

  const ledgerHead=typeof last.record_hash==='string'&&HEX64.test(last.record_hash)?last.record_hash:null;
  const integrity=errors.length?'failed':'verified';
  return {
   status:errors.length?'invalid':'valid',
   portable:!errors.length,
   verifier_version:VERIFIER_VERSION,
   profile:CANONICALIZATION_PROFILE,
   verification:dimensions(integrity,timeAuthority),
   checks,
   errors,
   bundle_digest:digest,
   manifest_sha256:manifestSha,
   receipt_sha256:receiptSha,
   ledger_head:ledgerHead,
   verified_files:manifest.files.length,
   clock_binding:clockBinding
  };
 }catch(error){
  errors.push(error.message);
  return {
   status:'invalid',
   portable:false,
   verifier_version:VERIFIER_VERSION,
   profile:CANONICALIZATION_PROFILE,
   verification:dimensions('failed','failed'),
   checks,
   errors,
   bundle_digest:null,
   manifest_sha256:null,
   receipt_sha256:null,
   ledger_head:null,
   verified_files:0,
   clock_binding:'invalid'
  };
 }
}
