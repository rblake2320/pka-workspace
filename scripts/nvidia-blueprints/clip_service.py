"""
CLIP Embedding Service — Windows PC RTX 5090
Runs on port 8320. Called by Spark-1 Video Search API (:8310).

Embeds both images (from video frames) and text (search queries)
using CLIP ViT-L/14 (768-dim vectors).

Setup:
    pip install transformers torch Pillow fastapi uvicorn[standard]
    python3 clip_service.py

Test:
    curl -X POST http://localhost:8320/embed -H "Content-Type: application/json" \
         -d '{"text": "city council votes on budget"}'

    curl http://localhost:8320/health
"""
import base64
import io
import logging
from typing import Optional

import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from PIL import Image
from pydantic import BaseModel
from transformers import CLIPModel, CLIPProcessor

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = FastAPI(title="CLIP Embedding Service", version="1.0.0")

MODEL_ID = "openai/clip-vit-large-patch14"  # 768-dim, fits easily in 32GB VRAM
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

log.info("Loading %s on %s...", MODEL_ID, DEVICE)
_model = CLIPModel.from_pretrained(MODEL_ID, torch_dtype=DTYPE).to(DEVICE)
_processor = CLIPProcessor.from_pretrained(MODEL_ID)
_model.eval()

if DEVICE == "cuda":
    vram_gb = torch.cuda.memory_allocated() / 1e9
    log.info("CLIP loaded. VRAM used: %.1f GB / 32.0 GB available", vram_gb)
else:
    log.info("CLIP loaded on CPU (no GPU detected)")


class EmbedRequest(BaseModel):
    text: Optional[str] = None
    image_b64: Optional[str] = None  # base64-encoded JPEG/PNG


class EmbedResponse(BaseModel):
    embedding: list[float]
    dim: int
    modality: str


@app.post("/embed", response_model=EmbedResponse)
async def embed(req: EmbedRequest):
    if req.text is None and req.image_b64 is None:
        raise HTTPException(400, "Provide either 'text' or 'image_b64'")

    with torch.inference_mode():
        if req.image_b64:
            img_bytes = base64.b64decode(req.image_b64)
            image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            inputs = _processor(images=image, return_tensors="pt").to(DEVICE)
            features = _model.get_image_features(**inputs)
            modality = "image"
        else:
            inputs = _processor(
                text=[req.text], return_tensors="pt",
                padding=True, truncation=True
            ).to(DEVICE)
            features = _model.get_text_features(**inputs)
            modality = "text"

        # Normalize to unit vector for cosine similarity
        features = features / features.norm(dim=-1, keepdim=True)
        embedding = features[0].cpu().float().tolist()

    return EmbedResponse(embedding=embedding, dim=len(embedding), modality=modality)


@app.get("/health")
async def health():
    vram = round(torch.cuda.memory_allocated() / 1e9, 2) if DEVICE == "cuda" else 0
    return {
        "status": "ok",
        "device": DEVICE,
        "model": MODEL_ID,
        "embedding_dim": 768,
        "vram_gb": vram,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8320)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()
    log.info("Starting CLIP service on %s:%d", args.host, args.port)
    uvicorn.run(app, host=args.host, port=args.port)
