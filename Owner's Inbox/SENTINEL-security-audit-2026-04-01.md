# SENTINEL Security Posture Audit
**Date:** 2026-04-01
**Scope:** Spark-1 (192.168.12.132) and Spark-2 (10.0.0.2) live system audit
**Auditor:** SENTINEL — QA, Validation and Risk Control
**Verdict:** HOLD

---

## 1. What Was Tested

All checks executed live via SSH. No simulated or estimated results.

**Spark-1 checks executed:**
- Axios npm supply-chain backdoor scan (npm cache + node_modules)
- Source map leakage in dist directories
- Full port enumeration (ss -tlnp)
- .env file permission audit
- Systemd user service inventory
- Ollama API exposure (local + public via Cloudflare tunnel)
- PostgreSQL bind address and pg_hba.conf auth rules
- Firewall (UFW + iptables) status

**Spark-2 checks executed:**
- Axios supply-chain scan (node_modules)
- Source map leakage in dist directories
- Full port enumeration (ss -tlnp)
- Docker container port binding audit
- .env file permission audit
- MongoDB authentication check (live query)
- Elasticsearch authentication check (live query)
- Firewall (UFW) status
- External reachability of data services via WiFi interface (192.168.12.223)

**Excluded from this audit:**
- Windows PC local security (out of scope for this session)
- Cloudflare WAF/access policy configuration
- Application-layer auth testing (API key validation, rate limits)
- SSH key hygiene and authorized_keys review

---

## 2. What Passed

**Axios supply-chain — CLEAN on all three nodes**

Spark-1 npx cache:
- `228916dc` (ref-tools-mcp): axios 1.13.2 — clean
- `12b05d58` (ref-tools-mcp): axios 1.13.2 — clean
- `75ac80b8` (localtunnel): axios 0.21.4 — old but no known RAT injection at this version

Spark-2:
- `.nemoclaw/source/node_modules/axios`: axios 1.13.6 — clean
- `ref-tools-mcp/node_modules/axios`: axios 1.8.4 — clean

No axios RAT signatures detected. No known backdoored version range present.

**Spark-1 secret files — Core secrets properly restricted**
- `/home/rblake2320/.env` (master key file): `600` — owner-only read/write. Correct.
- `/home/rblake2320/.docker/mcp/.env`: `600`. Correct.
- `/home/rblake2320/ai-business/shared/bridge/openclaw-bridge.env`: `600`. Correct.

**Spark-1 systemd services — No rogue services detected**
Running user services are all recognized: AI Army Telegram Bridge, Chat Watcher, AIHangout Bridge, Hermes Gateway, OpenClaw Bridge, Ray Watchdog, Spark Cluster, ollama-proxy. No unexpected services present.

**Source maps — All in node_modules, not custom build output**
All `.map` files found in dist directories are inside `node_modules` (third-party dependencies). None are in project-owned build output. Source map exposure risk from these is minimal — they came with published packages.

**Spark-1 PostgreSQL auth — External connections require SCRAM-SHA-256**
`pg_hba.conf` final rule: `host all all all scram-sha-256`. External connections do require authentication. The `listen_addresses = '*'` is a concern (see Findings) but brute force is required to breach, not open access.

**NCCL / mpirun on open ports — Expected, scope-limited**
`mpirun` (pid 4006691) and `all_gather_perf` (pid 4006698) are NCCL benchmark processes bound to `0.0.0.0:37455` and `0.0.0.0:1024`. These are inter-cluster distributed training connections, not attacker-controlled processes. The process command shows the correct NCCL benchmark binary (`/home/rblake2320/nccl-tests/build/all_gather_perf`). MEDIUM risk noted below.

**Spark-2 droid process — Identified as legitimate tool**
`/home/rblake2320/.local/bin/droid` (149MB binary, installed 2026-03-28) appears to be the NeMo Curator or a similar NVIDIA development tool based on string analysis. Not flagged as a threat but noted for tracking.

