---
date: 2026-05-20T00:00:00Z
title: 2.0.0
weight: 10
---

# PKI Maturity Model 2.0.0 — Summary of changes

This document summarises the changes from PKI Maturity Model 1.0.0 to 2.0.0. It is intended for assessors, consultants, and PKI program owners who use the model to evaluate or improve PKI programs.

## Change types

This summary uses the following change-type vocabulary:

| Change type | Definition |
|---|---|
| <span class="badge text-bg-success">Evolving</span> | Changes ensuring the model is up to date with emerging threats and technologies. Examples include new or removed categories or requirements. |
| <span class="badge text-bg-warning">Clarification or Guidance</span> | Updates to wording, explanation, definition, or label to increase understanding without changing the intent of an existing assessment. |
| <span class="badge text-bg-info">Structure or format</span> | Reorganisation of content — including category and requirement renaming, identifier changes, or reorganisation — to align content. |

## Summary of general changes

- Maturity level 2 was renamed from "Basic" to "Foundational" to better convey the level's intent. The level number and the description of what it means to achieve that level are unchanged. <span class="badge text-bg-warning">Clarification or Guidance</span>
- Stable identifiers were introduced for categories and requirements. Previously, categories and requirements were referenced by position-based numbers (e.g., `G.1`, `G.1.1`); they are now referenced by stable string identifiers (e.g., `G.strategy-and-vision`, `G.strategy-and-vision.sponsor-support`). These identifiers remain valid across future minor releases. <span class="badge text-bg-info">Structure or format</span>
- A shared references catalog was introduced for the standards, regulations, and publications cited from the model. Reference titles and links can now be maintained centrally between major releases. <span class="badge text-bg-info">Structure or format</span>
- Category page URLs and headings no longer carry numeric position prefixes — bookmarks or report links should be updated. <span class="badge text-bg-info">Structure or format</span>

## Summary of changes to modules

| Module | Change | Change type |
|---|---|---|
| Governance | Added the Cryptography category (see Categories below). | <span class="badge text-bg-success">Evolving</span> |

(Management, Operations, and Resources have no module-level changes in 2.0.0.)

## Summary of changes to categories

| Category | Change | Change type |
|---|---|---|
| Cryptography (Governance, new) | New category that centralises governance of cryptographic algorithms and parameters, protocols and versions, cryptographic asset visibility, and cryptographic lifecycle, deprecation, and agility. Previously these concerns were spread across Key management and Certificate management as cipher-suite requirements, leading to overlap and ambiguous terminology. The new category consolidates them into a single coherent place. | <span class="badge text-bg-success">Evolving</span> |
| Certificate management (Management) | Removed the "Certificate cipher suites are documented" requirement. Cipher suites are a protocol-level concept primarily associated with TLS and similar protocols; certificates themselves do not define or negotiate them. Including this requirement in Certificate management mixed cryptographic governance with certificate lifecycle management. Cryptographic algorithm and protocol governance is now handled centrally in the new Cryptography category, so Certificate management focuses on certificate lifecycle topics. | <span class="badge text-bg-success">Evolving</span> |
| Key management (Management) | Removed the "Cryptographic cipher suites and protocols are documented and maintained" requirement. Algorithm and protocol approval are governance concerns, not key lifecycle concerns. The requirement duplicated cryptographic decision-making that is now covered in the new Cryptography category, so Key management focuses exclusively on key lifecycle topics. | <span class="badge text-bg-success">Evolving</span> |

(Other categories carried over from 1.0.0 have no content changes in 2.0.0. The category-page format updates noted under "General changes" apply uniformly.)

## Summary of changes to requirements

