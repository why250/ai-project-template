# ============================================================
# ai-project-template — developer tooling
# ============================================================
# Usage:
#   make setup     — interactive harness setup (run once per harness)
#   make generate  — generate harness-native assets from plugins/
#   make validate  — check generated harness files are not drifted
#   make validate-generated — check committed generated assets match plugins/
#   make validate-template — check template structure and docs wiring
#   make help      — list available targets

.PHONY: setup generate generate-all validate validate-generated validate-template help

## setup: Interactive harness setup — run once when adopting a new AI harness
setup:
	python tools/setup_harness.py

## generate: Generate Cursor assets from plugins/ (default local adapter)
generate:
	python tools/generate_adapters.py --harness cursor

## generate-all: Generate all harness-native assets from plugins/
generate-all:
	python tools/generate_adapters.py --all

## validate: Check generated harness entry-point files against AGENT.md for drift
validate:
	python tools/validate_harness.py

## validate-generated: Check committed Cursor assets match plugins/
validate-generated:
	python tools/validate_generated.py

## validate-template: Check template structure, links, and adapter contracts
validate-template:
	python tools/validate_template.py

## help: List all available targets
help:
	@grep -E '^## [a-zA-Z_-]+:' $(MAKEFILE_LIST) | \
		sed 's/^## //' | \
		awk -F: '{ printf "  %-12s %s\n", $$1, $$2 }'
