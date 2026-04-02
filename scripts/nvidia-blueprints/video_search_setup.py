"""
Video Search Setup — NVIDIA AI Blueprints Integration
RTX 5090 runs CLIP/SigLIP inference locally.
Spark-1 stores embeddings in pgvector + serves search API on :8310.

Steps this script performs:
  1. Install Python deps (transformers, clip, opencv, ffmpeg-python)
  2. Create pgvector schema on Spark-1 for video embeddings
  3. Deploy FastAPI search service on Spark-1:8310
  4. Add :8310 to Cloudflare tunnel config

Usage:
    python3 video_search_setup.py --install-deps
    python3 video_search_setup.py --create-schema
    python3 video_search_setup.py --ingest path/to/video.mp4 --title "Council Meeting 2026-03"
    python3 video_search_setup.py --search "planning commission budget vote"
"""
from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SPARK1_HOST = "rblake2320@192.168.12.132"
SPARK1_PG_DSN = "postgresql://memoryweb:memoryweb@localhost:5432/memoryweb"
VIDEO_API_PORT = 8310
CLIP_MODEL = "openai/clip-vit-large-patch14"  # Best quality on RTX 5090 32GB

# pgvector schema SQL — runs on Spark-1
SCHEMA_SQL = """
-- Video Search Schema — added 2026-03-23
CREATE TABLE IF NOT EXISTS video_library (
    id          SERIAL PRIMARY KEY,
    title       TEXT NOT NULL,
    source_path TEXT,
    duration_s  FLOAT,
    fps         FLOAT,
    frame_count INTEGER,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    metadata    JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS video_frames (
    id          BIGSERIAL PRIMARY KEY,
    video_id    INTEGER NOT NULL REFERENCES video_library(id) ON DELETE CASCADE,
    timestamp_s FLOAT NOT NULL,
    frame_idx   INTEGER NOT NULL,
    embedding   vector(768),   -- CLIP ViT-L/14 embedding dimension
    ocr_text    TEXT,          -- optional Tesseract OCR on frame
    caption     TEXT,          -- optional NIM-generated caption
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- HNSW index for fast ANN search
CREATE INDEX IF NOT EXISTS video_frames_emb_hnsw
    ON video_frames USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Index for video lookups
CREATE INDEX IF NOT EXISTS video_frames_video_idx ON video_frames(video_id);
CREATE INDEX IF NOT EXISTS video_frames_ts_idx ON video_frames(timestamp_s);

-- Convenience view: search results with video metadata
CREATE OR REPLACE VIEW video_search_results AS
SELECT
    vf.id AS frame_id,
    vl.title,
    vf.timestamp_s,
    vf.frame_idx,
    vf.ocr_text,
    vf.caption,
    vl.source_path,
    vl.id AS video_id
FROM video_frames vf
JOIN video_library vl ON vl.id = vf.video_id;

COMMENT ON TABLE video_library IS 'Video Search — ingested video metadata';
COMMENT ON TABLE video_frames IS 'Video Search — per-frame CLIP embeddings';
"""


# ---------------------------------------------------------------------------
# Spark-1 FastAPI video search service
# ---------------------------------------------------------------------------

