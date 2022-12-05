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
| [2](#requirement-2) | Certificate cipher suites are documented and maintained        | 2      |
| [3](#requirement-3) | Process and protocols for certificate generation is documented | 2      |
| [4](#requirement-4) | Methods for certificate installation are documented            | 1      |
| [5](#requirement-5) | Inventory of issued certificates is documented and maintained  | 3      |
| [6](#requirement-6) | Certificate expiration is documented and monitored             | 3      |
| [7](#requirement-7) | Certificate revocation process                                 | 2      |
| [8](#requirement-8) | Network certificates are discovered                            | 2      |
| [9](#requirement-9) | Certificate management is periodically reviewed and updated    | 4      |

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

<a name="requirement-2"></a>
### Certificate cipher suites are documented and maintained

#### Guidance

Cipher suites, for certificates specifically defining key algorithms, key security levels and signature algorithms are important to be crypto agile. For example, the change of the cipher suites can be required when the cryptographic algorithm becomes broken, or deprecated. An organization should have a clear rationale to the usage of specific algorithms, and how long they will be valid and what may replace them in the future.

#### Assessment

* Determine the scope of applicability
* Documented and approved cipher suites with rationale for inclusion of algorithms
* Documented agile path for migration to other algorithms if needed
* Cipher suites are enforced by certificate authority

#### References

* [RFC 5280 - Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile](https://datatracker.ietf.org/doc/html/rfc5280)
* [SOG-IS crypto algorithms](https://www.sogis.eu/uk/supporting_doc_en.html)
* NIST approved algorithms [CNSA 2.0](https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF) and [Suite B](https://apps.nsa.gov/iaarchive/programs/iad-initiatives/cnsa-suite.cfm)
* [NIST SP 800-208 - Recommendation for Stateful Hash-Based Signature Schemes](https://csrc.nist.gov/publications/detail/sp/800-208/final)

<a name="requirement-3"></a>
### Process and protocols for certificate generation is documented

#### Guidance

Issuance of certificates follow specific procedures, be it manual processes or automated processes using a standard or non-standard PKI protocol. An organization should be clear about:
* Validation procedures used for issuing certificates, by RAs and CAs
* On-line or off-line protocols used for enrollment

#### Assessment

* Documented automated / manual process for issuing certificates
* Documented validation rules for certification requests
* Documented on-line protocols for issuing certificates, and the configuration of protocols

#### References

Some examples of protocols and profiled usage of protocols are:
* [RFC 4210 - Internet X.509 Public Key Infrastructure
  Certificate Management Protocol (CMP)](https://datatracker.ietf.org/doc/html/rfc4210/)
* [3GPP 33.310 - Network Domain Security (NDS); Authentication Framework (AF)](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=2293)
* [UNISIG SUBSET-137](https://web.archive.org/web/20180917143529/https://www.era.europa.eu/filebrowser/download/542_en)

<a name="requirement-4"></a>
### Methods for certificate installation are documented

#### Guidance

When certificates are issued, they must also be installed. This can be done manually or automated.

#### Assessment

* Documented certificate subject installation procedures
* User guidance

#### References

<a name="requirement-5"></a>
### Inventory of certificates is documented and maintained

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

<a name="requirement-6"></a>
### Certificate expiration is documented and monitored

#### Guidance

Certificate expirations are historically a case of severe and costly outages, and expired certificates can be a subject of various vulnerabilities and attacks. Proper process of monitoring expiring certificates prevents common issues that can break trust between relying parties. Owner of the certificate should always provide information about the certificate renewal process or termination of its operation.

#### Assessment
 
* Documented criticality of expiration for different use cases
* Automated monitoring and alerting of expiration for critical systems
* Automated certificate renewal
* Distribution of renewed certificate to all locations where it should replace expiring certificate
* Decommissioning of expired certificate in case it is not renewed

#### References

<a name="requirement-7"></a>
### Certificate revocation process

#### Guidance

When certificates need to be revoked it is important to have a well-defined certificate revocation process:
* Where subjects can contact to get a certificate revoked
* Where misuse of certificates can be reported
* How long after a revocation request it takes for a certificate to be revoked
* How revocation information is disseminated to relying parties

#### Assessment

* Documented revocation procedures, both for subjects and administrators
* Documented contact points for reports in the organizations or from relying parties
* List of relying parties that depend on updated revocation information
* Documentation how relying parties get access to revocation information

#### References

<a name="requirement-8"></a>
### Certificate discovery process is documented and implemented

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

<a name="requirement-9"></a>
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