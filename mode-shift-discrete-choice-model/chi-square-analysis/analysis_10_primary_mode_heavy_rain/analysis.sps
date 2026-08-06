* ==============================================================================
* Analysis 10: Primary Mode x Heavy Rain Behaviour
* ==============================================================================
* Pearson Chi-square + Monte Carlo Permutation Robustness + Cramér's V
*
* H0: Primary travel mode and heavy rain behaviour are independent.
* H1: Primary travel mode and heavy rain behaviour are associated.
*
* Author : Majharul Islam
* Date   : 2026-08-07
* SPSS   : v21+
* ==============================================================================

SET UNICODE=ON.
SET DECIMAL DOT.

* --- Load Dataset ---
GET DATA
  /TYPE = XLSX
  /FILE = '..\data\Mode_shift_bubt.xlsx'
  /SHEET = NAME 'Form Responses 3'
  /CELLRANGE = FULL
  /READNAMES = ON
  /DATATYPEMIN PERCENTAGE = 95.0
  /HIDDEN = IGNORE.
EXECUTE.
DATASET NAME ChapterFour WINDOW=FRONT.

* --- Rename variables ---
RENAME VARIABLES (V13 = PrimaryMode  V28 = HeavyRain).
EXECUTE.
* --- Cross-tabulation: Pearson Chi-square + Monte Carlo Permutation Robustness ---
CROSSTABS
  /TABLES = PrimaryMode BY HeavyRain
  /FORMAT = AVALUE TABLES
  /STATISTICS = CHISQ PHI CC
  /CELLS = COUNT EXPECTED ROW COLUMN TOTAL
  /COUNT ROUND CELL
  /METHOD = MC CIN(99) SAMPLES(99999).

* OUTPUT INTERPRETATION:
* Primary inference: Pearson Chi-Square (Asymp. Sig.).
* Robustness check: Monte Carlo Sig. column (99,999 replications).

* ==============================================================================
* END OF ANALYSIS 10
* ==============================================================================
