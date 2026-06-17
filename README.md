# /fusion

A local fusion-style coding skill for Codex and Claude Code.

`/fusion` combines the compound-engineering workflow style with `claude-channel-cli` so Codex and Claude Code can collaborate without collapsing into one anchored opinion. It uses blind planning and review panels, writes durable artifacts, judges consensus and disagreement, and then runs a bounded engineering loop through implementation, verification, and commit/PR gates.

This is inspired by OpenRouter's Fusion pattern, adapted for local development. It is not a server-side multi-model API. It is a practical repo workflow for getting useful disagreement between two coding agents.

## Install

For Codex and other Agent Skills hosts:

```bash
npx skills add neocybereth/fusion-skill -g
```

For Claude Code plugin-style installs:

```bash
/plugin marketplace add neocybereth/fusion-skill
/plugin install fusion
```

The skill expects a reachable Claude Code session with `claude-channel-cli` enabled.

## Usage

```text
/fusion Add refresh-token rotation to the auth service
```

Typical loop:

```text
PLAN
  Codex writes an independent plan
  Claude writes an independent plan
  Codex judges consensus, contradictions, unique insights, and blind spots
  Codex synthesizes the implementation direction

IMPLEMENT
  One writer edits the repo

REVIEW
  Codex and Claude independently review the diff
  Findings are judged and synthesized

VERIFY
  Tests, build, browser checks, or dogfood checks run

COMMIT/PR
  User approval gate before commit, push, or PR
```

## Artifacts

Every run stores its memory under `.fusion/<run-id>/`:

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

These files make the loop resumable, reviewable, and easy to inspect after the agents disagree.

## What It Is Good For

- ambiguous implementation plans
- risky refactors
- review-heavy changes
- product or architecture tradeoffs
- using Claude Code's native harness from Codex
- preserving independent reasoning before synthesis

## What It Avoids

- no daemon
- no database
- no concurrent repo writers
- no pretending to do true parallel OpenRouter-style fanout
- no auto-commit or PR without a user gate

## Repository Layout

```text
skills/fusion/SKILL.md
skills/fusion/agents/openai.yaml
skills/fusion/references/
skills/fusion/scripts/
scripts/validate.py
```

The runtime contract lives in [skills/fusion/SKILL.md](skills/fusion/SKILL.md).
