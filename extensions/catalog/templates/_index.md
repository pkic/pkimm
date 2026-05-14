---
date: "2026-05-13T7:00:00Z"
title: Extension documentation template
draft: true

---

# Extension documentation template

This document is a template for the documentation page of an extension in the [Extension catalog](../). Every extension's `_index.md` should follow the structure below so readers can quickly find the same information across extensions.

## How to use this template

- Copy this file to a new folder under `extensions/catalog/<extension-id>/_index.md`.
- Place the corresponding `<extension-id>-extension.yaml` file in the same folder.
- Replace parts written in *italic* with the extension's actual content.
- Remove any sections that don't apply, but keep their headings unchanged when they do apply.
- Remove the `draft: true` front-matter flag once the page is ready to publish.
- Add the extension to the table in [`extensions/catalog/_index.md`](../).

---

# *[Extension name]*

*[One short paragraph stating the extension's purpose: what aspect of PKI maturity it covers and why it exists. Two to four sentences.]*

*[A second short paragraph providing additional context — for example, the threat model it addresses, the regulatory drivers, or the use case where the extension is most useful.]*

## Status

*[State the maturity of the extension. Use one of the badges from the catalog (`Under development`, `Release candidate`, `Stable`, `Deprecated`).]*

- **Complete** — *[Which modules / categories have full Level 1–5 criteria, assessor guidance, and overlay weights defined.]*
- **Outline** — *[Which modules / categories are identified but not yet fully developed.]*
- **YAML version** — *[The version field in the YAML, with a short note about what triggers a version bump.]*

*[If there are unresolved design decisions or open questions that affect interpretation, list them here. Each item should be one or two sentences pointing at the trade-off.]*

## Scope

*[Who is the extension for? List the primary audiences (e.g., CA operators, PKI architects, auditors) and explicitly call out audiences that are NOT covered or are covered shallowly.]*

## What the extension covers

*[Section per PKI MM module that the extension addresses. For each category provide a 1–3 paragraph summary of what PQC-specific (or extension-specific) maturity looks like. The YAML is the canonical source of the Level 1–5 criteria — the prose here orients the reader.]*

### *[PKI MM Module name]*

#### *[Category N — name]*

*[Short summary of how this extension's criteria differ from or extend the baseline PKI MM category. Keep this to a few sentences — the level criteria live in the YAML.]*

*[Optional: highlight critical transitions, key probes, or evidence examples that don't fit cleanly into level criteria.]*

## YAML definition

The machine-readable definition of this extension is in [`<extension-id>-extension.yaml`](./<extension-id>-extension.yaml). Tools consume the YAML directly; this page is the human-readable companion.

## References

*[Bulleted list of standards, regulations, and other sources the extension draws on. Prefer authoritative primary sources (NIST, ETSI, ISO, regulatory texts).]*

- *[Reference 1]*
- *[Reference 2]*

## Attribution

*[Optional. Credit the authors and contributors. Useful if the extension was prepared by an external party or working group sub-team.]*
