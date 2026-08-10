* ==============================================================================
* analysis.sps — In-Vehicle Time (min) Kruskal-Wallis H Test
* ==============================================================================
* Non-parametric comparison of In-Vehicle Time (min) across Primary Modes of transport.
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
  /K-W=InVehicleTime BY PrimaryMode_num(1 4)
  /STATISTICS=DESCRIPTIVES.

NPTESTS
  /INDEPENDENT TEST (InVehicleTime) GROUP(PrimaryMode_num) KRUSKAL_WALLIS(COMPARE=PAIRWISE).
