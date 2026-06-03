#!/usr/bin/env python3
"""Install Skill Routing Kit into a local Codex home."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


BEGIN_MARKER = "<!-- BEGIN Skill Routing Kit -->"
END_MARKER = "<!-- END Skill Routing Kit -->"
PLUGIN_DIR_NAME = "skill-routing-kit"
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def default_codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()


def default_target() -> Path:
    return default_codex_home() / "plugins" / PLUGIN_DIR_NAME


def default_agents_path() -> Path:
    return default_codex_home() / "AGENTS.md"


def repo_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    manifest = root / ".codex-plugin" / "plugin.json"
    if not manifest.exists():
        raise SystemExit(f"Cannot find plugin manifest at {manifest}")
    return root


def should_skip(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    return path.suffix in SKIP_SUFFIXES


def copy_plugin(source: Path, target: Path) -> None:
    if target.exists():
        backup_root = target.parent / ".backups"
        backup_root.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = backup_root / f"{target.name}-{stamp}"
        shutil.move(str(target), str(backup_path))
        print(f"Backed up existing plugin to: {backup_path}")

    target.mkdir(parents=True, exist_ok=True)

    for item in source.rglob("*"):
        relative = item.relative_to(source)
        if should_skip(relative):
            continue
        destination = target / relative
        if item.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination)


def install_agents_snippet(snippet_path: Path, agents_path: Path) -> str:
    snippet = snippet_path.read_text(encoding="utf-8")
    agents_path.parent.mkdir(parents=True, exist_ok=True)

    if agents_path.exists():
        current = agents_path.read_text(encoding="utf-8")
    else:
        current = ""

    if BEGIN_MARKER in current and END_MARKER in current:
        before = current.split(BEGIN_MARKER, 1)[0].rstrip()
        after = current.split(END_MARKER, 1)[1].lstrip()
        updated = f"{before}\n\n{snippet.rstrip()}\n\n{after}".strip() + "\n"
        action = "Updated"
    else:
        separator = "\n\n" if current.strip() else ""
        updated = f"{current.rstrip()}{separator}{snippet.rstrip()}\n"
        action = "Added"

    agents_path.write_text(updated, encoding="utf-8")
    return action


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Skill Routing Kit without manually creating directories."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=default_target(),
        help="Plugin install directory. Default: $CODEX_HOME/plugins/skill-routing-kit or ~/.codex/plugins/skill-routing-kit.",
    )
    parser.add_argument(
        "--install-agents",
        action="store_true",
        help="Also install the routing guard snippet into an AGENTS.md file.",
    )
    parser.add_argument(
        "--agents",
        type=Path,
        default=default_agents_path(),
        help="AGENTS.md path used with --install-agents. Default: $CODEX_HOME/AGENTS.md or ~/.codex/AGENTS.md.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    source = repo_root()
    target = args.target.expanduser().resolve()

    if source.resolve() == target:
        print(f"Skill Routing Kit is already at: {target}")
    else:
        try:
            target.relative_to(source)
        except ValueError:
            pass
        else:
            raise SystemExit("Install target cannot be inside the repository being installed.")
        copy_plugin(source, target)
        print(f"Installed Skill Routing Kit to: {target}")

    if args.install_agents:
        snippet_path = target / "assets" / "agents-routing-snippet.md"
        action = install_agents_snippet(snippet_path, args.agents.expanduser().resolve())
        print(f"{action} routing guard in: {args.agents.expanduser().resolve()}")
    else:
        print("Routing guard not installed. Add --install-agents to enable it automatically.")

    print("Restart Codex or reload plugins if the new plugin does not appear immediately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
