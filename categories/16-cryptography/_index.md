---
date: 2026-02-09T7:00:00Z
title: 16 - Cryptography
weight: 16

---

# 16 - Cryptography

## Overview

The organization defines how it governs the selection, approval, documentation, visibility, and evolution of cryptographic algorithms, cryptographic parameters, and cryptographic protocols used within its PKI and related systems.

The cryptographic policy and strategic direction should be established. It ensures that cryptographic choices are deliberate, consistent, risk-based, and adaptable over time.

Organization should separate cryptographic decision-making from cryptographic execution.
- It defines what cryptography is allowed and why
- It does not define how keys or certificates are technically managed
- It provides a single authoritative source for cryptographic rules

Cryptographic governance may be implemented using policies, standards, profiles, baselines, or other organizational mechanisms, provided the governance outcomes defined in this category are achieved.

This category does not address the operational lifecycle of cryptographic keys or certificates, which are covered in the Key Management and Certificate Management categories.

## Category maturity levels description

| Maturity level    | Description                                                                                                                                                                                                                                                                               |
|:------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1 - Initial**   | Cryptographic algorithms and protocols are chosen locally by teams or products with little or no centralized guidance. Documentation is informal or inconsistent, and cryptographic decisions are largely reactive.                                                                       |
| **2 - Basic**     | Basic cryptographic rules exist, such as preferred algorithms or minimum key sizes. However, documentation is incomplete, visibility into cryptographic usage is limited, and cryptographic decisions are not consistently enforced.                                                      |
| **3 - Advanced**  | The organization documents approved cryptographic algorithms, parameters, and protocols. Cryptographic terminology is standardized, cryptographic profiles are defined, and visibility into cryptographic usage exists for critical systems.                                              |                               
| **4 - Managed**   | Cryptographic governance is comprehensive and consistently applied. The organization actively manages cryptographic lifecycles, monitors cryptographic usage, and plans cryptographic transitions based on risk, standards evolution, and business impact.                                | 
| **5 - Optimized** | Cryptographic governance is proactive and adaptive. The organization continuously assesses cryptographic risks, practices cryptographic agility, and integrates cryptographic transition planning (including emerging technologies) into enterprise risk and change management processes. |

## Requirements

