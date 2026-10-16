"""PayGod bilingual V2 editorial source: canonical home + V2 routes; no verifier or Kernel logic lives here."""
from pathlib import Path
from html import escape
import shutil
import os
import re
from urllib.parse import urljoin
from v2.lens import render_lens, render_journey, build_translations_json

ROOT=Path(__file__).parent
KERNEL="https://github.com/hamadalmunyif/paygod-kernel-mvp"
CLAIMS=KERNEL+"/blob/main/docs/CLAIMS_REGISTER.md"
PACKS=KERNEL+"/tree/main/packs/core"
STANDALONE=KERNEL+"/blob/main/docs/STANDALONE_VERIFIER.md"

COPY={
"en":{
"nav":["Home","How it works","Use cases","Evidence atlas","Verifier"],"github":"Kernel on GitHub","language":"العربية","preview":"PAYGOD V2 / EVIDENCE INFRASTRUCTURE","open":"Explore","next":"Next slide","prev":"Previous slide","current":"Previous edition","eyebrow":"PORTABLE DECISION EVIDENCE","hero1":"Evidence that travels.","hero2":"Authority that stays accountable.","herodesc":"A decision is not its proof. Package the evidence and decision context you actually hold; let another party inspect the bundle beyond the originating system. Source truth, delegated authority and live execution require separate witnesses.","herocta":"Explore the trust path","herocta2":"Open the real verifier","path":"INTERACTIVE TRUST PATH","pathhint":"Use the arrows to move the cards. Select a card to open its real page or repository source.","view":"OPEN PAGE","pill1":"DETERMINISTIC KERNEL","pill2":"PORTABLE BUNDLE","pill3":"INDEPENDENT CHECKS",
"stage":[("Source","What was measured or declared","Declared inputs are not automatically trusted."),("Evidence","Committed bytes and references","Integrity proves content consistency, not source truth."),("Policy","Explicit, versioned rules","See runnable Pack fixtures and tests."),("Decision","One canonical decision authority","An adapter cannot originate the Kernel verdict."),("Receipt","Bound, inspectable artifacts","The receipt carries the claimed decision context."),("Verification","Independent receiving environment","Check bundle properties without re-running policy.")],
"featuretitle":"Built around boundaries, not promises.","features":[("Evidence first","Move files and commitments; do not replace them with a screenshot."),("Single decision path","Keep decision ownership in the canonical Kernel."),("Independent verification","The recipient can check integrity without your app session."),("Explicit limits","Authenticity, time, correctness and authority are separate claims.")],
"casehead":"Real Kernel Pack examples","casetip":"Executable Pack fixtures in source, not integrated production deployments.","cases":[("GHG / SCOPE 1 + 2","Environmental evidence","A Pack evaluates supplied energy and emission fields against declared controls.","ghg-scope-1-2-guard"),("CRITICAL CVE","Software supply-chain controls","A Pack evaluates declared vulnerability severity and gate conditions.","critical-cve-blocker"),("ISO 27001","Governance evidence","A Pack records supplied policy-review control outcomes.","iso27001-policy-review")],
"source":"Source Pack","tests":"Test cases","allcases":"Full existing use-cases page","stagehead":"Trust is a series of separately testable statements.","stagelabel":"HOW IT WORKS","steps":[("01 / OBSERVE","Declare the fact","Provide source, context and a known contract. Do not assume an external measurement is authenticated."),("02 / EVALUATE","Apply a rule","The canonical Kernel evaluates explicitly supplied data. Schema preadmission is not universal."),("03 / PACKAGE","Bind artifacts","Manifest and receipts commit to the included evidence and decision context."),("04 / TRANSFER","Leave the system","The recipient gets portable artifacts, not credentials or the producer's database."),("05 / CHECK","Independently verify","The verifier checks declared integrity and bindings. It does not certify the real-world event.")],
"atlashead":"What does a PASS actually prove?","atlasdesc":"Inspect the boundary of every claim before extending the product to payments, agents or industrial use.","claims":[("Integrity","Checks committed bytes and bundle bindings","Does not show the measurement was true."),("Authenticity","May inspect a signature under an explicit trust configuration","A signature alone does not prove authority."),("Provenance","Requires independently grounded source attribution","Self-declared origin is not independent provenance."),("Correctness","Requires rule and input validity tests","Matching hashes does not establish policy correctness."),("Time authority","Requires a trusted independent time source","Repository timestamps are not an external time authority."),("Execution authority","Requires an actual release gate and witness","An evidence card is not permission to move money.")],
"readatlas":"Existing detailed evidence atlas","readclaims":"Canonical claims register",
"verifhead":"Inspect the actual verifier.","verifdesc":"The original v0.4 verifier remains unchanged. This V2 page only presents it within the new visual language. Its checks concern the received bundle, not underlying source truth or delegated release authority.","launch":"Open the full verifier","offline":"Verifier technical documentation","frame":"Existing independent verifier interface (original v0.4)","framenote":"The embedded panel below loads the existing /verifier/ route on this preview deployment. Its controls remain in English.","legacy":"OPEN EXISTING EXPERIENCE","legacylink":"View the original PayGod homepage","footer":"Evidence infrastructure · Scope-bound claims · No new Kernel capability asserted."},
"ar":{
"nav":["الرئيسية","كيف يعمل","حالات الاستخدام","أطلس الأدلة","المحقق"],"github":"النواة على GitHub","language":"English","preview":"PAYGOD V2 / بنية الأدلة","open":"استعرض","next":"الشريحة التالية","prev":"الشريحة السابقة","current":"الإصدار السابق","eyebrow":"أدلة قرار قابلة للنقل","hero1":"الدليل ينتقل.","hero2":"ومسؤولية القرار تبقى واضحة.","herodesc":"القرار ليس إثبات صحته. ننقل الأدلة وسياق القرار المتاحين فعلاً ليتمكن طرف مستقل من فحص الحزمة خارج نظام المنتج. صحة المصدر والتفويض والتنفيذ الفعلي تحتاج شواهد أخرى مستقلة.","herocta":"استعرض مسار الثقة","herocta2":"افتح المحقق الفعلي","path":"مسار الثقة التفاعلي","pathhint":"حرّك الشرائح بالأسهم، واضغط على أي شريحة للانتقال إلى الصفحة أو ملف المستودع الحقيقي.","view":"افتح الصفحة","pill1":"نواة قرار حتمية","pill2":"حزمة أدلة متنقلة","pill3":"فحوص مستقلة",
"stage":[("المصدر","ما تم قياسه أو التصريح به","المدخلات المعلنة ليست موثوقة تلقائيًا."),("الدليل","ملفات والتزامات محتوى","سلامة الملف لا تثبت حقيقة المصدر."),("السياسة","قواعد صريحة ومؤرخة","حزم قابلة للتنفيذ مع اختبارات موثقة."),("القرار","سلطة قرار واحدة للنواة","لا يحق للمحول اختراع قرار نيابة عن النواة."),("الإيصال","ربط نتيجة القرار بالأدلة","يحمل الإيصال السياق المعلن للقرار."),("التحقق","بيئة استقبال مستقلة","فحص سلامة الحزمة دون إعادة تنفيذ السياسة.")],
"featuretitle":"حدود قابلة للفحص، لا وعود واسعة.","features":[("الدليل أولًا","ننقل الملفات والتزاماتها، لا مجرد صور من الشاشة."),("مسار قرار واحد","تبقى سلطة القرار في النواة المرجعية."),("تحقق مستقل","يمكن للمستلم فحص سلامة الأدلة دون جلسة داخل التطبيق."),("حدود صريحة","الأصالة والزمن والصحة والسلطة ادعاءات مختلفة.")],
"casehead":"أمثلة فعلية لحزم النواة","casetip":"حزم واختبارات بمستودع المصدر، وليست تكاملات إنتاجية مثبتة.","cases":[("GHG / النطاقان 1 و2","أدلة الانبعاثات","تقيّم الحزمة حقول الطاقة والانبعاثات المقدمة مقابل ضوابط معلنة.","ghg-scope-1-2-guard"),("CVE الحرج","ضوابط سلسلة البرمجيات","تقيّم الحزمة درجة خطورة ثغرة مُدخلة وشروط قرار التحكم.","critical-cve-blocker"),("ISO 27001","أدلة الحوكمة","تسجل الحزمة نتائج مراجعة ضوابط السياسة المقدمة.","iso27001-policy-review")],
"source":"ملف الحزمة","tests":"حالات الاختبار","allcases":"حالات الاستخدام في الموقع الحالي","stagehead":"الثقة سلسلة من ادعاءات منفصلة قابلة للاختبار.","stagelabel":"كيف يعمل","steps":[("01 / المصدر","تحديد الحقيقة المدعاة","نربط المصدر والسياق والعقد. لا نفترض أن القياس الخارجي موثوق."),("02 / التقييم","تطبيق القاعدة","تقيّم النواة بيانات مُدخلة صراحة؛ لا يوجد فرض تلقائي شامل لكل مخططات الحزم."),("03 / التجميع","ربط المخرجات","يربط البيان والإيصالات الأدلة المتضمنة وسياق القرار."),("04 / النقل","العبور إلى الطرف الآخر","يتسلم المراجع ملفات مستقلة لا بيانات دخول أو قاعدة بيانات المنتج."),("05 / الفحص","تحقق مستقل","يفحص المحقق السلامة والارتباطات المعلنة، ولا يصادق على الحدث الواقعي.")],
"atlashead":"ماذا يثبت اجتياز التحقق تحديدًا؟","atlasdesc":"افحص حدود كل ادعاء قبل التوسع في المدفوعات والوكلاء والعمليات الصناعية.","claims":[("السلامة","اتساق الملفات والالتزامات والربط","لا تثبت أن القياس صحيح."),("الأصالة","فحص توقيع ضمن إعداد ثقة صريح","التوقيع وحده لا يثبت التفويض."),("المنشأ","يتطلب نسبة للمصدر مؤيدة بشاهد مستقل","إعلان المصدر عن نفسه ليس منشأ مستقلًا."),("صحة القرار","تتطلب اختبارات المدخلات والقواعد","تطابق البصمات لا يثبت صحة السياسة."),("الزمن الموثوق","يحتاج مصدر وقت خارجيًا موثوقًا","تاريخ المستودع ليس سلطة وقت مستقلة."),("سلطة التنفيذ","تحتاج بوابة إفراج وشاهد تنفيذ فعلي","إيصال الأدلة ليس إذنًا بتحويل الأموال.")],
"readatlas":"أطلس الأدلة التفصيلي الحالي","readclaims":"سجل الادعاءات المرجعي",
"verifhead":"افحص المحقق الفعلي.","verifdesc":"لم نغير محرك التحقق v0.4. هذه الصفحة تقدمه ضمن الهوية التجريبية فقط. فحوصه تخص الحزمة المستلمة، لا حقيقة المصدر أو التفويض بالإفراج.","launch":"فتح المحقق الكامل","offline":"توثيق المحقق التقني","frame":"واجهة المحقق المستقل الحالية (v0.4)","framenote":"تظهر أدناه واجهة /verifier/ القائمة في نفس معاينة Vercel، وتظل عناصر التحكم التقنية بالإنجليزية.","legacy":"استعراض النسخة المعتمدة","legacylink":"استعرض النسخة الأولى للموقع","footer":"بنية أدلة منشورة · ادعاءات محددة النطاق · دون إضافة قدرات للنواة."}
}

