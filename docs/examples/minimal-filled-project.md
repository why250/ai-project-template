# Minimal Filled Project Example

> Example-only fixture for adopting this template. Do not copy these facts into a real project unless they are true there.

This page shows what a small filled project can look like after the placeholders are replaced.
It is intentionally concrete enough to test the router, SSOT map, rules, and skills without becoming a second source of truth for this template.

## Example Project

Project name: Inventory API

Purpose: Provide a small HTTP API for tracking products, stock levels, and warehouse movements.

Primary stack:

| Layer | Example value |
|-------|---------------|
| Backend | FastAPI |
| Database | PostgreSQL |
| Tests | pytest |
| Deployment | Docker Compose for local development |

## Router Behavior

The agent starts at `AGENT.md`, then loads only the docs needed for the task.

| User task | Router choice | Canonical docs |
|-----------|---------------|----------------|
| Add product search endpoint | API change | `docs/api/products.md`, then relevant source files |
| Add stock movement table | Database change | `docs/database/schema.md`, `docs/database/migrations.md` |
| Explain warehouse reservation rules | Business domain | `docs/business/inventory.md` |
| Fix local Docker startup | Deployment | `docs/deployment/local.md` |

The generated harness entry points still contain only `AGENT.md`.
They should not duplicate this table.

## Docs Facts

Facts about the example system would live in exactly one canonical file:

| Fact type | Canonical owner |
|-----------|-----------------|
| Product endpoint request and response shapes | `docs/api/products.md` |
| Stock reservation state machine | `docs/business/inventory.md` |
| Product and stock movement tables | `docs/database/schema.md` |
| Migration safety convention | `docs/database/migrations.md` |
| Local environment variables | `docs/deployment/local.md` |

If a Cursor context provider summarizes any of these facts, it links back to the owning doc instead of copying the full content.

## Rules Constraints

Behavior constraints belong in `plugins/project-template/rules/cursor/` before adapter generation.

Example refinements for this project:

- `security.mdc`: never log product supplier tokens or warehouse integration credentials.
- `database.mdc`: migrations touching stock counts must include rollback notes and data integrity checks.
- `testing.mdc`: API changes need request validation and error-shape tests.

Hard stops that must apply in every harness stay in `AGENT.md`.

## Skills SOP

Repeatable workflows belong in `plugins/project-template/skills/`.

Example candidate skills:

| Skill | Trigger |
|-------|---------|
| `api-endpoint-change` | Add or modify an HTTP endpoint |
| `safe-stock-migration` | Change inventory tables or backfill stock data |
| `local-docker-troubleshooting` | Local environment startup fails |

Each skill keeps the essential steps in `SKILL.md` and moves long examples to `references/details.md`.

## Cross-Tool Adaptation

After plugin edits, run:

```bash
python tools/generate_adapters.py --all --dry-run
```

Expected shape:

| Harness | Entry point | Native generated assets |
|---------|-------------|-------------------------|
| Cursor | `.cursor/` | Rules, context providers, skills |
| Codex | `AGENTS.md` | `.codex/skills/` plus generated README index |
| Claude Code | `CLAUDE.md` | `.claude/skills/` plus generated README index |
| Gemini | `GEMINI.md` | `skills/` plus generated README index |
| OpenCode | `.opencode/AGENTS.md` | `.opencode/skills/` plus generated README index |

The invariant is: entry point -> `AGENT.md` -> task routing -> canonical docs and generated assets.

## Adoption Checklist

1. Replace project placeholders in `README.md` and `docs/architecture/overview.md`.
2. Register every real docs file in `docs/SSOT-map.md`.
3. Add only project facts to `docs/`.
4. Add only reusable procedures to `plugins/project-template/skills/`.
5. Add only behavior constraints to `plugins/project-template/rules/cursor/`.
6. Run `python tools/check_template.py`.
