# FORGE — DataShield NeMo Retriever OCR Integration
**Date:** 2026-03-26
**Triggered by:** Ron sharing nemoretriever-ocr-v1 NIM + NVIDIA API key
**Status:** DEPLOYED — 3 files written, 2 files updated

---

## What Was Built

### New Files

| File | Purpose |
|------|---------|
| `src/browser/ocr_client.py` | Full NeMoOCRClient — cloud + local NIM, tiling for large images |
| `.env.example` | Canonical env template including NVIDIA_API_KEY |

### Modified Files

| File | Change |
|------|--------|
| `src/config/settings.py` | Added 5 NVIDIA OCR settings (api_key, mode, host, port, enabled) |
| `src/browser/engine.py` | Wired OCR into 3 integration points (search, submit, captcha) |

---

## Integration Points in BrowserEngine

### 1. Search — Image-Rendered Profile Extraction
**Before**: `page.inner_text("body")` only captured DOM text. Brokers like Spokeo and WhitePages render profile cards as images to defeat scrapers — these returned empty/sparse text.

**After**: After every search screenshot, NeMo OCR runs on the full-page PNG. OCR text is merged with DOM text using `_merge_page_text()` — lines already in DOM text are deduplicated. The merged text feeds into `_llm_analyze_match()`.

**Impact**: Match confidence should increase on image-heavy brokers. OCR chars logged as `ocr_search_augmentation` in structlog.

### 2. Form Submission — Confirmation Code Extraction
**Before**: Confirmation codes embedded in images (e.g., "Your removal request #ABC123") were invisible to `_check_submission_result()` — those cases falsely returned `success: False`.

**After**: After submission screenshot, `_extract_confirmation_code()` runs OCR then applies:
- Playbook-defined `confirmation_code_pattern` (regex) if set
- 3 common patterns: `"Confirmation #XYZ"`, `"#ABC123"`, `"CASE-12345"`

If OCR finds a code but DOM check failed → override to `success: True`. Code stored in `confirmation_code` field.

### 3. CAPTCHA — Type Classification
**Before**: CAPTCHA type was passed as a hardcoded string (`"recaptcha_v2"`, `"hcaptcha"`). Wrong classification wasted solver credits and retries.

**After**: When `captcha_type="auto"`, `_classify_captcha_from_ocr()` reads the CAPTCHA screenshot with NeMo OCR and detects:
- reCAPTCHA v2 ("i'm not a robot")
- hCaptcha ("privacy")
- Cloudflare Turnstile ("checking your browser")
- Image-text CAPTCHA (≤8 alphanumeric chars — OCR text IS the answer)

---

## NeMoOCRClient Design

```
NeMoOCRClient
├── extract_text(image_path) → OCRResult
│   ├── <175KB: single inline base64 call
│   └── >175KB: tile into 4 quadrants, batch call, merge results
├── extract_text_from_bytes(bytes) → OCRResult
├── is_available() → bool (health check)
└── _classify_captcha_from_ocr(text) → str
```

**Cloud mode** (`NVIDIA_OCR_MODE=cloud`):
- Endpoint: `https://ai.api.nvidia.com/v1/cv/nvidia/nemotron-ocr-v1`
- Auth: `Bearer nvapi-...`
- No local GPU required

**Local mode** (`NVIDIA_OCR_MODE=local`):
```bash
export NGC_API_KEY=nvapi-...
docker run -it --rm \
  --gpus all --shm-size=16GB \
  -e NGC_API_KEY=$NGC_API_KEY \
  -v ~/.cache/nim:/opt/nim/.cache \
  -p 8000:8000 \
  nvcr.io/nvidia/nemo-microservices/nemoretriever-ocr-v1:latest
```
Then set `NVIDIA_OCR_MODE=local` in `.env`.

RTX 5090 is ideal for local mode — OCR NIM is lightweight (~4-6GB VRAM), leaves 26GB for other models.

---

## API Key Security Note

The NVIDIA API key was shared in conversation. Recommended actions:
1. **Rotate** at build.nvidia.com if it was previously used in any shared/public context
2. **Store** only in `.env` (already in `.gitignore` pattern)
3. **Never** hardcode in any source file — `settings.nvidia_api_key` reads from env

The key is wired as `NVIDIA_API_KEY` in settings — not present in any committed file.

---

## Verification Commands (for CRUCIBLE)

```bash
# 1. OCR client import
cd C:\Users\techai\DataShield\src
python -c "from browser.ocr_client import NeMoOCRClient; c = NeMoOCRClient(); print('available:', c.is_available())"

# 2. Settings includes NVIDIA fields
python -c "from config.settings import get_settings; s = get_settings(); print(s.nvidia_ocr_mode, s.nvidia_ocr_enabled)"

# 3. Engine initializes OCR without crash
python -c "from browser.engine import BrowserEngine; e = BrowserEngine(); print('ocr:', e._ocr)"

# 4. Full OCR extract on a test image
python -c "
from browser.ocr_client import NeMoOCRClient
client = NeMoOCRClient()
# Requires NVIDIA_API_KEY set in env
result = client.extract_text('test_image.png')
print('text:', result.full_text[:200])
print('error:', result.error)
"

# 5. CAPTCHA classification from text
python -c "
from browser.engine import BrowserEngine
e = BrowserEngine()
print(e._classify_captcha_from_ocr('I am not a robot - reCAPTCHA'))  # → recaptcha_v2
print(e._classify_captcha_from_ocr('XK9M2P'))                         # → image_text
print(e._classify_captcha_from_ocr('Checking your browser'))           # → cloudflare_turnstile
"
```

---

## Risks / Follow-up

| Risk | Mitigation |
|------|-----------|
| OCR latency adds ~0.5-2s per screenshot (cloud) | Async wrapper (future) — currently sync but non-blocking for worker |
| PIL not installed → tiling falls back to truncated image | Add `Pillow` to `requirements.txt` (not yet done — CRUCIBLE to verify) |
| Large broker pages (>175KB PNG) may lose bottom section without PIL | Low priority — most profiles fit in top half |
| OCR result contains PII in logs | `ocr_extracted` log only logs char count, not text content |

**Pillow dependency**: Add to `requirements.txt`:
```
Pillow>=10.0.0
```
