* ==============================================================================
* Analysis 06: Reliability Level x Willingness to Switch
* ==============================================================================
* Pearson Chi-square + Cramér's V (Reliability recoded Poor/Moderate/Good)
*
* H0: Reliability level and willingness to switch are independent.
* H1: Reliability level and willingness to switch are associated.
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
RENAME VARIABLES (V23 = Reliability  V22 = SwitchReliability).
EXECUTE.

* Recode 5-point Likert reliability to 3 ordered groups
RECODE Reliability (1,2=1)(3=2)(4,5=3) INTO ReliabilityLevel.
VALUE LABELS ReliabilityLevel 1 'Poor (1-2)' 2 'Moderate (3)' 3 'Good (4-5)'.
EXECUTE.
* --- Cross-tabulation: Reliability Level BY Would Switch if Unreliable ---
CROSSTABS
  /TABLES = ReliabilityLevel BY SwitchReliability
  /FORMAT = AVALUE TABLES
  /STATISTICS = CHISQ PHI CC LAMBDA
  /CELLS = COUNT EXPECTED ROW COLUMN TOTAL
  /COUNT ROUND CELL.

* OUTPUT INTERPRETATION:
* Chi-Square Tests Table: Pearson Chi-Square statistic, df, Asymp. Sig. (2-sided p-value).
* Symmetric Measures Table: Phi and Cramér's V (Effect Size).
* DECISION RULE: If Asymp. Sig. < 0.05, reject H0 (significant association).

* ==============================================================================
* END OF ANALYSIS 06
* ==============================================================================
