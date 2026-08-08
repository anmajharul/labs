# Statistical Methodology: Mann-Whitney U Test

## 1. Overview

The **Mann-Whitney U test** (also called the Wilcoxon rank-sum test) is a non-parametric test used to determine whether there is a statistically significant difference between two independent groups on an ordinal or continuous outcome. It does not assume normality.

In this analysis, we compare **Male** vs **Female** respondents on five ordinal (1–5 Likert scale) travel-experience variables.

---

## 2. Mathematical Derivation

### 2.1 Ranking

Given two independent samples:
- Group 1 (Male): x₁, x₂, ..., x_{n₁}  (n₁ observations)
- Group 2 (Female): y₁, y₂, ..., y_{n₂}  (n₂ observations)
- Total: N = n₁ + n₂

Pool all N observations and assign ranks 1 through N. Tied values receive the **average rank** of the positions they occupy.

### 2.2 Rank Sums

- R₁ = sum of ranks for Group 1 (Male)
- R₂ = sum of ranks for Group 2 (Female)

**Identity check:** R₁ + R₂ = N(N + 1) / 2

### 2.3 U Statistics

U₁ = n₁ · n₂ + n₁(n₁ + 1)/2 − R₁

U₂ = n₁ · n₂ + n₂(n₂ + 1)/2 − R₂

**Identity check:** U₁ + U₂ = n₁ · n₂

The **reported U** is typically U = min(U₁, U₂), though some software reports U₁ (for the first group).

### 2.4 Expected Value Under H₀

Under the null hypothesis (identical distributions):

μ_U = n₁ · n₂ / 2

### 2.5 Variance and Tie Correction

Without ties:

Var(U) = n₁ · n₂ · (N + 1) / 12

With ties (Likert data always has ties), the **tie-corrected variance** is:

Var(U) = (n₁ · n₂ / 12) × [(N + 1) − Σ(tᵢ³ − tᵢ) / (N(N − 1))]

where:
- tᵢ = number of observations sharing rank i (the size of each tie group)
- The summation is over all unique values (tie groups)

σ_U = √Var(U)

### 2.6 Z-Statistic

**Without continuity correction:**

Z = (U − μ_U) / σ_U

**With continuity correction** (shift U by 0.5 toward the mean):

Z_CC = (U − μ_U ± 0.5) / σ_U

The correction adds 0.5 if U < μ_U, subtracts 0.5 if U > μ_U.

### 2.7 P-Value (Two-Tailed)

p = 2 × P(Z ≥ |z|) = 2 × Φ(−|z|)

where Φ is the standard normal CDF.

### 2.8 Effect Size

**r** = |Z| / √N

Interpretation (Cohen, 1988):
| r | Interpretation |
|---|---|
| < 0.10 | Negligible |
| 0.10 – 0.29 | Small |
| 0.30 – 0.49 | Medium |
| ≥ 0.50 | Large |

**Rank-biserial correlation:**

r_rb = 1 − (2U) / (n₁ · n₂)

This gives the proportion of favorable pairs minus unfavorable pairs.

---

## 3. Software Convention Differences

### 3.1 U vs W

| Software | Statistic Reported | Name |
|---|---|---|
| Python (scipy) | U for the first sample | `mannwhitneyu().statistic` |
| R (wilcox.test) | W = rank sum of the first sample | `$statistic` |
| SPSS | U = min(U₁, U₂) | Mann-Whitney U |

**Converting R's W to U:** U₁ = W − n₁(n₁ + 1)/2

### 3.2 Continuity Correction

| Software | Default CC |
|---|---|
| Python scipy `use_continuity=True` | Yes |
| R `correct=TRUE` | Yes |
| SPSS (recent versions) | Yes |

This pipeline computes **both** Z_no_CC and Z_CC.

### 3.3 Tie Handling

All three software packages include tie correction in the asymptotic Z calculation. The formula used is the standard one shown in Section 2.5.

### 3.4 Asymptotic vs Exact

For N > 20 (our N = 319), the asymptotic normal approximation is appropriate. Exact methods are computationally expensive and unnecessary here.

---

## 4. Multiple Testing

With five simultaneous tests, the family-wise error rate (FWER) increases. We report:

1. **Unadjusted p-values** (as in the thesis)
2. **Bonferroni correction**: p_adj = min(p × k, 1.0) where k = 5
3. **Holm step-down procedure**: More powerful than Bonferroni while still controlling FWER

The thesis does not appear to address multiplicity. For Q1-journal defense, both adjusted and unadjusted p-values should be reported.

---

## 5. Assumptions

1. **Independence**: Male and Female observations are independent (different respondents) ✓
2. **Ordinal scale**: Likert 1–5 ratings are ordinal ✓
3. **Same shape**: MWU tests whether one group tends to have larger values; it does not require identical distributions, but interpretation as a location shift requires similar shapes
4. **Sample size**: N = 319 (n₁ = 214, n₂ = 105) is sufficient for asymptotic approximation ✓

---

## 6. References

- Mann, H. B., & Whitney, D. R. (1947). On a test of whether one of two random variables is stochastically larger than the other. *Annals of Mathematical Statistics*, 18(1), 50–60.
- Wilcoxon, F. (1945). Individual comparisons by ranking methods. *Biometrics Bulletin*, 1(6), 80–83.
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum.
- Bergmann, R., Ludbrook, J., & Spooren, W. P. J. M. (2000). Different outcomes of the Wilcoxon-Mann-Whitney test from different statistics packages. *The American Statistician*, 54(1), 72–77.
