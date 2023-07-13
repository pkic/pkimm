---
date: 2023-05-10T9:00:00Z
title: 15 - Resilience
weight: 15

---

# 15 - Resilience

## Overview

Resilience is the key for any organization wanting to thrive in an ever-changing world, which is obviously s very important factor for any PKI implementation. The PKI is planned to be trusted for multiple years, if not decades. Therefore, the ability to absorb and adapt to the unpredictability, while continuing to deliver on the objectives is becoming mandatory.

A robust resilience framework helps organizations future-proof their PKI oriented business, detailing key principles, attributes and activities that are followed to ensure that the PKI implementation will be trusted, secure, and effective all the time.

## Requirements

|                                                        # | Requirement                                        | Weight |
|---------------------------------------------------------:|----------------------------------------------------|-------:|
|       [1](#risk-assessment-and-business-impact-analysis) | Risk assessment and business impact analysis       |      6 |
|    [2](#cyber-security-management-and-incident-planning) | Cyber-security management and incident planning    |      4 |
| [3](#business-continuity-planning-and-disaster-recovery) | Business continuity planning and disaster recovery |      5 |
|                         [4](#technology-future-proofing) | Technology future proofing                         |      3 |
|                 [5](#competence-and-information-sharing) | Competence and information sharing                 |      3 |
|                   [6](#continual-review-and-improvement) | Continual review and improvement                   |      4 |

## Details

### Risk assessment and business impact analysis

#### Guidance

Proper risk assessment provides robust understanding about the risks and their impact on the business and organization PKI. The risk assessment results (for example potential loss scenarios) are documented and serves as input for the business impact analysis to identify the critical PKI-related business processes and their dependencies.

Documented results of the business impact analysis are used to develop recovery strategies for the PKI implementation with required resources and availability.

#### Assessment

The following is sample evidence that can be used to assess the requirement:
- Risk management and assessment process
- Documented risk assessment results
- Documented business impact analysis results
- Documented recovery strategies
- Understanding of the resilience and approval of the results
- Interview with the PKI management

#### References

- [ISO/IEC 27005 - Guidance on managing information security risks](https://www.iso.org/standard/80585.html)
- [NIST Risk Management Framework](https://csrc.nist.gov/Projects/risk-management)
- [ISO/TS 22317 - Guidelines for business impact analysis](https://www.iso.org/standard/79000.html)

### Cyber-security management and incident planning

#### Guidance

Cyber-security management covers activities to ensure that the PKI is protected against known and zero-day vulnerabilities, cyberattacks and other threats. The operational procedures and technologies are evolving and the PKI needs to be able to adapt to the changes. Without knowing the threats and vulnerabilities, it is not possible to plan for the resilience and properly plan for incident response.

Incident response planning helps to ensure that the organization is able to respond to the suspected incidents. Incident response plans should be documented and tested regularly. The result of executed incident response plans should be documented and used to improve the plan, even if it was a false alarm.

Cyber-security management and incident planning covers important aspects such as vulnerability management and security operations center (SOC) identification and response to potential incidents.

#### Assessment

The following is sample evidence that can be used to assess the requirement:
- Documented vulnerability management
- Vulnerability scanning results
- Documented incident response plans
- Documented incident response test results
- Monitoring of cyber-security threats
- Interview with the security operations team

#### References

- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)
- [Common Vulnerabilities and Exposures (CVE) Program](https://www.cve.org/About/Overview)
- [NIST Special Publication 800-61 Revision 2 - Computer Security Incident Handling Guide](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [SANS Guide to Security Operations](https://www.sans.org/posters/guide-to-security-operations/)

### Business continuity planning and disaster recovery

#### Guidance

The business continuity planning and disaster recovery are the key activities to ensure availability of the PKI operations. The business continuity planning is used to define the recovery time objectives (RTO) and recovery point objectives (RPO) for the PKI. The RTO and RPO are used to define the required resources and their availability.

Requirements for the business continuity and disaster recovery should be properly defined. It contains backups of the PKI resources, such as hardware security modules (HSM), databases, configuration files, etc. The availability of backups should be tested regularly to ensure that the backups are available when needed, especially during the disaster.

Proper measures are applied to identify the disaster and a communication matrix is maintained to ensure that the right people are informed about the disaster on time and the recovery process can be started.

The following parts are typically covered:
- Scope of the business continuity and disaster recovery
- Roles and responsibilities
- Activation of disaster recovery
- Physical locations
- Communication matrix
- Other requirements and information needed

#### Assessment

The following is sample evidence that can be used to assess the requirement:
- Documented business continuity and disaster recovery plans
- Documented recovery time objectives (RTO) and recovery point objectives (RPO)
- Documented backup and recovery procedures
- Communication matrix and contact information
- Availability of backups and other requirements to execute the disaster recovery procedure
- Periodically tested effectiveness of the disaster recovery

#### References

- [ISO/IEC 22301 - Business continuity management systems](https://www.iso.org/standard/50056.html)
- [NIST Special Publication 800-34 Revision 1 - Contingency Planning Guide for Federal Information Systems](https://csrc.nist.gov/publications/detail/sp/800-34/rev-1/final)

### Technology future proofing

#### Guidance

Applicable technology should always be future proofed to ensure that the PKI is able to adapt to changes, and will support the organization PKI in the future when new standards, algorithms, and approach will be developed.

When deciding to apply new technologies, or evaluating if the current technology is still suitable and support the goals of the PKI implementation, the following should be considered:
- Technology is supported by the vendor
- Industry standards are applied for interoperability and security
- Review and references on the vendor and technology
- Applicability of the technology for long-term use
- Vulnerabilities and security reports of the technology
- Integration capabilities and customizations needed
- Open source vs. proprietary technology

#### Assessment

The following is sample evidence that can be used to assess the requirement:
- Interview with the CTO or CIO
- Documentation of the technology future proofing
- RFI and RFP documents
- Vendor and technology check

#### References

- [ISO 223XX Security and resilience standards](https://www.iso.org/standard/77008.html)
- [ISO/IEC 22301 - Business continuity management systems](https://www.iso.org/standard/50056.html)

### Competence and information sharing

#### Guidance

Organization environments may change over time. The impact of changes can be in various forms, for example:
- personnel can rotate in their positions, new people can be hired, or people can leave the organization
- technologies are changing, therefore required skills and knowledge may change
- procedures and eventually management of the PKI will be adjusted

The organization needs to ensure that the competence of the personnel is maintained and the information is shared to not lose the knowledge introduced by changes within known and unknown variables. The organization should have a plan to ensure that the competence is maintained for the most critical parts of the PKI.

The competence and information sharing is an important part to achieve the resilience of the PKI implementation by having relevant information and competencies ready when needed.

#### Assessment

The following is sample evidence that can be used to assess the requirement:
- Documentation and collaboration
- Onboarding and offboarding procedures
- Building competence and knowledge sharing

#### References

- [ISO 223XX Security and resilience standards](https://www.iso.org/standard/77008.html)

### Continual review and improvement

#### Guidance

The resilience of the PKI implementation should be reviewed and improved regularly. The review and improvement process should be documented and the results should be used to improve the resilience of the PKI implementation. The frequency of review should be based on the organizational risks and needs to be protected against current and future trends.

#### Assessment

The following is sample evidence that can be used to assess the requirement:
- Resilience effectiveness review frequency
- Implementation of review process
- Validation of documentation and reviews
- Training records

#### References

- [ISO 223XX Security and resilience standards](https://www.iso.org/standard/77008.html)
- [NIST Special Publications 800 - 30, 34, 37, 46, 53, 84](https://csrc.nist.gov/publications)
