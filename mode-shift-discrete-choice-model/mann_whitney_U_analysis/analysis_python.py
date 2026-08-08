#!/usr/bin/env python3
"""
analysis_python.py
==================
Main Mann-Whitney U reproducibility pipeline for Chapter 4, Table 4.4.
Reads raw data from Mode_shift_bubt.xlsx, performs complete analysis,
and generates all output files.

Usage:
    python analysis_python.py

Author : Majharul Islam
Date   : 2026-08-09
"""

import logging
import os
import sys

# Ensure UTF-8 output for Windows console compatibility
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
from pathlib import Path

import numpy as np
import pandas as pd

# Ensure the script's directory is on the path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from mann_whitney_utils import (
    ANALYSIS_LABELS,
    RAW_COLUMN_MAP,
    load_raw_data,
    detect_column,
    extract_gender,
    validate_data,
    format_validation_report,
    compute_mann_whitney_full,
    multiple_testing_correction,
    build_reported_vs_reproduced,
    build_descriptive_table,
    build_tie_correction_table,
    export_full_results_csv,
    export_table_4_4_csv,
    export_table_4_4_xlsx,
    generate_all_figures,
    run_all_assertions,
    format_test_results,
    build_comparison_row,
)

# ============================================================
# CONFIGURATION
# ============================================================
DATA_PATH = str(SCRIPT_DIR / "data" / "Mode_shift_bubt.xlsx")
OUTPUT_DIR = str(SCRIPT_DIR / "outputs")
FIGURES_DIR = str(SCRIPT_DIR / "figures")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            os.path.join(OUTPUT_DIR, "analysis_log.txt") if os.path.isdir(OUTPUT_DIR)
            else "analysis_log.txt",
            mode="w",
        ),
    ],
)
logger = logging.getLogger("analysis_python")


