# PKI MM - *Certificate Management*

## Overview

Certificate management is the set of techniques and procedures supporting certificate lifecycle management. Certificate management encompasses techniques and procedures supporting:

* Definition of certificate profiles
* Generation of certificates
* Installation and orchestation of certificates
* Inventory of certificates
* State management of certificates, i.e. expiration and revocation
* Discovery of certificates

## Requirements

> **Note**
> Overview of the requirements that are applicable for the category together with weights. This should serve as a quick overview of what should be assessed.

> **Note**
> The overview of requirements can be also used for quick assessment and reporting, because it contains references to requirements and may be filled with the assessment level.

| #                      | Requirement                 | Weight     |
|------------------------|-----------------------------|------------|
| [1](#certificate-profiles-are-documented) | Certificate profiles are documented | 2 |
| [2](#certificate-cipher-suites-are-documented-and-maintained) | Certificate cipher suites are documented and maintained| 2 |
| [3](#process-and-protocols-for-certificate-generation-is-documented) | Process and protocols for certificate generation is documented | 2 |
| [4](#methods-for-certificate-installation-are-documented) | Methods for certificate installation are documented | 1 |
| [5](#inventory-of-issued-certificates-is-documented-and-maintained) | Inventory of issued certificates is documented and maintained | 3 |
| [6](#certificate-expiration-is-documented-and-monitored) | Certificate expiration is documented and monitored | 3 |
| [7](#certificate-revocation-process) | Certificate revocation process | 2 |
| [8](#network-certificates-are-discovered) | Network certificates are discovered | 2 |
| [9](#certificate-management-is-periodically-reviewed-and-updated) | Certificate management is periodically reviewed and updated | 4 |


> **Note**
> The weights can be evenly distributed to have each requirement with the same impact.

> **Note**
> Maturity level for each catogry is selected based on the assessment result and for the values refer to [Maturity Levels](../../model/pkimm.md#maturity-levels).

## Details

### Certificate profiles are documented
#### Guidance
Certificate profiles specify the contents of certificates for one or more use cases. It defines things such as:
* Certificate use case(s) for certificates covered by a specific profiles
* Naming standards for subject distinguished name and subject alternative names, which are allowed and mandatory fields.
* Certificate validity periods
* Certificate extensions, mandatory and allowed extensions, their criticality and possible values
* Allowed key types and signature algorithms
* Revocation profiles, i.e. CRL and/or OCSP

#### Assessment
* Determine the scope of applicability
* Documented and approved certificate profiles
* Content of the profiles is complete and unambiguous
* Certificate profiles are implemented in certificate authority
* Certificate profiles are enforced by certificate authority
* Certificate profiles are compatible with RFC5280, or deviations are well documented
* Profiles for CRLs and/or OCSP usage, i.e. validity periods, issuance intervals, max revocation time delay, etc

#### Refences
Most certificate profiles aim for compatibility with RFC5280 for maximum interoperability. Some examples of specific profiles are given below.
* RFC5280
* CA/B FOrum baseline requirements
* ETSI QCP

### Certificate cipher suites are documented and maintained
#### Guidance
Cipher suites, for certificates specifically defining key algorithms, key security levels and signature algorithms are important to be crypto agile. In particular during the coming years phased migration to post quantum signature algorithms. An organization should have a clear rationale to the usage of specific algorithms, and how long they will be valid and what may replace them in the future.

#### Assessment
* Determine the scope of applicability
* Documented and approved cipher suites with rationale for inclusion of algorithms
* Documented agile path for migration to other algrithms
* Cipher suites are enforced by certificate authority

#### Refences
* RFC5280
* RFC algorithms(?)
* SOG-IS crypto algorithms
* NIST approved algorithms CSNA 2.0 and Suite B
* NIST round 3 report
* SP 800-208

### Process and protocols for certificate generation is documented
#### Guidance
Issuance of certificates follow specific procedures, be it manual processes or automated processes using a standard or non-standard PKI protocol. An organization should be clear about:
* Validation procedures used for issuing certificates, by RAs and CAs
* On-line or off-line protocols used for enrollment

#### Assessment
* Documented validation rules
* Documented manual processes for issuing certificates
* Documented on-line protocols for issuing certificates, and the configuration of protocols
* 

#### Refences
Some examples of protocols and profiled usage of protocols
* RFC4210
* 3GPP 33.310
* Unisig subset-137

### Methods for certificate installation are documented
#### Guidance
When certificates are issued, they must also be installed. This can be done manually or automated.

#### Assessment
* Documented certificate subject installation procedures
* User guidance

#### Refences

### Inventory of issued certificates is documented and maintained
#### Guidance
Issued certificates must be known, in order to be able to track their life cycle, be able to revoke, and renew. Everything does not have to be centralized, there are use cases where a central inventory is not needed, for example specific device use cases, and there are use cases where a central inventory is critical in order to avoid severe outages.

#### Assessment
* Documented criticality of inventory for different use cases
* Documented inventory and inventory management
* System implementation of inventory, i.e. database vs spread sheet

#### Refences
Wikipedia on certificate lifecycle management

### Certificate expiration is documented and monitored
#### Guidance
Certificate expirations are historically a case of severe and costly outages, which can be prevented with a proper inventory and expiration monitoring.

#### Assessment
* Documented criticality of expiration for different use cases
* Automated monitoring and alerting of expiration for critical systems
* Automated certificate renewal

#### Refences

### Certificate revocation process
#### Guidance
When certificates need to be revoked it is important to have a well defined process for this.
* Where subjects can contact to get a certificate revoked
* Where misuse of certificates can be reported
* How long after a revocation request it takes for a certificate to be revoked
* How revocation information is dessiminated to relying parties

#### Assessment
* Documented revocation procedures, both for subjects and administrators
* Documented contact points for reports in the organizations or from relying parties
* List of relying parties that depend on updated revocation information
* Documentation how relying parties get access to revocation information

#### Refences

### Network certificates are discovered
#### Guidance
A simple way to avoid a server-side shadow (unknown to the security team) certificates, and avoid outages is to scan the network for certificates used on known protocols and ports.

#### Assessment
* A network discovery tool is run regularly
* Certificate inventory is updated with discovered certificates

#### Refences

### Certificate management is periodically reviewed and updated
#### Guidance
No certificate issuance and management system works over long periods of time without changes to use cases, processes, protocols and algorithms. It is important that the management systems are updated to vaoid gaps.

#### Assessment
* Documented process for reviewing the certificate management process and systems
* Ability to implement updates to ceritficate management system

#### Refences

