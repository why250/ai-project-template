# Skills (SOPs)

> This directory contains Standard Operating Procedures accumulated from real project work.
> Skills are created AFTER a task is completed — not speculatively.
> Each skill describes a repeatable workflow that the AI (or a developer) can follow.

---

## When to create a skill

A skill is worth creating when:
- You've completed a workflow that will recur (e.g., integrating a third-party service)
- A multi-step process has non-obvious ordering or gotchas
- You want the next session to pick up exactly where this one left off

A skill is NOT needed for:
- One-off tasks that won't repeat
- Simple operations documented in the library's own docs
- Things covered by a rule (rules = constraints, skills = procedures)

---

## Naming convention

```
skills/
  [domain]-[action]/
    README.md       ← the skill itself
    [supporting files if needed]
```

Examples:
```
skills/stripe-payment-integration/
skills/auth-jwt-refresh/
skills/release-process/
skills/pr-review/
skills/feature-flag-rollout/
```

---

## Skill file template

Copy `_template.md` and rename the directory when creating a new skill.
