# SECURITY FIX: Spark-2 Database LAN Binding — 2026-04-01

**Executed by:** FORGE
**Date:** 2026-04-01
**Verdict:** FIXED

---

## Summary

All four target databases on Spark-2 (MongoDB, Elasticsearch, Redis, Neo4j) were previously
binding to `0.0.0.0`, accepting unauthenticated connections from any device on the LAN.
Port bindings have been changed to `127.0.0.1` only. All five ports confirmed BLOCKED from
Spark-1 LAN after restart.

---

## Files Changed

### File 1 — Flywheel Stack (MongoDB + Redis + Elasticsearch)
**Path:** `/home/rblake2320/ai-business/nvidia-data-flywheel/deploy/docker-compose.yaml`

| Service | Old Binding | New Binding |
|---------|------------|-------------|
| Redis | `"6379:6379"` | `"127.0.0.1:6379:6379"` |
| MongoDB | `"27017:27017"` | `"127.0.0.1:27017:27017"` |
| Elasticsearch | `"9200:9200"` | `"127.0.0.1:9200:9200"` |

### File 2 — Video-Search Stack (Neo4j)
**Path:** `/home/rblake2320/ai-business/video-search-and-summarization/deploy/docker/local_deployment_single_gpu/compose.yaml`

| Service | Old Binding | New Binding |
|---------|------------|-------------|
| Neo4j HTTP | `"${GRAPH_DB_HTTP_PORT:-7474}:${GRAPH_DB_HTTP_PORT:-7474}"` | `"127.0.0.1:${GRAPH_DB_HTTP_PORT:-7474}:${GRAPH_DB_HTTP_PORT:-7474}"` |
| Neo4j Bolt | `"${GRAPH_DB_BOLT_PORT:-7687}:${GRAPH_DB_BOLT_PORT:-7687}"` | `"127.0.0.1:${GRAPH_DB_BOLT_PORT:-7687}:${GRAPH_DB_BOLT_PORT:-7687}"` |

---

## docker ps After Restart

```
NAMES                                    STATUS                    PORTS
local_deployment_single_gpu-graph-db-1   Up 16 seconds             127.0.0.1:7474->7474/tcp, 7473/tcp, 127.0.0.1:7687->7687/tcp
deploy-elasticsearch-1                   Up 35 seconds             127.0.0.1:9200->9200/tcp, 9300/tcp
deploy-redis-1                           Up 35 seconds             127.0.0.1:6379->6379/tcp
deploy-mongodb-1                         Up 35 seconds (healthy)   127.0.0.1:27017->27017/tcp
deploy-celery_worker-1                   Up Less than a second
deploy-api-1                             Up Less than a second
deploy-celery_parent_worker-1            Up 1 second
openshell-cluster-nemoclaw               Up 3 days (healthy)       0.0.0.0:8080->30051/tcp
memory-web-celery-1                      Up 3 days                 8100/tcp
memory-web-app-1                         Up 3 days (healthy)       0.0.0.0:8100->8100/tcp
memory-web-postgres-1                    Up 3 days (healthy)       0.0.0.0:5432->5432/tcp, 0.0.0.0:5433->5432/tcp
memory-web-redis-1                       Up 3 days (healthy)       6379/tcp
local_deployment_single_gpu-minio-1      Up 3 days                 0.0.0.0:9000-9001->9000-9001/tcp
```

All patched databases show `127.0.0.1:PORT->PORT` in the PORTS column.

---

## LAN Access Test Results (from Spark-1 at 192.168.12.132 → Spark-2 at 10.0.0.2)

| Port | Service | Result |
|------|---------|--------|
| 27017 | MongoDB | BLOCKED |
| 9200 | Elasticsearch | BLOCKED |
| 6379 | Redis | BLOCKED |
| 7474 | Neo4j HTTP | BLOCKED |
| 7687 | Neo4j Bolt | BLOCKED |

All five ports are now unreachable from the LAN.

---

## Services NOT Changed (Out of Scope)

The following remain on `0.0.0.0` — they are intentional or require separate review:

| Container | Port | Reason |
|-----------|------|--------|
| `openshell-cluster-nemoclaw` | 8080 | Application port — NemoClaw UI, intentionally accessible |
| `memory-web-app-1` | 8100 | MemoryWeb API — intentionally accessible (used by Cloudflare tunnel) |
| `memory-web-postgres-1` | 5432/5433 | PostgreSQL — separate stack, not in scope for this fix |
| `local_deployment_single_gpu-minio-1` | 9000-9001 | MinIO — separate review needed |

**Note on memory-web-postgres-1:** PostgreSQL on Spark-2 is exposed to `0.0.0.0:5432` and
`0.0.0.0:5433`. This was out of scope for this task but should be reviewed. If no LAN device
needs direct Postgres access (MemoryWeb app connects internally via Docker network), its host
binding should also be restricted to `127.0.0.1`.

**Note on MinIO (9000-9001):** Similarly exposed. Requires credential check and access scope
review before binding.

---

## Operational Impact

- Flywheel workers (celery + api) connect to MongoDB/Redis/Elasticsearch via `localhost` inside
  `network_mode: host` — these connections are unaffected by the host binding change.
- Neo4j is accessed by the video-search VIA server via Docker service name `graph-db` on the
  internal Docker network — unaffected.
- The internal application stack continues to function normally.

---

## Verdict: FIXED

All five unauthenticated database ports are now blocked from LAN access.
The fix is persistent — it lives in the docker-compose source files and will survive container
restarts.
