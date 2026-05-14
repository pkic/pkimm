---
date: "2026-05-13T7:00:00Z"
title: Scoring model
weight: 2
---

# Scoring model

This page covers how the framework computes scores for an extension: the two assessment modes (full vs self), the per-stage formulas, and an end-to-end worked example. It is intended for tool implementers and reviewers — readers focused on what an extension *is* should start with [Extension structure](../structure/).

## Assessment

Extension scoring supports two assessment modes.  
Both modes use the same scoring model, but differ in how category maturity levels are obtained.

| Aspect                 | Full assessment              | Self-assessment               |
|------------------------|------------------------------|-------------------------------|
| Requirement details    | Used                         | Not used                      |
| Category level source  | Calculated from requirements | Provided directly by the user |
| Category weights       | Used                         | Used                          |
| Scoring math (overall) | Same                         | Same                          |

> 💡 **Concept**
>
> The difference between assessment modes exists only at the **requirement aggregation stage**.
> Once a category maturity level exists, extension scoring behaves identically.

### Full assessment

In full assessment mode:

- Requirement maturity levels are provided by the user.
- Category maturity levels are calculated as a weighted average of requirement levels (using requirement weights, optionally adjusted by overlays).
- Overall PKI MM maturity is calculated as a weighted average of category maturity levels (using category weights, optionally adjusted by overlays).

> 🔧 **Implementation detail**
>
> Requirement overlays affect category maturity calculation only (because requirements are part of the full assessment).
> Category overlays affect the overall maturity calculation.

### Self-assessment

In self-assessment mode:

- Requirement details are not evaluated.
- Users provide category maturity levels directly.
- Overall PKI MM maturity is calculated as a weighted average of category maturity levels (using category weights, optionally adjusted by overlays).

> 🔧 **Implementation detail**
>
> Requirement overlays are applied to the model weights but do not depend on requirement-level user inputs in self-assessment.
> Category overlays apply normally.

<div class="border-start border-3 ps-3 my-3">

**Example – Why scoring stays consistent**

Both modes compute the overall score from category maturity levels and category weights using the same formula.
The only difference is how category maturity levels are obtained:

- Full assessment: derived from requirement answers
- Self-assessment: entered directly by the user

</div>

## Scoring model details

The PKI MM calculates maturity in two stages:

1. **Category maturity level** is calculated from requirements as a weighted average of requirement maturity levels.
2. **Overall PKI MM maturity** is calculated as a weighted average of category levels.

Extensions reuse this same model to ensure consistency. For a single extension, the order of operations is:

1. **Apply requirement overlays** to derive effective requirement weights.
2. **Aggregate to category maturity** as a weighted average of requirement levels using the effective requirement weights — this produces `Level_C` and the corresponding `WeightSum_C`.
3. **Blend with relevance** (if defined for the category) to produce `ExtensionCategoryLevel_C` per the formula in [Extension category level](#extension-category-level).
4. **Apply category overlays** to derive `effective_category_weight`.
5. **Aggregate to the extension score** as a weighted average of `ExtensionCategoryLevel_C` values using `effective_category_weight` per the formula in [Extension progress score](#extension-progress-score).

In self-assessment mode, step 2 is replaced by direct user input of `Level_C`; the remaining steps are identical.

Each extension is scored independently — see the [Extension framework FAQ](../../faq/#extension-framework) on composition across extensions.

> 🔧 **Normative Rule**
>
> Extensions MUST NOT modify the baseline category level calculation or the PKI MM aggregation model.
>
> Extensions may influence scoring only through:
> - relevance definitions (including relevance weights)
> - overlays (weight adjustments applied to PKI MM items)

### Extension category level

The extension category level blends the baseline category maturity with the extension relevance maturity.

Let:

- `Level_C` be the baseline PKI MM category level
- `WeightSum_C` be the baseline aggregation weight of the category, calculated as the sum of effective requirement weights after overlays. This value depends only on the PKI MM model and the extension's overlays and does **not** depend on user-selected maturity levels.
- `RelLevel_C` be the relevance maturity level
- `RelWeight_C` be the relevance weight

The extension category level is calculated as:

```
ExtensionCategoryLevel_C =

(Level_C × WeightSum_C + RelLevel_C × RelWeight_C)
------------------------------------
(WeightSum_C + RelWeight_C)
```

If relevance is not defined for a category:

`ExtensionCategoryLevel_C = Level_C`

> 💡 **Concept**
>
> `WeightSum_C` represents the baseline aggregation strength of the category.
> It is derived from requirement weights and overlays and does **not** represent the PKI MM category weight (`effective_category_weight`)
used during overall score aggregation.
>
> Relevance behaves like an additional weighted maturity signal added
> at the category aggregation stage.

<div class="border-start border-3 ps-3 my-3">

**Example – Extension category level**

Baseline category level (`Level_C`) = `3.6`  
Baseline aggregation weight (`WeightSum_C`) = `7.5`  
Relevance level (`RelLevel_C`) = `2`  
Relevance weight (`RelWeight_Cz`) = `2`  

ExtensionCategoryLevel = `(3.6×7.5 + 2×2) / (7.5 + 2)`  
= `(27 + 4) / 9.5`  
= `31 / 9.5`  
= `3.26`

</div>

### Category weight

Category weights remain explicit values defined by the PKI MM model. An extension may adjust a category weight by attaching a category-level overlay; `effective_category_weight` is then derived from the base weight using the overlay's `type` per the [Overlay types](#overlay-types) table.

If no category-level overlay is defined, `effective_category_weight = base_category_weight`.

> 🔧 **Implementation detail**
>
> Requirement overlays influence category maturity calculation only.
> Category overlays influence overall aggregation.

### Extension progress score

The extension progress score is calculated as a weighted average of extension category levels:

```
ExtensionScore =
Σ(ExtensionCategoryLevel_C × effective_category_weight)
-------------------------------------------------------
Σ(effective_category_weight)
```

<div class="border-start border-3 ps-3 my-3">

**Example – Extension score**

Category `G.1` level = `2.53` with weight `4`  
Category `G.2` level = `3.0` with weight `6`  

ExtensionScore = `(2.53×4 + 3×6) / (4 + 6)`  
= `(10.12 + 18) / 10`  
= `2.81`

</div>

### Extension floor score (optional)

When `extension.floorScore` is set to `true`, the extension reports an additional **floor score** representing the lowest extension category level encountered:

`ExtensionFloor = minimum(ExtensionCategoryLevel_C)`

The floor score highlights weakest-link maturity risks within the extension's scope.

The floor score is scoped to a single extension. When multiple extensions are active simultaneously, each extension computes and reports its **own** floor independently. Extensions are not combined into a single aggregate floor — see the [Extension framework FAQ](../../faq/#extension-framework) on composition across extensions.

### Extension-weighted PKI MM score

Extensions may also provide a PKI MM view using extension-adjusted category weights:

```
ExtensionWeightedPKIMM =

Σ(Level_C × effective_category_weight)
--------------------------------------
Σ(effective_category_weight)
```

This recalculates baseline PKI MM maturity using extension emphasis while preserving baseline maturity values.

### Example – Scoring behavior in full assessment vs self-assessment

The extension scoring formula is identical in both assessment modes.
The only difference is how the baseline category maturity level (`Level_C`) is obtained.

- In **full assessment**, `Level_C` is calculated from requirement maturity values.
- In **self-assessment**, the user selects `Level_C` directly (1–5) based on the category maturity description.

Because the input resolution differs, the numerical result may differ slightly, but the scoring behavior remains consistent.

<div class="border-start border-3 ps-3 my-3">

**Example — Full assessment**

Category maturity derived from requirements:

Baseline category level (`Level_C`) = `3.6`  
Baseline aggregation weight (`WeightSum_C`) = `7.5`  
Relevance level (`RelLevel_C`) = `2`  
Relevance weight (`RelWeight_C`) = `2`

ExtensionCategoryLevel = `(3.6×7.5 + 2×2) / (7.5 + 2)`  
= `(27 + 4) / 9.5`  
= `31 / 9.5`  
= `3.26`

</div>

<div class="border-start border-3 ps-3 my-3">

**Example — Self-assessment**

In the self-assessment application, the user selects a discrete maturity level:

Baseline category level (`Level_C`) = **`4`**  
Baseline aggregation weight (`WeightSum_C`) = `7.5`  
Relevance level (`RelLevel_C`) = `2`  
Relevance weight (`RelWeight_C`) = `2`

ExtensionCategoryLevel = `(4×7.5 + 2×2) / (7.5 + 2)`  
= `(30 + 4) / 9.5`  
= `34 / 9.5`  
= `3.58`

</div>

#### Consistency clarification

Full assessment and self-assessment use the **same scoring model**. The difference in results comes only from the source of the category level:

- full assessment → calculated weighted average
- self-assessment → user-selected maturity level (1–5)

Extension scoring always operates at the **category aggregation stage**, which guarantees consistent behavior across both assessment modes.

### End-to-end worked example

This example walks the full scoring pipeline for **one extension** across **one category** in full-assessment mode, illustrating each step in the order described in [Scoring model details](#scoring-model-details).

**Setup.** A category `C` with three requirements (`r1`, `r2`, `r3`), to which the extension applies one requirement-level overlay, one relevance entry, and one category-level overlay:

| Item                              | Base value  | Overlay              | Effective value                     |
|-----------------------------------|-------------|----------------------|-------------------------------------|
| Requirement `r1` weight           | `3`         | `multiplier 1.5`     | `3 × 1.5 = 4.5`                     |
| Requirement `r2` weight           | `2`         | —                    | `2`                                 |
| Requirement `r3` weight           | `1`         | —                    | `1`                                 |
| User-selected `r1` level          | `4`         | —                    | `4`                                 |
| User-selected `r2` level          | `3`         | —                    | `3`                                 |
| User-selected `r3` level          | `4`         | —                    | `4`                                 |
| Relevance level (`RelLevel_C`)    | `2`         | —                    | `2`                                 |
| Relevance weight (`RelWeight_C`)  | `2`         | —                    | `2`                                 |
| Category base weight              | `4`         | `multiplier 1.25`    | `4 × 1.25 = 5`                      |

**Step 1 — Apply requirement overlays.** Effective requirement weights: `4.5`, `2`, `1`. Total `WeightSum_C = 7.5`.

**Step 2 — Aggregate to baseline category level.**

```
Level_C = (4 × 4.5 + 3 × 2 + 4 × 1) / 7.5
        = (18 + 6 + 4) / 7.5
        = 28 / 7.5
        = 3.73
```

**Step 3 — Blend with relevance.**

```
ExtensionCategoryLevel_C = (3.73 × 7.5 + 2 × 2) / (7.5 + 2)
                         = (28.00 + 4) / 9.5
                         = 32.00 / 9.5
                         = 3.37
```

**Step 4 — Apply the category overlay.** `effective_category_weight = 4 × 1.25 = 5`.

**Step 5 — Aggregate into the extension score.** Assume this category contributes alongside one other category `C'` with `ExtensionCategoryLevel = 4.10` and `effective_category_weight = 3`:

```
ExtensionScore = (3.37 × 5 + 4.10 × 3) / (5 + 3)
               = (16.85 + 12.30) / 8
               = 29.15 / 8
               = 3.64
```

**Floor score** (if `floorScore: true`): `min(3.37, 4.10) = 3.37`.

> 💡 **What this illustrates**
>
> - The requirement overlay (`r1` × 1.5) lifts the influence of `r1` on `Level_C`, but doesn't change `r1`'s maturity value (still `4`).
> - Relevance acts as one additional weighted maturity signal at the category level; with `WeightSum_C = 7.5` versus `RelWeight_C = 2`, the relevance signal contributes about 21% of the blended category level.
> - The category overlay (`× 1.25`) lifts this category's influence on the overall extension score, but doesn't change `ExtensionCategoryLevel_C` itself.
> - Baseline PKI MM scoring is untouched throughout.


