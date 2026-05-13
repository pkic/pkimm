---
date: "2026-05-13T7:00:00Z"
title: Extension structure
weight: 1
---

# Extension structure

An extension consists of three logical parts. The first defines what the extension is; the other two are the only mechanisms by which an extension can influence scoring:

- **Extension** — metadata describing the extension (id, version, compatibility, documentation, etc.).
- **Relevance** — extension-specific maturity criteria attached to selected PKI MM categories (see definition below).
- **Overlays** — weight adjustments attached to existing PKI MM categories or requirements (see definition below).

Scoring is defined separately from the extension structure to ensure that extensions remain purely descriptive and non-destructive to the core PKI MM calculation model — see [Scoring model](../scoring/) for the formulas.

**Relevance** is a set of **extension-specific maturity criteria** attached to selected PKI MM categories. Each relevance entry adds an additional category-level maturity signal (`RelLevel_C`) with its own weight (`RelWeight_C`). Relevance never adds new PKI MM requirements and never changes baseline scoring; it produces a separate **extension-scored** view of the same category.

**Overlay** is a **weight adjustment** attached to an existing PKI MM category or requirement. An overlay declares a `type` (`multiplier`, `addition`, or `override`) and a matching value, plus a `rationale`. Overlays change how strongly an item contributes to extension scoring; they never change baseline maturity values entered by users.

The full structure is described by the [extension JSON Schema](../extension.schema.json) and follows this shape:

```yaml
extension:
  id: "example"
  name: "Example Extension"
  version: "1.0.0"
  description: "Short summary of what the extension covers."
  compatibility:
    - "1.1.0"
  documentation: "https://example.org/extensions/example"
  floorScore: true

relevance:
  modules:
    - id: "G"
      categories:
        - id: "1"
          weight: 4
          guidance: |
            ...
          assessment: |
            ...
          references: |
            ...
          levels:
            - number: 1
              name: "1 - Initial"
              description: "..."
            # levels 2 through 5

overlays:
  modules:
    - id: "M"
      categories:
        - id: "7"
          type: "multiplier"
          multiplier: 1.5
          rationale: "..."
          requirements:
            - id: "1"
              type: "addition"
              addition: 1
              rationale: "..."
```

### Extension

Defines metadata describing the extension:

| Field           | Required | Description                                                                                                                                                                              |
|-----------------|:--------:|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `id`            | yes      | Short, stable identifier used in filenames and tooling.                                                                                                                                  |
| `name`          | yes      | Human-readable name.                                                                                                                                                                     |
| `version`       | yes      | Extension version in [Semantic Versioning](https://semver.org/) form (`MAJOR.MINOR.PATCH`).                                                                                              |
| `description`   | yes      | One- to two-sentence summary of what the extension covers.                                                                                                                               |
| `compatibility` | yes      | List of PKI MM model versions this extension is compatible with, e.g. `["1.1.0"]`. Tools use this to decide whether the extension applies to a given baseline assessment.                |
| `documentation` | yes      | URL to detailed documentation explaining the extension's purpose, scope, and design.                                                                                                     |
| `floorScore`    | no       | When `true`, the extension reports a floor score (minimum extension category level) alongside the aggregate score.                                                                       |

The extension block does not affect scoring directly.

#### Filename convention

Extension YAML files are named `<extension-id>-extension.yaml`, where `<extension-id>` matches the `extension.id` field. This keeps discovery and loading consistent across tools.

### Relevance

The **Relevance** section defines extension-specific maturity criteria for selected PKI MM categories.

Relevance behaves like an additional **category-level maturity signal**.

Each relevance entry **must include a relevance weight** because it participates directly in the category maturity calculation.

Each relevance entry should include:

- maturity levels (1--5)
- guidance text
- assessment instructions
- references
- relevance weight

Relevance does **not** add new PKI MM requirements or change baseline scoring.

<div class="border-start border-3 ps-3 my-3">

**Example - Relevance as additional maturity signal**

If a category has baseline maturity level `3.5` and the extension relevance level is `2` with relevance weight `2`, the extension contributes an additional weighted signal used during extension scoring.

</div>

### Overlays

The **Overlays** section defines weight adjustments applied to existing PKI MM items when calculating extension scores.

Overlays change **importance**, not maturity levels.

Each overlay **must declare a `type`** indicating how the adjustment is applied, the value field matching that type, and a **`rationale`** explaining why. The rationale provides transparency and helps reviewers understand the intent of the extension.

Overlays may be defined at:

- category level — applies when the category aggregates into the overall score
- requirement level — applies when the requirement aggregates into the category maturity level

An item (a specific category or a specific requirement) may carry **at most one overlay** within a given extension. Overlays are not stacked: there is no combining of multiple overlays on the same item, and extensions are evaluated independently of each other.

#### Overlay types

| `type`       | Value field  | Effective weight formula                       | Use when                                                            |
|--------------|--------------|------------------------------------------------|---------------------------------------------------------------------|
| `multiplier` | `multiplier` | `effective_weight = base_weight × multiplier`  | Scaling the item's importance up or down (for example `1.5×`).      |
| `addition`   | `addition`   | `effective_weight = base_weight + addition`    | Shifting the weight by a fixed amount.                              |
| `override`   | `override`   | `effective_weight = override`                  | Replacing the base weight entirely.                                 |

Exactly one value field is set per overlay, matching the declared `type`.

> 💡 **Concept**
>
> Overlays adjust how strongly an area influences extension scoring.
> They never modify the actual maturity levels entered by the user.

<div class="border-start border-3 ps-3 my-3">

**Example – Requirement multiplier**

Requirement weight = `2`  
Requirement multiplier = `1.5`

Effective requirement weight = `2 × 1.5 = 3`

</div>

<div class="border-start border-3 ps-3 my-3">

**Example – Addition**

Requirement weight = `2`  
Addition = `1`

Effective requirement weight = `2 + 1 = 3`

</div>

<div class="border-start border-3 ps-3 my-3">

**Example – Override**

Requirement weight = `2`  
Override = `5`

Effective requirement weight = `5` (base value replaced)

------------------------------------------------------------------------

</div>