VIDEO_API_SERVICE = '''#!/usr/bin/env python3
"""
Video Search API — Spark-1:8310
RTX 5090 embeds via CLIP; this service stores/queries pgvector.

Endpoints:
  POST /api/video/ingest     { video_path, title }       — start ingestion job
  GET  /api/video/search     ?q=<text>&top_k=5           — semantic search
  GET  /api/video/videos      — list all videos
  GET  /api/video/{id}/frames — frames for a video
"""
import asyncio
import json
import logging
import os
import time
from typing import Optional

import asyncpg
import httpx
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Video Search API", version="1.0.0")

PG_DSN = os.getenv("VIDEO_SEARCH_PG_DSN", "postgresql://memoryweb:memoryweb@localhost:5432/memoryweb")
EMBED_ENDPOINT = os.getenv("VIDEO_EMBED_URL", "http://192.168.12.198:8320/embed")  # Windows PC CLIP service


@app.on_event("startup")
async def startup():
    app.state.pool = await asyncpg.create_pool(PG_DSN, min_size=2, max_size=10)
    log.info("Video Search API started — pool connected")


@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()


class IngestRequest(BaseModel):
    video_path: str
    title: str
    frame_interval_s: float = 5.0  # Extract one frame every N seconds


class SearchResult(BaseModel):
    frame_id: int
    title: str
    timestamp_s: float
    similarity: float
    caption: Optional[str]
    ocr_text: Optional[str]
    video_id: int


@app.post("/api/video/ingest")
async def ingest_video(req: IngestRequest, bg: BackgroundTasks):
    """Register video and queue frame extraction + embedding."""
    async with app.state.pool.acquire() as conn:
        vid_id = await conn.fetchval(
            "INSERT INTO video_library(title, source_path) VALUES($1, $2) RETURNING id",
            req.title, req.video_path
        )
    bg.add_task(_ingest_job, vid_id, req.video_path, req.frame_interval_s)
    return {"video_id": vid_id, "status": "ingesting", "title": req.title}


async def _ingest_job(video_id: int, video_path: str, interval_s: float):
    """Background task: extract frames, get embeddings from Windows PC CLIP service."""
    try:
        import cv2
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_s = frame_count / fps

        # Update video metadata
        async with app.state.pool.acquire() as conn:
            await conn.execute(
                "UPDATE video_library SET duration_s=$1, fps=$2, frame_count=$3 WHERE id=$4",
                duration_s, fps, frame_count, video_id
            )

        frame_interval = int(fps * interval_s)
        frames_processed = 0
        frame_idx = 0

        while True:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                break

            timestamp_s = frame_idx / fps

            # Send frame to Windows PC CLIP service for embedding
            import cv2
            import base64
            _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            img_b64 = base64.b64encode(buf).decode()

            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    resp = await client.post(EMBED_ENDPOINT, json={"image_b64": img_b64})
                    resp.raise_for_status()
                    embedding = resp.json()["embedding"]  # list of 768 floats

                # Store in pgvector
                async with app.state.pool.acquire() as conn:
                    await conn.execute(
                        """INSERT INTO video_frames(video_id, timestamp_s, frame_idx, embedding)
                           VALUES($1, $2, $3, $4::vector)""",
                        video_id, timestamp_s, frame_idx, str(embedding)
                    )
                frames_processed += 1
            except Exception as e:
                log.warning("Frame %d embedding failed: %s", frame_idx, e)

            frame_idx += frame_interval

        cap.release()
        log.info("Ingested video %d: %d frames processed", video_id, frames_processed)

    except Exception as e:
        log.error("Ingest job failed for video %d: %s", video_id, e)


@app.get("/api/video/search", response_model=list[SearchResult])
async def search_video(
    q: str = Query(..., description="Natural language search query"),
    top_k: int = Query(5, ge=1, le=50),
    video_id: Optional[int] = Query(None, description="Limit to specific video"),
):
    """Semantic search across all ingested video frames."""
    # Get text embedding from Windows PC CLIP service
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(EMBED_ENDPOINT, json={"text": q})
            resp.raise_for_status()
            query_embedding = resp.json()["embedding"]
    except Exception as e:
        raise HTTPException(502, f"Embedding service unavailable: {e}")

    emb_str = str(query_embedding)

    async with app.state.pool.acquire() as conn:
        if video_id:
            rows = await conn.fetch(
                """SELECT vf.id, vl.title, vf.timestamp_s, vf.caption, vf.ocr_text, vl.id as vid_id,
                          1 - (vf.embedding <=> $1::vector) AS similarity
                   FROM video_frames vf JOIN video_library vl ON vl.id = vf.video_id
                   WHERE vl.id = $3
                   ORDER BY vf.embedding <=> $1::vector
                   LIMIT $2""",
                emb_str, top_k, video_id
            )
        else:
            rows = await conn.fetch(
                """SELECT vf.id, vl.title, vf.timestamp_s, vf.caption, vf.ocr_text, vl.id as vid_id,
                          1 - (vf.embedding <=> $1::vector) AS similarity
                   FROM video_frames vf JOIN video_library vl ON vl.id = vf.video_id
                   ORDER BY vf.embedding <=> $1::vector
                   LIMIT $2""",
                emb_str, top_k
            )

    return [
        SearchResult(
            frame_id=r["id"],
            title=r["title"],
            timestamp_s=r["timestamp_s"],
            similarity=round(r["similarity"], 4),
            caption=r["caption"],
            ocr_text=r["ocr_text"],
            video_id=r["vid_id"],
        )
        for r in rows
    ]


@app.get("/api/video/videos")
async def list_videos():
    async with app.state.pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, title, duration_s, frame_count, ingested_at FROM video_library ORDER BY ingested_at DESC"
        )
    return [dict(r) for r in rows]


@app.get("/api/video/health")
async def health():
    try:
        async with app.state.pool.acquire() as conn:
            count = await conn.fetchval("SELECT COUNT(*) FROM video_frames")
        return {"status": "ok", "total_frames": count}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8310)
'''

# ---------------------------------------------------------------------------
# Windows PC CLIP embedding service (run locally on RTX 5090)
# ---------------------------------------------------------------------------

