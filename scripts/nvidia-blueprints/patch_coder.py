"""Patch coder.py to integrate guardrails."""

with open('/home/rblake2320/ai-army-os/agents/coder.py') as f:
    src = f.read()

assert 'CoderGuardrails' not in src, "Already patched!"

# 1. Add import after existing imports
old_import = 'from tools.file_tool import read_file, list_files'
new_import = ('from tools.file_tool import read_file, list_files\n'
              'from agent_guardrails import CoderGuardrails, GuardrailViolation')
src = src.replace(old_import, new_import, 1)
assert 'CoderGuardrails' in src, "Import inject failed"

# 2. Initialize guardrail at top of _code_workflow after setup_git_config
old_setup = 'setup_git_config(repo_path, f"AI Army Coder ({self.agent_id})")'
new_setup = ('setup_git_config(repo_path, f"AI Army Coder ({self.agent_id})")\n\n'
             '        # Initialize guardrails for this task\n'
             '        guard = CoderGuardrails(allowed_paths=[repo_path])')
src = src.replace(old_setup, new_setup, 1)
assert 'guard = CoderGuardrails' in src, "Guard init inject failed"

# 3. Wrap the write_file call with guardrail check
old_write = '''            write_result = write_file(repo_path, rel_path, file_content)
            if write_result["ok"]:
                files_written.append(rel_path)
                logger.info(f"Wrote {rel_path} ({write_result['bytes']} bytes)")
            else:
                logger.warning(f"Failed to write {rel_path}: {write_result.get('error')}")'''

new_write = '''            # Guardrail check before writing — blocks dangerous patterns
            try:
                warns = guard.check_code_output(file_content, file_path=rel_path, repo_root=repo_path)
                if warns:
                    logger.warning("Guardrail WARNs for %s: %s", rel_path, [w.rule for w in warns])
            except GuardrailViolation as gv:
                logger.error("GUARDRAIL BLOCKED write to %s: %s", rel_path, gv)
                return {
                    "result": f"BLOCKED by safety guardrail: {gv}",
                    "model_used": None, "tokens": 0, "cost": 0.0,
                }
            write_result = write_file(repo_path, rel_path, file_content)
            if write_result["ok"]:
                files_written.append(rel_path)
                logger.info(f"Wrote {rel_path} ({write_result['bytes']} bytes)")
            else:
                logger.warning(f"Failed to write {rel_path}: {write_result.get('error')}")'''

src = src.replace(old_write, new_write, 1)
assert 'check_code_output' in src, "Guard check inject failed"

with open('/home/rblake2320/ai-army-os/agents/coder.py', 'w') as f:
    f.write(src)

print("coder.py patched successfully")
print(f"  import added:  {'CoderGuardrails' in src}")
print(f"  guard init:    {'guard = CoderGuardrails' in src}")
print(f"  check added:   {'check_code_output' in src}")
