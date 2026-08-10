# Kruskal-Wallis: Chapter 4 Reported vs Reproduced

> **Important**: Chapter 4 values are used ONLY as validation targets.  
> All reproduced values are computed from raw data only.  
> No Chapter 4 figure was manually entered into any calculation.

---

## Group Size Validation

| Mode | Chapter 4 N | Computed N | Difference | Match |
|------|------------|-----------|-----------|-------|
| Public Bus | 120 | 120 | 0 | ✓ MATCH |
| MRT (Metro Rail) | 96 | 96 | 0 | ✓ MATCH |
| Personal Motorcycle | 62 | 62 | 0 | ✓ MATCH |
| Ridesharing (Uber/Pathao) | 41 | 41 | 0 | ✓ MATCH |
| **Total** | **319** | **319** | 0 | ✓ MATCH |

---

## Kruskal-Wallis H: Reported vs Reproduced

| Variable | Chapter 4 H | Reproduced H | ΔH | Chapter 4 p | Reproduced p | Status |
|----------|------------|-------------|-----|------------|-------------|--------|
| One-Way Cost (BDT) | 97.911 | 97.9107 | 0.0003 | < 0.001 | < 0.001 | **PASS** |
| Access Time (min) | 169.538 | 169.5376 | 0.0004 | < 0.001 | < 0.001 | **PASS** |
| In-Vehicle Time (min) | 110.929 | 110.9288 | 0.0002 | < 0.001 | < 0.001 | **PASS** |
| Total Travel Time (min) | 73.325 | 73.3255 | 0.0005 | < 0.001 | < 0.001 | **PASS** |

**All four variables: PASS** ✓

---

## Tie Correction Details

| Variable | N | N³–N | Σ(t³–t) | C | H_uncorrected | H_corrected |
|----------|---|------|---------|---|--------------|------------|
| One-Way Cost | 319 | 32,461,440 | 321,024 | 0.99011061 | 96.942461 | 97.9107 |
| Access Time | 319 | 32,461,440 | 209,208 | 0.99355518 | 168.444995 | 169.5376 |
| In-Vehicle Time | 319 | 32,461,440 | 42,870 | 0.99867936 | 110.782333 | 110.9288 |
| Total Travel Time | 319 | 32,461,440 | 26,688 | 0.99917786 | 73.265200 | 73.3255 |

---

## Mean Ranks by Group

### One-Way Cost (BDT)
| Mode | n | Rank Sum | Mean Rank |
|------|---|---------|----------|
| Public Bus | 120 | 13,350.00 | 111.250 |
| MRT (Metro Rail) | 96 | 17,896.00 | 186.417 |
| Personal Motorcycle | 62 | 8,910.00 | 143.710 |
| Ridesharing (Uber/Pathao) | 41 | 10,884.00 | 265.463 |

### Access Time (min)
| Mode | n | Rank Sum | Mean Rank |
|------|---|---------|----------|
| Public Bus | 120 | 20,541.50 | 171.179 |
| MRT (Metro Rail) | 96 | 22,578.00 | 235.188 |
| Personal Motorcycle | 62 | 2,756.50 | 44.460 |
| Ridesharing (Uber/Pathao) | 41 | 5,164.00 | 125.951 |

### In-Vehicle Time (min)
| Mode | n | Rank Sum | Mean Rank |
|------|---|---------|----------|
| Public Bus | 120 | 25,560.50 | 213.004 |
| MRT (Metro Rail) | 96 | 7,898.50 | 82.276 |
| Personal Motorcycle | 62 | 11,161.00 | 180.016 |
| Ridesharing (Uber/Pathao) | 41 | 6,420.00 | 156.585 |

### Total Travel Time (min)
| Mode | n | Rank Sum | Mean Rank |
|------|---|---------|----------|
| Public Bus | 120 | 25,967.00 | 216.392 |
| MRT (Metro Rail) | 96 | 11,382.50 | 118.568 |
| Personal Motorcycle | 62 | 8,062.00 | 130.032 |
| Ridesharing (Uber/Pathao) | 41 | 5,628.50 | 137.280 |

---

## Status Legend

| Status | Meaning |
|--------|---------|
| **PASS** | \|ΔH\| < 0.5 — within rounding/precision tolerance |
| **MINOR DISCREPANCY** | 0.5 ≤ \|ΔH\| < 5.0 — investigate |
| **MAJOR DISCREPANCY** | \|ΔH\| ≥ 5.0 — potential error |
| **NOT REPRODUCIBLE** | Calculation failed |

---

## Notes

- Reproduced H statistics match Chapter 4 reported values within **0.001** for all four variables.
- The tiny differences (e.g., ΔH = 0.0003 for Cost) are due to floating-point rounding
  in the final decimal place, not a methodological difference.
- Total Travel Time is a derived variable: AT + IVT (not measured directly).
- Tie correction C was applied to all variables.
- All computations independently verified in Python (manual + scipy), R (manual + kruskal.test), and Node.js.
- **FINAL VERDICT: ALL PASS** ✓

---

*Report generated: 2026-08-11*  
*Primary calculation: Python + Node.js*  
*Cross-validation: R kruskal.test()*