| Category | Requirement | Change | Change type |
|---|---|---|---|
| Cryptography | Cryptographic terminology and scope are defined and documented | Added. Assessors evaluate whether the organisation has defined and documented the cryptographic terminology and scope applicable to its PKI. | <span class="badge text-bg-success">Evolving</span> |
| Cryptography | Cryptographic algorithms and parameters are documented and approved | Added. Assessors evaluate whether the organisation has documented and formally approved the cryptographic algorithms and parameters in use across its PKI. Where a regulatory regime or trust scheme mandates a cryptographic catalog, approvals are expected to be traceable to that catalog. | <span class="badge text-bg-success">Evolving</span> |
| Cryptography | Cryptographic protocols and versions are documented and approved | Added. Assessors evaluate whether the organisation has documented and approved the cryptographic protocols and protocol versions in use. | <span class="badge text-bg-success">Evolving</span> |
| Cryptography | Visibility into cryptographic usage is established and maintained | Added. Assessors evaluate whether the organisation has established and maintains visibility into its actual cryptographic usage. | <span class="badge text-bg-success">Evolving</span> |
| Cryptography | Cryptographic lifecycle and deprecation rules are defined | Added. Assessors evaluate whether the organisation has defined cryptographic lifecycle and deprecation rules. | <span class="badge text-bg-success">Evolving</span> |
| Cryptography | Cryptographic agility is defined and governed | Added. Assessors evaluate whether the organisation has defined and governs cryptographic agility — the ability to replace cryptographic algorithms or parameters in a controlled way in response to threats or regulatory requirements. | <span class="badge text-bg-success">Evolving</span> |
| Certificate management | Certificate cipher suites are documented | Removed. Cipher suites are a protocol-level concept; their governance is now handled in the new Cryptography category. | <span class="badge text-bg-success">Evolving</span> |
| Key management | Cryptographic cipher suites and protocols are documented and maintained | Removed. Algorithm and protocol approval are governance concerns; they are now covered in the new Cryptography category. | <span class="badge text-bg-success">Evolving</span> |

## Summary of changes to extensions

2.0.0 introduces the extension **framework and schema**: a defined mechanism for optional overlays that add emphasis, additional requirements, or alternative weighting for a specific risk profile or industry context. Extensions do not change the core model; they supplement it for organisations that need a more targeted view. The framework and its JSON Schema live in this repository (`extensions/extension.schema-1.0.0.json`).

The extension **catalog** — the actual published extensions — is maintained separately in the [`pkimm-extensions`](https://pkic.org/wg/pkimm/extensions/) repository and published at that site. This repository no longer ships or tracks individual extension content; consult `pkimm-extensions` for available extensions, their status, and version compatibility with the core model.

## Summary of changes to integrations and tools

- **Integrations moved.** The Eramba CSV converter scripts (previously under `integrations/eramba/`) have moved to the separate [`pkimm-integrations`](https://pkic.org/wg/pkimm/integrations/) repository. The in-repo `integrations/eramba/*.csv` paths are retired.
- **Excel assessment tools retired.** The Excel-based assessment tools (`tools/PKI_Maturity_Assessment_Tool_*.xlsx`, `tools/PKI_Maturity_Self_Assessment_Tool_*.xlsx`) are retired from this repository as of 2.0.0 and are superseded by the web self-assessment. They remain available at the `1.0.0`-tagged raw URLs and in the 1.0.0 website section; the `/main/`-pinned raw `tools/*.xlsx` URLs will no longer resolve.

## Notes for assessors and consultants

- **Category URL changes.** Bookmarks pointing to old `01-…`, `02-…` style category URLs should be updated to the new identifier-only form (for example, `categories/strategy-and-vision/`).
- **Reports referencing "level 2 — Basic".** Existing assessment reports completed under 1.0.0 are not invalidated. If you regenerate or reissue a report, update references from "level 2 — Basic" to "level 2 — Foundational" to align with 2.0.0 terminology.
- **Existing assessments.** Categories carried over from 1.0.0 have no content changes other than the cipher-suite removals from Certificate management and Key management. Scores for those categories may need a small re-evaluation if the removed requirement materially influenced the maturity level; for most assessments the impact is minor and limited to a single requirement.
- **Cryptography category.** Organisations that completed a 1.0.0 assessment should add the Cryptography category to their next assessment cycle.
- **Extensions.** Published extensions are maintained in the `pkimm-extensions` repository, not this one; they are optional and apply only when explicitly enabled. Consult that repository for available extensions and their model-version compatibility.
- **Excel tools retired.** If you have bookmarked or automated against the `/main/`-pinned raw `tools/*.xlsx` URLs, switch to the web self-assessment or the `1.0.0`-tagged URLs, as those links will no longer resolve.
- **Questions and discussions.** Engage with the working group via the [PKI Maturity Model community discussion](https://github.com/orgs/pkic/discussions/categories/pki-maturity-model-pkimm).
