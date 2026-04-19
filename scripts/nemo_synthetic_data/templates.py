from __future__ import annotations

from .models import InferenceSpec, LLMTextColumnSpec, ModelSpec, SamplerColumnSpec, TemplateSpec


DEFAULT_MODELS = [
    "nvidia/nemotron-3-nano-30b-a3b",
    "nvidia/nvidia-nemotron-nano-9b-v2",
    "nvidia/llama-3.3-nemotron-super-49b-v1.5",
    "mistralai/mistral-small-24b-instruct",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "meta/llama-4-scout-17b-16e-instruct",
]


def _primary_model(alias: str = "primary") -> list[ModelSpec]:
    return [
        ModelSpec(
            alias=alias,
            model=DEFAULT_MODELS[0],
            inference=InferenceSpec(temperature=0.55, top_p=0.9, max_tokens=700),
        )
    ]


def build_bpc_security_events_template() -> TemplateSpec:
    alias = "security-analyst"
    return TemplateSpec(
        name="bpc_security_events",
        description="Synthetic BPC/API auth events for anomaly tuning, demos, and security testing.",
        purpose=(
            "Generate structured security-event datasets around pair auth, replay defense, "
            "rate-limit pressure, signature misuse, and expected verdicts."
        ),
        tags=["security", "bpc", "anomaly-detection", "api-auth", "testing"],
        models=_primary_model(alias),
        context_defaults={
            "system_name": "BPC Protocol",
            "deployment_tier_hint": "production",
            "tenant_name": "Acme Systems",
            "region": "us-east-1",
        },
        context_help={
            "system_name": "Product or platform name the events should reference.",
            "deployment_tier_hint": "Human hint for the target environment.",
            "tenant_name": "Customer or tenant label used in analyst notes.",
            "region": "Primary region used in generated event narratives.",
        },
        columns=[
            SamplerColumnSpec(name="deployment_tier", sampler_type="category", params={"values": ["development", "staging", "production"], "weights": [1, 1, 3]}),
            SamplerColumnSpec(name="pair_scope", sampler_type="category", params={"values": ["read", "read-write", "admin"], "weights": [3, 4, 1]}),
            SamplerColumnSpec(name="endpoint_family", sampler_type="category", params={"values": ["status", "users", "billing", "admin", "webhooks", "partner-api"]}),
            SamplerColumnSpec(
                name="http_method",
                sampler_type="subcategory",
                params={
                    "category": "endpoint_family",
                    "values": {
                        "status": ["GET", "HEAD"],
                        "users": ["GET", "POST", "PATCH"],
                        "billing": ["GET", "POST"],
                        "admin": ["GET", "DELETE", "POST"],
                        "webhooks": ["POST"],
                        "partner-api": ["GET", "POST", "PUT"],
                    },
                },
            ),
            SamplerColumnSpec(name="client_type", sampler_type="category", params={"values": ["browser", "mobile", "server-agent", "ci-runner", "partner-integration"]}),
            SamplerColumnSpec(
                name="traffic_pattern",
                sampler_type="category",
                params={
                    "values": ["normal", "burst", "replay_attempt", "forged_signature", "unknown_pair", "scope_violation", "timestamp_skew", "rate_limit_probe"],
                    "weights": [5, 2, 1, 1, 1, 1, 1, 1],
                },
            ),
            SamplerColumnSpec(name="timestamp_skew_seconds", sampler_type="uniform", params={"low": -900, "high": 900}, convert_to="int"),
            SamplerColumnSpec(name="prior_failed_attempts", sampler_type="uniform", params={"low": 0, "high": 25}, convert_to="int"),
            SamplerColumnSpec(name="request_burst_size", sampler_type="uniform", params={"low": 1, "high": 120}, convert_to="int"),
            SamplerColumnSpec(
                name="expected_verdict",
                sampler_type="subcategory",
                params={
                    "category": "traffic_pattern",
                    "values": {
                        "normal": ["allow"],
                        "burst": ["allow", "rate_limit_exceeded"],
                        "replay_attempt": ["replay_detected"],
                        "forged_signature": ["invalid_signature", "pair_locked"],
                        "unknown_pair": ["unknown_pair"],
                        "scope_violation": ["scope_violation"],
                        "timestamp_skew": ["timestamp_expired"],
                        "rate_limit_probe": ["rate_limit_exceeded", "pair_locked"],
                    },
                },
            ),
            LLMTextColumnSpec(
                name="request_story",
                model_alias=alias,
                prompt=(
                    "Write a concise synthetic security event narrative for {{ tenant_name }} running {{ system_name }} in {{ deployment_tier }}. "
                    "The request came from a {{ client_type }} client targeting the {{ endpoint_family }} endpoint with HTTP {{ http_method }}. "
                    "Traffic pattern is '{{ traffic_pattern }}', prior failed attempts={{ prior_failed_attempts }}, request burst size={{ request_burst_size }}, "
                    "timestamp skew={{ timestamp_skew_seconds }} seconds, expected verdict={{ expected_verdict }}. Return only the narrative."
                ),
                system_prompt="You write crisp security event descriptions for synthetic datasets. Keep entries specific, realistic, and operational. No bullets, no JSON.",
            ),
            LLMTextColumnSpec(
                name="analyst_recommendation",
                model_alias=alias,
                prompt=(
                    "Given this synthetic event in {{ region }} for {{ system_name }}: scope={{ pair_scope }}, traffic_pattern={{ traffic_pattern }}, "
                    "expected_verdict={{ expected_verdict }}, prior_failed_attempts={{ prior_failed_attempts }}, request_burst_size={{ request_burst_size }}. "
                    "Write a one-sentence analyst recommendation describing the next action."
                ),
                system_prompt="Respond with one sentence only. Focus on detection, containment, or follow-up validation.",
            ),
        ],
    )


