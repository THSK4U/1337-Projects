*This project has been created as part of the 42 curriculum by tsellak.*

# Call Me Maybe — مقدمة في استدعاء الدوال باستخدام نماذج اللغة الكبيرة (LLMs)

---

## الوصف

هذا المشروع يطلب منك بناء أداة تحوّل الأوامر المكتوبة بلغة طبيعية إلى استدعاءات دوال منظمة بصيغة JSON، باستخدام نموذج لغوي صغير (Qwen3-0.6B) وتقنية تسمى **Constrained Decoding**.

**مثال:**

```
المدخل:  "What is the sum of 40 and 2?"
المخرج:  { "name": "fn_add_numbers", "parameters": { "a": 40.0, "b": 2.0 } }
```

النظام لا يجيب على السؤال مباشرة، بل يُخرج اسم الدالة المناسبة ومعاملاتها بالأنواع الصحيحة.

---

## المفاهيم الأساسية

---

### ١. استدعاء الدوال (Function Calling)

**ماذا؟**
هي تقنية تحوّل طلبًا مكتوبًا بلغة بشرية عادية إلى استدعاء دالة برمجية منظمة. مثلاً: الجملة *"Reverse the string 'hello'"* تتحول إلى:

```json
{ "name": "fn_reverse_string", "parameters": { "s": "hello" } }
```

**لماذا؟**
لأن نماذج اللغة الكبيرة (LLMs) تفهم اللغة البشرية لكنها لا تُنتج مخرجات منظمة بشكل طبيعي. هذه التقنية تجعل النموذج قادرًا على التفاعل مع أنظمة خارجية (APIs)، تنفيذ أكواد، وتحويل النصوص إلى بيانات مهيكلة يمكن للبرامج استخدامها.

**كيف؟**
يُعطى النموذج **الأمر** (prompt) مع **تعريفات الدوال المتاحة** (function definitions)، ثم يختار الدالة المناسبة ويستخرج المعاملات (arguments) بأنواعها الصحيحة. يتم فرض صحة المخرج باستخدام **Constrained Decoding**.

---

### ٢. فك التشفير المقيّد (Constrained Decoding)

**ماذا؟**
هي تقنية تتدخل في عملية توليد النص عند النموذج، حيث تُجبره على إنتاج مخرجات تتبع بنية معينة (في حالتنا: JSON صالح يتوافق مع schema محدد). بدلاً من "الأمل" أن النموذج يُنتج JSON صحيح، نحن **نفرض** ذلك.

**لماذا؟**
لأن النماذج الصغيرة مثل Qwen3-0.6B تنجح في إنتاج JSON صحيح فقط حوالي **30%** من الوقت عند الاعتماد على الـ prompting وحده. لكن بالـ Constrained Decoding نحصل على **100%** صحة في بنية JSON. هذا يثبت أن **التوجيه البنيوي** أقوى من حجم النموذج.

**كيف؟**
في كل خطوة من توليد token جديد:

1. النموذج يُعطي درجات احتمالية (**logits**) لكل token ممكن.
2. نحدد أي tokens ستُحافظ على بنية JSON صالحة وتتوافق مع الـ schema.
3. نضع احتمالية كل token **غير صالح** على سالب ما لا نهاية (`-∞`).
4. نختار فقط من الـ tokens **الصالحة** المتبقية.

**مثال:** إذا كان الحقل `"name"` لا يقبل إلا `"fn_add_numbers"` أو `"fn_greet"` أو `"fn_reverse_string"`، فالـ decoder يمنع أي قيمة أخرى.

---

### ٣. خط أنابيب التوليد (LLM Generation Pipeline)

**ماذا؟**
هي المراحل التي يمر بها النص — من أمر بلغة طبيعية إلى مخرج النموذج — token بـ token.

**لماذا؟**
لأن فهم هذه المراحل ضروري لتطبيق Constrained Decoding بشكل صحيح. التدخل يحصل تحديدًا بعد مرحلة الـ **Logits** وقبل اختيار الـ Token التالي.

**كيف؟**

```
Prompt → Tokenization → Input IDs → LLM → Logits → Token Selection
```

