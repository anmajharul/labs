# Kruskal-Wallis H Analysis — Chapter 4

**BUBT Mode-Choice Research | Fully Reproducible Statistical Pipeline**

---

## Overview

This project implements a completely reproducible Kruskal-Wallis H analysis for
Chapter 4 of the BUBT student mode-choice research thesis.

**Analysis variables:**
- One-Way Cost (BDT)
- Access Time (min)
- In-Vehicle Time (min)
- Total Travel Time (min) — *derived: AT + IVT*

**Grouping variable:** Primary Mode (Public Bus, MRT, Personal Motorcycle, Ridesharing)

---

## Quick Results

| Variable | H (corrected) | C | df | p | η² | Status |
|----------|--------------|---|----|----|-----|--------|
| One-Way Cost | **97.9107** | 0.9901 | 3 | < 0.001 | 0.3013 (Large) | ✓ PASS |
| Access Time | **169.5376** | 0.9936 | 3 | < 0.001 | 0.5287 (Large) | ✓ PASS |
| In-Vehicle Time | **110.9288** | 0.9987 | 3 | < 0.001 | 0.3426 (Large) | ✓ PASS |
| Total Travel Time | **73.3255** | 0.9992 | 3 | < 0.001 | 0.2233 (Large) | ✓ PASS |

**FINAL VERDICT: FULLY REPRODUCIBLE** ✓

---

## Project Structure

```
Kruskal-Wallis-H-analysis/
├── data/
│   └── raw/Mode_shift_bubt.xlsx         ← RAW DATA (only computational source)
│
├── analysis/
│   ├── python/
│   │   ├── kw_utils.py                  ← Core statistical engine (manual implementation)
│   │   ├── 00_data_audit.py             ← Data quality audit
│   │   ├── 13_kruskal_wallis.py         ← Main KW analysis
│   │   ├── 14_kw_tie_correction.py      ← Detailed tie correction
│   │   ├── 15_dunn_bonferroni.py        ← Dunn post-hoc (all 6 pairs)
│   │   ├── 16_kw_effect_size.py         ← Effect size (η²)
│   │   ├── 17_kw_validation.py          ← Chapter 4 validation
│   │   ├── 18_table4_13_reproduced.py   ← Table 4.13 reproduction
│   │   └── 26_master_run.py             ← Run everything
│   │
│   ├── r/
│   │   ├── kw_utils.R                   ← R utility functions
│   │   ├── 13_kruskal_wallis.R          ← R KW analysis
│   │   ├── 14_kw_tie_correction.R       ← R tie correction
│   │   ├── 15_dunn_bonferroni.R         ← R Dunn post-hoc
│   │   ├── 16_kw_effect_size.R          ← R effect size
│   │   ├── 17_kw_validation.R           ← R validation
│   │   └── 26_master_run.R              ← Run everything (R)
│   │
│   └── spss/
│       ├── 12_kruskal_wallis.sps        ← SPSS KW syntax
│       ├── 13_dunn_posthoc.sps          ← SPSS post-hoc options
│       └── 14_kw_validation.sps         ← SPSS validation
│
├── results/
│   ├── python/                          ← Python output CSVs
│   ├── r/                               ← R output CSVs
│   ├── tables/Table_4_13_REPRODUCED.md  ← Reproduced table
│   └── spss/                            ← SPSS output
│
├── tests/
│   └── test_kruskal_wallis.py           ← Automated test suite (9 test blocks)
│
├── docs/
│   ├── KRUSKAL_WALLIS_DATA_AUDIT.md
│   ├── KRUSKAL_WALLIS_REPORTED_VS_REPRODUCED.md
│   ├── KRUSKAL_WALLIS_REPRODUCIBILITY.md
│   ├── KRUSKAL_WALLIS_Q1_REVIEW.md
│   └── SPSS_KRUSKAL_WALLIS_LIMITATIONS.md
│
├── requirements.txt
└── README.md
```

---

## Reproduction Commands

### Python (Primary)
```bash
# From project root:
python analysis/python/26_master_run.py

# Or step by step:
python analysis/python/00_data_audit.py
python analysis/python/13_kruskal_wallis.py
python analysis/python/14_kw_tie_correction.py
python analysis/python/15_dunn_bonferroni.py
python analysis/python/16_kw_effect_size.py
python analysis/python/17_kw_validation.py
python analysis/python/18_table4_13_reproduced.py
```

### Tests
```bash
python tests/test_kruskal_wallis.py
```

### R (Cross-validation)
```r
Rscript analysis/r/26_master_run.R
```

---

## Key Design Principles

1. **Raw data is the ONLY computational source** — Chapter 4 H values are never used in calculation
2. **Manual implementation + software cross-check** — H is calculated from scratch and validated via scipy/kruskal.test()
3. **Full tie correction** — C = 1 – Σ(t³–t)/(N³–N) applied and documented for all variables
4. **All 6 Dunn pairs reported** — no pair is omitted regardless of significance
5. **Effect size documented** — η² with Tomczak & Tomczak (2014) thresholds and citation
6. **No silent exclusions** — every data decision is logged

---

## Dependencies

```
pandas>=2.0, numpy>=1.24, scipy>=1.10, openpyxl>=3.1
```

Install: `pip install -r requirements.txt`

---

## Author

Majharul Islam | BUBT | 2026-08-11