ROUTES={"home":"","how":"how-it-works/","cases":"use-cases/","atlas":"atlas/","verifier":"verifier/"}
def url(lang, name): return "/v2/"+("ar/" if lang=="ar" else "")+ROUTES[name]
def ext(link, label):
    return f'<a href="{escape(link,quote=True)}" target="_blank" rel="noopener noreferrer">{escape(label)} <span aria-hidden="true">↗</span></a>'
def logo():
    return """<svg class="monogram" viewBox="0 0 160 112" role="img" aria-label="PayGod PG geometric monogram"><g fill="none" stroke="currentColor" stroke-linejoin="round" stroke-linecap="round"><path stroke-width="5" d="M29 25V10l51 32 51-32v15c18 3 29 17 29 37 0 23-17 39-40 39h-10L80 81l-30 20H40C17 101 0 84 0 62c0-20 11-34 29-37Z" transform="translate(2 -1) scale(.97)"/><circle cx="51" cy="64" r="24" stroke-width="8"/><circle cx="111" cy="64" r="24" stroke-width="8"/><path stroke-width="4" d="M68 47L96 30M66 82L95 100"/></g></svg>"""
def escape_str(s): return escape(str(s))
def make_nav(lang, current, t):
    labels=t["nav"]; keys=list(ROUTES.keys())
    anchors="".join(f'<a class="{"selected" if current==k else ""}" href="{url(lang,k)}">{escape_str(label)}</a>' for k,label in zip(keys,labels))
    anchors += ('<a class="' + ('selected' if current == 'developers' else '') +
                '" href="' + ('/ar/developers/' if lang == 'ar' else '/developers/') +
                '">' + ('للمطورين' if lang == 'ar' else 'Developers') + '</a>')
    anchors += ('<a class="' + ('selected' if current == 'lab' else '') +
                '" href="' + ('/ar/lab/' if lang == 'ar' else '/lab/') +
                '">' + ('مختبر الأدلة' if lang == 'ar' else 'Evidence Lab') + '</a>')
    swap="ar" if lang=="en" else "en"
    swap_link = (
        ("/ar/developers/" if lang == "en" else "/developers/") if current == "developers"
        else ("/ar/lab/" if lang == "en" else "/lab/") if current == "lab"
        else url(swap, current)
    )
    return f'<header class="site-header"><div class="header-inner"><a class="brand" href="{url(lang,"home")}" aria-label="PayGod home">{logo()}<span>PayGod</span></a><nav aria-label="{"التنقل الرئيسي" if lang=="ar" else "Main navigation"}">{anchors}</nav><div class="header-tools"><a class="lang-switch" lang="{swap}" hreflang="{swap}" href="{swap_link}">{t["language"]}</a><a class="header-cta" href="/verifier/">{escape_str(t["nav"][4])}<span aria-hidden="true"> ↗</span></a></div></div></header>'
