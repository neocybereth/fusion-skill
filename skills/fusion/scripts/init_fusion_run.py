#!/usr/bin/env python3
"""Initialize a .fusion run directory for the fusion skill."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str, fallback: str = "task") -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug[:48].strip("-") or fallback


def write_new(path: Path, content: str) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a fusion run directory.")
    parser.add_argument("--goal", required=True, help="User goal for the fusion run.")
    parser.add_argument("--root", default=".", help="Repository root. Defaults to cwd.")
    parser.add_argument("--run-id", help="Optional explicit run id.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_id = args.run_id or f"{timestamp}-{slugify(args.goal)}"
    run_dir = root / ".fusion" / run_id
    round_dir = run_dir / "round-1"

    if run_dir.exists():
        raise FileExistsError(f"Run already exists: {run_dir}")

    round_dir.mkdir(parents=True)

    task = f"""# Fusion Task

Goal: {args.goal}

Repository: {root}
Run ID: {run_id}
Created UTC: {datetime.now(timezone.utc).isoformat(timespec="seconds")}

## Constraints

- Preserve blind independence between Codex and Claude panel answers.
- Use one writer at a time.
- Gate irreversible actions with the user.

## Current Phase

plan
"""

    state = {
        "run_id": run_id,
        "goal": args.goal,
        "repository": str(root),
        "phase": "plan",
        "round": 1,
        "status": "PROCEED",
        "writer": "none",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    write_new(run_dir / "task.md", task)
    write_new(run_dir / "decision-log.md", f"# Decision Log\n\n- {state['created_utc']} initialized run {run_id}\n")
    write_new(run_dir / "state.json", json.dumps(state, indent=2) + "\n")
    write_new(round_dir / "task.md", task)
    write_new(round_dir / "codex.md", "# Codex Panel\n\n")
    write_new(round_dir / "claude.md", "# Claude Panel\n\n")
    write_new(round_dir / "judge.md", "# Judge\n\n")
    write_new(round_dir / "synthesis.md", "# Synthesis\n\nSTATUS: PROCEED\nNEXT_PHASE: plan\nWRITER: none\n")

    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
