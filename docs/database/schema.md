# Database Schema

> SSOT for the current database schema.
> Replace placeholders with real tables, collections, fields, and relationships when the project chooses a data store.

---

## Current state

No application schema has been defined yet.

---

## Table template

```markdown
## [table_name]

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | uuid | no | gen_random_uuid() | Primary key |

**Indexes:** [list indexes]

**Foreign keys:** [list relationships]

**Business notes:** [link to docs/business/ when relevant]
```
