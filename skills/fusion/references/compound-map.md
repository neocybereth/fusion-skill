# Compound Engineering Map

Use this map when the compound-engineering skill stack is available. If a named skill is unavailable, continue with a local equivalent and record the fallback.

## Phase Mapping

| Fusion phase | Preferred compound skill | Notes |
| --- | --- | --- |
| orient | ce-brainstorm or ce-plan | Use only if requirements are unclear enough to merit a planning pass. |
| plan | ce-plan | Panel this phase. Codex and Claude should produce independent plans. |
| implement | ce-work | Single writer only. Do not panel mechanical edits. |
| review | ce-code-review | Panel this phase. Use report-only review before fixes. |
| verify | ce-test-browser, ce-dogfood-beta, project tests | Pick checks based on changed surface. |
| simplify | ce-simplify-code | Use after implementation if the diff is too complex. |
| commit-pr | ce-commit-push-pr | Hard user gate before commit, push, or PR. |
| document learning | ce-compound | Use after a solved non-trivial problem if the repo has a learning/docs pattern. |

## Selection Rules

- Use compound skills for workflow discipline, not as a substitute for judging evidence.
- Keep the fusion judge separate from the implementation writer.
- If Claude uses a compound skill, ask for a concise report rather than a transcript.
- If Codex uses a compound skill, still persist the phase decision in `.fusion/<run-id>/`.
