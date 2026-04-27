# PKA Machine Health Report

- Timestamp: 2026-04-03T16:49:35Z
- Overall: warnings present

## Checks
- chat_script: PASS | AI Army chat client present
- spark_key_present: PASS | Spark key path: C:\Users\techai\.ssh\ai_army_codex
- spark_ssh: WARN | Load key "C:\\Users\\techai\\.ssh\\ai_army_codex": Permission denied
rblake2320@192.168.12.132: Permission denied (publickey,password).
- aws_identity: PASS | arn:aws:iam::723013807658:user/Spark1-Agent

## Notes
- This is a live environment diagnostic, not a release verdict.
- Spark SSH warnings usually indicate key ACL, host trust, or network reachability issues outside the workspace code.
