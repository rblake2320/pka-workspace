# FORGE — Shared AI Toolkit

**Status**: Built and tested. 25/25 tests passing. Installed at `C:\Users\techai\toolkit\`.

---

## What Was Built

A shared Python package (`ai-toolkit`) installed at `C:\Users\techai\toolkit\` that works
as Lego bricks — any project imports only what it needs, nothing else loads.

### Files created

```
C:\Users\techai\toolkit\
├── pyproject.toml                          installable package config
├── README.md                               full usage docs with examples
├── tests\test_toolkit_core.py             25 tests, all passing
└── toolkit\
    ├── __init__.py
    ├── _credentials.py                     auto-loads ~/.nvidia.env + ~/.env
    ├── _exceptions.py                      ToolkitDependencyError, ToolkitAuthError
    ├── vision\
    │   ├── base.py                         OCRClient ABC, OCRResult, DetectionClient ABC
    │   ├── ocr\
    │   │   ├── nemo.py                     NeMo Retriever OCR (adapted from DataShield)
    │   │   ├── easy.py                     EasyOCR — handwriting, non-Latin scripts
    │   │   ├── tesseract.py               Tesseract — clean printed text, no GPU
    │   │   ├── paddle.py                   PaddleOCR — Asian langs, dense text
    │   │   └── router.py                   OCRRouter — auto-pick + fallback chain
    │   └── detection\
    │       ├── base.py
    │       ├── clip.py                     CLIP zero-shot image classification
    │       └── router.py                   DetectionRouter
    └── llm\
        ├── base.py                         LLMClient ABC, LLMResponse
        └── router.py                       LLMRouter — task-aware, cost-optimized
```

`C:\Users\techai\DataShield\src\browser\ocr_client.py` was updated to a thin
backwards-compatible re-export shim. All existing DataShield imports continue to work
without any change.

---

## How to Add the Toolkit to a New Project

Three lines, done:

```bash
# 1. Install into your project's venv — pick only what you need
pip install -e "C:/Users/techai/toolkit[nemo,llm]"
```

```python
# 2. Import and use — credentials are auto-loaded, nothing else to configure
from toolkit.vision.ocr.router import OCRRouter
from toolkit.llm.router import LLMRouter
```

```ini
# 3. Credentials already live in C:\Users\techai\.nvidia.env and .env — done
```

Available extras groups for step 1:

| Extra | What it installs |
|-------|-----------------|
| `nemo` | requests + Pillow (NeMo OCR cloud/local) |
| `easy` | easyocr + Pillow |
| `tesseract` | pytesseract + Pillow + pandas |
| `paddle` | paddleocr + paddlepaddle-gpu |
| `paddle-cpu` | paddleocr + paddlepaddle (CPU only) |
| `clip` | torch + torchvision + transformers + Pillow |
| `llm` | anthropic |
| `all` | everything except GPU paddle |

---

## How to Add a New Tool to the Toolkit

1. Create `toolkit/toolkit/<category>/<name>.py`
2. Inherit from the base class for that category:
   - OCR: `from toolkit.vision.base import OCRClient, OCRResult`
   - Detection: `from toolkit.vision.base import DetectionClient, DetectionResult`
   - LLM: `from toolkit.llm.base import LLMClient, LLMResponse`
3. Implement the single abstract method (`extract_text`, `classify`, or `complete`)
4. Wrap all heavy imports in `__init__` with `ToolkitDependencyError` on ImportError
5. Add an extras group in `pyproject.toml`
6. Add a factory function and entry to the relevant `router.py` chain
7. Add tests to `tests/test_toolkit_core.py`

Minimal new OCR backend (annotated template):

```python
from toolkit._exceptions import ToolkitDependencyError
from toolkit.vision.base import OCRClient, OCRResult

class MyOCR(OCRClient):
    def __init__(self):
        try:
            import mylib             # lazy — only loads when this class is used
        except ImportError:
            raise ToolkitDependencyError(
                package="mylib",
                extras="mylib",      # maps to pyproject.toml [extras.mylib]
                pip_packages="mylib",
            )
        self._lib = mylib

    def extract_text(self, image_path: str) -> OCRResult:
        import time
        t0 = time.perf_counter()
        try:
            text = self._lib.run(image_path)
            return OCRResult(
                full_text=text,
                model="mylib",
                source=image_path,
                latency_ms=(time.perf_counter() - t0) * 1000,
            )
        except Exception as exc:
            return OCRResult(full_text="", error=str(exc), source=image_path)
```

---

## Lego Patterns — Which Tools Work Together for Which Use Cases

### Pattern 1: Screenshot automation (Playwright, DataShield)
Best for: capturing text from rendered web pages, CAPTCHAs, UI testing.

```python
from toolkit.vision.ocr.router import OCRRouter
from toolkit.vision.detection.router import DetectionRouter
from toolkit.llm.router import LLMRouter