def main() -> int:
    """Run the complete Mann-Whitney U analysis pipeline."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    # Reconfigure file handler now that output dir exists
    file_handler = logging.FileHandler(
        os.path.join(OUTPUT_DIR, "analysis_log.txt"), mode="w"
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    logging.getLogger().addHandler(file_handler)

    print("=" * 70)
    print("MANN-WHITNEY U REPRODUCIBILITY PIPELINE")
    print("Chapter 4, Table 4.4: Male vs Female Comparisons")
    print("=" * 70)

    # ============================================================
    # STEP 1: Load raw data
    # ============================================================
    print("\n[STEP 1] Loading raw data...")
    df = load_raw_data(DATA_PATH)
    print(f"  Loaded: {len(df)} rows × {len(df.columns)} columns")

    # ============================================================
    # STEP 2: Data validation
    # ============================================================
    print("\n[STEP 2] Data validation...")
    gender_series = extract_gender(df)

    # Detect actual column names
    outcome_cols = {}
    for short_name in RAW_COLUMN_MAP:
        try:
            col = detect_column(df, short_name)
            outcome_cols[short_name] = col
            print(f"  Mapped: {short_name} → '{col}'")
        except ValueError as e:
            print(f"  ERROR: {e}")
            return 1

    validation = validate_data(df, outcome_cols, gender_series)
    validation_text = format_validation_report(validation)
    print(validation_text)

    # Save validation report
    with open(os.path.join(OUTPUT_DIR, "data_validation_report.txt"), "w",
              encoding="utf-8") as f:
        f.write(validation_text)

    # Check for critical issues
    if validation["missing_gender"] > 0:
        print(f"  WARNING: {validation['missing_gender']} rows with missing Gender")
    if validation["invalid_gender_codes"] > 0:
        print(f"  WARNING: {validation['invalid_gender_codes']} invalid Gender codes")

    # ============================================================
    # STEP 3-8: Mann-Whitney U calculations
    # ============================================================
    print("\n[STEPS 3-8] Computing Mann-Whitney U for all five variables...")
    gender_clean = gender_series.astype(str).str.strip()
    results = {}

    for short_name, col_name in outcome_cols.items():
        label = ANALYSIS_LABELS.get(short_name, short_name)
        print(f"\n  --- {label} ---")

        # Extract values by gender (complete cases only)
        mask_valid = gender_clean.isin(["Male", "Female"]) & df[col_name].notna()
        male_vals = pd.to_numeric(
            df.loc[mask_valid & (gender_clean == "Male"), col_name],
            errors="coerce"
        ).dropna().values.astype(float)
        female_vals = pd.to_numeric(
            df.loc[mask_valid & (gender_clean == "Female"), col_name],
            errors="coerce"
        ).dropna().values.astype(float)

        if len(male_vals) == 0 or len(female_vals) == 0:
            print(f"  ERROR: No valid data for {label}")
            return 1

        print(f"  Male N = {len(male_vals)}, Female N = {len(female_vals)}")

        res = compute_mann_whitney_full(male_vals, female_vals, label)
        results[short_name] = res

        # Print key results
        print(f"  R1 (Male) = {res['R1_male']:.1f}")
        print(f"  R2 (Female) = {res['R2_female']:.1f}")
        print(f"  R1 + R2 = {res['R1_plus_R2']:.1f} "
              f"[expected N(N+1)/2 = {res['expected_rank_sum']:.1f}] "
              f"{'✓' if res['rank_sum_identity_ok'] else '✗ FAIL'}")
        print(f"  U1 (Male) = {res['U1_male']:.1f}")
        print(f"  U2 (Female) = {res['U2_female']:.1f}")
        print(f"  U1 + U2 = {res['U1_plus_U2']:.1f} "
              f"[expected n1×n2 = {res['n1_times_n2']}] "
              f"{'✓' if res['U_identity_ok'] else '✗ FAIL'}")
        print(f"  U (min) = {res['U_min']:.1f}  [{res['U_direction']}]")
        print(f"  μ_U = {res['mu_U']:.1f}")
        print(f"  Σ(t³-t) = {res['tie_sum_t3_minus_t']:.0f}")
        print(f"  σ_U (tie-corrected) = {res['sigma_U']:.4f}")
        print(f"  Z (no CC) = {res['Z_no_CC']:.4f}")
        print(f"  Z (CC) = {res['Z_CC']:.4f}")
        print(f"  p (no CC) = {res['p_no_CC_manual']:.6f}")
        print(f"  p (CC) = {res['p_CC_manual']:.6f}")
        print(f"  SciPy p (CC) = {res.get('scipy_p_CC', 'N/A')}")
        print(f"  Effect size r = {res['effect_size_r']:.4f} "
              f"({res['effect_size_r_interpretation']})")
        print(f"  Rank-biserial r = {res['rank_biserial_signed']:.4f}")
        print(f"  Decision: {res['decision']}")

    # ============================================================
    # STEP 9: Multiple testing correction
    # ============================================================
    print("\n[STEP 9] Multiple testing correction...")
    raw_pvals = {k: v["p_no_CC_manual"] for k, v in results.items()}
    mt_results = multiple_testing_correction(raw_pvals)

    print(f"\n  {'Variable':<30} {'Raw p':>10} {'Bonferroni':>10} {'Holm':>10}")
    print(f"  {'-'*30} {'-'*10} {'-'*10} {'-'*10}")
    for var_name, mt in mt_results.items():
        label = ANALYSIS_LABELS.get(var_name, var_name)
        sig_raw = "*" if mt["significant_raw"] else ""
        sig_bonf = "*" if mt["significant_bonferroni"] else ""
        sig_holm = "*" if mt["significant_holm"] else ""
        print(f"  {label:<30} {mt['raw_p']:>9.6f}{sig_raw} "
              f"{mt['bonferroni_p']:>9.6f}{sig_bonf} "
              f"{mt['holm_p']:>9.6f}{sig_holm}")

    # Save multiple testing results
    mt_rows = []
    for var_name, mt in mt_results.items():
        mt_rows.append({
            "Variable": ANALYSIS_LABELS.get(var_name, var_name),
            **mt,
        })
    pd.DataFrame(mt_rows).to_csv(
        os.path.join(OUTPUT_DIR, "multiple_testing.csv"), index=False
    )

    # ============================================================
    # STEP 12: Reported vs reproduced
    # ============================================================
    print("\n[STEP 12] Reported vs reproduced comparison...")
    rvr_df = build_reported_vs_reproduced(results)
    rvr_df.to_csv(
        os.path.join(OUTPUT_DIR, "reported_vs_reproduced.csv"), index=False
    )
    print(rvr_df.to_string(index=False))

    # ============================================================
    # STEP 13: Automated tests
    # ============================================================
    print("\n[STEP 13] Running automated tests...")
    tests = run_all_assertions(results, mt_results)
    test_text = format_test_results(tests)
    print(test_text)

    with open(os.path.join(OUTPUT_DIR, "test_results.txt"), "w",
              encoding="utf-8") as f:
        f.write(test_text)

    # Check if any tests failed
    failed = [t for t in tests if not t["passed"]]
    if failed:
        print(f"\n*** {len(failed)} TESTS FAILED — SEE ABOVE ***")

    # ============================================================
    # STEP 14: Export all output files
    # ============================================================
    print("\n[STEP 14] Exporting output files...")

    export_full_results_csv(
        results, os.path.join(OUTPUT_DIR, "mann_whitney_full_results.csv")
    )
    export_table_4_4_csv(
        results, os.path.join(OUTPUT_DIR, "mann_whitney_table4_4.csv")
    )
    export_table_4_4_xlsx(
        results, os.path.join(OUTPUT_DIR, "Table_4_4_reproduced.xlsx")
    )

    # Descriptive statistics
    desc_df = build_descriptive_table(df, outcome_cols, gender_series)
    desc_df.to_csv(
        os.path.join(OUTPUT_DIR, "descriptive_statistics.csv"), index=False
    )

    # Tie correction details
    tie_df = build_tie_correction_table(results)
    tie_df.to_csv(
        os.path.join(OUTPUT_DIR, "tie_correction_details.csv"), index=False
    )

    # Cross-software comparison (Python-only for now)
    comparison_rows = []
    for short_name in outcome_cols:
        comparison_rows.append(
            build_comparison_row(short_name, results[short_name])
        )
    pd.DataFrame(comparison_rows).to_csv(
        os.path.join(OUTPUT_DIR, "cross_software_comparison.csv"), index=False
    )

    print("  All CSV/XLSX files exported to outputs/")

    # ============================================================
    # STEP 15: Generate figures
    # ============================================================
    print("\n[STEP 15] Generating figures...")
    try:
        generated = generate_all_figures(
            df, outcome_cols, gender_series, results, FIGURES_DIR
        )
        print(f"  Generated {len(generated)} figures in figures/")
        for f in generated:
            print(f"    → {os.path.basename(f)}")
    except ImportError as e:
        print(f"  WARNING: Could not generate figures: {e}")
        print("  Install matplotlib: pip install matplotlib")

    # ============================================================
    # FINAL SUMMARY
    # ============================================================
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    all_passed = all(t["passed"] for t in tests)
    all_match = all(
        row["Status"] in ("EXACT MATCH", "MINOR SOFTWARE DIFFERENCE")
        for _, row in rvr_df.iterrows()
    )

    if all_passed and all_match:
        print("REPRODUCIBILITY STATUS: FULLY REPRODUCIBLE")
    elif all_passed:
        print("REPRODUCIBILITY STATUS: PARTIALLY REPRODUCIBLE")
        print("(All identity checks pass, but some thesis values differ)")
    else:
        print("REPRODUCIBILITY STATUS: NOT REPRODUCIBLE")
        print("(Identity checks failed — see test results)")

    print("\nSignificant results (α = 0.05, no CC):")
    for var_name, res in results.items():
        label = ANALYSIS_LABELS.get(var_name, var_name)
        if res["significant_no_CC"]:
            print(f"  ★ {label}: U = {res['U_min']:.1f}, "
                  f"p = {res['p_no_CC_manual']:.6f}, "
                  f"r = {res['effect_size_r']:.4f}")
        else:
            print(f"    {label}: U = {res['U_min']:.1f}, "
                  f"p = {res['p_no_CC_manual']:.6f} (ns)")

    print("\nOutput directory: outputs/")
    print("Figures directory: figures/")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
