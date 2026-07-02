"""
Run the full cross-platform validation suite for this AI project template.

This is the Windows-friendly equivalent of `make check`.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

COMMANDS = [
    [sys.executable, "tools/validate_template.py"],
    [sys.executable, "tools/validate_generated.py"],
    [sys.executable, "tools/validate_harness.py", "--strict"],
    [sys.executable, "tools/generate_adapters.py", "--all", "--dry-run"],
]


def display_command(command: list[str]) -> str:
    parts = ["python" if part == sys.executable else part for part in command]
    return " ".join(parts)


def main() -> None:
    for command in COMMANDS:
        print(f"\n$ {display_command(command)}", flush=True)
        completed = subprocess.run(command, cwd=REPO_ROOT)
        if completed.returncode != 0:
            sys.exit(completed.returncode)

    print("\nAll template checks passed.")


if __name__ == "__main__":
    main()
