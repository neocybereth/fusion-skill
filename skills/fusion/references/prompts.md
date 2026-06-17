# Claude Prompt Templates

Use these as starting points. Replace bracketed text with task-specific context.

## Plan Panel

```text
From Codex:

We are running a blind local fusion panel. You are PANEL_B.

Do not assume Codex's answer. You have not seen it. Reason independently from the frozen task below.

Phase: plan
Repository: [absolute path]
Branch: [branch]

Frozen task:
[paste task.md]

Return:
1. Proposed plan
2. Files or modules likely involved
3. Risks and unknowns
4. Verification strategy
5. Questions that must be answered before implementation, if any

Do not edit files in this phase.
```

## Writer Implementation

```text
From Codex:

You are the assigned WRITER for this fusion run.

Phase: implement
Repository: [absolute path]
Branch: [branch]

Decision from synthesis:
[paste decision and constraints]

Use the relevant compound-engineering workflow if available, usually ce-work. Keep edits scoped to the approved plan.

When complete, return:
1. Summary
2. Files changed
3. Tests or checks run
4. Anything not completed
5. Any follow-up risks
```

## Review Panel

```text
From Codex:

We are running a blind review panel. You are PANEL_B reviewer.

Do not assume Codex's review. You have not seen it. Review independently.

Phase: review
Repository: [absolute path]
Branch: [branch]

Task:
[brief goal]

Diff or changed files:
[paste git diff summary, file list, or focused diff]

Use ce-code-review in report-only mode if available. Do not edit files.

Return findings first, ordered by severity. For each finding include:
- severity
- file and line if available
- concrete failure mode
- suggested fix
- confidence

If there are no material findings, say that clearly and list residual risks.
```

## Verification

```text
From Codex:

You are verifying a completed implementation for this fusion run.

Phase: verify
Repository: [absolute path]
Branch: [branch]

Goal:
[brief goal]

Changed files:
[file list]

Run the most relevant checks available. Prefer existing project commands. Use browser or dogfood checks for user-facing UI changes.

Return:
1. Commands run
2. Results
3. Failures and likely causes
4. Whether the task is ready for commit/PR
```

## Commit Or PR Gate

```text
From Codex:

Prepare, but do not perform, the final commit/PR step for this fusion run.

Phase: commit-pr
Repository: [absolute path]
Branch: [branch]

Goal:
[brief goal]

Implementation summary:
[summary]

Verification:
[commands and results]

Return:
1. Proposed commit message
2. Proposed PR title and body
3. Remaining risks
4. Any files that should not be committed

Do not commit, push, or create a PR unless explicitly instructed after this gate.
```
