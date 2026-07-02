"""
Validate structural contracts for this AI project template.

This complements validate_harness.py:
- validate_harness.py checks committed generated harness entry-point files.
- validate_template.py checks the template source files and documentation wiring.

Usage:
    python tools/validate_template.py
"""

from __future__ import annotations

import re
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
ADAPTERS_MANIFEST = REPO_ROOT / "tools" / "harness_adapters.json"
EXPECTED_HARNESS_REDIRECT = "AGENT.md\n"


def strip_fenced_code(markdown: str) -> str:
    """Remove fenced code blocks so examples do not get treated as real links."""
    return re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)


def iter_knowledge_files() -> list[Path]:
    patterns = ["*.md", "docs/**/*.md", ".cursor/**/*.md", ".cursor/**/*.mdc"]
    files: set[Path] = set()
    for pattern in patterns:
        files.update(REPO_ROOT.glob(pattern))
    return sorted(files)


def load_adapter_manifest() -> dict:
    """Load the shared adapter manifest used by setup and harness validation."""
    return json.loads(ADAPTERS_MANIFEST.read_text(encoding="utf-8"))


def is_external_or_placeholder(target: str) -> bool:
    target = target.strip()
    return (
        not target
        or target.startswith("#")
        or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) is not None
        or "[" in target
        or "]" in target
    )


def check_markdown_links() -> list[str]:
    errors: list[str] = []
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

    for path in iter_knowledge_files():
        text = strip_fenced_code(path.read_text(encoding="utf-8"))
        for match in link_re.finditer(text):
            raw_target = match.group(1).strip()
            target = raw_target.split("#", 1)[0].strip()
            if is_external_or_placeholder(target):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                rel_path = path.relative_to(REPO_ROOT)
                errors.append(f"{rel_path}: broken local link -> {raw_target}")

    return errors


def check_rule_registration() -> list[str]:
    errors: list[str] = []
    agent = (REPO_ROOT / "AGENT.md").read_text(encoding="utf-8")

    for rule_path in sorted((REPO_ROOT / ".cursor" / "rules").glob("*.mdc")):
        name = rule_path.name
        if f"`{name}`" not in agent:
            errors.append(f"AGENT.md does not register .cursor/rules/{name}")

    return errors


def check_harness_templates() -> list[str]:
    errors: list[str] = []
    templates_dir = REPO_ROOT / "tools" / "harness_templates"

    for template_path in sorted(templates_dir.glob("*.tmpl")):
        content = template_path.read_text(encoding="utf-8")
        if content != EXPECTED_HARNESS_REDIRECT:
            rel_path = template_path.relative_to(REPO_ROOT)
            errors.append(
                f"{rel_path}: expected exactly {EXPECTED_HARNESS_REDIRECT!r}, found {content!r}"
            )

    return errors


def check_adapter_manifest() -> list[str]:
    errors: list[str] = []
    manifest = load_adapter_manifest()
    adapters = manifest.get("adapters", [])
    docs_text = (REPO_ROOT / "docs" / "architecture" / "harness-adapters.md").read_text(
        encoding="utf-8"
    )

    if manifest.get("canonical_router") != "AGENT.md":
        errors.append("tools/harness_adapters.json canonical_router must be AGENT.md")

    if manifest.get("generated_entry_content") != EXPECTED_HARNESS_REDIRECT:
        errors.append(
            "tools/harness_adapters.json generated_entry_content must be exactly 'AGENT.md\\n'"
        )

    keys = [adapter.get("key") for adapter in adapters]
    if len(keys) != len(set(keys)):
        errors.append("tools/harness_adapters.json contains duplicate adapter keys")

    entry_points = [adapter.get("entry_point") for adapter in adapters]
    if len(entry_points) != len(set(entry_points)):
        errors.append("tools/harness_adapters.json contains duplicate entry points")

    for adapter in adapters:
        key = adapter.get("key")
        entry_point = adapter.get("entry_point")
        template = adapter.get("template")
        generated = adapter.get("generated")

        if not key or not entry_point:
            errors.append("Every adapter needs key and entry_point")
            continue

        if f"`{entry_point}`" not in docs_text:
            errors.append(f"docs/architecture/harness-adapters.md missing entry point `{entry_point}`")

        if generated:
            if not template:
                errors.append(f"Generated adapter {key} is missing a template")
                continue
            template_path = REPO_ROOT / "tools" / "harness_templates" / template
            if not template_path.exists():
                errors.append(f"Generated adapter {key} template does not exist: {template}")
            elif template_path.read_text(encoding="utf-8") != EXPECTED_HARNESS_REDIRECT:
                errors.append(f"Generated adapter {key} template must redirect exactly to AGENT.md")
        else:
            if template is not None:
                errors.append(f"Non-generated adapter {key} should not declare a template")
            if not (REPO_ROOT / entry_point).exists():
                errors.append(f"Non-generated adapter {key} entry point does not exist: {entry_point}")

    return errors


def extract_ssot_paths() -> list[str]:
    ssot = (REPO_ROOT / "docs" / "SSOT-map.md").read_text(encoding="utf-8")
    paths: list[str] = []

    for line in ssot.splitlines():
        if not line.startswith("|") or "`" not in line:
            continue
        for value in re.findall(r"`([^`]+)`", line):
            paths.append(value)

    return paths


def is_generated_or_pattern(path_text: str) -> bool:
    return (
        " " in path_text
        or "[" in path_text
        or "]" in path_text
        or "*" in path_text
        or "," in path_text
    )


def check_ssot_concrete_paths() -> list[str]:
    errors: list[str] = []

    for path_text in extract_ssot_paths():
        if is_generated_or_pattern(path_text):
            continue
        resolved = REPO_ROOT / path_text
        if not resolved.exists():
            errors.append(f"docs/SSOT-map.md references missing path: {path_text}")

    return errors


def check_skill_template_contract() -> list[str]:
    errors: list[str] = []
    template_dir = REPO_ROOT / ".cursor" / "skills" / "_template"

    expected = [
        template_dir / "SKILL.md",
        template_dir / "references" / "details.md",
    ]
    for path in expected:
        if not path.exists():
            errors.append(f"Missing skill template file: {path.relative_to(REPO_ROOT)}")

    readme = (REPO_ROOT / ".cursor" / "skills" / "README.md").read_text(encoding="utf-8")
    if "README.md       \u2190 the skill itself" in readme:
        errors.append(".cursor/skills/README.md still documents README.md as the skill file")

    return errors


def run_checks() -> list[str]:
    checks = [
        ("Markdown links", check_markdown_links),
        ("Rule registration", check_rule_registration),
        ("Adapter manifest", check_adapter_manifest),
        ("Harness templates", check_harness_templates),
        ("SSOT concrete paths", check_ssot_concrete_paths),
        ("Skill template contract", check_skill_template_contract),
    ]

    all_errors: list[str] = []
    for label, check in checks:
        errors = check()
        if errors:
            print(f"FAIL {label}")
            for error in errors:
                print(f"  - {error}")
            all_errors.extend(errors)
        else:
            print(f"OK   {label}")

    return all_errors


def main() -> None:
    print("Validating template structure...")
    errors = run_checks()

    if errors:
        print(f"\n{len(errors)} check(s) failed.")
        sys.exit(1)

    print("\nAll template checks passed.")


if __name__ == "__main__":
    main()
