"""Patch llm_router.py to add flywheel tier support."""

with open('/home/rblake2320/ai-army-os/llm_router.py') as f:
    src = f.read()

assert 'flywheel' not in src, "Already patched!"

# 1. Add flywheel to TIER_ORDER so it's tried before other tiers
old_tier = 'TIER_ORDER = ["fast", "medium", "strong", "strongest"]'
new_tier = 'TIER_ORDER = ["flywheel", "fast", "medium", "strong", "strongest"]'
src = src.replace(old_tier, new_tier, 1)
assert 'flywheel' in src, "Tier order patch failed"

# 2. Extend _auto_select to include flywheel in complexity routing
old_select = '        tier_map = {"simple": "fast", "medium": "medium", "complex": "strong", "fast": "fast"}'
new_select = ('        tier_map = {"simple": "fast", "medium": "medium", "complex": "strong", "fast": "fast",\n'
              '                     "flywheel": "flywheel"}  # Explicit flywheel routing')
src = src.replace(old_select, new_select, 1)

# 3. Add flywheel_complete() convenience method before list_providers
old_list = '    def list_providers(self) -> dict:'
new_list = '''    def flywheel_complete(
        self,
        messages: list,
        fallback_complexity: str = "medium",
        **kwargs,
    ) -> dict:
        """
        Route to flywheel-tier model if available, else fall back.
        Use this when you want to A/B test the fine-tuned model.
        """
        flywheel_candidates = self._get_models_by_tier("flywheel")
        if flywheel_candidates:
            # Try flywheel model first
            try:
                return self.complete(messages, model="auto", complexity="flywheel", **kwargs)
            except Exception as e:
                logger.warning("Flywheel model failed, falling back: %s", e)
        # Fall back to standard routing
        return self.complete(messages, model="auto", complexity=fallback_complexity, **kwargs)

    def list_providers(self) -> dict:'''

src = src.replace(old_list, new_list, 1)
assert 'flywheel_complete' in src, "flywheel_complete inject failed"

with open('/home/rblake2320/ai-army-os/llm_router.py', 'w') as f:
    f.write(src)

print("llm_router.py patched successfully")
print(f"  flywheel tier in TIER_ORDER: {'flywheel' in src}")
print(f"  flywheel_complete method: {'flywheel_complete' in src}")
