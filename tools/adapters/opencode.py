from __future__ import annotations

import re
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

_VALID_SKILL_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def opencode_skill_name(plugin: Plugin, skill_name: str) -> str:
    name = f"{plugin.name}-{skill_name}".replace("_", "-")
    if not _VALID_SKILL_NAME.fullmatch(name):
        raise ValueError(f"Invalid OpenCode skill name: {name}")
    if len(name) > 64:
        raise ValueError(f"OpenCode skill name is longer than 64 chars: {name}")
    return name


class OpenCodeAdapter(Adapter):
    key = "opencode"

    def generate(self, plugins: list[Plugin], *, dry_run: bool = False) -> list[Path]:
        root = REPO_ROOT / ".opencode" / "skills"
        clean_dir(root, dry_run=dry_run)
        written: list[Path] = []
        for plugin in plugins:
            for skill in skill_dirs(plugin):
                generated_name = opencode_skill_name(plugin, skill.name)
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
                harness_label="OpenCode",
                harness_key=self.key,
                skill_name=opencode_skill_name,
                dry_run=dry_run,
            )
        )
        return written
