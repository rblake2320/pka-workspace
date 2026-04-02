# NOVA: OCR and Computer Vision Toolkit Research
**Prepared for:** Ron / AXIOM Workspace
**Date:** 2026-03-26
**Scope:** Best-in-class OCR and CV tools for a shared toolkit at `C:\Users\techai\toolkit\`

---

## 1. Objective

Identify which OCR and computer vision tools should live in Ron's shared toolkit, given existing assets (NeMo Retriever OCR v1, EasyOCR, RTX 5090, Spark-1 GB10), and which tools serve his active projects: DataShield, aihangout.ai, BehaviorShield, IMDS AutoQA, and general browser automation.

---

## 2. Key Findings (ranked by decision impact)

**Finding 1 — PaddleOCR (PP-OCRv5) is the must-have general OCR engine.**
It beats EasyOCR at 3x throughput on RTX hardware (12.7 vs 4.2 FPS on RTX 3080), runs at 15MB total model size vs EasyOCR's 200MB+, covers 100+ languages, supports tables and complex layouts, and costs ~$0.09/1,000 pages self-hosted versus $1.50+ for cloud APIs. PP-OCRv5 (released May 2025) adds a 13-point accuracy gain over v4.

**Finding 2 — NeMo Retriever OCR v1 (already integrated) is best for structured document RAG.**
It has a 19.5% lower character error rate and 56.2% lower bag-of-word error rate versus its benchmark competitor. At 52.5M parameters it is lightweight for a production NIM. Its limitation: English-only, no math/formula support, and it requires Ampere or newer. It is not a replacement for a general OCR layer — it is a precision instrument for the ingestion pipeline.

**Finding 3 — Surya OCR is the accuracy ceiling for document parsing on GPU.**
97.7% invoice accuracy, 97.4% overall in structured benchmarks. It also includes layout detection, reading order, table recognition, and LaTeX/math parsing in one pip install. The tradeoff: it needs 16-20GB VRAM at default batch sizes and carries a non-commercial license restriction (free under $2M revenue, GPL code). For DataShield and IMDS it is the right heavyweight.

**Finding 4 — OmniParser v2 is the only serious answer for UI screen parsing.**
0.6s/frame latency on A100, 39.5% on ScreenSpot Pro (new state of art as of Feb 2025). It is purpose-built for exactly what IMDS AutoQA needs: detecting interactable elements in legacy software screenshots without HTML access. Nothing else in the open-source ecosystem is close.

**Finding 5 — YOLO11 remains the production-safe detection backbone; YOLOv12 is the accuracy leader.**
YOLO11m achieves 2.4ms/frame average inference. YOLOv12 beats YOLO11 by 1.1-2.1% mAP on COCO but is 3-9% slower and has training instability — Ultralytics recommends YOLO11 for most production workloads. BehaviorShield's trained YOLO model is on solid ground and does not need a rebuild.

**Finding 6 — EasyOCR is now a second-tier option and should be kept only for quick prototyping.**
No active development momentum in 2025. PaddleOCR PP-OCRv5 is strictly superior on speed and accuracy for anything beyond simple scenes. EasyOCR's only remaining edge: easier first-run install for experimentation since it has no PaddlePaddle dependency.

**Finding 7 — Florence-2 + SAM2 is the best zero-shot detection + segmentation stack.**
Florence-2 (0.77B, MIT license) provides text-prompted bounding boxes; SAM2 provides pixel-accurate masks at ~44 FPS. Together they replace the need for a custom detection model in most aihangout.ai content moderation workflows. Neither requires fine-tuning for common objects.

**Finding 8 — Cloud OCR APIs are economically indefensible for self-hosted GPU workloads.**
Google Cloud Vision, Azure AI Vision OCR, and AWS Textract all price at $1.50/1,000 pages basic and $10-50/1,000 for structured extraction. Self-hosted VLM-OCR is 167x cheaper per page at H100 scale. On an RTX 5090 the cost advantage is even larger. Cloud APIs are only justified for one-off, no-infra scenarios or for handwriting where cloud models still outperform open-source options.

---

## 3. Evidence and Source Data

### 3.1 OCR Landscape

#### NVIDIA NeMo Retriever OCR v1 (`nemoretriever-ocr-v1`) — ALREADY INTEGRATED

| Metric | NeMo Retriever OCR v1 | Competitor | Delta |
|--------|----------------------|------------|-------|
| Character Error Rate | 0.1633 | 0.2029 | -19.5% |
| Bag-of-word Error Rate | 0.1203 | 0.2748 | -56.2% |
| Multimodal Recall@5 | 0.779-0.901 | Varies | +0.5-2.0% |

- **Parameters:** 52.5M total (detector 45.3M, recognizer 4.9M, relational 2.3M)
- **Architecture:** Detector + Transformer recognizer + relational layout model
- **Output:** Bounding boxes, text strings, confidence scores, reading order
- **GPU support:** NVIDIA Ampere, Hopper, Lovelace, Blackwell; tested on H100, A100, L40s, L4, A10G
- **License:** NVIDIA Open Model License — commercially usable
- **Limitation:** English only. No math/formula. No table structure (just text in boxes).
- **Install:** Served as a NIM — `docker run nvcr.io/nim/nvidia/nemoretriever-ocr-v1:latest` or via NVIDIA NIM API

**Verdict:** Keep it where it is (DataShield ingestion). Do not use it as the general-purpose OCR layer.

---

#### PaddleOCR (PP-OCRv5, released May 2025) — MUST-HAVE TIER 1

- **Accuracy:** 13-point gain over PP-OCRv4; state of art on complex real-world scenarios at sub-100M parameters
- **Speed (RTX 3080 CUDA 11.8):** 12.7 FPS vs EasyOCR's 4.2 FPS (3x faster)
- **Model size:** ~15MB total (detection 4.4MB + recognition 10.5MB)
- **Language support:** Simplified Chinese, Traditional Chinese, English, Japanese, Pinyin in single model; 100+ language ecosystem
- **Table support:** Yes, via PP-StructureV2 (bundled)
- **License:** Apache 2.0 (fully commercial)
- **OmniDocBench score:** PaddleOCR-VL 7B scores 92.86, highest open-source model on that benchmark
- **Install:**
  ```bash
  pip install paddleocr
  pip install paddlepaddle-gpu==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
  # For GPU (CUDA 12.6+), RTX 5090 qualifies
  ```
- **Weakness:** PaddlePaddle framework dependency (not PyTorch-native); initialization 4.2s first call

---

#### EasyOCR — ALREADY INSTALLED, DEMOTE TO PROTOTYPING ONLY

- **Accuracy:** ~87-92% on invoices (vs PaddleOCR 96.58%, Surya 97.70%)
- **Speed (GPU):** Fast on GPU but 3x slower throughput than PaddleOCR in batch
- **Model size:** ~200MB+ (vs PaddleOCR 15MB)
- **Languages:** 90+ languages
- **License:** Apache 2.0
- **Install:** Already installed at `~/.EasyOCR/`
- **Strength:** Easiest Python API, good for single-image scripts, solid number recognition
- **Weakness:** Slower, less accurate on structured docs, no active development push in 2025
- **Keep/remove:** Keep installed (no cost). Do not route production workloads through it.

---

#### Tesseract 5 (LSTM) — KEEP AS OFFLINE FALLBACK ONLY

- **State:** Version 5.x stable since November 2021; LSTM-based, CPU-first
- **Accuracy:** ~87% overall on clean printed text; degrades on complex layouts, handwriting
- **Speed:** Fastest CPU option; slower GPU path
- **License:** Apache 2.0
- **Install:** `pip install pytesseract` + system binary (`choco install tesseract`)
- **Best use case:** Air-gapped deployments, pre-processing step to flag images needing a heavier model, CI test fixtures where a GPU is unavailable
- **Worst use case:** Complex layouts, tables, noisy scans, mixed-language content
- **2025 verdict:** Still valuable as zero-dependency offline fallback. Not a primary OCR engine.

---

#### Surya OCR — MUST-HAVE TIER 1 (GPU workloads)

- **Accuracy:** 97.70% on invoices (highest in structured-document benchmarks); 97.41% overall
- **Capabilities:** OCR + line detection + layout analysis + reading order + table recognition + LaTeX math
- **Languages:** 90+ languages
- **VRAM requirements:**
  - Recognition: ~20GB (default batch 512)
  - Detection: ~16GB (default batch 36)
  - Layout: ~7GB (default batch 32)
  - Table: ~10GB (default batch 64)
  - RTX 5090 (32GB) handles all modes comfortably
- **License:** Modified AI Pubs Open Rail-M + GPL code — free for personal/research/startups under $2M revenue; commercial license available from Datalab
- **Install:** `pip install surya-ocr`
- **Relationship to Marker:** Marker uses Surya as its OCR backend; Marker adds PDF structure, formatting, and optional LLM enhancement on top

---

#### Marker — OPTIONAL (PDF pipeline)

- **What it is:** PDF-to-Markdown/JSON pipeline using Surya as OCR core
- **Benchmark:** Outperforms GPT-4o, DeepSeek OCR, Mistral OCR, and olmOCR on olmOCR-Bench (1,403 PDF files)
- **Optional LLM mode:** Adds quality at latency/cost cost
- **License:** Same as Surya (OpenRAIL + GPL)
- **Install:** `pip install marker-pdf`
- **Verdict:** Only needed if processing PDFs at scale for RAG ingestion. Ultra RAG already handles this; add Marker as an optional enhancement module if document quality becomes a bottleneck.

---

#### GOT-OCR 2.0 (General OCR Theory) — OPTIONAL (scientific/mixed content)

- **Architecture:** 580M parameter end-to-end model — high-compression encoder + long-context decoder
- **Unique capabilities:** Handles plain text, formatted documents, math equations, charts, sheet music, and tables in one model. No pipeline assembly required.
- **Benchmark:** Strong on Fox benchmark (Chinese + English PDF OCR); competitive on scene text; slower than modular pipelines
- **GPU requirement:** Requires GPU for real-time performance
- **License:** MIT
- **Install:** `pip install transformers` then load `ucas-haoranwei/GOT-OCR2.0` from HuggingFace
- **Best use case:** Scientific papers, academic documents with embedded formulas, mixed-content images
- **Limitation:** Higher GPU load than PaddleOCR; no table structure output as structured data; inference latency higher than modular pipelines on standard docs

---

#### Florence-2 (Microsoft) — MUST-HAVE TIER 1 (vision foundation)

- **Size:** Florence-2-base (0.23B), Florence-2-large (0.77B)
- **License:** MIT — fully commercial, no restrictions
- **Capabilities via prompts:** OCR, object detection, grounding, image captioning, region-based text extraction, referring expression comprehension
- **Performance:** Outperforms Kosmos-2 (1.6B) zero-shot across all benchmarks despite smaller size
- **Install:** `pip install transformers` then load `microsoft/Florence-2-large`
- **GPU requirement:** 4-8GB VRAM for inference at FP16
- **Key use for toolkit:** Zero-shot bounding box detection from text prompts (feeds into SAM2), screenshot captioning, element localization in aihangout.ai uploads
- **Works with SAM2:** Florence-2 detects → SAM2 segments. This is the de facto open-source grounded segmentation stack in 2026.

---

#### DocTR — OPTIONAL (PyTorch-native production OCR)

- **Architecture:** Two-stage: detection (DBNet/LinkNet) + recognition (SAR/MASTER/ViT)
- **Framework:** PyTorch or TensorFlow backend; GPU-ready Docker with CUDA 12.2
- **Benchmarks:** Competitive with Google Vision / AWS Textract on FUNSD and CORD datasets
- **License:** Apache 2.0
- **Install:** `pip install "python-doctr[torch,viz]"`
- **Best use case:** Production OCR pipeline that needs PyTorch-native code, structured output, and no PaddlePaddle dependency. Good alternative if PaddleOCR's framework causes integration friction.

---

#### Cloud APIs: Azure AI Vision OCR / Google Cloud Vision / AWS Textract

| Service | Basic pricing (per 1,000 pages) | Structured extraction | Strengths |
|---------|--------------------------------|-----------------------|-----------|
| Azure AI Vision OCR | ~$1.50 | $10-50 | Handwriting, Microsoft ecosystem |
| Google Cloud Vision | ~$1.50 | $10-50 | Layout detection, multilingual |
| AWS Textract | ~$1.50 | $10-50 | Messy/handwritten forms |
| Self-hosted (RTX 5090) | ~$0.09 | Same cost | 167x cheaper at scale |

**Verdict:** None of these belong in the shared toolkit as default paths. Reserve for: (a) handwritten forms where cloud still leads, (b) one-off tasks with no infra budget. Never route DataShield or IMDS production volumes through them.

---

### 3.2 Computer Vision Landscape

#### YOLO11 (Ultralytics) — PRODUCTION BACKBONE, ALREADY IN USE

- **mAP (COCO, YOLO11m):** Beats YOLOv8m with 22% fewer parameters
- **Inference (YOLO11n):** ~17ms/frame (~57 FPS); YOLO11m: ~27ms (~37 FPS)
- **Architecture:** C3k2 block + C2PSA spatial attention; better small object detection vs YOLOv8
- **License:** AGPL-3.0 (Ultralytics); commercial license available
- **Install:** `pip install ultralytics`
- **BehaviorShield status:** Trained model (best.pt) at 93.3% mAP@0.5 is solid. No rebuild needed.

#### YOLOv12 — TRACK BUT DO NOT DEPLOY YET

- **mAP improvement:** +1.2% over YOLO11n; +2.1% over YOLOv10n on COCO val2017
- **Speed trade-off:** 3-9% slower than YOLO11 due to attention blocks; higher memory consumption
- **Stability:** Community-driven release; Ultralytics officially recommends YOLO11 for production
- **Watch trigger:** Move to YOLOv12 when Ultralytics officially integrates it and training instability issues are resolved (likely H2 2026)

---

#### OmniParser v2 (Microsoft) — MUST-HAVE TIER 1 (UI/screen parsing)

- **Benchmark:** 39.5% on ScreenSpot Pro (new SOTA, Feb 2025)
- **Latency:** 0.6s/frame on A100; 0.8s on RTX 4090; ~3s on T4
- **Latency reduction:** 60% faster than OmniParser v1
- **Capabilities:** Detects all interactable UI elements from pixel screenshots; produces structured element list with bounding boxes and labels
- **License:** MIT
- **Install:**
  ```bash
  git clone https://github.com/microsoft/OmniParser
  pip install omniparser opencv-python pillow numpy torch torchvision
  # Download model weights:
  huggingface-cli download microsoft/OmniParser-v2.0 \
    icon_detect/model.pt icon_caption/model.safetensors \
    --local-dir weights
  ```
- **Key project:** IMDS AutoQA — this is the right tool for detecting form fields and UI elements in legacy defense software screenshots without HTML access. No other open-source tool benchmarks at this level for pure-vision UI parsing.

---

#### SAM2 (Meta Segment Anything Model 2) — MUST-HAVE TIER 1 (segmentation)

- **Performance:** 6x more accurate than SAM1; ~44 FPS real-time; works on images and video
- **GPU requirement:** CUDA GPU for real-time; CPU-only possible on edge devices
- **License:** Apache 2.0
- **Install:** `pip install sam2` (or `pip install 'git+https://github.com/facebookresearch/sam2.git'`)
- **Use pattern:** Pair with Florence-2 for grounded segmentation: Florence-2 provides bounding boxes from text prompts → SAM2 produces pixel masks
- **Use cases in toolkit:** aihangout.ai image understanding, content region isolation for moderation, DataShield broker screenshot region extraction

---

#### CLIP / OpenCLIP — MUST-HAVE TIER 1 (embedding and search)

- **Model options:** ViT-B/32 (small/fast) through ViT-L/14-336px (large/accurate, 3.5GB VRAM)
- **License:** MIT (OpenAI CLIP); varied (OpenCLIP, check per checkpoint)
- **Install:** `pip install open_clip_torch` or `pip install clip` (OpenAI original)
- **Speed:** 3.5GB VRAM max for largest model; inference in milliseconds for single images
- **Use cases:** Image-text similarity scoring, content moderation zero-shot classification, deduplication, semantic image search in aihangout.ai
- **Key point:** CLIP is not an OCR tool — it is the glue between image content and text queries. Every toolkit needs it.

---

#### NVIDIA Grounding DINO (NIM) — OPTIONAL

- **Capability:** Open-vocabulary zero-shot object detection from text prompts
- **Variants:** Standard (ViT-L backbone), Edge (EfficientViT-L1 for edge deployment)
- **NVIDIA NIM access:** Available at `build.nvidia.com/nvidia/nv-grounding-dino`
- **Training data:** NVIDIA proprietary NVImageNetv2 (commercial use allowed)
- **Alternative:** Florence-2 covers much of the same use case with lower overhead and MIT license. Use Grounding DINO when you need NVIDIA's fine-tuned commercial detection weights specifically.
- **Verdict:** Optional — Florence-2 is preferred in the toolkit unless Grounding DINO's commercial weights show a specific accuracy advantage on your target domain.

---

#### NVIDIA DALI — OPTIONAL (training/inference pipeline only)

- **Purpose:** GPU-accelerated data loading and preprocessing (replaces CPU bottleneck in training pipelines)
- **Not an OCR or detection tool** — it is a preprocessing infrastructure component
- **Install:** `pip install nvidia-dali-cuda120`
- **Use case for Ron:** Only needed if training throughput becomes a bottleneck when running distributed training on Spark-1/Spark-2. Not needed for inference-only toolkit usage.

---

#### NVIDIA OCDRNet — SKIP FOR TOOLKIT

- **What it is:** DBNet-based text detection network (detects text regions, does not recognize/transcribe text)
- **Available via:** NVIDIA NIM at `build.nvidia.com/nvidia/ocdrnet`
- **Why skip:** NeMo Retriever OCR v1 already subsumes this capability with better end-to-end accuracy. OCDRNet is useful only if you need to run detection and recognition as separately controllable stages with NVIDIA's specific trained weights. PaddleOCR's detection stage is a stronger open-source alternative.

---

#### InternVL2 / InternVL3 — OPTIONAL (vision-language understanding)

- **Variants:** 1B to 108B parameters; InternVL3 released April 2025
- **Strengths:** Complex layout reasoning, chart understanding, PDF summarization, GUI agent tasks
- **License:** MIT (select variants)
- **Use case for toolkit:** Screenshot captioning and reasoning beyond what Florence-2 can do (e.g., "explain what is on this form"). InternVL2.5-4B is the practical toolkit candidate — 4B parameters, efficient, broadly capable.
- **Verdict:** Optional module. Load on demand from Spark-1 (119GB unified memory handles this easily).

---

#### Content Moderation (aihangout.ai user uploads)

| Tool | Architecture | Speed | License | Install |
|------|-------------|-------|---------|---------|
| NudeNet | EfficientNet-based | ~142ms | LGPL | `pip install nudenet` |
| Freepik nsfw_image_detector | EVA ViT, SigLIP2 fine-tuned | GPU-fast | Open | `pip install nsfw-image-detector` |
| CLIP zero-shot | Already in toolkit | Milliseconds | MIT | Same install |

**Recommendation:** Use `nsfw-image-detector` (PyPI 0.1.2, May 2025) as primary moderation layer — it uses a proper vision transformer trained on 100K labeled images with 4 severity levels. Add NudeNet for granular body-part detection if moderation requirements escalate. CLIP zero-shot can serve as a fast pre-filter that routes borderline images to the more expensive models.

---

### 3.3 olmOCR-Bench Leaderboard (current as of early 2026, complex document parsing)

| Model | Score | Params | Pages/sec | Cost/1M pages (H100) |
|-------|-------|--------|-----------|---------------------|
| Chandra | 83.1 | 9B | 1.29 | $605 |
| OlmOCR-2 | 82.4 | 7.7B | 1.78 | $439 |
| PaddleOCR-VL | 80.0 | 0.9B | 2.20 | $355 |
| DeepSeek-OCR | 75.7 | 3B* | 4.65 | $168 |
| LightOn OCR | 76.1 | 1B | 5.55 | $141 |

*570M active parameters via MoE

These are VLM-class models suitable for Spark-1's 119GB unified memory, not for real-time inference on a toolkit endpoint. They belong in a batch processing pipeline, not the shared toolkit core.

---

## 4. Risks and Confidence Notes

- **Surya license risk:** The OpenRAIL + GPL license may conflict with commercial SaaS use in DataShield or aihangout.ai. Before deploying Surya in production pipelines that process paying customer data, verify with LEGAL whether the revenue threshold applies or whether a commercial license from Datalab is needed. Chargeable commercial tier is available.
- **PaddleOCR framework risk:** PaddlePaddle (Baidu's framework) adds a non-standard dependency. On Windows, CUDA version compatibility requires care — CUDA 12.6+ is needed for the `cu126` wheel. RTX 5090 supports this.
- **YOLOv12 instability:** Not production-ready. Do not migrate BehaviorShield to YOLOv12 without waiting for Ultralytics official integration.
- **NeMo OCR English-only limitation:** Any multilingual content in DataShield or IMDS screenshots will silently fail. Have PaddleOCR as fallback for non-English text.
- **OmniParser VRAM:** The icon_caption Florence model adds ~4-6GB VRAM on top of the detection model. On RTX 5090 this is fine; on anything smaller, expect OOM at high batch sizes.
- **Benchmark provenance:** OmniDocBench and olmOCR-Bench are the most credible current benchmarks (as of Q1 2026). Invoice/structured document benchmarks from E2E Networks and Researchify are real-world but not peer-reviewed. Treat accuracy numbers as directionally correct, not exact.

---

## 5. Recommendation — Shared Toolkit Composition

### Tier 1: Must-Have (install in toolkit core, always available)

| Tool | Primary role | GPU VRAM needed | Install command | Accuracy tier |
|------|-------------|-----------------|-----------------|---------------|
| **PaddleOCR (PP-OCRv5)** | General OCR, structured docs | 2-4GB | `pip install paddleocr paddlepaddle-gpu==3.2.0` | A |
| **Surya OCR** | High-accuracy OCR + layout + tables | 7-20GB (mode-dependent) | `pip install surya-ocr` | A+ |
| **Florence-2** | Zero-shot detection, grounding, OCR | 4-8GB | `pip install transformers` + HF model | A |
| **SAM2** | Pixel segmentation | 4-8GB | `pip install sam2` | A |
| **OmniParser v2** | UI/screen element parsing | 6-10GB | `git clone + pip install -r requirements.txt` | A (UI-specific) |
| **OpenCLIP** | Image-text embedding, similarity | 2-4GB (ViT-B/32) | `pip install open_clip_torch` | A |
| **YOLO11** | Real-time object detection | 2-6GB | `pip install ultralytics` | A |

### Tier 2: Optional (install on demand, not in core)

| Tool | When to add | Install |
|------|-------------|---------|
| **Marker** | PDF-to-Markdown RAG pipeline | `pip install marker-pdf` |
| **GOT-OCR 2.0** | Scientific papers, math equations | `pip install transformers` + HF model |
| **DocTR** | Pure PyTorch OCR alternative | `pip install "python-doctr[torch,viz]"` |
| **nsfw-image-detector** | aihangout.ai content moderation | `pip install nsfw-image-detector` |
| **NudeNet** | Granular body-part moderation | `pip install nudenet` |
| **InternVL2.5-4B** | Advanced screenshot reasoning | `pip install transformers` + HF model |
| **NVIDIA DALI** | Training data pipeline acceleration | `pip install nvidia-dali-cuda120` |

### Tier 3: Skip (not worth complexity)

| Tool | Reason |
|------|--------|
| **EasyOCR** (new installs) | Already installed; keep for legacy scripts but do not route new work here |
| **Tesseract** (new installs) | Keep only as offline/CPU fallback in CI; not a production engine |
| **Azure/Google/AWS OCR APIs** | 167x more expensive than self-hosted; no accuracy advantage for standard documents |
| **NVIDIA OCDRNet** | Subsumed by NeMo OCR v1 already in use |
| **YOLOv12** | Not production-stable; revisit H2 2026 |
| **NVIDIA Grounding DINO NIM** | Florence-2 covers same use case; MIT license is cleaner than NVIDIA OML |

---

## 6. Project-to-Tool Mapping

### DataShield (broker site screenshots — image-rendered text, confirmation codes, CAPTCHAs)

| Need | Tool | Rationale |
|------|------|-----------|
| Image-rendered text (broker sites) | **Surya OCR** → fallback to **PaddleOCR** | Surya handles degraded/stylized fonts; PaddleOCR covers anything Surya misses |
| Confirmation code detection | **PaddleOCR PP-OCRv5** | Sub-word accuracy on short alphanumeric strings; 12.7 FPS throughput |
| CAPTCHA type classification | **CLIP zero-shot** | "Is this a text CAPTCHA, image CAPTCHA, or checkbox challenge?" — no fine-tuning needed |
| Document structure (if PDFs added later) | **NeMo Retriever OCR v1** (already integrated) | Precision RAG ingestion; keep where it is |

### aihangout.ai (content moderation, user image uploads)

| Need | Tool | Rationale |
|------|------|-----------|
| NSFW/explicit content detection | **nsfw-image-detector** (primary) + **NudeNet** (escalation) | 4-level severity scoring; GPU-fast |
| Object/scene understanding | **Florence-2** | Zero-shot detection with text prompts; MIT license |
| Semantic image search / tagging | **OpenCLIP** | Image-text embedding for similarity indexing |
| Pixel segmentation for cropping/blurring | **SAM2** | Precise region isolation for moderation actions |

### BehaviorShield (security detection — YOLO model already trained)

| Need | Tool | Rationale |
|------|------|-----------|
| Existing pipeline | **YOLO11 (best.pt)** | 93.3% mAP@0.5 — do not rebuild |
| Potential improvement: zone analysis | **SAM2** | Segment detected regions for fine-grained activity analysis within zones |
| False positive reduction | **CLIP** | Score detection confidence against text description of expected scenario |
| Future: migrate to YOLOv12 | **Wait** | Track Ultralytics official release; ~6-12 months |

### IMDS AutoQA (Air Force CAMS/IMDS — legacy defense software screenshots)

| Need | Tool | Rationale |
|------|------|-----------|
| UI element detection (form fields, buttons, error codes) | **OmniParser v2** | Only tool with SOTA benchmark for pure-vision UI parsing; 39.5% ScreenSpot Pro |
| Text extraction from screenshots | **Surya OCR** (primary) → **PaddleOCR** (fallback) | High accuracy on rendered UI text; both GPU-accelerated |
| Air-gapped fallback (if no GPU available on GFE) | **Tesseract 5** | CPU-only, no cloud dependency, 100+ languages |
| Field value validation | **PaddleOCR PP-OCRv5** | High throughput for repeated screenshot comparison in test loops |

### General Browser Automation (UI element detection in screenshots)

| Need | Tool |
|------|------|
| Parse any screenshot into structured UI elements | **OmniParser v2** |
| Identify specific UI regions from text description | **Florence-2** (grounding) |
| Extract text from identified regions | **PaddleOCR PP-OCRv5** |
| Match screenshot state to expected state | **CLIP** (image-text similarity) |

---

## 7. Quick Integration Notes for `C:\Users\techai\toolkit\vision\`

Recommended directory structure:

```
C:\Users\techai\toolkit\
└── vision\
    ├── ocr\
    │   ├── paddle.py      # PaddleOCR wrapper — detect+recognize, returns {text, bbox, confidence}
    │   ├── surya.py       # Surya wrapper — returns {text, bbox, layout, reading_order}
    │   ├── nemo.py        # NeMo Retriever OCR NIM client (already wired in DataShield — copy pattern)
    │   └── tesseract.py   # Fallback CPU wrapper via pytesseract
    ├── detection\
    │   ├── yolo.py        # YOLO11 wrapper — load model, run inference, return detections
    │   ├── florence.py    # Florence-2 wrapper — text-prompted bbox, captioning, OCR
    │   └── omniparser.py  # OmniParser v2 wrapper — screenshot → element list
    ├── segmentation\
    │   └── sam2.py        # SAM2 wrapper — accepts bboxes or points, returns masks
    ├── embedding\
    │   └── clip.py        # OpenCLIP wrapper — encode image, encode text, cosine similarity
    └── moderation\
        └── nsfw.py        # nsfw-image-detector + NudeNet router
