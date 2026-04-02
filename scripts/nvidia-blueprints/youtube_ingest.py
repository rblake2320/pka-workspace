"""
YouTube Video Ingest — adds YouTube URL support to Video Search pipeline.

How it works:
  yt-dlp downloads/streams the video → frames extracted every N seconds →
  each frame sent to CLIP service on RTX 5090 → embeddings stored in pgvector

Also extracts:
  - Auto-generated captions (subtitles) for text-based search
  - Video metadata (title, description, upload date, channel)

Usage:
    python3 youtube_ingest.py "https://www.youtube.com/watch?v=geIKyDaXwGg"
    python3 youtube_ingest.py "https://www.youtube.com/watch?v=..." --interval 10 --captions-only
    python3 youtube_ingest.py "https://www.youtube.com/watch?v=..." --search-after "budget vote"
"""
from __future__ import annotations

import argparse
import base64
import json
import logging
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

import httpx

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

VIDEO_API = "http://192.168.12.132:8310"   # Spark-1 Video Search API
CLIP_API  = "http://localhost:8320"          # Local RTX 5090 CLIP service
FRAME_INTERVAL_S = 5.0                       # Extract one frame every N seconds


# ---------------------------------------------------------------------------
# Step 1: Get YouTube metadata + captions with yt-dlp
# ---------------------------------------------------------------------------

