# SECURITY FIX — Ollama Tunnel Removal
**Date**: 2026-04-01
**Executed by**: FORGE
**Severity**: CRITICAL — DoD fine-tuned models were publicly accessible
**Verdict**: FIXED

---

## What Was Exposed

The Cloudflare tunnel `ollama.ultrarag.app` was routing public internet traffic directly to the
Ollama API on Spark-1 (localhost:11434) with **zero authentication**. Anyone with the URL could:

- List all 46 models: `GET /api/tags`
- Query DoD fine-tuned models directly: `f15-expert`, `dod-cyber`
- Pull model weights, run arbitrary prompts, extract training artifacts

This is a critical data exposure incident under OWASP A02 (Cryptographic/Auth Failures) and
a potential violation of DoD data handling obligations.

---

## Config Before (relevant lines)

```yaml
ingress:
  - hostname: army.ultrarag.app
    service: http://localhost:8500
  - hostname: memoryweb.ultrarag.app
    service: http://10.0.0.2:8100
  - hostname: api.ultrarag.app
    service: http://localhost:8300
  - hostname: ollama.ultrarag.app          # <-- EXPOSED
    service: http://localhost:11434        # <-- REMOVED
  - hostname: ultrarag.app
    service: http://localhost:8300
  - hostname: voice.ultrarag.app
    service: http://localhost:9000
  - service: http_status:404
```

---

## Config After (grep confirms entry is gone)

```
$ grep -n ollama /etc/cloudflared/config.yml
(no output — entry removed)
```

Full config after fix:

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
  - hostname: ultrarag.app
    service: http://localhost:8300
  - hostname: voice.ultrarag.app
    service: http://localhost:9000
  - service: http_status:404
```

---

## Cloudflared Restart Status

```
Active: active (running) since Wed 2026-04-01 02:39:48 CDT
Main PID: 3093137 (cloudflared)
Registered tunnel connection connIndex=0 ... location=mia02 protocol=quic
```

Service restarted cleanly. No errors. All remaining tunnels reconnected.

---

## Curl Verification

```
$ curl -s --connect-timeout 10 https://ollama.ultrarag.app/api/tags
HTTP_STATUS=404
```

**Result: CLOSED.** The endpoint returns 404 (Cloudflare tunnel catch-all). No model list,
no API access, no response body. The Ollama service itself is still running on Spark-1 LAN
at localhost:11434 — it is accessible only from within the private network.

---

## Verdict: FIXED

The public Ollama API exposure has been eliminated. DoD models (`f15-expert`, `dod-cyber`)
are no longer reachable from the internet.

---

## Residual Risk

1. **Unknown exposure window**: The tunnel was active at an unknown start date. Any actor
   with prior knowledge of the URL may have already enumerated or queried the models.
   Check Cloudflare tunnel access logs if available to assess whether unauthorized queries
   occurred.

2. **Other services still public**: `army.ultrarag.app` (AI Army OS :8500) and
   `api.ultrarag.app` (Ultra RAG :8300) remain on the tunnel. Confirm both require
   authentication before any sensitive data can be accessed. SENTINEL should audit these.

3. **Ollama itself has no auth**: If any other internal service forwards traffic to
   localhost:11434 without a guard, the models remain exposed on LAN. This is acceptable
   for a private network but should be noted.

4. **Model weights on disk**: The LoRA adapters and fine-tuned models remain on Spark-1
   disk. Physical and SSH access controls are the only remaining protection.

---

## Recommended Follow-Up (SENTINEL)

- [ ] Audit Cloudflare tunnel access logs for `ollama.ultrarag.app` queries
- [ ] Confirm `api.ultrarag.app` requires auth before returning RAG content
- [ ] Confirm `army.ultrarag.app` requires auth before accepting task submissions
- [ ] Consider adding Cloudflare Access (zero-trust) in front of any future Ollama exposure
      if LAN-external access is ever needed
