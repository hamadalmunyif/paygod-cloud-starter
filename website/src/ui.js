const $=id=>document.getElementById(id);let latest=null,runId=0;
const editor=$('bundle-editor');
function invalidate(){runId++;latest=null;$('status').textContent='NOT RUN';$('status').className='status pending';$('result-title').textContent='Ready for independent checks.';$('result-summary').textContent='Run verification on the current bytes.';$('checks').replaceChildren();$('error-detail').textContent='';$('digest').textContent='Run verification to calculate';$('download-result').disabled=true;}
function load(kind='clean'){
 const t=structuredClone(SAMPLE);
 if(kind==='tamper')t.files['measurement.json']=t.files['measurement.json'].replace('420','421');
 if(kind==='receipt-tamper'){const r=JSON.parse(t.files['receipt.json']);r.verdict.value='allow';t.files['receipt.json']=JSON.stringify(r,null,2)+'\n';}
 editor.value=JSON.stringify(t,null,2);invalidate();$('edit-state').textContent=kind==='clean'?'CLEAN SAMPLE':kind==='tamper'?'1 BYTE CHANGED':'RECEIPT ALTERED';
 for(const id of ['clean','tamper','receipt-tamper'])$(id).classList.toggle('active',kind===id);
}
function save(name,data){const blob=new Blob([typeof data==='string'?data:JSON.stringify(data,null,2)+'\n'],{type:'application/json'});const u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),5000);}
$('clean').onclick=()=>load();$('tamper').onclick=()=>load('tamper');$('receipt-tamper').onclick=()=>load('receipt-tamper');
editor.oninput=()=>{invalidate();$('edit-state').textContent='EDITED — REVERIFY';for(const id of ['clean','tamper','receipt-tamper'])$(id).classList.remove('active');};
$('verify').onclick=async()=>{
 const current=++runId; $('verify').disabled=true; $('verify').textContent='Checking…';
 let result;
 try {if(new TextEncoder().encode(editor.value).length>2000000)throw Error('Demo transport must be at most 2 MB.');result=await verifyTransport(JSON.parse(editor.value));}
 catch(e){result={status:'INVALID',checks:[],errors:[e.message],issuer_authenticated:false,external_fact_verified:false};}
 $('verify').disabled=false;$('verify').textContent='Run verification ↗';if(current!==runId)return;
 latest=result;const ok=result.status==='VALID';$('status').textContent=result.status;$('status').className='status '+(ok?'valid':'invalid');$('result-title').textContent=ok?'Evidence is internally consistent.':'Evidence verification failed.';$('result-summary').textContent=ok?'All supported checks passed. Issuer identity and source truth remain unverified.':'One or more checks failed. Inspect the failed bindings below.';
 $('checks').replaceChildren();for(const check of result.checks){const row=document.createElement('div');row.className='check-row'+(check.ok?'':' failed');const icon=document.createElement('span');icon.textContent=check.ok?'✓':'×';const label=document.createElement('div');label.textContent=check.name;row.append(icon,label);$('checks').append(row);}
 $('error-detail').textContent=result.errors.join('\n');$('digest').textContent=result.bundle_digest||'Not calculated';$('download-result').disabled=false;
};
$('download').onclick=()=>save('paygod-demo-bundle.json',editor.value);$('download-result').onclick=()=>{if(latest)save('paygod-verification-result.json',latest);};
$('upload').onchange=async event=>{const f=event.target.files[0];if(!f)return;invalidate();try{if(f.size>2000000)throw Error('Import rejected: maximum size is 2 MB.');editor.value=await f.text();$('edit-state').textContent='IMPORTED — REVERIFY';for(const id of ['clean','tamper','receipt-tamper'])$(id).classList.remove('active');}catch(e){$('error-detail').textContent=e.message;}event.target.value='';};
load();