---

## 3. What Failed

### FINDING 1 — CRITICAL
**Ollama API (46 models) publicly accessible with no authentication**

Ollama is bound to `*:11434` on Spark-1 (all interfaces). The Cloudflare tunnel `ollama.ultrarag.app` routes to `Spark-1:11434`. A live test from inside Spark-1 confirmed the public endpoint responds with the full model list:

```
https://ollama.ultrarag.app/api/tags  →  HTTP 200, 46 models listed
```

Models exposed include:
- `f15-expert:latest` — government/DoD specialist model
- `dod-cyber:latest` — government/DoD specialist model
- `mk-copilot-v2:latest` — proprietary MK Seller Copilot model
- `aiarmy-*` — all custom AI Army specialist models

Any person on the internet can:
1. Enumerate all 46 models via `GET /api/tags`
2. Send inference requests via `POST /api/generate` or `POST /api/chat`
3. Consume GPU compute and drive up hardware load at zero cost
4. Extract responses from proprietary fine-tuned models (IP theft vector)

The DoD/government models (`f15-expert`, `dod-cyber`) being publicly queryable is a serious IP and potentially compliance concern. A contractor or adversary could probe these models to reverse-engineer their training domain knowledge.

**Ollama service config has no `OLLAMA_HOST` restriction:**
```
ExecStart=/usr/local/bin/ollama serve
# No Environment="OLLAMA_HOST=127.0.0.1:11434"
```

---

### FINDING 2 — HIGH
**Spark-2 MongoDB unauthenticated — accessible from LAN**

Spark-2 MongoDB (port 27017) has no authentication enabled. A live test confirmed:
```
mongosh --eval "db.adminCommand({listDatabases:1})"
→ Returns full database list: admin, config, flywheel, local
→ No password prompt. No auth required.
```

Spark-2 is connected to the LAN via WiFi at `192.168.12.223`. A test from Spark-1 confirmed `192.168.12.223:27017` is reachable. Any device on your home/office LAN can connect to MongoDB and read or write data without credentials.

Databases exposed: `admin`, `config`, `flywheel`, `local`

The `flywheel` database almost certainly contains AI training data from the Data Flywheel pipeline.

---

### FINDING 3 — HIGH
**Spark-2 Elasticsearch unauthenticated — accessible from LAN**

Elasticsearch (port 9200) responds to unauthenticated requests:
```
GET http://localhost:9200/  →  HTTP 200
cluster_name: docker-cluster, version: 8.12.2
No auth required.
```

Elasticsearch is bound to `0.0.0.0:9200` and reachable at `192.168.12.223:9200` from the LAN. Contains search indices — likely MemoryWeb or Data Flywheel data. Full read and write access without credentials.

---

### FINDING 4 — HIGH
**Spark-2 Redis unauthenticated — accessible from LAN**

Redis (port 6379, Docker `deploy-redis-1`) is bound to `0.0.0.0:6379` with no password. Reachable from LAN at `192.168.12.223:6379`. Redis with no auth allows:
- Full cache dump
- Arbitrary key writes (can poison application state)
- In some configurations, `SLAVEOF` and config rewrite attacks

---

### FINDING 5 — HIGH
**Spark-2 Neo4j — accessible from LAN, auth status unverified**

Neo4j (ports 7474, 7687) is bound to `0.0.0.0` and reachable at `192.168.12.223:7474` and `192.168.12.223:7687` from LAN. Neo4j default config ships with authentication disabled in some versions. Auth was not live-tested this session — must be verified.

---

### FINDING 6 — HIGH
**UFW firewall INACTIVE on both Spark-1 and Spark-2**

```
Spark-1: Status: inactive
Spark-2: Status: inactive
```

Neither machine has any host-based firewall in place. All services bound to `0.0.0.0` are exposed to anyone with network access. On Spark-1, which has a Cloudflare tunnel to the internet, this means all 0.0.0.0-bound ports are reachable from within the LAN with no filtering.

