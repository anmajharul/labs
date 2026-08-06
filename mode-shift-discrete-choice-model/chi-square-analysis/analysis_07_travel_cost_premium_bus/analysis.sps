* ==============================================================================
* Analysis 07: Travel Cost x Premium Bus Acceptance
* ==============================================================================
* Pearson Chi-square + Cramér's V (Cost binned: <30, 30-50, 50-70, >70 BDT)
*
* H0: Travel cost group and premium bus acceptance are independent.
* H1: Travel cost group and premium bus acceptance are associated.
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
RENAME VARIABLES (V17 = TravelCost  V21 = PremiumBus).
EXECUTE.

* Bin continuous cost into 4 groups matching Table 4.9
RECODE TravelCost (LO THRU 29.99=1)(30 THRU 50=2)(50.01 THRU 70=3)(70.01 THRU HI=4)
  INTO CostGroup.
VALUE LABELS CostGroup 1 '< 30 BDT' 2 '30-50 BDT' 3 '50-70 BDT' 4 '> 70 BDT'.
EXECUTE.
* --- Cross-tabulation: Current Travel Cost BY Would Accept Premium Bus ---
CROSSTABS
  /TABLES = CostGroup BY PremiumBus
  /FORMAT = AVALUE TABLES
  /STATISTICS = CHISQ PHI CC LAMBDA
  /CELLS = COUNT EXPECTED ROW COLUMN TOTAL
  /COUNT ROUND CELL.

* OUTPUT INTERPRETATION:
* Chi-Square Tests Table: Pearson Chi-Square statistic, df, Asymp. Sig. (2-sided p-value).
* Symmetric Measures Table: Phi and Cramér's V (Effect Size).
* DECISION RULE: If Asymp. Sig. < 0.05, reject H0 (significant association).

* ==============================================================================
* END OF ANALYSIS 07
* ==============================================================================
