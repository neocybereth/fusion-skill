# Fusion Protocol

Use this reference when running, resuming, or debugging a fusion loop.

## Artifact Rules

Every run lives under `.fusion/<run-id>/`.

```text
.fusion/<run-id>/
  task.md
  decision-log.md
  state.json
  round-1/
    task.md
    codex.md
    claude.md
    judge.md
    synthesis.md
```

Write artifacts before making dependent decisions. Prefer concise markdown over large transcripts. Link to full logs or command output files when needed.

## Round Types

### Panel Round

Use for planning and review.

1. Freeze `round-N/task.md`.
2. Write Codex's independent answer to `codex.md`.
3. Ask Claude the same frozen task. Save answer to `claude.md`.
4. Judge both answers in `judge.md`.
5. Choose next action in `synthesis.md`.
6. Append one line to `decision-log.md`.

### Writer Round

Use for implementation and verification.

1. Assign exactly one writer.
2. Give the writer a scoped prompt.
3. Save the writer's completion report.
4. Have the non-writer inspect the result before the next phase.

## Judge Rubric

The judge must identify:

- consensus points
- contradictions
- partial coverage
- unique insights from Codex
- unique insights from Claude
- blind spots for each side
- concrete risks and likely regressions

Reject vague judgments. A useful judgment names files, tests, commands, behavior, or code paths whenever possible.

## Synthesis Contract

Every synthesis starts with:

```markdown
STATUS: PROCEED
NEXT_PHASE: implement
WRITER: claude
```

Allowed statuses:

- `PROCEED`: continue.
- `NEEDS_INPUT`: ask the user before continuing.
- `BLOCKED`: no safe progress without external change.
- `DONE`: goal is handled.

Allowed phases:

- `orient`
- `plan`
- `implement`
- `review`
- `verify`
- `commit-pr`
- `done`

Allowed writer values:

- `codex`
- `claude`
- `none`

## Resume Procedure

1. Open the latest `.fusion/<run-id>/state.json` if present.
2. Read the latest `synthesis.md`.
3. Check repository status and current branch.
4. Re-check the Claude channel target.
5. Continue from `NEXT_PHASE` unless the repo state contradicts the artifact.

If state and repo disagree, write a new round explaining the mismatch and set `STATUS: NEEDS_INPUT` or synthesize a safe reconciliation.

## Stop Conditions

Stop when:

- the synthesis status is `DONE`, `NEEDS_INPUT`, or `BLOCKED`
- the phase has reached two panel rounds without convergence
- Claude channel becomes unreachable
- the writer reports changed files that Codex cannot inspect
- verification fails in a way that requires product judgment
- a commit, push, PR, destructive operation, or dependency install needs user approval

## Anti-Patterns

- Sending Claude Codex's draft before Claude's independent pass.
- Running panels on every mechanical step.
- Treating consensus as truth without inspecting evidence.
- Letting both agents write concurrently.
- Hiding all reasoning in chat instead of artifacts.
- Creating a daemon, database, or web UI before the artifact loop proves useful.