| المرحلة            | الشرح                                                                                                                                                |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Prompt**          | الأمر بلغة طبيعية:*"What is the sum of 2 and 3?"*                                                                                        |
| **Tokenization**    | تقسيم النص إلى وحدات فرعية (tokens):`["What", "Ġis", "Ġthe", ...]` — الرمز `Ġ` يعني مسافة قبل الكلمة |
| **Input IDs**       | تحويل الـ tokens إلى أرقام يفهمها النموذج:`[892, 318, 262, ...]`                                                           |
| **LLM Processing**  | الشبكة العصبية تعالج الأرقام                                                                                                     |
| **Logits**          | النموذج يُخرج احتمالية لكل token ممكن                                                                                          |
| **Token Selection** | يتم اختيار الـ token الأعلى احتمالية —**هنا يتم تطبيق Constrained Decoding**                                  |

هذه العملية تتكرر token بـ token حتى يكتمل المخرج.

---

### ٤. ربط المفردات (Vocabulary Mapping)

**ماذا؟**
ملف JSON يحتوي على جدول ربط بين أرقام الـ tokens (IDs) وتمثيلها النصي. هو الجسر بين عالم الأرقام (النموذج) وعالم النصوص (JSON).

**لماذا؟**
لأننا نحتاج لمعرفة أي token يُنتج أي حرف/كلمة لكي نقرر هل هذا الـ token "صالح" أم لا في السياق الحالي من بنية الـ JSON.

**كيف؟**
الـ SDK يوفر دالة `get_path_to_vocabulary_json()` التي تُرجع مسار هذا الملف. أثناء الـ Constrained Decoding، نحمّل هذا الملف ونستخدمه في كل خطوة توليد للتحقق: "هل هذا الـ token سيُنتج JSON صحيح يتوافق مع الـ schema؟"

---

### ٥. حزمة LLM SDK

**ماذا؟**
هي حزمة جاهزة (`Small_LLM_Model`) توفر واجهة مبسطة للتعامل مع نموذج Qwen3-0.6B.

**لماذا؟**
لأنها تختصر عليك تعقيد تحميل النموذج والـ tokenization والاستنتاج (inference)، فتركّز أنت على منطق **Constrained Decoding**.

**كيف؟**

| الدالة                             | الوصف                                                                   |
| ---------------------------------------- | ---------------------------------------------------------------------------- |
| `get_logits_from_input_ids(input_ids)` | تأخذ input IDs وتُرجع الـ logits الخام من النموذج |
| `get_path_to_vocabulary_json()`        | تُرجع مسار ملف الربط بين الـ tokens والنصوص    |
| `encode(text)`                         | تحوّل نصًا إلى قائمة أرقام token IDs                   |
| `decode(token_ids)`                    | تحوّل أرقام الـ tokens إلى نص (اختياري)             |

> ⚠️ **ممنوع** استخدام أي methods أو attributes خاصة (private) من الـ `llm_sdk`.

---

## ما المطلوب منك بالتحديد؟

### ملفات الإدخال (`data/input/`)

- **`function_calling_tests.json`** — مصفوفة من الأوامر بلغة طبيعية:

  ```json
  [
    { "prompt": "What is the sum of 2 and 3?" },
    { "prompt": "Greet shrek" },
    { "prompt": "Reverse the string 'hello'" }
  ]
  ```
- **`functions_definition.json`** — تعريفات الدوال المتاحة (الاسم، المعاملات، الأنواع):

  ```json
  {
    "name": "fn_add_numbers",
    "description": "Add two numbers together and return their sum.",
    "parameters": { "a": { "type": "number" }, "b": { "type": "number" } }
  }
  ```

### ملف الإخراج (`data/output/function_calling_results.json`)

لكل أمر، كائن JSON يحتوي:

```json
{
  "prompt": "What is the sum of 2 and 3?",
  "name": "fn_add_numbers",
  "parameters": { "a": 2.0, "b": 3.0 }
}
```

### قواعد التحقق

- الملف يجب أن يكون JSON صالح (بدون فواصل زائدة أو تعليقات)
- المفاتيح والأنواع يجب أن تتطابق مع الـ schema في `functions_definition.json`
- جميع المعاملات المطلوبة يجب أن تكون موجودة
- **ممنوع** عمل hardcode للحلول

---

## التعليمات

### المتطلبات

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

### التثبيت

```bash
git clone <repository-url>
cd CALL_ME
uv sync
```

