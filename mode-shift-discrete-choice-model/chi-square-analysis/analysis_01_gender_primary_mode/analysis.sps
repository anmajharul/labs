* ==============================================================================
* Analysis 01: Gender x Primary Travel Mode
* ==============================================================================
* Pearson Chi-square + Cramér's V
*
* H0: Gender and primary travel mode are independent.
* H1: Gender and primary travel mode are associated.
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
RENAME VARIABLES (V4 = Gender  V13 = PrimaryMode).
EXECUTE.
* --- Cross-tabulation: Gender BY Primary Mode ---
CROSSTABS
  /TABLES = Gender BY PrimaryMode
  /FORMAT = AVALUE TABLES
  /STATISTICS = CHISQ PHI CC LAMBDA
  /CELLS = COUNT EXPECTED ROW COLUMN TOTAL
  /COUNT ROUND CELL.

* OUTPUT INTERPRETATION:
* Chi-Square Tests Table: Pearson Chi-Square statistic, df, Asymp. Sig. (2-sided p-value).
* Symmetric Measures Table: Phi and Cramér's V (Effect Size).
* DECISION RULE: If Asymp. Sig. < 0.05, reject H0 (significant association).

* ==============================================================================
* END OF ANALYSIS 01
* ==============================================================================
