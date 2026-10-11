"""Read-only bilingual explanation UI: links existing bounded evidence; never claims live execution."""
from html import escape as esc

ROOT="https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/"
CLAIMS=ROOT+"docs/CLAIMS_REGISTER.md"
BOUNDARY=ROOT+"docs/REPOSITORY_BOUNDARY.md"
STANDALONE=ROOT+"docs/STANDALONE_VERIFIER.md"
VERIFIER_IMPL=ROOT+"tools/verify_portable_evidence.py"
ADMISSION=ROOT+"adrs/0003-evidence-admission-before-decision-execution.md"
CVE_PACK=ROOT+"packs/core/critical-cve-blocker/pack.yaml"
CVE_TESTS=ROOT+"packs/core/critical-cve-blocker/tests/cases.yaml"

DATA={
"en":{
"lens_kicker":"EVIDENCE LENS / TAP TO EXAMINE",
"lens_h":"See the claim. Then inspect its evidence.",
"lens_desc":"Every statement has a source, a bounded witness, and something it cannot establish. This is a read-only navigation layer—not a live integrity test.",
"tabs":["Portable evidence","One authority","Pack controls"],
"controls":["STORY / CLAIM","PROOF / SOURCES"],
"story":[
("Evidence beyond the producing system","The transferred bundle can be inspected for defined integrity and binding checks without a producer application session.","The files must actually be present in a transferred bundle; this statement is about named verifier checks."),
("One canonical decision owner","Registered adapters submit to the Kernel; they may not originate another verdict, receipt, or bundle identity.","This restriction has bounded CI witnesses for registered adapters—not a guarantee about every external system."),
("Readable controls and test fixtures","A CVE Pack declares policy and test inputs, including an illustrative critical CVE expected to produce DENY.","The test definition does not prove a live scanner, production deployment, or independent release authority.")
],
"proof":[
("Inspectable verifier contract","The standalone verifier documents checks on committed artifacts, receipts, ledgers, and optional issuer authentication.","Does not establish external source truth, universally trusted time, replay, or actual payment release."),
("Named repository boundary witness","The repository boundary document describes its registered-adapter gate and forbids local decision, receipt, and bundle origins.","Does not cover arbitrary off-repository adapters or prove a bank's authorization."),
("Actual Pack source and example test inputs","The critical-cve-blocker pack defines an integer CVSS threshold; its cases include an example score of 98/10 and expected DENY.","Expected YAML assertions are not a witnessed live scan or production receipt.")
],
"what":"WHAT IS SUPPORTED","limit":"NOT ESTABLISHED","sources":"INSPECT SOURCE","switch":"Switch between editorial claim and concrete source boundaries.",
"source":[[(STANDALONE,"Verifier scope"),(VERIFIER_IMPL,"Verifier implementation"),(CLAIMS,"Claims register")],[(BOUNDARY,"Boundary closure"),(CLAIMS,"Claims register")],[(CVE_PACK,"Pack policy YAML"),(CVE_TESTS,"Fixture expectations"),(ADMISSION,"Admission ADR")]],
"journey_kicker":"FOLLOW ONE REAL SOURCE EXAMPLE","journey_h":"Trace a Pack, without inventing a receipt.",
"journey_desc":"Choose a published Kernel Pack, select one of six stations, and open its real source material. The final verifier is an independent generic demo, not a receipt generated from your selected Pack.",
"pack_names":["Critical CVE","GHG Scope 1 + 2","ISO 27001"],
"stage_names":["Fixture input","Declared context","Pack policy","Expected decision","Receipt contract","Verifier demo"],
"stage_notes":[
"Read the defined example input. This is a fixture—not live telemetry.",
"Inspect what the Pack declares; an upstream source is not authenticated by its label.",
"Review the rule definition in pack.yaml, including its limits.",
"Read the expected decision from tests/cases.yaml. It is not a fresh execution result.",
"Inspect documented receipt and bundle binding checks, not a generated Pack-specific receipt.",
"Open the unchanged recipient verifier. Its sample is independent of this selected Pack."
],
"pack_scenarios":["CVE fixture: example CVSS 9.8, expected DENY; no real-world scan is being performed.","GHG policy fixture: configured input and expected decision; not an independently measured emission.","ISO 27001 policy-review fixture: declared controls and expected outcome; not an accreditation audit."],
"open":"OPEN ORIGINAL SOURCE","more":"READ PROOF LIMITS","sample":"SELECT AN EXISTING PACK","stage":"SELECT A STATION","separation":"Fixture expectation ≠ actual execution ≠ independent verification ≠ authorization to release.",
"open_lens":"Explore Evidence Lens"
},
"ar":{
"lens_kicker":"عدسة الدليل / افحص الادعاء",
"lens_h":"اقرأ الادعاء، ثم افحص دليله.",
"lens_desc":"لكل عبارة مصدر وشاهد محدود وأمور لا يمكن استنتاجها منه. هذه واجهة استكشاف للمصادر، وليست اختبار سلامة حيًا.",
"tabs":["الأدلة المحمولة","سلطة قرار واحدة","ضوابط الحزم"],
"controls":["الرؤية / الادعاء","الدليل / المصادر"],
"story":[
("أدلة قابلة للفحص خارج نظام المنتج","يمكن فحص سلامة حزمة الأدلة المنقولة وارتباطاتها المعرّفة دون جلسة في تطبيق المنتج الأصلي.","يشترط وجود الملفات فعلًا في الحزمة المستلمة؛ ويتعلق الادعاء بفحوص محددة."),
("صاحب قرار مرجعي واحد","ترسل المحولات المسجلة طلباتها إلى النواة؛ ولا تنشئ قرارًا أو إيصالًا أو هوية حزمة محلية مستقلة.","توجد شواهد CI محددة للمحولات المسجلة، وليس لكل نظام خارجي."),
("قواعد واختبارات يمكن قراءتها","تصرّح حزمة CVE بقواعدها ومدخلات اختبارية؛ ومنها مثال ثغرة حرجة يتوقع منها القرار DENY.","وجود حالة اختبار لا يثبت فحص ماسح حي أو تكامل نشر أو سلطة إفراج مستقلة.")
],
"proof":[
("عقد المحقق القابل للفحص","يوثق المحقق المستقل فحص الملفات المرتبطة والإيصالات والسجل والتوقيع الاختياري تحت إعداد ثقة محدد.","لا يثبت حقيقة المصدر الخارجية أو الوقت الموثوق المستقل أو إعادة التنفيذ أو الإفراج المالي."),
("شاهد موثق لحدود السلطة في المستودع","يوضح مستند الحدود بوابة CI للمحولات المسجلة ومنع اختراع قرار أو إيصال أو هوية حزمة خارج النواة.","لا يشمل محولات خارج المستودع تلقائيًا ولا يثبت تفويض البنك."),
("ملف الحزمة ومدخلات الاختبار الفعلية","تحدد حزمة الثغرات الحرجة عتبة CVSS صحيحة العدد؛ وتتضمن حالاتها مثال 98 من 100 مع توقع DENY.","نتيجة متوقعة في YAML ليست فحصًا حيًا مشهودًا ولا إيصالًا إنتاجيًا.")
],
"what":"ما تدعمه المصادر","limit":"ما لا يثبته ذلك","sources":"افتح المصدر","switch":"بدّل بين صياغة الادعاء وقيود المصادر الأصلية.",
"source":[[(STANDALONE,"نطاق المحقق"),(VERIFIER_IMPL,"تنفيذ المحقق"),(CLAIMS,"سجل الادعاءات")],[(BOUNDARY,"إغلاق حدود السلطة"),(CLAIMS,"سجل الادعاءات")],[(CVE_PACK,"سياسة الحزمة"),(CVE_TESTS,"اختبارات الحزمة"),(ADMISSION,"قرار قبول الأدلة")]],
"journey_kicker":"تتبّع مثالًا موجودًا في المستودع","journey_h":"افحص الحزمة خطوة بخطوة، دون اختلاق إيصال.",
"journey_desc":"اختر حزمة موجودة فعلًا في Kernel، ثم محطة من ست محطات وافتح ملفها الأصلي. المحقق النهائي تجربة عامة مستقلة، وليس إيصالًا صادرًا عن الحزمة المختارة.",
"pack_names":["ثغرة CVE حرجة","انبعاثات GHG 1 و2","مراجعة ISO 27001"],
"stage_names":["مدخلات الاختبار","سياق المصدر","قاعدة الحزمة","القرار المتوقع","عقد الإيصال","المحقق التجريبي"],
"stage_notes":[
"اقرأ المدخلات المحددة في حالة اختبار. ليست قياسًا حيًا.",
"افحص ما تعلنه الحزمة عن مصدرها؛ اسم المصدر لا يثبت أصالته.",
"اقرأ القاعدة الفعلية في pack.yaml وحدودها.",
"اقرأ النتيجة المتوقعة في tests/cases.yaml؛ ليست تنفيذًا جديدًا.",
"راجع توثيق ارتباط الإيصالات والحزم؛ لا يوجد هنا إيصال مخصص للحزمة المختارة.",
"افتح المحقق الأصلي دون تغيير. العينة فيه مستقلة عن الحزمة المختارة."
],
"pack_scenarios":["حالة CVE: درجة 9.8 متوقعة DENY، ولا يجري فحص حقيقي الآن.","حالة GHG: مدخلات وقواعد وقرار متوقع؛ لا يوجد قياس انبعاثات موثّق خارجيًا.","حالة ISO 27001: ضوابط مصرح بها ونتيجة متوقعة؛ ليست مراجعة اعتماد."],
"open":"افتح المصدر الأصلي","more":"حدود الإثبات","sample":"اختر حزمة منشورة","stage":"اختر محطة","separation":"النتيجة المتوقعة ≠ التنفيذ الفعلي ≠ التحقق المستقل ≠ تفويض الإفراج.",
"open_lens":"استكشف عدسة الدليل"
}
}
PACKS=("critical-cve-blocker","ghg-scope-1-2-guard","iso27001-policy-review")
def link(href,label):
    return f'<a href="{esc(href,quote=True)}" target="_blank" rel="noopener noreferrer">{esc(label)} <span aria-hidden="true">↗</span></a>'