### التشغيل

```bash
# الاستخدام الافتراضي
uv run python -m src

# مع مسارات مخصصة
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

### أوامر Makefile

| الأمر       | الوصف                                  |
| ---------------- | ------------------------------------------- |
| `make install` | تثبيت التبعيات                 |
| `make run`     | تشغيل البرنامج                 |
| `make debug`   | تشغيل في وضع التصحيح (pdb) |
| `make clean`   | حذف الملفات المؤقتة        |
| `make lint`    | فحص `flake8` و `mypy`               |

---

## معايير الأداء المطلوبة

| المعيار                   | الهدف               |
| -------------------------------- | ------------------------ |
| دقة اختيار الدالة | 90%+                     |
| صحة بنية JSON             | 100%                     |
| وقت المعالجة          | أقل من 5 دقائق |
| معالجة الأخطاء      | بدون أي crash      |

---

## القيود والقواعد الأساسية

- ✅ استخدم `pydantic` لجميع الـ classes
- ✅ يمكنك استخدام `numpy` و `json`
- ✅ اتبع معيار `flake8` و `mypy`
- ✅ Type hints إلزامية لكل الدوال
- ✅ Docstrings إلزامية (PEP 257)
- ❌ **ممنوع** استخدام dspy, pytorch, huggingface, transformers, outlines
- ❌ **ممنوع** استخدام heuristics بدلاً من LLM لاختيار الدالة
- ❌ **ممنوع** الاعتماد على prompting وحده لإنتاج JSON صحيح

---

## هيكل المشروع

```
CALL_ME/
├── src/                  # الكود المصدري الرئيسي
├── llm_sdk/              # حزمة SDK للتعامل مع النموذج
├── data/
│   ├── input/            # ملفات الإدخال (الأوامر + تعريفات الدوال)
│   └── output/           # المخرجات (لا تُرفع على git)
├── Makefile              # أتمتة البناء والتشغيل
├── pyproject.toml        # إعدادات المشروع والتبعيات
├── uv.lock               # ملف قفل التبعيات
└── README.md             # هذا الملف
```



## حوّل الـcache لـ `goinfre`

<pre><div node="[object Object]" class="relative whitespace-pre-wrap word-break-all my-2 rounded-lg bg-list-hover-subtle border border-gray-500/20"><div class="min-h-7 relative box-border flex flex-row items-center justify-between rounded-t border-b border-gray-500/20 px-2 py-0.5"><div class="font-sans text-sm text-ide-text-color opacity-60">bash</div><div class="flex flex-row gap-2 justify-end"></div></div><div class="p-3"><div class="w-full h-full text-xs cursor-text"><div class="code-block"><div class="code-line" data-line-number="1" data-line-start="1" data-line-end="1"><div class="line-content"><span class="mtk6">export</span><span class="mtk1"></span><span class="mtk10">UV_CACHE_DIR</span><span class="mtk3">=</span><span class="mtk1">/</span><span class="mtk10">goinfre</span><span class="mtk1">/</span><span class="mtk10">tsellak</span><span class="mtk1">/.</span><span class="mtk10">cache</span><span class="mtk1">/</span><span class="mtk10">uv</span></div></div><div class="code-line" data-line-number="2" data-line-start="2" data-line-end="2"><div class="line-content"><span class="mtk16">uv</span><span class="mtk1"></span><span class="mtk12">sync</span></div></div></div></div></div></div></pre>

h,

---

## المراجع

- [Qwen3-0.6B Model](https://huggingface.co/Qwen/Qwen3-0.6B) — النموذج اللغوي المستخدم
- [Constrained Decoding](https://huggingface.co/blog/constrained-beam-search) — شرح تقنية التوليد المقيّد
- [Pydantic Documentation](https://docs.pydantic.dev/) — مكتبة التحقق من البيانات
- [Function Calling in LLMs](https://platform.openai.com/docs/guides/function-calling) — دليل OpenAI لاستدعاء الدوال

### استخدام الذكاء الاصطناعي

تم استخدام أدوات الذكاء الاصطناعي في:

- فهم خوارزمية Constrained Decoding وأسسها النظرية
- تصحيح حالات حدية في ربط الـ tokens وفرض schema الـ JSON
- إنشاء هيكل التوثيق الأولي
