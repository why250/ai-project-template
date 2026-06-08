# LEARNINGS.md — Memory Distillation Buffer

> This is a **staging buffer**, not a permanent log.
> Write raw task observations here immediately (while context is fresh), then distill each entry into a rule, skill, ADR, or doc update.
> Process each entry within the same session or the next one.

---

## Entry template

Copy this block for each new learning:

```
### [YYYY-MM-DD] [One-line task summary]

**Raw observation:** What happened that was surprising, non-obvious, or worth remembering.

**Trigger signal:** What situation would cause this to matter again.

**Distillation candidate:**
- [ ] Rule → `.cursor/rules/[topic].mdc`
- [ ] Skill → `.cursor/skills/[domain]-[action]/`
- [ ] ADR → `docs/architecture/decisions.md`
- [ ] Doc update → `docs/[canonical-file].md` (see `docs/SSOT-map.md`)
- [ ] Discard — not repeatable enough

**Status:** [ ] Pending distillation  [ ] Distilled (link: _____)  [ ] Discarded
```

---

## Needs Review

<!-- Pending entries accumulate here. If an entry has been here for more than one session, act on it now. -->

*(No entries yet — add your first learning after completing a task.)*

---

## Distilled

<!-- Processed entries move here with a link to where the knowledge now lives. -->

---

## Examples (delete once you add real entries)

### [2024-01-15] Stripe webhook validation

**Raw observation:** Skipped signature validation on a test webhook handler. Worked fine locally, but staging failed because the test runner sends real Stripe payloads that require `Stripe-Signature` header.

**Trigger signal:** Whenever adding a new webhook endpoint, even for testing.

**Distillation candidate:**
- [x] Rule → `.cursor/rules/security.mdc`

**Status:** [x] Distilled (link: `.cursor/rules/security.mdc` — "Validate webhooks with signatures")

---

### [2024-01-20] Migration rollback on large table

**Raw observation:** Running a migration that added a NOT NULL column on a 2M-row table caused a 45-second lock. Should have used a two-step migration: add nullable first, backfill, then add NOT NULL constraint.

**Trigger signal:** Any migration adding a NOT NULL column to a table with >100k rows.

**Distillation candidate:**
- [x] Skill → `.cursor/skills/safe-migration-large-table/`

**Status:** [x] Distilled (link: `.cursor/skills/safe-migration-large-table/README.md`)
