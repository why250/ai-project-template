# AGENT.md — Context Router

> This file is a **router**, not a knowledge base.
> Do NOT add business logic, architecture details, or API specs here.
> Every piece of knowledge lives exactly once, in `docs/`.

---

## Step 1 — Read First (Always)

Before any task, read:
- `docs/architecture/overview.md` — what this system is
- `.cursor/rules/always.mdc` — non-negotiable constraints

---

## Step 2 — Identify Task Domain

| Task type | Load these docs |
|-----------|----------------|
| New feature | `docs/architecture/overview.md` + relevant `docs/business/` |
| API change | `docs/api/` |
| Database change | `docs/database/` |
| Bug fix | `docs/architecture/overview.md` + file context |
| Deployment | `docs/deployment/` |
| Refactor | `docs/architecture/` + `docs/architecture/decisions.md` |
| Unknown | Ask the user before loading anything |

**Rule: Load only what the task requires. Do not load the full `docs/` tree.**

---

## Step 3 — Apply Rules

All rules live in `.cursor/rules/`.

| Rule file | When it applies |
|-----------|----------------|
| `always.mdc` | Every task, no exceptions |
| `code-style.mdc` | Any code generation or modification |
| `testing.mdc` | Any new function, module, or API endpoint |
| `database.mdc` | Any schema or migration change |
| `security.mdc` | Auth, permissions, data handling |

---

## Step 4 — Use Skills (SOPs)

Before implementing a known workflow, check `.cursor/skills/` first.

If a matching skill exists → follow it exactly.
If no skill exists → implement, then consider creating one after.

---

## Step 5 — After Task Completion

Ask yourself (or ask the user):

1. Did we encounter a constraint that should always be enforced?
   → Add to `.cursor/rules/`

2. Did we complete a repeatable workflow?
   → Add to `.cursor/skills/`

3. Did facts about the system change?
   → Update the relevant file in `docs/` (SSOT only)

4. Did we make a non-obvious architectural decision?
   → Append to `docs/architecture/decisions.md`

---

## Directory Map

```
AGENT.md                        ← you are here (router only)
README.md                       → human-facing intro, links to docs/

docs/
  architecture/
    overview.md                 ← what the system is and how it's structured
    decisions.md                ← ADR log: why we made key choices
  business/                     ← domain logic, business rules, user flows
  api/                          ← API contracts, endpoints, request/response shapes
  database/                     ← schema, ERD, migration conventions
  deployment/                   ← environments, CI/CD, runbooks

.cursor/
  rules/
    always.mdc                  ← loaded every session, keep it short
    code-style.mdc
    testing.mdc
    database.mdc
    security.mdc
  skills/                       ← SOPs accumulated over project lifetime
    _template.md                ← copy this when creating a new skill

.gitignore
```

---

## SSOT Principle

Every fact exists in **exactly one place**.

- README.md → links to `docs/`, does not duplicate it
- AGENT.md → links to `docs/`, does not duplicate it
- If two files say the same thing, one of them is wrong

---

## What NOT to put in this file

- ❌ Tech stack details → `docs/architecture/overview.md`
- ❌ Business rules → `docs/business/`
- ❌ Coding style preferences → `.cursor/rules/code-style.mdc`
- ❌ How to deploy → `docs/deployment/`
- ❌ Lessons learned → `.cursor/rules/` or `.cursor/skills/`