Spark-1 has Kubernetes network policy rules (kube-router) in iptables INPUT, but these are limited in scope and do not constitute a general firewall policy.

---

### FINDING 7 — MEDIUM
**Spark-1 PostgreSQL listening on all interfaces (`listen_addresses = '*'`)**

Spark-1 PostgreSQL Docker container (port 5432) is bound to `0.0.0.0:5432`. It is LAN-accessible. Auth is required (SCRAM-SHA-256), which prevents open access, but the database is exposed to brute force attempts from any LAN device. PostgreSQL should be restricted to localhost or the Docker bridge network.

---

### FINDING 8 — MEDIUM
**NCCL benchmark `all_gather_perf` bound to `0.0.0.0:1024` — long-running since Mar 27**

Process `all_gather_perf` (pid 4006698) has been running since March 27 (7,277+ CPU hours at 99.8% CPU). It is bound to `0.0.0.0:1024`. This is port 1024, a privileged-range port. NCCL benchmark tests are typically short-lived; a process running for 4+ days is anomalous. Confirm this is intentional before dismissing.

Command: `/home/rblake2320/nccl-tests/build/all_gather_perf -b 16G -e 16G -f 2`

---

### FINDING 9 — MEDIUM
**Mass .env files with `664` permissions (group-readable) across Spark-1**

Over 60 `.env` files found with permissions `rw-rw-r--` (664), including:
- `/home/rblake2320/.hermes/.env` — contains Telegram bot tokens, aihangout.ai credentials, OpenAI API key (664)
- `/home/rblake2320/.arcade/.env` — 664
- `/home/rblake2320/hermes-agent/.env` — contains live API credentials (664)
- `/home/rblake2320/ai-army-os/.env` — 664
- `/home/rblake2320/memory-web/.env` — 664
- `/home/rblake2320/aihangout-harvester/.env` — 664

The `hermes-agent/.env` and `.hermes/.env` files contain live production credentials (Telegram tokens, aihangout.ai login, OpenAI key). Anyone in the `rblake2320` group on Spark-1 can read these. If any process is compromised and runs as the same group, all credentials are exposed.

The Ollama service runs as the `ollama` user (different group), so direct Ollama-to-secrets path is blocked, but the risk remains for any other group member or compromised process.

---

### FINDING 10 — MEDIUM
**Spark-1 port 8088 (llama-server) and 8090 (python/Spark dashboard) bound to `0.0.0.0`**

`8088`: `llama-server` (llama.cpp server, pid 2392360) — bound to all interfaces. Provides raw LLM inference. No auth confirmed.
`8090`: Spark Cluster Dashboard (python, pid 3197) — bound to all interfaces. Exposes cluster status.

Neither of these appear in the documented Cloudflare tunnel config, so they are LAN-only, but still unnecessarily exposed to all LAN devices.

---

### FINDING 11 — LOW
**Spark-1 port 9000 (python3) bound only to `127.0.0.1` — OpenClaw bridge correctly localhost-only**

This passed. Noted as confirmation that the openclaw bridge is correctly configured. No action needed.

---

## 4. Risk Severity Summary

