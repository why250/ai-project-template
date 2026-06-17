"""
Generate harness-native AI assets from plugins/.

plugins/ is the source of truth for portable AI assets. Adapters emit each harness'
native or native-ish discovery layout:

    cursor       -> .cursor/rules, .cursor/context, .cursor/skills
    codex        -> .codex/skills
    claude_code  -> .claude/skills
    gemini       -> skills
    opencode     -> .opencode/skills

Usage:
    python tools/generate_adapters.py --harness cursor
    python tools/generate_adapters.py --all
    python tools/generate_adapters.py --all --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.adapters.base import discover_plugins
from tools.adapters.claude_code import ClaudeCodeAdapter
from tools.adapters.codex import CodexAdapter
from tools.adapters.cursor import CursorAdapter
from tools.adapters.gemini import GeminiAdapter
from tools.adapters.opencode import OpenCodeAdapter

ADAPTERS = {
    "cursor": CursorAdapter(),
    "codex": CodexAdapter(),
    "claude_code": ClaudeCodeAdapter(),
    "gemini": GeminiAdapter(),
    "opencode": OpenCodeAdapter(),
}


def run(keys: list[str], *, dry_run: bool) -> None:
    plugins = discover_plugins()
    if not plugins:
        print("No plugins found.")
        return

    print("Discovered plugins:")
    for plugin in plugins:
        print(f"  - {plugin.name}")

    for key in keys:
        adapter = ADAPTERS[key]
        print(f"\nGenerating {key}...")
        written = adapter.generate(plugins, dry_run=dry_run)
        print(f"  {'Would write' if dry_run else 'Wrote'} {len(written)} file(s).")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate harness-native assets from plugins/.")
    parser.add_argument("--harness", nargs="+", choices=sorted(ADAPTERS), help="Harness adapters to run")
    parser.add_argument("--all", action="store_true", help="Run all adapters")
    parser.add_argument("--dry-run", action="store_true", help="Print planned writes without changing files")
    args = parser.parse_args()

    if args.harness and args.all:
        parser.error("Use either --harness or --all, not both.")
    if not args.harness and not args.all:
        parser.error("Pass --harness or --all.")

    keys = sorted(ADAPTERS) if args.all else args.harness
    run(keys, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
