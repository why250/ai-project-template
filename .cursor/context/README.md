# Context Providers

Context providers are MDC files that auto-deliver domain knowledge to Cursor.
The source of truth lives in `plugins/project-template/context/`; `.cursor/context/` is generated.
They are **different from rules** in `.cursor/rules/`.

| Directory | Contains | Purpose |
|-----------|----------|---------|
| `plugins/project-template/rules/cursor/` | Behavior constraints | Source rules generated to `.cursor/rules/` |
| `plugins/project-template/context/` | Knowledge summaries | Source context generated to `.cursor/context/` |

---

## How context providers work

Each `.mdc` file here has `globs` frontmatter. When you open a file matching those patterns in Cursor, the context MDC auto-attaches to the AI's context window.

Example: a `payment-context.mdc` with `globs: ["src/payments/**"]` will auto-load payment domain knowledge whenever you're working in the payments module.

---

## Key design rule: summarize and link, do not duplicate

A context MDC is an **index entry**, not a fact store.

- It summarizes the 3-5 most important facts about a domain
- It links to the canonical file in `docs/` for full detail
- If a fact changes, update `docs/` first, then update the summary bullet here

This keeps the Single Source of Truth (SSOT) intact. See `docs/SSOT-map.md` for ownership.

---

## When to create a context MDC

Create one when:
- A domain has a dedicated directory in your source code (e.g., `src/payments/`, `src/auth/`)
- AI agents frequently need orientation on that domain when editing code files
- The full `docs/[domain].md` is too long to always load into context

Do NOT create one just because a docs/ file exists. Only create a context MDC when there are code files that benefit from auto-attach.

---

## Naming convention

`[domain]-context.mdc` under `plugins/project-template/context/` — for example:
- `payments-context.mdc` → globs: `["src/payments/**"]`
- `auth-context.mdc` → globs: `["src/auth/**", "**/middleware/**"]`
- `notifications-context.mdc` → globs: `["src/notifications/**"]`

Keep each file under **40 lines**. If it's longer, the summary is too detailed — trim and link to docs/.
After editing context providers, run `python tools/generate_adapters.py --harness cursor`.

---

## Non-Cursor harness users

Codex, Claude Code, Gemini, and OpenCode do not use Cursor glob auto-attach.
Their generated skill directories include README indexes that point back to `AGENT.md`, `docs/SSOT-map.md`, and the plugin source.
When working in a domain outside Cursor, use `AGENT.md` to choose the canonical docs first; load context MDC files only as optional summaries.
