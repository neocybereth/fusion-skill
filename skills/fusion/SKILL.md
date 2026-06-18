---
name: fusion
description: Fusion loop for local coding work with Codex and Claude Code. Use when the user asks for /fusion, wants Codex and Claude collaboration through claude-channel-cli, requests a blind planning or review panel, needs claude-channel-cli setup guidance before fusion, or asks for a local OpenRouter Fusion-style compound-engineering loop.
---

# Fusion

Run a local fusion loop between Codex and a live Claude Code session. Fusion means a predictable process: freeze the task, get blind independent judgment, judge the disagreement, synthesize one next action, and let only one writer edit the repo at a time.

This skill is for codebase work where another independent agent can materially improve planning or review. It is not a server-side multi-model API, a daemon, or a reason to panel mechanical implementation steps.

## Core Rules

- Keep panel work blind: Claude must not see Codex's draft before writing its own.
- Persist every phase under `.fusion/<run-id>/` before using it to decide the next action.
- Use one writer per implementation or fix phase: `codex`, `claude`, or `none`.
- Panel planning and review by default. Do not panel implementation or routine verification unless the user explicitly asks.
- Stop on `NEEDS_INPUT`, `BLOCKED`, `DONE`, an unreachable Claude channel, or two non-converging panel rounds in one phase.
- Ask the user before destructive changes, dependency installs, commits, pushes, or PRs.

For detailed stop conditions, resume rules, and artifact contracts, read `references/protocol.md` when a run spans more than one phase, resumes after interruption, or hits disagreement.

For missing or unreachable Claude Channel setup, read `references/channel-setup.md` before telling the user what to do.

For Claude-facing prompt templates, read `references/prompts.md` before the first `ask_claude` call.

For compound-engineering skill mapping, read `references/compound-map.md` when `ce-*` skills are available.

## Step 1 - Check The Channel

Use `claude-channel-cli` to reach Claude Code. Diagnose setup before creating fusion artifacts.

1. If Claude Channel MCP tools are available, call `list_claude_targets`, then `status_claude_channel` for the selected target.
2. If MCP tools are unavailable, check CLI fallback with `command -v claude-channel`, `claude-channel --version`, and `claude-channel status`.
3. If the CLI is missing, or status/list shows no live target, stop the fusion run and walk the user through `references/channel-setup.md`.
4. If there is one live target, use it.
5. If there are multiple live targets, ask the user which visible Claude Code window to use.

Completion criterion: exactly one reachable Claude target is selected, or the run is stopped before any fusion artifacts claim Claude participated.

## Step 2 - Start Or Resume Artifacts

Resolve `SKILL_DIR` to the directory containing this `SKILL.md`. Start a new run with:

```bash
python3 "$SKILL_DIR/scripts/init_fusion_run.py" --goal "USER GOAL"
```

The run directory is:

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

For a resume, read the latest `.fusion/<run-id>/state.json` and latest `synthesis.md`, then verify the repository branch and Claude target still match the run.

Completion criterion: the active run has `task.md`, `state.json`, `decision-log.md`, and a current round directory before planning continues.

## Step 3 - Freeze The Task

Inspect the repository enough to write a concise frozen task in `round-N/task.md`.

Include:

- user goal
- repository path and branch
- current phase
- relevant constraints and gates
- files or modules already known to matter
- verification expectations

Do not include Codex's proposed solution in the frozen task. The task is the shared panel input.

Completion criterion: `round-N/task.md` is specific enough for Claude to produce an independent plan or review without seeing Codex's answer.

## Step 4 - Run A Blind Panel

Use this step for planning and review.

1. Codex writes its independent answer to `round-N/codex.md`.
2. Send Claude only `round-N/task.md` plus role instructions. Save the response to `round-N/claude.md`.
3. Do not revise `codex.md` after reading Claude. Put corrections in judge or synthesis.
4. Write `round-N/judge.md` with:
   - consensus
   - contradictions
   - Codex unique insights
   - Claude unique insights
   - blind spots
   - risks
5. Write `round-N/synthesis.md` starting with:

```markdown
STATUS: PROCEED
NEXT_PHASE: implement
WRITER: claude
```

Allowed statuses are `PROCEED`, `NEEDS_INPUT`, `BLOCKED`, and `DONE`.

Completion criterion: synthesis names one status, one next phase, one writer, the chosen action, and the reason discarded alternatives lost.

## Step 5 - Implement With One Writer

Assign exactly one writer from the synthesis.

- If `WRITER: claude`, ask Claude to use the relevant compound-engineering workflow, usually `ce-work`, and require a completion report with changed files, checks run, and blockers.
- If `WRITER: codex`, edit locally and record the implementation summary in the run directory.
- If the assigned writer needs to change scope materially, stop and write a new synthesis before continuing.

After implementation, the non-writer inspects the diff before review or verification.

Completion criterion: the writer's changed files are inspectable from the current checkout, and the run directory records what changed and what checks were run.

## Step 6 - Review The Diff

Use a blind panel on the diff when the change is non-trivial.

1. Freeze the review task with the goal, changed files, and focused diff context.
2. Codex writes findings to `round-N/codex.md`.
3. Ask Claude for an independent report-only review, preferably with `ce-code-review` if available. Save it to `round-N/claude.md`.
4. Judge findings by concrete failure mode, severity, confidence, overlap, and actionability.
5. Synthesize which fixes to apply and who writes them.

Do not apply a review comment unless it names a plausible failure mode.

Completion criterion: every accepted finding has an owner and fix plan, and every rejected material finding has a recorded reason.

## Step 7 - Verify

Run the checks appropriate to the changed surface:

- tests, typecheck, lint, or build
- browser or dogfood checks for UI changes
- targeted manual verification where automation is insufficient

Record commands and outcomes in the run directory. If checks fail, synthesize whether to return to implementation, ask the user, or block.

Completion criterion: verification evidence is recorded and the synthesis says either `DONE`, `PROCEED` to commit/PR, `PROCEED` back to implementation, `NEEDS_INPUT`, or `BLOCKED`.

## Step 8 - Commit Or PR Gate

Commit, push, or open a PR only after explicit user approval.

Before asking, show:

- change summary
- tests and checks run
- remaining risks
- files changed
- proposed commit message or PR title

Use `ce-commit-push-pr` when available and appropriate.

Completion criterion: the user approved the final git action, or the run stops before any irreversible git operation.
