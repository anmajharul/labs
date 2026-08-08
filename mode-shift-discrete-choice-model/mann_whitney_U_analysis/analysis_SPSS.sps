* =============================================================================.
* analysis_SPSS.sps
* =============================================================================.
* Independent SPSS syntax for the Mann-Whitney U analysis, Chapter 4 Table 4.4.
*
* INSTRUCTIONS:
* 1. Open Mode_shift_bubt.xlsx in SPSS (File > Open > Data).
* 2. The raw column names have trailing spaces. After import, run the
*    RENAME VARIABLES block below to assign clean analysis names.
* 3. Gender is coded as string "Male" / "Female". We recode to numeric
*    1 = Male, 2 = Female for the NPAR TESTS syntax.
* 4. Run the full syntax file.
*
* Author : Majharul Islam
* Date   : 2026-08-09
* =============================================================================.

* --- Step 0: Open data --------------------------------------------------------.
* Adjust the path below to your local file location.
* GET DATA /TYPE=XLSX
*   /FILE='C:\path\to\mann_whitney_U_analysis\data\Mode_shift_bubt.xlsx'
*   /SHEET=name 'Sheet1'
*   /CELLRANGE=full
*   /READNAMES=on.

* --- Step 1: Rename raw columns to clean analysis names -----------------------.
* SPSS may import the long column headers with truncation.
* After import, verify the actual SPSS variable names using the Variable View,
* then map them below. The fragments shown are the identifying parts.
*
* These renames must match what SPSS actually imported. Adjust if needed.

* RENAME VARIABLES
*   (harassment_pickpocketing_var = security_harassment)
*   (reliable_var                = reliability)
*   (road_accidents_var          = road_accidents)
*   (comfort_var                 = comfort)
*   (crowded_var                 = crowding).

* --- Step 2: Recode Gender to numeric -----------------------------------------.
* The raw data has Gender as string "Male" / "Female".
* Mann-Whitney in SPSS requires a numeric grouping variable.

STRING Gender_clean (A10).
COMPUTE Gender_clean = LTRIM(RTRIM(Gender)).
EXECUTE.

RECODE Gender_clean ('Male'=1) ('Female'=2) INTO Gender_numeric.
VARIABLE LABELS Gender_numeric 'Gender (1=Male, 2=Female)'.
VALUE LABELS Gender_numeric 1 'Male' 2 'Female'.
EXECUTE.

* --- Step 3: Descriptive statistics -------------------------------------------.

MEANS TABLES=security_harassment reliability road_accidents
             comfort crowding BY Gender_numeric
  /CELLS MEAN MEDIAN STDDEV COUNT.

FREQUENCIES VARIABLES=security_harassment reliability road_accidents
                      comfort crowding
  /FORMAT=NOTABLE
  /STATISTICS=MEAN MEDIAN STDDEV MIN MAX
  /ORDER=ANALYSIS.

* --- Step 4: Mann-Whitney U tests (all five variables) -----------------------.
* SPSS NPAR TESTS /MANN-WHITNEY reports:
*   - Mean Rank per group
*   - Mann-Whitney U
*   - Wilcoxon W (rank sum of the smaller group)
*   - Z (with tie correction, with continuity correction by default)
*   - Asymptotic Sig. (2-tailed)
*
* IMPORTANT NOTES:
* - SPSS uses continuity correction by default in recent versions.
* - The reported U is min(U1, U2).
* - Z includes tie correction.
* - Compare the SPSS output against the Python/R results.

NPAR TESTS
  /MANN-WHITNEY = security_harassment reliability road_accidents
                  comfort crowding
    BY Gender_numeric(1 2)
  /MISSING ANALYSIS.

* --- Step 5: Descriptives split by gender -------------------------------------.

SORT CASES BY Gender_numeric.
SPLIT FILE LAYERED BY Gender_numeric.

FREQUENCIES VARIABLES=security_harassment reliability road_accidents
                      comfort crowding
  /FORMAT=NOTABLE
  /STATISTICS=MEAN MEDIAN STDDEV
  /HISTOGRAM
  /ORDER=ANALYSIS.

SPLIT FILE OFF.

* --- Step 6: Non-parametric comparison with exact test -----------------------.
* For small samples, exact test is preferred. With N=319, asymptotic is fine.
* This is included for completeness.

NPAR TESTS
  /MANN-WHITNEY = security_harassment reliability road_accidents
                  comfort crowding
    BY Gender_numeric(1 2)
  /MISSING ANALYSIS
  /METHOD=EXACT TIMER(5).

* =============================================================================.
* NOTES FOR CROSS-SOFTWARE COMPARISON:
*
* 1. SPSS reports U = min(U1, U2) by default.
* 2. SPSS Z includes tie correction automatically.
* 3. SPSS uses continuity correction (recent versions).
* 4. Compare SPSS p-value against:
*    - Python p_CC_manual (if CC matches)
*    - Python p_no_CC_manual (if no CC)
* 5. Record the exact SPSS output for the cross_software_comparison.csv.
*
* After running this syntax, manually record:
*   Variable | SPSS_U | SPSS_Z | SPSS_p
* and add to the cross_software_comparison.csv file.
* =============================================================================.
