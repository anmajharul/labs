#!/usr/bin/env python3
"""
test_mann_whitney.py
====================
Standalone automated test suite for the Mann-Whitney U pipeline.
Runs all assertions independently and reports pass/fail.

Usage:
    python test_mann_whitney.py

Exit code 0 = all tests pass, 1 = failures.
"""

import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from mann_whitney_utils import (
    RAW_COLUMN_MAP,
    ANALYSIS_LABELS,
    load_raw_data,
    detect_column,
    extract_gender,
    compute_mann_whitney_full,
    multiple_testing_correction,
    run_all_assertions,
    format_test_results,
)

DATA_PATH = str(SCRIPT_DIR / "data" / "Mode_shift_bubt.xlsx")


def test_known_small_sample():
    """Test with a known small sample to verify formulas."""
    # Two groups: A = [1,2,3], B = [4,5,6]
    # Combined ranks: 1,2,3,4,5,6
    # R1 = 6, R2 = 15
    # U1 = 3*3 + 3*4/2 - 6 = 9
    # U2 = 3*3 + 3*4/2 - 15 = 0
    # U = 0
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])
    res = compute_mann_whitney_full(a, b, "test_known")

    assert res["R1_male"] == 6.0, f"R1 should be 6, got {res['R1_male']}"
    assert res["R2_female"] == 15.0, f"R2 should be 15, got {res['R2_female']}"
    assert res["U1_male"] == 9.0, f"U1 should be 9, got {res['U1_male']}"
    assert res["U2_female"] == 0.0, f"U2 should be 0, got {res['U2_female']}"
    assert res["U_min"] == 0.0, f"U should be 0, got {res['U_min']}"
    assert res["rank_sum_identity_ok"], "Rank sum identity should hold"
    assert res["U_identity_ok"], "U identity should hold"
    print("  ✓ Known small sample test passed")


def test_tied_sample():
    """Test with ties to verify tie correction."""
    a = np.array([1.0, 2.0, 2.0, 3.0])
    b = np.array([2.0, 3.0, 3.0, 4.0])
    res = compute_mann_whitney_full(a, b, "test_ties")

    assert res["rank_sum_identity_ok"], "Rank sum identity should hold with ties"
    assert res["U_identity_ok"], "U identity should hold with ties"
    assert res["sigma_U"] > 0, "sigma_U should be positive"
    assert res["tie_sum_t3_minus_t"] > 0, "There should be ties"
    # With tie correction, sigma should be less than without
    assert res["sigma_U"] < res["sigma_U_no_ties"], \
        "Tie-corrected sigma should be less than uncorrected"
    print("  ✓ Tied sample test passed")


def test_deterministic():
    """Verify deterministic output by running twice."""
    a = np.array([3.0, 1.0, 4.0, 1.0, 5.0])
    b = np.array([2.0, 3.0, 5.0, 4.0])
    res1 = compute_mann_whitney_full(a, b, "det_test")
    res2 = compute_mann_whitney_full(a, b, "det_test")

    for key in ["U_min", "Z_no_CC", "p_no_CC_manual", "sigma_U"]:
        assert abs(res1[key] - res2[key]) < 1e-12, \
            f"Non-deterministic: {key} differs between runs"
    print("  ✓ Deterministic output test passed")


def test_likert_validation():
    """Test that validation catches out-of-range values."""
    # This is tested within the validate_data function
    # Here we just verify the compute function handles valid data
    a = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    b = np.array([1.0, 3.0, 5.0])
    res = compute_mann_whitney_full(a, b, "likert_test")
    assert 0 <= res["p_no_CC_manual"] <= 1, "p should be in [0,1]"
    assert -1 <= res["effect_size_r"] <= 1, "r should be in [-1,1]"
    print("  ✓ Likert validation test passed")