ocr = OCRRouter()
detector = DetectionRouter()
llm = LLMRouter()

# Detect what kind of page this is, then extract and analyze
page_type = detector.classify(screenshot, labels=["login", "form", "confirmation", "error"])
text = ocr.route(screenshot, hint="screenshot")  # NeMo cloud → EasyOCR fallback

if page_type.label == "form":
    fields = llm.route("extract", prompt=f"Extract all field names and values:\n{text.full_text}")
```

### Pattern 2: Document ingestion pipeline
Best for: scanned PDFs, typed forms, printed invoices.

```python
from toolkit.vision.ocr.tesseract import TesseractOCR
from toolkit.llm.router import LLMRouter

ocr = TesseractOCR(preprocess=True)   # built-in grayscale + threshold cleanup
llm = LLMRouter()

text = ocr.extract_text("scanned_invoice.png")
data = llm.route("extract", prompt=f"Extract: vendor, amount, date, line items.\n{text.full_text}")
```

### Pattern 3: Multi-language document processing
Best for: Chinese, Japanese, Korean, Arabic, Hindi documents.

```python
from toolkit.vision.ocr.paddle import PaddleOCR    # Chinese/Japanese/Korean
from toolkit.vision.ocr.easy import EasyOCR         # Arabic, mixed scripts
from toolkit.llm.router import LLMRouter

zh_ocr = PaddleOCR(lang="ch")
ar_ocr = EasyOCR(languages=["ar"])
llm = LLMRouter()

zh_text = zh_ocr.extract_text("chinese_doc.png")
translation = llm.route("translate", prompt=f"Translate to English:\n{zh_text.full_text}")
```

### Pattern 4: Zero-shot content moderation / image classification
Best for: content safety, document type detection, UI state detection.

```python
from toolkit.vision.detection.clip import CLIPDetector

detector = CLIPDetector()   # downloads CLIP model once, caches locally
result = detector.classify(
    "upload.png",
    labels=["safe content", "adult content", "violence", "spam", "misinformation"]
)
if result.label != "safe content" and result.score > 0.7:
    flag_for_review(result.label, result.score)
```

### Pattern 5: Cost-aware LLM routing across task types
Best for: pipelines with mixed task complexity — pay Haiku rates for simple
classifications and Opus rates only when the task demands it.

```python
from toolkit.llm.router import LLMRouter

router = LLMRouter()

# Cheap tasks automatically go to Haiku
tags = router.route("classify", prompt="Is this an invoice, receipt, or contract?")

# Complex tasks automatically escalate to Sonnet/Opus
analysis = router.route("analyze", prompt="Identify all risk factors in this legal clause...")

# Legal-grade — always goes to Opus, no downgrade
letter = router.route("legal", prompt="Draft a GDPR data deletion request for...")

# Check what you spent
report = router.get_cost_report()
print(report["_totals"]["cost_usd"])
```

### Pattern 6: DataShield integration (existing project)
DataShield's existing code continues to work unchanged. New DataShield
code can import from the toolkit directly for cleaner dependencies:

```python
# Old code (still works — backwards-compatible shim in place)
from browser.ocr_client import NeMoOCRClient

# New code (use toolkit directly)
from toolkit.vision.ocr.nemo import NeMoOCR
from toolkit.vision.ocr.router import OCRRouter   # adds auto-fallback
```

---

## Key Design Decisions

**Why lazy imports**: Importing `from toolkit.vision.ocr.nemo import NeMoOCR` never
touches EasyOCR or PaddleOCR. The module files import nothing heavy at the top level.
Heavy library imports only happen inside `__init__` of each class, which runs only
when you instantiate that specific client.

**Why credentials auto-load**: `_credentials.py` runs `load_dotenv()` at import time
(once, module-level). `python-dotenv` respects already-set env vars — it never
overwrites a key the OS already has. Projects that set env vars before importing the
toolkit keep their values. Projects that do nothing get the keys from the env files.

**Why results never raise**: OCR and detection results return `OCRResult.error` rather
than raising exceptions. This is intentional — a failed OCR call in a pipeline should
not crash the pipeline; it should be logged and the next tool should be tried. The router
exploits this contract to implement fallback without try/except boilerplate.

**Why LLMRouter does raise**: `ToolkitCallError` from the LLM router is appropriate
because a failed LLM call is usually a genuine pipeline failure, not a gracefully
degradable condition.

---

## Validation Results

```
25 passed in 0.31s
```

Tests cover: exception messages, credential loading, OCRResult dataclass, router
fallback logic, auth guard, NeMoOCR unit logic (parse, availability, missing file).

---

## To Extend the Router Chains

Edit `toolkit/toolkit/vision/ocr/router.py` — the `_ROUTE_TABLE` dict maps
hint strings to ordered lists of `(factory_fn, label)` tuples. Add a new entry or
insert a new tool into an existing chain. The router tries them in order, skipping
any that fail to instantiate or report `is_available() == False`.
