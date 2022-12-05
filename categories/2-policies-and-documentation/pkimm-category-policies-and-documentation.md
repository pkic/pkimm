# PKI MM - *Policies and documentation*

> **Warning**
> TBD

## Overview

Policies, processes, and procedures plays important role in the secure and consistent management of the public key infrastructure. Integrated and followed set of policies and documentation covers all areas and aspects of establishment and maintenance of the trust between external and internal parties:
- formal policies and practice statements for supported PKI services and use-cases
- formal management of agreements between parties involved in the PKI
- certificate and key management rules
- roles and responsibilities in the management of the PKI
- documented disclosure statements
- maintenance and review of policies and documentation

Proper documentation, policies, and related processes and procedures keeps the PKI assets trusted over the time. It is a living management system that is continuously updated and changed as technologies, security, and compliance requirements change.

## Requirements

| #                   | Requirement                                                        | Weight |
|---------------------|--------------------------------------------------------------------|--------|
| [1](#requirement-1) | Certificate policy (CP) is documented and published                | 5      |
| [2](#requirement-2) | Certification practice statement (CPS) is documented and published | 5      |
| [3](#requirement-3) | Key management policy is documented and integrated                 | 3      |
| [4](#requirement-4) | Policies are periodically reviewed and updated                     | 3      |

## Details

<a name="requirement-3"></a>
### Key management policy is documented and integrated

#### Guidance

The key management policy is a high-level statement of organizational key management policies that identifies high-level structure, responsibilities, governing standards and guidelines, organizational dependencies and other relationships, and security policies.

Key management is defined within the context of a specific key management policy. The policy affects the stringency of cryptographic requirements, depending on the susceptibility of the environment in question to various types of attack. Security policies typically also specify:
- practices and procedures to be followed in carrying out technical and administrative aspects of key management, both automated and manual;
- the responsibilities and accountability of each party involved; and
- the types of records (audit trail information) to be kept, to support subsequent reports or reviews of security-related events.

The key management policy describes basic principles adopted like dual control, split knowledge, separation of duties, boundaries for the management of cryptographic keys, as well as requirements on the hardware security.

#### Assessment

- Determine the scope of applicability
- Documented and approved key management policy
- Content of the key management policy is complete
- Key management policy is integrated in oraganization

#### References

- [NIST SP 800-57 Recommendation for Key Management](https://csrc.nist.gov/projects/key-management/key-management-guidelines)
- [ISO/IEC 11770 Key Management](https://www.iso.org/standard/53456.html)