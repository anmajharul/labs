# Kruskal-Wallis Reproducibility Document

## Study Information

- **Project**: BUBT Mode-Choice Research — Chapter 4
- **Analysis**: Kruskal-Wallis H Test across Primary Transport Mode
- **Author**: Majharul Islam (BUBT)
- **Date**: 2026-08-11

---

## Dataset

| Field | Value |
|-------|-------|
| Raw file | `data/raw/Mode_shift_bubt.xlsx` |
| Sheet | `Form Responses 3` |
| Raw rows | 319 (plus 1 header) |
| Analysis N | Computed from data (see Data Audit) |
| SHA-256 | Run `certutil -hashfile data/raw/Mode_shift_bubt.xlsx SHA256` to verify |

---

## Analytical N and Grouping Variable

| Parameter | Value |
|-----------|-------|
| Grouping variable | Primary Mode of Transport |
| Expected groups | Public Bus, MRT (Metro Rail), Personal Motorcycle, Ridesharing (Uber/Pathao) |
| Analysis N | Computed from data (never hard-coded) |
| Exclusion criteria | Invalid mode, zero/negative cost, zero/negative travel time |

---

## Variables Tested

| Variable | Source | Derivation |
|----------|--------|-----------|
| One-Way Cost (BDT) | Column: "What is the TOTAL One-Way Cost of this trip?" | Direct |
| Access Time (min) | Column: "What is your total Access Time..." | Direct |
| In-Vehicle Time (min) | Column: "What is yout total In-Vehicle Time..." | Direct |
| Total Travel Time (min) | Derived | Access Time + In-Vehicle Time |

---

## Missing Value Treatment

| Rule | Action |
|------|--------|
| Invalid Primary Mode | Excluded |
| Missing numerical value | Excluded (per variable) |
| Zero or negative cost | Excluded |
| Zero or negative travel time | Excluded |
| Duplicate rows | **Retained** (potential legitimate ties) |

Every exclusion is logged in `docs/KRUSKAL_WALLIS_DATA_AUDIT.md`.
No silent removal.

---

## Ranking Method

| Parameter | Value |
|-----------|-------|
| Method | Average-rank tie handling |
| Formula | Rank positions averaged when two or more observations have equal values |
| Implementation | Manual (transparent) + scipy.stats.rankdata(method='average') cross-check |
| Scope | All N observations pooled before ranking |

---

## H Statistic Formula

$$H = \frac{12}{N(N+1)} \sum_{i=1}^{k} \frac{R_i^2}{n_i} - 3(N+1)$$

Where:
- N = total valid observations (all groups combined)
- k = number of groups = 4
- n_i = sample size of group i
- R_i = sum of ranks in group i

---

## Tie Correction Formula

$$C = 1 - \frac{\sum_j (t_j^3 - t_j)}{N^3 - N}$$

$$H_{corrected} = \frac{H_{uncorrected}}{C}$$

Where:
- t_j = frequency of observations with the same tied value
- Summation is over all distinct tied values

---

## p-value Method

| Parameter | Value |
|-----------|-------|
| Distribution | Chi-squared approximation |
| Degrees of freedom | df = k – 1 = 3 |
| Function (Python) | `scipy.stats.chi2.cdf(H_corrected, df=3)` |
| Function (R) | `pchisq(H_corrected, df=3, lower.tail=FALSE)` |
| Function (SPSS) | Internal chi-squared approximation |

---

## Post-Hoc Method

| Parameter | Value |
|-----------|-------|
| Test | Dunn's pairwise test |
| Number of comparisons | 6 (C(4,2)) |
| Multiple comparison correction | Bonferroni |
| Bonferroni formula | p_adj = min(p_raw × 6, 1.0) |
| Significance threshold | α_Bonferroni = 0.05/6 = 0.008333 |

---

## Effect Size Formula

$$\eta^2 = \frac{H - k + 1}{N - k}$$

| η² threshold | Interpretation |
|-------------|----------------|
| ≥ 0.14 | Large |
| 0.06 – 0.13 | Medium |
| 0.01 – 0.05 | Small |
| < 0.01 | Negligible |

**Citation**: Tomczak, M. & Tomczak, E. (2014). The need to report effect size
estimates revisited. An overview of some recommended measures of effect size.
*Trends in Sport Sciences*, 1(21), 19–25.

---

## Software Versions

| Software | Version |
|----------|---------|
| Python | ≥ 3.10 |
| pandas | ≥ 2.0 |
| numpy | ≥ 1.24 |
| scipy | ≥ 1.10 |
| openpyxl | ≥ 3.1 |
| R | ≥ 4.2 |
| readxl | ≥ 1.4 |
| SPSS | ≥ 25 (≥ 28 recommended for Dunn post-hoc) |

To check installed versions:
```bash
python -c "import pandas,numpy,scipy; print(pandas.__version__, numpy.__version__, scipy.__version__)"
```
```r
packageVersion("readxl")
R.version$version.string
```

---

## Reproduction Command

```bash
# Full Python pipeline (from project root):
cd Kruskal-Wallis-H-analysis
python analysis/python/26_master_run.py

# Individual scripts:
python analysis/python/00_data_audit.py
python analysis/python/13_kruskal_wallis.py
python analysis/python/14_kw_tie_correction.py
python analysis/python/15_dunn_bonferroni.py
python analysis/python/16_kw_effect_size.py
python analysis/python/17_kw_validation.py
python analysis/python/18_table4_13_reproduced.py

# Test suite:
python tests/test_kruskal_wallis.py

# R pipeline:
Rscript analysis/r/26_master_run.R
```

---

## Cross-Software Consistency Requirements

Results from Python and R must agree within:
- |ΔH| < 0.01 for H statistics
- |Δp| < 0.001 for p-values
- |Δz| < 0.01 for Dunn z-statistics

If SPSS results differ from Python/R by more than 0.01, the source must be
identified and documented in `docs/SPSS_KRUSKAL_WALLIS_LIMITATIONS.md`.

---

## Prohibited Practices

- Hard-coding any numerical result from Chapter 4
- Running analysis on a subset without documenting the subset criteria
- Using Mann-Whitney pairs as a substitute for Dunn's test without disclosure
- Reporting effect size without citing the threshold source
- Omitting any of the 6 pairwise Dunn comparisons
- Claiming "FULLY REPRODUCIBLE" unless all scripts run without error and
  all test_kruskal_wallis.py assertions pass

---

*Document version: 1.0 — 2026-08-11*
