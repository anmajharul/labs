# SPSS Kruskal-Wallis Limitations

## Overview

This document classifies every component of the Kruskal-Wallis analysis pipeline
by its availability and accuracy in native SPSS syntax.

**Classification scheme:**

| Status | Meaning |
|--------|---------|
| **Exact** | SPSS produces bit-identical results to Python/R |
| **Equivalent** | SPSS uses the same method; minor precision difference (< 0.01) |
| **Approximate** | SPSS uses a related but different method; results may differ |
| **Not Available** | SPSS cannot compute this natively without Python plugin |

---

## Component-by-Component Classification

### 1. Kruskal-Wallis H Statistic

**Classification: Equivalent**

SPSS `NPAR TESTS /K-W` procedure:
- Uses the same formula: H = [12 / N(N+1)] × Σ(R_i²/n_i) – 3(N+1)
- Applies tie correction automatically
- Tie correction formula: C = 1 – Σ(t_j³–t_j) / (N³–N)
- Does NOT display C separately in output
- H_corrected matches Python/R within numerical precision (|Δ| < 0.01)

**Potential discrepancy sources:**
- SPSS may handle missing values differently if `ANALYSIS` vs `LISTWISE` is used
- SPSS uses floating-point representation that may cause tiny rounding differences

---

### 2. Tie Correction Factor C

**Classification: Not Available**

SPSS applies tie correction internally but does not report:
- The value of C
- Σ(t_j³–t_j)
- N³–N
- H_uncorrected separately

**Workaround:** Use Python `14_kw_tie_correction.py` or R `14_kw_tie_correction.R`
for full documented tie correction calculation.

---

### 3. Dunn Post-Hoc Test

**Classification: Approximate (SPSS < 28) / Exact (SPSS ≥ 28)**

**SPSS < 28:**
- Native `NPAR TESTS` does NOT provide Dunn's pairwise post-hoc
- The only built-in alternative is Mann-Whitney U for each pair
- **Critical difference**: Mann-Whitney uses pair-wise ranks (within the two groups)
  while Dunn's test uses pooled ranks (from all N observations)
- This produces DIFFERENT z-statistics and p-values
- Classification: **Approximate** (direction of significance usually matches, but
  exact values differ — see Python `15_dunn_bonferroni.py` for exact results)

**SPSS ≥ 28:**
- `NPTESTS /INDEPENDENT KRUSKAL_WALLIS(COMPARE=PAIRWISE)` provides Dunn-style
  pairwise comparisons with Bonferroni correction
- Classification: **Exact**
- Syntax: see `analysis/spss/13_dunn_posthoc.sps` Option C

---

### 4. Bonferroni Correction

**Classification: Exact (SPSS ≥ 28) / Not Available (SPSS < 28 — must apply manually)**

For SPSS ≥ 28 `NPTESTS COMPARE=PAIRWISE`:
- Bonferroni threshold = 0.05 / m where m = k(k-1)/2 = 6
- Identical to Python/R implementation
- Classification: **Exact**

For SPSS < 28 with Mann-Whitney pairs:
- User must apply Bonferroni adjustment manually (α = 0.05/6 = 0.00833)
- SPSS does not auto-adjust — Classification: **Not Available** (must be manual)

---

### 5. Effect Size (η²)

**Classification: Not Available**

SPSS `NPAR TESTS /K-W` does not compute:
- η² (eta-squared)
- ε² (epsilon-squared)
- Any other KW effect size

**Workaround:** Compute manually:
```
η² = (H – k + 1) / (N – k)
```
Or use Python `16_kw_effect_size.py` / R `16_kw_effect_size.R`.

---

### 6. Shapiro-Wilk Normality Test

**Classification: Exact**

SPSS `EXAMINE /PLOT NPPLOT` produces Shapiro-Wilk W and p-value.
- Results match scipy `shapiro()` within rounding
- Both use the Royston (1995) algorithm
- Slight differences may appear for large n (> 50) due to approximation methods

---

### 7. Levene's Test (Homogeneity of Variance)

**Classification: Equivalent (with caveat)**

SPSS `ONEWAY /STATISTICS HOMOGENEITY` uses:
- **Mean-centered Levene** by default (classical Levene)
- Python/R default in this pipeline uses **median-centered** (Brown-Forsythe)

**These will produce different F-statistics** because they use different centering.
Both are documented in Python script `13_kruskal_wallis.py`.

To match SPSS in Python/R, use `center='mean'` in Levene test.
To match the more robust option in SPSS, use `Analyze > Explore > Levene Mean`
vs `Levene Median` option.

**Classification: Equivalent** if same centering is used; **Approximate** if different.

---

### 8. Group Descriptive Statistics

**Classification: Exact**

SPSS `MEANS /CELLS MEAN COUNT STDDEV MEDIAN MIN MAX` produces identical descriptive
statistics to Python/R.

---

## Summary Table

| Component | SPSS < 28 | SPSS ≥ 28 | Python | R |
|-----------|-----------|-----------|--------|---|
| KW H (corrected) | Equivalent | Equivalent | **Exact** | **Exact** |
| Tie correction C | Not Available | Not Available | **Exact** | **Exact** |
| Tie table | Not Available | Not Available | **Exact** | **Exact** |
| Dunn post-hoc | Approximate¹ | **Exact** | **Exact** | **Exact** |
| Bonferroni correction | Not Available² | **Exact** | **Exact** | **Exact** |
| Effect size η² | Not Available | Not Available | **Exact** | **Exact** |
| Shapiro-Wilk | **Exact** | **Exact** | **Exact** | **Exact** |
| Levene (mean) | **Exact** | **Exact** | **Exact** | **Exact** |
| Levene (median/BF) | Approximate³ | Approximate³ | **Exact** | **Exact** |

**Notes:**
1. Mann-Whitney used instead of Dunn — different ranking basis
2. Must apply Bonferroni manually (0.05/6 = 0.00833)
3. SPSS default uses mean-centering; pipeline uses median-centering (Brown-Forsythe)

---

## Recommendation

For Q1 journal reproducibility:
- **Primary analysis**: Python (fully transparent manual calculation)
- **Cross-validation**: R `kruskal.test()` (matches within 0.001)
- **SPSS**: Use for reporting if your institution requires it, but note the
  limitations above in your Methods section
- **Effect size**: Python or R only (SPSS cannot compute η² natively)
- **Dunn post-hoc**: Python or R (exact); SPSS ≥ 28 `NPTESTS` (equivalent)

---

*Document generated: 2026-08-11*
*Author: Majharul Islam (BUBT)*
