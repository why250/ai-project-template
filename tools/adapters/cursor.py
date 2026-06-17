from __future__ import annotations

from pathlib import Path

from tools.adapters.base import Adapter, Plugin, REPO_ROOT, clean_dir, copy_tree


class CursorAdapter(Adapter):
    key = "cursor"

    def generate(self, plugins: list[Plugin], *, dry_run: bool = False) -> list[Path]:
        written: list[Path] = []
        outputs = [
            REPO_ROOT / ".cursor" / "rules",
            REPO_ROOT / ".cursor" / "context",
            REPO_ROOT / ".cursor" / "skills",
        ]
        for out in outputs:
            clean_dir(out, dry_run=dry_run)

        for plugin in plugins:
            written.extend(copy_tree(plugin.rules_cursor_dir, REPO_ROOT / ".cursor" / "rules", dry_run=dry_run))
            written.extend(copy_tree(plugin.context_dir, REPO_ROOT / ".cursor" / "context", dry_run=dry_run))
            written.extend(copy_tree(plugin.skills_dir, REPO_ROOT / ".cursor" / "skills", dry_run=dry_run))
        return written
