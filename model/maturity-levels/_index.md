---
date: 2023-03-21T7:00:00Z
title: Levels description
weight: 3

---

# Levels description

Based on the nature of PKI part, these maturity levels are described accordingly. Overall maturity level is calculated as weighted average of maturity level of PKI categories.

There are defined the following overall maturity levels for the PKI Maturity Model:

| **Maturity level** | **Indicators**                                                                                                                                                                                                                                                                                                                                    | **Associated risks**                                                                                                       |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| **1 – Initial**    | <ul> <li>PKI is ad-hoc managed, reactive</li> <li>There are minimum processes and procedures, which are typically not followed and</li> <li>There is no approach how to address certificate related issues</li> <li>PKI does not take into account any industry standards or regulations</li> <li>Insufficient resources and knowledge</li> </ul> | <ul> <li>High probability of compromise</li> <li>High probability of operational issues</li> <li>No trust</li> </ul>       |
| **2 - Basic**      | <ul> <li>PKI is ad-hoc managed, often reactive</li> <li>There are defined processes and procedures which are followed</li> <li>PKI is not managed according industry standards and regulations</li> <li>Insufficient knowledge</li> </ul>                                                                                                         | <ul> <li>High probability of operational issues</li> <li>Medium probability of compromise</li> <li>No trust</li> </ul>     |
| **3 – Advanced**   | <ul> <li>Certificate services are not consistent</li> <li>Procedures are defined and followed</li> <li>CP and CPS partially exist</li> <li>Partially available resources and knowledge</li> </ul>                                                                                                                                                 | <ul> <li>Medium probability of operational issues</li> <li>Low probability of compromise</li> </ul>                        |
| **4 – Managed**    | <ul> <li>PKI is consistently managed</li> <li>Well defined CP and CPS for provided services</li> <li>Available skilled resources</li> <li>Documented processes and procedures to manage certificates and related keys</li> <li>Inconsistent approach to certificate related activities</li> </ul>                                                 | <ul> <li>Low probability of operational issues</li> <li>Low probability of compromise and loosing trust</li> </ul>         |
| **5 – Optimized**  | <ul> <li>Well defined CP and CPS</li> <li>Effective procedures for certificate management exists</li> <li>Resources with knowledge and experience available</li> <li>Consistent PKI with alignment to current practice and regulation</li> <li>Future proof</li> </ul>                                                                            | <ul> <li>Minimal probability of operational issues</li> <li>Minimal probability of compromise and loosing trust</li> </ul> |

```mermaid
classDiagram
    direction LR

    class PKIMM["PKI maturity levels"]{
        Initial
        Basic
        Advanced
        Managed
        Optimized
    }
    class Initial_Indicators["Initial level indicators"]{
        PKI is ad-hoc managed, reactive
        There are minimum processes and procedures, which are typically not followed and 
        There is no approach how to address certificate related issues
        PKI does not take into account any industry standards or regulations
        Insufficient resources and knowledge
    }
    class Initial_Risks["Initial level risks"]{
        High probability of compromise
        High probability of operational issues
        No trust
    }
    class Basic_Indicators["Basic level indicators"]{
        PKI is ad-hoc managed, often reactive
        There are defined processes and procedures which are followed
        PKI is not managed according industry standards and regulations
        Insufficient knowledge
    }
    class Basic_Risks["Basic level risks"]{
        High probability of operational issues
        Medium probability of compromise
        No trust
    }
    class Advanced_Indicators["Advanced level indicators"]{
        Certificate services are not consistent
        Procedures are defined and followed
        CP and CPS partially exist
        Partially available resources and knowledge
    }
    class Advanced_Risks["Advanced level risks"]{
        Medium probability of operational issues
        Low probability of compromise
    }
    class Managed_Indicators["Managed level indicators"]{
        PKI is consistently managed
        Well defined CP and CPS for provided services
        Available skilled resources
        Documented processes and procedures to manage certificates and related keys
        Inconsistent approach to certificate related activities
    }
    class Managed_Risks["Managed level risks"]{
        Low probability of operational issues
        Low probability of compromise and loosing trust
    }
    class Optimized_Indicators["Optimized level indicators"]{
        Well defined CP and CPS
        Effective procedures for certificate management exists
        Resources with knowledge and experience available
        Consistent PKI with alignment to current practice and regulation
        Future proof
    }
    class Optimized_Risks["Optimized level risks"]{
        Minimal probability of operational issues
        Minimal probability of compromise and loosing trust
    }
    
    PKIMM <-- Initial_Indicators
    Initial_Indicators -- Initial_Risks
    PKIMM <-- Basic_Indicators
    Basic_Indicators -- Basic_Risks
    PKIMM <-- Advanced_Indicators
    Advanced_Indicators -- Advanced_Risks
    PKIMM <-- Managed_Indicators
    Managed_Indicators -- Managed_Risks
    PKIMM <-- Optimized_Indicators
    Optimized_Indicators -- Optimized_Risks
```