---
task_id: "TASK-20260401-004"
title: "Deploy Hermes service health watchdog on Spark-1"
state: "delivered"
priority: "high"
owner: "FORGE"
route:
  - "AXIOM"
  - "FORGE"
  - "SENTINEL"
intake_file: ""
deliverable_file: "Spark-1:~/hermes-agent/scripts/health_check.sh + Hermes cron job service-health-watchdog"
verdict: "GO"
created_at: "2026-04-01"
updated_at: "2026-04-01"
definition_of_done: "health_check.sh exists on Spark-1, Hermes cron job service-health-watchdog created, Telegram report received with service status table, cron persists in ~/.hermes/cron/jobs.json"
blockers: []
---

# Task Summary

## Objective
Deploy an automated service health watchdog that runs every 4 hours via Hermes cron and sends Telegram alerts for down services on Spark-1 and Spark-2.

## Context
Multiple services had been found dead silently in previous sessions. No automated monitoring existed. Hermes (hermes-gateway.service) has terminal_tool (SSH) and cronjob_tools built in. Watchdog script written to ~/hermes-agent/scripts/health_check.sh, cron job created via Hermes, triggers every 4 hours.

## Evidence Required
- `~/hermes-agent/scripts/health_check.sh` created on Spark-1 with systemctl + port probe checks for both Spark-1 and Spark-2
- Hermes cron job `service-health-watchdog` created, interval 4h, persisted in `~/.hermes/cron/jobs.json`
- Telegram report received via @RonAIArmy_bot with service status table (timestamp + UP/DOWN per service)
- Alert prefix "ALERT:" confirmed for any DOWN service
- Covers: hermes-gateway, ai-army-telegram-bridge, ports 8300/8301/8500/8765/8767/11434 (Spark-1), ports 8100/8765/9902/8080/11434 (Spark-2), Docker containers on both nodes

## Notes
- Deployed 2026-03-31, verified same session via immediate test run
- Hermes runs as hermes-gateway.service with Restart=always — watchdog runs indefinitely with zero maintenance
