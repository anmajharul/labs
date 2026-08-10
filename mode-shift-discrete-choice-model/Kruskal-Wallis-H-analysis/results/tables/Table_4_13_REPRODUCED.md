# Table 4.13 REPRODUCED

> **Note**: This table is reproduced entirely from raw data.  
> It does **not** overwrite the original Chapter 4 Table 4.13.  
> No Chapter 4 figures were manually entered. All values were computed.

---

## Table 4.13 REPRODUCED — KW H Analysis Summary

| Variable | ANOVA F | ANOVA p | KW H (corrected) | df | KW p | η² | Interpretation |
|----------|---------|---------|---------|------|------|-----|----------------|
| One-Way Cost (BDT) | *see Python script* | < 0.001 | **97.9107** | 3 | < 0.001 | **0.3013** | Large |
| Access Time (min) | *see Python script* | < 0.001 | **169.5376** | 3 | < 0.001 | **0.5287** | Large |
| In-Vehicle Time (min) | *see Python script* | < 0.001 | **110.9288** | 3 | < 0.001 | **0.3426** | Large |
| Total Travel Time (min) | *see Python script* | < 0.001 | **73.3255** | 3 | < 0.001 | **0.2233** | Large |

> **Note**: ANOVA F values require `18_table4_13_reproduced.py` (scipy).  
> Effect size η² formula: (H – k + 1)/(N – k) where k=4, N=319.  
> Thresholds: Tomczak & Tomczak (2014): Large ≥ 0.14.

---

## Dunn Post-Hoc Results (Bonferroni Correction)

### One-Way Cost (BDT)

| Comparison | Mean Rank A | Mean Rank B | z | p_raw | p_Bonf | Sig? |
|-----------|------------|------------|---|-------|--------|------|
| MRT vs Personal Motorcycle | 186.417 | 143.710 | 2.8561 | 0.0043 | 0.0257 | **Yes** |
| MRT vs Public Bus | 186.417 | 111.250 | 5.9814 | < 0.001 | < 0.001 | **Yes** |
| MRT vs Ridesharing | 186.417 | 265.463 | -4.6167 | < 0.001 | < 0.001 | **Yes** |
| Personal Motorcycle vs Public Bus | 143.710 | 111.250 | 2.2614 | 0.0237 | 0.1424 | No |
| Personal Motorcycle vs Ridesharing | 143.710 | 265.463 | -6.5907 | < 0.001 | < 0.001 | **Yes** |
| Public Bus vs Ridesharing | 111.250 | 265.463 | -9.2890 | < 0.001 | < 0.001 | **Yes** |

**Chapter 4 claim verification:**
- ✓ Ridesharing significantly differs from all others (3/3 confirmed)
- ✓ Public Bus vs Personal Motorcycle: NOT significant (p_Bonf = 0.1424)

### Access Time (min)

| Comparison | Mean Rank A | Mean Rank B | z | p_raw | p_Bonf | Sig? |
|-----------|------------|------------|---|-------|--------|------|
| MRT vs Personal Motorcycle | 235.188 | 44.460 | 12.7333 | < 0.001 | < 0.001 | **Yes** |
| MRT vs Public Bus | 235.188 | 171.179 | 5.0846 | < 0.001 | < 0.001 | **Yes** |
| MRT vs Ridesharing | 235.188 | 125.951 | 6.3688 | < 0.001 | < 0.001 | **Yes** |
| Personal Motorcycle vs Public Bus | 44.460 | 171.179 | -8.8129 | < 0.001 | < 0.001 | **Yes** |
| Personal Motorcycle vs Ridesharing | 44.460 | 125.951 | -4.4036 | < 0.001 | 0.0001 | **Yes** |
| Public Bus vs Ridesharing | 171.179 | 125.951 | 2.7196 | 0.0065 | 0.0392 | **Yes** |

### In-Vehicle Time (min)

| Comparison | Mean Rank A | Mean Rank B | z | p_raw | p_Bonf | Sig? |
|-----------|------------|------------|---|-------|--------|------|
| MRT vs Personal Motorcycle | 82.276 | 180.016 | -6.5085 | < 0.001 | < 0.001 | **Yes** |
| MRT vs Public Bus | 82.276 | 213.004 | -10.3580 | < 0.001 | < 0.001 | **Yes** |
| MRT vs Ridesharing | 82.276 | 156.585 | -4.3213 | < 0.001 | 0.0001 | **Yes** |
| Personal Motorcycle vs Public Bus | 180.016 | 213.004 | -2.2883 | 0.0221 | 0.1327 | No |
| Personal Motorcycle vs Ridesharing | 180.016 | 156.585 | 1.2629 | 0.2066 | 1.0000 | No |
| Public Bus vs Ridesharing | 213.004 | 156.585 | 3.3838 | 0.0007 | 0.0043 | **Yes** |

### Total Travel Time (min)

| Comparison | Mean Rank A | Mean Rank B | z | p_raw | p_Bonf | Sig? |
|-----------|------------|------------|---|-------|--------|------|
| MRT vs Personal Motorcycle | 118.568 | 130.032 | -0.7632 | 0.4453 | 1.0000 | No |
| MRT vs Public Bus | 118.568 | 216.392 | -7.7490 | < 0.001 | < 0.001 | **Yes** |
| MRT vs Ridesharing | 118.568 | 137.280 | -1.0879 | 0.2766 | 1.0000 | No |
| Personal Motorcycle vs Public Bus | 130.032 | 216.392 | -5.9891 | < 0.001 | < 0.001 | **Yes** |
| Personal Motorcycle vs Ridesharing | 130.032 | 137.280 | -0.3906 | 0.6961 | 1.0000 | No |
| Public Bus vs Ridesharing | 216.392 | 137.280 | 4.7436 | < 0.001 | < 0.001 | **Yes** |

**Chapter 4 claim verification:**
- ✓ Public Bus vs MRT: Significant (confirmed)
- ✓ Public Bus vs Personal Motorcycle: Significant (confirmed)
- ✓ Public Bus vs Ridesharing: Significant (confirmed)
- ✓ MRT vs Personal Motorcycle: NOT significant (confirmed)
- ✓ MRT vs Ridesharing: NOT significant (confirmed)
- ✓ Personal Motorcycle vs Ridesharing: NOT significant (confirmed)

**All 6 Chapter 4 TTT claims: CONFIRMED ✓**

---

## Footnotes

1. Bonferroni correction: m = C(4,2) = 6 pairs; adjusted α = 0.05/6 = 0.00833
2. Effect size η² formula: Tomczak & Tomczak (2014)
3. Large effect threshold: η² ≥ 0.14 (Tomczak & Tomczak, 2014)
4. All H statistics are tie-corrected: H_cor = H_unc / C
5. p-values use chi-squared approximation with df = 3

---

*Table generated: 2026-08-11*  
*Script: `analysis/python/18_table4_13_reproduced.py`*  
*Data source: `data/raw/Mode_shift_bubt.xlsx`*
