---
date: 2026-05-20T00:00:00Z
title: Release notes
weight: 6
---

# Release notes

Release notes for each version of the PKI Maturity Model. Each release page documents what was added, changed, and removed since the previous version, plus the migration notes needed by downstream consumers (assessment tools, integrators, content maintainers).

## Versioning policy

PKI Maturity Model uses [semantic versioning](https://semver.org/):

- **Major** (`X.0.0`): breaking changes — categories removed or restructured, identifiers renamed, schema shape changed.
- **Minor** (`X.Y.0`): additive changes — new categories or requirements, new optional schema fields. Existing identifiers remain valid.
- **Patch** (`X.Y.Z`): editorial fixes — typo corrections, clarifications, reference URL updates. No structural change.

The references catalog (`data/pkimm-references.yaml`) has its own independent version field; reference-metadata updates can ship without a model release.

## Summary

| Version | Date | Headline change |
|---------|------|-----------------|
| [**2.0.0**](2.0.0/) | <span class="badge text-bg-warning">Under development</span> | Adds the Cryptography category; renames maturity level 2 to "Foundational"; introduces stable identifiers and a shared references catalog. |
| [1.0.0](1.0.0/) | 2023-08-10 | Initial release. Four modules, 15 assessment categories, five-level maturity rubric. |
