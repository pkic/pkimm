# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Content repository for the **PKI Maturity Model (PKIMM)**, maintained by the PKI Consortium PKIMM working group. The content is rendered at https://pkic.org/pkimm by an external Hugo-based site — this repo holds the source markdown, the canonical model data, and assessment tools. There is **no build system, no test suite, and no application code** here. Treat changes as documentation/data edits, not software changes.

## Repository layout

- `_index.md` — top-level overview page (Hugo front matter).
- `model/` — definitions of maturity levels, modules, and the list of categories.
- `categories/<slug>/_index.md` — one file per category (16 categories: five in Governance including the Cryptography category, four each in Management and Operations, three in Resources). Folder name matches the YAML `id` (kebab-case, no numeric prefix). Ordering is controlled by `weight:` in the front matter.
- `categories/templates/_index.md` — the canonical template for new category descriptions. Anything in `categories/` must follow its structure (Overview → Maturity levels table → Requirements table → Details with Guidance/Assessment/References per requirement).
- `assessment/` — assessment process pages (scoping, assessment, evaluation, reporting, implementation, action plans).
- `data/pkimm-model-2.0.0.yaml` — **machine-readable source of truth** for the 2.0.0 model: modules → categories → levels + requirements (with weights, guidance, assessment, references as catalog IDs). Validated by `data/pkimm-model.schema-2.0.0.json`. Downstream integrations consume this file. The version suffix tracks the model version (see the `version` field inside the file).
- `data/pkimm-model-1.0.0.yaml` — archived 1.0.0 model; validated by `data/pkimm-model.schema-1.0.0.json`.
- `data/pkimm-model.schema-2.0.0.json` — JSON Schema for the 2.0.0 YAML shape. Category and requirement `id` fields are kebab-case strings; `requirements[].references` is an array of catalog IDs.
- `data/pkimm-model.schema-1.0.0.json` — JSON Schema for the 1.0.0 YAML shape (retroactively renamed from `pkimm-model.schema.json`).
- `data/pkimm-references.yaml` — **independently-versioned references catalog**. Per-requirement `references` fields in the 2.0.0 model contain arrays of IDs from this catalog. Edit here to update reference metadata without touching the model YAML.
- `data/pkimm-references.schema-1.0.0.json` — JSON Schema for the references catalog.
- `extensions/extension.schema-1.0.0.json` — JSON Schema for PKIMM extension files.
- `extensions/catalog/pqc/pqc-extension.yaml` — PQC (Post-Quantum Cryptography) extension version 0.2.0, compatible with PKIMM 2.0.0.
- `scripts/` — authoring and validation scripts (see "Authoring workflow" below).
- `tools/` — published Excel assessment tools (`PKI_Maturity_Assessment_Tool_*.xlsx`, `PKI_Maturity_Self_Assessment_Tool_*.xlsx`).
- `integrations/eramba/` — per-schema-version converters that produce Eramba-importable CSV packages.
  - `convert-yaml-data-to-csv-package-1.0.0.py` — reads `data/pkimm-model-1.0.0.yaml` (schema 1.0.0) and writes `pkimm-1.0.0.csv`.
  - `convert-yaml-data-to-csv-package-2.0.0.py` — reads `data/pkimm-model-2.0.0.yaml` (schema 2.0.0) and `data/pkimm-references.yaml`; writes `pkimm-2.0.0.csv`. Future schema versions get their own script alongside.
- `release-notes/` — per-version release notes (`release-notes/1.0.0/`, `release-notes/2.0.0/`) and a template at `release-notes/templates/`. See the release notes for consumer-facing changes and migration guidance.
- `faq/`, `.github/README.md` — supplementary content; the GitHub-rendered README lives in `.github/README.md`, not the repo root.

## Authoring conventions

- All markdown files use Hugo-style YAML front matter (`date`, `title`, `weight`, optional `draft`, `sideMenu`, `tags`, `summary`, hero fields on `_index.md`). Keep `weight` consistent with intended navigation order (category folders no longer carry a numeric prefix; order is determined by `weight:` alone).
- Category files mirror `categories/templates/_index.md` exactly — the table columns, anchor-link pattern in the Requirements overview (`[id](#requirement-slug)`), and the per-requirement Guidance/Assessment/References subsections are load-bearing for both readers and downstream tooling.
- Mark in-progress category drafts with `draft: true` in the front matter; remove it when the category is ready to publish.
- The maturity-level vocabulary (2.0.0) is: `1 - Initial`, `2 - Foundational`, `3 - Advanced`, `4 - Managed`, `5 - Optimized`. Note: 1.0.0 used "Basic" for level 2; "Foundational" is the 2.0.0 name. Don't introduce new level names.
- The category maturity formula is the weighted average of requirement ratings: `Σ(rᵢ·wᵢ) / Σ(wᵢ)`. Requirement weights are non-negative integers; preserve them when editing.
- Category and requirement identifiers are stable kebab-case strings (e.g., `strategy-and-vision`, `sponsor-support`). Do not rename them after release — downstream integrations depend on them.

## Authoring workflow (YAML-first)

The markdown category pages and `data/pkimm-model-2.0.0.yaml` describe the same model in two forms. YAML is the source of truth; markdown is generated from it.

1. **Edit YAML**: make your change in `data/pkimm-model-2.0.0.yaml` (or `data/pkimm-references.yaml` for reference-metadata changes).
2. **Regenerate markdown**: run `python scripts/generate_category_docs.py` to regenerate all category pages under `categories/` from the updated YAML.
3. **Update narrative docs**: manually update `model/` pages, `_index.md` mindmap, and `release-notes/` notes if the change is consumer-facing.
4. **Validate**: run `python scripts/check_model_docs_consistency.py --repo-root .` — must exit `0 error(s), 0 warning(s)` before committing.
5. **Tag**: when releasing, bump `version` in `data/pkimm-model-2.0.0.yaml`, copy the file to `data/pkimm-model-<new>.yaml`, add a schema file for the new shape, and author release notes under `release-notes/<new>/`.

CI runs the validator on every PR and push to main (`.github/workflows/check-consistency.yml`).

**Key scripts in `scripts/`:**
- `generate_category_docs.py` — regenerates `categories/` markdown from YAML.
- `check_model_docs_consistency.py` — validates YAML ↔ markdown parity, vocabulary, counts, references, and schema consistency. Run this before every commit.

## Contribution constraints

Contributions are governed by the PKI Consortium IPR Agreement (https://pkic.org/ipr/) and the PKIMM working group charter (https://pkic.org/wg/pkimm/charter/). Substantive model changes are working-group decisions — don't redesign categories, levels, modules, or weights unilaterally; editorial fixes, typos, and clarifications are fine.
