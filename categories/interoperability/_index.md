---
date: 2023-06-10T9:00:00Z
title: 7 - Interoperability
weight: 7

---

# 7 - Interoperability

Interoperability means the ability of two or more systems or components to exchange information and to use the information that has been exchanged.

A PKI is composed of multiple components, which are often provided by different vendors, or can be developed and maintained in-house. Interoperability keeps the PKI components working together and allows the PKI to function properly in the long term.

Adopting open standards and protocols helps to ensure interoperability between PKI components and Relying Party (RP) applications and avoids vendor lock-in that may lead to interoperability issues in the future, especially when the PKI needs to be trusted for a long time, may have no control over RPs or needs to be scaled.

Interoperability includes the following aspects:
- Interface specifications
- Data formats
- Communication protocols
- Algorithms
- Open standards

Main principles of interoperability are:
- Transparency and openness
- Technology neutrality
- Reusability and scalability
- Security and privacy
- Accessibility
- Sustainability
- Portability and extensibility

## Requirements

|                                                # | Requirement                                | Weight |
|-------------------------------------------------:|--------------------------------------------|-------:|
|     [1](#maintain-pki-interoperability-strategy) | Maintain PKI interoperability strategy     |      3 |
|            [2](#documented-integration-guidance) | Documented integration guidance            |      1 |
| [3](#adoption-and-application-of-open-standards) | Adoption and application of open standards |      3 |

## Details

### Maintain PKI interoperability strategy

#### Guidance

The interoperability strategy defines the interoperability requirements and the approach to achieve interoperability between the PKI components to ensure the PKI implementation is able to adopt new technologies and standards in the future, and will not be locked-in to a specific vendor.

PKI interoperability strategy should be maintained, documented, and integrated in the organization. It should cover at least the following information:
- Application of interoperability
- Using open standards and protocols
- Conditions for PKI components to be interoperable
- Restrictions on the use of proprietary interfaces
- Interoperability testing
- Requirements for migration to new technologies
- Requirements for vendors
- Other relevant information

#### Assessment

The following evidence should be available for the assessment of the requirement:
- Documented and approved interoperability strategy
- Interoperability strategy is integrated in the organization
- Interview with the responsible person(s) to verify understanding of the interoperability strategy
- Review documentation for PKI components to verify the requirements for interoperability

#### References

- [The Open Group Architecture Framework (TOGAF)](https://www.opengroup.org/togaf)

### Documented integration guidance

#### Guidance

To have effective interoperability between PKI components, it is important to have a proper integration in place that serves the purpose and does not expose any potential risks. Available and documented integration guidance for the developers and administrators should be maintained and updated regularly.

The integration guidance should be available for all critical PKI components and should cover at least the following information:
- Integration requirements and prerequisites
- Applicable standards and protocols
- Integration architecture
- Integration testing

#### Assessment

The following evidence should be available for the assessment of the requirement:
- Documented integration guidance for all critical PKI components
- Interview with the system administrators and developers
- Review of the integration guidance
- System configuration review

#### References

- [The Open Group Architecture Framework (TOGAF)](https://www.opengroup.org/togaf)
- Integration instructions provided by the vendors

### Adoption and application of open standards

#### Guidance

Open standards are publicly available standards that are developed and maintained by communities or standardization bodies. Open standards are developed through a consensus-based process and are available to everyone without any restrictions. Open standards are usually free to use and implement.

The open standards are important for interoperability as they are typically technology-agnostic and are supported by technologies and solutions. Open standards are applicable for interfaces, communication protocols, cryptographic algorithms, data formats, automation and orchestration, and other aspects of the PKI.

The adoption of open standards significant increase interoperability and reduce the risk of vendor lock-in.

#### Assessment

The following evidence should be available for the assessment of the requirement:
- Documented list of open standards used by the PKI
- Policies requiring the use of open standards
- Interview with the responsible person to verify understanding of the open standards
- Review of training materials

#### References

- [Open Standards Principles](https://www.gov.uk/government/publications/open-standards-principles/open-standards-principles)
- [IETF Request for Comments (RFC)](https://www.ietf.org/standards/rfcs/)
- [OASIS Standards](https://www.oasis-open.org/standards)
- [ISO Standards](https://www.iso.org/standards.html)
- [ITU Standards](https://www.itu.int/en/ITU-T/standardization/)
- [NIST Standards](https://www.nist.gov/standards)
- [ETSI Standards](https://www.etsi.org/standards)