def stage_cards(lang,t):
    dest=[url(lang,"atlas"),url(lang,"atlas"),KERNEL+"/blob/main/packs/core/critical-cve-blocker/pack.yaml",url(lang,"how"),url(lang,"verifier"),"/verifier/"]
    cards=[]
    for i,((title,body,note),link) in enumerate(zip(t["stage"],dest)):
        rel=' target="_blank" rel="noopener noreferrer"' if link.startswith("https:") else ""
        cards.append(f'<a class="stage-card" href="{escape(link,quote=True)}"{rel} data-stage="{i}" aria-label="{escape_str(title)} — {escape_str(t["view"])}"><span class="card-index">{i+1:02d} / 06</span><span class="stage-emblem" aria-hidden="true"><span>{i+1:02d}</span></span><strong>{escape_str(title)}</strong><small>{escape_str(body)}</small><em>{escape_str(note)}</em><span class="stage-link">{escape_str(t["view"])} <b aria-hidden="true">↗</b></span></a>')
    return f'<div class="path-visual"><div class="orbit" aria-hidden="true"></div><div class="path-meta"><span class="eyebrow">{escape_str(t["path"])}</span><span class="path-counter" data-counter>01 / 06</span></div><div class="rail-wrapper"><div class="stage-rail" data-rail aria-label="{escape_str(t["path"])}">{"".join(cards)}</div></div><div class="rail-foot"><p>{escape_str(t["pathhint"])}</p><div class="rail-arrows"><button type="button" class="rail-arrow" data-prev aria-label="{escape_str(t["prev"])}">←</button><button type="button" class="rail-arrow" data-next aria-label="{escape_str(t["next"])}">→</button></div></div></div>'
