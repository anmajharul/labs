
* ============================================================
* CHAPTER 4 - Mann-Whitney U reproducibility syntax.
* IMPORTANT:
* 1. Open the raw dataset first, or change the GET FILE path.
* 2. Gender coding: 1=Male, 2=Female.
* 3. Replace road_accidents with the exact SPSS variable name.
* ============================================================.

* GET FILE='C:\YOUR_PATH\chapter4_raw.sav'.

TEMPORARY.
SELECT IF NOT MISSING(Gender) AND NOT MISSING(road_accidents).

NPAR TESTS
  /MANN-WHITNEY = road_accidents BY Gender(1 2)
  /MISSING ANALYSIS.

* Descriptive means/medians for direct comparison with Table 4.4.
MEANS TABLES=road_accidents BY Gender
  /CELLS MEAN MEDIAN COUNT.

* NOTE:
* SPSS reports the Mann-Whitney statistic and asymptotic significance.
* Depending on version/settings, the displayed statistic may be W/U and
* continuity/tie handling may differ from R/Python. Use the SPSS output
* as the software-specific reproducibility record, not a hard-coded number.
