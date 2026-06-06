# Business Domain

> This directory contains domain knowledge: business rules, user flows, and domain terminology.
> These are facts about the business, not instructions to the AI.

---

## How to organize this directory

Create one file per major domain. Examples:

```
business/
  user.md          ← user roles, permissions, lifecycle
  payment.md       ← payment flows, states, Stripe integration facts
  order.md         ← order lifecycle, states, business rules
  notifications.md ← when and how notifications are triggered
```

---

## What belongs here

- Domain entities and their relationships
- Business rules (e.g., "an order cannot be cancelled after shipping")
- User roles and what each can do
- State machines and lifecycle diagrams
- Terminology / glossary

## What does NOT belong here

- How to implement these in code → `.cursor/skills/`
- Constraints on how AI should code → `.cursor/rules/`
- API endpoint definitions → `../api/`
- Database schema → `../database/`