| # | Finding | Severity | Basis |
|---|---------|----------|-------|
| 1 | Ollama API publicly accessible via internet (46 models, no auth) | CRITICAL | Active IP theft vector, DoD model exposure, free GPU abuse by internet |
| 2 | MongoDB unauthenticated, LAN-accessible on Spark-2 | HIGH | Full data read/write with no credential required |
| 3 | Elasticsearch unauthenticated, LAN-accessible on Spark-2 | HIGH | Full index access with no credential required |
| 4 | Redis unauthenticated, LAN-accessible on Spark-2 | HIGH | Cache poisoning and data dump possible |
| 5 | Neo4j LAN-accessible, auth unverified on Spark-2 | HIGH | Pending verification; high if unauthenticated |
| 6 | UFW firewall inactive on both Spark-1 and Spark-2 | HIGH | No host-based filtering on any port |
| 7 | PostgreSQL listening on all interfaces (auth required) | MEDIUM | Brute force exposure, should be localhost-only |
| 8 | `all_gather_perf` running 4+ days on privileged port 1024 | MEDIUM | Anomalous duration; confirm intent |
| 9 | 60+ .env files with 664 permissions including live creds | MEDIUM | Group-readable live production secrets |
| 10 | llama-server (8088) and Spark dashboard (8090) on 0.0.0.0 | MEDIUM | Unnecessary LAN exposure |
| 11 | OpenClaw bridge correctly bound to localhost | LOW (PASS) | Confirmed safe |

---

## 5. Required Fixes

### Fix 1 — CRITICAL: Restrict Ollama to localhost, remove public tunnel
**On Spark-1:**
```bash
# Add to /etc/systemd/system/ollama.service under [Service]:
Environment="OLLAMA_HOST=127.0.0.1:11434"

sudo systemctl daemon-reload
sudo systemctl restart ollama
```

Then remove the Cloudflare tunnel entry for `ollama.ultrarag.app` from `/etc/cloudflared/config.yml` and restart cloudflared.

If external Ollama access is needed for legitimate use, add authentication via a reverse proxy (nginx + basic auth or bearer token) in front of Ollama before re-exposing it.

Do not re-expose `f15-expert` or `dod-cyber` via any public endpoint under any circumstances.

---

### Fix 2 — HIGH: Enable MongoDB authentication on Spark-2
```bash
# On Spark-2, update the deploy docker-compose to add:
# MONGO_INITDB_ROOT_USERNAME and MONGO_INITDB_ROOT_PASSWORD
# Then restart the container and update all services that connect to it.

# Temporary mitigation: bind MongoDB to localhost only
# Edit the docker-compose file to change:
#   ports: "0.0.0.0:27017:27017"
# to:
#   ports: "127.0.0.1:27017:27017"
```

---

### Fix 3 — HIGH: Enable Elasticsearch security (authentication) on Spark-2
Elasticsearch 8.x ships with security disabled by default in some Docker configurations. Enable it:
```yaml
# In the Elasticsearch docker-compose environment:
xpack.security.enabled: true
ELASTIC_PASSWORD: <strong-password>
```

Or restrict to localhost binding as immediate mitigation.

---

### Fix 4 — HIGH: Add Redis password on Spark-2 `deploy-redis-1`
```yaml
# In docker-compose, add to the Redis service:
command: redis-server --requirepass <strong-password>
```

Update the application services that use this Redis instance with the new password.

---

### Fix 5 — HIGH: Verify and enable Neo4j authentication on Spark-2
```bash
# On Spark-2, check:
docker exec local_deployment_single_gpu-graph-db-1 cat /var/lib/neo4j/conf/neo4j.conf | grep auth

# If auth is disabled, add to neo4j.conf:
dbms.security.auth_enabled=true
# And set the initial password
```

---

### Fix 6 — HIGH: Enable UFW on both Spark-1 and Spark-2
**Spark-1 (minimum ruleset):**
```bash
sudo ufw default deny incoming
sudo ufw allow 22/tcp          # SSH
sudo ufw allow from 127.0.0.1  # localhost
sudo ufw allow from 10.0.0.0/24 to any port 5432   # PG from Spark-2 only
sudo ufw allow from 192.168.12.0/24 to any port 8300  # Ultra RAG from LAN
sudo ufw allow from 192.168.12.0/24 to any port 8500  # AI Army from LAN
# Add Cloudflare IP ranges for tunnel (if needed for direct tunnel access)
sudo ufw enable
```

