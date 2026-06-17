---
name: fusion
description: Run a local fusion-style coding loop between Codex and Claude Code through claude-channel-cli. Use when the user asks for /fusion, Codex and Claude collaboration, blind panel planning or review, local OpenRouter Fusion-style development, or a compound-engineering loop that coordinates plan, implementation, review, verification, and commit/PR work.
---

# Fusion

Use this skill to coordinate Codex and a live Claude Code session as a local two-agent panel for real codebase work. The goal is not to mimic OpenRouter Fusion exactly. The goal is to adapt its strongest pattern locally: independent passes, a judge that exposes agreement and disagreement, and a synthesizer that chooses the next engineering action.

## Preconditions

- Use `claude-channel-cli` to communicate with Claude Code.
- If the Claude Channel MCP tools are not loaded, search for them with `tool_search` before falling back to the CLI.
- Call `list_claude_targets` or `status_claude_channel` before every `ask_claude` sequence.
- If multiple Claude targets are live, ask the user which visible Claude Code window to use.
- If no Claude target is reachable, stop and tell the user to start Claude Code with the channel enabled. Do not pretend the fusion loop ran.
- When compound-engineering skills are available, use them for their matching phase. If they are unavailable, continue with the closest local workflow and record the fallback in the run log.

## Non-Negotiables

1. Preserve blind independence. Send Claude only the frozen task or phase prompt, never Codex's draft answer.
2. Persist artifacts before moving to the next phase.
3. Use one writer at a time. Do not let Codex and Claude edit the same working tree concurrently.
4. Panel only judgment-heavy phases by default: planning and review.
5. Use explicit status values: `PROCEED`, `NEEDS_INPUT`, `BLOCKED`, or `DONE`.
6. Gate irreversible actions with the user: branch creation if disruptive, dependency installation, destructive changes, commits, pushes, and PR creation.
7. Bound the loop. Default to one panel round per phase, with a hard maximum of two rounds per phase unless the user explicitly asks for more.

## Start A Run

Create a run directory before the first panel:

```bash
python3 "$SKILL_DIR/scripts/init_fusion_run.py" --goal "USER GOAL"
```

Resolve `SKILL_DIR` to the directory that contains this `SKILL.md`. If this repository is checked out directly, `skills/fusion` is the skill directory. The script creates:

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

Keep all fusion artifacts in that run directory. They are the shared memory, audit trail, and resume point.

## Workflow

### 1. Orient

Read the user's goal, inspect the repository, and write a concise frozen task spec to `.fusion/<run-id>/task.md` and `round-1/task.md`.

Include:

- user goal
- repository path and branch
- relevant constraints
- current phase
- files or modules already known to matter
- budget limits or gates

### 2. Plan Panel

Run a blind panel:

- Codex writes its independent plan to `round-N/codex.md`.
- Ask Claude the same frozen task spec through `ask_claude`; save the answer to `round-N/claude.md`.
- Do not show Claude Codex's plan.
- Do not revise Codex's plan after reading Claude's answer; write corrections in judge or synthesis instead.

Judge the two plans in `round-N/judge.md` with exactly these sections:

```markdown
# Judge

## Consensus

## Contradictions

## Codex Unique Insights

## Claude Unique Insights

## Blind Spots

## Risks
```

Synthesize in `round-N/synthesis.md`:

```markdown
# Synthesis

STATUS: PROCEED
NEXT_PHASE: implement
WRITER: claude

## Decision

## Rationale

## Gates

## Next Prompt
```

If the plan is risky or ambiguous, set `STATUS: NEEDS_INPUT` and ask the user before implementation.

### 3. Implement

Use one writer. The writer may be Codex or Claude, but not both at once.

Default choices:

- Use Claude as writer when the user wants Claude Code's native compound-engineering loop.
- Use Codex as writer when Codex has more local context, loaded skills, or tool access for the task.

If Claude writes, ask it to use the relevant compound-engineering workflow, usually `ce-work`, and require a concise completion report with changed files, tests run, and blockers. After Claude finishes, Codex must inspect the diff before proceeding.

If Codex writes, make scoped edits locally and record the implementation summary in the run directory.

### 4. Review Panel

Panel the diff, not the whole original task.

- Codex reviews independently and writes findings to `round-N/codex.md`.
- Ask Claude to review the same diff or file list independently, preferably with `ce-code-review` in report-only mode. Save the answer to `round-N/claude.md`.
- Judge findings by severity, confidence, overlap, and actionability.
- Synthesize which fixes to apply.

Do not apply low-confidence review comments just because both agents produced words. Require a concrete failure mode.

### 5. Verify

Run the repository's normal checks. Use the most relevant compound-engineering verification skill when available:

- unit or integration tests
- typecheck or lint
- build
- browser or dogfood checks for UI changes
- targeted manual checks for behavior that automation cannot cover

Record commands and outcomes in the run directory. If verification fails, synthesize whether to return to implementation, ask the user, or block.

### 6. Commit Or PR

Commit, push, or open a PR only after a user gate. Use the repository's normal flow or `ce-commit-push-pr` if available.

Before the gate, show:

- summary of changes
- tests run
- remaining risks
- files changed
- proposed commit message or PR title

## Claude Prompts

Use `references/prompts.md` for phase-specific Claude prompts. Keep every Claude-facing prompt explicit and source-labeled with `From Codex:`.

For every Claude ask:

- include the phase
- include the frozen task or diff context
- state whether Claude is panelist, writer, or reviewer
- require a structured response
- require Claude to avoid editing unless assigned `WRITER`

## Status Handling

- `PROCEED`: continue to the next phase.
- `NEEDS_INPUT`: stop and ask the user a specific question.
- `BLOCKED`: stop after documenting the blocker and what was tried.
- `DONE`: final response may be sent.

If an artifact lacks a status, treat the phase as `BLOCKED` until clarified.

## Failure Modes

Read `references/protocol.md` when the loop gets complex, resumes after interruption, or hits disagreement. The common failures are:

- anchoring: Claude saw Codex's reasoning before writing its own
- stale channel: Claude target restarted or became unreachable
- conflicting edits: both agents wrote to the same files
- shallow agreement: judge found consensus without checking evidence
- context blowup: artifacts are too large to reuse directly
- runaway loop: no round cap or no explicit stop condition

Mitigate by freezing task specs, checking channel status before asks, using one writer, judging concrete claims, summarizing artifacts, and enforcing phase caps.