def render_lens(lang):
    d=DATA[lang]
    selector="".join(f'<button type="button" class="lens-claim-tab{" is-active" if i==0 else ""}" data-claim="{i}" aria-pressed="{"true" if i==0 else "false"}">{esc(label)}</button>' for i,label in enumerate(d["tabs"]))
    views=[]
    for i in range(3):
        for mode,items in (("story",d["story"]),("proof",d["proof"])):
            title,body,limit=items[i]
            sources="".join(link(href,label) for href,label in d["source"][i])
            hidden="" if i==0 and mode=="story" else " hidden"
            views.append(f'<article class="lens-view" data-claim-panel="{i}" data-lens-mode="{mode}"{hidden}><span class="lens-prompt">{esc(d["what"])}</span><h3>{esc(title)}</h3><p>{esc(body)}</p><div class="lens-boundary"><span>{esc(d["limit"])}</span><p>{esc(limit)}</p></div><div class="lens-source-links"><span>{esc(d["sources"])}</span>{sources}</div></article>')
    return f'''<section id="evidence-lens" class="lens-section section-block" aria-labelledby="evidence-lens-title" data-evidence-lens><div class="section-heading"><p class="eyebrow">{esc(d["lens_kicker"])}</p><h2 id="evidence-lens-title">{esc(d["lens_h"])}</h2><p>{esc(d["lens_desc"])}</p></div><div class="lens-workspace"><div class="lens-rail"><div class="lens-claim-list" role="group" aria-label="{esc(d["lens_h"])}">{selector}</div><span class="lens-note">{esc(d["switch"])}</span></div><div class="lens-inspector"><div class="lens-toolbar" role="group" aria-label="{esc(d["switch"])}"><button type="button" class="is-active" aria-pressed="true" data-lens-toggle="story">{esc(d["controls"][0])}</button><button type="button" aria-pressed="false" data-lens-toggle="proof">{esc(d["controls"][1])}</button></div>{"".join(views)}</div></div></section>'''