|                                                                         # | Requirement                                                         | Weight |
|--------------------------------------------------------------------------:|---------------------------------------------------------------------|-------:|
|      [1](#cryptographic-terminology-and-scope-are-defined-and-documented) | Cryptographic terminology and scope are defined and documented      |      3 |
| [2](#cryptographic-algorithms-and-parameters-are-documented-and-approved) | Cryptographic algorithms and parameters are documented and approved |      5 |
|    [3](#cryptographic-protocols-and-versions-are-documented-and-approved) | Cryptographic protocols and versions are documented and approved    |      3 |
|   [4](#visibility-into-cryptographic-usage-is-established-and-maintained) | Visibility into cryptographic usage is established and maintained   |      5 |
|           [5](#cryptographic-lifecycle-and-deprecation-rules-are-defined) | Cryptographic lifecycle and deprecation rules are defined           |      4 |
|                                [6](#cryptographic-agility-is-established) | Cryptographic agility is established                                |      5 |

## Details

### Cryptographic terminology and scope are defined and documented

#### Guidance

Inconsistent or ambiguous terminology leads to misinterpretation of requirements, incorrect implementation, and duplication across teams. Clear terminology ensures that cryptographic policy, key management, certificate management, and change processes are aligned and understood in the same way.

The organization should define and document consistent terminology for cryptographic concepts, including:
- Cryptographic algorithms
- Cryptographic keys
- Digital certificates
- Cryptographic protocols
- Cryptographic parameters and security levels
- Cryptographic profiles
Terminology should be used consistently across policies, standards, and procedures.

#### Assessment

- Documented cryptographic definitions exist.
- Terminology is consistently used across PKI documentation.
- Stakeholders demonstrate a shared understanding of terms.

#### References

- [NIST SP 800-57 Part 1 Rev. 5 - Recommendation for Key Management](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
- [PCI Cryptography Guidance](https://docs-prv.pcisecuritystandards.org/Guidance%20Document/Cryptography/PCI-Cryptography-Guidance-v1_0.pdf)
- [CycloneDX - Cryptography Registry](https://cyclonedx.org/registry/cryptography/)

### Cryptographic algorithms and parameters are documented and approved

#### Guidance

Without explicit approval rules, cryptographic algorithms are often selected based on defaults, legacy compatibility, or convenience. Documented approvals ensure consistent security levels, reduce technical debt, and enable controlled cryptographic evolution.

The organization should document:
- Approved cryptographic algorithms
- Approved cryptographic parameters (e.g., key sizes, curves)
- Restricted, deprecated, or prohibited algorithms

Each decision should include rationale and applicability.

#### Assessment

- Approved and prohibited algorithms are documented.
- Parameter requirements are clearly defined.
- Documentation is reviewed periodically.

#### References

- [NIST SP 800-131A Rev. 2 - Transitioning the Use of Cryptographic Algorithms and Key Lengths](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-131Ar2.pdf)

### Cryptographic protocols and versions are documented and approved

#### Guidance

Protocols define how cryptography is actually used in communication. Even strong algorithms can be undermined by weak or outdated protocol versions. Clear protocol governance prevents insecure defaults and uncontrolled legacy usage.

The organization should define which cryptographic protocols and protocol versions are approved, restricted, deprecated, or prohibited.

#### Assessment

- Protocol and version rules are documented.
- Deprecated or prohibited protocols are identified. 
- Exceptions are formally approved.

#### References

- [NIST SP 800-52 Rev. 2 - Guidelines for the Selection, Configuration, and Use of Transport Layer Security (TLS) Implementations](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r2.pdf)
- [OWASP Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)

### Visibility into cryptographic usage is established and maintained

#### Guidance

Cryptographic risk cannot be managed if cryptographic usage is unknown. Visibility is essential for impact analysis, deprecation planning, incident response, and cryptographic agility.

The organization should maintain visibility into where cryptography is used, including algorithms, keys, certificates, and protocols.

#### Assessment

- Cryptographic usage information exists for critical systems.
- Visibility supports risk and transition planning.
- Gaps are identified and addressed.

#### References

- [NIST Cybersecurity Framework - Identify Function](https://www.nist.gov/cyberframework/identify)
- [EUCC Guidelines on Cryptography Inventory](https://certification.enisa.europa.eu/publications/eucc-guidelines-cryptography_en)
- [CycloneDX Cryptography Bill of Materials (CBOM)](https://cyclonedx.org/capabilities/cbom/)

### Cryptographic lifecycle and deprecation rules are defined

#### Guidance

Cryptography degrades over time due to advances in computing and cryptanalysis. Explicit lifecycle rules prevent reactive, crisis-driven migrations and support predictable, risk-based transitions.

The organization should define rules for:
- Approving new cryptography
- Setting expected validity periods
- Deprecating cryptography
- Identifying replacement options

#### Assessment

- Lifecycle and deprecation rules are documented.
- Deprecation decisions follow defined criteria.
- Replacement planning is evident.

#### References

- [NIST SP 800-131A Rev. 2 - Transitioning the Use of Cryptographic Algorithms and Key Lengths](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-131Ar2.pdf)
- [NIST SP 800-57 Part 1 Rev. 5 - Recommendation for Key Management](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)

### Cryptographic agility is established

#### Guidance

Cryptographic change is inevitable. Organizations that established cryptographic agility can respond in a controlled and timely manner, reducing operational risk and business disruption.

The organization should maintain plans to respond to cryptographic change drivers such as algorithm compromise, deprecation, regulatory change, or emerging cryptographic requirements.

#### Assessment

- Cryptographic transition plans exist.
- Plans align with change management processes.
- Preparedness for cryptographic transitions can be demonstrated.

#### References

- [NIST CSWP 39 - Considerations for Achieving Cryptographic Agility: Strategies and Practices](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.39.pdf)