def build_api_abuse_patterns_template() -> TemplateSpec:
    alias = "abuse-model"
    return TemplateSpec(
        name="api_abuse_patterns",
        description="Reusable cross-project API abuse scenarios for security and resiliency testing.",
        purpose="Generate structured abuse-pattern datasets covering endpoint classes, actor profiles, pressure types, expected controls, and analyst summaries.",
        tags=["security", "api", "testing", "abuse", "resilience"],
        models=_primary_model(alias),
        context_defaults={"company_name": "Acme Systems", "product_name": "Unified Platform API", "compliance_focus": "SOC 2 and customer trust"},
        context_help={"company_name": "Company or customer whose API is being modeled.", "product_name": "API or product name referenced in narratives.", "compliance_focus": "Compliance or trust angle emphasized in summaries."},
        columns=[
            SamplerColumnSpec(name="actor_profile", sampler_type="category", params={"values": ["trusted-client", "partner", "botnet", "curious-user", "malicious-insider"]}),
            SamplerColumnSpec(name="endpoint_class", sampler_type="category", params={"values": ["public-read", "authenticated-read", "write", "admin", "webhook", "upload"]}),
            SamplerColumnSpec(name="abuse_type", sampler_type="category", params={"values": ["credential_stuffing", "scraping", "burst_write", "header_bloat", "payload_tampering", "replay", "permission_escalation"]}),
            SamplerColumnSpec(name="impact_band", sampler_type="category", params={"values": ["low", "medium", "high", "critical"], "weights": [2, 3, 3, 1]}),
            SamplerColumnSpec(name="expected_control", sampler_type="category", params={"values": ["rate_limit", "nonce_replay_detection", "signature_verification", "scope_enforcement", "header_size_guardrail", "manual_review"]}),
            SamplerColumnSpec(name="requests_per_minute", sampler_type="uniform", params={"low": 1, "high": 5000}, convert_to="int"),
            LLMTextColumnSpec(
                name="scenario_summary",
                model_alias=alias,
                prompt=(
                    "Write a realistic synthetic abuse scenario for {{ company_name }}'s {{ product_name }} API. Actor={{ actor_profile }}, endpoint={{ endpoint_class }}, "
                    "abuse_type={{ abuse_type }}, impact={{ impact_band }}, requests_per_minute={{ requests_per_minute }}, expected_control={{ expected_control }}. Return one compact paragraph."
                ),
                system_prompt="Write security test scenarios with operational realism. Avoid hype. No markdown.",
            ),
        ],
    )


