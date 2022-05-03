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
|--------------------|--------------------------------------------------------------------------------------------------------------|
| **Initial**        | Unpredictable process with poor control and always reactive                                                  |
| **Basic**          | Process is characterized by each particular case or project and controls are often reactive                  |
| **Advanced**       | Process is characterized by organizational standards and controls are proactive                              |
| **Managed**        | Processes are measured and controlled, proactive approach                                                    |
| **Optimized**      | Continuous improvement of the processes and procedures, proactive approach for future technology improvement |

### Categories and weights

The following categories of the PKI maturity model are defined with the appropriate weight based on the applicability and importance:

| **Part**                       | **Short description**                                                                                                               | **Weight** |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|------------|
| **Strategy and vision**        | Responsibility matrix for the PKI and strategy for the PKI management over time to respond on trends and risks                      | 5          |
| **Policies and documentation** | Formal policies and practice statements for PKI services and formal management of all agreement between parties involved in the PKI | 4          |
| **Compliance**                 | Adherence to standards and applicable regulations and requirements for the PKI and trust services                                   | 2          |
| **Processes and procedures**   | Processes and procedures related to PKI management tasks and operational activities                                                 | 3          |
| **Key Management**             | Key management policy and procedures related to PKI cryptographic keys and its lifecycle                                            | 4          |
| **Certificate Management**     | Certificate management policy and lifecycle                                                                                         | 4          |
| **Interoperability**           | Application of interoperable protocols and standards, avoidance to vendor lock                                                      | 2          |
| **Infrastructure Management**  | Infrastructure setup and high availability of the PKI services, environments                                                        | 1          |
| **Change Management**          | Change management process, accepting requests and staging process                                                                   | 3          |
| **Sourcing**                   | Availability of skilled resources to manage PKI                                                                                     | 5          |
| **Knowledge and Training**     | Education of people and continuously gathering required knowledge                                                                   | 2          |
| **Monitoring and Auditing**    | Measure the PKI attributes, provide evidence, monitoring and alerting of relevant issues, incident response management              | 2          |
| **Automation**                 | Automation of certificate management, tooling                                                                                       | 1          |
| **Visibility**                 | Visibility on certificates issued and used in the infrastructure and application to manage its compliance                           | 2          |
| **Awareness**                  | Working with the certificates, awareness about the PKI in the organization                                                          | 3          |
| **Resilience**                 | Quickly respond to potential attack and unavailability of PKI services or other related resources                                   | 4          |

### Overall maturity level

Based on the nature of PKI part, these maturity levels are described accordingly. Overall maturity level is calculated as weighted average of maturity level of PKI parts.

There are defined the following overall maturity levels for the PKI Maturity Model:

| **Maturity level** | **Indicators** | **Associated risks**  |
|--------------------|----------------|-----------------------|
| **1 – Initial**    | <ul> <li>PKI is ad-hoc managed, reactive</li> <li>There are minimum processes and procedures, which are typically not followed and</li> <li>There is no approach how to address certificate related issues</li> <li>PKI does not take into account any industry standards or regulations</li> <li>Insufficient resources and knowledge</li> </ul> | <ul> <li>High probability of compromise</li> <li>High probability of operational issues</li> <li>No trust</li> </ul> |
| **2 - Basic**      | <ul> <li>PKI is ad-hoc managed, often reactive</li> <li>There are defined processes and procedures which are followed</li> <li>PKI is not managed according industry standards and regulations</li> <li>Insufficient knowledge</li> </ul> | <ul> <li>High probability of operational issues</li> <li>Medium probability of compromise</li> <li>No trust</li> </ul> |
| **3 – Advanced**   | <ul> <li>Certificate services are not consistent</li> <li>Procedures are defined and followed</li> <li>CP and CPS partially exist</li> <li>Partially available resources and knowledge</li> </ul> | <ul> <li>Medium probability of operational issues</li> <li>Low probability of compromise</li> </ul> |
| **4 – Managed**    | <ul> <li>PKI is consistently managed</li> <li>Well defined CP and CPS for provided services</li> <li>Available skilled resources</li> <li>Documented processes and procedures to manage certificates and related keys</li> <li>Inconsistent approach to certificate related activities</li> </ul> | <ul> <li>Low probability of operational issues</li> <li>Low probability of compromise and loosing trust</li> </ul> |
| **5 – Optimized**  | <ul> <li>Well defined CP and CPS</li> <li>Effective procedures for certificate management exists</li> <li>Resources with knowledge and experience available</li> <li>Consistent PKI with alignment to current practice and regulation</li> <li>Future proof</li> </ul> | <ul> <li>Minimal probability of operational issues</li> <li>Minimal probability of compromise and loosing trust</li> </ul> |




