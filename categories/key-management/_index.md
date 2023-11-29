---
date: 2023-03-21T7:00:00Z
title: 5 - Key management
weight: 5

---

# 5 - Key management

## Overview

Key management is the set of techniques and procedures supporting the establishment and maintenance of keying relationships between parties and components in the public key infrastructure. Key management encompasses techniques and procedures supporting:
- Initialization of system users and components;
- Generation, distribution, and installation of keying material;
- Controlling the use of keying material;
- Update, revocation, and destruction of keying material; and
- Storage, backup/recovery, and archival of keying material.

The key management is important for the PKI to maintain trust. It should be an integral part of the PKI procedures. Proper key management is one of the basic stones on which the PKI stands and relies on.

## Category maturity levels description

| Maturity level    | Description                                                                                                                                                                                                                                                      |
|:------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1 - Initial**   | No key management is defined. There are no key management responsibilities defined and assigned.                                                                                                                                                                 |
| **2 - Basic**     | Responsibilities and roles for key management are defined. Key management is managed ad-hoc and there is no documentation and inventory of cryptographic keys maintained.                                                                                        |
| **3 - Advanced**  | Key management and lifecycle is documented and maintained. Inventory of cryptographic keys and devices is avaialble. Procedures are formally followed.                                                                                                           |
| **4 - Managed**   | Encryption and key management policies are documented, followed, and integrated in the organization. Inventory of cryptographic keys and devices is maintained and validated. Responsibilities and roles are assigned and aware of all processes and procedures. |
| **5 - Optimized** | Key management is periodically reviewed and updated. Inventory of cryptographic keys and devices is complete, maintained and frequently validated. Process and procedures are formally approved, integrated and followed in the organization.                    |

## Requirements

