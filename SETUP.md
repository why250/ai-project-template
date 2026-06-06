# How to use this template

## Day 1 checklist

Copy the template and fill in the blanks in order:

### 1. Architecture (start here)

Edit `docs/architecture/overview.md`:
- [ ] What does this system do? (2-4 sentences)
- [ ] Tech stack table
- [ ] System structure diagram or description
- [ ] Key external dependencies

### 2. AGENT.md routing table

Edit the routing table in `AGENT.md`:
- [ ] Add any project-specific task types
- [ ] Adjust which docs map to which tasks
- [ ] Remove rows that don't apply to your project

### 3. Rules

Edit `.cursor/rules/always.mdc`:
- [ ] Add project-specific hard stops
- [ ] Add project-specific non-negotiable constraints
- [ ] Keep it under 50 lines

Edit the other rule files to match your stack:
- [ ] `code-style.mdc` — adjust naming and patterns
- [ ] `testing.mdc` — adjust coverage requirements and test runner commands
- [ ] `database.mdc` — adjust if not using a relational DB
- [ ] `security.mdc` — adjust to your auth system

### 4. README.md

- [ ] Replace `[Project Name]`
- [ ] Add actual quick start commands
- [ ] Add links to docs that exist

### 5. Delete the placeholders

- [ ] Delete `docs/*/README.md` guidance files once you've created real content
- [ ] Keep `docs/architecture/overview.md` and `docs/architecture/decisions.md` — fill them in

---

## As the project grows

### When to create a new `docs/` file

- A new business domain is introduced
- The API surface expands significantly
- A new service or integration is added

### When to create a new rule

After a task where you think: *"the AI should always do X"* or *"the AI should never do Y"*

```
.cursor/rules/[topic].mdc
```

Add a row to the rules table in `AGENT.md`.

### When to create a new skill

After completing a repeatable workflow for the first time:

```bash
cp -r .cursor/skills/_template.md .cursor/skills/[domain]-[action]/README.md
```

Fill in the steps while they're fresh. Add it to the skills table in `AGENT.md`.

### When to add an ADR entry

Any time you make a decision that future-you will wonder about:
- "Why did we pick X over Y?"
- "Why is this structured this way?"
- "Why is this constraint here?"

Append to `docs/architecture/decisions.md`.

---

## The one rule that matters most

> Every piece of information lives in **exactly one place**.
> Everything else links to it.

If you find yourself copying text from one file to another, stop — link instead.
