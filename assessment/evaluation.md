---
date: 2023-06-17T7:00:00Z
title: Evaluation
weight: 3
---

# Evaluation

The evaluation is the process of analyzing the results of the assessment and determining the maturity level of the PKI implementation.

The maturity level is determined for each category, module, and eventually for the overall PKI implementation.

## Category maturity evaluation

First, each category is evaluated individually to provide the following data:
- Category maturity level
- Category maturity percentage
- Overview of the assessed requirements

Maturity level of each category is calculated as the weighted average of requirements maturity levels within the category.
See [Categories description](../categories/) for more information about category requirements. 

## Module maturity evaluation

After each category is evaluated, the maturity level of each module is determined based on the maturity level of the categories.
Each category is evaluated individually to provide the following data:
- Module maturity level
- Module maturity percentage
- Cumulative overview of the assessed requirements

Maturity level of each module is calculated as the weighted average of categories maturity levels within the module.
See [Modules](../model/maturity-modules/) for more information about modules.

## PKI maturity evaluation

Eventually, the overall maturity level of the PKI implementation is determined based on the maturity levels of categories.
See [Levels](../model/maturity-levels/) for more information about maturity levels.

> **Info**
> The overall maturity level of the PKI implementation is calculated based on the maturity levels of the categories, not modules. Modules provide a different perspective on the maturity of the PKI implementation, but their are not used to calculate the overall maturity level.
{class="callout-info"}

