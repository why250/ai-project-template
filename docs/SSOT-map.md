# SSOT Map — Canonical File Registry

> This file is the ownership registry for the Single Source of Truth (SSOT) principle.
> It does not contain facts — it maps topics to their canonical fact files.
> Before writing any fact into any file, look up the owning file here.

---

## Domain Registry

| Domain | Canonical File | What lives here | What does NOT live here |
|--------|---------------|-----------------|-------------------------|
| System purpose & structure | `docs/architecture/overview.md` | What the system does, tech stack, data flow, key boundaries | Business rules, API details |
| Architectural decisions | `docs/architecture/decisions.md` | Why non-obvious choices were made (ADR log) | Current-state facts |
| Business domain rules | `docs/business/[domain].md` | User roles, state machines, terminology, flows | Implementation details, code constraints |
| API contracts | `docs/api/[resource].md` | Endpoint signatures, auth requirements, request/response shapes, error codes | Business logic behind endpoints |
| Database schema | `docs/database/schema.md` | Table definitions, column types, nullability, defaults, foreign keys | Migration history, index rationale |
| Migration history | `docs/database/migrations.md` | Migration conventions, timeline, rationale | Current schema state |
| Index strategy | `docs/database/indexes.md` | Index decisions and rationale | Schema definitions |
| Environments & config | `docs/deployment/environments.md` | Dev/staging/prod URLs, per-env configs, access levels | How to run locally |
| Local setup | `docs/deployment/local.md` | Prerequisites, env vars, setup commands, common issues | Production configuration |
| CI/CD pipeline | `docs/deployment/ci-cd.md` | Pipeline stages, deploy conditions, rollback triggers | Environment configs |
| Behavior constraints (AI) | `.cursor/rules/*.mdc` | Hard rules for AI agent behavior | Facts about the system |
| 4-mechanism compliance check | `.cursor/rules/self-check.mdc` | Checklist verifying SSOT, routing, MDC, memory distillation | Behavior rules (those are in other rule files) |
| Domain knowledge (AI) | `.cursor/context/[domain]-context.mdc` | Summaries and pointers for AI context loading | Authoritative facts (those live in docs/) |
| Repeatable workflows | `.cursor/skills/[domain]-[action]/README.md` | Step-by-step SOPs with gotchas | Business rules, system facts |
| Task learnings (staging) | `LEARNINGS.md` | Raw episodic captures pending distillation | Distilled rules, skills, or ADRs |
| Context routing | `AGENT.md` + `CLAUDE.md` | Task type → docs routing logic | Any domain facts |

---

## Rules

### Conflict resolution
If two files contain the same fact, the file listed in this registry is the correct one.
The other file must be updated to link here instead — it should not carry the fact itself.

### Anti-duplication checklist (for AI agents)
Before writing any fact into a file:
1. Check this registry — does a canonical owner already exist?
2. If yes → update or link to the canonical file; do not write the fact in the current file
3. If no → decide which file should own it, add it to this registry, then write the fact there

### Registry update protocol
- Add a row to this table every time a new `docs/` file is created
- Do this in the same commit as the new file — registry must never lag behind
- Never create a `docs/` file without a corresponding row here

---

## What does NOT live in this file

- The actual facts (those live in the files listed above)
- Routing logic (that lives in `AGENT.md` / `CLAUDE.md`)
- Behavior rules (those live in `.cursor/rules/`)
