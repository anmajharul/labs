# Q1 Reviewer Defense: Kruskal-Wallis Analysis — Chapter 4

**Role**: Hostile Q1 journal reviewer  
**Standard**: Transportation Research Part A / B / C or equivalent SSCI Q1 journal  
**Date**: 2026-08-11

---

> This review evaluates the Kruskal-Wallis H analysis from Chapter 4 of the
> BUBT student mode-choice research thesis. Every identified problem is assessed
> for severity and corrective action.

---

## Problem 1: Total Travel Time is a Derived Variable Without Documentation

**Evidence**:  
The dataset contains no column labelled "Total Travel Time." This variable is
computed as `Access Time + In-Vehicle Time`. Chapter 4 treats it as if it were
directly measured.

**Severity**: MAJOR

**Why a reviewer would object**:  
> "The authors refer to 'Total Travel Time' as if it is a directly measured variable.
> The methods section must explicitly state that TTT = AT + IVT and justify whether
> this derivation is appropriate. Ignoring egress time and waiting time may
> systematically underestimate actual travel time, invalidating comparisons between
> modes that have different transfer requirements."

**Exact correction**:  
Add to Methods: *"Total Travel Time was derived as the sum of Access Time and
In-Vehicle Time. This does not include waiting time, transfer time, or egress time.
The derivation is mode-agnostic and applied uniformly across all respondents.
Sensitivity analysis on alternative TTT definitions is recommended for future work."*

---

## Problem 2: Normality Assessment Language May Be Overconfident

**Evidence**:  
If Chapter 4 states that Shapiro-Wilk "proved" non-normality or "confirmed" that
KW is necessary, this is methodologically incorrect.

**Severity**: MAJOR

**Why a reviewer would object**:  
> "A Shapiro-Wilk p < 0.05 is evidence against the null hypothesis of normality,
> not proof of non-normality. Furthermore, the Shapiro-Wilk test is known to be
> overly sensitive for small samples and underpowered for large samples. The authors
> should acknowledge that KW was selected as a conservative non-parametric alternative,
> not because normality was definitively disproven."

**Exact correction**:  
Replace: *"Shapiro-Wilk results confirmed non-normality..."*  
With: *"Shapiro-Wilk tests indicated statistically significant departures from
normality in most groups (p < 0.05), providing justification for the non-parametric
Kruskal-Wallis H test as a more robust alternative to one-way ANOVA."*

---

## Problem 3: Levene's Variant Must Be Specified

**Evidence**:  
The Python pipeline uses the Brown-Forsythe (median-centered) Levene test.
SPSS defaults to mean-centered Levene. If these are mixed in reporting,
the F-statistics will not match.

**Severity**: MAJOR

**Why a reviewer would object**:  
> "The authors report Levene's test results but do not specify whether the
> mean-centered or median-centered (Brown-Forsythe) variant was used. These
> produce different F-statistics. This ambiguity makes the analysis unreproducible."

**Exact correction**:  
Specify in Methods: *"Variance homogeneity was assessed using the Brown-Forsythe
version of Levene's test (median-centered residuals), which is more robust to
non-normal distributions than the classical mean-centered variant
(Levene, 1960; Brown & Forsythe, 1974)."*

---

## Problem 4: Tie Correction Not Explicitly Reported

**Evidence**:  
Chapter 4 reports H statistics without documenting whether tie correction was applied.
For transportation data with many repeated cost and time values, ties are frequent
and the correction is material.

**Severity**: MAJOR

**Why a reviewer would object**:  
> "Kruskal-Wallis results with tied observations require a tie correction factor C.
> The authors report H statistics without stating whether correction was applied or
> what the correction factor was. For Access Time (many repeated integer minute values),
> the tie correction can materially affect H. This must be documented."

**Exact correction**:  
Add to Methods: *"The Kruskal-Wallis H statistic was corrected for ties using
C = 1 – Σ(t_j³ – t_j)/(N³ – N), where t_j is the frequency of each tied value.
The corrected statistic H_corrected = H_uncorrected / C was used for all reported
results and p-value calculations."*

Add to Table 4.13: a column for the tie correction factor C, or footnote it.

---

## Problem 5: Dunn Post-Hoc Test Not Identified by Name

**Evidence**:  
If Chapter 4 refers only to "pairwise comparisons" or "post-hoc tests" without
naming Dunn's test, this is insufficient for reproducibility.

**Severity**: MAJOR

**Why a reviewer would object**:  
> "Multiple pairwise post-hoc tests exist for Kruskal-Wallis (Dunn, Conover-Iman,
> Steel-Dwass). The authors must identify which test was used. Without this, the
> analysis cannot be reproduced."

**Exact correction**:  
State: *"Pairwise comparisons following significant Kruskal-Wallis results were
conducted using Dunn's test (Dunn, 1964) with Bonferroni correction
(adjusted α = 0.05/6 = 0.0083)."*

Citation: *Dunn, O.J. (1964). Multiple comparisons using rank sums. Technometrics, 6(3), 241-252.*

---

## Problem 6: Effect Size Not Reported

**Evidence**:  
Chapter 4 reports only H and p-values. A significant KW test with a trivial effect
size is not a meaningful finding.

**Severity**: MAJOR

**Why a reviewer would object**:  
> "Statistical significance with N=319 is nearly guaranteed for any non-trivial
> between-group difference. Without an effect size, the practical significance of
> the findings cannot be assessed. All four tests showing p < 0.001 does not tell
> the reader whether the differences are large or small."

**Exact correction**:  
Report η² = (H – k + 1)/(N – k) for each variable in Table 4.13.  
Cite thresholds: *"Effect sizes were interpreted using the thresholds proposed by
Tomczak & Tomczak (2014): η² ≥ 0.14 = large, ≥ 0.06 = medium, ≥ 0.01 = small."*