def hero(lang,t):
    features="".join(f'<article class="value-card"><span class="value-index">{i+1:02d}</span><h3>{escape_str(name)}</h3><p>{escape_str(desc)}</p></article>' for i,(name,desc) in enumerate(t["features"]))
    cards="".join(f'<a class="case-teaser" href="{url(lang,"cases")}#{code}"><span class="case-overline">{escape_str(k)}</span><h3>{escape_str(name)}</h3><p>{escape_str(desc)}</p><span class="case-open">{escape_str(t["open"])} ↗</span></a>' for k,name,desc,code in t["cases"])
    return f'''<section class="hero-shell"><div class="hero-copy"><p class="eyebrow"><span class="tiny-gold"></span>{escape_str(t["eyebrow"])}</p><div class="hero-brand">{logo()}<span>PayGod</span></div><h1>{escape_str(t["hero1"])}<br><span>{escape_str(t["hero2"])}</span></h1><p class="hero-desc">{escape_str(t["herodesc"])}</p><div class="actions"><a class="btn btn-primary" href="{url(lang,"how")}">{escape_str(t["herocta"])} <span>↗</span></a><a class="btn btn-ghost" href="/verifier/">{escape_str(t["herocta2"])} <span>↗</span></a></div><div class="hero-pills"><span>{escape_str(t["pill1"])}</span><span>{escape_str(t["pill2"])}</span><span>{escape_str(t["pill3"])}</span></div></div>{stage_cards(lang,t)}</section><section class="section-block"><div class="section-heading"><p class="eyebrow">BOUNDARY PRINCIPLES</p><h2>{escape_str(t["featuretitle"])}</h2></div><div class="value-grid">{features}</div></section><section class="section-block"><div class="section-heading section-heading-row"><div><p class="eyebrow">IMPLEMENTED FIXTURES / NOT DEPLOYED INTEGRATIONS</p><h2>{escape_str(t["casehead"])}</h2><p>{escape_str(t["casetip"])}</p></div><a class="text-action" href="{url(lang,"cases")}">{escape_str(t["open"])} ↗</a></div><div class="teaser-grid">{cards}</div></section>'''
