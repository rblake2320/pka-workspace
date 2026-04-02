# FORGE — MemoryWeb Tunnel Fix Report
**Date**: 2026-03-30
**Agent**: FORGE
**Task**: Fix broken `memoryweb.ultrarag.app` Cloudflare tunnel on Spark-1

---

## Status: FIXED AND VERIFIED

---

## What the Config Looked Like Before

File: `/etc/cloudflared/config.yml` on Spark-1 (`192.168.12.132`)

```yaml
ingress:
  - hostname: army.ultrarag.app
    service: http://localhost:8500
  - hostname: memoryweb.ultrarag.app
    service: http://localhost:8100        # <-- WRONG: Spark-1 localhost has nothing on 8100
  - hostname: api.ultrarag.app
    service: http://localhost:8300
  - hostname: ollama.ultrarag.app
    service: http://localhost:11434
  - hostname: ultrarag.app
    service: http://localhost:8300
  - hostname: voice.ultrarag.app
    service: http://localhost:9000
  - service: http_status:404
```

MemoryWeb is not running on Spark-1. It runs on Spark-2 (`10.0.0.2`) at port `8100`.
Routing to `localhost:8100` on Spark-1 produced a connection refused error, breaking the tunnel.

---

## The Exact Change Made

**Single line changed** in `/etc/cloudflared/config.yml`:

```diff
  - hostname: memoryweb.ultrarag.app
-   service: http://localhost:8100
+   service: http://10.0.0.2:8100
```

Change method: Python inline edit via SSH (`str.replace` on file content). Multiline `sed` was
attempted first but failed due to YAML line boundary handling — Python was used instead.

**Config after change (full file):**

```yaml
tunnel: 0d7aa55d-6226-4cb4-a3e0-4fe51c314e36
credentials-file: /home/rblake2320/.cloudflared/0d7aa55d-6226-4cb4-a3e0-4fe51c314e36.json

ingress:
  - hostname: army.ultrarag.app
    service: http://localhost:8500
  - hostname: memoryweb.ultrarag.app
    service: http://10.0.0.2:8100
  - hostname: api.ultrarag.app
    service: http://localhost:8300
  - hostname: ollama.ultrarag.app
    service: http://localhost:11434
  - hostname: ultrarag.app
    service: http://localhost:8300
  - hostname: voice.ultrarag.app
    service: http://localhost:9000
  - service: http_status:404
```

---

## Cloudflared Restart

```
sudo systemctl restart cloudflared
```

Post-restart status confirmed: `active (running)` — 4 tunnel connections registered to
Cloudflare PoPs in Miami (mia01, mia02, mia09 x2) via QUIC protocol.

---

## Test Results

| Test | Result |
|------|--------|
| `curl -s -o /dev/null -w '%{http_code}' https://memoryweb.ultrarag.app/` | `200 OK` |
| `curl -s https://memoryweb.ultrarag.app/api/health` | `{"status":"ok","version":"0.1.0"}` |
| `curl -s https://memoryweb.ultrarag.app/api/memories?limit=1` | Returns memory items (93 total in DB) |

The service is responding with real data — this is confirmed live MemoryWeb traffic from Spark-2.

---

## Nothing Unexpected Found

- Only one cloudflared config exists: `/etc/cloudflared/config.yml`
- Only one cloudflared service: `cloudflared.service` (systemd, enabled at boot)
- Tunnel ID `0d7aa55d-6226-4cb4-a3e0-4fe51c314e36` is unchanged
- No other ingress rules were touched
- All other routes (ultrarag.app, army.ultrarag.app, etc.) remain on localhost as before

---

## Risk Note

Spark-1 routes to Spark-2 (`10.0.0.2`) over the local LAN. This path assumes:
1. Spark-2 is reachable from Spark-1 at `10.0.0.2` (confirmed by successful tunnel response)
2. MemoryWeb on Spark-2 stays on port 8100 (documented in CLAUDE.md and project memory)

If Spark-2 goes down, `memoryweb.ultrarag.app` will return a tunnel error — same as before.
No mitigation needed; this is the correct architecture.
