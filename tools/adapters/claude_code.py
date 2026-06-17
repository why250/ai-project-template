from __future__ import annotations

from pathlib import Path

from tools.adapters.base import Adapter, Plugin, REPO_ROOT, clean_dir, emit_skill_dir, skill_dirs


class ClaudeCodeAdapter(Adapter):
    key = "claude_code"

    def generate(self, plugins: list[Plugin], *, dry_run: bool = False) -> list[Path]:
        root = REPO_ROOT / ".claude" / "skills"
        clean_dir(root, dry_run=dry_run)
        written: list[Path] = []
        for plugin in plugins:
            for skill in skill_dirs(plugin):
                generated_name = f"{plugin.name}__{skill.name}"
                written.extend(
                    emit_skill_dir(
                        skill,
                        root / generated_name,
                        generated_name=generated_name,
                        dry_run=dry_run,
                    )
                )
        return written
