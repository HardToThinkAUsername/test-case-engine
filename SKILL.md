---
name: test-case-engine
description: "AI-powered test case generation from requirement documents. Use when user wants to generate test cases from requirements, PRD, or business descriptions."
---

# Test Case Engine

Generate comprehensive test cases from requirement documents using business tree modeling.

## Core Principles

- **Perfect**: Zero omissions, zero redundancy, zero false positives
- **Explicit guidance**: Don't assume AI will think of it - explicitly ask
- **Breadth first**: Cover all scenarios before deep analysis
- **Business tree as core asset**: Reuse across all phases

## Flow

```
Phase 1: Business Modeling (model)
Phase 2: Requirement Review (review) - loop with user
Phase 3: Test Outline (outline)
Phase 4: Case Generation (generate)
Export: Excel (export)
```

## When to Use

- User uploads requirement document → start with init
- User wants to generate test cases → follow the full flow
- User wants to review requirements → use review command

## Skill Files

All prompts are in `prompts/` directory:
- `constitution.md` - Core principles (read first)
- `extraction-guide.md` - Detailed execution steps
- `commands/*.md` - Individual command instructions

## Commands

```bash
# Initialize project
init --project-name <name>

# Business modeling
model --document <path>

# Requirement review
review [--adjustment "..."]

# Build test outline
outline

# Generate test cases
generate [--module <name>]

# Export to Excel
export [--output <path>]
```

## 示例

See `examples/online-shop-prd.md` for a sample requirement document.
See `examples/output/` for sample outputs (business_tree.json, outline.json, test_cases.json, test_cases.xlsx).

## Execution Rules

1. Always read constitution.md first
2. Follow extraction-guide.md steps exactly
3. Use explicit prompts, never assume AI will think of something
4. Validate at each step before proceeding
5. Output structured JSON for machine processing

## Output Format

Each phase produces structured output:
- Phase 1: `business_tree.json`
- Phase 2: `review_result.json`
- Phase 3: `outline.json`
- Phase 4: `test_cases.json` + Excel export

## Example

See `examples/online-shop-prd.md` for a sample requirement document.
See `examples/output/` for sample outputs.