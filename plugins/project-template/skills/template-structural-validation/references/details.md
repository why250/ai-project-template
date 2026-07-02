# Template Structural Validation Details

## What Each Check Covers

| Command | Purpose |
|---------|---------|
| `python tools/check_template.py` | Runs the full cross-platform template validation suite and previews every harness adapter output. |
| `make check` | Convenience wrapper for `python tools/check_template.py` when Make is available. |
| `python tools/validate_template.py` | Checks structural wiring: markdown links, rule registration, adapter manifest, harness templates, SSOT concrete paths, and skill template contract. |
| `python tools/validate_generated.py` | Checks committed Cursor output against `plugins/project-template/`. |
| `python tools/validate_harness.py --strict` | Checks committed generated harness entry-point files such as `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and `.opencode/AGENTS.md`. |
| `python tools/generate_adapters.py --all --dry-run` | Shows what Codex, Claude Code, Cursor, Gemini, and OpenCode adapters would emit, including non-Cursor README indexes. |

## Expected Source Boundaries

- Add or edit project facts in `docs/`.
- Add or edit portable AI rules, context providers, and skills in `plugins/`.
- Regenerate `.cursor/` from `plugins/`.
- Do not put project facts into generated harness output.
- Do not hand-edit generated Cursor assets unless the same change is made in `plugins/` first.

## Common Fixes

| Symptom | Fix |
|---------|-----|
| `validate_generated.py` reports a differing `.cursor` file | Run `python tools/generate_adapters.py --harness cursor`, or move the intended edit back to `plugins/project-template/`. |
| `validate_template.py` reports a missing SSOT path | Create the canonical file or correct `docs/SSOT-map.md`. |
| `validate_harness.py --strict` reports missing entry files | Run `python tools/setup_harness.py --all --commit` or generate only the required harnesses. |
