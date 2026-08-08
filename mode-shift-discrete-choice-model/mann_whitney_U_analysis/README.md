# Chapter 4 — Mann-Whitney U Reproducibility Package

## Overview

This package provides a fully reproducible Mann-Whitney U analysis pipeline
for Chapter 4, Table 4.4 of the transportation research thesis. It compares
**Male** vs **Female** respondents on five ordinal (1–5 Likert) travel-experience
variables.

## Variables Tested

| # | Variable | Raw Column |
|---|---|---|
| 1 | Safety: Harassment/Security | How safe do you feel regarding harassment...? |
| 2 | Reliability | How reliable is your current mode...? |
| 3 | Safety: Road Accidents | How safe do you feel regarding road accidents...? |
| 4 | Comfort | How would you rate the physical comfort...? |
| 5 | Crowding | How crowded is the vehicle usually? |

## Dataset

- **Source**: `data/Mode_shift_bubt.xlsx` (319 respondents × 30 columns)
- **Gender**: Text labels (`Male` = 214, `Female` = 105)
- **See**: `data/DATA_DICTIONARY.md` for full column mapping

## Quick Start

### Python

```bash
# From the mann_whitney_U_analysis directory:
.python\python.exe analysis_python.py
```

### R

```r
# Requires: readxl
Rscript analysis_R.R
```

### SPSS

Open `analysis_SPSS.sps` in SPSS after loading the Excel data.

### Automated Tests

```bash
.python\python.exe test_mann_whitney.py
```

## What the Pipeline Produces

### All intermediate statistics (per variable):
- R₁, R₂ (rank sums) with identity check
- U₁, U₂ with identity check
- U = min(U₁, U₂)
- μ_U (expected mean under H₀)
- Tie correction (Σ(tᵢ³−tᵢ) per tie group)
- σ_U (tie-corrected standard deviation)
- Z (without and with continuity correction)
- Two-tailed p-value (manual + scipy cross-validation)
- Effect size r = |Z|/√N
- Rank-biserial correlation
- Statistical decision

### Output files:
| File | Description |
|---|---|
| `outputs/mann_whitney_full_results.csv` | Complete results with all intermediates |
| `outputs/mann_whitney_table4_4.csv` | Table 4.4 format |
| `outputs/Table_4_4_reproduced.xlsx` | Publication-ready Excel |
| `outputs/reported_vs_reproduced.csv` | Thesis vs computed comparison |
| `outputs/tie_correction_details.csv` | Tie groups per variable |
| `outputs/descriptive_statistics.csv` | N, mean, median, SD, frequencies |
| `outputs/multiple_testing.csv` | Raw + Bonferroni + Holm p-values |
| `outputs/cross_software_comparison.csv` | Python vs R vs SPSS |
| `outputs/test_results.txt` | Automated test results |

### Figures:
| File | Description |
|---|---|
| `figures/fig_*_distribution.png` | Grouped bar charts (5 variables) |
| `figures/fig_boxplots_all_variables.png` | Box + jitter plots |
| `figures/fig_effect_size_forest.png` | Effect size forest plot |
| `figures/fig_mean_rank_comparison.png` | Mean rank comparison |

## Three Independent Implementations

1. **Python** (`analysis_python.py` + `mann_whitney_utils.py`)
   - Complete from-scratch calculation with scipy cross-validation
   - All intermediate statistics preserved
   - Automated test suite

2. **R** (`analysis_R.R`)
   - Independent implementation using base R
   - Cross-validated against `wilcox.test()`
   - Exports `outputs/mann_whitney_results_R.csv`

3. **SPSS** (`analysis_SPSS.sps`)
   - Syntax for NPAR TESTS /MANN-WHITNEY
   - Requires manual execution in SPSS

## Documentation

| File | Description |
|---|---|
| `docs/statistical_methodology.md` | Mathematical derivation and software conventions |
| `docs/q1_audit_report.md` | 16-point Q1 journal reviewer checklist |
| `data/DATA_DICTIONARY.md` | Variable definitions and column mapping |

## Reproducibility

The pipeline independently computes ALL statistics from the raw data. No thesis
values are hard-coded into the calculations. The `reported_vs_reproduced.csv`
file compares computed values against the thesis manuscript.

## Requirements

Python: pandas ≥ 2.0, numpy ≥ 1.24, scipy ≥ 1.10, openpyxl, matplotlib
R: readxl
SPSS: Version 25+