def how_page(lang,t):
    content="".join(f'<article class="step-panel" id="step-{i+1}"><span class="step-no">{escape_str(code)}</span><div><h2>{escape_str(name)}</h2><p>{escape_str(desc)}</p></div><span class="step-decoration" aria-hidden="true">↗</span></article>' for i,(code,name,desc) in enumerate(t["steps"]))
    return f'<section class="subhero"><p class="eyebrow">{escape_str(t["stagelabel"])}</p><h1>{escape_str(t["stagehead"])}</h1><p>{escape_str(t["herodesc"])}</p></section><div class="steps-layout">{content}</div><div class="callout"><span>{escape_str(t["readclaims"])}</span>{ext(CLAIMS,t["readclaims"])}</div>'
def cases_page(lang,t):
    contents=[]
    for i,(code,title,desc,pack) in enumerate(t["cases"]):
        root=KERNEL+"/blob/main/packs/core/"+pack
        contents.append(f'<article class="case-detail" id="{pack}"><div class="case-detail-heading"><span class="case-overline">{i+1:02d} / {escape_str(code)}</span><h2>{escape_str(title)}</h2><p>{escape_str(desc)}</p></div><div class="case-links">{ext(root+"/pack.yaml",t["source"])}{ext(root+"/tests/cases.yaml",t["tests"])}</div></article>')
    real=url(lang,"home")
    existing="/ar/use-cases/" if lang=="ar" else "/use-cases/"
    return f'<section class="subhero"><p class="eyebrow">KERNEL PACKS / VERIFIED SCOPE</p><h1>{escape_str(t["casehead"])}</h1><p>{escape_str(t["casetip"])}</p></section><div class="details-grid">{"".join(contents)}</div><div class="callout"><span>{escape_str(t["allcases"])}</span><a href="{existing}">{escape_str(t["allcases"])} ↗</a></div>'
def atlas_page(lang,t):
    entries="".join(f'<article class="claim-row"><div><h3>{escape_str(head)}</h3><p>{escape_str(check)}</p></div><span>{escape_str(no)}</span></article>' for head,check,no in t["claims"])
    existing="/ar/" if lang=="ar" else "/explore/"
    return f'<section class="subhero"><p class="eyebrow">CLAIMS / BOUNDARIES</p><h1>{escape_str(t["atlashead"])}</h1><p>{escape_str(t["atlasdesc"])}</p></section><div class="claim-grid">{entries}</div><div class="callout"><a href="{existing}">{escape_str(t["readatlas"])} ↗</a>{ext(CLAIMS,t["readclaims"])}</div>'
def verifier_page(lang,t):
    return f'<section class="subhero"><p class="eyebrow">INDEPENDENT VERIFIER / UNCHANGED ENGINE</p><h1>{escape_str(t["verifhead"])}</h1><p>{escape_str(t["verifdesc"])}</p><div class="actions"><a class="btn btn-primary" href="/verifier/">{escape_str(t["launch"])} ↗</a><a class="btn btn-ghost" href="{STANDALONE}" target="_blank" rel="noopener noreferrer">{escape_str(t["offline"])} ↗</a></div></section><section class="verifier-preview"><div class="frame-head"><span class="status-dot"></span>{escape_str(t["frame"])}</div><p>{escape_str(t["framenote"])}</p><iframe src="/verifier/" title="{escape_str(t["frame"])}" loading="lazy" referrerpolicy="no-referrer"></iframe></section>'
