#!/usr/bin/env python3
"""Validate the fusion skill repository without third-party dependencies."""

from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "fusion"


def fail(message: str) -> None:
    print(f"validate: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(path: Path) -> None:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail("SKILL.md is missing YAML frontmatter")

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            fail(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def main() -> int:
    require(SKILL_DIR / "SKILL.md")
    require(SKILL_DIR / "agents" / "openai.yaml")
    require(SKILL_DIR / "scripts" / "init_fusion_run.py")
    require(SKILL_DIR / "references" / "channel-setup.md")
    require(SKILL_DIR / "references" / "protocol.md")
    require(SKILL_DIR / "references" / "prompts.md")
    require(ROOT / ".claude-plugin" / "plugin.json")

    frontmatter = parse_frontmatter(SKILL_DIR / "SKILL.md")
    if frontmatter.get("name") != "fusion":
        fail("SKILL.md frontmatter name must be fusion")
    if len(frontmatter.get("description", "")) < 80:
        fail("SKILL.md description is too short to trigger reliably")
    extra_keys = sorted(set(frontmatter) - {"name", "description"})
    if extra_keys:
        fail(f"unexpected SKILL.md frontmatter keys: {', '.join(extra_keys)}")

    for json_path in [
        ROOT / ".claude-plugin" / "plugin.json",
        ROOT / ".claude-plugin" / "marketplace.json",
        ROOT / ".agents" / "plugins" / "marketplace.json",
    ]:
        require(json_path)
        json.loads(json_path.read_text(encoding="utf-8"))

    py_compile.compile(str(SKILL_DIR / "scripts" / "init_fusion_run.py"), doraise=True)
    print("validate: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
