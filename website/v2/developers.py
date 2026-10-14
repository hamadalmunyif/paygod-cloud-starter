"""Static bilingual EIK developer entry; editorial navigation only, no API or verifier authority."""
from html import escape as html_escape

ROOT = "https://github.com/hamadalmunyif/paygod-kernel-mvp"
PAGES = {
    "en": {
        "title": "Developers & AI Agents",
        "subtitle": "Understand the contract. Build your own Pack. Contribute only if you choose.",
        "intro": "PayGod's EIK entry uses an existing deterministic Kernel and portable evidence. Create private policy Packs, compare native tools, and check bounded results. The GitHub Actions reference is a saved synthetic scan, not a live security-scanner or release-authorization integration.",
        "eyebrow": "EIK / SELF-SERVICE / SYNTHETIC REFERENCE",
        "steps": [
            ("Learn the boundary", "Read current implemented capabilities, claims and the Pack YAML contract.", "Learn EIK", "docs/eik/README.md"),
            ("Build privately", "Author and test a private Pack without a PayGod account or mandatory upstream PR.", "Pack examples", "docs/STARTER_PACKS.md"),
            ("Run the reference", "Reproduce saved-report admission, canonical CLI and no-checkout recipient verification.", "Synthetic GitHub example", "examples/eik-github-actions/README.md"),
            ("Contribute optionally", "Send a focused PR only if the improvement belongs in the public repository.", "Contributing guide", "CONTRIBUTING.md"),
        ],
        "agent": "Agent instructions",
        "capabilities": "Machine-readable capability description",
        "status": "Current EIK evidence and unresolved tests",
        "claims": "Read verified claims and limits",
        "warning": "What this does NOT establish",
        "limits": "No authenticated real scanner, no mandatory runtime source admission, no permission to deploy or move funds, no independent organizational adoption, no EIK SDK, MCP/A2A service or Pack marketplace. A valid bundle checks scoped integrity, not source truth or delegated authority.",
        "next": "Next validation required",
        "nextdesc": "Request an unfamiliar developer/agent to repeat the example; test an authorized real saved report; compare against GitHub-native controls and direct CLI; ask a genuinely independent recipient to explain the result and its limits.",
        "back": "Back to home",
    },
    "ar": {
        "title": "للمطورين ووكلاء الذكاء الاصطناعي",
        "subtitle": "افهم العقد. ابنِ Pack خاصًا بك. ساهم فقط إن أردت.",
        "intro": "يتيح مدخل EIK استخدام نواة PayGod الحتمية وأدلتها القابلة للنقل. يمكنك بناء Packs خاصة، ومقارنة الأدوات الأصلية، والتحقق من النتائج ضمن حدودها. مرجع GitHub Actions يستخدم تقرير فحص اصطناعيًا محفوظًا؛ وليس تكامل ماسح حيًا أو تفويضًا للنشر.",
        "eyebrow": "EIK / استخدام مستقل / مثال اصطناعي",
        "steps": [
            ("افهم الحدود", "راجع القدرات المثبتة والعقود وحدود الادعاءات وصيغة YAML.", "دليل EIK", "docs/eik/README.md"),
            ("ابنِ بصورة مستقلة", "أنشئ Pack خاصًا واختبره دون حساب PayGod أو إلزام بتقديم PR.", "أمثلة الـPacks", "docs/STARTER_PACKS.md"),
            ("شغّل المثال", "كرر قبول تقرير محفوظ، وتشغيل CLI المرجعي، والتحقق لدى مستلم دون تنزيل المستودع.", "مرجع GitHub الاصطناعي", "examples/eik-github-actions/README.md"),
            ("ساهم اختياريًا", "قدّم PR محددًا إذا رغبت في إضافة منفعة عامة إلى المستودع.", "دليل المساهمة", "CONTRIBUTING.md"),
        ],
        "agent": "تعليمات وكلاء البرمجة",
        "capabilities": "وصف القدرات القابل للقراءة آليًا",
        "status": "حالة EIK الحالية وما لم يُثبت",
        "claims": "حدود الادعاءات والشواهد",
        "warning": "ما الذي لا يثبته هذا المثال؟",
        "limits": "لم نثبت ماسحًا حقيقيًا موثوق المصدر، ولا فرضًا تلقائيًا عامًا لقبول جميع المدخلات، ولا تفويضًا للنشر أو تحويل الأموال، ولا تبنيًا مؤسسيًا مستقلًا، ولا SDK أو خدمات MCP/A2A أو سوق Packs. سلامة الحزمة لا تثبت حقيقة المصدر أو التفويض.",
        "next": "التحقق الخارجي المطلوب",
        "nextdesc": "نطلب من مطور أو وكيل جديد تكرار المثال، ثم فحص تقرير حقيقي محفوظ بتصريح، ومقارنة أدوات GitHub الأصلية وCLI المباشر، وإجراء تحقق لدى مستلم مستقل يشرح النتيجة وحدودها.",
        "back": "العودة للرئيسية",
    },
}