def build_page(lang,which):
    t=COPY[lang];dirs='rtl' if lang=="ar" else 'ltr'
    other="ar" if lang=="en" else "en"
    body={"home":hero,"how":how_page,"cases":cases_page,"atlas":atlas_page,"verifier":verifier_page}[which](lang,t)
    if which == "home":
        body = body.replace('<section class="section-block">', render_journey(lang) + render_lens(lang) + '<section class="section-block">', 1)
        eik_link = '/ar/developers/' if lang == 'ar' else '/developers/'
        eik_title = 'ابنِ Pack خاصًا بك — دليل EIK للمطورين والوكلاء' if lang == 'ar' else 'Build your own Pack — EIK for developers and agents'
        eik_limit = 'تكامل مرجعي اصطناعي؛ دون ماسح حي أو تفويض نشر.' if lang == 'ar' else 'Synthetic reference only; no live scanner or deployment authorization.'
        body += '<section class="section-block"><div class="callout"><span>' + escape_str(eik_limit) + '</span><a href="' + eik_link + '">' + escape_str(eik_title) + ' ↗</a></div></section>'
        lab_link = '/ar/lab/' if lang == 'ar' else '/lab/'
        lab_title = 'جرّب مختبر الأدلة التفاعلي' if lang == 'ar' else 'Try the interactive Evidence Lab'
        lab_limit = 'سياسة CVE تعليمية وتحقيق سلامة فعلي لحزمة اصطناعية.' if lang == 'ar' else 'Illustrative CVE policy + real integrity checks on a synthetic bundle.'
        body += '<section class="section-block"><div class="callout"><span>' + escape_str(lab_limit) + '</span><a href="' + lab_link + '">' + escape_str(lab_title) + ' ↗</a></div></section>'
    elif which == "how":
        body += render_journey(lang)
    elif which == "atlas":
        body += render_lens(lang)
    return f'''<!doctype html><html lang="{lang}" dir="{dirs}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#070b0e"><meta name="description" content="PayGod V2 visual exploration of portable decision evidence, canonical Kernel, and independent verification."><title>PayGod V2 — {escape_str(t["nav"][list(ROUTES).index(which)])}</title><link rel="alternate" hreflang="en" href="{url("en",which)}"><link rel="alternate" hreflang="ar" href="{url("ar",which)}"><link rel="stylesheet" href="/v2/assets/style.css"><link rel="stylesheet" href="/v2/assets/lens.css"></head><body><a class="skip-link" href="#content">Skip to content</a>{make_nav(lang,which,t)}<main id="content" class="container"><div class="preview-strip"><span class="status-dot"></span>{escape_str(t["preview"])}<a href="{"/v1/ar/home/" if lang=="ar" else "/v1/"}">{escape_str(t["current"])} ↗</a></div>{body}<section class="bottom-banner"><div>{logo()}<p>PORTABLE EVIDENCE <span> / </span> INDEPENDENT VERIFICATION</p></div>{ext(CLAIMS,t["readclaims"])}</section></main><footer><div class="container footer-inner"><a href="{url(lang,"home")}" class="footer-brand">PayGod <span>V2</span></a><p>{escape_str(t["footer"])}</p><a href="{"/v1/ar/home/" if lang=="ar" else "/v1/"}">{escape_str(t["legacylink"])} ↗</a></div></footer><script defer src="/v2/assets/interactions.js"></script><script type="application/json" id="v2-lens-translations">{build_translations_json()}</script><script defer src="/v2/assets/lens.js"></script></body></html>'''
def _archive_previous_home(original, language):
    """Keep the previous self-contained landing accessible at /v1/ with working links."""
    original_base = "/" if language == "en" else "/ar/home/"
    def retarget(m):
        value = m.group(2)
        if not value or value.startswith(("#", "/", "http:", "https:", "mailto:", "data:")):
            return m.group(0)
        path = urljoin(original_base, value)
        if path == "/":
            path = "/v1/"
        elif path == "/ar/home/":
            path = "/v1/ar/home/"
        return m.group(1) + path + '"'
    original = re.sub(r'((?:href|src)=")([^"]+)"', retarget, original)
    original = original.replace('<meta name="robots" content="index,follow">', '<meta name="robots" content="noindex,nofollow">')
    original = re.sub(r'<link rel="canonical" href="[^"]+">', '', original)
    return original


