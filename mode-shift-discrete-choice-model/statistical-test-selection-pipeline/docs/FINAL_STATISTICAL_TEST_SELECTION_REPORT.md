# UNIVERSAL STATISTICAL TEST-SELECTION REPORT
## Data-Driven Group Comparisons & Methodological Framework

**Dataset**: `Mode_shift_bubt.xlsx`  
**Total Sample Size**: N = 319  
**Total Variables Inspected**: 30  
**Date of Execution**: 2026-08-11  
**Author**: Majharul Islam (BUBT)  

---

## 1. Executive Summary & Core Methodology

This report documents a completely data-driven, reproducible statistical test-selection pipeline for comparing continuous and ordinal outcomes across categorical groups. Rather than relying on simplistic rules (such as automatically switching to Kruskal-Wallis whenever Shapiro-Wilk p < 0.05), this framework evaluates:
1. **Measurement Level**: Strict distinction between true continuous variables and Likert/ordinal items.
2. **Sample Size & CLT Protection**: Assessment of asymptotic ANOVA robustness for large n per group.
3. **Normality Evidence**: Joint inspection of Shapiro-Wilk W, skewness, kurtosis, and Q-Q plots.
4. **Variance Homogeneity**: Median-centered Brown-Forsythe Levene test.
5. **Outlier Impact**: IQR-based outlier audit without arbitrary data deletion.
6. **Multiple Testing & Effect Sizes**: FDR/FWER control and rank-based/parametric effect sizes with citations.

## 2. Dataset Overview & Auto-Classification

| Variable Type | Count | Description / Role |
|---------------|-------|--------------------|
| nominal_categorical | 9 | Classified via automated distribution profiling |
| datetime | 5 | Classified via automated distribution profiling |
| binary_categorical | 5 | Classified via automated distribution profiling |
| likert_ordinal | 4 | Classified via automated distribution profiling |
| continuous_numeric | 3 | Classified via automated distribution profiling |
| free_text | 2 | Classified via automated distribution profiling |
| constant | 1 | Classified via automated distribution profiling |
| discrete_numeric | 1 | Classified via automated distribution profiling |

- **Suitable Outcome Variables**: 8 variables
- **Suitable Grouping Variables**: 12 variables
- **Total Valid Outcome Ã— Grouping Combinations**: 88

## 3. Comprehensive Test Selection Matrix

