---
date: 2023-06-11T9:00:00Z
title: Infrastructure Management
weight: 8

---

# Infrastructure Management

The PKI implementation is a combination of software, hardware, network service, and resources that are needed to operate and manage the environment.
The environment can be hosted on-premise, in the cloud, or in a hybrid environment.

Independently on the hosting model, the PKI environment needs to be properly managed and maintained, which requires resources and processes.
The infrastructure management refers to management of the technical and operational components of the PKI environment, which includes software, hardware, network, equipment, facilities, and other related resources.

The PKI components may be distributed across multiple locations and managed by different teams. Therefore, it is important to have a clear description of the operational infrastructure with all dependencies and prerequisites. The infrastructure management should be aligned with the overall strategy of the organization and the scope of the PKI.

When the infrastructure and environment where the PKI is implemented are not effectively managed and maintained, the complexity of the environment increases and the risk of failure increases as well. The infrastructure is often one of key targets for attackers, therefore it is important to ensure that it is properly secured and available.

## Requirements

|                                                                    # | Requirement                                                    | Weight |
|---------------------------------------------------------------------:|----------------------------------------------------------------|-------:|
|            [1](#network-and-deployment-infrastructure-is-documented) | Network and deployment infrastructure is documented            |      4 |
|             [2](#separation-and-segmentation-principles-are-applied) | Separation and segmentation principles are applied             |      3 |
| [3](#network-vulnerability-management-is-implemented-and-maintained) | Network vulnerability management is implemented and maintained |      3 |
|                     [4](#infrastructure-recovery-objectives-control) | Infrastructure recovery objectives control                     |      1 |
|            [5](#infrastructure-activities-are-periodically-reviewed) | Infrastructure activities are periodically reviewed            |      2 |

## Details

### Network and deployment infrastructure is documented

#### Guidance

The network and deployment infrastructure should be aligned with the architecture and design of the PKI. In that terms, it provides details about how is the implementation done in the real environment.

The network and deployment infrastructure should be properly documented and maintained. The documentation should include the following:
- PKI components and their dependencies
- facilities and equipment
- deployment infrastructure description
- clustering and load balancing
- network topology and diagram
- communication and open ports requirements
- supported cloud providers and services
- supporting systems and services (identity management, access control, logging, monitoring, etc.)

#### Assessment

The following is sample evidence that can be used to assess the requirement:
- network topology and diagram
- deployment documentation
- sample configuration of network to compare with the documentation
- integration with supporting and other systems
- interview with the network administrators

#### References

- [ISO/IEC 20000 and related standards](https://www.iso.org/standard/70636.html)
- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)
- [Guidance for Containers and Container Orchestration Tools](https://docs-prv.pcisecuritystandards.org/Guidance%20Document/Containers%20and%20Container%20Orchestration%20Tools/Guidance-for-Containers-and-Container-Ochestration-Tools-v1_0.pdf)

### Separation and segmentation principles are applied

#### Guidance

The PKI environment should be properly separated and segmented from other environments and systems. The separation and segmentation should be applied on all levels, including network, infrastructure, and application. The separation and segmentation should be applied based on the security requirements and risk assessment.

Segmentation isolates the PKI environment from the remaining environment and reduces the risk of unauthorized access and data leakage. It also helps to reduce the impact of a potential compromise of the PKI environment from other systems and environments. Segmentation can be achieved using a number of physical or logical methods, such as:
- properly configured internal network security controls
- routers with strong access control lists
- other technologies that restrict access to a particular segment of a network

For the proper maintenance of the infrastructure and deployed PKI components, the staging/testing environment should be available in the same configuration as the production environment. If needed, development environment can be used for testing and development purposes.
Production, staging, and development environments should be logically separated and isolated from each other, including data that is used in the environments.

#### Assessment

The following is sample evidence that can be used to assess the requirement:
- network topology and diagram
- implementation of network isolation
- separation of production and testing environments
- sample data
- interview with the network administrators
- 
#### References

- [ISO/IEC 20000 and related standards](https://www.iso.org/standard/70636.html)
- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)

### Network vulnerability management is implemented and maintained

#### Guidance

The network vulnerability management is a process that is used to identify, classify, remediate, and mitigate vulnerabilities in the network infrastructure and protects PKI implementation from potential attacks. The process should be implemented and maintained in order to ensure that the network infrastructure is properly secured and protected from potential attacks.

The network vulnerability management should include the following:
- included in the overall vulnerability management process
- periodical scanning of the network infrastructure
- identification of vulnerabilities
- categorization and prioritization of vulnerabilities and remediation
- updating and patching requirements

#### Assessment

The following is sample evidence that can be used to assess the requirement:
- network vulnerability management process
- results from last network vulnerability scan
- remediation plan
- interview with the network administrators

#### References

- [Common Vulnerability Scoring System (CVSS)](https://www.first.org/cvss/)
- [ISO/IEC 20000 and related standards](https://www.iso.org/standard/70636.html)
- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)

### Infrastructure recovery objectives control

#### Guidance

In case of issues with the infrastructure, it should be possible to quickly identify the root cause and recover the infrastructure to the operational state. The recovery objectives should be defined and aligned with the overall business continuity and disaster recovery strategy of the organization.

The infrastructure should be frequently backed up and the backups should be stored in a secure location. The backups should be tested and validated on a regular basis. The infrastructure managed as a code may help to reduce complexity and increase the speed of recovery.

#### Assessment

The following is sample evidence that can be used to assess the requirement:
- infrastructure recovery objectives
- backup and recovery plan
- infrastructure configuration as a code
- interview with the infrastructure administrators

#### References

- [ISO/IEC 20000 and related standards](https://www.iso.org/standard/70636.html)
- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)

### Infrastructure activities are periodically reviewed

#### Guidance

Infrastructure management related activities should be periodically reviewed, updated and approved. The frequency of review should be based on the organizational risks and needs to be protected against current and future trends.

Periodical review helps to keep the infrastructure management accurate and helps to maintain required skills and knowledge.
It provides also assurance that the expected controls are active and working as intended.

The review can include the following:
- changes made to the infrastructure
- regular check of firewall rules
- review of the network topology
- review of the network segmentation
- regular check of access control lists
- vulnerability reports and timely remediation
- review and correlation of logs
- and other activities related to the infrastructure management

#### Assessment

The following is sample evidence that can be used to assess the requirement:
- infrastructure management activities review frequency
- organizational implementation of review process
- validation of documentation, reports, records, and reviews

#### References

- [ISO/IEC 20000 and related standards](https://www.iso.org/standard/70636.html)
- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)