```

**For each wrapper, the contract is:**
1. Lazy-load model on first call (not at import time)
2. Accept either a file path or a PIL Image
3. Return a typed dict with consistent keys (`text`, `bbox`, `confidence`, `labels` as applicable)
4. Accept a `device` parameter defaulting to `"cuda"` if available, `"cpu"` otherwise

**Priority order to build:**
1. `paddle.py` — covers 80% of OCR needs across all projects
2. `omniparser.py` — unblocks IMDS AutoQA immediately
3. `florence.py` — enables DataShield CAPTCHA classification and aihangout.ai zero-shot detection
4. `clip.py` — enables semantic search and content filtering in aihangout.ai

The Surya, SAM2, and moderation wrappers can follow since they layer on top of the first four.

---

## 8. Next Actions

1. **Verify Surya license with LEGAL before routing DataShield production data through it.** The OpenRAIL-M + GPL combination needs a clean ruling on whether commercial deployment in a paid SaaS constitutes the revenue threshold trigger. This is a one-time check that unblocks the highest-accuracy OCR path.

2. **Install PaddleOCR PP-OCRv5 on the RTX 5090 today.** This is a straight drop-in that immediately improves any workflow currently using EasyOCR. Confirm CUDA 12.6 wheel installs cleanly: `pip install paddlepaddle-gpu==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/` then `pip install paddleocr`.

3. **Set up OmniParser v2 for IMDS AutoQA.** Clone the repo, download weights via `huggingface-cli download microsoft/OmniParser-v2.0`, and test against one IMDS screenshot. This is the highest-value unblocked task for the IMDS test framework.

4. **Build the `toolkit/vision/` directory scaffold.** Start with `paddle.py`, `omniparser.py`, `florence.py`, `clip.py` as the first four wrappers. Hand this task to FORGE with the directory structure above and the wrapper contract defined in Section 7.

5. **Do not rebuild BehaviorShield YOLO.** The model is solid at 93.3% mAP. Consider SAM2 as an additive layer for zone analysis only if there is a specific false-positive or precision problem in production.

---

*Research by NOVA. Deliverable placed in Owner's Inbox. Cross-domain note: Surya license issue flagged for LEGAL. Implementation task defined for FORGE.*
