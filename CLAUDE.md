# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Identity

This repository is a **Claude Code Skill** — the `SKILL.md` file at the root is the registration entry point. When installed, Claude Code gains the ability to generate test cases from requirement documents.

## Project Overview

AI-powered test case generation from requirement documents. Uses business tree modeling to produce comprehensive test cases, exported as formatted Excel files.

The engine is **prompt-driven, not code-driven**: the CLI (`src/cli.py`) prints instructions for an AI agent. The actual test case generation is performed by an AI agent following the prompt files in `prompts/`. The `SKILL.md` file registers this as a Claude Code skill.

## Environment

- **Python >= 3.12** required
- Dependencies: `typer>=0.12,<1.0`, `openpyxl>=3.1,<4.0`
- Install: `pip install -e .`

## Commands

```bash
# Install (editable)
pip install -e .

# CLI entry point
test-case-engine --help

# Initialize a project directory
test-case-engine init --project-name <name>

# Show project status
test-case-engine status

# Start business modeling from a requirement document
test-case-engine model --document <path>

# Review requirements
test-case-engine review [--adjustment <text>]

# Build test outline
test-case-engine outline

# Generate test cases
test-case-engine generate [--module <name>]

# Export to Excel
test-case-engine export [--output <path>]

# Show built-in prompt content for a topic
test-case-engine explain [topic]
```

`quick-start.sh` provides a one-command demo: installs deps, runs `init`, and shows status.

## Architecture

```
SKILL.md                  # Skill registration entry point — loaded by Claude Code
src/
├── cli.py                # Typer CLI — thin orchestration layer (7 commands)
├── session_service.py    # State file management (.test-case/*.json)
└── excel_exporter.py     # openpyxl-based Excel export
prompts/
├── constitution.md       # Core principles (the "constitution") — read first, highest priority
├── extraction-guide.md   # Full Phase 1-4 execution guide
└── commands/             # Per-phase AI agent instructions
    ├── init.md
    ├── model.md
    ├── review.md
    ├── outline.md
    ├── generate.md
    └── export.md
examples/
├── online-shop-prd.md    # Sample requirement document (online shop)
├── validation-result.md  # Validation findings and improvement notes
└── output/               # Sample outputs from each phase
    ├── business_tree.json
    ├── outline.json
    ├── test_cases.json
    └── test_cases.xlsx
```

**Pipeline**: `init` → `model` → `review` (loop with user) → `outline` → `generate` → `export`

Each phase produces a state file in `.test-case/`:
- `constitution.md` — project constitution
- `business_tree.json` — entry points, flows, branch points, L1-L4 scenarios
- `review_result.json` — 5-dimension review output (status: pending/approved)
- `outline.json` — test points organized by module
- `test_cases.json` — final test cases with coverage report

Phases are sequential and each depends on the previous phase's output.

## Key Design Decisions

- **The CLI never implements business logic.** It loads state files, prints instructions, and delegates to the AI agent. The `prompts/` directory is the real engine.
- **Business tree is the core asset.** Built in Phase 1 (model), reused in all subsequent phases for review, outline, and case generation.
- **L1-L4 scenario coverage**: L1 (main paths, 100%), L2 (branch paths, 100%), L3 (exception templates, 100%), L4 (imagination scenarios — 10 enhancement techniques, breadth inquiry until convergence: 2 consecutive rounds with no new scenarios).
- **Constitution priority**: The constitution (`prompts/constitution.md`) has the highest priority — all execution must follow it. The core principle is "explicit guidance" (never assume AI will think of something, explicitly ask for it).
- **SessionService** manages all intermediate state as JSON files under `.test-case/`. Each phase loads the previous phase's output and saves its own.
- **Excel export** uses openpyxl with frozen headers, P1 red highlighting, auto-filters, and 10 standard columns.
- **Functional vs performance testing separation**: The constitution mandates these be kept in separate test suites. L4 scenarios that are performance-oriented (concurrency, large data volume, file size) are tagged with `test_type: "performance"` and not mixed into functional test cases.