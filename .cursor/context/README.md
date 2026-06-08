# Context Providers

Context providers are MDC files that auto-deliver domain knowledge to your AI editor.
They are **different from rules** in `.cursor/rules/`.

| Directory | Contains | Purpose |
|-----------|----------|---------|
| `.cursor/rules/` | Behavior constraints | Tell the AI what to do or not do |
| `.cursor/context/` | Knowledge summaries | Orient the AI on domain facts when editing relevant files |

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

`[domain]-context.mdc` — for example:
- `payments-context.mdc` → globs: `["src/payments/**"]`
- `auth-context.mdc` → globs: `["src/auth/**", "**/middleware/**"]`
- `notifications-context.mdc` → globs: `["src/notifications/**"]`

Keep each file under **40 lines**. If it's longer, the summary is too detailed — trim and link to docs/.

---

## Claude Code users

Claude Code does not use glob auto-attach. Instead, `CLAUDE.md` references the context directory.
When working in a domain, load the relevant context MDC manually per the Layer 2 routing in `CLAUDE.md`.
