# ============================================================
# ai-project-template — developer tooling
# ============================================================
# Usage:
#   make setup     — interactive harness setup (run once per harness)
#   make validate  — check generated harness files are not drifted
#   make help      — list available targets

.PHONY: setup validate help

## setup: Interactive harness setup — run once when adopting a new AI harness
setup:
	python tools/setup_harness.py

## validate: Check generated harness entry-point files against AGENT.md for drift
validate:
	python tools/validate_harness.py

## help: List all available targets
help:
	@grep -E '^## [a-zA-Z_-]+:' $(MAKEFILE_LIST) | \
		sed 's/^## //' | \
		awk -F: '{ printf "  %-12s %s\n", $$1, $$2 }'
