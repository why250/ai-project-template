from __future__ import annotations

from pathlib import Path

from tools.adapters.base import (
    Adapter,
    Plugin,
    REPO_ROOT,
    clean_dir,
    emit_asset_index,
    emit_skill_dir,
    skill_dirs,
)


class GeminiAdapter(Adapter):
    key = "gemini"

    def generate(self, plugins: list[Plugin], *, dry_run: bool = False) -> list[Path]:
        root = REPO_ROOT / "skills"
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
        written.extend(
            emit_asset_index(
                plugins,
                root,
                harness_label="Gemini",
                harness_key=self.key,
                skill_name=lambda plugin, name: f"{plugin.name}__{name}",
                dry_run=dry_run,
            )
        )
        return written