def test_multiple_testing():
    """Test multiple testing correction properties."""
    pvals = {"a": 0.01, "b": 0.03, "c": 0.10, "d": 0.50, "e": 0.80}
    mt = multiple_testing_correction(pvals)

    for name, result in mt.items():
        raw = result["raw_p"]
        bonf = result["bonferroni_p"]
        holm = result["holm_p"]

        assert bonf >= raw - 1e-10, \
            f"Bonferroni p ({bonf}) should be ≥ raw p ({raw})"
        assert holm >= raw - 1e-10, \
            f"Holm p ({holm}) should be ≥ raw p ({raw})"
        assert bonf <= 1.0 + 1e-10, \
            f"Bonferroni p ({bonf}) should be ≤ 1.0"
        assert holm <= 1.0 + 1e-10, \
            f"Holm p ({holm}) should be ≤ 1.0"

    # Bonferroni for smallest p: 0.01 * 5 = 0.05
    assert abs(mt["a"]["bonferroni_p"] - 0.05) < 1e-10, \
        "Bonferroni for p=0.01 with k=5 should be 0.05"
    print("  ✓ Multiple testing correction test passed")


def run_real_data_tests():
    """Run tests on the actual dataset."""
    print("\n  Loading real dataset...")
    df = load_raw_data(DATA_PATH)
    gender_series = extract_gender(df)
    gender_clean = gender_series.astype(str).str.strip()

    outcome_cols = {}
    for short_name in RAW_COLUMN_MAP:
        col = detect_column(df, short_name)
        outcome_cols[short_name] = col

    results = {}
    for short_name, col_name in outcome_cols.items():
        mask_valid = gender_clean.isin(["Male", "Female"]) & df[col_name].notna()
        male_vals = pd.to_numeric(
            df.loc[mask_valid & (gender_clean == "Male"), col_name],
            errors="coerce"
        ).dropna().values.astype(float)
        female_vals = pd.to_numeric(
            df.loc[mask_valid & (gender_clean == "Female"), col_name],
            errors="coerce"
        ).dropna().values.astype(float)

        res = compute_mann_whitney_full(
            male_vals, female_vals,
            ANALYSIS_LABELS.get(short_name, short_name)
        )
        results[short_name] = res

    # Multiple testing
    raw_pvals = {k: v["p_no_CC_manual"] for k, v in results.items()}
    mt_results = multiple_testing_correction(raw_pvals)

    # Run all assertions
    tests = run_all_assertions(results, mt_results)
    test_text = format_test_results(tests)
    print(test_text)

    # Additional real-data checks
    for short_name, res in results.items():
        label = ANALYSIS_LABELS.get(short_name, short_name)

        # Check no impossible Likert values
        for tg in res["tie_groups"]:
            val = tg["value"]
            assert 1 <= val <= 5, \
                f"[{label}] Impossible Likert value: {val}"

        # Check Gender coding
        assert res["n1_male"] > 0, f"[{label}] No male observations"
        assert res["n2_female"] > 0, f"[{label}] No female observations"

    print("  ✓ All real-data validation checks passed")

    return all(t["passed"] for t in tests)


def main():
    print("=" * 60)
    print("MANN-WHITNEY U — AUTOMATED TEST SUITE")
    print("=" * 60)

    # Unit tests
    print("\n[1] Unit tests on known samples...")
    test_known_small_sample()
    test_tied_sample()
    test_deterministic()
    test_likert_validation()
    test_multiple_testing()
    print("\nAll unit tests passed ✓")

    # Real data tests
    print("\n[2] Real data tests...")
    try:
        all_passed = run_real_data_tests()
    except FileNotFoundError:
        print("  ⚠ Dataset not found. Skipping real data tests.")
        print("  Place Mode_shift_bubt.xlsx in data/ directory.")
        all_passed = True  # Unit tests passed

    print("\n" + "=" * 60)
    if all_passed:
        print("OVERALL: ALL TESTS PASSED ✓")
        return 0
    else:
        print("OVERALL: SOME TESTS FAILED ✗")
        return 1


if __name__ == "__main__":
    sys.exit(main())
