from __future__ import annotations

import json
import shutil
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGINS_DIR = REPO_ROOT / "plugins"


@dataclass(frozen=True)
class Plugin:
    name: str
    root: Path
    manifest: dict

    @property
    def rules_cursor_dir(self) -> Path:
        return self.root / "rules" / "cursor"

    @property
    def context_dir(self) -> Path:
        return self.root / "context"

    @property
    def skills_dir(self) -> Path:
        return self.root / "skills"


def discover_plugins() -> list[Plugin]:
    plugins: list[Plugin] = []
    if not PLUGINS_DIR.exists():
        return plugins

    for manifest_path in sorted(PLUGINS_DIR.glob("*/plugin.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        plugins.append(
            Plugin(
                name=manifest["name"],
                root=manifest_path.parent,
                manifest=manifest,
            )
        )
    return plugins


def ensure_inside_repo(path: Path) -> Path:
    resolved = path.resolve()
    root = REPO_ROOT.resolve()
    if resolved != root and root not in resolved.parents:
        raise ValueError(f"Refusing to write outside repository: {resolved}")
    return resolved


def clean_dir(path: Path, *, dry_run: bool) -> None:
    resolved = ensure_inside_repo(path)
    if not resolved.exists():
        return
    if dry_run:
        print(f"  Would clean: {resolved.relative_to(REPO_ROOT)}")
        return
    shutil.rmtree(resolved)


def copy_tree(src: Path, dst: Path, *, dry_run: bool) -> list[Path]:
    written: list[Path] = []
    if not src.exists():
        return written

    for item in sorted(src.rglob("*")):
        if not item.is_file():
            continue
        rel = item.relative_to(src)
        out = ensure_inside_repo(dst / rel)
        written.append(out)
        if dry_run:
            print(f"  Would write: {out.relative_to(REPO_ROOT)}")
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, out)
    return written


def skill_dirs(plugin: Plugin, *, include_private: bool = False) -> list[Path]:
    if not plugin.skills_dir.exists():
        return []
    dirs = []
    for path in sorted(plugin.skills_dir.iterdir()):
        if not path.is_dir():
            continue
        if not include_private and path.name.startswith("_"):
            continue
        if (path / "SKILL.md").exists():
            dirs.append(path)
    return dirs


def context_provider_files(plugin: Plugin) -> list[Path]:
    """Return public Cursor context providers from a plugin."""
    if not plugin.context_dir.exists():
        return []
    return [
        path
        for path in sorted(plugin.context_dir.glob("*.mdc"))
        if path.is_file() and not path.name.startswith("_")
    ]


def rewrite_skill_name(content: str, name: str) -> str:
    if not content.startswith("---\n"):
        return f"---\nname: {name}\n---\n\n{content}"

    end = content.find("\n---", 4)
    if end == -1:
        return content

    frontmatter = content[4:end].splitlines()
    body = content[end + len("\n---") :]
    found = False
    rewritten: list[str] = []
    for line in frontmatter:
        if line.startswith("name:"):
            rewritten.append(f"name: {name}")
            found = True
        else:
            rewritten.append(line)
    if not found:
        rewritten.insert(0, f"name: {name}")
    return "---\n" + "\n".join(rewritten) + "\n---" + body


def emit_skill_dir(
    src_dir: Path,
    dst_dir: Path,
    *,
    generated_name: str,
    dry_run: bool,
) -> list[Path]:
    written: list[Path] = []
    skill_md = src_dir / "SKILL.md"
    if not skill_md.exists():
        return written

    out_skill = ensure_inside_repo(dst_dir / "SKILL.md")
    written.append(out_skill)
    if dry_run:
        print(f"  Would write: {out_skill.relative_to(REPO_ROOT)}")
    else:
        out_skill.parent.mkdir(parents=True, exist_ok=True)
        content = skill_md.read_text(encoding="utf-8")
        out_skill.write_text(rewrite_skill_name(content, generated_name), encoding="utf-8")

    for item in sorted(src_dir.rglob("*")):
        if not item.is_file() or item.name == "SKILL.md":
            continue
        rel = item.relative_to(src_dir)
        out = ensure_inside_repo(dst_dir / rel)
        written.append(out)
        if dry_run:
            print(f"  Would write: {out.relative_to(REPO_ROOT)}")
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, out)

    return written


def emit_asset_index(
    plugins: list[Plugin],
    dst_dir: Path,
    *,
    harness_label: str,
    harness_key: str,
    skill_name: Callable[[Plugin, str], str],
    dry_run: bool,
) -> list[Path]:
    """Emit a README that explains generated non-Cursor asset discovery."""
    out = ensure_inside_repo(dst_dir / "README.md")
    written = [out]
    if dry_run:
        print(f"  Would write: {out.relative_to(REPO_ROOT)}")
        return written

    lines = [
        f"# Generated {harness_label} AI Assets",
        "",
        "> Generated from `plugins/`. Do not edit this directory by hand.",
        "",
        "Read `AGENT.md` first. It is the canonical router for hard stops, task routing, docs, rules, and skills.",
        "",
        "## Skills",
        "",
    ]

    skill_lines: list[str] = []
    for plugin in plugins:
        for skill in skill_dirs(plugin):
            generated_name = skill_name(plugin, skill.name)
            source = (plugin.skills_dir / skill.name / "SKILL.md").relative_to(REPO_ROOT).as_posix()
            skill_lines.append(f"- `{generated_name}`: generated from `{source}`")

    lines.extend(skill_lines or ["- No public skills found yet."])
    lines.extend(
        [
            "",
            "## Context",
            "",
            "This harness does not auto-load Cursor MDC context providers.",
            "Use `AGENT.md` and `docs/SSOT-map.md` to find the canonical docs for the task.",
        ]
    )

    context_lines: list[str] = []
    for plugin in plugins:
        for context in context_provider_files(plugin):
            source = context.relative_to(REPO_ROOT).as_posix()
            context_lines.append(f"- Context hint source: `{source}`")

    if context_lines:
        lines.extend(["", "Available context hint sources:"])
        lines.extend(context_lines)

    lines.extend(
        [
            "",
            "## Regeneration",
            "",
            f"Run `python tools/generate_adapters.py --harness {harness_key}` to refresh this directory.",
            "Run `python tools/generate_adapters.py --all --dry-run` to preview every harness output.",
            "",
        ]
    )

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return written


class Adapter:
    key: str

    def generate(self, plugins: list[Plugin], *, dry_run: bool = False) -> list[Path]:
        raise NotImplementedError
