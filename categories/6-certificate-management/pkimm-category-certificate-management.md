# PKI MM - *Certificate Management*

## Overview

Certificate management is the set of techniques and procedures supporting certificate lifecycle management. Certificate management encompasses techniques and procedures supporting:
* Definition of certificate profiles
* Generation of certificates
* Installation and orchestration of certificates
* Inventory of certificates
* State management of certificates, i.e. expiration and revocation
* Discovery of certificates

## Requirements

| #                   | Requirement                                                    | Weight |
|---------------------|----------------------------------------------------------------|--------|
| [1](#requirement-1) | Certificate profiles are documented                            | 2      |
| [2](#requirement-2) | Certificate cipher suites are documented                       | 2      |
| [3](#requirement-3) | Certificate Life Cycle Management is documented                | 2      |
| [5](#requirement-4) | Inventory of issued certificates is documented                 | 3      |
| [8](#requirement-5) | Certificate discovery process is documented                    | 2      |
| [9](#requirement-6) | Certificate management is periodically reviewed and updated    | 4      |

## Details

<a name="requirement-1"></a>
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

#### References

Most certificate profiles aim for compatibility with RFC 5280 for maximum interoperability. Some examples of specific profiles are given below.
* [RFC 5280 - Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile](https://datatracker.ietf.org/doc/html/rfc5280)
* [CA/B Forum baseline requirements](https://cabforum.org/baseline-requirements/)
* [ETSI Qualified Certificate Profiles](https://portal.etsi.org/TB-SiteMap/ESI/Trust-Service-Providers)
* [ETSI 319-411-1](https://www.etsi.org/deliver/etsi_en/319400_319499/31941101/01.03.01_60/en_31941101v010301p.pdf)
* [ETSI 319-411-2](https://www.etsi.org/deliver/etsi_en/319400_319499/31941102/02.03.01_60/en_31941102v020301p.pdf)
* [3GPP 33.310 - Network Domain Security (NDS); Authentication Framework (AF)](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=2293)
* [UNISIG SUBSET-137](https://www.era.europa.eu/system/files/2022-11/index083_-_subset-137_v100.pdf)

<a name="requirement-2"></a>
### Certificate cipher suites are documented

#### Guidance

Cipher suites, for certificates specifically defining key algorithms, key security levels and signature algorithms are important to be crypto agile. For example, the change of the cipher suites can be required when the cryptographic algorithm becomes broken, or deprecated. An organization should have a clear rationale to the usage of specific algorithms, and how long they will be valid and what may replace them in the future.

#### Assessment

* Determine the scope of applicability
* Documented and approved cipher suites with rationale for inclusion of algorithms
* Documented agile path for migration to other algorithms when needed
* Cipher suites are enforced by certificate authority

#### References

* [RFC 5280 - Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile](https://datatracker.ietf.org/doc/html/rfc5280)
* [SOG-IS crypto algorithms](https://www.sogis.eu/uk/supporting_doc_en.html)
* NIST [Suite B](https://apps.nsa.gov/iaarchive/programs/iad-initiatives/cnsa-suite.cfm)
* NIST approved algorithms [CNSA 2.0](https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF)
* [NIST SP 800-208 - Recommendation for Stateful Hash-Based Signature Schemes](https://csrc.nist.gov/publications/detail/sp/800-208/final)

<a name="requirement-3"></a>
### Certificate Life Cycle Management is documented

#### Guidance

Issuance of certificates follow specific procedures, be it manual processes or automated processes using standard or non-standard PKI protocol. An organization should be clear about the full life cycle management of certificates:
1. Certificate Application and the validation procedures used, by RAs and CAs
2. Certificate Issuance and protocols used for enrollment, on-line and off-line
3. Certificate Renewal, Re-key and Modification, upon exiration or other causes
  * Certificate expirations are historically a case of severe and costly outages. Proper process of renewal and monitoring expiring certificates prevents common issues
4. Certificate Revocation
  * When certificates need to be revoked it is important to have a well-defined certificate revocation process:
    * Where subjects can contact to get a certificate revoked
    * Where misuse of certificates can be reported
    * How long after a revocation request it takes for a certificate to be revoked
    * How revocation information is disseminated to relying parties
5. Certificate status dissemination
6. Key escrow and recovery
7. Trust anchor management

#### Assessment

* Documented application and validation rules
* Documented process for issuing certificates
** configuration of protocols
* Documented Certificate Acceptance and certificate subject installation procedures
* Documented renewal criteria, where re-key is nessecary and which certificate modifications are allowed
** Documented criticality of expiration for different use cases
** Automated monitoring and alerting of expiration for critical systems
** Automated certificate renewal
* Documented revocation process
** Documented revocation procedures, both for subjects and administrators
** If suspension is used the un-revocation process
** Documented contact points for reports in the organizations or from relying parties
** List of relying parties that depend on updated revocation information
* Documented Certificate status service
** OCSP and/or CRLs
** Documentation how relying parties get access to revocation information
* Documented process for key escrow and recovery when encryption keys need to be stored centrally
* Documented trust anchor management
** Distribution of new and updated trust anchors (Root CA certificates)

#### References

Examples of process, protocols and profiled usage:
* [RFC 4210 - Internet X.509 Public Key Infrastructure
  Certificate Management Protocol (CMP)](https://datatracker.ietf.org/doc/html/rfc4210/)
* [CA/B Forum baseline requirements](https://cabforum.org/baseline-requirements/)
* [3GPP 33.310 - Network Domain Security (NDS); Authentication Framework (AF)](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=2293)
* [UNISIG SUBSET-137](https://www.era.europa.eu/system/files/2022-11/index083_-_subset-137_v100.pdf)


<a name="requirement-4"></a>
### Inventory of certificates is documented

#### Guidance

Certificate inventory consists of all known certificates and provides an overview of the managed and unmanaged certificates in the infrastructure. Without knowing certificates. it is not possible to track their life cycle, revoke, or renew on time. The certificate inventory is important for the organization because:
- it provides immediate access to the current status of certificate
- provides possibility to react on certificate-related events (compromise, change, expiration, etc.)
- we understand impact of lifecycle changes 
- it gives information on all locations of certificates
- can enforce and maintain ownership of certificates

The certificate inventory therefore consists of information related to certificate like certificate attributes, validity and validation information, fingerprint and serial number, trust chain, owner, public key, signature algorithm, certificate type, compliance information, certificate locations, change history, or any other attributes and properties of the certificates that is required.

#### Assessment

* Documented criticality of inventory for different use cases
* Documented certificate inventory management
* Validation of certificate inventory records
* Effectiveness of the certificate inventory implementation

#### References

* [RFC 3647 - Internet X.509 Public Key Infrastructure
  Certificate Policy and Certification Practices Framework - Certificate Life-Cycle Operational Requirements](https://datatracker.ietf.org/doc/html/rfc3647/#section-4.4)
* [NIST SP 800-57 Part 1 Rev. 5 - certificate inventory management](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)



<a name="requirement-5"></a>
### Certificate discovery process is documented

#### Guidance

Certificate discovery process protect organization from unknown certificates that may be deployed in the infrastructure. Unknown certificates may be further issued by unauthorized certification authorities and mislead users of services. Certificate discovery helps to maintain current inventory of certificates. Certificate discovery process should be implemented based on supported certificates and use-cases, for example:
- to scan the network for certificates used on known protocols and ports to discover certificates that can potentially cause service outage or breach 
- search for the certificates on the file system to discover unauthorized or unsecured certificates

Discovery process should be run frequently on the specified locations and the certificate inventory should be updated based on the results of the certificate discovery to keep it current.

#### Assessment

* Documented certificate discovery requirements
* Documented certificate discovery process and its frequency
* Effectiveness of the supporting tools for the certificate discovery
* Certificate inventory is updated with discovered certificates

#### References

<a name="requirement-6"></a>
### Certificate management is periodically reviewed and updated

#### Guidance

No certificate issuance and management system works over long periods of time without changes to use-cases, processes, protocols and algorithms. It is important that the certificate management is periodically review and updated to avoid gaps. The frequency of review should be based on the organizational risks and needs to be protected against current and future trends.

Periodical review helps to keep the certificate management accurate and helps to maintain required skills and knowledge.
It provides also assurance that the expected controls are active and working as intended.

#### Assessment

* Documented process for reviewing the certificate management process and systems
* Ability to implement updates to certificate management system
* Document management system and validation of review

#### References

- [ISO/IEC 27001 and related standards](https://www.iso.org/isoiec-27001-information-security.html)