def render(lang: str, production: bool, make_nav, logo, claims_url: str) -> str:
    text = PAGES[lang]
    alternate = "ar" if lang == "en" else "en"
    uri = "/ar/developers/" if lang == "ar" else "/developers/"
    other_uri = "/ar/developers/" if alternate == "ar" else "/developers/"
    root_home = "/ar/home/" if lang == "ar" else "/"
    css = "/v2/assets/style.css"
    cards = []
    for title, desc, label, path in text["steps"]:
        href = ROOT + "/blob/main/" + path
        cards.append(
            '<article class="case-detail"><div class="case-detail-heading"><h2>' +
            html_escape(title) + '</h2><p>' + html_escape(desc) +
            '</p></div><div class="case-links"><a target="_blank" rel="noopener noreferrer" href="' +
            html_escape(href, quote=True) + '">' + html_escape(label) + ' ↗</a></div></article>'
        )
    refs = [
        (text["agent"], ROOT + "/blob/main/AGENTS.md"),
        (text["capabilities"], ROOT + "/blob/main/docs/eik/capabilities.v0.json"),
        (text["status"], ROOT + "/blob/main/docs/eik/STATUS_2026-10-14.md"),
        (text["claims"], claims_url),
    ]
    links = " ".join(
        '<a href="' + html_escape(href, quote=True) + '" target="_blank" rel="noopener noreferrer">' +
        html_escape(label) + ' ↗</a>' for label, href in refs
    )
    canonical = "https://paygod.net" + uri
    seo = ('<meta name="robots" content="index,follow"><link rel="canonical" href="' +
           canonical + '">' if production else '<meta name="robots" content="noindex,nofollow">')
    # The existing V2 navigation function is supplied as a callable and is used
    # unchanged except for the public developer link included in its nav.
    nav = make_nav(lang)
    return (
        '<!doctype html><html lang="' + lang + '" dir="' + ("rtl" if lang == "ar" else "ltr") +
        '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
        seo + '<meta name="description" content="' + html_escape(text["subtitle"], quote=True) +
        '"><title>PayGod — ' + html_escape(text["title"]) +
        '</title><link rel="alternate" hreflang="' + lang + '" href="' + canonical +
        '"><link rel="alternate" hreflang="' + alternate + '" href="https://paygod.net' +
        other_uri + '"><link rel="stylesheet" href="' + css +
        '"></head><body><a class="skip-link" href="#content">' +
        ("انتقل إلى المحتوى" if lang == "ar" else "Skip to content") +
        '</a>' + nav + '<main class="container" id="content"><section class="subhero"><p class="eyebrow">' +
        html_escape(text["eyebrow"]) + '</p><h1>' + html_escape(text["title"]) +
        '</h1><h2>' + html_escape(text["subtitle"]) + '</h2><p>' + html_escape(text["intro"]) +
        '</p></section><div class="details-grid">' + "".join(cards) +
        '</div><div class="callout">' + links + '</div><section class="section-block"><h2>' +
        html_escape(text["warning"]) + '</h2><p>' + html_escape(text["limits"]) +
        '</p><h2>' + html_escape(text["next"]) + '</h2><p>' + html_escape(text["nextdesc"]) +
        '</p><a class="btn btn-ghost" href="' + root_home + '">' + html_escape(text["back"]) +
        ' ↗</a></section></main><footer><div class="container footer-inner"><p>PayGod — ' +
        html_escape(text["title"]) +
        '</p><a href="' + root_home + '">' + html_escape(text["back"]) +
        ' ↗</a></div></footer></body></html>'
    )
