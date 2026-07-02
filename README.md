# AI Project Template

> A project template for routing AI coding agents through one canonical router, SSOT docs, behavior rules, repeatable skills, and cross-tool adapters.

---

## For humans

- **What is this?** → [docs/architecture/overview.md](docs/architecture/overview.md)
- **How to run it?** → [docs/deployment/local.md](docs/deployment/local.md)
- **API reference?** → [docs/api/](docs/api/)
- **Database schema?** → [docs/database/](docs/database/)
- **Why did we build it this way?** → [docs/architecture/decisions.md](docs/architecture/decisions.md)
- **What does a filled project look like?** → [docs/examples/minimal-filled-project.md](docs/examples/minimal-filled-project.md)

## For AI agents

See [AGENT.md](AGENT.md).

---

## Quick start

```bash
python tools/setup_harness.py --list
python tools/setup_harness.py --describe
python tools/setup_harness.py --all --dry-run
python tools/setup_harness.py --harness codex --commit
python tools/generate_adapters.py --harness cursor
python tools/generate_adapters.py --all --dry-run
python tools/validate_generated.py
python tools/validate_harness.py --strict
python tools/validate_template.py
python tools/check_template.py
# Optional when make is available:
make check
```

---

> This README intentionally contains no architecture, business logic, or API details.
> Everything lives in `docs/` as a single source of truth.
