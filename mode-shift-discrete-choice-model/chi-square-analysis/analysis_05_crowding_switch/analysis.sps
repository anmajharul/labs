* ==============================================================================
* Analysis 05: Crowding Level x Willingness to Switch
* ==============================================================================
* Pearson Chi-square + Cramér's V (Crowding recoded Low/Moderate/High)
*
* H0: Crowding level and willingness to switch are independent.
* H1: Crowding level and willingness to switch are associated.
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
RENAME VARIABLES (V18 = Crowding  V20 = SwitchCrowding).
EXECUTE.

* Recode 5-point Likert crowding to 3 ordered groups
RECODE Crowding (1,2=1)(3=2)(4,5=3) INTO CrowdingLevel.
VALUE LABELS CrowdingLevel 1 'Low (1-2)' 2 'Moderate (3)' 3 'High (4-5)'.
EXECUTE.
* --- Cross-tabulation: Crowding Level BY Would Switch (for Guaranteed Seat) ---
CROSSTABS
  /TABLES = CrowdingLevel BY SwitchCrowding
  /FORMAT = AVALUE TABLES
  /STATISTICS = CHISQ PHI CC LAMBDA
  /CELLS = COUNT EXPECTED ROW COLUMN TOTAL
  /COUNT ROUND CELL.

* OUTPUT INTERPRETATION:
* Chi-Square Tests Table: Pearson Chi-Square statistic, df, Asymp. Sig. (2-sided p-value).
* Symmetric Measures Table: Phi and Cramér's V (Effect Size).
* DECISION RULE: If Asymp. Sig. < 0.05, reject H0 (significant association).

* ==============================================================================
* END OF ANALYSIS 05
* ==============================================================================