def build_fraud_signals_template() -> TemplateSpec:
    alias = "fraud-analyst"
    return TemplateSpec(
        name="fraud_signals",
        description="Synthetic fraud-risk cases for transaction and account-abuse modeling.",
        purpose="Generate structured fraud cases with actor, transaction context, risk label, and investigator notes.",
        tags=["fraud", "risk", "payments", "detection"],
        models=_primary_model(alias),
        context_defaults={"merchant_name": "Acme Commerce", "risk_team": "Trust and Safety"},
        context_help={"merchant_name": "Merchant or platform being modeled.", "risk_team": "Internal team name used in summaries."},
        columns=[
            SamplerColumnSpec(name="actor_type", sampler_type="category", params={"values": ["new_user", "repeat_buyer", "seller", "bot", "account_takeover"]}),
            SamplerColumnSpec(name="transaction_type", sampler_type="category", params={"values": ["purchase", "refund", "payout", "gift_card", "account_change"]}),
            SamplerColumnSpec(name="signal_pattern", sampler_type="category", params={"values": ["normal", "velocity_spike", "geo_mismatch", "device_mismatch", "promo_abuse", "chargeback_cluster"]}),
            SamplerColumnSpec(name="risk_label", sampler_type="subcategory", params={"category": "signal_pattern", "values": {"normal": ["low"], "velocity_spike": ["medium", "high"], "geo_mismatch": ["medium", "high"], "device_mismatch": ["medium", "high"], "promo_abuse": ["medium"], "chargeback_cluster": ["high", "critical"]}}),
            SamplerColumnSpec(name="amount_usd", sampler_type="uniform", params={"low": 5, "high": 5000}, convert_to="int"),
            LLMTextColumnSpec(name="case_summary", model_alias=alias, prompt="Write a concise fraud investigation case summary for {{ merchant_name }}. Actor={{ actor_type }}, transaction_type={{ transaction_type }}, signal_pattern={{ signal_pattern }}, risk_label={{ risk_label }}, amount_usd={{ amount_usd }}. Return only the summary.", system_prompt="Write short operational fraud case summaries. No bullets, no markdown."),
            LLMTextColumnSpec(name="next_action", model_alias=alias, prompt="Write a one-sentence next action for {{ risk_team }} reviewing a case with risk_label={{ risk_label }} and signal_pattern={{ signal_pattern }}.", system_prompt="One sentence only. Focus on review, hold, block, or escalation."),
        ],
    )


def build_rag_eval_corpus_template() -> TemplateSpec:
    alias = "rag-eval"
    return TemplateSpec(
        name="rag_eval_corpus",
        description="Synthetic RAG evaluation rows with query, answer, evidence style, and grading target.",
        purpose="Generate reusable evaluation corpora for retrieval and answer quality testing.",
        tags=["rag", "evaluation", "knowledge-base", "qa"],
        models=_primary_model(alias),
        context_defaults={"domain_name": "Enterprise Knowledge Base", "audience": "operators"},
        context_help={"domain_name": "Knowledge domain used in the eval rows.", "audience": "Primary user group for the synthetic QA set."},
        columns=[
            SamplerColumnSpec(name="topic", sampler_type="category", params={"values": ["security", "billing", "deployment", "compliance", "troubleshooting"]}),
            SamplerColumnSpec(name="question_type", sampler_type="category", params={"values": ["fact_lookup", "procedure", "comparison", "policy", "edge_case"]}),
            SamplerColumnSpec(name="difficulty", sampler_type="category", params={"values": ["easy", "medium", "hard"], "weights": [2, 3, 2]}),
            SamplerColumnSpec(name="grading_target", sampler_type="category", params={"values": ["exactness", "groundedness", "citation_quality", "completeness"]}),
            LLMTextColumnSpec(name="user_query", model_alias=alias, prompt="Write a realistic user query for {{ domain_name }} aimed at {{ audience }}. topic={{ topic }}, question_type={{ question_type }}, difficulty={{ difficulty }}. Return only the query.", system_prompt="Write one realistic user query. No markdown."),
            LLMTextColumnSpec(name="ideal_answer", model_alias=alias, prompt="Write a concise ideal answer to a {{ question_type }} query in the {{ topic }} domain for {{ audience }}. Optimize for {{ grading_target }} and {{ difficulty }} difficulty.", system_prompt="Write a grounded answer suitable for evaluation. No markdown."),
        ],
    )


