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

Edit `plugins/project-template/rules/cursor/always.mdc`:
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

### 6. SSOT Registry

- [ ] Open `docs/SSOT-map.md`
- [ ] Add a row for every `docs/` file you created in steps 1-5
- [ ] Verify no domain is listed in two rows (no duplicates)
- [ ] Verify the "What does NOT live here" column is filled in for each row

### 7. Context providers

For each domain that has its own directory in your source code (`src/payments/`, `src/auth/`, etc.):
- [ ] Copy `plugins/project-template/context/_template.mdc` to `plugins/project-template/context/[domain]-context.mdc`
- [ ] Set `globs` to match the code file paths for that domain
- [ ] Write 3-5 summary bullets derived from `docs/[domain]/` — do not invent facts
- [ ] Keep the file under 40 lines

If you have no code yet, skip this step and come back once source directories exist.

### 8. Glob customization

- [ ] Open each `plugins/project-template/rules/cursor/*.mdc` and review the `globs` array
- [ ] Remove glob patterns that don't match your stack (e.g., remove `*.py` if Python-only)
- [ ] Add any project-specific paths that should trigger a rule
- [ ] Misconfigured globs silently load irrelevant rules — trim them now

---

## As the project grows

### When to create a new `docs/` file

- A new business domain is introduced
- The API surface expands significantly
- A new service or integration is added

### When to create a new rule

After a task where you think: *"the AI should always do X"* or *"the AI should never do Y"*

```
plugins/project-template/rules/cursor/[topic].mdc
```

Rules go in `rules/` — constraints on AI behavior. Add a row to the rules table in `AGENT.md`.
If the content is domain facts (not behavior constraints), create a context provider in `context/` instead.

### When to create a new context provider

When a domain has its own source directory and you find yourself repeatedly loading the same `docs/` file as orientation:

```
plugins/project-template/context/[domain]-context.mdc
```

Context providers go in `context/` — they summarize `docs/` facts and auto-attach via globs.
Keep them under 40 lines. They link to `docs/`, they do not duplicate it.

### When to write to LEARNINGS.md

After any task where you noticed something non-obvious — a constraint you almost forgot, a workflow with unexpected steps, a decision you made that future-you will wonder about.

Write the raw observation immediately, while context is fresh. Then distill it into a rule, skill, or ADR in the same session. See the entry template in `LEARNINGS.md`.

### When to update SSOT-map.md

Every time a new `docs/` file is created. Update the registry in the same commit — the registry must never lag behind the files it tracks.

### When to create a new skill

After completing a repeatable workflow for the first time:

```bash
cp -r plugins/project-template/skills/_template plugins/project-template/skills/[domain]-[action]
```

Fill in `plugins/project-template/skills/[domain]-[action]/SKILL.md` while the steps are fresh.
Add the skill to the skills table in `AGENT.md` only if it should be discoverable from routing.

### When to validate the template

After editing `AGENT.md`, `docs/`, `plugins/`, `.cursor/rules/`, `.cursor/context/`, `.cursor/skills/`, or `tools/harness_templates/`:

```bash
python tools/validate_template.py
python tools/validate_generated.py
python tools/validate_harness.py
```

If you add or change a supported AI harness, update `tools/harness_adapters.json` first.
Then update `docs/architecture/harness-adapters.md` so humans can see the same adapter contract.

Useful adapter commands:

```bash
python tools/setup_harness.py --describe
python tools/setup_harness.py --all --dry-run
python tools/setup_harness.py --all --commit
python tools/generate_adapters.py --harness cursor
python tools/generate_adapters.py --all --dry-run
```

### When to update plugins/

Use `plugins/` as the source of truth for portable AI assets:

- Cursor rules live in `plugins/[name]/rules/cursor/`
- Cursor context providers live in `plugins/[name]/context/`
- Portable skills live in `plugins/[name]/skills/[skill]/SKILL.md`

After editing `plugins/`, regenerate the affected harness output:

```bash
python tools/generate_adapters.py --harness cursor
```

Generate all native skill outputs only when you want local Codex, Claude Code, Gemini, or OpenCode discovery files:

```bash
python tools/generate_adapters.py --all
```

Use strict harness validation in CI after generated entry points are expected to exist:

```bash
python tools/validate_harness.py --strict
```

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
