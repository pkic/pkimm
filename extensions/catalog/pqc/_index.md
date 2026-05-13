---
date: "2026-05-13T7:00:00Z"
title: PQC Readiness Extension
weight: 1
---

# PQC Readiness Extension

The Post-Quantum Cryptography (PQC) Readiness Extension adds quantum-safe transition criteria to the PKI Maturity Model. It introduces an extension-specific maturity signal alongside the baseline PKI MM categories, plus weight overlays that emphasize requirements most relevant to PQC migration.

The quantum threat fundamentally changes what PKI maturity means. An organization achieving Level 5 on every current PKI MM requirement may still face material cryptographic risk if its foundations are quantum-vulnerable. The Dutch government's "harvest-now, decrypt-later" framing makes this a **present-day** risk for long-lived confidentiality, not a future concern.

## Status

This extension is **under development**.

- **Complete** — Governance module (categories 1 – 4): full Level 1–5 criteria, assessor guidance, evidence examples, and overlay weights are defined.
- **Outline** — Management, Operations, and Resources modules: PQC-critical considerations identified, but Level 1–5 criteria are not yet developed.
- **YAML version** — `0.1.0`. The extension version will move to `1.0.0` when all modules reach full Level 1–5 development and the working group endorses the content.

### Open question

The placement of overlay weights is **not yet settled** between two candidate designs:

- **Governance-centric overlays** (current YAML): per-requirement multipliers applied to Governance categories 1 – 4, emphasizing the requirements where PQC introduces fundamentally new evidence or review cadence.
- **Capability-centric overlays** (Kennedy's proposal, section 7): multipliers applied to crypto-agility (Change Management & Agility) and PQC training (Knowledge & Training), elevating the operational capabilities most underweighted for quantum readiness.

The current YAML follows the Governance-centric design (because that is what the self-assessment tool currently exercises). Resolving this is a working-group decision and will land in a future revision.

## Scope

The extension targets the following audiences:

- **Certification Authority operators (CA / TSP)** — primary audience; most existing content reflects CA/TSP archetypes.
- **PKI architects and operators in enterprises** — assessing internal PKI quantum-readiness.
- **Auditors and consultants** — using the extension as part of broader PKI maturity engagements.

Persona coverage for **certificate-consuming organizations**, **software vendors**, and **AI-system-layer cryptographic governance** is identified as a known gap and tracked for a later revision.

## What the extension covers

The four Governance categories receive full PQC-specific Level 1–5 criteria; the remaining modules are identified at an outline level only.

### Governance — Module G

#### Strategy and vision (G:1)

Strategic direction for PQC transition: executive sponsorship of the quantum threat, the Mosca inequality applied to data lifetimes, organizational persona per the Dutch Migration Handbook, board-level visibility, and budget for PQC activities.

**Key transitions:**
- Level 2 → 3 — "Awareness to Action": formal strategy incorporation, executive sponsorship extended, working group established.
- Level 4 → 5 — "Execution to Leadership": competitive positioning, ecosystem contribution, crypto-agility as ongoing capability.

#### Policies and documentation (G:2)

Policy framework for PQC: CP/CPS updates to incorporate NIST FIPS 203/204/205, deprecation schedules aligned with SP 800-131A Rev 3, hybrid-vs-pure PQC strategy, key management policy adjustments (larger keys, HSM support, stateful HBS state management), CBOM adoption, and multi-jurisdiction policy alignment (BSI / ANSSI hybrid versus CNSA 2.0 pure PQ).

#### Compliance (G:3)

Regulatory mapping and audit scope for PQC requirements: DORA ICT risk management (EU financial services from January 2025), eIDAS 2.0 cryptographic requirements, CNSA 2.0 timelines (US National Security Systems), NIS2 implementing measures, and the 18 EU Member States Joint Statement recommendations. Audit criteria evolution under WebTrust and ETSI scopes is tracked here.

#### Processes and procedures (G:4)

Operational procedures transformed for PQC: key ceremony evolution (hybrid generation, quorum, HSM activation, stateful HBS state management), crypto-agility procedures per NIST CSWP 39, quantum risk assessment with Mosca inequality, change management for phased migration, incident response for cryptographic events, and extended segregation of duties for PQC-specific roles.

### Modules M, O, R — outline only

The following PQC-critical considerations are identified for the remaining modules. Full Level 1–5 development is pending.

#### Management — Module M (PQC technical considerations)

- **Key Management (M:6)** — algorithm inventory and CBOM generation; PQC key lifecycle (larger keys, longer generation times); stateful hash-based signature state management (XMSS, LMS); hybrid key management; HSM PQC algorithm support verification.
- **Certificate Management (M:7)** — hybrid certificate issuance (composite signatures, external keys); certificate validity periods versus algorithm security lifetimes; revocation strategy for quantum-vulnerable certificates; template updates; cross-certification for hybrid PKI.
- **Infrastructure Management (M:8)** — HSM firmware upgrade roadmaps; network capacity for larger PQC keys and signatures; storage for larger certificates; performance testing.
- **Change Management and Agility (M:9)** — crypto-agility architecture enabling algorithm substitution; transition procedures; rollback for failed PQC deployments; configuration management for cryptographic parameters.

#### Operations — Module O (PQC security considerations)

- **Resilience (O:10)** — quantum threat in business continuity planning; recovery procedures for cryptographic compromise; redundancy for PQC algorithm availability.
- **Automation (O:11)** — automated cryptographic inventory discovery; automated certificate replacement for PQC migration; CI/CD integration for PQC algorithm validation.
- **Interoperability (O:12)** — PQC interoperability testing with relying parties; hybrid certificate compatibility verification; cross-vendor PQC algorithm interoperability; protocol-version negotiation.
- **Monitoring and Auditing (O:13)** — algorithm usage monitoring and reporting; quantum-vulnerable algorithm detection; CBOM drift monitoring; audit trail for algorithm transitions.

#### Resources — Module R (PQC people and sourcing considerations)

- **Sourcing (R:14)** — vendor PQC roadmap assessment in procurement; contract requirements for PQC support timelines; third-party certificate provider PQC readiness; supply-chain security for cryptographic components.
- **Knowledge and Training (R:15)** — PQC technical training for PKI operations staff; executive education on quantum risk; certification programs incorporating PQC; knowledge transfer from PQC migration projects.
- **Awareness (R:16)** — organization-wide quantum-threat awareness; developer education on PQC implications; stakeholder communication for migration activities.

## Product and service dependency

Organizational PKI maturity depends on the readiness of products and services in the dependency chain — Certificate Authority software, HSMs, IAM platforms, cloud PKI offerings, application frameworks, IoT firmware. An organization can achieve Level 5 on internal governance while being blocked from PQC deployment by a critical vendor not supporting quantum-safe algorithms until later in the decade.

The PKI Consortium's separate Post-Quantum Cryptography Maturity Model (PQCMM) assesses product / service PQC readiness. The PQC extension is designed to be used **alongside** PQCMM: the PKIMM extension scores the organization's governance and operational readiness; PQCMM scores the dependencies. Integration guidance is on the working group's roadmap.

## YAML definition

The machine-readable definition of the PQC Readiness Extension is in [`pqc-extension.yaml`](./pqc-extension.yaml). Tools consume the YAML directly; this page is the human-readable companion. The YAML is the canonical source for assessment use — the prose above is a summary.

## References

- **NIST FIPS 203 / 204 / 205** — ML-KEM, ML-DSA, SLH-DSA (August 2024)
- **NIST SP 800-131A Rev. 3** — Transitioning the Use of Cryptographic Algorithms and Key Lengths
- **NIST CSWP 39** — Considerations for Achieving Cryptographic Agility
- **NIST SP 800-208** — Stateful Hash-Based Signatures
- **CNSA 2.0** — NSA Commercial National Security Algorithm Suite 2.0 (2022)
- **Regulation (EU) 2022/2554 (DORA)** — Digital Operational Resilience Act
- **Regulation (EU) 2024/1183 (eIDAS 2.0)**
- **NIS2 Implementing Regulation 2024/2690**
- **18 EU Member States Joint Statement on Post-Quantum Cryptography**
- **Dutch PQC Migration Handbook**
- **CycloneDX Cryptography Bill of Materials (CBOM)**

## Attribution

This extension is based on the *Proposal for Post-Quantum Cryptography Readiness Extension to the PKI Maturity Model (PKIMM)* (Draft v1.3, December 2025) prepared for the PKI Consortium by Kennedy Nwup, Principal Consultant — Post-Quantum Cryptography & PKI Readiness, Afield AB.
