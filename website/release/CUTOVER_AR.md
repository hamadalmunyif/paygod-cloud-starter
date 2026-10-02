# خطة إطلاق PayGod — 2 أكتوبر 2026

الحالة: تجهيز للمراجعة؛ لم ينفذ نشر Production ولم تعدل GoDaddy أو DNS.

## ما أُنجز

- أضيف paygod.net وwww.paygod.net في مشروع Vercel paygod-evidence-preview كربط تمهيدي ببيئة Production.
- يعرض كلا النطاقين Invalid Configuration لأن DNS لم يوجه إلى Vercel. لا توجد نسخة Production في المشروع بعد.
- نجح اختبار المستخدم على الآيباد: VALID، جميع الفحوص 11/11، دون أخطاء. هذا تقرير أرسله المستخدم، وليس إثبات تشغيل دون إنترنت.
- أُعد production.patch واختُبر تطبيقه في نسخة مؤقتة فقط. لم يتغير إعداد المعاينة الفعلي.

## القيم الدقيقة المعروضة في Vercel

| النوع | الاسم | القيمة الجديدة | القديم حسب صور 30 سبتمبر |
|---|---|---|---|
| A | @ | 216.198.79.1 | WebsiteBuilder Site؛ الرقم الفعلي غير متاح في الصور |
| CNAME | www | 04de084ca186f6de.vercel-dns-017.com. | paygod.net. |

تؤخذ نسخة جديدة من منطقة DNS من GoDaddy قبل التنفيذ، وتراجع أي سجلات A/AAAA متعارضة. لا تستخدم وصف WebsiteBuilder Site كعنوان IP للاستعادة.

## تسلسل التنفيذ بعد الاعتماد

1. إنشاء فرع website/paygod-production من آخر نسخة مراجعة، وتطبيق production.patch فيه. لا يدمج في master.
2. تغيير فرع Production لهذا المشروع فقط إلى website/paygod-production. يبقى Root Directory=website وBuild=python3 build.py وOutput=dist.
3. نشر الإنتاج وفحصه على رابط Vercel قبل لمس DNS. يسمح شرط البناء بالإنتاج من هذا الفرع وحده؛ يسمح بالمعاينات ويمنع إنتاج master.
4. الصفحة الرئيسية تستخدم canonical https://paygod.net/ وتسمح بالفهرسة في الإنتاج فقط. يبقى verifier وdownloads دون فهرسة. www يعاد توجيهه دائمًا إلى paygod.net مع الحفاظ على المسار.
5. حفظ سجلات DNS الأصلية ومراجعة استعادة GoDaddy Website Builder. لا تلغ اشتراكه ولا تحذف الموقع القديم.
6. تعديل سجلي A وCNAME بالقيم أعلاه بعد الموافقة النهائية. تبقى ملكية النطاق وnameservers في GoDaddy؛ تحفظ سجلات البريد وTXT وDMARC و_domainconnect.
7. فحص HTTPS وpaygod.net وwww والتحويل وأداة التحقق والتنزيل. لا يعد الإطلاق ناجحًا قبل هذه الفحوص.

## الرجوع

قبل تغيير DNS نحتاج قيم الاستعادة الفعلية أو مسار إعادة ربط Website Builder المؤكد. عند فشل النقل تستعاد السجلات السابقة من النسخة المأخوذة مباشرة قبل التنفيذ. الانتشار ليس فوريًا. بعد أول نشر ناجح يمكن الرجوع بين نسخ Vercel عند الحاجة.

## قيد باقٍ

اختبار تنزيل الحزمة ثم تشغيل ملف HTML على جهاز مفصول عن الإنترنت لم يُثبت بعد. لا يدعي الإطلاق اكتمال هذا الاختبار أو التحقق من هوية المصدر أو صدق القياس الواقعي.

## مراجع التنفيذ

معاينة المحتوى: https://paygod-evidence-preview-3ypduajqg-paygod1.vercel.app/
إعداد النطاقات: https://vercel.com/paygod1/paygod-evidence-preview/settings/domains
وثائق Vercel: https://vercel.com/docs/domains/working-with-domains/add-a-domain