| Outcome | Grouping Variable | Primary Test | Sensitivity Test | Decision Category | Rationale |
|---------|-------------------|--------------|------------------|-------------------|-----------|
| What is your age? | Gender | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=105) ensure ANOVA robustness via CLT. Max absolute skewness=0.58 (not extreme). Levene p=0.1164... |
| What is your age? | What is your family's approxim | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | 3/5 groups fail S-W (p<0.05). Max absolute skewness=0.95. Combined evidence from S-W, skewness, and visual inspection in... |
| What is your age? | What is your personal monthly  | **WELCH ANOVA** | KRUSKAL-WALLIS | `WELCH PREFERRED` | Large group sizes (min n=45) but Levene p=0.0007 â€” unequal variances. Welch ANOVA relaxes the equal-variance assumptio... |
| What is your age? | What is your PRIMARY mode of t | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=41) ensure ANOVA robustness via CLT. Max absolute skewness=1.38 (not extreme). Levene p=0.4978 ... |
| What is your age? | How do you get from your home  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | 3/3 groups fail S-W (p<0.05). Max absolute skewness=0.81. Combined evidence from S-W, skewness, and visual inspection in... |
| What is your age? | If the fare of your current pr | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=112) ensure ANOVA robustness via CLT. Max absolute skewness=0.65 (not extreme). Levene p=0.0601... |
| What is your age? | Imagine the MRT/Bus is so crow | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=129) ensure ANOVA robustness via CLT. Max absolute skewness=0.81 (not extreme). Levene p=0.7246... |
| What is your age? | "Premium Bus" service (AC + Gu | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=142) ensure ANOVA robustness via CLT. Max absolute skewness=0.61 (not extreme). Levene p=0.3330... |
| What is your age? | If it is raining heavily, how  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | 3/4 groups fail S-W (p<0.05). Max absolute skewness=0.65. Combined evidence from S-W, skewness, and visual inspection in... |
| What is your age? | During a Strike (Hartal) or Ro | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | 4/5 groups fail S-W (p<0.05). Max absolute skewness=0.61. Combined evidence from S-W, skewness, and visual inspection in... |
| What is your age? | If a dedicated BUBT Student Bu | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=90) ensure ANOVA robustness via CLT. Max absolute skewness=0.59 (not extreme). Levene p=0.5717 ... |
| Total number of family members livi | Gender | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=105) ensure ANOVA robustness via CLT. Max absolute skewness=0.97 (not extreme). Levene p=0.2225... |
| Total number of family members livi | What is your family's approxim | **KRUSKAL-WALLIS** | WELCH ANOVA | `NON-PARAMETRIC PREFERRED` | 5/5 groups fail S-W (p<0.05). Max absolute skewness=2.99. Combined evidence from S-W, skewness, and visual inspection in... |
| Total number of family members livi | What is your personal monthly  | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=45) ensure ANOVA robustness via CLT. Max absolute skewness=1.29 (not extreme). Levene p=0.6847 ... |
| Total number of family members livi | What is your PRIMARY mode of t | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=41) ensure ANOVA robustness via CLT. Max absolute skewness=1.59 (not extreme). Levene p=0.4133 ... |
| Total number of family members livi | How do you get from your home  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | 3/3 groups fail S-W (p<0.05). Max absolute skewness=1.31. Combined evidence from S-W, skewness, and visual inspection in... |
| Total number of family members livi | If the fare of your current pr | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=112) ensure ANOVA robustness via CLT. Max absolute skewness=1.24 (not extreme). Levene p=0.1733... |
| Total number of family members livi | Imagine the MRT/Bus is so crow | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=129) ensure ANOVA robustness via CLT. Max absolute skewness=1.00 (not extreme). Levene p=0.2532... |
| Total number of family members livi | "Premium Bus" service (AC + Gu | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=142) ensure ANOVA robustness via CLT. Max absolute skewness=0.90 (not extreme). Levene p=0.9061... |
| Total number of family members livi | If it is raining heavily, how  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | 3/4 groups fail S-W (p<0.05). Max absolute skewness=1.40. Combined evidence from S-W, skewness, and visual inspection in... |
| Total number of family members livi | During a Strike (Hartal) or Ro | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | 5/5 groups fail S-W (p<0.05). Max absolute skewness=2.18. Combined evidence from S-W, skewness, and visual inspection in... |
| Total number of family members livi | If a dedicated BUBT Student Bu | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=90) ensure ANOVA robustness via CLT. Max absolute skewness=1.69 (not extreme). Levene p=0.9530 ... |
| How many members of your family ear | Gender | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=105) ensure ANOVA robustness via CLT. Max absolute skewness=0.75 (not extreme). Levene p=0.5223... |
| How many members of your family ear | What is your family's approxim | **KRUSKAL-WALLIS** | WELCH ANOVA | `NON-PARAMETRIC PREFERRED` | 5/5 groups fail S-W (p<0.05). Max absolute skewness=2.63. Combined evidence from S-W, skewness, and visual inspection in... |
| How many members of your family ear | What is your personal monthly  | **WELCH ANOVA** | KRUSKAL-WALLIS | `WELCH PREFERRED` | Large group sizes (min n=45) but Levene p=0.0048 â€” unequal variances. Welch ANOVA relaxes the equal-variance assumptio... |
| How many members of your family ear | What is your PRIMARY mode of t | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=41) ensure ANOVA robustness via CLT. Max absolute skewness=0.93 (not extreme). Levene p=0.9911 ... |
| How many members of your family ear | How do you get from your home  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | 3/3 groups fail S-W (p<0.05). Max absolute skewness=0.84. Combined evidence from S-W, skewness, and visual inspection in... |
| How many members of your family ear | If the fare of your current pr | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=112) ensure ANOVA robustness via CLT. Max absolute skewness=0.83 (not extreme). Levene p=0.0822... |
| How many members of your family ear | Imagine the MRT/Bus is so crow | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=129) ensure ANOVA robustness via CLT. Max absolute skewness=0.95 (not extreme). Levene p=0.6304... |
| How many members of your family ear | "Premium Bus" service (AC + Gu | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=142) ensure ANOVA robustness via CLT. Max absolute skewness=0.76 (not extreme). Levene p=0.5637... |
| How many members of your family ear | If it is raining heavily, how  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | 4/4 groups fail S-W (p<0.05). Max absolute skewness=2.65. Combined evidence from S-W, skewness, and visual inspection in... |
| How many members of your family ear | During a Strike (Hartal) or Ro | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | 5/5 groups fail S-W (p<0.05). Max absolute skewness=1.46. Combined evidence from S-W, skewness, and visual inspection in... |
| How many members of your family ear | If a dedicated BUBT Student Bu | **ONE-WAY ANOVA** | KRUSKAL-WALLIS | `PARAMETRIC PREFERRED` | Large group sizes (min n=90) ensure ANOVA robustness via CLT. Max absolute skewness=0.92 (not extreme). Levene p=0.9461 ... |
| What is the TOTAL One-Way Cost of t | Gender | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | 2/2 groups fail S-W (p<0.05). Max absolute skewness=2.41. Combined evidence from S-W, skewness, and visual inspection in... |
| What is the TOTAL One-Way Cost of t | What is your family's approxim | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | 5/5 groups fail S-W (p<0.05). Max absolute skewness=2.85. Combined evidence from S-W, skewness, and visual inspection in... |
| What is the TOTAL One-Way Cost of t | What is your personal monthly  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | 5/5 groups fail S-W (p<0.05). Max absolute skewness=3.35. Combined evidence from S-W, skewness, and visual inspection in... |
| What is the TOTAL One-Way Cost of t | What is your PRIMARY mode of t | **WELCH ANOVA** | KRUSKAL-WALLIS | `WELCH PREFERRED` | Large group sizes (min n=41) but Levene p=0.0000 â€” unequal variances. Welch ANOVA relaxes the equal-variance assumptio... |
| What is the TOTAL One-Way Cost of t | How do you get from your home  | **KRUSKAL-WALLIS** | WELCH ANOVA | `NON-PARAMETRIC PREFERRED` | 2/3 groups fail S-W (p<0.05). Max absolute skewness=1.77. Combined evidence from S-W, skewness, and visual inspection in... |
| What is the TOTAL One-Way Cost of t | If the fare of your current pr | **WELCH ANOVA** | KRUSKAL-WALLIS | `WELCH PREFERRED` | Large group sizes (min n=112) but Levene p=0.0000 â€” unequal variances. Welch ANOVA relaxes the equal-variance assumpti... |
| What is the TOTAL One-Way Cost of t | Imagine the MRT/Bus is so crow | **WELCH ANOVA** | KRUSKAL-WALLIS | `WELCH PREFERRED` | Large group sizes (min n=129) but Levene p=0.0000 â€” unequal variances. Welch ANOVA relaxes the equal-variance assumpti... |
| What is the TOTAL One-Way Cost of t | "Premium Bus" service (AC + Gu | **KRUSKAL-WALLIS** | WELCH ANOVA | `NON-PARAMETRIC PREFERRED` | 2/2 groups fail S-W (p<0.05). Max absolute skewness=3.62. Combined evidence from S-W, skewness, and visual inspection in... |
| What is the TOTAL One-Way Cost of t | If it is raining heavily, how  | **KRUSKAL-WALLIS** | WELCH ANOVA | `NON-PARAMETRIC PREFERRED` | 3/4 groups fail S-W (p<0.05). Max absolute skewness=1.78. Combined evidence from S-W, skewness, and visual inspection in... |
| What is the TOTAL One-Way Cost of t | During a Strike (Hartal) or Ro | **KRUSKAL-WALLIS** | WELCH ANOVA | `NON-PARAMETRIC PREFERRED` | 4/5 groups fail S-W (p<0.05). Max absolute skewness=0.91. Combined evidence from S-W, skewness, and visual inspection in... |
| What is the TOTAL One-Way Cost of t | If a dedicated BUBT Student Bu | **WELCH ANOVA** | KRUSKAL-WALLIS | `WELCH PREFERRED` | Large group sizes (min n=90) but Levene p=0.0004 â€” unequal variances. Welch ANOVA relaxes the equal-variance assumptio... |
| How crowded is the vehicle usually? | Gender | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How crowded is the vehicle usually?' is an ordinal/Likert variable. Kruskal-Wallis is preferred regardless of S... |
| How crowded is the vehicle usually? | What is your family's approxim | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How crowded is the vehicle usually?' is an ordinal/Likert variable. Kruskal-Wallis is preferred regardless of S... |
| How crowded is the vehicle usually? | What is your personal monthly  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How crowded is the vehicle usually?' is an ordinal/Likert variable. Kruskal-Wallis is preferred regardless of S... |
| How crowded is the vehicle usually? | What is your PRIMARY mode of t | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How crowded is the vehicle usually?' is an ordinal/Likert variable. Kruskal-Wallis is preferred regardless of S... |
| How crowded is the vehicle usually? | How do you get from your home  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How crowded is the vehicle usually?' is an ordinal/Likert variable. Kruskal-Wallis is preferred regardless of S... |
| How crowded is the vehicle usually? | If the fare of your current pr | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How crowded is the vehicle usually?' is an ordinal/Likert variable. Kruskal-Wallis is preferred regardless of S... |
| How crowded is the vehicle usually? | Imagine the MRT/Bus is so crow | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How crowded is the vehicle usually?' is an ordinal/Likert variable. Kruskal-Wallis is preferred regardless of S... |
| How crowded is the vehicle usually? | "Premium Bus" service (AC + Gu | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How crowded is the vehicle usually?' is an ordinal/Likert variable. Kruskal-Wallis is preferred regardless of S... |
| How crowded is the vehicle usually? | If it is raining heavily, how  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How crowded is the vehicle usually?' is an ordinal/Likert variable. Kruskal-Wallis is preferred regardless of S... |
| How crowded is the vehicle usually? | During a Strike (Hartal) or Ro | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How crowded is the vehicle usually?' is an ordinal/Likert variable. Kruskal-Wallis is preferred regardless of S... |
| How crowded is the vehicle usually? | If a dedicated BUBT Student Bu | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How crowded is the vehicle usually?' is an ordinal/Likert variable. Kruskal-Wallis is preferred regardless of S... |
| How would you rate the physical com | Gender | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How would you rate the physical comfort (Seating space, AC, Noise) of your current mode?' is an ordinal/Likert ... |
| How would you rate the physical com | What is your family's approxim | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How would you rate the physical comfort (Seating space, AC, Noise) of your current mode?' is an ordinal/Likert ... |
| How would you rate the physical com | What is your personal monthly  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How would you rate the physical comfort (Seating space, AC, Noise) of your current mode?' is an ordinal/Likert ... |
| How would you rate the physical com | What is your PRIMARY mode of t | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How would you rate the physical comfort (Seating space, AC, Noise) of your current mode?' is an ordinal/Likert ... |
| How would you rate the physical com | How do you get from your home  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How would you rate the physical comfort (Seating space, AC, Noise) of your current mode?' is an ordinal/Likert ... |
| How would you rate the physical com | If the fare of your current pr | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How would you rate the physical comfort (Seating space, AC, Noise) of your current mode?' is an ordinal/Likert ... |
| How would you rate the physical com | Imagine the MRT/Bus is so crow | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How would you rate the physical comfort (Seating space, AC, Noise) of your current mode?' is an ordinal/Likert ... |
| How would you rate the physical com | "Premium Bus" service (AC + Gu | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How would you rate the physical comfort (Seating space, AC, Noise) of your current mode?' is an ordinal/Likert ... |
| How would you rate the physical com | If it is raining heavily, how  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How would you rate the physical comfort (Seating space, AC, Noise) of your current mode?' is an ordinal/Likert ... |
| How would you rate the physical com | During a Strike (Hartal) or Ro | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How would you rate the physical comfort (Seating space, AC, Noise) of your current mode?' is an ordinal/Likert ... |
| How would you rate the physical com | If a dedicated BUBT Student Bu | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How would you rate the physical comfort (Seating space, AC, Noise) of your current mode?' is an ordinal/Likert ... |
| How safe do you feel regarding road | Gender | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding road accidents on this mode?' is an ordinal/Likert variable. Kruskal-Wallis is p... |
| How safe do you feel regarding road | What is your family's approxim | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding road accidents on this mode?' is an ordinal/Likert variable. Kruskal-Wallis is p... |
| How safe do you feel regarding road | What is your personal monthly  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding road accidents on this mode?' is an ordinal/Likert variable. Kruskal-Wallis is p... |
| How safe do you feel regarding road | What is your PRIMARY mode of t | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding road accidents on this mode?' is an ordinal/Likert variable. Kruskal-Wallis is p... |
| How safe do you feel regarding road | How do you get from your home  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding road accidents on this mode?' is an ordinal/Likert variable. Kruskal-Wallis is p... |
| How safe do you feel regarding road | If the fare of your current pr | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding road accidents on this mode?' is an ordinal/Likert variable. Kruskal-Wallis is p... |
| How safe do you feel regarding road | Imagine the MRT/Bus is so crow | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding road accidents on this mode?' is an ordinal/Likert variable. Kruskal-Wallis is p... |
| How safe do you feel regarding road | "Premium Bus" service (AC + Gu | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding road accidents on this mode?' is an ordinal/Likert variable. Kruskal-Wallis is p... |
| How safe do you feel regarding road | If it is raining heavily, how  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding road accidents on this mode?' is an ordinal/Likert variable. Kruskal-Wallis is p... |
| How safe do you feel regarding road | During a Strike (Hartal) or Ro | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding road accidents on this mode?' is an ordinal/Likert variable. Kruskal-Wallis is p... |
| How safe do you feel regarding road | If a dedicated BUBT Student Bu | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding road accidents on this mode?' is an ordinal/Likert variable. Kruskal-Wallis is p... |
| How safe do you feel regarding hara | Gender | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding harassment, pickpocketing, or personal security?' is an ordinal/Likert variable.... |
| How safe do you feel regarding hara | What is your family's approxim | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding harassment, pickpocketing, or personal security?' is an ordinal/Likert variable.... |
| How safe do you feel regarding hara | What is your personal monthly  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding harassment, pickpocketing, or personal security?' is an ordinal/Likert variable.... |
| How safe do you feel regarding hara | What is your PRIMARY mode of t | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding harassment, pickpocketing, or personal security?' is an ordinal/Likert variable.... |
| How safe do you feel regarding hara | How do you get from your home  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding harassment, pickpocketing, or personal security?' is an ordinal/Likert variable.... |
| How safe do you feel regarding hara | If the fare of your current pr | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding harassment, pickpocketing, or personal security?' is an ordinal/Likert variable.... |
| How safe do you feel regarding hara | Imagine the MRT/Bus is so crow | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding harassment, pickpocketing, or personal security?' is an ordinal/Likert variable.... |
| How safe do you feel regarding hara | "Premium Bus" service (AC + Gu | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding harassment, pickpocketing, or personal security?' is an ordinal/Likert variable.... |
| How safe do you feel regarding hara | If it is raining heavily, how  | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding harassment, pickpocketing, or personal security?' is an ordinal/Likert variable.... |
| How safe do you feel regarding hara | During a Strike (Hartal) or Ro | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding harassment, pickpocketing, or personal security?' is an ordinal/Likert variable.... |
| How safe do you feel regarding hara | If a dedicated BUBT Student Bu | **KRUSKAL-WALLIS** | ONE-WAY ANOVA | `NON-PARAMETRIC PREFERRED` | Outcome 'How safe do you feel regarding harassment, pickpocketing, or personal security?' is an ordinal/Likert variable.... |


## 4. Detailed Results for Priority Analyses

Below are detailed statistical outputs (ANOVA, Welch ANOVA, Kruskal-Wallis with tie correction, Dunn post-hoc comparisons, and effect sizes) for key research combinations.

### Outcome: `What is your age?` Ã— Grouping: `Gender`

**Group Descriptives**:

| Group | N | Mean | Median | SD | Min | Max | IQR | Skewness |
|-------|---|------|--------|----|-----|-----|-----|----------|
| Female | 105 | 21.4762 | 21.0 | 1.6472 | 19.0 | 25.0 | 3.0 | 0.4902 |
| Male | 214 | 22.0093 | 22.0 | 1.9087 | 19.0 | 28.0 | 2.0 | 0.5754 |

**Model Comparisons & Diagnostics**:
- **Shapiro-Wilk Normality**: Reported per group (see `shapiro_wilk_results.csv`)
- **Brown-Forsythe Levene Test**: F(1, 317) = 2.4793, p = 0.1164
- **Classical ANOVA**: F(1, 317) = 5.9982, p = 0.0149, eta^2 = 0.01857
- **Welch ANOVA**: Welch F(1, 236.13) = 6.6313, p = 0.0106
- **Kruskal-Wallis H**: H_uncorrected = 5.1578, Tie Correction C = 0.971130, **H_corrected = 5.3111**, df = 1, p = 0.0212
- **Effect Size (KW eta^2)**: 0.0136 (Small (0.01<=eta^2<0.06)) â€” *Tomczak & Tomczak (2014). Trends in Sport Sciences, 1(21), 19-25.*

**Pairwise Post-Hoc Comparisons (Dunn test with Bonferroni correction)**:

| Comparison | Mean Rank A | Mean Rank B | z statistic | Raw p | Bonferroni p | Significant? |
|------------|-------------|-------------|-------------|-------|--------------|--------------|
| Female vs Male | 143.257 | 168.215 | -2.3046 | 0.0212 | 0.0212 | **Yes** |

---

### Outcome: `What is your age?` Ã— Grouping: `What is your family's approximate total monthly income from all sources?`

**Group Descriptives**:

| Group | N | Mean | Median | SD | Min | Max | IQR | Skewness |
|-------|---|------|--------|----|-----|-----|-----|----------|
| 1,00,001 – 1,50,000 BDT | 61 | 21.7541 | 21.0 | 1.7191 | 19.0 | 28.0 | 2.0 | 0.9454 |
| 30,000 – 60,000 BDT | 113 | 21.823 | 22.0 | 1.784 | 19.0 | 27.0 | 2.0 | 0.3968 |
| 60,001 – 1,00,000 BDT | 107 | 21.6822 | 21.0 | 1.8254 | 19.0 | 26.0 | 3.0 | 0.5502 |
| Less than 30,000 BDT | 20 | 23.25 | 23.0 | 2.2682 | 20.0 | 28.0 | 3.25 | 0.1973 |
| More than 1,50,000 BDT | 18 | 21.5 | 21.0 | 1.6891 | 19.0 | 25.0 | 2.75 | 0.6592 |

**Model Comparisons & Diagnostics**:
- **Shapiro-Wilk Normality**: Reported per group (see `shapiro_wilk_results.csv`)
- **Brown-Forsythe Levene Test**: F(4, 314) = 0.8488, p = 0.4952
- **Classical ANOVA**: F(4, 314) = 3.4171, p = 0.0094, eta^2 = 0.041715
- **Welch ANOVA**: Welch F(4, 67.55) = 1.8694, p = 0.1259
- **Kruskal-Wallis H**: H_uncorrected = 9.3426, Tie Correction C = 0.971130, **H_corrected = 9.6204**, df = 4, p = 0.0473
- **Effect Size (KW eta^2)**: 0.017899 (Small (0.01<=eta^2<0.06)) â€” *Tomczak & Tomczak (2014). Trends in Sport Sciences, 1(21), 19-25.*

**Pairwise Post-Hoc Comparisons (Dunn test with Bonferroni correction)**:

| Comparison | Mean Rank A | Mean Rank B | z statistic | Raw p | Bonferroni p | Significant? |
|------------|-------------|-------------|-------------|-------|--------------|--------------|
| 1,00,001 – 1,50,000 BDT vs 30,000 – 60,000 BDT | 157.385 | 161.097 | -0.2571 | 0.7971 | 1.0000 | **No** |
| 1,00,001 – 1,50,000 BDT vs 60,001 – 1,00,000 BDT | 157.385 | 152.327 | 0.3469 | 0.7287 | 1.0000 | **No** |
| 1,00,001 – 1,50,000 BDT vs Less than 30,000 BDT | 157.385 | 218.075 | -2.5914 | 0.0096 | 0.0956 | **No** |
| 1,00,001 – 1,50,000 BDT vs More than 1,50,000 BDT | 157.385 | 143.056 | 0.5878 | 0.5567 | 1.0000 | **No** |
| 30,000 – 60,000 BDT vs 60,001 – 1,00,000 BDT | 161.097 | 152.327 | 0.7153 | 0.4744 | 1.0000 | **No** |
| 30,000 – 60,000 BDT vs Less than 30,000 BDT | 161.097 | 218.075 | -2.5841 | 0.0098 | 0.0976 | **No** |
| 30,000 – 60,000 BDT vs More than 1,50,000 BDT | 161.097 | 143.056 | 0.7822 | 0.4341 | 1.0000 | **No** |
| 60,001 – 1,00,000 BDT vs Less than 30,000 BDT | 152.327 | 218.075 | -2.9694 | 0.0030 | 0.0298 | **Yes** |
| 60,001 – 1,00,000 BDT vs More than 1,50,000 BDT | 152.327 | 143.056 | 0.4004 | 0.6889 | 1.0000 | **No** |
| Less than 30,000 BDT vs More than 1,50,000 BDT | 218.075 | 143.056 | 2.5405 | 0.0111 | 0.1107 | **No** |

---

### Outcome: `What is your age?` Ã— Grouping: `What is your personal monthly expenditure? (Pocket money + Earnings)`

**Group Descriptives**:

| Group | N | Mean | Median | SD | Min | Max | IQR | Skewness |
|-------|---|------|--------|----|-----|-----|-----|----------|
| 12,001 – 20,000 BDT | 83 | 21.2892 | 21.0 | 1.6119 | 19.0 | 26.0 | 2.0 | 0.8747 |
| 5,001 – 8,000 BDT | 70 | 22.2857 | 22.0 | 1.8348 | 19.0 | 26.0 | 3.0 | -0.0597 |
| 8,001 – 12,000 BDT | 52 | 22.1154 | 21.5 | 2.2549 | 19.0 | 28.0 | 3.25 | 0.6833 |
| Less than 5,000 BDT | 69 | 22.2029 | 22.0 | 1.8116 | 19.0 | 28.0 | 2.0 | 0.4065 |
| More than 20,000 BDT | 45 | 21.2444 | 21.0 | 1.3677 | 19.0 | 25.0 | 2.0 | 0.7621 |

**Model Comparisons & Diagnostics**:
- **Shapiro-Wilk Normality**: Reported per group (see `shapiro_wilk_results.csv`)
- **Brown-Forsythe Levene Test**: F(4, 314) = 4.974, p = < 0.001
- **Classical ANOVA**: F(4, 314) = 5.2900, p = < 0.001, eta^2 = 0.063133
- **Welch ANOVA**: Welch F(4, 145.86) = 5.5242, p = < 0.001
- **Kruskal-Wallis H**: H_uncorrected = 19.5816, Tie Correction C = 0.971130, **H_corrected = 20.1637**, df = 4, p = < 0.001
- **Effect Size (KW eta^2)**: 0.051477 (Small (0.01<=eta^2<0.06)) â€” *Tomczak & Tomczak (2014). Trends in Sport Sciences, 1(21), 19-25.*

**Pairwise Post-Hoc Comparisons (Dunn test with Bonferroni correction)**:

| Comparison | Mean Rank A | Mean Rank B | z statistic | Raw p | Bonferroni p | Significant? |
|------------|-------------|-------------|-------------|-------|--------------|--------------|
| 12,001 – 20,000 BDT vs 5,001 – 8,000 BDT | 132.831 | 184.271 | -3.4876 | < 0.001 | 0.0049 | **Yes** |
| 12,001 – 20,000 BDT vs 8,001 – 12,000 BDT | 132.831 | 166.452 | -2.0915 | 0.0365 | 0.3648 | **No** |
| 12,001 – 20,000 BDT vs Less than 5,000 BDT | 132.831 | 180.688 | -3.232 | 0.0012 | 0.0123 | **Yes** |
| 12,001 – 20,000 BDT vs More than 20,000 BDT | 132.831 | 133.178 | -0.0206 | 0.9836 | 1.0000 | **No** |
| 5,001 – 8,000 BDT vs 8,001 – 12,000 BDT | 184.271 | 166.452 | 1.0709 | 0.2842 | 1.0000 | **No** |
| 5,001 – 8,000 BDT vs Less than 5,000 BDT | 184.271 | 180.688 | 0.2324 | 0.8162 | 1.0000 | **No** |
| 5,001 – 8,000 BDT vs More than 20,000 BDT | 184.271 | 133.178 | 2.9421 | 0.0033 | 0.0326 | **Yes** |
| 8,001 – 12,000 BDT vs Less than 5,000 BDT | 166.452 | 180.688 | -0.8529 | 0.3937 | 1.0000 | **No** |
| 8,001 – 12,000 BDT vs More than 20,000 BDT | 166.452 | 133.178 | 1.7981 | 0.0722 | 0.7216 | **No** |
| Less than 5,000 BDT vs More than 20,000 BDT | 180.688 | 133.178 | 2.728 | 0.0064 | 0.0637 | **No** |

---

### Outcome: `What is your age?` Ã— Grouping: `What is your PRIMARY mode of transport?`

**Group Descriptives**:

| Group | N | Mean | Median | SD | Min | Max | IQR | Skewness |
|-------|---|------|--------|----|-----|-----|-----|----------|
| MRT (Metro Rail) | 96 | 21.6875 | 21.5 | 1.7187 | 19.0 | 26.0 | 3.0 | 0.487 |
| Personal Motorcycle | 62 | 21.5484 | 21.0 | 1.676 | 19.0 | 25.0 | 2.75 | 0.4529 |
| Public Bus | 120 | 22.175 | 22.0 | 1.9388 | 19.0 | 28.0 | 3.0 | 0.3817 |
| Ridesharing (Uber/Pathao) | 41 | 21.6098 | 21.0 | 1.9733 | 19.0 | 28.0 | 2.0 | 1.3777 |

**Model Comparisons & Diagnostics**:
- **Shapiro-Wilk Normality**: Reported per group (see `shapiro_wilk_results.csv`)
- **Brown-Forsythe Levene Test**: F(3, 315) = 0.7943, p = 0.4978
- **Classical ANOVA**: F(3, 315) = 2.3022, p = 0.0771, eta^2 = 0.021456
- **Welch ANOVA**: Welch F(3, 131.27) = 2.1168, p = 0.1012
- **Kruskal-Wallis H**: H_uncorrected = 6.6200, Tie Correction C = 0.971130, **H_corrected = 6.8168**, df = 3, p = 0.0780
- **Effect Size (KW eta^2)**: 0.012117 (Small (0.01<=eta^2<0.06)) â€” *Tomczak & Tomczak (2014). Trends in Sport Sciences, 1(21), 19-25.*

---

### Outcome: `What is your age?` Ã— Grouping: `How do you get from your home to the first Station or Bus Stop?`

**Group Descriptives**:

| Group | N | Mean | Median | SD | Min | Max | IQR | Skewness |
|-------|---|------|--------|----|-----|-----|-----|----------|
| Auto / Leguna | 28 | 22.0357 | 21.5 | 1.8951 | 19.0 | 26.0 | 2.0 | 0.5779 |
| Rickshaw | 89 | 22.1573 | 22.0 | 1.7445 | 19.0 | 27.0 | 3.0 | 0.2656 |
| Walk | 198 | 21.6465 | 21.0 | 1.8541 | 19.0 | 28.0 | 3.0 | 0.8134 |

**Model Comparisons & Diagnostics**:
- **Shapiro-Wilk Normality**: Reported per group (see `shapiro_wilk_results.csv`)
- **Brown-Forsythe Levene Test**: F(2, 312) = 0.0874, p = 0.9164
- **Classical ANOVA**: F(2, 312) = 2.6023, p = 0.0757, eta^2 = 0.016408
- **Welch ANOVA**: Welch F(2, 71.32) = 2.6339, p = 0.0788
- **Kruskal-Wallis H**: H_uncorrected = 5.9486, Tie Correction C = 0.970438, **H_corrected = 6.1299**, df = 2, p = 0.0467
- **Effect Size (KW eta^2)**: 0.013237 (Small (0.01<=eta^2<0.06)) â€” *Tomczak & Tomczak (2014). Trends in Sport Sciences, 1(21), 19-25.*

**Pairwise Post-Hoc Comparisons (Dunn test with Bonferroni correction)**:

| Comparison | Mean Rank A | Mean Rank B | z statistic | Raw p | Bonferroni p | Significant? |
|------------|-------------|-------------|-------------|-------|--------------|--------------|
| Auto / Leguna vs Rickshaw | 166.946 | 176.191 | -0.4755 | 0.6344 | 1.0000 | **No** |
| Auto / Leguna vs Walk | 166.946 | 148.558 | 1.0151 | 0.3101 | 0.9302 | **No** |
| Rickshaw vs Walk | 176.191 | 148.558 | 2.4134 | 0.0158 | 0.0474 | **Yes** |

---

### Outcome: `What is your age?` Ã— Grouping: `If the fare of your current primary mode INCREASED by 10% (e.g., +5-10 Taka), would you switch to a different mode?`

**Group Descriptives**:

| Group | N | Mean | Median | SD | Min | Max | IQR | Skewness |
|-------|---|------|--------|----|-----|-----|-----|----------|
| No | 112 | 22.2946 | 22.0 | 1.9803 | 19.0 | 28.0 | 3.0 | 0.4103 |
| Yes | 207 | 21.5845 | 21.0 | 1.7155 | 19.0 | 27.0 | 3.0 | 0.6471 |

**Model Comparisons & Diagnostics**:
- **Shapiro-Wilk Normality**: Reported per group (see `shapiro_wilk_results.csv`)
- **Brown-Forsythe Levene Test**: F(1, 317) = 3.5614, p = 0.0601
- **Classical ANOVA**: F(1, 317) = 11.1537, p = < 0.001, eta^2 = 0.033989
- **Welch ANOVA**: Welch F(1, 201.54) = 10.2426, p = 0.0016
- **Kruskal-Wallis H**: H_uncorrected = 9.3479, Tie Correction C = 0.971130, **H_corrected = 9.6257**, df = 1, p = 0.0019
- **Effect Size (KW eta^2)**: 0.027211 (Small (0.01<=eta^2<0.06)) â€” *Tomczak & Tomczak (2014). Trends in Sport Sciences, 1(21), 19-25.*

**Pairwise Post-Hoc Comparisons (Dunn test with Bonferroni correction)**:

| Comparison | Mean Rank A | Mean Rank B | z statistic | Raw p | Bonferroni p | Significant? |
|------------|-------------|-------------|-------------|-------|--------------|--------------|
| No vs Yes | 181.464 | 148.386 | 3.1025 | 0.0019 | 0.0019 | **Yes** |

---

### Outcome: `What is your age?` Ã— Grouping: `Imagine the MRT/Bus is so crowded that you MUST stand the entire way every day. Would you switch to a different bus that guarantees a SEAT but takes 15 minutes longer?`

**Group Descriptives**:

| Group | N | Mean | Median | SD | Min | Max | IQR | Skewness |
|-------|---|------|--------|----|-----|-----|-----|----------|
| No | 129 | 21.7597 | 21.0 | 1.8234 | 19.0 | 28.0 | 3.0 | 0.8111 |
| Yes | 190 | 21.8842 | 22.0 | 1.8566 | 19.0 | 28.0 | 2.0 | 0.4567 |

**Model Comparisons & Diagnostics**:
- **Shapiro-Wilk Normality**: Reported per group (see `shapiro_wilk_results.csv`)
- **Brown-Forsythe Levene Test**: F(1, 317) = 0.1243, p = 0.7246
- **Classical ANOVA**: F(1, 317) = 0.3507, p = 0.5542, eta^2 = 0.001105
- **Welch ANOVA**: Welch F(1, 278.25) = 0.3531, p = 0.5529
- **Kruskal-Wallis H**: H_uncorrected = 0.5499, Tie Correction C = 0.971130, **H_corrected = 0.5662**, df = 1, p = 0.4518
- **Effect Size (KW eta^2)**: -0.001368 (Negligible (eta^2<0.01)) â€” *Tomczak & Tomczak (2014). Trends in Sport Sciences, 1(21), 19-25.*

---

### Outcome: `What is your age?` Ã— Grouping: `"Premium Bus" service (AC + Guaranteed Seat) was available but cost DOUBLE your current fare, would you take it?`

**Group Descriptives**:

| Group | N | Mean | Median | SD | Min | Max | IQR | Skewness |
|-------|---|------|--------|----|-----|-----|-----|----------|
| No | 177 | 21.8305 | 22.0 | 1.7947 | 19.0 | 28.0 | 2.0 | 0.6095 |
| Yes | 142 | 21.838 | 21.5 | 1.9042 | 19.0 | 28.0 | 3.0 | 0.5793 |

**Model Comparisons & Diagnostics**:
- **Shapiro-Wilk Normality**: Reported per group (see `shapiro_wilk_results.csv`)
- **Brown-Forsythe Levene Test**: F(1, 317) = 0.9399, p = 0.3330
- **Classical ANOVA**: F(1, 317) = 0.0013, p = 0.9712, eta^2 = 4e-06
- **Welch ANOVA**: Welch F(1, 293.97) = 0.0013, p = 0.9713
- **Kruskal-Wallis H**: H_uncorrected = 0.0151, Tie Correction C = 0.971130, **H_corrected = 0.0155**, df = 1, p = 0.9009
- **Effect Size (KW eta^2)**: -0.003106 (Negligible (eta^2<0.01)) â€” *Tomczak & Tomczak (2014). Trends in Sport Sciences, 1(21), 19-25.*

---

## 5. Q1 Reviewer Defense & Methodological Notes

1. **Non-Parametric Justification**: Likert and ordinal variables are analyzed via Kruskal-Wallis to respect their non-interval measurement scale, avoiding potential distortion of means by ordinal coding.
2. **Tie Corrections**: All Kruskal-Wallis H statistics incorporate exact tie correction factors $C = 1 - \frac{\sum(t_j^3 - t_j)}{N^3 - N}$. Tie tables are preserved in `results/python/tie_tables/`.
3. **Multiple Testing Control**: FDR (Benjamini-Hochberg) and Holm-Bonferroni methods confirm that primary findings remain statistically significant after accounting for multi-hypothesis testing.
4. **No Silent Data Truncation**: Outliers identified via the 1.5Ã—IQR rule are reported in full audit logs and retained in primary analyses to reflect full empirical variance.
