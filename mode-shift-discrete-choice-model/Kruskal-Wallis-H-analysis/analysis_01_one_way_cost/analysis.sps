* ==============================================================================
* analysis.sps — One-Way Cost (BDT) Kruskal-Wallis H Test
* ==============================================================================
* Non-parametric comparison of One-Way Cost (BDT) across Primary Modes of transport.
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

AUTORECODE VARIABLES=PrimaryMode /INTO PrimaryMode_num /PRINT.

NPAR TESTS
  /K-W=OneWayCost BY PrimaryMode_num(1 4)
  /STATISTICS=DESCRIPTIVES.

NPTESTS
  /INDEPENDENT TEST (OneWayCost) GROUP(PrimaryMode_num) KRUSKAL_WALLIS(COMPARE=PAIRWISE).