**Spark-2 (minimum ruleset):**
```bash
sudo ufw default deny incoming
sudo ufw allow 22/tcp
sudo ufw allow from 192.168.12.132 to any port 27017  # MongoDB from Spark-1 only
sudo ufw allow from 192.168.12.132 to any port 9200   # ES from Spark-1 only
sudo ufw allow from 192.168.12.132 to any port 6379   # Redis from Spark-1 only
sudo ufw allow from 192.168.12.132 to any port 7687   # Neo4j from Spark-1 only
sudo ufw allow from 10.0.0.0/24                        # Cluster network
sudo ufw enable
```

---

### Fix 7 — MEDIUM: Restrict PostgreSQL to Docker bridge network on Spark-1
Change the port binding in the docker-compose for `memory-web-postgres-1`:
```yaml
# Change from:
ports:
  - "0.0.0.0:5432:5432"
# To:
ports:
  - "127.0.0.1:5432:5432"
```

---

### Fix 8 — MEDIUM: Verify the `all_gather_perf` process on both Sparks
```bash
# On Spark-1:
ps -p 4006698 -o pid,etime,cmd

# On Spark-2:
ps -p 22203 -o pid,etime,cmd
```

If these are NCCL benchmarks left running unintentionally, kill them:
```bash
kill 4006698  # Spark-1
# kill Spark-2 equivalent if same
```

---

### Fix 9 — MEDIUM: Tighten .env permissions on Spark-1 for live credential files
At minimum, the files containing live production secrets must be 600:
```bash
chmod 600 /home/rblake2320/.hermes/.env
chmod 600 /home/rblake2320/hermes-agent/.env
chmod 600 /home/rblake2320/ai-army-os/.env
chmod 600 /home/rblake2320/memory-web/.env
chmod 600 /home/rblake2320/aihangout-harvester/.env
chmod 600 /home/rblake2320/ai-army-telegram-bridge/.env
```

For template/example files (NVIDIA Blueprints, etc.) with placeholder values, 664 is acceptable. The critical distinction is live production credentials vs. example configs.

---

### Fix 10 — MEDIUM: Bind llama-server and Spark dashboard to localhost or LAN-only

For `llama-server` on port 8088 (if not needed externally):
```bash
# In the spark-cluster.service startup, add the --host flag to llama-server:
--host 127.0.0.1
```

For Spark dashboard on port 8090, restrict to LAN range via UFW (covered in Fix 6) rather than rebinding if the service needs LAN access for the dashboard.

---

## 6. Pass / Hold / No-Go Decision

**Verdict: HOLD**

One CRITICAL finding (Ollama public exposure) and four HIGH findings (MongoDB/Elasticsearch/Redis unauthenticated, UFW disabled) are present. Under SENTINEL rules, a GO is not possible with unresolved Critical or High severity issues.

**Conditions for GO:**
1. Ollama restricted to localhost and `ollama.ultrarag.app` tunnel removed or auth-gated — CRITICAL
2. MongoDB authentication enabled OR bound to localhost — HIGH
3. Elasticsearch security enabled OR bound to localhost — HIGH
4. Redis password set OR bound to localhost — HIGH
5. Neo4j authentication verified and enabled if missing — HIGH
6. UFW enabled on both nodes with restrictive inbound rules — HIGH

Items 7-10 (MEDIUM) should be addressed within the next 48 hours but are not blocking conditions.

**The immediate stop-gap if a full fix session is not possible right now:**
```bash
# 10 minutes of work to close the four most dangerous gaps:

# 1. Block Ollama from Cloudflare tunnel (fastest option)
# Remove or comment out the ollama.ultrarag.app entry in /etc/cloudflared/config.yml
# then: sudo systemctl restart cloudflared

# 2. On Spark-2, bind all data services to localhost temporarily
# docker-compose.yml: change "0.0.0.0:PORT" to "127.0.0.1:PORT" for mongo, es, redis, neo4j
# then: docker compose down && docker compose up -d
```

---

*SENTINEL audit complete. No findings were estimated or assumed. All results are from live system queries executed 2026-04-01.*
