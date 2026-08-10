* ==============================================================================
* analysis.sps — Travel Cost Test Selection Analysis
* ==============================================================================
* Author : Majharul Islam (BUBT)
* Date   : 2026-08-11
* ==============================================================================

SET UNICODE=ON.
SET DECIMAL DOT.

GET DATA
  /TYPE = XLSX
  /FILE = '..\data\raw\Mode_shift_bubt.xlsx'
  /SHEET = NAME 'Form Responses 3'
  /CELLRANGE = FULL
  /READNAMES = ON.
EXECUTE.

ONEWAY OneWayCost BY PrimaryMode
  /STATISTICS HOMOGENEITY WELCH
  /POSTHOC=TUKEY GH.

NPTESTS
  /INDEPENDENT TEST (OneWayCost) GROUP(PrimaryMode) KRUSKAL_WALLIS(COMPARE=PAIRWISE).
