"""Bilingual educational Evidence Lab. Neither a second Kernel nor a verifier implementation."""
from html import escape
from pathlib import Path
import shutil

HERE = Path(__file__).parent
KERNEL = "https://github.com/hamadalmunyif/paygod-kernel-mvp"
PACK = KERNEL + "/blob/main/packs/core/critical-cve-blocker/pack.yaml"
TESTS = KERNEL + "/blob/main/packs/core/critical-cve-blocker/tests/cases.yaml"

TEXT = {
 "en": {
  "title":"Evidence Lab", "tag":"INTERACTIVE / BOUNDED / SYNTHETIC",
  "lead":"Explore a policy expectation. Then test real evidence-integrity checks.",
  "intro":"Two distinct activities: the CVE control is a browser-only educational model of an existing Pack; the evidence challenge calls the unchanged PayGod browser verifier v0.4 against a prepared synthetic bundle.",
  "home":"Home", "switch":"العربية", "back":"Back to the site",
  "cve":"01 / CVE policy explorer", "cvdesc":"Change a prepared single-vulnerability observation. This is an illustrative expected outcome, NOT a Kernel execution, authenticated scanner result, or permission to deploy.",
  "score":"CVSS score (×10 integer)", "status":"Installed remediation state",
  "unfixed":"Unpatched / fix not confirmed", "fixed":"Patched: installed version independently confirmed",
  "complete":"Scanner finished successfully; all required fields present (illustrative admission)",
  "expected":"Expected Pack outcome, not executed", "withheld":"WITHHELD / NOT RUN",
  "withheldwhy":"Mandatory source information is absent or incomplete. Admission is withheld before invoking Kernel.",
  "deny":"DENY", "denywhy":"An unpatched critical finding with CVSS ≥ 9.0 meets the first Pack rule.",
  "flag":"FLAG", "flagwhy":"An unpatched high finding with 7.0 ≤ CVSS < 9.0 meets the second Pack rule.",
  "allow":"ALLOW", "allowwhy":"No unpatched high/critical finding is present in this single-fixture illustration. This is not a clean-scan guarantee.",
  "warning":"The upstream Trivy status fixed means a fix is available, not necessarily installed. This demo's Patched choice explicitly assumes separately confirmed installed-version evidence.",
  "packlink":"Inspect actual Pack YAML", "testlink":"Read source fixtures",
  "evidence":"02 / Byte-change challenge",
  "evdesc":"Run the unchanged browser verifier on a synthetic transfer. Compare the intact sample against the same bundle after altering its measurement file. No new receipt, manifest, hash, or verdict is invented by this page.",
  "clean":"Verify intact sample", "tamper":"Change a measurement and verify",
  "state":"Verifier result", "unrun":"NOT RUN", "checking":"CHECKING", "verified":"INTEGRITY VERIFIED", "failed":"INTEGRITY FAILED", "failure":"Unable to run verifier",
  "verificationNote":"Integrity verification does not prove the source measurement was true, policy was correct, signature authority, replay, trusted time, or downstream permission. Issuer trust keys are deliberately not loaded in this small challenge.",
  "recipient":"Open standalone recipient verifier", "producer":"Open original producer demo", "docs":"Canonical claim limits",
  "source":"SOURCE / BOUNDARY", "sourceText":"The CVE slider never calls Kernel. The integrity challenge imports the exact existing v0.4 verifier module as an unchanged static asset and uses an existing generated synthetic bundle; it is not a new independent institution or financial release gate.",
  "readout":"Ready. Select a challenge to run the verifier."
 },
 "ar": {
  "title":"مختبر الأدلة", "tag":"تفاعلي / محدود / اصطناعي",
  "lead":"استكشف نتيجة سياسة متوقعة، ثم اختبر سلامة الأدلة بالمتحقق الحقيقي.",
  "intro":"تجربتان منفصلتان: حالة CVE نموذج تعليمي داخل المتصفح لسياسة Pack موجودة، بينما اختبار العبث يستدعي متحقق PayGod v0.4 دون تعديل على حزمة أدلة اصطناعية محفوظة.",
  "home":"الرئيسية", "switch":"English", "back":"العودة للموقع",
  "cve":"01 / استكشاف سياسة الثغرات", "cvdesc":"غيّر تقريرًا افتراضيًا يحوي ثغرة واحدة. النتيجة المتوقعة توضيحية؛ ليست تنفيذًا للـ Kernel أو تقرير ماسح موثوقًا أو إذنًا بالنشر.",
  "score":"درجة CVSS (عدد صحيح ×10)", "status":"حالة الإصلاح المثبت على النظام",
  "unfixed":"غير مُرقّع / لم يثبت الإصلاح", "fixed":"مُرقّع: ثُبتت النسخة المثبتة بدليل مستقل",
  "complete":"اكتمل الفحص بنجاح وتوفرت الحقول الإلزامية (قبول تمثيلي)",
  "expected":"النتيجة المتوقعة للسياسة، لا قرار منفذ", "withheld":"WITHHELD / NOT RUN",
  "withheldwhy":"المصدر الإلزامي ناقص أو غير مكتمل؛ يحجب القبول قبل استدعاء Kernel.",
  "deny":"DENY", "denywhy":"ثغرة حرجة غير مرقعة بدرجة CVSS لا تقل عن 9.0 تحقق قاعدة المنع الأولى.",
  "flag":"FLAG", "flagwhy":"ثغرة عالية غير مرقعة بدرجة CVSS بين 7.0 وأقل من 9.0 تحقق قاعدة التنبيه.",
  "allow":"ALLOW", "allowwhy":"لا توجد ثغرة عالية/حرجة غير مرقعة في هذا المثال المفرد. ليس هذا إثباتًا لسلامة فحص شامل.",
  "warning":"حالة fixed في Trivy تعني توفر إصلاح، لا إثبات تثبيته. خيار «مُرقّع» هنا يفترض تحققًا منفصلًا من نسخة البرنامج المثبتة.",
  "packlink":"افحص ملف Pack الفعلي", "testlink":"اختبارات السياسة في المستودع",
  "evidence":"02 / تحدي تغيير بايتات الدليل",
  "evdesc":"شغّل المتحقق الحالي على حزمة اصطناعية منقولة. قارن العينة السليمة بالعينة نفسها بعد تغيير ملف القياس. هذه الواجهة لا تنشئ إيصالًا أو بيانًا أو بصمة أو قرارًا بديلًا.",
  "clean":"تحقق من العينة السليمة", "tamper":"غيّر القياس ثم تحقق",
  "state":"نتيجة المتحقق", "unrun":"لم يُشغّل", "checking":"جارٍ التحقق", "verified":"اجتازت الحزمة تحقق السلامة", "failed":"فشل التحقق من السلامة", "failure":"تعذر تشغيل المتحقق",
  "verificationNote":"سلامة الحزمة لا تثبت صحة القياس، أو صحة السياسة، أو سلطة الموقّع، أو إعادة التنفيذ، أو صحة الزمن، أو تفويض الإجراء. لا تُحمّل هذه التجربة المختصرة مفاتيح ثقة المصدر.",
  "recipient":"افتح المتحقق المستقل للمستلم", "producer":"افتح تجربة المُنتج الأصلية", "docs":"حدود الادعاءات المثبتة",
  "source":"المصدر وحدود الادعاء", "sourceText":"لا يستدعي شريط CVE النواة. وتستورد تجربة سلامة الأدلة وحدة متحقق v0.4 الحالية كما هي، مع حزمة اصطناعية موجودة. هذا لا يمثل اعتمادًا مؤسسيًا مستقلًا أو إذنًا بتنفيذ مالي.",
  "readout":"جاهز. اختر اختبارًا لتشغيل المتحقق."
 }
}

