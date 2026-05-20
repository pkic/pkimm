# PKI Maturity Model

This repository holds the PKI Maturity Model maintained by the PKI Consortium PKIMM working group. The content is published at https://pkic.org/pkimm, where readers can browse the model, the assessment process, and the published release notes.

## For users

- Browse the latest model: https://pkic.org/wg/pkimm/
- Release notes for each version: [`release-notes/`](../release-notes/)
- Charter of the working group: https://pkic.org/wg/pkimm/charter/

## For contributors

The authoritative content lives in two places:

- `data/pkimm-model-<version>.yaml` — the machine-readable model (modules, categories, requirements, levels). This is the source of truth for downstream tooling.
- `data/pkimm-references.yaml` — the shared catalog of standards, regulations, and publications cited from the model. Independently versioned so reference-metadata updates do not require a model release.

The per-category markdown under `categories/` and the references summary at `model/references/_index.md` are **generated** from the YAML files. Edit the YAML, run the generator, commit both.

### Local setup

The authoring scripts need Python 3.12+:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements-dev.txt
```

### Authoring workflow

1. Edit `data/pkimm-model-<version>.yaml` (model content) or `data/pkimm-references.yaml` (reference catalog).
2. Regenerate per-category markdown and the references summary:
   ```sh
   python scripts/generate_category_docs.py \
     --model data/pkimm-model-2.0.0.yaml \
     --references data/pkimm-references.yaml \
     --categories-dir categories \
     --references-md model/references/_index.md
   ```
3. Update narrative pages (`model/`, root `_index.md`) by hand if their content cites model facts.
4. Run the consistency validator until it passes:
   ```sh
   python scripts/check_model_docs_consistency.py --repo-root .
   ```
5. Commit. The same checks run on every PR via [`.github/workflows/check-consistency.yml`](workflows/check-consistency.yml).

### Repository layout

- `data/` — versioned model YAML files and their JSON schemas, plus the references catalog and its schema.
- `categories/` — generated per-category markdown (one folder per category, named by stable kebab-case id).
- `model/` — narrative pages: vocabulary, modules, categories overview, references summary.
- `release-notes/` — per-version release notes. Each version subdirectory uses the template at `release-notes/templates/_index.md`.
- `assessment/` — assessment process pages (scoping, assessment, evaluation, reporting, implementation).
- `extensions/` — extension framework schema and the catalog of published extensions.
- `tools/` — Excel-based assessment tools and the web self-assessment configuration.
- `integrations/` — converters that produce artifacts for downstream tools (e.g., Eramba CSV packages).
- `scripts/` — authoring scripts (generator, validator) and their tests.

### Conventions

- **Stable identifiers**: category and requirement `id` fields are kebab-case strings (`strategy-and-vision`, `sponsor-support`), not positional numbers. Ordering is expressed via the YAML array position and Hugo's `weight:` front-matter field.
- **Maturity-level vocabulary**: `Initial`, `Foundational`, `Advanced`, `Managed`, `Optimized`. The numeric level (1–5) lives in the sibling `number` field; display layers compose `"${number} - ${name}"` where the prefixed form is needed.
- **References**: cite catalog entries by id in each requirement's `references:` array. Add new entries to `data/pkimm-references.yaml`; do not inline references in model YAML.
- **Markdown anchors**: requirement headings carry an explicit `<a id="<id>"></a>` tag so links work consistently across GitHub, Hugo, and other renderers.

### Adding a reference

Edit `data/pkimm-references.yaml`, append a new entry with a short kebab-case `id` (convention: `<authority>-<doc-id>`, e.g., `iso-27001`, `nist-fips-140-3`). Bump the catalog's `version:` field — patch for editorial fixes, minor for new entries, major for renames or removals (very rare). Cite the new id from any requirement's `references:` array.

### Adding a category or requirement

Edit `data/pkimm-model-<version>.yaml` under the relevant module. Use a short kebab-case `id` distinct from existing ones. Run the generator to produce the markdown. The validator will flag any inconsistencies in the surrounding documentation.

### Adding an extension

Each extension is a single YAML file under `extensions/catalog/<id>/<id>-extension.yaml` validating against `extensions/extension.schema-1.0.0.json`. Declare which model versions the extension targets in its `compatibility` array. Extension-specific references go in an inline top-level `references:` block on the extension; common references resolve against the global catalog.

## License & IPR

We welcome contributions from members and non-members alike. All contributions are subject to the PKI Consortium [Intellectual Property Rights Agreement](https://pkic.org/ipr/).
