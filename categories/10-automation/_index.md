---
date: 2023-06-05T9:00:00Z
title: 10 - Automation
weight: 10

---

# 10 - Automation

## Overview

Automation of certificate management is the process of using technology to perform tasks with reduced human assistance. Automation is used to improve the efficiency of the PKI management and to reduce the risk of human error. Automation can be used to perform tasks that are repetitive, time-consuming, or difficult to perform manually.

On the other hand the automation can introduce new risks and challenges. The automation should be used only for tasks that are well-defined and that can be performed in a reliable way.

Justified, well-designed, and documented automation of certificate lifecycle management can significantly contribute to the efficiency of the PKI management while reducing the risk of human error. However, automation is not a silver bullet and should be controlled, monitored, and audited to prevent the risk of misuse.

## Category maturity levels description

| Maturity level    | Description                                                                                                                                                                                                   |
|:------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1 - Initial**   | No automation in place.                                                                                                                                                                                       |
| **2 - Basic**     | Automation is used for some tasks, however, it is not described and it is not reliable or repeatable.                                                                                                         |
| **3 - Advanced**  | Automation is used for most of the tasks, where it makes sense. Automation is described but not monitoring or audited.                                                                                        |
| **4 - Managed**   | Automation is used for all tasks, where it makes sense. Automation is described, followed and monitored or audited.                                                                                           |
| **5 - Optimized** | Automation is analyzed and designed to apply the best practices. Automation is described, followed, monitored, and audited. Procedures are in place to handle exceptions and incidents related to automation. |

## Requirements

|                                                  # | Requirement                                  | Weight |
|---------------------------------------------------:|----------------------------------------------|-------:|
|               [1](#process-automation-description) | Process automation description               |      3 |
| [2](#monitoring-and-auditing-of-automated-process) | Monitoring and auditing of automated process |      1 |
|            [3](#incidents-and-exceptions-handling) | Incidents and exceptions handling            |      1 |

## Details

### Process automation description

#### Guidance

Every automated certificate management process should be properly described and documented. The documentation should contain information relevant to the process automation and understanding the reasons for automation. Monitoring, auditing, and potential measures and controls would be ineffective without proper description and understanding of the automation process.

The description can include for example the following:
- Use-case or process to be automated
- Reasons for automation
- Description of the automation process
- Involved tools and technologies
- Monitoring and auditing requirements
- Potential measures and controls
- Exceptions
- Logging and reporting
- Any other relevant information and requirements

#### Assessment

The following is sample evidence that can be used to assess the requirement:
- Process automation description
- Interview with the process owner
- Interview with administrators
- Sample of automated process logs

#### References

N/A

### Monitoring and auditing of automated process

#### Guidance

The automated process of certificate management can cause significant damage if misused or misconfigured. The monitoring and auditing of the automated process is essential to prevent the risk of misuse and to detect any potential issues, inefficiencies, or exceptions.

The monitoring and auditing should be performed on a regular basis and should be aligned with the overall monitoring and auditing strategy of the organization.
It should provide sufficient information to detect any potential issues with the automated process. For successful detection or identification of issues, proper expectations should be based on the description of the automated process.

#### Assessment

Monitoring of automated processes should be supported by monitoring tools and technologies that can provide the necessary overview, reporting, and potential alerting in case of issues.
The following is sample evidence that can be used to assess the requirement:
- Documented monitoring and auditing measures
- Monitoring and auditing tools and technologies applied
- Sample report or dashboard from monitoring
- Interview with responsible personnel
- Simulate failure of the automated certificate management process and verify that the failure is detected and reported

#### References

N/A

### Incidents and exceptions handling

#### Guidance

No automation is perfect and covers everything. There can be edge cases and other situations that were not part of the initial analysis or were simply forgotten. Therefore, there will always be exceptions and incidents that will require manual intervention. The automated process should be able to handle such exceptions and incidents in a way that will not cause any significant damage or disruption to the service.

It may happen that some certificates are required to be handled manually and therefore the exception should be approved and documented. 

Handling of exceptional situations should be covered in the documentation, stating what should be done in case of an exception or incident:
- Communication of the exception
- Approval of the exception
- Incident handling and reporting
- Any other relevant information

The handling of exceptions should be tested and verified on a regular basis to ensure that the process is working as expected.

#### Assessment

The following is sample evidence that can be used to assess the requirement:
- Documented exceptions
- Interview with responsible personnel about how to handle exceptions or incidents

#### References

N/A
