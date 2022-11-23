# PKI MM - Key Management

## Overview

Key management is the set of techniques and procedures supporting the establishment and maintenance of keying relationships between parties and components in the public key infrastructure. Key management encompasses techniques and procedures supporting:
- initialization of system users and components;
- generation, distribution, and installation of keying material;
- controlling the use of keying material;
- update, revocation, and destruction of keying material; and
- storage, backup/recovery, and archival of keying material.

The key management is important for the public key infrastructure to maintain trust. It should be integral part of the PKI procedures. Proper key management is one of the basic stones on which the PKI stands and relies on.

## Requirements

| #                   | Requirement                                                                    | Weight |
|---------------------|--------------------------------------------------------------------------------|--------|
| [1](#requirement-1) | Key management policy is documented and integrated                             | 4      |
| [2](#requirement-2) | Key management roles and responsibilities are documented and formally assigned | 2      |
| [3](#requirement-3) | Inventory of cryptographic keys is documented and maintained                   | 2      |
| [4](#requirement-4) | Inventory of cryptographic devices is documented and maintained                | 1      |
| [5](#requirement-5) | Each cryptographic key is defined and has documented lifecycle procedures      | 2      |
| [6](#requirement-6) | Cryptographic cipher suites and protocols are documented and maintained        | 2      |
| [7](#requirement-7) | Key management is periodically reviewed and updated                            | 3      |

## Details

<a name="requirement-1"></a>
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

<a name="requirement-2"></a>
### Key management roles and responsibilities are documented and formally assigned

#### Guidance

Proper definition of roles and responsibilities for key management operations establishes a good basis for accountability and auditing. The roles and responsibilities should follow key management policy, principles, and boundaries.

Personnel should be formally assigned to the role based on appropriate skills, and background check to ensure that there are no external risks associated that can cause potential compromise of key management.

Naming or assignment record should contain relevant information such as:
- identification of personnel
- role to be assigned
- date of appointment
- confirmation of required skills
- acknowledgment of responsibilities

#### Assessment

- Documented roles and responsibilities
- Signed naming protocol of personnel to role(s)
- Roles and responsibilities matrix (that may be used to cross-check if there are any conflicting roles)
- Validation of required knowledge and skills
- Review according the key management policy

#### References

- [ISO/IEC 27001 and related standards](https://www.iso.org/isoiec-27001-information-security.html)

<a name="requirement-3"></a>
### Inventory of cryptographic keys is documented and maintained

#### Guidance

Inventory of cryptographic keys is important and strategic database for organization to:
- monitor cryptographic key status and compliance
- quickly react on changes and incidents (deprecation of algorithms, compromise, new attacks and vulnerabilities)
- understand impact of lifecycle changes, migration and using keys

Although cryptographic key inventory may be implemented and maintained using various tools and approaches, it should serve the purpose of having consistent and accurate map of all cryptographic keys deployed in organization with details like algorithm, key length, usage, storage, location, generation and distribution method, backup and recovery, key check value, fingerprint, number of share or components, owner or responsible person, uniqueness, crypto-periods, or any other application attributes and properties of the key.

Inventory should follow procedures and business as usual activities to keep it accurate and updated in time.

#### Assessment

- Documented inventory of cryptographic keys
- Accuracy and consistency 
- Completeness of inventory
- Validation od cryptographic key records

#### References

- [NIST SP 800-57 Recommendation for Key Management](https://csrc.nist.gov/projects/key-management/key-management-guidelines)
- [ISO/IEC 11770 Key Management](https://www.iso.org/standard/53456.html)

<a name="requirement-4"></a>
### Inventory of cryptographic devices is documented and maintained

#### Guidance

Sensitive cryptographic keys are protected by hardware security modules that can have various forms and complies with security standards such as FIPS 140-3 or Common Criteria Protection Profiles. The keys may be in some case software-protected when there is no high risk associated with its compromise.

The approved ways of protecting cryptographic keys should have defined rules, which can be specified by the key management policy and followed using the key management procedures. Cryptographic devices that protect keys may be quickly identified using inventory of cryptographic keys with reference to inventory of cryptographic devices.

The inventory of cryptographic devices should contain relevant information such as:
- vendor and device model identification
- serial numbers
- hardware / firmware / software versions
- security certification and expiration dates
- locations

#### Assessment

- Documented requirements on cryptographic devices
- Documented inventory of cryptographic devices
- Completeness, accuracy, and consistency of inventory
- Validation of records

#### References

- [NIST SP 800-57 Recommendation for Key Management](https://csrc.nist.gov/projects/key-management/key-management-guidelines)
- [ISO/IEC 11770 Key Management](https://www.iso.org/standard/53456.html)

<a name="requirement-5"></a>
### Each cryptographic key is defined and has documented lifecycle procedures

#### Guidance

Each cryptographic key type that is defined and used for specific use-case should have complete description of its lifecycle. Each lifecycle phase has proper description of process and is backed up with the procedure that is executed when needed.

The key can have various lifecycle phases, such as generation, registration, initialization, distribution, loading, storage, archiving, backup, recovery, revocation, removal, destruction, or other applicable for the key.

The lifecycle phases contains appropriate description of the procedure such as:
- prerequisites for execution
- required roles and permissions
- procedure and records

#### Assessment

- Examine the definition of cryptographic key
- Documented key lifecycle phases
- Documented procedures and related records for the key lifecycle
- Lifecycle is integrated and followed in organization

#### References

- [NIST SP 800-57 Recommendation for Key Management](https://csrc.nist.gov/projects/key-management/key-management-guidelines)
- [ISO/IEC 11770 Key Management](https://www.iso.org/standard/53456.html)

<a name="requirement-6"></a>
### Cryptographic cipher suites and protocols are documented and maintained

#### Guidance

Protocols and encryption strengths may quickly change or be deprecated due to identification of vulnerabilities or design flaws. In order to support current and future data security needs, organization should know where cryptography is used and understand how they would be able to respond rapidly to changes impacting the strength of their cryptographic implementations.

Specific rules and boundaries to be applied for cryptographic cipher suites and protocols should be documented in encryption management policy that reflect the current status of cryptography practice.

Cipher suites and protocols should be regularly checked against the implemented technology and configuration. The deviation from the documented and allowed protocols should be fixed.

#### Assessment

- Documented encryption management policy
- Validation of implementation and used protocols against what is documented
- Accuracy of the description
- Security and vulnerabilities of applicable cipher suites and protocols

#### References

- [NIST SP 800-57 Recommendation for Key Management](https://csrc.nist.gov/projects/key-management/key-management-guidelines)
- [ISO/IEC 11770 Key Management](https://www.iso.org/standard/53456.html)
- [NIST SP 800-131A Transitioning the Use of Cryptographic Algorithms and Key Lengths](https://csrc.nist.gov/publications/detail/sp/800-131a/rev-2/final)

<a name="requirement-7"></a>
### Key management is periodically reviewed and updated

#### Guidance

Key management policy, processes and procedures related to cryptographic keys, inventory and lifecycle should be periodically reviewed, updated and approved. The frequency of review should be based on the organizational risks and needs to be protected against current and future trends.

Periodical review helps to keep the key management accurate and helps to maintain required skills and knowledge.
It provides also assurance that the expected controls are active and working as intended.

#### Assessment

- Risk management and review frequency
- Implementation of review process
- Validation of documentation and reviews

#### References

- [ISO/IEC 27001 and related standards](https://www.iso.org/isoiec-27001-information-security.html)