# Database Documentation

> SSOT for schema, migration conventions, and data model decisions.

---

## Files to create here

```
database/
  schema.md          ← current table/collection definitions
  migrations.md      ← migration conventions and history notes
  indexes.md         ← index strategy and rationale
  seeds.md           ← seed data for dev/staging
```

---

## schema.md template

```markdown
# Schema

## [TableName]

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | uuid | no | gen_random_uuid() | PK |
| created_at | timestamptz | no | now() | |
| ... | | | | |

**Indexes:** ...
**Foreign keys:** ...
**Business notes:** (e.g., "soft delete via deleted_at, never hard delete")
```

---

## Migration conventions

- All schema changes go through migrations (never manual ALTER in prod)
- Migration files named: `YYYYMMDDHHMMSS_description.sql`
- Every migration must be reversible (include a `down` migration)
- Test migrations on a copy of production data before deploying
