# Reproducible Statistical Analysis Suite: University Student Mode-Shift Behavior

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-4.3%2B-276DC3?style=for-the-badge&logo=r)](https://www.r-project.org/)
[![SPSS](https://img.shields.io/badge/IBM_SPSS-v21%2B-red?style=for-the-badge&logo=ibm)](https://www.ibm.com/products/spss-statistics)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Publication Ready](https://img.shields.io/badge/Publication-Q1_Journal_Ready-orange?style=for-the-badge)](docs/chapter_4_mapping.md)

A complete, publication-ready reproducible statistical analysis repository designed for **Chapter 4** of a transportation engineering thesis. It conducts **11 statistical association analyses** examining university student mode choice and mode-shift behavior in Dhaka, Bangladesh (Case study: BUBT, Sample size $N = 319$).

Every analysis is fully synchronized to yield **identical statistical results across three major computing platforms: Python, R, and IBM SPSS Statistics**.

---

## 🌟 Key Features

* **Cross-Platform Reproducibility:** Every analysis module includes standalone scripts in **Python 3.11+**, **R 4.3+**, and **SPSS Syntax (`.sps`)** producing identical Chi-square statistics ($\chi^2$), degrees of freedom ($df$), $p$-values, and effect sizes.
* **Multi-Format Automated Exports:** Automatically exports publication-ready **APA-7 Word documents (`.docx`)**, **LaTeX `booktabs` tables (`.tex`)**, and **CSV summary files** for every analysis.
* **Exact Testing & Robustness Checks:** Automatically inspects expected cell frequencies ($E_{ij} < 5$). When assumptions are violated, it seamlessly executes **Monte Carlo Fisher-Freeman-Halton Exact Tests** ($n = 99,999$ replications, random seed = 42).
* **Bias-Corrected Effect Sizes:** Implements Bergsma (2013) bias-corrected **Cramér's V** to prevent effect size inflation in smaller contingency tables.
* **High-Resolution Figures Suite:** Generates **300 DPI PNG** and **Vector PDF** charts formatted for Q1 transportation journals (IEEE T-ITS, Elsevier, TRB).

---

## 📁 Repository Structure

```
chi-square-analysis/
├── README.md                              # Main documentation & execution guide
├── LICENSE                                # MIT License
├── requirements.txt                       # Python dependencies
├── environment.yml                        # Conda environment definition
├── .gitignore                             # Git ignore rules
├── CITATION.cff                           # Standard citation metadata file
├── chi_square_utils.py                    # Modular Python statistical & export engine
├── chi_square_utils.R                     # Modular R statistical & export engine
├── run_all_analyses.py                    # Master execution script for all 11 analyses
├── data/
│   └── Mode_shift_bubt.xlsx               # Source survey dataset (Form Responses 3, N=319)
├── docs/
│   ├── statistical_methodology.md         # Mathematical formulations & exact test guidelines
│   └── chapter_4_mapping.md               # Thesis chapter & table mapping guide
├── figures/                               # 300 DPI PNG & Vector PDF publication graphics
│   ├── fig_4_1_cramers_v_comparison.png/.pdf
│   ├── fig_4_2_mode_switch_comparison.png/.pdf
│   └── fig_analysis_01_gender_primary_mode.png/.pdf ...
├── results/                               # Master consolidated exports
│   ├── all_analyses_summary.csv           # Master summary dataset
│   └── all_analyses_summary.docx          # APA-7 Master summary table (Word)
├── analysis_01_gender_primary_mode/       # Analysis 01 Module
├── analysis_02_family_income_expenditure/ # Analysis 02 Module
├── analysis_03_family_income_primary_mode/# Analysis 03 Module
├── analysis_04_trip_purpose_primary_mode/ # Analysis 04 Module
├── analysis_05_crowding_switch/            # Analysis 05 Module
├── analysis_06_reliability_switch/         # Analysis 06 Module
├── analysis_07_travel_cost_premium_bus/    # Analysis 07 Module
├── analysis_08_primary_mode_fare_increase/# Analysis 08 Module
├── analysis_09_primary_mode_dedicated_bus/# Analysis 09 Module
├── analysis_10_primary_mode_heavy_rain/    # Analysis 10 Module
└── analysis_11_primary_mode_hartal/       # Analysis 11 Module
```

---

## 📊 Summary of 11 Statistical Analyses

| Module | Analysis Topic | Primary Test | $N$ | $\chi^2$ ($df$) | $p$-value | Cramér's V | Association / Decision |
|---|---|---|---|---|---|---|---|
| **01** | Gender × Primary Mode | Pearson $\chi^2$ | 319 | 1.9128 (3) | 0.5907 | 0.0000 | Negligible (Fail to reject $H_0$) |
| **02** | Family Income × Expenditure | Pearson $\chi^2$ | 319 | 63.3572 (16) | < 0.0001 | 0.1932 | Small (Reject $H_0$) |
| **03** | Family Income × Primary Mode | Pearson $\chi^2$ | 319 | 24.4040 (12) | 0.0179 | 0.1139 | Small (Reject $H_0$) |
| **04** | Trip Purpose × Primary Mode | Monte Carlo FFH Exact | 319 | 45.4192 (6) | 0.00001 | 0.2668 | Moderate (Reject $H_0$, MC $p=0.00001$) |
| **05** | Crowding Level × Switch (Seat) | Pearson $\chi^2$ | 319 | 64.9123 (2) | < 0.0001 | 0.4507 | Large (Reject $H_0$) |
| **06** | Reliability Level × Switch (Late) | Pearson $\chi^2$ | 319 | 35.8821 (2) | < 0.0001 | 0.3353 | Moderate (Reject $H_0$) |
| **07** | Travel Cost × Premium Bus | Pearson $\chi^2$ | 319 | 18.2341 (3) | 0.0004 | 0.2391 | Moderate (Reject $H_0$) |
| **08** | Primary Mode × Fare Increase | Pearson $\chi^2$ | 319 | 108.4102 (3) | < 0.0001 | 0.5829 | Large (Reject $H_0$) |
| **09** | Primary Mode × Dedicated Bus | Pearson $\chi^2$ | 319 | 134.8210 (3) | < 0.0001 | 0.6499 | Strongest effect (Reject $H_0$) |
| **10** | Primary Mode × Heavy Rain | Pearson $\chi^2$ + MC Perm | 319 | 42.1804 (9) | < 0.0001 | 0.2098 | Moderate (Reject $H_0$, MC $p=0.00001$) |
| **11** | Primary Mode × Strike / Hartal | Pearson $\chi^2$ | 319 | 51.6201 (12) | < 0.0001 | 0.2323 | Moderate (Reject $H_0$) |

---

## 🚀 How to Run

### Option 1: Python Master Execution (Recommended)
Run all 11 analyses, generate publication tables, and build the master summary in one command:
```powershell
cd c:\Users\ASUS\Desktop\labs\mode-shift-discrete-choice-model\chi-square-analysis
$env:PYTHONIOENCODING='utf-8'
python run_all_analyses.py
```

### Option 2: R Execution
Execute individual R scripts from your R console or RStudio:
```r
source("analysis_01_gender_primary_mode/analysis.R")
```

### Option 3: IBM SPSS Statistics Syntax
Open any `.sps` file (e.g., `analysis_01_gender_primary_mode/analysis.sps`) in IBM SPSS Statistics and execute:
```spss
Run -> All
```

---

## 🎯 Use Case & Publication Readiness

Developed for **Chapter 4** of a research thesis on **Discrete Choice Modeling and Mode-Shift Behavior**. The outputs follow strict editorial formatting required by top transportation journals:
* **IEEE Transactions on Intelligent Transportation Systems (T-ITS)**
* **Transportation Research Part A: Policy and Practice (Elsevier)**
* **Transportation Research Board (TRB) Annual Meeting**

---

# Author

**Majharul Islam**  
Civil Engineering Student  
Bangladesh University of Business and Technology (BUBT)  

**Research Focus:**  
* Transportation Engineering  
* Travel Behavior Analysis  
* Discrete Choice Modeling  

[![Portfolio](https://img.shields.io/badge/Website-anmajharul.bd-blue?style=for-the-badge&logo=googlechrome)](https://anmajharul.bd) 

© 2026 Majharul Islam – Research Portfolio
