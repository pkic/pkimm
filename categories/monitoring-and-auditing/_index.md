---
date: 2023-07-06T7:00:00Z
title: 12 - Monitoring and auditing
weight: 12

---

# 12 - Monitoring and auditing

Monitoring and auditing establish the necessary controls to detect and respond to security events and to provide evidence of compliance with the disclosed business practices.
The events and logs typically serves as a basis for incident response and forensic analysis in case of security incidents, however, they can also be used for other purposes, such as performance analysis, capacity planning, and troubleshooting.

Monitoring and auditing provide reasonable assurance that:
- Unauthorized PKI system usage is detected
- Critical high impact events are monitored
- Appropriate logs are collected and relevant issues are alerted
- The confidentiality and integrity of current and archived audit logs are maintained for the required period of time
- Audit logs are completely and confidentially archived in accordance with disclosed business practices
- Events and logs are reviewed periodically by authorized personnel

The outputs from the monitoring and auditing activities are typically used as inputs for the risk assessment and management activities, including incident response management and investigation of high impact events.

## Requirements

|                                                                                               # | Requirement                                                                               | Weight |
|------------------------------------------------------------------------------------------------:|-------------------------------------------------------------------------------------------|-------:|
|                     [1](#monitoring-events-and-logging-requirements-are-defined-and-documented) | Monitoring events and logging requirements are defined and documented                     |      4 |
|                                                     [2](#event-logs-from-systems-are-collected) | Event logs from systems are collected                                                     |      4 |
|                                          [3](#audit-trail-can-be-reconstructed-from-audit-logs) | Audit trail can be reconstructed from audit logs                                          |      5 |
|                              [4](#monitoring-of-operational-and-security-events-is-implemented) | Monitoring of operational and security events is implemented                              |      5 |
| [5](#critical-events-are-immediately-alerted-and-resolved-according-to-incident-response-plans) | Critical events are immediately alerted and resolved according to incident response plans |      3 |
|                                       [6](#review-of-events-and-logs-is-periodically-performed) | Review of events and logs is periodically performed                                       |      2 |

## Details

### Monitoring events and logging requirements are defined and documented

#### Guidance

The monitoring and logging requirements should be defined and documented in the certificate policy, certification practice statement, or other relevant documents. The requirements should be aligned with the overall PKI policies and statements, and should be based on the risk assessment and management activities.

The requirements can typically include:
- Events to be monitored
- Frequency of monitoring
- Logs to be collected
- Retention period for logs
- Audit trail requirements
- Audit log protection requirements
- Formatting and interpretation of logs (syslog, JSON, XML, CEF, etc.)
- And other relevant requirements

#### Assessment

- Documented monitoring and logging requirements
- Policies and procedures for monitoring and logging
- Review of records
- Interviews with personnel

#### References

- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)
- [ISO/IEC 20000 and related standards](https://www.iso.org/standard/70636.html)

### Event logs from systems are collected

#### Guidance

The event logs from systems should be collected and available for analysis, including correlation with other records. Centralized logging is recommended to ensure that the logs are collected and stored consistently. Solution like security information and event management (SIEM) can be used to collect and analyze the logs.

The availability of records for analysis depends on understanding logging format and interpretation of the information, therefore each system should provide logs in a consistent format that can be further processed and analyzed (or automated).

The event should contain sufficient information to identify the event, including:
- User identification
- Type of event
- Date and time
- Success or failure indication
- Origination of event
- Identity or name of affected data, system component, or resource
- Additional details

#### Assessment

- Logs are collected from systems
- Logs have a consistent format and can be further processed and analyzed
- Review of records and their formatting
- Review of configuration standards for logging
- Interviews with personnel to check the understanding of logging format and interpretation of the information

#### References

- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)
- [ISO/IEC 20000 and related standards](https://www.iso.org/standard/70636.html)
- [NIST - Guide to Computer Security Log Management](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf)

### Audit trail can be reconstructed from audit logs

#### Guidance

Audit logging should be implemented to ensure that the audit trail can be reconstructed from audit logs any time. Audit logs are typically recorder for any user executed events that are important for security of the PKI implementation. Audit logs should be stored in a secure location. The audit logs should be protected against unauthorized access, modification, and deletion.

Typically, the following events are important for security of the PKI implementation:
- All individual user accesses to sensitive data
- All actions taken by any individual with root or administrative privileges
- Access to all audit trails
- Invalid logical access attempts
- Use of and changes to identification and authentication mechanisms - including but not limited to creation of new accounts and elevation of privileges - and all changes, additions, or deletions to accounts with root or administrative privileges
- Initialization, stopping, or pausing of the audit logs
- Creation and deletion of system-level objects

#### Assessment

- Audit trail can be reconstructed from audit logs
- Audit logs are stored in a secure location
- Audit logs are protected against unauthorized access, modification, and deletion
- Review of records
- Interviews with personnel to understand the audit logging implementation

#### References

- [RFC 3647 - Internet X.509 Public Key Infrastructure Certificate Policy and Certification Practices Framework](https://tools.ietf.org/html/rfc3647)
- [NIST - Guide to Computer Security Log Management](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf)
- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)

### Monitoring of operational and security events is implemented

#### Guidance

Monitoring of operational and security events should be implemented to ensure that the PKI implementation is operating as expected and that the security events are detected and responded to in a timely manner. The monitoring should be implemented for all critical systems and components, including the CA, RA, OCSP, HSM, and other relevant systems.

Monitoring should be aligned with the monitoring and auditing requirements defined in the certificate policy, certification practice statement, or other relevant documents. The monitoring should be implemented to ensure that the requirements are met.

#### Assessment

- Monitoring of operational and security events is implemented according the requirements
- Review of monitoring implementation
- Review of monitoring events and alerts
- Interviews with personnel responsible for monitoring

#### References

- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)
- [ISO/IEC 20000 and related standards](https://www.iso.org/standard/70636.html)

### Critical events are immediately alerted and resolved according to incident response plans

#### Guidance

Critical events should be immediately alerted and resolved according to incident response plans. Monitoring implementation should ensure that the critical events are detected and alerted in a timely manner. This can be done manually or in automated way. 

#### Assessment

- Review of requirements for alerting on critical event
- Review of monitoring implementation
- Review of documentation on critical events
- Interviews with personnel to check the understanding of critical events and their handling

#### References

- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)
- [ISO/IEC 20000 and related standards](https://www.iso.org/standard/70636.html)

### Review of events and logs is periodically performed

#### Guidance

Logs and events should be reviewed frequently, preferably automatically, to determine security related issues, potential systems failure, identify anomalies or suspected activity. Regular review should be confirmed by authorized personnel and can proactively identify issues before they become problems.

The review of logs and events should be performed periodically and the frequency should be based on the risk assessment. Any potential issues should be reported and resolved according to the incident response plans.

#### Assessment

- Review of logs and events is performed periodically
- Review of logs and events is performed according to the requirements
- Review of logs and events is confirmed by authorized personnel
- Interview with personnel responsible for review of logs and events

#### References

- [ISO/IEC 27001 - Information security management systems](https://www.iso.org/standard/54534.html)
- [ISO/IEC 20000 and related standards](https://www.iso.org/standard/70636.html)
- [NIST - Guide to Computer Security Log Management](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf)