---

## Problem 7: Chapter 4 Reports ANOVA F and KW H for Same Variables

**Evidence**:  
Chapter 4 reports both ANOVA F and Kruskal-Wallis H for the same variables.
If ANOVA assumptions are violated (non-normality, heteroscedasticity), the ANOVA
F results should not be presented as primary findings.

**Severity**: MINOR

**Why a reviewer would object**:  
> "The authors present both ANOVA and Kruskal-Wallis results for the same comparison.
> If the data are non-normal (as indicated by Shapiro-Wilk), the ANOVA F is not a
> valid test. Presenting it alongside KW H implies equivalence, which is misleading."

**Exact correction**:  
Clarify the role of ANOVA in the analysis:  
*"One-way ANOVA results are reported for reference only. Because the normality
assumption was not met for several groups (Shapiro-Wilk p < 0.05), the
Kruskal-Wallis H test is the primary inferential test for all four variables."*

---

## Problem 8: Sample Size Justification

**Evidence**:  
N = 319 with a highly unbalanced design (120, 96, 62, 41).
No power analysis is reported.

**Severity**: MINOR

**Why a reviewer would object**:  
> "The smallest group (Ridesharing, n=41) provides limited statistical power for
> pairwise comparisons after Bonferroni correction. A post-hoc power analysis should
> confirm that the study was adequately powered to detect meaningful differences."

**Exact correction**:  
Add a power analysis footnote: *"With n_min = 41 and Bonferroni-adjusted α = 0.0083,
the study has [X]% power to detect a medium effect size (η² ≥ 0.06).
Power was computed using [cite package]."*

---

## Problem 9: H Statistics Are Reproducible — No Issue

**Evidence**:  
Reproduced H statistics from raw data match Chapter 4 reported values within
acceptable tolerance (see `docs/KRUSKAL_WALLIS_REPORTED_VS_REPRODUCED.md`).

**Severity**: N/A — PASS

**Note**:  
Any discrepancy > 5.0 should be investigated. See reproduced vs reported table.

---

## Problem 10: Causal Language Check

**Evidence**:  
Transportation mode-choice research frequently slips into causal language.

**Severity**: MINOR (if present)

**Why a reviewer would object**:  
> "Kruskal-Wallis is a test of distributional differences, not causation.
> Statements such as 'Primary Mode CAUSES higher costs' or 'MRT USE LEADS TO
> lower travel time' are not supported by a cross-sectional observational study."

**Exact correction**:  
Replace causal language:  
- "X causes Y" → "X is associated with Y"
- "Using MRT leads to..." → "MRT users report..."
- "Because of higher cost..." → "Groups with higher cost also show..."

---

## Problem 11: Ridesharing Group Size (n=41)

**Evidence**:  
Ridesharing has n = 41, which is the smallest group. For Dunn's pairwise tests,
this small n increases the standard error of the z-statistic.

**Severity**: MINOR

**Why a reviewer would object**:  
> "The Ridesharing group (n=41) is under-represented relative to Public Bus (n=120).
> This imbalance does not invalidate KW, but it reduces power for pairwise comparisons
> involving Ridesharing and should be acknowledged as a limitation."

**Exact correction**:  
Add to Limitations: *"The Ridesharing group was the smallest (n=41), which
limits statistical power for pairwise comparisons and may affect the
generalizability of findings for this transport mode."*

---

## Problem 12: Consistency Between Chapter 4 Text and Tables

**Evidence**:  
Any inconsistency between in-text H values and Table 4.13 values is a critical error.

**Severity**: CRITICAL (if present)

**Why a reviewer would object**:  
> "In-text reported H = 97.9 but Table 4.13 shows H = 97.911. While this may be
> rounding, reviewers scrutinize all numbers. Any inconsistency suggests
> cut-and-paste errors or multiple versions of the analysis."

**Exact correction**:  
Use consistent decimal precision throughout. If Table 4.13 reports three decimal
places, in-text references should use the same. Auto-generate Table 4.13 from
Python scripts to prevent manual transcription errors.

---

## Overall Assessment

| # | Issue | Severity | Status |
|---|-------|----------|--------|
| 1 | Total Travel Time not documented as derived | MAJOR | Requires correction |
| 2 | Normality language overconfident | MAJOR | Requires correction |
| 3 | Levene variant not specified | MAJOR | Requires correction |
| 4 | Tie correction not documented | MAJOR | Requires correction |
| 5 | Post-hoc test not named | MAJOR | Requires correction |
| 6 | Effect size absent | MAJOR | Requires correction |
| 7 | ANOVA presented without caveat | MINOR | Clarification needed |
| 8 | No power analysis | MINOR | Add footnote |
| 9 | H statistics reproducible | PASS | No action needed |
| 10 | Causal language risk | MINOR | Check text |
| 11 | Ridesharing small n | MINOR | Add to limitations |
| 12 | Text vs table consistency | CRITICAL | Verify all values |

---

## Recommended Actions Before Q1 Submission

1. **Must fix** (MAJOR/CRITICAL): Items 1–6, 12
2. **Should fix** (MINOR): Items 7–8, 10–11
3. **Run** `python tests/test_kruskal_wallis.py` — all tests must PASS
4. **Verify** `docs/KRUSKAL_WALLIS_REPORTED_VS_REPRODUCED.md` — all Status = PASS
5. **Auto-generate** Table 4.13 from `18_table4_13_reproduced.py`
6. **Add to Methods section** all corrections specified above

---

*Q1 Reviewer Defense prepared by: Majharul Islam (BUBT) — 2026-08-11*
