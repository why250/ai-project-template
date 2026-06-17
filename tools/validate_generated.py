"""
Validate committed generated assets against plugins/.

For this template, Cursor assets are committed for immediate editor support, but
their source of truth lives in plugins/. Other harness-native outputs are generated
locally on demand and are gitignored.

Usage:
    python tools/validate_generated.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SOURCE_PLUGIN = REPO_ROOT / "plugins" / "project-template"

TREE_PAIRS = [
    (SOURCE_PLUGIN / "rules" / "cursor", REPO_ROOT / ".cursor" / "rules"),
    (SOURCE_PLUGIN / "context", REPO_ROOT / ".cursor" / "context"),
    (SOURCE_PLUGIN / "skills", REPO_ROOT / ".cursor" / "skills"),
]


def rel_files(root: Path) -> set[Path]:
    if not root.exists():
        return set()
    return {path.relative_to(root) for path in root.rglob("*") if path.is_file()}


def compare_tree(source: Path, generated: Path) -> list[str]:
    errors: list[str] = []
    source_files = rel_files(source)
    generated_files = rel_files(generated)

    for rel in sorted(source_files - generated_files):
        errors.append(f"missing generated file: {generated.relative_to(REPO_ROOT) / rel}")
    for rel in sorted(generated_files - source_files):
        errors.append(f"stale generated file: {generated.relative_to(REPO_ROOT) / rel}")
    for rel in sorted(source_files & generated_files):
        src_bytes = (source / rel).read_bytes()
        out_bytes = (generated / rel).read_bytes()
        if src_bytes != out_bytes:
            errors.append(
                f"generated file differs: {generated.relative_to(REPO_ROOT) / rel} "
                f"(source: {source.relative_to(REPO_ROOT) / rel})"
            )

    return errors


def main() -> None:
    print("Validating generated Cursor assets against plugins/...")
    all_errors: list[str] = []
    for source, generated in TREE_PAIRS:
        errors = compare_tree(source, generated)
        label = f"{source.relative_to(REPO_ROOT)} -> {generated.relative_to(REPO_ROOT)}"
        if errors:
            print(f"FAIL {label}")
            for error in errors:
                print(f"  - {error}")
            all_errors.extend(errors)
        else:
            print(f"OK   {label}")

    if all_errors:
        print("\nGenerated assets are out of date. Run:")
        print("  python tools/generate_adapters.py --harness cursor")
        sys.exit(1)

    print("\nAll generated Cursor assets are current.")


if __name__ == "__main__":
    main()
