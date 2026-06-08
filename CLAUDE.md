# CLAUDE.md — Claude Code Entry Point

> Routing logic lives in `AGENT.md`. Read that file first.
> This file only documents what is different for Claude Code vs. Cursor.

---

## Start here

1. Read `AGENT.md` — it is the canonical context router for all AI agents
2. Read `docs/architecture/overview.md` — what this system is
3. Read `.cursor/rules/always.mdc` — non-negotiable constraints

---

## Claude Code differences from Cursor

| Feature | Cursor | Claude Code |
|---------|--------|-------------|
| MDC glob auto-attach | Automatic (`.cursor/rules/*.mdc`, `.cursor/context/*.mdc`) | Not supported — load files manually |
| Layer 2 context | Auto-attaches when matching file is open | Load `.cursor/context/[domain]-context.mdc` manually when domain matches |
| AGENT.md | Read automatically via MDC | Read explicitly at session start |

**When AGENT.md says "auto-attaches via globs" — in Claude Code, load that file manually.**

---

## SSOT enforcement

Before answering any factual question:
- Check `docs/SSOT-map.md` to find the canonical file for that domain
- Read the canonical file — do not invent or guess facts