def render_journey(lang):
    d=DATA[lang]
    choose="".join(f'<button type="button" data-journey-pack="{pack}" class="journey-pack{" is-active" if i==0 else ""}" aria-pressed="{"true" if i==0 else "false"}">{esc(d["pack_names"][i])}</button>' for i,pack in enumerate(PACKS))
    stations="".join(f'<button type="button" data-journey-step="{i}" aria-pressed="{"true" if i==0 else "false"}" class="journey-station{" is-active" if i==0 else ""}"><span>{i+1:02d}</span>{esc(name)}</button>' for i,name in enumerate(d["stage_names"]))
    return f'''<section class="journey-section section-block" id="source-journey" data-evidence-journey aria-labelledby="journey-title" data-language="{lang}"><div class="section-heading"><p class="eyebrow">{esc(d["journey_kicker"])}</p><h2 id="journey-title">{esc(d["journey_h"])}</h2><p>{esc(d["journey_desc"])}</p></div><p class="journey-field-label">{esc(d["sample"])}</p><div class="journey-packs" role="group" aria-label="{esc(d["sample"])}">{choose}</div><div class="journey-scenario" data-journey-scenario>{esc(d["pack_scenarios"][0])}</div><p class="journey-field-label">{esc(d["stage"])}</p><div class="journey-stations" role="group" aria-label="{esc(d["stage"])}">{stations}</div><div class="journey-detail" aria-live="polite"><div class="journey-detail-copy"><span class="eyebrow" data-journey-number>01 / 06</span><h3 data-journey-title>{esc(d["stage_names"][0])}</h3><p data-journey-description>{esc(d["stage_notes"][0])}</p></div><div class="journey-links"><a data-journey-primary href="{esc(ROOT+"packs/core/"+PACKS[0]+"/tests/cases.yaml",quote=True)}" target="_blank" rel="noopener noreferrer">{esc(d["open"])} ↗</a>{link(CLAIMS,d["more"])}</div></div><p class="journey-separation">{esc(d["separation"])}</p></section>'''

def build_translations_json():
    # Copy only already-authored display text; generated HTML is the source of truth.
    import json
    result={lang:{"stageNames":d["stage_names"],"stageNotes":d["stage_notes"],"scenarios":d["pack_scenarios"]} for lang,d in DATA.items()}
    return json.dumps(result,ensure_ascii=False,separators=(",",":"))