CLIP_SERVICE = '''#!/usr/bin/env python3
"""
CLIP Embedding Service — Windows PC RTX 5090
Runs on port 8320. Called by Spark-1 Video Search API.

Embeds both images and text using CLIP ViT-L/14 (768-dim).

Usage:
    python3 clip_service.py                    # Start on :8320
    python3 clip_service.py --port 8320        # Explicit port
"""
import base64
import io
import logging
import os
from typing import Optional

import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from PIL import Image
from pydantic import BaseModel
from transformers import CLIPModel, CLIPProcessor

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="CLIP Embedding Service", version="1.0.0")

MODEL_ID = "openai/clip-vit-large-patch14"  # 768-dim, best quality
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

log.info("Loading CLIP model %s on %s...", MODEL_ID, DEVICE)
model = CLIPModel.from_pretrained(MODEL_ID, torch_dtype=DTYPE).to(DEVICE)
processor = CLIPProcessor.from_pretrained(MODEL_ID)
model.eval()
log.info("CLIP model loaded. Device: %s, VRAM: %.1f GB",
         DEVICE,
         torch.cuda.memory_allocated() / 1e9 if DEVICE == "cuda" else 0)


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
            # Decode base64 image
            img_bytes = base64.b64decode(req.image_b64)
            image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            inputs = processor(images=image, return_tensors="pt").to(DEVICE)
            features = model.get_image_features(**inputs)
            modality = "image"
        else:
            inputs = processor(text=[req.text], return_tensors="pt",
                               padding=True, truncation=True).to(DEVICE)
            features = model.get_text_features(**inputs)
            modality = "text"

        # Normalize to unit vector (standard for cosine similarity search)
        features = features / features.norm(dim=-1, keepdim=True)
        embedding = features[0].cpu().float().tolist()

    return EmbedResponse(embedding=embedding, dim=len(embedding), modality=modality)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "device": DEVICE,
        "model": MODEL_ID,
        "vram_gb": round(torch.cuda.memory_allocated() / 1e9, 2) if DEVICE == "cuda" else 0,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8320)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)
'''


# ---------------------------------------------------------------------------
# Main setup runner
# ---------------------------------------------------------------------------

def install_deps():
    """Install Python deps for video search."""
    # Windows PC (local) — CLIP service deps
    local_deps = [
        "transformers", "torch", "Pillow", "opencv-python-headless",
        "ffmpeg-python", "fastapi", "uvicorn[standard]", "pydantic"
    ]
    print("Installing local (Windows PC) deps...")
    subprocess.run([sys.executable, "-m", "pip", "install"] + local_deps, check=True)
    print("[OK] Local deps installed")


def create_schema_on_spark1():
    """SSH to Spark-1 and create the pgvector schema."""
    sql = SCHEMA_SQL.replace("'", "'\\''")  # escape single quotes for shell
    cmd = f"ssh {SPARK1_HOST} \"psql '{SPARK1_PG_DSN}' -c '{sql}'\""
    print(f"Creating pgvector schema on Spark-1...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("[OK] Schema created on Spark-1")
    else:
        print(f"[WARN] Schema creation output: {result.stderr[:200]}")
        # May already exist — check for the table
        check = subprocess.run(
            f"ssh {SPARK1_HOST} \"psql '{SPARK1_PG_DSN}' -c '\\\\dt video_*'\"",
            shell=True, capture_output=True, text=True
        )
        print(check.stdout[:200])


def deploy_video_api_spark1():
    """Write and start the video search API on Spark-1."""
    # Write API file
    api_remote = "/home/rblake2320/video-search/video_api.py"
    service_remote = "/home/rblake2320/video-search/video_api.service"

    print("Deploying Video Search API to Spark-1...")
    subprocess.run(
        f"ssh {SPARK1_HOST} 'mkdir -p /home/rblake2320/video-search'",
        shell=True, check=True
    )

    # Write API via heredoc-safe method
    tmp_api = Path("/tmp/video_api_deploy.py")
    tmp_api.write_text(VIDEO_API_SERVICE)
    subprocess.run(f"scp {tmp_api} {SPARK1_HOST}:{api_remote}", shell=True, check=True)
    print(f"[OK] API deployed to Spark-1:{api_remote}")

    # Install Spark-1 deps
    subprocess.run(
        f"ssh {SPARK1_HOST} 'pip install asyncpg fastapi uvicorn httpx opencv-python-headless --quiet'",
        shell=True
    )
    print("[OK] Spark-1 deps installed")


def write_clip_service_local():
    """Write the CLIP embedding service for local RTX 5090."""
    out = Path("clip_service.py")
    out.write_text(CLIP_SERVICE)
    print(f"[OK] CLIP service written to {out.absolute()}")
    print(f"     Start with: python3 {out.name}")


def main():
    parser = argparse.ArgumentParser(description="Video Search Setup")
    parser.add_argument("--install-deps", action="store_true")
    parser.add_argument("--create-schema", action="store_true")
    parser.add_argument("--deploy-api", action="store_true")
    parser.add_argument("--write-clip-service", action="store_true")
    parser.add_argument("--all", action="store_true", help="Run all setup steps")
    args = parser.parse_args()

    if args.all or args.install_deps:
        install_deps()
    if args.all or args.create_schema:
        create_schema_on_spark1()
    if args.all or args.deploy_api:
        deploy_video_api_spark1()
    if args.all or args.write_clip_service:
        write_clip_service_local()

    if not any(vars(args).values()):
        parser.print_help()


if __name__ == "__main__":
    main()