def _published_home(language, production):
    """One source of truth for the live homepage and the /v2/ edition."""
    html = build_page(language, "home")
    # The entry URLs are canonical; supporting V2 routes remain under /v2/.
    html = html.replace('href="/v2/ar/"', 'href="/ar/home/"')
    html = html.replace('href="/v2/"', 'href="/"')
    html = html.replace('href="/v2/ar/"', 'href="/ar/home/"')
    html = html.replace('href="/v2/"', 'href="/"')
    html = html.replace(
        '<link rel="alternate" hreflang="en" href="/">',
        '<link rel="alternate" hreflang="en" href="https://paygod.net/">')
    html = html.replace(
        '<link rel="alternate" hreflang="ar" href="/ar/home/">',
        '<link rel="alternate" hreflang="ar" href="https://paygod.net/ar/home/">')
    html = html.replace(
        '<meta name="description" content="PayGod V2 visual exploration of portable decision evidence, canonical Kernel, and independent verification.">',
        '<meta name="description" content="' +
        ('PayGod بنية أدلة قابلة للنقل وقرارات محددة النطاق، مع مسارات تحقق مستقل ومصادر مفتوحة قابلة للفحص.' if language == "ar"
         else 'PayGod makes decision evidence portable, with inspectable Kernel sources, bounded claims and independent verification.') + '">')
    html = html.replace(
        '<title>PayGod V2 — ' + ('الرئيسية' if language == 'ar' else 'Home') + '</title>',
        '<title>' + ('PayGod — أدلة قرار قابلة للنقل والتحقق المستقل' if language == 'ar'
                     else 'PayGod — Portable Evidence & Independent Verification') + '</title>')
    if production:
        canonical = 'https://paygod.net/ar/home/' if language == 'ar' else 'https://paygod.net/'
        html = html.replace(
            '<meta name="robots" content="noindex,nofollow">',
            '<meta name="robots" content="index,follow"><link rel="canonical" href="' + canonical + '">', 1)
    return html


def build_v2(dist):
    assets=dist/"v2"/"assets"
    assets.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/"style.css",assets/"style.css")
    shutil.copyfile(ROOT/"interactions.js",assets/"interactions.js")
    shutil.copyfile(ROOT/"lens.css",assets/"lens.css")
    shutil.copyfile(ROOT/"lens.js",assets/"lens.js")
    for lang in ("en","ar"):
        for name,slug in ROUTES.items():
            path=dist/"v2"/("ar" if lang=="ar" else "")/slug/"index.html"
            path.parent.mkdir(parents=True,exist_ok=True)
            markup=build_page(lang,name)
            path.write_text(markup,encoding="utf-8")
            print("Built V2 "+str(path.relative_to(dist))+" ("+str(len(markup.encode()))+" bytes)")

    # Produce standalone, source-linked bilingual developer guidance from the
    # same V2 design system. This is an editorial route, not a hosted EIK SDK.
    from v2.developers import render as render_developer
    production = os.environ.get("VERCEL_ENV") == "production"
    for language in ("en", "ar"):
        output = dist / ("ar/developers/index.html" if language == "ar" else "developers/index.html")
        output.parent.mkdir(parents=True, exist_ok=True)
        markup = render_developer(
            language, production,
            lambda loc: make_nav(loc, "developers", COPY[loc]),
            logo, CLAIMS,
        )
        output.write_text(markup, encoding="utf-8")
        print("Built EIK developer guide " + str(output.relative_to(dist)))

    # Educational evidence-lab pages reuse the unmodified browser verifier as a static module.
    from v2.evidence_lab import build as build_lab
    build_lab(dist, production, lambda loc, current: make_nav(loc, current, COPY[loc]))

    # Preserve old homepages and promote V2 without touching verifier, atlas or use-case outputs.
    for lang, live, archive in (
        ("en", "index.html", "v1/index.html"),
        ("ar", "ar/home/index.html", "v1/ar/home/index.html"),
    ):
        old_path = dist / live
        old_html = old_path.read_text(encoding="utf-8")
        archived = dist / archive
        archived.parent.mkdir(parents=True, exist_ok=True)
        archived.write_text(_archive_previous_home(old_html, lang), encoding="utf-8")
        old_path.write_text(_published_home(lang, production), encoding="utf-8")
        print("Promoted V2 -> " + live + "; archived original -> " + archive)