def render(lang, production, nav):
    t = TEXT[lang]
    uri = "/ar/lab/" if lang == "ar" else "/lab/"
    alt = "/lab/" if lang == "ar" else "/ar/lab/"
    direction = "rtl" if lang == "ar" else "ltr"
    home = "/ar/home/" if lang == "ar" else "/"
    seo = ('<meta name="robots" content="index,follow"><link rel="canonical" href="https://paygod.net' + uri + '">'
           if production else '<meta name="robots" content="noindex,nofollow">')
    def e(value): return escape(value, quote=True)
    return f'''<!doctype html>
<html lang="{lang}" dir="{direction}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#070b0e">{seo}
<title>PayGod — {e(t["title"])}</title>
<meta name="description" content="{e(t["intro"])}">
<link rel="alternate" hreflang="en" href="https://paygod.net/lab/">
<link rel="alternate" hreflang="ar" href="https://paygod.net/ar/lab/">
<link rel="stylesheet" href="/v2/assets/style.css">
<link rel="stylesheet" href="/lab/assets/lab.css"></head>
<body><a class="skip-link" href="#content">{e(t["title"])}</a>
{nav(lang, "lab")}
<main id="content" class="container lab-shell">
<header class="lab-intro"><p class="eyebrow">{e(t["tag"])}</p><h1>{e(t["lead"])}</h1>
<p>{e(t["intro"])}</p><a class="lab-back" href="{home}">← {e(t["back"])}</a></header>
<section class="lab-card" aria-labelledby="cve-title">
<div class="lab-card-head"><span class="lab-number">01</span><div><h2 id="cve-title">{e(t["cve"])}</h2><p>{e(t["cvdesc"])}</p></div></div>
<div class="lab-layout">
<div class="lab-controls"><label for="cve-score">{e(t["score"])}: <output id="cve-value" for="cve-score">9.5</output></label>
<input id="cve-score" type="range" min="0" max="100" step="1" value="95">
<label for="remediation">{e(t["status"])}</label>
<select id="remediation"><option value="unfixed">{e(t["unfixed"])}</option><option value="fixed">{e(t["fixed"])}</option></select>
<label class="lab-checkbox"><input type="checkbox" id="scan-complete" checked> {e(t["complete"])}</label>
</div><div class="lab-result" aria-live="polite"><p>{e(t["expected"])}</p>
<strong id="cve-outcome" data-state="deny">{e(t["deny"])}</strong>
<span id="cve-reason">{e(t["denywhy"])}</span></div></div>
<p class="lab-caution">{e(t["warning"])}</p>
<div class="lab-links"><a href="{PACK}" target="_blank" rel="noopener noreferrer">{e(t["packlink"])} ↗</a>
<a href="{TESTS}" target="_blank" rel="noopener noreferrer">{e(t["testlink"])} ↗</a></div>
</section>
<section class="lab-card" aria-labelledby="integrity-title">
<div class="lab-card-head"><span class="lab-number">02</span><div><h2 id="integrity-title">{e(t["evidence"])}</h2><p>{e(t["evdesc"])}</p></div></div>
<div class="lab-buttons">
<button type="button" id="verify-clean" data-challenge="clean">{e(t["clean"])}</button>
<button type="button" id="verify-tampered" data-challenge="tampered">{e(t["tamper"])}</button></div>
<div class="lab-result" aria-live="polite"><p>{e(t["state"])}</p>
<strong id="integrity-outcome" data-state="idle">{e(t["unrun"])}</strong>
<span id="integrity-detail">{e(t["readout"])}</span>
<small id="integrity-checks"></small></div>
<p class="lab-caution">{e(t["verificationNote"])}</p>
<div class="lab-links"><a href="{"/v1/ar/home/" if lang == "ar" else "/v1/"}">{e(t["producer"])} ↗</a>
<a href="/verifier/">{e(t["recipient"])} ↗</a>
<a href="{KERNEL}/blob/main/docs/CLAIMS_REGISTER.md" target="_blank" rel="noopener noreferrer">{e(t["docs"])} ↗</a></div></section>
<section class="lab-source"><h2>{e(t["source"])}</h2><p>{e(t["sourceText"])}</p></section>
</main>
<script type="application/json" id="lab-labels">{__import__("json").dumps({k:t[k] for k in ("withheld","withheldwhy","deny","denywhy","flag","flagwhy","allow","allowwhy","checking","verified","failed","failure")},ensure_ascii=False).replace("<","\\\\u003c")}</script>
<script type="module" src="/lab/assets/lab.js"></script></body></html>'''

def build(dist, production, nav):
    assets = dist / "lab" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for asset in ("lab.css", "lab.js"):
        shutil.copyfile(HERE / asset, assets / asset)
    source = HERE.parent / "src"
    for asset in ("sha256.mjs", "verifier.mjs"):
        shutil.copyfile(source / asset, assets / asset)
    # The generated synthetic sample is the same fixture used by the existing producer workspace.
    shutil.copyfile(HERE.parent / "demo" / "sample.json", assets / "sample.json")
    for lang, path in (("en", "lab/index.html"), ("ar", "ar/lab/index.html")):
        dest = dist / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render(lang, production, nav), encoding="utf-8")
        print("Built bounded Evidence Lab " + path)