|                                                                                    # | Requirement                                                                    | Weight |
|-------------------------------------------------------------------------------------:|--------------------------------------------------------------------------------|-------:|
| [1](#key-management-roles-and-responsibilities-are-documented-and-formally-assigned) | Key management roles and responsibilities are documented and formally assigned |      2 |
|                   [2](#inventory-of-cryptographic-keys-is-documented-and-maintained) | Inventory of cryptographic keys is documented and maintained                   |      2 |
|                [3](#inventory-of-cryptographic-devices-is-documented-and-maintained) | Inventory of cryptographic devices is documented and maintained                |      1 |
|      [4](#each-cryptographic-key-is-defined-and-has-documented-lifecycle-procedures) | Each cryptographic key is defined and has documented lifecycle procedures      |      2 |
|        [5](#cryptographic-cipher-suites-and-protocols-are-documented-and-maintained) | Cryptographic cipher suites and protocols are documented and maintained        |      2 |
|                            [6](#key-management-is-periodically-reviewed-and-updated) | Key management is periodically reviewed and updated                            |      3 |

## Details

### Key management roles and responsibilities are documented and formally assigned

#### Guidance

Proper definition of roles and responsibilities for key management operations establishes a good basis for accountability and auditing. The roles and responsibilities should follow key management policy, principles, and boundaries.

Personnel should be formally assigned to the role based on appropriate skills, and background check to ensure that there are no external risks associated that can cause potential compromise of key management.

Naming or assignment records should contain relevant information such as:
- Identification of personnel
- Role to be assigned
- Date of appointment
- Confirmation of required skills
- Acknowledgment of responsibilities

#### Assessment

- Documented roles and responsibilities
- Signed naming protocol of personnel to role(s)
- Roles and responsibilities matrix (that may be used to cross-check if there are any conflicting roles)
- Validation of required knowledge and skills
- Review according to the key management policy

#### References

- [ISO/IEC 27001 and related standards](https://www.iso.org/isoiec-27001-information-security.html)

### Inventory of cryptographic keys is documented and maintained

#### Guidance

Inventory of cryptographic keys is important and a strategic database for organizations to:
- Monitor cryptographic key status and compliance
- Quickly react to changes and incidents (deprecation of algorithms, compromise, new attacks and vulnerabilities)
- Understand impact of lifecycle changes, migration and use of keys

Although the cryptographic key inventory may be implemented and maintained using various tools and approaches, it should serve the purpose of having a consistent and accurate map of all cryptographic keys deployed in the organization with details like algorithm, key length, usage, storage, location, generation and distribution method, backup and recovery, key check value, fingerprint, number of share or components, owner or responsible person, uniqueness, crypto-periods, or any other applicable attributes and properties of the key.

Inventory should follow procedures and business as usual activities to keep it accurate and updated in time.

#### Assessment

- Documented inventory of cryptographic keys
- Accuracy and consistency 
- Completeness of inventory
- Validation of cryptographic key records

#### References

- [NIST SP 800-57 Recommendation for Key Management](https://csrc.nist.gov/projects/key-management/key-management-guidelines)
- [ISO/IEC 11770 Key Management](https://www.iso.org/standard/53456.html)

### Inventory of cryptographic devices is documented and maintained

#### Guidance

Sensitive cryptographic keys are protected by hardware security modules that can have various forms and comply with security standards such as FIPS 140-3 or Common Criteria Protection Profiles. The keys may be in some case software-protected when there is no high risk associated with its compromise.

The approved ways of protecting cryptographic keys should have defined rules, which can be specified by the key management policy and followed using the key management procedures. Cryptographic devices that protect keys may be quickly identified using the inventory of cryptographic keys with reference to an inventory of cryptographic devices.

The inventory of cryptographic devices should contain relevant information such as:
- Vendor and device model identification
- Serial numbers
- Hardware / firmware / software versions
- Security certification and expiration dates
- Locations

#### Assessment

- Documented requirements for cryptographic devices
- Documented inventory of cryptographic devices
- Completeness, accuracy, and consistency of inventory
- Validation of records

#### References

- [NIST SP 800-57 Recommendation for Key Management](https://csrc.nist.gov/projects/key-management/key-management-guidelines)
- [ISO/IEC 11770 Key Management](https://www.iso.org/standard/53456.html)

### Each cryptographic key is defined and has documented lifecycle procedures

#### Guidance

Each cryptographic key type that is defined and used for specific use-case should have a complete description of its lifecycle. Each lifecycle phase has a proper description of the process and is backed up with the procedure that is executed when needed.

The key can have various lifecycle phases, such as generation, registration, initialization, distribution, loading, storage, archiving, backup, recovery, revocation, removal, destruction, or others applicable for the key.

The lifecycle phases contains appropriate description of the procedure such as:
- Prerequisites for execution
- Required roles and permissions
- Procedure and records

#### Assessment

- Examine the definition of cryptographic key
- Documented key lifecycle phases
- Documented procedures and related records for the key lifecycle
- Lifecycle is integrated and followed in the organization

#### References

- [NIST SP 800-57 Recommendation for Key Management](https://csrc.nist.gov/projects/key-management/key-management-guidelines)
- [ISO/IEC 11770 Key Management](https://www.iso.org/standard/53456.html)

### Cryptographic cipher suites and protocols are documented and maintained

#### Guidance

Protocols and encryption strengths may quickly change or be deprecated due to identification of vulnerabilities or design flaws. In order to support current and future data security needs, the organization should know where cryptography is used and understand how they would be able to respond rapidly to changes impacting the strength of their cryptographic implementations.

Specific rules and boundaries to be applied for cryptographic cipher suites and protocols should be documented in encryption management policy that reflect the current status of cryptography practice.

Cipher suites and protocols should be regularly checked against the implemented technology and configuration. Any deviation from the documented and allowed protocols should be fixed.

#### Assessment

- Documented encryption management policy
- Validation of implementation and used protocols against what is documented
- Accuracy of the description
- Security and vulnerabilities of applicable cipher suites and protocols

#### References

- [NIST SP 800-57 Recommendation for Key Management](https://csrc.nist.gov/projects/key-management/key-management-guidelines)
- [ISO/IEC 11770 Key Management](https://www.iso.org/standard/53456.html)
- [NIST SP 800-131A Transitioning the Use of Cryptographic Algorithms and Key Lengths](https://csrc.nist.gov/publications/detail/sp/800-131a/rev-2/final)

### Key management is periodically reviewed and updated

#### Guidance

Key management policy, processes and procedures related to cryptographic keys, inventory and lifecycle should be periodically reviewed, updated and approved. The frequency of review should be based on the organizational risks and needs to be protected against current and future trends.

Periodical review helps to keep the key management accurate and helps to maintain required skills and knowledge.
It provides assurance that the expected controls are active and working as intended.

#### Assessment

- Risk management and review frequency
- Implementation of review process
- Validation of documentation and reviews

#### References

- [ISO/IEC 27001 and related standards](https://www.iso.org/isoiec-27001-information-security.html)
