---
date: 2023-03-21T7:00:00Z
title: PKI Maturity Model

---

# PKI Maturity Model

The objective of this document is to provide a definition of the PKI maturity model and what is the maturity assessment process and procedures in order to rate the current maturity level according the model and track progress.

## Maturity Model

The maturity model is based on the Capability Maturity Model Integration ([CMMI](https://en.wikipedia.org/wiki/Capability_Maturity_Model_Integration)) developed by Carnegie Mellon University. It should provide the following::
- Quickly understand the current level of capabilities and performance of the PKI
- Support comparison of PKI maturity with similar organizations based on size or industry (anonymized)
- Action plans on how to improve the capabilities of the current PKI
- Improve overall PKI performance

### Maturity Levels

The maturity model consists of several categories which are directly associated with the PKI and covers all aspects and activities (people, processes, technology). Based on the maturity model parts, the overall maturity level is determined as a single value representing the current state of capabilities and performance.

Each category can be separately assessed for its maturity level. Maturity levels are generally defined as follows:

| **Maturity level** | **Short description (general)**                                                                              |
| ------------------ | ------------------------------------------------------------------------------------------------------------ |
| **Initial**        | Unpredictable process with poor control and always reactive                                                  |
| **Basic**          | Process is characterized by each particular case or project and controls are often reactive                  |
| **Advanced**       | Process is characterized by organizational standards and controls are proactive                              |
| **Managed**        | Processes are measured and controlled, proactive approach                                                    |
| **Optimized**      | Continuous improvement of the processes and procedures, proactive approach for future technology improvement |

### Modules

There are 4 modules defined for the maturity model. Each of the module is focused on the specific parts of the PKI.

| Module         | Description                                                                                                                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Governance** | Consist of the leadership, overall structures, and processes to enable organization using the PKI in a sustainable way. In also consists of having strategy and objectives and proper decision making  |
| **Management** | Translates the governance into actions that support the PKI, management of the resources to maintain the required level of trust                                                                       |
| **Operations** | Includes day to day business as usual activities that lead to secure and future-proof PKI in accordance with the organization goals                                                                    |
| **Resources**  | Ensures that the activities related to the PKI are performed with a proper knowledge and experience, with enough capacities, and that it provides complete and accurate information to relying parties |

### Categories and weights

The following categories of the PKI maturity model are defined with the appropriate weight based on the applicability and importance:

| Category                          | Weight |
| --------------------------------- | -----: |
| **Strategy and vision**           |   5    |
| **Policies and documentation**    |   4    |
| **Compliance**                    |   2    |
| **Processes and procedures**      |   3    |
| **Key Management**                |   4    |
| **Certificate Management**        |   4    |
| **Interoperability**              |   2    |
| **Infrastructure Management**     |   2    |
| **Change Management and Agility** |   3    |
| **Sourcing**                      |   4    |
| **Knowledge and Training**        |   3    |
| **Monitoring and Auditing**       |   2    |
| **Automation**                    |   2    |
| **Awareness**                     |   3    |
| **Resilience**                    |   4    |

For more information on categories, please refer to the [Categories Maturity Evaluation](../categories/).

The weights of the categories are used to calculate the overall maturity level of the PKI.

### Modules and categories

Each module consists of specific categories related to them:

| Governance                                                                                                                   | Management                                                                                                                              | Operations                                                                                               | Resources                                                                   |
| ---------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| <ul><li>Strategy and vision</li><li>Policies and documentation</li><li>Compliance</li><li>Processes and procedures</li></ul> | <ul><li>Key Management</li><li>Certificate Management</li><li>Infrastructure Management</li><li>Change Management and Agility</li></ul> | <ul><li>Resilience</li><li>Automation</li><li>Interoperability</li><li>Monitoring and Auditing</li></ul> | <ul><li>Sourcing</li><li>Knowledge and Training</li><li>Awareness</li></ul> |

### Overall maturity level

Based on the nature of PKI part, these maturity levels are described accordingly. Overall maturity level is calculated as weighted average of maturity level of PKI categories.

There are defined the following overall maturity levels for the PKI Maturity Model:

| **Maturity level** | **Indicators**                                                                                                                                                                                                                                                                                                                                    | **Associated risks**                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **1 – Initial**    | <ul> <li>PKI is ad-hoc managed, reactive</li> <li>There are minimum processes and procedures, which are typically not followed and</li> <li>There is no approach how to address certificate related issues</li> <li>PKI does not take into account any industry standards or regulations</li> <li>Insufficient resources and knowledge</li> </ul> | <ul> <li>High probability of compromise</li> <li>High probability of operational issues</li> <li>No trust</li> </ul>       |
| **2 - Basic**      | <ul> <li>PKI is ad-hoc managed, often reactive</li> <li>There are defined processes and procedures which are followed</li> <li>PKI is not managed according industry standards and regulations</li> <li>Insufficient knowledge</li> </ul>                                                                                                         | <ul> <li>High probability of operational issues</li> <li>Medium probability of compromise</li> <li>No trust</li> </ul>     |
| **3 – Advanced**   | <ul> <li>Certificate services are not consistent</li> <li>Procedures are defined and followed</li> <li>CP and CPS partially exist</li> <li>Partially available resources and knowledge</li> </ul>                                                                                                                                                 | <ul> <li>Medium probability of operational issues</li> <li>Low probability of compromise</li> </ul>                        |
| **4 – Managed**    | <ul> <li>PKI is consistently managed</li> <li>Well defined CP and CPS for provided services</li> <li>Available skilled resources</li> <li>Documented processes and procedures to manage certificates and related keys</li> <li>Inconsistent approach to certificate related activities</li> </ul>                                                 | <ul> <li>Low probability of operational issues</li> <li>Low probability of compromise and loosing trust</li> </ul>         |
| **5 – Optimized**  | <ul> <li>Well defined CP and CPS</li> <li>Effective procedures for certificate management exists</li> <li>Resources with knowledge and experience available</li> <li>Consistent PKI with alignment to current practice and regulation</li> <li>Future proof</li> </ul>                                                                            | <ul> <li>Minimal probability of operational issues</li> <li>Minimal probability of compromise and loosing trust</li> </ul> |




