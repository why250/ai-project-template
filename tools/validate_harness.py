"""
Validates that generated harness entry-point files are correct one-line redirects to AGENT.md.

Each generated file should contain exactly: AGENT.md

Usage:
    python tools/validate_harness.py         # check all known generated files
    python tools/validate_harness.py --strict  # exit 1 on any drift or missing file
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
ADAPTERS_MANIFEST = Path(__file__).parent / "harness_adapters.json"

def load_manifest() -> dict:
    """Load the shared cross-harness adapter manifest."""
    return json.loads(ADAPTERS_MANIFEST.read_text(encoding="utf-8"))


def generated_harness_files() -> dict[str, str]:
    """Return generated entry-point paths keyed to their adapter key."""
    manifest = load_manifest()
    return {
        adapter["entry_point"]: adapter["key"]
        for adapter in manifest["adapters"]
        if adapter.get("generated")
    }


EXPECTED_CONTENT = load_manifest()["generated_entry_content"]


def validate(strict: bool = False) -> bool:
    all_ok = True

    for rel_path, harness_key in generated_harness_files().items():
        full_path = REPO_ROOT / rel_path
        if not full_path.exists():
            print(f"  SKIP  {rel_path} (not generated - run `make setup` to create)")
            if strict:
                all_ok = False
            continue

        content = full_path.read_text(encoding="utf-8")
        if content == EXPECTED_CONTENT:
            print(f"  OK    {rel_path}")
        else:
            print(f"  DRIFT {rel_path}")
            print(f"         Expected: {EXPECTED_CONTENT!r}")
            print(f"         Found:    {content!r}")
            print(f"         Fix: run `python tools/setup_harness.py --harness {harness_key}`")
            all_ok = False

    return all_ok


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate harness entry-point files are correct AGENT.md redirects."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any file is missing or drifted",
    )
    args = parser.parse_args()

    print("Validating harness entry-point files...")
    ok = validate(strict=args.strict)

    if ok:
        print("\nAll checks passed.")
        sys.exit(0)
    else:
        print("\nOne or more checks failed.")
        sys.exit(1 if args.strict else 0)


if __name__ == "__main__":
    main()
