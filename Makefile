# ============================================================
# ai-project-template — developer tooling
# ============================================================
# Usage:
#   make setup     — interactive harness setup (run once per harness)
#   make generate  — generate harness-native assets from plugins/
#   make validate  — check generated harness files are not drifted
#   make validate-generated — check committed generated assets match plugins/
#   make validate-template — check template structure and docs wiring
#   make check     — run the full template validation suite
#   make help      — list available targets

.PHONY: setup generate generate-all validate validate-generated validate-template check help

## setup: Interactive harness setup — run once when adopting a new AI harness
setup:
	python tools/setup_harness.py

## generate: Generate Cursor assets from plugins/ (default local adapter)
generate:
	python tools/generate_adapters.py --harness cursor

## generate-all: Generate all harness-native assets from plugins/
generate-all:
	python tools/generate_adapters.py --all

## validate: Strictly check committed harness entry-point files against AGENT.md
validate:
	python tools/validate_harness.py --strict

## validate-generated: Check committed Cursor assets match plugins/
validate-generated:
	python tools/validate_generated.py

## validate-template: Check template structure, links, and adapter contracts
validate-template:
	python tools/validate_template.py

## check: Run the full template validation suite
check:
	python tools/check_template.py

## help: List all available targets
help:
	@grep -E '^## [a-zA-Z_-]+:' $(MAKEFILE_LIST) | \
		sed 's/^## //' | \
		awk -F: '{ printf "  %-12s %s\n", $$1, $$2 }'