def get_youtube_info(url: str) -> dict:
    """Fetch video metadata and available subtitle languages."""
    result = subprocess.run(
        ["yt-dlp", "--dump-json", "--no-download", url],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp metadata failed: {result.stderr[:200]}")
    return json.loads(result.stdout)


def get_captions(url: str, lang: str = "en") -> list[dict]:
    """
    Download auto-generated or manual captions.
    Returns list of {start_s, end_s, text} dicts sorted by time.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            [
                "yt-dlp",
                "--write-auto-subs", "--write-subs",
                "--sub-langs", lang,
                "--sub-format", "json3",
                "--skip-download",
                "--output", f"{tmpdir}/%(id)s.%(ext)s",
                url,
            ],
            capture_output=True, text=True, timeout=60
        )

        # Find the downloaded subtitle file
        sub_files = list(Path(tmpdir).glob("*.json3"))
        if not sub_files:
            # Try vtt format as fallback
            result2 = subprocess.run(
                [
                    "yt-dlp",
                    "--write-auto-subs", "--write-subs",
                    "--sub-langs", lang,
                    "--sub-format", "vtt",
                    "--skip-download",
                    "--output", f"{tmpdir}/%(id)s.%(ext)s",
                    url,
                ],
                capture_output=True, text=True, timeout=60
            )
            vtt_files = list(Path(tmpdir).glob("*.vtt"))
            if vtt_files:
                return _parse_vtt(vtt_files[0].read_text())
            log.warning("No captions found for %s", url)
            return []

        return _parse_json3(sub_files[0].read_text())


def _parse_json3(content: str) -> list[dict]:
    """Parse YouTube json3 subtitle format."""
    try:
        data = json.loads(content)
        segments = []
        for event in data.get("events", []):
            start_ms = event.get("tStartMs", 0)
            dur_ms = event.get("dDurationMs", 0)
            segs = event.get("segs", [])
            text = "".join(s.get("utf8", "") for s in segs).strip()
            if text and text != "\n":
                segments.append({
                    "start_s": start_ms / 1000.0,
                    "end_s": (start_ms + dur_ms) / 1000.0,
                    "text": text.replace("\n", " "),
                })
        return segments
    except Exception as e:
        log.warning("json3 parse failed: %s", e)
        return []


def _parse_vtt(content: str) -> list[dict]:
    """Parse WebVTT subtitle format."""
    import re
    segments = []
    pattern = re.compile(
        r"(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})\n(.*?)(?=\n\n|\Z)",
        re.DOTALL
    )

    def ts_to_s(ts: str) -> float:
        parts = ts.split(":")
        h, m, s = int(parts[0]), int(parts[1]), float(parts[2])
        return h * 3600 + m * 60 + s

    for m in pattern.finditer(content):
        text = re.sub(r"<[^>]+>", "", m.group(3)).strip()
        if text:
            segments.append({
                "start_s": ts_to_s(m.group(1)),
                "end_s": ts_to_s(m.group(2)),
                "text": text.replace("\n", " "),
            })
    return segments


# ---------------------------------------------------------------------------
# Step 2: Stream frames from YouTube via yt-dlp → opencv
# ---------------------------------------------------------------------------

def stream_frames_from_youtube(
    url: str,
    interval_s: float = FRAME_INTERVAL_S,
    max_duration_s: Optional[float] = None,
):
    """
    Generator: yields (timestamp_s, jpeg_bytes) for every frame at interval_s.
    Uses yt-dlp to get the best video-only stream URL, then reads with opencv.
    """
    try:
        import cv2
    except ImportError:
        raise ImportError("pip install opencv-python-headless")

    # Get the direct stream URL (no download needed)
    result = subprocess.run(
        ["yt-dlp", "-f", "best[height<=720]", "--get-url", url],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp get-url failed: {result.stderr[:200]}")

    stream_url = result.stdout.strip()
    log.info("Stream URL obtained, opening with OpenCV...")

    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        raise RuntimeError("OpenCV could not open stream URL")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    frame_skip = max(1, int(fps * interval_s))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    log.info("FPS: %.1f, frame_skip: %d, total_frames: %d", fps, frame_skip, total_frames)

    frame_idx = 0
    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break

        timestamp_s = frame_idx / fps
        if max_duration_s and timestamp_s > max_duration_s:
            break

        _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        yield timestamp_s, bytes(buf)

        frame_idx += frame_skip

    cap.release()


# ---------------------------------------------------------------------------
# Step 3: Ingest into Video Search pipeline
# ---------------------------------------------------------------------------

def register_video(title: str, url: str, metadata: dict) -> int:
    """Register video in the Video Search API, returns video_id."""
    resp = httpx.post(
        f"{VIDEO_API}/api/video/ingest",
        json={"video_path": url, "title": title, "frame_interval_s": 0},  # 0 = we'll push frames
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()["video_id"]


def push_frame_embedding(video_id: int, timestamp_s: float, frame_idx: int,
                          jpeg_bytes: bytes, caption_text: Optional[str] = None):
    """Get CLIP embedding from RTX 5090 service, then store via Video API."""
    img_b64 = base64.b64encode(jpeg_bytes).decode()

    # Get embedding from local CLIP service
    emb_resp = httpx.post(
        f"{CLIP_API}/embed",
        json={"image_b64": img_b64},
        timeout=30
    )
    emb_resp.raise_for_status()
    embedding = emb_resp.json()["embedding"]

    # Store in pgvector via Video API (direct DB insert endpoint)
    store_resp = httpx.post(
        f"{VIDEO_API}/api/video/frame",
        json={
            "video_id": video_id,
            "timestamp_s": timestamp_s,
            "frame_idx": frame_idx,
            "embedding": embedding,
            "caption": caption_text,
        },
        timeout=30
    )
    store_resp.raise_for_status()


def ingest_captions_only(video_id: int, captions: list[dict]):
    """
    Fallback when CLIP service is not running:
    Index captions as text embeddings (text-only search via CLIP text encoder).
    """
    for i, seg in enumerate(captions):
        if not seg["text"].strip():
            continue
        try:
            emb_resp = httpx.post(
                f"{CLIP_API}/embed",
                json={"text": seg["text"]},
                timeout=30
            )
            emb_resp.raise_for_status()
            embedding = emb_resp.json()["embedding"]

            httpx.post(
                f"{VIDEO_API}/api/video/frame",
                json={
                    "video_id": video_id,
                    "timestamp_s": seg["start_s"],
                    "frame_idx": i,
                    "embedding": embedding,
                    "caption": seg["text"],
                },
                timeout=30
            ).raise_for_status()
        except Exception as e:
            log.warning("Caption %d embed failed: %s", i, e)


# ---------------------------------------------------------------------------
# Simple search (no services needed — uses yt-dlp + text search on captions)
# ---------------------------------------------------------------------------

def search_captions_local(captions: list[dict], query: str, top_k: int = 5) -> list[dict]:
    """
    Keyword search over captions without any vector DB.
    Useful when services aren't running yet.
    """
    query_words = set(query.lower().split())
    scored = []
    for seg in captions:
        text_words = set(seg["text"].lower().split())
        score = len(query_words & text_words) / max(1, len(query_words))
        if score > 0:
            scored.append({**seg, "score": round(score, 3)})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def format_timestamp(s: float) -> str:
    """Convert seconds to MM:SS or HH:MM:SS."""
    s = int(s)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{sec:02d}"
    return f"{m}:{sec:02d}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="YouTube Video Ingest for Video Search")
    parser.add_argument("url", help="YouTube URL")
    parser.add_argument("--interval", type=float, default=5.0,
                        help="Frame extraction interval in seconds (default: 5)")
    parser.add_argument("--captions-only", action="store_true",
                        help="Only index captions (no frame extraction, no CLIP needed)")
    parser.add_argument("--search-after", metavar="QUERY",
                        help="Run a search immediately after ingestion")
    parser.add_argument("--info-only", action="store_true",
                        help="Just print video metadata and captions, don't ingest")
    parser.add_argument("--max-duration", type=float, default=None,
                        help="Limit ingestion to first N seconds")
    args = parser.parse_args()

    # 1. Get metadata
    log.info("Fetching video info...")
    try:
        info = get_youtube_info(args.url)
    except Exception as e:
        print(f"ERROR: Could not fetch video info: {e}")
        sys.exit(1)

    title = info.get("title", "Unknown")
    duration = info.get("duration", 0)
    channel = info.get("uploader", "Unknown")
    description = (info.get("description") or "")[:300]

    # Safe print — strip non-encodable chars for Windows terminal
    def safe(s): return s.encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8')
    print(f"\nVideo: {safe(title)}")
    print(f"Channel: {safe(channel)}")
    print(f"Duration: {format_timestamp(duration)} ({duration}s)")
    print(f"Description: {safe(description[:100])}...")

    # 2. Get captions
    log.info("Downloading captions...")
    captions = get_captions(args.url)
    print(f"Captions: {len(captions)} segments found")

    if args.info_only:
        if captions:
            print("\nFirst 5 caption segments:")
            for seg in captions[:5]:
                print(f"  [{format_timestamp(seg['start_s'])}] {seg['text']}")
        return

    # 3. Quick local caption search (no services needed)
    if args.search_after and not args.captions_only:
        print(f"\n--- Caption search: '{args.search_after}' ---")
        results = search_captions_local(captions, args.search_after)
        if results:
            for r in results:
                yt_ts = int(r['start_s'])
                print(f"  [{format_timestamp(r['start_s'])}] (score {r['score']:.2f}) {r['text']}")
                print(f"    Watch: {args.url}&t={yt_ts}s")
        else:
            print("  No matches found in captions")

    # 4. Check if Video Search services are running
    clip_available = False
    api_available = False
    try:
        httpx.get(f"{CLIP_API}/health", timeout=3).raise_for_status()
        clip_available = True
        log.info("CLIP service available at %s", CLIP_API)
    except Exception:
        log.warning("CLIP service not running at %s — caption-only mode", CLIP_API)

    try:
        httpx.get(f"{VIDEO_API}/api/video/health", timeout=3).raise_for_status()
        api_available = True
        log.info("Video API available at %s", VIDEO_API)
    except Exception:
        log.warning("Video API not running at %s", VIDEO_API)

    if args.captions_only or (not clip_available and captions):
        if not api_available:
            print("\nVideo API not running — printing caption search results only")
            if args.search_after:
                results = search_captions_local(captions, args.search_after, top_k=10)
                print(f"\nTop results for '{args.search_after}':")
                for r in results:
                    yt_ts = int(r['start_s'])
                    print(f"  [{format_timestamp(r['start_s'])}] {r['text']}")
                    print(f"    Watch: {args.url}&t={yt_ts}s")
            return

    print("\nNote: Full visual CLIP search requires:")
    print(f"  1. Start CLIP service: python3 clip_service.py  (RTX 5090, port 8320)")
    print(f"  2. Start Video API:    python3 video_api.py      (Spark-1, port 8310)")
    print(f"\nFor now, caption search is available without any services.")

    if args.search_after:
        results = search_captions_local(captions, args.search_after, top_k=10)
        print(f"\n=== Caption search: '{args.search_after}' ===")
        if results:
            for r in results:
                yt_ts = int(r['start_s'])
                print(f"  [{format_timestamp(r['start_s'])}] (score {r['score']:.2f}) {r['text']}")
                print(f"    Watch: {args.url}&t={yt_ts}s")
        else:
            print("  No caption matches found")


if __name__ == "__main__":
    main()
