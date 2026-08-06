* ==============================================================================
* Analysis 04: Trip Purpose x Primary Travel Mode
* ==============================================================================
* Monte Carlo Fisher-Freeman-Halton Exact Test (Chi-square assumptions violated)
*
* H0: Trip purpose and primary travel mode are independent.
* H1: Trip purpose and primary travel mode are associated.
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
RENAME VARIABLES (V12 = TripPurpose  V13 = PrimaryMode).
EXECUTE.
* --- Cross-tabulation with Monte Carlo Exact Test ---
* NOTE: Requires IBM SPSS Exact Tests add-on module.
CROSSTABS
  /TABLES = TripPurpose BY PrimaryMode
  /FORMAT = AVALUE TABLES
  /STATISTICS = CHISQ PHI CC
  /CELLS = COUNT EXPECTED ROW COLUMN TOTAL
  /COUNT ROUND CELL
  /METHOD = MC CIN(99) SAMPLES(99999).

* OUTPUT INTERPRETATION:
* The Monte Carlo p-value appears under 'Monte Carlo Sig. (2-sided)' (99,999 sampled tables).
* Use the Monte Carlo p-value as the primary inferential result when expected cell counts < 5 in >20% of cells.

* ==============================================================================
* END OF ANALYSIS 04
* ==============================================================================