def build_bpc_verification_claims_template() -> TemplateSpec:
    alias = "verification-analyst"
    return TemplateSpec(
        name="bpc_verification_claims",
        description="Report-driven BPC production verification scenarios tied to concrete remediation claims.",
        purpose="Generate reusable verification scenarios and analyst notes for the exact BPC claims proven in the final production-readiness report.",
        tags=["bpc", "verification", "production", "security", "claims"],
        models=_primary_model(alias),
        context_defaults={"report_commit": "4611d4f", "protocol_version": "1.0.0", "project_name": "BPC Protocol"},
        context_help={"report_commit": "Commit or release identifier being verified.", "protocol_version": "Protocol version under verification.", "project_name": "System name used in generated narratives."},
        columns=[
            SamplerColumnSpec(name="verification_profile", sampler_type="category", params={"values": ["oversized_headers_signature", "oversized_headers_pair_id", "pair_lockout_flood", "scope_read_post_block", "scope_rw_delete_block", "scope_admin_delete_allow", "revocation_reuse_block", "nonce_lru_replay_detected", "nonce_lru_allow_burst"], "weights": [1, 1, 2, 2, 2, 1, 2, 2, 1]}),
            SamplerColumnSpec(name="claim_name", sampler_type="subcategory", params={"category": "verification_profile", "values": {"oversized_headers_signature": ["Oversized Headers"], "oversized_headers_pair_id": ["Oversized Headers"], "pair_lockout_flood": ["Pair Lockout"], "scope_read_post_block": ["Scope Enforcement"], "scope_rw_delete_block": ["Scope Enforcement"], "scope_admin_delete_allow": ["Scope Enforcement"], "revocation_reuse_block": ["Revocation Endpoint"], "nonce_lru_replay_detected": ["Unbounded Nonce Cap"], "nonce_lru_allow_burst": ["Unbounded Nonce Cap"]}}),
            SamplerColumnSpec(name="attack_vector", sampler_type="subcategory", params={"category": "verification_profile", "values": {"oversized_headers_signature": ["oversized_signature"], "oversized_headers_pair_id": ["oversized_pair_id"], "pair_lockout_flood": ["forged_signature_flood"], "scope_read_post_block": ["read_pair_post_attempt"], "scope_rw_delete_block": ["read_write_delete_attempt"], "scope_admin_delete_allow": ["admin_delete_control"], "revocation_reuse_block": ["revoked_pair_reuse"], "nonce_lru_replay_detected": ["nonce_burst_replay_mix"], "nonce_lru_allow_burst": ["lru_eviction_pressure"]}}),
            SamplerColumnSpec(name="pair_scope", sampler_type="subcategory", params={"category": "verification_profile", "values": {"oversized_headers_signature": ["read"], "oversized_headers_pair_id": ["read-write"], "pair_lockout_flood": ["read-write", "admin"], "scope_read_post_block": ["read"], "scope_rw_delete_block": ["read-write"], "scope_admin_delete_allow": ["admin"], "revocation_reuse_block": ["read-write", "admin"], "nonce_lru_replay_detected": ["read-write"], "nonce_lru_allow_burst": ["admin"]}}),
            SamplerColumnSpec(name="expected_http_status", sampler_type="subcategory", params={"category": "verification_profile", "values": {"oversized_headers_signature": [400], "oversized_headers_pair_id": [400], "pair_lockout_flood": [401], "scope_read_post_block": [403], "scope_rw_delete_block": [403], "scope_admin_delete_allow": [200], "revocation_reuse_block": [401], "nonce_lru_replay_detected": [401], "nonce_lru_allow_burst": [200]}}, convert_to="int"),
            SamplerColumnSpec(name="expected_error_code", sampler_type="subcategory", params={"category": "verification_profile", "values": {"oversized_headers_signature": ["invalid_signed_data"], "oversized_headers_pair_id": ["invalid_signed_data"], "pair_lockout_flood": ["pair_locked"], "scope_read_post_block": ["scope_violation"], "scope_rw_delete_block": ["scope_violation"], "scope_admin_delete_allow": ["allow"], "revocation_reuse_block": ["pair_revoked"], "nonce_lru_replay_detected": ["replay_detected"], "nonce_lru_allow_burst": ["allow"]}}),
            SamplerColumnSpec(name="remediation_area", sampler_type="subcategory", params={"category": "verification_profile", "values": {"oversized_headers_signature": ["middleware_size_guard"], "oversized_headers_pair_id": ["middleware_size_guard"], "pair_lockout_flood": ["pair_registry_lockout"], "scope_read_post_block": ["middleware_scope_gate"], "scope_rw_delete_block": ["middleware_scope_gate"], "scope_admin_delete_allow": ["middleware_scope_gate"], "revocation_reuse_block": ["server_revocation_route"], "nonce_lru_replay_detected": ["memory_store_lru_cap"], "nonce_lru_allow_burst": ["memory_store_lru_cap"]}}),
            SamplerColumnSpec(name="verification_probe", sampler_type="subcategory", params={"category": "verification_profile", "values": {"oversized_headers_signature": ["live_server_probe", "source_inspection"], "oversized_headers_pair_id": ["live_server_probe"], "pair_lockout_flood": ["async_harness_attack", "live_server_probe"], "scope_read_post_block": ["live_server_probe"], "scope_rw_delete_block": ["live_server_probe"], "scope_admin_delete_allow": ["live_server_probe"], "revocation_reuse_block": ["async_harness_attack", "live_server_probe"], "nonce_lru_replay_detected": ["live_server_probe"], "nonce_lru_allow_burst": ["live_server_probe", "source_inspection"]}}),
            LLMTextColumnSpec(name="verification_scenario", model_alias=alias, prompt="Write a concise verification scenario for {{ project_name }} v{{ protocol_version }} at commit {{ report_commit }}. Claim={{ claim_name }}, attack_vector={{ attack_vector }}, pair_scope={{ pair_scope }}, expected_http_status={{ expected_http_status }}, expected_error_code={{ expected_error_code }}, remediation_area={{ remediation_area }}, verification_probe={{ verification_probe }}. Return only the scenario text.", system_prompt="Write production verification scenarios as short, concrete test narratives. No bullets, no markdown, no JSON."),
            LLMTextColumnSpec(name="acceptance_note", model_alias=alias, prompt="Write a one-sentence acceptance note for this verified BPC claim: {{ claim_name }} via {{ verification_probe }} with expected outcome {{ expected_http_status }} {{ expected_error_code }}. Focus on what this proves operationally.", system_prompt="Respond with one sentence only. Keep it concrete and operational."),
        ],
    )


TEMPLATE_REGISTRY: dict[str, TemplateSpec] = {
    "api_abuse_patterns": build_api_abuse_patterns_template(),
    "bpc_security_events": build_bpc_security_events_template(),
    "bpc_verification_claims": build_bpc_verification_claims_template(),
    "fraud_signals": build_fraud_signals_template(),
    "rag_eval_corpus": build_rag_eval_corpus_template(),
}


def get_template(name: str) -> TemplateSpec:
    try:
        return TEMPLATE_REGISTRY[name]
    except KeyError as exc:
        known = ", ".join(sorted(TEMPLATE_REGISTRY))
        raise KeyError(f"unknown template '{name}'. Known templates: {known}") from exc
