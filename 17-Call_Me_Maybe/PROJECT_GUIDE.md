# دليل مشروع CALL_ME

## ماذا؟ — ما هو المشروع

مشروع **CALL_ME** يطلب منك بناء نظام يحوّل أوامرًا بلغة طبيعية (مثل: *"What is the sum of 40 and 2?"*) إلى استدعاءات دوال منظمة بصيغة **JSON**، باستخدام:
- نموذج لغوي صغير: **Qwen3-0.6B**
- تقنية **Constrained Decoding** لضمان 100% صحة في بنية JSON

---

## لماذا؟ — لماذا هذا مهم قبل البدء

فهم ثلاثة مفاهيم جوهرية هو **شرط أساسي** قبل أي كود:

| المفهوم | لماذا تحتاجه؟ |
|---------|--------------|
| **Function Calling** | لتفهم ما يجب أن يُنتجه النظام |
| **Constrained Decoding** | هو القلب الفعلي للمشروع — بدونه لا يعمل شيء |
| **LLM Generation Pipeline** | لتعرف **أين بالضبط** تتدخل في عملية التوليد |

---

## كيف؟ — الخطوات الكاملة للإنجاز

### 🟦 المرحلة الأولى: الفهم النظري *(قبل لمس أي كود)*

**الخطوة 1 — افهم pipeline النموذج:**
اقرأ الجدول في `README.md` تحت قسم "خط أنابيب التوليد"، وافهم المراحل الست جيدًا:
```text
Prompt → Tokenization → Input IDs → LLM → Logits → Token Selection
```
تذكّر أن تدخلك يحصل **بعد Logits وقبل اختيار الـ Token**.

**الخطوة 2 — افهم Constrained Decoding بعمق:**
اقرأ الشرح المرفق في README عن Constrained Beam Search. الفكرة الجوهرية:
> في كل خطوة توليد، نُجبر النموذج على اختيار token يُنتج JSON صالحًا فقط — عن طريق وضع `-inf` على كل token غير صالح.

---

### 🟩 المرحلة الثانية: استكشاف الكود الموجود

**الخطوة 3 — استكشف هيكل المشروع:**
- افتح مجلد `llm_sdk/` وافهم الدوال الأربع المتاحة:
  - `get_logits_from_input_ids(input_ids)` ← الأهم
  - `get_path_to_vocabulary_json()` ← جسرك بين tokens والنصوص
  - `encode(text)` و `decode(token_ids)`
- افتح `data/input/` لترى ملفي الإدخال: `function_calling_tests.json` و `functions_definition.json`

**الخطوة 4 — نفّذ المشروع وتأكد أنه يعمل:**
```bash
make install
make run
```
> إذا لم يعمل، هذا طبيعي — مجلد `src/` فارغ وأنت من ستملأه.

---

### 🟨 المرحلة الثالثة: بناء المنطق خطوة بخطوة

بنِ مشروعك بهذا الترتيب المنطقي:

**الخطوة 5 — بناء الـ Prompt:**
تعلّم كيف تُركّب prompt يشمل:
1. تعريفات الدوال المتاحة (من ملف `functions_definition.json`)
2. الأمر المطلوب (prompt المستخدم)
3. توجيه للنموذج لإنتاج JSON بتنسيق محدد

**الخطوة 6 — بناء JSON Schema:**
تعلّم بنية **JSON Schema** لأنك ستحتاج أن تعرّف للـ Constrained Decoder ما الذي يُعتبر JSON صالحًا. مثال:
```json
{"name": "اسم الدالة", "parameters": {"a": 0, "b": 0}}
```
يجب أن تبني هذا الـ schema **ديناميكيًا** من ملف `functions_definition.json`.

**الخطوة 7 — بناء Constrained Decoder:**
هذا هو قلب المشروع. ستبني حلقة توليد token بـ token:
1. أخذ الـ `input_ids` الحالية
2. الحصول على `logits` عبر `get_logits_from_input_ids()`
3. تحميل vocabulary وفحص أي tokens تُنتج JSON صالحًا مع الـ schema
4. وضع `-inf` على كل token غير صالح
5. اختيار أعلى token احتمالية من الباقي
6. إضافته لـ `input_ids` والتكرار حتى اكتمال JSON

**الخطوة 8 — ربط كل شيء:**
اكتب الكود الرئيسي في `src/` الذي:
1. يقرأ ملف الأوامر `function_calling_tests.json`
2. لكل أمر: يبني الـ prompt → يشغّل Constrained Decoder → يُخرج JSON
3. يكتب النتائج في `data/output/function_calling_results.json`

---

### 🟥 المرحلة الرابعة: التحقق والتنظيف

**الخطوة 9 — التحقق من المعايير:**

| المعيار | الهدف |
|---------|-------|
| دقة اختيار الدالة | ≥ 90% |
| صحة بنية JSON | 100% |
| وقت المعالجة | أقل من 5 دقائق |

**الخطوة 10 — الفحص النهائي:**
```bash
make lint    # تحقق من flake8 و mypy
make run     # تأكد أن المخرجات صحيحة
```

---

## ⚠️ تحذيرات مهمة

- لا تستخدم `pytorch`, `transformers`, `outlines` أو `huggingface` مباشرةً
- لا تعمل **hardcode** للحلول — النظام يجب أن يعمل على أي دوال جديدة
- يجب أن تعتمد على **Constrained Decoding حقيقي** وليس prompting فقط
- كل دالة تحتاج **type hints** و **docstring** (إجباري)
