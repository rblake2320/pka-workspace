#!/usr/bin/env python3
"""
AI Army -> aihangout.ai Participation Agent
Runs hourly on Spark-1, polls for unanswered problems, routes to the right agent, posts solutions.
Deploy to: /home/rblake2320/ai-business/scripts/aihangout_agents.py
"""

import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# -- Config ------------------------------------------------------------------
API_BASE = "https://aihangout.ai/api"
LOG_FILE = Path("/home/rblake2320/ai-business/logs/aihangout_agents.log")
STATE_FILE = Path("/home/rblake2320/ai-business/logs/aihangout_solved_ids.json")

# Passwords are loaded from environment variables — never hardcoded.
# Set these in the Spark-1 systemd service environment:
#   Environment=NOVA_AGENT_PASSWORD=<password>
#   Environment=FORGE_AGENT_PASSWORD=<password>
#   Environment=SENTINEL_AGENT_PASSWORD=<password>
_nova_pw = os.environ.get("NOVA_AGENT_PASSWORD")
_forge_pw = os.environ.get("FORGE_AGENT_PASSWORD")
_sentinel_pw = os.environ.get("SENTINEL_AGENT_PASSWORD")

if not all([_nova_pw, _forge_pw, _sentinel_pw]):
    raise OSError(
        "Missing required env vars: NOVA_AGENT_PASSWORD, FORGE_AGENT_PASSWORD, "
        "SENTINEL_AGENT_PASSWORD. Set these in the systemd service file."
    )

AGENTS = {
    "nova_agent": {
        "email": "nova_agent@aiarmyos.com",
        "password": _nova_pw,
        "agent_type": "research-agent",
        "keywords": [
            "ai", "ml", "research", "paper", "model", "dataset",
            "training", "pytorch", "tensorflow", "llm", "gpt",
            "batch", "learning", "neural", "rate limit", "api",
            "openai", "anthropic", "analysis", "gpu", "cuda",
        ],
        "categories": ["ai-ml", "AI/ML", "Data Science"],
        "model": "qwen2.5:7b",
    },
    "forge_agent": {
        "email": "forge_agent@aiarmyos.com",
        "password": _forge_pw,
        "agent_type": "code-agent",
        "keywords": [
            "javascript", "typescript", "python", "node", "react",
            "function", "implement", "build", "architecture", "code",
            "runtime", "backend", "frontend", "database", "algorithm",
            "performance", "optimize", "async", "promise", "class",
        ],
        "categories": ["Programming", "DevOps", "Software Engineering"],
        "model": "qwen2.5:7b",
    },
    "sentinel_agent": {
        "email": "sentinel_agent@aiarmyos.com",
        "password": _sentinel_pw,
        "agent_type": "qa-agent",
        "keywords": [
            "security", "cve", "vulnerability", "bug", "test",
            "validate", "audit", "compliance", "review", "qa",
            "azure", "aws", "authentication", "exploit", "rce",
            "injection", "xss", "csrf", "log", "monitor",
        ],
        "categories": ["Security", "QA", "Compliance"],
        "model": "qwen2.5:7b",
    },
}

# -- Logging -----------------------------------------------------------------
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("aihangout-agents")


# -- State -------------------------------------------------------------------
def load_solved_ids():
    if STATE_FILE.exists():
        try:
            return set(json.loads(STATE_FILE.read_text()))
        except Exception:
            pass
    return set()


def save_solved_ids(ids):
    STATE_FILE.write_text(json.dumps(sorted(ids)))


# -- Auth --------------------------------------------------------------------
def get_token(agent_name):
    cfg = AGENTS[agent_name]
    try:
        resp = requests.post(
            f"{API_BASE}/auth/login",
            json={"email": cfg["email"], "password": cfg["password"]},
            timeout=15,
        )
        data = resp.json()
        if data.get("success"):
            return data["token"]
        log.warning("Login failed for %s: %s", agent_name, data.get("error"))
    except Exception as e:
        log.error("Login error for %s: %s", agent_name, e)
    return None


# -- Problem fetching --------------------------------------------------------
def fetch_open_problems(limit=50):
    try:
        resp = requests.get(
            f"{API_BASE}/problems",
            params={"limit": limit, "sort": "newest"},
            timeout=15,
        )
        data = resp.json()
        if data.get("success"):
            return [p for p in data["problems"] if p.get("solution_count", 0) == 0]
    except Exception as e:
        log.error("Failed to fetch problems: %s", e)
    return []


# -- Routing -----------------------------------------------------------------
def score_problem_for_agent(problem, agent_name):
    cfg = AGENTS[agent_name]
    text = (
        problem.get("title", "") + " " +
        problem.get("description", "") + " " +
        (problem.get("category", "") or "") + " " +
        (problem.get("tags", "") or "")
    ).lower()
    score = 0
    for kw in cfg["keywords"]:
        if kw.lower() in text:
            score += 1
    cat = problem.get("category", "")
    if cat in cfg["categories"]:
        score += 3
    return score


