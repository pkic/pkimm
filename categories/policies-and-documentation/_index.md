---
date: 2023-03-21T7:00:00Z
title: 2 - Policies and documentation
weight: 2

---

# 2 - Policies and documentation

Documented policies plays important role in the secure and consistent management of the public key infrastructure. The goal is to minimize financial and operational threats and risks in the digital world. Well-described policies and security measures increase overall trust in the ecosystem of trust services and are conditional to be able to operate. The basis for these matters lies in relevant laws and regulations, international standards and best practices.

It consists of:
- formal policies and practice statements for supported PKI services and use-cases
- formal management of agreements between parties involved in the PKI
- certificate and key management rules
- roles and responsibilities in the management of the PKI
- documented disclosure statements
- maintenance and review of policies and documentation
- code of practice for information security management, techniques and risk management

Properly documented policies keeps the PKI assets trusted over the time and serves as a basis for integrated processes and procedures. It is a living management system that is continuously updated and changed as technologies, security, and compliance requirements change.

The certificate policy (CP) defines the overall policies and requirements of a PKI, the certification practice statement (CPS) provides detailed operational procedures followed by the certification authority, and the disclosure statement offers transparency about the CA's identity and services to relying parties.

## Requirements

|                                                                  # | Requirement                                                  | Weight |
|-------------------------------------------------------------------:|--------------------------------------------------------------|-------:|
|              [1](#the-scope-of-policies-is-defined-and-documented) | The scope of policies is defined and documented              |      2 |
|               [2](#certificate-policy-is-documented-and-published) | Certificate policy is documented and published               |      5 |
| [3](#certification-practice-statement-is-documented-and-published) | Certification practice statement is documented and published |      5 |
|             [4](#disclosure-statement-is-documented-and-published) | Disclosure statement is documented and published             |      4 |
|               [5](#policies-are-periodically-reviewed-and-updated) | Policies are periodically reviewed and updated               |      3 |

## Details

### The scope of policies is defined and documented

#### Guidance

Each PKI implementation and use case is different, therefore it requires different care. The scope of policies that are applicable for the implementation should be defined and documented. When the proper description of the policies scope is provided, it helps all parties involved to understand the purpose of the policies and their applicability.

The scope can include the following:
- Identification of the policies required for the implementation
- Reasoning why the policies are required or not required
- Structure of policies and documentation
- List of policies with references, versions, etc.
- Any other relevant information

#### Assessment

- The scope of policies is defined and documented
- The scope of policies is complete
- Interview with the management and PKI responsible personnel to confirm the scope

#### References

- [RFC 3647 - Internet X.509 Public Key Infrastructure Certificate Policy and Certification Practices Framework](https://tools.ietf.org/html/rfc3647)
- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)
- [ETSI EN 319 401 - General Policy Requirements for Trust Service Providers](https://www.etsi.org/deliver/etsi_en/319400_319499/319401/02.03.01_60/en_319401v020301p.pdf)

### Certificate policy is documented and published

#### Guidance

Certificate policy (CP) is used to establish the controls of the issuing party and the roles and responsibilities of its entities for the specific PKI implementation and use case. Its used to provide assurance to partners and show the trustworthiness by the use of standards. It can be considered as a high level contract between the parties involved in the PKI and therefore should be published and available to all parties involved.

CPs are described in a document form where the content may differ. Multiple policies can be part of a single document for different use cases. A CP contains a set of rules that indicates the applicability of a certificate to a particular community and/or class of applications with common security requirements or level of security (for instance certificates for the purpose of: persons, domains, organizations, authenticity and confidentiality, services). To uniquely identify the purpose of the certificates the CP contains unique numbers (Object Identifier, OID) which needs to be registered.

In general CP is addressing the following items:
-	Types of certificates
-	Document name and identification
-	PKI participants
-	Certificate usage
-	Policy administration
-	Definitions
-	Publication and repository responsibilities
-	Identification and authentication
-	Certificate life-cycle operational requirements
-	Facility management and operational controls
-	Technical security controls
-	Certificate CRL and OCSP profiles
-	Compliance audit and other assessments
-	Other business and legal matters

#### Assessment

- The CP is properly documented in its full scope
- The CP clearly defines the scope of the policy, such as the purpose of the security and assurance levels, the type and use of its certificates and parties involved
- The legal rights and responsibilities of parties are described in the CP
- CP has listed correct object identifiers for the purpose its used for
- Verify that the CP is published and available to all parties involved
- Interview with the management and PKI responsible personnel to confirm the CP is accurate and followed

#### References

- [RFC 3647 - Internet X.509 Public Key Infrastructure Certificate Policy and Certification Practices Framework](https://tools.ietf.org/html/rfc3647)
- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)
- [ETSI EN 319 411-1 - Policy and security requirements for Trust Service Providers issuing certificates](https://www.etsi.org/deliver/etsi_en/319400_319499/31941101/01.03.01_60/en_31941101v010301p.pdf)

### Certification practice statement is documented and published

#### Guidance

In addition to CP, there is typically a certification practice statement (CPS). While a CP is more at a strategic level, detailed information about how things should be carried out is part of a CPS (tactical level). In most cases the CP and CPS are combined into a single managed document, however they can be split in case needed.

The CPS covers the same items as the CP, but in a technical detail to let know how the CP is implemented. All parties involved in the PKI should be aware of the CPS and follow it. The CPS is a living document that is continuously updated and changed as technologies, security, and compliance requirements change.

#### Assessment

- The CPS is properly documented in its full scope
- CPS is published and available to all parties involved
- Interview with the management and PKI responsible personnel to confirm the CPS is accurate and followed
- Confirm that the information in the CPS is consistent with the information in the CP

#### References

- [RFC 3647 - Internet X.509 Public Key Infrastructure Certificate Policy and Certification Practices Framework](https://tools.ietf.org/html/rfc3647)
- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)
- [ETSI EN 319 411-1 - Policy and security requirements for Trust Service Providers issuing certificates](https://www.etsi.org/deliver/etsi_en/319400_319499/31941101/01.03.01_60/en_31941101v010301p.pdf)

### Disclosure statement is documented and published

#### Guidance

The disclosure statement (DS) is a document that describes the PKI and its services. It refers to a document that discloses the relevant information about the CA and its services to the relying parties.

It typically includes information like:
- CA's identity, legal status, and contact information
- Certificate types, verification procedures and compliance with standards
- Reliance limits
- Obligations of the CA and the relying parties
- Warranty and liability limitations
- Agreement, CP and CPS
- Privacy policy
- Refund policy and claims
- Information on audit and compliance

The purpose of a DS is to provide transparency to relying parties, allowing them to assess the trustworthiness and reliability of the CA before relying on its certificates.

#### Assessment

- The DS is properly documented in its full scope
- DS is published and available to all parties involved
- Interview with the management and PKI responsible personnel to confirm the DS is accurate
- Confirm that the information in the DS is consistent with the information in the CP and CPS

#### References

- [ETSI EN 319 411-1 - Policy and security requirements for Trust Service Providers issuing certificates](https://www.etsi.org/deliver/etsi_en/319400_319499/31941101/01.03.01_60/en_31941101v010301p.pdf)

### Policies are periodically reviewed and updated

#### Guidance

Policies are living documents that are continuously updated and changed as technologies, security, and compliance requirements change. The policies should be reviewed and updated periodically. The frequency of review should be determined by the organization. Good practice is to review policies at least annually or when there are significant changes in the PKI or its environment.

#### Assessment

- The policies are reviewed and updated periodically
- Check the last review date of the policies
- Implementation of review process
- Validation of documentation and reviews
- Interview with the management and PKI responsible personnel to confirm the policies are reviewed and updated periodically

#### References

- [RFC 3647 - Internet X.509 Public Key Infrastructure Certificate Policy and Certification Practices Framework](https://tools.ietf.org/html/rfc3647)
- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)
- [ETSI EN 319 401 - General Policy Requirements for Trust Service Providers](https://www.etsi.org/deliver/etsi_en/319400_319499/319401/02.03.01_60/en_319401v020301p.pdf)
