# Categories Maturity Evaluation

For the evaluation of the maturity level of the category, the following formula is applied:

```
Category maturity level = floor ( ( Q1(score) + … + Qn(score) ) / n )
```

Where `n` is the number of questions in the category.

## List of categories

The following categories are recognized as part of the PKI maturity assessment:
- [Strategy and vision](./strategy-and-vision/pkimm-category-strategy-and-vision.md)
- Policies and documentation
- Compliance
- Processes and procedures
- Key Management
- Certificate Management
- Interoperability
- Infrastructure Management
- Change Management
- Sourcing
- Knowledge and Training
- Monitoring and Auditing
- Automation
- Visibility
- Awareness
- Resilience

## Example

```
Q1(score) = 3, Q2(score) = 4, Q3(score) = 1, Q4(score) = 5, Q5(score) = 5

Category maturity level = floor(3+4+1+5+5) / 5 = floor(3,6) = 3 (Advanced)
```