def route_problem(problem):
    scores = {agent: score_problem_for_agent(problem, agent) for agent in AGENTS}
    best_agent, best_score = max(scores.items(), key=lambda x: x[1])
    log.debug("Routing problem %d scores: %s", problem["id"], scores)
    if best_score == 0:
        return None
    return best_agent


# -- Solution generation via Ollama ------------------------------------------
ROLE_PROMPTS = {
    "nova_agent": (
        "You are NOVA, an AI research and intelligence agent. "
        "Provide research-backed, accurate technical answers. "
        "Include code examples where appropriate. Be specific and practical."
    ),
    "forge_agent": (
        "You are FORGE, a senior software architect and builder. "
        "Provide working code implementations with clear explanations. "
        "Include edge cases and production considerations."
    ),
    "sentinel_agent": (
        "You are SENTINEL, a QA and security specialist. "
        "Provide thorough validation approaches, test cases, and security hardening steps. "
        "Be precise about risks and detection methods."
    ),
}


def generate_solution(problem, agent_name):
    cfg = AGENTS[agent_name]
    model = cfg["model"]
    role = ROLE_PROMPTS[agent_name]

    prompt = (
        f"{role}\n\n"
        f"Answer this problem from aihangout.ai:\n\n"
        f"TITLE: {problem['title']}\n"
        f"CATEGORY: {problem.get('category', 'General')}\n"
        f"DESCRIPTION: {problem['description']}\n\n"
        f"Write a clear, practical solution. Include code if relevant. "
        f"Be specific and accurate. Do not use placeholder text."
    )

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120,
        )
        solution = result.stdout.strip()
        if len(solution) < 50:
            log.warning("Ollama returned short response for problem %d", problem["id"])
            return None
        # Trim to stay under 10K limit
        if len(solution) > 8000:
            solution = solution[:8000] + "\n\n[Response trimmed for length]"
        return solution
    except subprocess.TimeoutExpired:
        log.error("Ollama timed out for problem %d", problem["id"])
    except Exception as e:
        log.error("Ollama error for problem %d: %s", problem["id"], e)
    return None


# -- Posting -----------------------------------------------------------------
def post_solution(problem_id, solution_text, agent_name, token):
    cfg = AGENTS[agent_name]
    try:
        resp = requests.post(
            f"{API_BASE}/problems/{problem_id}/solutions",
            headers={
                "Content-Type": "application/json",
                "X-Agent-Type": cfg["agent_type"],
                "Authorization": f"Bearer {token}",
            },
            json={"solutionText": solution_text},
            timeout=20,
        )
        data = resp.json()
        if data.get("success"):
            log.info(
                "Posted solutionId=%s by %s on problem %d",
                data.get("solutionId"), agent_name, problem_id,
            )
            return True
        else:
            log.warning("Post failed for problem %d: %s", problem_id, data.get("error"))
    except Exception as e:
        log.error("Post error for problem %d: %s", problem_id, e)
    return False


# -- Main --------------------------------------------------------------------
def run_once():
    log.info("=== AI Army aihangout.ai participation run: %s ===",
             datetime.now(timezone.utc).isoformat())

    solved_ids = load_solved_ids()
    problems = fetch_open_problems(limit=50)
    log.info("Fetched %d open problems, %d already solved by us",
             len(problems), len([p for p in problems if p["id"] in solved_ids]))

    new_problems = [p for p in problems if p["id"] not in solved_ids]
    if not new_problems:
        log.info("No new problems to solve this run")
        return

    # Get tokens upfront (one login per agent)
    tokens = {}
    for agent_name in AGENTS:
        t = get_token(agent_name)
        if t:
            tokens[agent_name] = t
        time.sleep(2)  # avoid hitting login rate limit (ip60: 10)

    if not tokens:
        log.error("No agents authenticated - aborting")
        return

    posted_count = 0
    max_posts_per_run = 3  # one per agent, conservative

    for problem in new_problems:
        if posted_count >= max_posts_per_run:
            log.info("Reached max posts per run (%d)", max_posts_per_run)
            break

        agent_name = route_problem(problem)
        if not agent_name:
            log.debug("No suitable agent for problem %d: %s",
                      problem["id"], problem["title"][:60])
            continue

        if agent_name not in tokens:
            log.warning("Agent %s has no valid token, skipping", agent_name)
            continue

        log.info("Routing problem %d '%s...' -> %s",
                 problem["id"], problem["title"][:50], agent_name)

        solution = generate_solution(problem, agent_name)
        if not solution:
            log.warning("No solution generated for problem %d", problem["id"])
            continue

        success = post_solution(problem["id"], solution, agent_name, tokens[agent_name])
        if success:
            solved_ids.add(problem["id"])
            save_solved_ids(solved_ids)
            posted_count += 1
            time.sleep(5)  # space out posts

    log.info("=== Run complete: %d solutions posted ===", posted_count)


if __name__ == "__main__":
    run_once()
