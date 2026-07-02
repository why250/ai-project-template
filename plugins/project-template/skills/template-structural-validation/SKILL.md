---
name: template-structural-validation
description: Validate this AI project template after changes to AGENT.md, docs, plugins, adapters, harness templates, or generated Cursor assets. Use when editing project governance files or cross-harness adapter behavior.
---

# Template Structural Validation

> Created: 2026-06-17
> Origin: Drift found between routing docs, Cursor rules, skill naming, and harness adapter behavior.

## Core guidance

- Run `python tools/check_template.py` for the full cross-platform validation suite.
- Run `make check` only as a convenience wrapper when Make is available.
- Run `python tools/validate_template.py` to check links, rule registration, adapter manifest wiring, harness templates, SSOT paths, and skill template structure.
- Run `python tools/validate_generated.py` after editing `plugins/` or `.cursor/` to ensure committed Cursor assets still match the source plugin.
- Run `python tools/validate_harness.py --strict` after editing harness entry templates or committed generated entry files.
- Run `python tools/generate_adapters.py --harness cursor` when `plugins/project-template/` changes.
- Use `python tools/generate_adapters.py --all --dry-run` to preview Codex, Claude Code, Gemini, and OpenCode skill outputs and README indexes without creating local generated directories.

## Key constraints

- `plugins/` is the source of truth for portable AI assets.
- `.cursor/rules`, `.cursor/context`, and `.cursor/skills` are generated Cursor assets.
- `docs/` remains the source of truth for project facts.
- `AGENT.md` remains the short router and cross-harness constraint entry point.

## Verification

- [ ] `python tools/check_template.py` passes, or each command below has been run individually.
- [ ] `python tools/validate_template.py` passes.
- [ ] `python tools/validate_generated.py` passes.
- [ ] `python tools/validate_harness.py --strict` passes.
- [ ] `python tools/generate_adapters.py --all --dry-run` shows the expected harness-native outputs.

## Where to find more

- Adapter contract: `docs/architecture/harness-adapters.md`
- Source plugin: `plugins/project-template/plugin.json`
- Deep detail: `references/details.md`
